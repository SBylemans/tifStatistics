import cv2
import sys

import numpy as np

img = cv2.imread(sys.argv[1])

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray_img, 230, 255, cv2.THRESH_BINARY_INV)


img_contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
img_contours = sorted(img_contours, key=cv2.contourArea)

mask = np.zeros(img.shape[:2], np.uint8)

cv2.drawContours(mask, img_contours,-1, 255, -1)

new_img = cv2.bitwise_and(img, img, mask=mask)
cv2.imwrite(sys.argv[2], new_img)

exit()
