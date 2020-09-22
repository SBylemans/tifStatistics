from PIL import Image
import cv2
import sys
import os

for f in os.listdir(sys.argv[1]):
    try:
        image = cv2.imread(sys.argv[1]+"/"+f)
        width, height,_ = image.shape
        print(((4*width)*(height-1))+(4*width))
        if(((4*width)*(height-1))+(4*width) > 2147483647):
            print(f, width, height)
    except Exception as e:
        continue
