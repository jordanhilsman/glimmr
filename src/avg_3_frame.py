#!/usr/bin/env python
import cv2
import numpy as np

write_to_vid = True
cap = cv2.VideoCapture(0)

diff1 = 0
diff2 = 0


def glitch(frame, intensity):
    h, w, _ = frame.shape
    for _ in range(intensity):
        x = np.random.randint(1, w)
        y = np.random.randint(1, h)
        frame[:, x:] = frame[:, :-x]
        frame[y:, :] = frame[:-y, :]
    return frame


images = []
while True:
    _, frame = cap.read()
    _, frame2 = cap.read()
    _, frame3 = cap.read()
    diff1 += (frame - frame2) / 600
    diff2 += (frame2 - frame3) / 600
    diff1_flat = frame - frame2
    diff2_flat = frame2 - frame3
    if (np.max(np.max(diff1)) > 475) | (np.max(np.max(diff2)) > 475):
        diff1, diff2 = 0
    frame = np.stack([frame, (frame2 * diff1_flat) ** diff1, (frame3 * diff2_flat) ** diff2])
    frame = np.mean(frame, axis=0)
    #    intense = np.random.randint(1,4)
    #    frame = glitch(frame, intense)
    cv2.imshow("frame", frame)
    images.append(frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

if write_to_vid:
    print("Writing to video")
    #    video = cv2.VideoWriter('ascii.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))
    #    video.fourcc(*'H264')
    video = cv2.VideoWriter("average.avi", cv2.VideoWriter_fourcc(*"XVID"), 30, (640, 480))
    for image in images:
        video.write(image)


cap.release()
cv2.destroyAllWindows()
