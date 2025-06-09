#!/usr/bin/env python
import cv2
import numpy as np
import random

cap = cv2.VideoCapture(0)

grayscale_array = np.array([[[0.07, 0.72, 0.21]]])
def stipple_frame(frame, dot_size = 2, max_density = 1000):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    stippled_frame = np.ones_like(frame) * 255
    for y in range(0, frame.shape[0], dot_size):
        for x in range(0, frame.shape[1], dot_size):
            brightness = frame[y, x]
            dot_prob = 1 - (brightness / 255.0)
            if random.random() < dot_prob:
                cv2.circle(stippled_frame, (x,y), dot_size // 2, (0,0,0), -1)
    return stippled_frame


while True:
    _, frame = cap.read()
    stipple = stipple_frame(frame, dot_size=2)
    cv2.imshow('frame', stipple)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
