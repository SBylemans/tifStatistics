import gdal
import sys

from gdalconst import GA_ReadOnly

def inVlaanderen(filename):
    data = gdal.Open(filename, GA_ReadOnly)
    geoTransform = data.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1] * data.RasterXSize
    miny = maxy + geoTransform[5] * data.RasterYSize
    vlaanderen = [9928.000000, 66928.000000, 272072.000000, 329072.000000]

    return minx > vlaanderen[0] and miny > vlaanderen[1] and maxx < vlaanderen[2] and maxy < vlaanderen[3]
