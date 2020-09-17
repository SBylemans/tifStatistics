import cv2
import sys
import scipy.cluster.hierarchy as hcluster
import os

import numpy as np

def convex_hull(input, imageOutput = None, debug = False):

    THRESHOLD = 230

    if debug:
        print(" - Reading image")

    img = cv2.imread(input)

    if img is None:
        return "Could not read file"

    if debug:
        print(" - Threshold")

    split_input = input.split('.')
    mask_filename = ".".join([split_input[i] for i in range(len(split_input)-1)]) + '.mask.npy'

    if os.path.isfile(mask_filename):
        if debug:
            print(" - Read mask")
        mask = np.load(mask_filename)
    else:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_img, THRESHOLD, 255, cv2.THRESH_BINARY_INV)


        if debug:
            print(" - Find contours")

        img_contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
        img_contours = sorted(img_contours, key=cv2.contourArea)

        #enkel significante contouren behouden
        img_contours = [c for c in img_contours if cv2.contourArea(c) > 100]

        contour_dict = {}

        contour_centers = []

        if debug:
            print(" - Cluster contours")

        clusters = None
        try:
            # loop over the contours
            if len(img_contours) > 1:
                for c in img_contours:
                    # compute the center of the contour
                        M = cv2.moments(c)
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        contour_centers.append([cX,cY])

                c_thresh = 250
                clusters = hcluster.fclusterdata(contour_centers, c_thresh, criterion="distance")
            else:
                cont = np.vstack(list(img_contours[i] for i in range(len(img_contours))))

        except ZeroDivisionError:
            if debug:
                print(" - Cluster contours (Failed)")
            cont = np.vstack(list(img_contours[i] for i in range(len(img_contours))))

        mask = np.zeros(img.shape[:2], np.uint8)
        if clusters is not None:
            for cluster in np.unique(clusters):
                cont = np.vstack(list(c for (i,c) in enumerate(img_contours) if clusters[i] == cluster))
                hull = cv2.convexHull(cont)
                cv2.drawContours(mask, [hull],-1, 255, -1)
        else:
            hull = cv2.convexHull(cont)
            cv2.drawContours(mask, [hull],-1, 255, -1)

        np.save(mask_filename, mask)
        del gray_img, thresh, img_contours

    if debug:
        print(" - Calculate white (%)")

    not_masked = np.nonzero(mask)

    white_points = 0
    points = len(img[not_masked])

    threshImage = img[not_masked] - [THRESHOLD,THRESHOLD,THRESHOLD]

    white_points = np.count_nonzero((threshImage >= [0,0,0]).all(axis=1))

    if imageOutput is not None:
        if debug:
            print(" - Save image")
        new_img = cv2.bitwise_and(img, img, mask=mask)
        cv2.imwrite(imageOutput, new_img)

    del mask, threshImage

    return (white_points/points)*100

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        print(convex_hull(sys.argv[1], sys.argv[2], sys.argv[3]))
    else:
        print(convex_hull(sys.argv[1], sys.argv[2]))
