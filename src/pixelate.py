#!/usr/bin/env python
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

pixel_x = 10
pixel_y = 10


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


box_shape = int(input("What size pixelation would you like to create? "))

while True:
    _, frame = cap.read()
    frame = pixelate(frame, box_shape, box_shape)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
