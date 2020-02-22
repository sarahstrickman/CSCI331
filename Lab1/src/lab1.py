import sys
import PIL
import math
from src.util import *

map = []

'''
Process the elevation map. This is the first function run, and is responsible 
for creating the mapPoints and populating the map. 
'''
def processElevation(elevationFileName : str):
    global map
    f = open(elevationFileName)
    i = 0   # line number
    for line in f:
        map.append([])
        points = line.split()
        j = 0
        for item in points:
            # initialize all points with their elevation. -1 == uninitialized MapPoint attribute.
            map[i].append(MapPoint(PIXELMETERS_X * i, PIXELMETERS_Y * j, float(item), ""))
        i += 1
    f.close()


def processTerrains(terrainimg : str):
    pass

'''
Given a file containing the path, make a list of points that you're travelling to.

pathFileName : the filename of the file containing path points/data
return : a list of MapPoint objects. This is the path of points to pass through.
'''
def processPath(pathFileName : str):
    path = []
    with open(pathFileName) as f:
        for line in f:
            coords = line.split()
            # n_point = map[int(coords[0])][int(coords[1])]
            n_point = MapPoint(int(coords[0]) * PIXELMETERS_X, int(coords[1]) * PIXELMETERS_Y, 0, "")

    return path

'''
Handles argument things. Differs execution of the image processing and A* to other functions.
'''
def main():
    if len(sys.argv) != 6:
        print("Usage :\n\t$python3 lab1.py terrain.png mpp.txt red.txt winter redWinter.png")

    terrain_map = sys.argv[1]
    elevation_file = sys.argv[2]
    path_file = sys.argv[3]
    season = ""
    if sys.argv[4].lower() in SEASONS:  # it's gotta be a valid season, bro.
        season = sys.argv[4].lower()
    else:
        print("invalid season. Season must be [spring, summer, fall, winter]")
        sys.exit( 1 )
    output_filename = sys.argv[5]

    processElevation(elevation_file)


if __name__ == "__main__":
    main()