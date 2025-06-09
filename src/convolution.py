import os
import cv2
import numpy as np
from skimage.exposure import rescale_intensity

def convolve(image, kernel):
    imgH, imgW = image.shape
    kerH, kerW = kernel.shape
    pad = (kerW - 1) // 2
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_REPLICATE)
    output = np.zeros((imgH, imgW), dtype='float32')
    for y in np.arange(pad, imgH + pad):
        for x in np.arange(pad, imgW + pad):
            roi = image[y - pad:y+pad+1, x-pad:x+pad+1]
            k = (roi * kernel).sum()
            output[y-pad, x-pad] = k
    output = rescale_intensity(output, in_range=(0,255))
    output = (output * 255).astype("uint8")
    return output

    
kernel = np.array((
    [-1, -1, -1],
    [-1, 8,-1],
    [-1, -1, -1]), dtype='int')

kernel = np.array((
    [-1, 0, 1],
    [-2, 0,2],
    [-1, 0, 1]), dtype='int')

#image = cv2.imread('/home/jordan/photos/loveless.jpg')
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frame = cv2.imread('/home/jordan/photos/loveless.jpg')
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = convolve(frame, kernel)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
