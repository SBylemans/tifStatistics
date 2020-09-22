from PIL import Image
import cv2
import sys
import os
import csv

def size(dir, output_dir = None):
    list = []
    for f in os.listdir():
        try:
            image = cv2.imread(dir+"/"+f)
            width, height,_ = image.shape
            list.append(f, width, height, ((4*width)*(height-1))+(4*width) > 2147483647)
        except Exception as e:
            continue
    if output_dir is None:
        return list
    else:
        with open(output_dir+'/statistics.csv', 'w') as outputCsv:
            writer = csv.writer(outputCsv)
            for l in list:
                writer.writerow(l)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] Geef file mee voor ids")
        exit()
    if len(sys.argv) < 3:
        for (f, w, h, bt) in size(sys.argv[1]):
            print(f,w,h,bt)
    else:
        size(sys.argv[1], sys.argv[2])
