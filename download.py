import sys
import os


stukIds = sys.argv[1]

url = "https://dsi-oefen.omgeving.vlaanderen.be/api/fiches/stukken/{}/document"

with open(stukIds, 'r') as idFile:
    reader = csv.reader(idFile)
    for [id] in reader:
        if os.path.isfile(sys.argv[2]+'/'+id+'.tif'):
            print("File {} already retrieved".format(id))
        else:
            if not os.path.isdir(sys.argv[2]):
                os.makedirs(sys.argv[2])
            print("Retrieving {}".format(id))
            data = requests.get(url.format(id))
            if data.status_code == 200:
                print(" => Retrieved {}".format(id))
                with open(sys.argv[2]+'/'+id+'.tif', 'wb') as output:
                    output.write(data.content)
            else:
                print(" => Could not retrieve {}".format(id))
                continue
