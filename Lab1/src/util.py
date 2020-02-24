'''

Functions that I refer to.

'''
from dataclasses import dataclass
from typing import Union
import math

SEASONS = {"summer", "winter", "fall", "spring"}    # valid seasons
TERRAINS = {"OPEN" : 4.0,
            "MEADOW" : 1.0,
            "FOREST_EASY_MOVEMENT" : 3.0,
            "FOREST_SLOW_RUN" : 2.0,
            "FOREST_WALK" : 1.0,
            "IMPASSIBLE" : 0.0,
            "WATER" : 0.0,
            "ICE" : 2.0,                    # for winter
            "MUD" : 1.0,                    # for spring
            "PAVED" : 5.0,
            "FOOTPATH" : 5.0,
            "FOOTPATH_FALL" : 4.0,          # for fall
            "OUT_OF_BOUNDS" : 0.0} # different terrains and their default speed (slope = 0)

TERRAINCOLORS = {(248,148,18) : "OPEN",
                 (255,192,0) : "MEADOW",
                 (255,255,255) : "FOREST_EASY_MOVEMENT",
                 (2,208,60) : "FOREST_SLOW_RUN",
                 (2,136,40) : "FOREST_WALK",
                 (5,73,24) : "IMPASSIBLE",
                 (0,0,255) : "WATER",
                 (105, 255, 255) : "ICE",           # for winter
                 (53, 148, 158) : "MUD",             # for spring
                 (71,51,3) : "PAVED",
                 (0,0,0) : "FOOTPATH",
                 (221, 221, 221) : "FOOTPATH_FALL", # for fall
                 (205,0,101) : "OUT_OF_BOUNDS"}

SOL_COLOR = (176, 86, 205)   # color for solution path

PIXELMETERS_X = 10.29
PIXELMETERS_Y = 7.55

@dataclass
class MapPoint:
    x : float     # latitude in meters
    y : float     # longitude in meters
    z : float     # elevation in meters
    terrain : str
    isSolution : bool
    # parent : Union[None, 'MapPoint'] = None

    def toString(self):
        return str(self.x) + ";" + str(self.y)


'''
Amount of time it will take to travel from curr to dest. (t = d/s)

Distance = 3 dimensional distance between the points

Speed = Tobler's walking function.  This function only takes into account the distance 
between curr and dest (not any obstacles between them).

Acts as heuristic function in this example.
return : -1 for error code. This means that the path is not possible because of terrain.
'''
def getTime(curr : MapPoint, dest : MapPoint):
    x_dist = dest.x - curr.x
    y_dist = dest.y - curr.y
    z_dist = dest.z - curr.z    # height
    flat_ground_distance = math.sqrt((x_dist ** 2) + (y_dist ** 2))
    real_distance = math.sqrt((x_dist ** 2) + (y_dist ** 2) + (z_dist ** 2))
    # if flat_ground_distance == 0:   # it's the same location.
    #     return 0
    # slope = (z_dist) / flat_ground_distance
    # default_speed = TERRAINS[curr.terrain]
    # real_speed = default_speed * math.e ** (-3.5 * abs(slope + 0.05))
    # if real_speed == 0:
    #     return -1
    return real_distance * (7 - TERRAINS[curr.terrain]) #/ real_speed

def heuristicFunction(curr : MapPoint, dest : MapPoint):
    x_dist = dest.x - curr.x
    y_dist = dest.y - curr.y
    z_dist = dest.z - curr.z  # height
    flat_ground_distance = math.sqrt((x_dist ** 2) + (y_dist ** 2))
    real_distance = math.sqrt((x_dist ** 2) + (y_dist ** 2) + (z_dist ** 2))
    if flat_ground_distance == 0:  # it's the same location.
        return 0
    slope = (z_dist) / flat_ground_distance
    default_speed = 6
    real_speed = default_speed * math.e ** (-3.5 * abs(slope + 0.05))
    if real_speed == 0:
        return -1
    return real_distance #/ real_speed













































