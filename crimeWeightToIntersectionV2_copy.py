from collections import defaultdict
from geopy import distance
from nodesToStreet import findTwoClosest
import pickle
import geocoder
import threading
import json
import sys

# CONST: Neighborhood radius (in meters) to consider (for computeCrimeWeightV2)
# from a given intersection
RADIUS = 100

# Opens the mappings of intersection and edge to crime weight, version 1.
file1 = open("intersectionToCrimeWeight.pickle", "rb")
intersectionWeightsV1 = pickle.load(file1)
file1.close()

file2 = open("edgeToCrimeWeight.pickle", "rb")
edgeWeightsV1 = pickle.load(file2)
file2.close()

# Opens the mapping from intersection coordinate (key) to intersection cross
# streets (value).
file3 = open("intersectionToCrossStreets_financialDistrict.pickle", "rb")
intersectionToCrossStreets = pickle.load(file3)
file3.close()

# Opens the mapping from an intersection cross street to its neighboring
# intersection coordinates.
file4 = open("neighborMap.pickle", "rb")
neighborMap = pickle.load(file4)
file4.close()

def computeCrimeWeightV2(intersectionCoord, intersectionWeights, edgeWeights):
    if intersectionCoord not in intersectionToCrossStreets: 
        print("Could not find intersectionCoord in intersectionToCrossStreets: ", intersectionCoord)
        return 0 #take out LATER
    crossStreets = intersectionToCrossStreets[intersectionCoord]
    # Set of visited neighboring intersections.
    visited = set([crossStreets])
    crimeWeight = intersectionWeights[intersectionCoord]
    print("origina crime weight: ", crimeWeight)
    for neighborCoord in neighborMap[crossStreets]:
        print("neighbor coord: ", neighborCoord)
        #NOTE: this SAME AS LINE 75's PROBLEM
        if neighborCoord is None: continue
        neighborCrossStreets = intersectionToCrossStreets[neighborCoord]
        if neighborCrossStreets not in visited:
            crimeWeight += computeCrimeWeightV2Helper(
                                neighborCoord,
                                intersectionCoord,
                                visited,
                                intersectionWeights,
                                edgeWeights
                           )
    return crimeWeight

def computeCrimeWeightV2Helper(currCoord, originCoord, visited, intersectionWeights, edgeWeights):
    distToOrigin = distance.distance(currCoord, originCoord).m
    if RADIUS < distToOrigin:
        return 0

    edge = tuple(sorted(list((currCoord, originCoord))))
    inverseDistance = float(1) / distToOrigin
    intersectionWeight = 0
    if currCoord in intersectionWeights: intersectionWeight = intersectionWeights[currCoord]
    edgeWeight = 0
    if edge in edgeWeights: edgeWeight = edgeWeights[edge]
    crimeWeight = inverseDistance * (intersectionWeight + edgeWeight)

    currCrossStreets = intersectionToCrossStreets[currCoord]
    visited.add(currCrossStreets)

    for neighborCoord in neighborMap[currCrossStreets]:
        # IF statement is a TEMPORARy fix for a problem described below:
        # THING TO FIX: neighborMAPS HAS CROSS STREETS MAPPING TO NEIGHBOR NODES THAT include
        # "NONE" values.
        # TO FIX, GO INTO NODESTOSTREET.PY AND FIX LINES 14-19.
        # NOTE: fixing this will update the neighborMap dictionary –– because this is used 
        # to create other dictionaries (like the original crime weight mappings), if we update
        # neighborMap, WE HAVE TO UPDATE EVERY OTHER MAPPING THAT DEPENDS ON IT :)
        if neighborCoord is None: continue
        neighborCrossStreets = intersectionToCrossStreets[neighborCoord]
        if neighborCrossStreets not in visited:
            crimeWeight += computeCrimeWeightV2Helper(
                                neighborCoord,
                                originCoord,
                                visited,
                                intersectionWeights,
                                edgeWeights
                            )
    return crimeWeight

# Returns a mapping between each intersection (key) and a crime weight (value)
# that is computed according to the formula described in computeCrimeWeightV2.
def assignCrimeWeightToIntersection(intersectionWeights, edgeWeights):
    intersectionWeightsV2 = defaultdict(float)
    for intersection, weightV1 in intersectionWeights.items():
        weightV2 = computeCrimeWeightV2(intersection, intersectionWeights, edgeWeights)
        intersectionWeightsV2[intersection] = weightV2

    return intersectionWeightsV2


intersectionWeightsV2 = assignCrimeWeightToIntersection(intersectionWeightsV1, edgeWeightsV1)


s = open("intersectionToCrimeWeightV2.pickle", "wb")
pickle.dump(intersectionWeightsV2, s)
