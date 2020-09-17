import sys
import csv
import requests
import os
from pathlib import Path

import convex_hull as ch
import is_georeferenced as gr

stukIds = sys.argv[1]
imageFileDirectory = sys.argv[2]
outputDirectory = sys.argv[3]

if not os.path.isfile(stukIds):
    print('No file for stukIds present ({})'.format(stukIds))

if not os.path.isdir(outputDirectory):
    os.makedirs(outputDirectory)

with open(stukIds, 'r') as idFile:
    reader = csv.reader(idFile)

    with open(outputDirectory+'/statistics.csv', 'w') as outputCsv:
        writer = csv.writer(outputCsv)
        writer.writerow(['StukId', 'Wit %', 'InVlaanderen', 'Bestandsgrootte'])
        for [id] in reader:
            print(" => Executing for id {}".format(id))

            if not os.path.isfile(imageFileDirectory+'/'+id+'.tif'):
                print("File {} not present".format(id))
                continue

            data=[id]

            print("Calculate convex hull")
            try:
                data.append(",".join(str(ch.convex_hull(imageFileDirectory+'/'+id+'.tif', debug=True)).split('.')))
            except Exception as e:
                data.append(e)

            print(" => Calculated convex hull")

            print("Calculate georefence")
            data.append(str(gr.inVlaanderen(imageFileDirectory+'/'+id+'.tif')))
            print(" => Calculated convex hull")

            print("Calculate filesize")
            data.append(str(os.path.getsize(imageFileDirectory+'/'+id+'.tif')))
            print(" => Calculated filesize")

            writer.writerow(data)
            outputCsv.flush()
