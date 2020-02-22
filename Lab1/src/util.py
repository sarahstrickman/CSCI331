'''

Functions that I refer to.

'''
from dataclasses import dataclass
from typing import Union
import math

SEASONS = {"summer", "winter", "fall", "spring"}    # valid seasons
TERRAINS = {"OPEN" : 100,
            "MEADOW" : 100,
            "FOREST_EASY_MOVEMENT" : 100,
            "FOREST_SLOW_RUN" : 100,
            "FOREST_WALK" : 100,
            "IMPASSIBLE" : 100,
            "WATER" : 100,
            "PAVED" : 100,
            "FOOTPATH" : 100,
            "OUT_OF_BOUNDS" : 100} # different terrains and their default speed (slope = 0)

TERRAINCOLORS = {(248,148,18) : "OPEN",
                 (255,192,0) : "MEADOW",
                 (255,255,255) : "FOREST_EASY_MOVEMENT",
                 (2,208,60) : "FOREST_SLOW_RUN",
                 (2,136,40) : "FOREST_WALK",
                 (5,73,24) : "IMPASSIBLE",
                 (0,0,255) : "WATER",
                 (71,51,3) : "PAVED",
                 (0,0,0) : "FOOTPATH",
                 (205,0,101) : "OUT_OF_BOUNDS"}

PIXELMETERS_X = 10.29
PIXELMETERS_Y = 7.55

@dataclass
class MapPoint:
    x : float     # latitude in meters
    y : float     # longitude in meters
    z : float     # elevation in meters
    terrain : str

@staticmethod
def heuristicFunction(starting, ending):
    return 0

'''
Tobler's walking function.  This function only takes into account the distance 
between curr and dest (not any obstacles between them)
'''
@staticmethod
def getSpeed(curr : MapPoint, dest : MapPoint):
    x_dist = dest.x - curr.x
    y_dist = dest.y - curr.y
    z_dist = dest.z - curr.z    # height
    flat_ground_distance = math.sqrt((x_dist ** 2) + (y_dist ** 2))
    if flat_ground_distance == 0:   # it's the same location.
        return 0
    slope = (z_dist) / flat_ground_distance
    default_speed = TERRAINS[curr.terrain]
    return default_speed * math.e ** (-3.5 * abs(slope + 0.5))













































