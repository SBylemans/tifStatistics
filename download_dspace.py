import sys
import os
import requests
import csv

def process_data(data, writeMode):
    with open(sys.argv[1], writeMode) as outputCsv:
        writer = csv.writer(outputCsv)
        for id in [b['id'] for d in data for b in d['bitstreams'] if b['format'] == 'TIFF']:
            writer.writerow([str(id)])
            outputCsv.flush()


# stukIds = sys.argv[1]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] Geef file mee voor ids")
        exit()

    list_url = "http://archief-algemeen-pr-757.lb.cumuli.be:8080/rest/api/search/item?fields=dc.identifier:uitsnede&expand=bitstreams&offset={}&limit={}"
    limit = 100
    offset = 0

    token = input("Enter production token: ")

    data = requests.get(list_url.format(offset, limit), headers={"openamssoid": token})
    process_data(data.json(), "w")
    while data.status_code == 200 and len(data.json()) == limit:
        offset = offset + limit
        print('Retrieving offset {}'.format(offset))
        data = requests.get(list_url.format(offset, limit), headers={"openamssoid": token})
        process_data(data.json(), "a+")

# with open(stukIds, 'r') as idFile:
#     reader = csv.reader(idFile)
#     for [id] in reader:
#         if os.path.isfile(sys.argv[2]+'/'+id+'.tif'):
#             print("File {} already retrieved".format(id))
#         else:
#             if not os.path.isdir(sys.argv[2]):
#                 os.makedirs(sys.argv[2])
#             print("Retrieving {}".format(id))
#             data = requests.get(url.format(id))
#             if data.status_code == 200:
#                 print(" => Retrieved {}".format(id))
#                 with open(sys.argv[2]+'/'+id+'.tif', 'wb') as output:
#                     output.write(data.content)
#             else:
#                 print(" => Could not retrieve {}".format(id))
#                 continue
