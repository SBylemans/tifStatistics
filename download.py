import sys
import os
import csv
import requests

def download(url, token = None):
    stukIds = sys.argv[1]

    with open(stukIds, 'r') as idFile:
        reader = csv.reader(idFile)
        for [id] in reader:
            if os.path.isfile(sys.argv[2]+'/'+id+'.tif'):
                print("File {} already retrieved".format(id))
            else:
                if not os.path.isdir(sys.argv[2]):
                    os.makedirs(sys.argv[2])
                print("Retrieving {}".format(id))
                if token is None:
                    data = requests.get(url.format(id))
                else:
                    data = requests.get(url.format(id), headers={"openamssoid": token})
                if data.status_code == 200:
                    print(" => Retrieved {}".format(id))
                    with open(sys.argv[2]+'/'+id+'.tif', 'wb') as output:
                        output.write(data.content)
                else:
                    print(" => Could not retrieve {}".format(id))
                    continue

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] Geef file mee voor ids")
        exit()
    if len(sys.argv) < 3:
        print("[ERROR] Geef directory mee voor bestanden in op te slaan")
        exit()
    dsiOrDspace = input("Data halen van DSI of DSPACE (DSI, DSPACE): ")
    while not (dsiOrDspace == 'DSPACE' or dsiOrDspace == "DSI"):
        if dsiOrDspace == 'quit':
            exit()
        dsiOrDspace = input("Ongeldige keuze: ")
    if dsiOrDspace == 'DSI':
        download("https://dsi-oefen.omgeving.vlaanderen.be/api/fiches/stukken/{}/document")
    if dsiOrDspace == 'DSPACE':
        token = input("Enter production token: ")
        download("http://archief-algemeen-pr-757.lb.cumuli.be:8080/rest/api/bitstreams/{}/retrieve", token)
