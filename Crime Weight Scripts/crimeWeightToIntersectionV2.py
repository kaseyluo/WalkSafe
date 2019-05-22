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
neighborMap = pickle.laod(file4)
file4.close()

def assignCrimeToLocation(crimeMap):
	intersectionWeights = defaultdict(float)
	edgeWeights = defaultdict(float)
	numReqs = 0
	for latLong in crimeMap:
		street = ""
		print(numReqs)
		if numReqs <= REQUEST_LIMIT:
			# print(latLong)
			street = getStreet(latLong, KEY1)
		elif numReqs <= 2*REQUEST_LIMIT:
			street = getStreet(latLong, KEY2)
		elif numReqs <= 3*REQUEST_LIMIT:
			street = getStreet(latLong, KEY3)

		crimeWeight = crimeMap[latLong]
		if street not in streetMap:
			# print("NOT IN STREET MAP {}".format(street))
			numReqs += 1
			continue
		intersections = streetMap[street]


		for i in intersections:
			distFromCrimeToNode = distance.distance(eval(latLong), i).m
			if distFromCrimeToNode < DIST_TO_INTERSECTION: #if within DIST_TO_INTERSECTION to an intersection
				intersectionWeights[latLong] += crimeWeight
			else:
				node1, node2 = findTwoClosest(intersections, eval(latLong))
				edge = (node1, node2)
				edgeWeights[edge] += crimeWeight
		numReqs += 1
	return intersectionWeights, edgeWeights

def computeCrimeWeightV2(intersectionCoord, intersectionWeights, edgeWeights):
    crossStreets = intersectionToCrossStreets[intersectionCoord]
    # Set of visited neighboring intersections.
    visited = Set([crossStreets])
    crimeWeight = intersectionWeights[intersectionCoord]
    for neighborCoord in neighborMap[crossStreets]:
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
    crimeWeight = inverseDistance * (intersectionWeights[currCoord] + edgeWeights[edge])

    currCrossStreets = intersectionToCrimeWeight[currCoord]
    visited.add(currCrossStreets)
    for neighborCoord in neighborMap[currCrossStreets]:
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


intersectionWeightsV2 = assignCrimeToLocation(intersectionWeightsV1, edgeWeightsV1)

s = open("intersectionToCrimeWeightV2.pickle", "wb")
pickle.dump(intersectionWeightsV2, s)
