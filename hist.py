import cv2
import sys
import os
import numpy as np
import csv

def hist(dir, output=None):
    if not output is None:
        with open(output, 'w') as out:
            for f in os.listdir(dir):
                csvWriter = csv.writer(out)
                try:
                    l = __histFile(dir +'/'+ f)
                    csvWriter.writerow(l)
                    out.flush()
                except Exception as e:
                    print(e)
                    continue
    else:
        for f in os.listdir(dir):
            print(__histFile(dir +'/'+ f))

def __histFile(f):
    print(f)
    if f.endswith('.tif'):
        img = cv2.imread(f)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # white = np.where(img[:,:,1] <= 1 and img[:,:,2] >= 70)
        # print(white)
        # print(img)
        reshaped = hsv.reshape(-1, hsv.shape[-1])

        del hsv
        del img

        # Get the unique indices and their counts
        _, unq_idx, counts = np.unique(reshaped, return_index = True, return_counts=True, axis=0)
        while len(counts) > 0:
            # print((reshaped[unq_idx[np.argmax(counts)]][1]/255)*100, (reshaped[unq_idx[np.argmax(counts)]][2]/255)*100)
            if (reshaped[unq_idx[np.argmax(counts)]][1]/255)*100 <= 5 and (reshaped[unq_idx[np.argmax(counts)]][2]/255)*100 >= 50:
                break
            else:
                unq_idx = np.delete(unq_idx, np.argmax(counts))
                counts = np.delete(counts, np.argmax(counts))
        if len(counts) > 0:
            return [f, cv2.cvtColor(np.uint8([[reshaped[unq_idx[np.argmax(counts)]]]]), cv2.COLOR_HSV2RGB)[0,0]]

    return [f, None, None]

# print(__histFile(sys.argv[1]))

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        hist(sys.argv[1], sys.argv[2])
    else:
        hist(sys.argv[1])
