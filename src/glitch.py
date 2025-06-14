#!/usr/bin/env python
import numpy as np
import cv2


def glitch(frame, intensity):
    h, w, _ = frame.shape
    for _ in range(intensity):
        x = np.random.randint(1, w)
        y = np.random.randint(1, h)
        frame[:, x:] = frame[:, :-x]
        frame[y:, :] = frame[:-y, :]
    return frame


def glitch_color(frame, intensity):
    h, w, _ = frame.shape
    r = frame[:, :, 0]
    g = frame[:, :, 1]
    b = frame[:, :, 2]
    for _ in range(intensity):
        x = np.random.randint(1, w)
        y = np.random.randint(1, h)
        frame[:, x:, 0] = frame[:, :-x, 1]
        frame[:, :-x, 2] = r[:, x:]
        frame[y:, :, 1] = frame[:-y, :, 2]
    return frame


def main():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        intense = np.random.randint(1, 5)
        glitch_frame = glitch(frame, intense)
        # glitch_frame = glitch_color(frame, intense)
        cv2.imshow("frame", glitch_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
