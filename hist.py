import cv2
import sys
import os
import numpy as np
import csv

def hist(dir, output=None):
    if not output is None:
        with open(output, 'w') as out:
            csvWriter = csv.writer(out)
            csvWriter.writerow(['File', 'Color', 'Color Percentage Above Sat. Thresh.'])
            for f in os.listdir(dir):
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

        reshaped = hsv.reshape(-1, hsv.shape[-1])

        del hsv
        del img

        # Get the unique color indices and their counts
        _, unq_idx, counts = np.unique(reshaped, return_index = True, return_counts=True, axis=0)

        condition = np.where((reshaped[unq_idx][:,1].astype(np.int32) * reshaped[unq_idx][:,2].astype(np.int32)) > 2500)

        return [f, __getWhiteBand(reshaped, counts, unq_idx), np.sum(counts[condition[0]])/np.sum(counts)]

def __getWhiteBand(img, count_array, idx_array):
    while len(count_array) > 0:
        if (img[idx_array[np.argmax(count_array)]][1]/255)*100 <= 5 and (img[idx_array[np.argmax(count_array)]][2]/255)*100 >= 50:
            break
        else:
            idx_array = np.delete(idx_array, np.argmax(count_array))
            count_array = np.delete(count_array, np.argmax(count_array))
    if len(count_array) > 0:
        return cv2.cvtColor(np.uint8([[img[idx_array[np.argmax(count_array)]]]]), cv2.COLOR_HSV2RGB)[0,0]

    return None

# print(__histFile(sys.argv[1]))

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        hist(sys.argv[1], sys.argv[2])
    else:
        hist(sys.argv[1])
