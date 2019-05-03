from collections import defaultdict
from geopy import distance
import pickle

#NEED THIS FROM DANIEL'S CODE
intersectionToCoord = {}

def constructStreetMap(intersectionToCoord):
	# a map of "street name": set of all intersections on that street -- {(lat, long), (lat, long), ...}
	streetMap = defaultdict(set)
	for crossStreet, coord in intersectionToCoord.items():
		st1 = crossStreet[0]
		st2 = crossStreet[1]
		streetMap[st1].add(coord)
		streetMap[st2].add(coord)
	return streetMap

def findTwoClosest(setOfNodes, currNode): #set of nodes on a street, latLong of the currNode 
	minimum = sys.maxint
	node1 = None
	nextMin = syst.maxint
	node2 = None
	for coord in setOfNodes:
		distFromCurrToCoord = distance.distance(currNode, coord).m
		if distFromCurrToCoord < minimum: 
			nextMin = minimum
			node2 = node1
			minimum = distFromCurrToCoord
			node1 = coord
		elif distFromCurrToCoord < nextMin:
			nextMin = distFromCurrToCoord
			node2 = coord
	return node1, node2


def constructNeighborsMap(intersectionToCoord, streetMap):
	neighborMap = defaultdict(set)
	for crossStreet, coord in intersectionToCoord.items():
		for street in crossStreet:
			#find two closest nodes on this street
			node1, node2 = findTwoClosest(streetMap[street], coord)

			#add these neighbors to map
			neighborMap[crossStreet].add(node1)
			neighborMap[crossStreet].add(node2)

	return neighborMap


streetMap = constructStreetMap(intersectionToCoord)
neighborMap = constructNeighborsMap(intersectionToCoord, streetMap)

s = open("streetMap.pickle", "wb")
pickle.dump(streetMap, s)

n = open("neighborMap.pickle", "wb")
pickle.dump(neighborMap, n)










