from PIL import Image
import cv2
import sys
import os
import csv

def size(dir, output_file = None):
    list = []
    for f in os.listdir(dir):
        try:
            image = cv2.imread(dir+"/"+f)
            width, height, depth = image.shape
            list.append([f, width, height, depth])
        except Exception as e:
            list.append([f, "", "", ""])
            continue
    if output_file is None:
        return list
    else:
        with open(output_file, 'w') as outputCsv:
            writer = csv.writer(outputCsv)
            for l in list:
                writer.writerow(l)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] Geef file mee voor ids")
        exit()
    if len(sys.argv) < 3:
        for (f, w, h, d) in size(sys.argv[1]):
            print(f,w,h,d)
    else:
        size(sys.argv[1], sys.argv[2])
