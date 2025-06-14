#!/usr/bin/env python
import cv2
import random
import numpy as np
import os

write_to_vid = True
images = []
cap = cv2.VideoCapture(0)


def glitch(frame, intensity):
    h, w, _ = frame.shape
    for _ in range(intensity):
        x = np.random.randint(1, w)
        y = np.random.randint(1, h)
        frame[:, x:] = frame[:, :-x]
        frame[y:, :] = frame[:-y, :]
    return frame


while True:
    _, frame = cap.read()
    _, frame2 = cap.read()
    diff1_flat = frame - frame2
    frame = cv2.GaussianBlur(diff1_flat, (5, 5), 0)
    #    frame_2 = frame[:,:,1]
    #    frame_1 = frame[:,:,0]
    #    frame[:,:,0]=frame_2
    #    frame[:,:,1] = frame_1
    cv2.imshow("frame", frame)
    images.append(frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

if write_to_vid:
    print("Writing to video")
    #    video = cv2.VideoWriter('ascii.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))
    #    video.fourcc(*'H264')
    video = cv2.VideoWriter("gauss.avi", cv2.VideoWriter_fourcc(*"XVID"), 30, (640, 480))
    for image in images:
        video.write(image)


cap.release()
cv2.destroyAllWindows()
