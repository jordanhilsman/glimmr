#!/usr/bin/env python
import random
import numpy as np
import cv2
import os
import argparse
import time

# DIMS: 1080, 1920


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-wp", "--write_path", type=str, help="Write path for video", required=True)
    parser.add_argument("-ip", "--image_path", type=str, help="Image path for video", required=True)
    return parser.parse_args()


args = parse_args()

print(args.image_path)
image_choices = [fp for fp in os.listdir(args.image_path) if fp.endswith("JPG")]
print(len(image_choices))
video_path = args.write_path
im_choice = random.choice(image_choices)
image_path = os.path.join(args.image_path, im_choice)

im1 = cv2.imread(image_path)
height, width, _ = im1.shape
images = [im1]

pixel_x = 10
pixel_y = 10

cap = cv2.VideoCapture(0)


def stipple_frame(frame, dot_size=2, max_density=1000):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    stippled_frame = np.ones_like(frame) * 255
    for y in range(0, frame.shape[0], dot_size):
        for x in range(0, frame.shape[1], dot_size):
            brightness = frame[y, x]
            dot_prob = 1 - (brightness / 255.0)
            if random.random() < dot_prob:
                cv2.circle(stippled_frame, (x, y), dot_size // 2, (0, 0, 0), -1)
    return stippled_frame


def glitch(frame, intensity):
    h, w, _ = frame.shape
    for _ in range(intensity):
        x = np.random.randint(1, w)
        y = np.random.randint(1, h)
        frame[:, x:] = frame[:, :-x]
        frame[y:, :] = frame[:-y, :]
    return frame


def pixelate(frame, px=pixel_x, py=pixel_y):
    cur_x = 0
    cur_y = 0
    h, w, _ = frame.shape
    if (h % px != 0) | (w % py != 0):
        raise ValueError("Dimensions of image are not compatible with pixelation selection")
    while cur_x < w:
        while cur_y < h:
            block = frame[cur_y : cur_y + px, cur_x : cur_x + py]
            block_mean = np.mean(block, axis=(0, 1))
            frame[cur_y : cur_y + py, cur_x : cur_x + px] = block_mean
            cur_y += py
        cur_y = 0
        cur_x += px
    return frame


def glitch_color(frame, intensity):
    h, w, _ = frame.shape
    r = frame[:, :, 0]
    g = frame[:, :, 1]
    b = frame[:, :, 2]
    for _ in range(intensity):
        x = np.random.randint(1, w)
        y = np.random.randint(1, h)
        ph = frame
        frame[:, x:, 0] = frame[:, :-x, 1]
        frame[:, :-x, 2] = r[:, x:]
        frame[y:, :, 1] = frame[:-y, :, 2]
    return frame


mod = input("What would you like to do to this image? ")
if mod.lower() in ["pixelate", "pixel"]:
    modify = "pixel"
    box_shape = int(
        input(
            f"What size pixelation would you like? Note the dimensions of this image are {height}, {width}. "
        )
    )
elif mod.lower() == "glitch":
    modify = "glitch"
elif mod.lower() in ["glitch_color", "glitch color"]:
    modify = "glitch_color"
elif mod.lower() == "pointillism":
    modify = "point"
elif mod.lower() == "glitch_point":
    modify = "gp"

last_read = time.time()
read_interval = 0.7

while True:
    current_time = time.time()
    print(current_time)
    if current_time - last_read >= read_interval:
        image_path = os.path.join(args.image_path, random.choice(image_choices))
        last_read = current_time
    frame = cv2.imread(image_path)
    if (modify == "glitch") | (modify == "glitch_color"):
        intense = np.random.randint(1, 5)
        if modify == "glitch":
            new_frame = glitch(frame, intense)
        elif modify == "glitch_color":
            new_frame = glitch_color(frame, intense)
    elif modify == "pixel":
        new_frame = pixelate(frame, box_shape, box_shape)
    elif modify == "point":
        new_frame = stipple_frame(frame)
    elif modify == "gp":
        intense = np.random.randint(1, 10)
        f1 = glitch_color(frame, intense)
        new_frame = stipple_frame(frame)
    images.append(new_frame)
    cv2.imshow("frame", new_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

print("Writing to video")
video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"mp4v"), 15, (width, height))
video.fourcc(*"H264")

for image in images:
    video.write(image)

cap.release()
cv2.destroyAllWindows()
video.release
