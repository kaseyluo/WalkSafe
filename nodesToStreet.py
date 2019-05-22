from collections import defaultdict
from geopy import distance
import pickle
import sys

#NEED THIS FROM DANIEL'S CODE
f_new = open("crossStreetsToIntersections_financialDistrict.pickle", "rb")
intersectionToCoord = pickle.load(f_new)

def constructStreetMap(intersectionToCoord):
	# a map of "street name": set of all intersections on that street -- {(lat, long), (lat, long), ...}
	streetMap = defaultdict(set)
	for crossStreet, coord in intersectionToCoord.items():
		st1 = crossStreet[0]
		st2 = crossStreet[1]
		streetMap[st1].add(tuple(coord))
		streetMap[st2].add(tuple(coord))
		# print(crossStreet)
		# print(coord)
		# print(" ")

	return streetMap

def findTwoClosest(setOfNodes, currNode): #set of nodes on a street, latLong of the currNode 
	minimum = sys.maxsize
	node1 = None
	nextMin = sys.maxsize
	node2 = None
	currNode = tuple(currNode)
	for coord in setOfNodes:
		# print("FIND TWO CLOSEST")
		# print(coord)
		# print(currNode)
		# print(" ")
		# if coord == currNode: print("FOUND MATCHING")
		if coord != currNode: 
			distFromCurrToCoord = distance.distance(currNode, coord).m
			if distFromCurrToCoord < minimum: 
				nextMin = minimum
				node2 = node1
				minimum = distFromCurrToCoord
				node1 = coord
			elif distFromCurrToCoord < nextMin:
				nextMin = distFromCurrToCoord
				node2 = coord
	# print(node1, node2)
	return node1, node2


def constructNeighborsMap(intersectionToCoord, streetMap):
	neighborMap = defaultdict(set)
	for crossStreet, coord in intersectionToCoord.items():
		for street in crossStreet:
			# print(street)
			# print(streetMap[street])
			# print("CurrNode: ", coord)
			# print(" ")

			#find two closest nodes on this street
			node1, node2 = findTwoClosest(streetMap[street], coord)

			#add these neighbors to map
			neighborMap[crossStreet].add(node1)
			neighborMap[crossStreet].add(node2)

	return neighborMap


streetMap = constructStreetMap(intersectionToCoord)

# for s in streetMap:
# 	print(s, ": ", streetMap[s])
neighborMap = constructNeighborsMap(intersectionToCoord, streetMap)
# for n in neighborMap:
# 	print(n, ": ", neighborMap[n])


s = open("streetMap.pickle", "wb")
pickle.dump(streetMap, s)

n = open("neighborMap.pickle", "wb")
pickle.dump(neighborMap, n)










