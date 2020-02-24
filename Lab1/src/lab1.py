import sys
from PIL import Image
import math
from src.util import *

map = []


'''
f = g + h
g = accumulative cost to move (from start)
h = heuristic (lower == better)
'''
def a_star(startpoint : MapPoint, endPoint : MapPoint):

    done = False

    frontier = dict()       # (MapPoint : int)
    closed = dict()     # (MapPoint : int)
    parents = dict()    # (MapPoint : MapPoint)
    startpoint = startpoint.toString()
    parents[startpoint] = None
    frontier[startpoint] = 0 #getTime(startpoint, endPoint) + heuristicFunction(startpoint, endPoint)
    keyList = list(frontier.keys())
    while len(keyList) > 0:
        chosen_st = keyList[0]         # chosen    = node with smallest f
        smallest = frontier[chosen_st]     # smallest  = smallest f
        for item in keyList:
            if frontier[item] < smallest:
                smallest = frontier[item]
        print(item, " : ", frontier[item])
        # smallest will now be a number corresponding to the smallest f
        # in the frontier keys.

        # take the smallest value out of the frontier dictionary
        # del frontier[chosen_st]
        frontier.pop(chosen_st)
        print(chosen_st)
        chosen = fromString(chosen_st)
        #chosen.isSolution = True
        neighbors = getNeighbors(chosen)
        parent_g = smallest - heuristicFunction(chosen, endPoint)       # g = f - h
        if chosen_st == endPoint.toString():
            break
        for n in neighbors:
            # print(chosen_st, " : ", n.toString())

            succ_g = getTime(chosen, n)
            succ_h = heuristicFunction(n, endPoint)
            succ_f = (parent_g + succ_g) + succ_h

            toSkip = False
            if TERRAINS[n.terrain] == 0.0:
                toSkip = True
            if n.toString() in closed.keys():
                toSkip = True
            if toSkip == False:
                parents[n.toString()] = chosen
                frontier[n.toString()] = succ_f
                closed[n.toString()] = succ_f
        closed[chosen_st] = smallest
        keyList = list(frontier.keys())
        print(len(keyList))

    backTrace = endPoint

    if endPoint.toString() not in parents.keys():
        return 0
    tt = 0
    dist = 0
    while backTrace != None and parents[backTrace.toString()] != None:
        backTrace.isSolution = True

        print(backTrace)
        dist += heuristicFunction(backTrace, parents[backTrace.toString()])
        backTrace = parents[backTrace.toString()]
        tt+=1
    return dist


def a_star_path(path):
    # print(path)
    i = 0
    dist = 0.0
    while i < len(path) - 1:
        dist += a_star(path[i], endPoint=path[i + 1])
        i += 1
        if dist == 0:
            print("No solution found")
            return
    print(dist)

'''
Process the map during the spring.
'''
def processSpring():
    global map
    border_land_pixels = []
    visited = dict()  # set of all explored nodes
    for x in range(len(map)):
        for y in range(len(map[x])):
            p = map[x][y]
            # print(p.toString())
            if p.terrain == "WATER":
                n = getNeighbors(p)
                for item in n:
                    if item.terrain != "WATER":
                        border_land_pixels.append(item)
    iteration = 0
    waterheight = border_land_pixels[0].z
    while iteration < 15:
        frontier = list()
        for idx in range(len(border_land_pixels)):
            border_land_pixels[idx].terrain = "MUD"
            neighbors = getNeighbors(border_land_pixels[idx])
            for n in neighbors:
                visited[border_land_pixels[idx].toString()] = border_land_pixels[idx]
                if (n.terrain == "WATER") or (n.terrain == "OUT_OF_BOUNDS") or\
                          (n.toString() in visited):  # ((n.z - waterheight) > 1.0) or
                    pass
                # elif ((n.z - waterheight) > 1.0):
                #     print(n.z - waterheight)
                else:
                    frontier.append(n)
        border_land_pixels = frontier
        iteration += 1

'''
Process the map during the winter.
'''
def processWinter():
    global map
    border_water_pixels = []
    visited = dict()     # set of all explored nodes
    for x in range(len(map)):
        for y in range(len(map[x])):
            p = map[x][y]
            if p.terrain == "WATER":
                n = getNeighbors(p)
                for item in n:
                    if item.terrain != "WATER":
                        border_water_pixels.append(p)
                        break
    iteration = 0
    while iteration < 7:
        frontier = list()
        for idx in range(len(border_water_pixels)):
            border_water_pixels[idx].terrain = "ICE"
            neighbors = getNeighbors(border_water_pixels[idx])
            for n in neighbors:
                visited[border_water_pixels[idx].toString()] = border_water_pixels[idx]
                if (n.terrain != "WATER") or (n.toString() in visited):
                    pass
                else:
                    frontier.append(n)
        border_water_pixels = frontier
        iteration += 1

'''
Process the map during the fall.
'''
def processFall():
    global map
    affectedPixels = []
    for x in range(len(map)):
        for y in range(len(map[x])):
            p = map[x][y]
            if p == "FOOTPATH":
                if (p.x > 0) and (map[x - 1][y].terrain == "FOREST_EASY_MOVEMENT"):    # check pixel above p
                    affectedPixels.append(p)
                elif (p.x < (len(map) - 1)) and (map[x + 1][y].terrain) == "FOREST_EASY_MOVEMENT": # check pixel below p
                    affectedPixels.append(p)
                elif (p.y > 0) and (map[x][y - 1].terrain == "FOREST_EASY_MOVEMENT"):    # check pixel left of p
                    affectedPixels.append(p)
                elif (p.y < (len(map[x]) - 1)) and (map[x][y + 1].terrain == "FOREST_EASY_MOVEMENT"): # check pixel right of p
                    affectedPixels.append(p)
                elif p.x > 0 and p.y > 0 and map[x - 1][y - 1] == "FOREST_EASY_MOVEMENT": # check top left
                    affectedPixels.append(p)
                elif p.x > 0 and p.y < len(map[x]) and map[x - 1][y + 1] == "FOREST_EASY_MOVEMENT":   # check top right
                    affectedPixels.append(p)
                elif p.x < len(map) and p.y > 0 and map[x + 1][y - 1] == "FOREST_EASY_MOVEMENT":  # check bot left
                    affectedPixels.append(p)
                elif p.x < len(map) and p.y < len(map[x]) and map[x + 1][y + 1] == "FOREST_EASY_MOVEMENT":  # check bot right
                    affectedPixels.append(p)
    for item in affectedPixels:
        item.terrain = "FOOTPATH_FALL"

#########

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
            # initialize all points with their location.
            # By default, all points are out of bounds. This will be initialized in processTerrains().
            map[i].append(MapPoint(PIXELMETERS_X * i, PIXELMETERS_Y * j, float(item), "OUT_OF_BOUNDS", False))
            j += 1
        i += 1
    f.close()

'''
Process the terrains for the map. Given an image filename, assign terrains to the pre-existing MapPoints.
'''
def processTerrains(terrainimg : str):
    global map
    im = Image.open(terrainimg)
    px = im.load()
    width, height = im.size
    for x in range(width):
        for y in range(height):
            rgba = im.getpixel((x, y))
            r = rgba[0]
            g = rgba[1]
            b = rgba[2]
            if (r, g, b) in TERRAINCOLORS:
                map[y][x].terrain = TERRAINCOLORS[(r, g, b)]
    im.close()

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
            n_point = map[int(coords[1])][int(coords[0])]
            path.append(n_point)
    f.close()
    return path

#########

'''
Get all of the neighbors of a point.
'''
def getNeighbors(p : MapPoint):
    ix = int(p.x / PIXELMETERS_X)
    iy = int(p.y / PIXELMETERS_Y)
    neighbors = []
    # if ix > 0 and iy > 0:                                     # check top left
    #     neighbors.append(map[ix - 1][iy - 1])
    # if ix > 0 and iy < len(map[ix]):                          # check top right
    #     neighbors.append(map[ix - 1][iy + 1])
    # if ix < len(map) and iy > 0:                              # check bot left
    #     neighbors.append(map[ix + 1][iy - 1])
    # if ix < len(map) and iy < len(map[ix]):                   # check bot right
    #     neighbors.append(map[ix + 1][iy + 1])
    if (ix > 0):                                               # check pixel above p
       neighbors.append(map[ix - 1][iy])
    if (ix < (len(map) - 1)):                                  # check pixel below p
        neighbors.append(map[ix + 1][iy])
    if (iy > 0):                                               # check pixel left of p
        neighbors.append(map[ix][iy - 1])
    if (iy < (len(map[ix]) - 1)):                              # check pixel right of p
        neighbors.append(map[ix][iy + 1])
    return neighbors

def fromString(code : str):
    splitter = code.split(";")
    ix = int(float(splitter[0]) / PIXELMETERS_X)
    iy = int(float(splitter[1]) / PIXELMETERS_Y)
    return map[ix][iy]

'''
output the map data to an image.
'''
def writeImage(outputFile : str):
    im = Image.new("RGB", (len(map[0]) - 5, len(map) - 5), 0)
    t_colors = dict()
    for k in TERRAINCOLORS.keys():
        t_colors[TERRAINCOLORS[k]] = k
    for x in range(len(map) - 5):
        for y in range(len(map[x]) - 5):
            pixelColor = (0, 0, 0)
            if map[x][y].isSolution == False:
                pixelColor = t_colors[map[x][y].terrain]
            else:
                pixelColor = SOL_COLOR
            im.putpixel((y, x), pixelColor)
    im.show()

#########

'''
Handles argument things. Differs execution of the image processing and A* to other functions.
'''
def main():
    if len(sys.argv) != 6:
        print("Usage :\n\t$python3 lab1.py terrain.png mpp.txt red.txt winter redWinter.png")

    terrain_file = sys.argv[1]
    elevation_file = sys.argv[2]
    path_file = sys.argv[3]
    season = ""
    if sys.argv[4].lower() in SEASONS:  # it's gotta be a valid season, bro.
        season = sys.argv[4].lower()
    else:
        print("invalid season. Season must be [spring, summer, fall, winter]")
        sys.exit( 1 )
    output_filename = sys.argv[5]

    # process the files and parameters that you're given
    processElevation(elevation_file)
    processTerrains(terrain_file)
    dests = processPath(path_file)

    if season == "fall":
        processFall()
    elif season == "winter":
        processWinter()
    elif season == "spring":
        processSpring()
    a_star_path(dests)
    writeImage(output_filename)



if __name__ == "__main__":
    main()