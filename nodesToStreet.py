from collections import defaultdict
from geopy import distance
from checkAccuracyOfNeighbors import checkAccuracyOfNeighbors
import pickle
import sys
from checkAccuracyOfNeighbors import checkAccuracyOfNeighbors

<<<<<<< HEAD
#NEED THIS FROM DANIEL'S CODE
#TO DO, CHANGE THIS TO crossStreetsToIntersection.pickle
# f_new = open("crossStreetsToIntersections_financialDistrict.pickle", "rb")
# intersectionToCoord = pickle.load(f_new)
# =======
f = open("crossStreetsToIntersection.pickle", "rb")
crossStreetsToIntersection = pickle.load(f)
# >>>>>>> 6f13f334cdb45bf1dbee88e8e35525ea49fafbaa

# Constructs a map between each street to the set of all intersection
# coordinates on that street -- ''{(lat, long), (lat, long), ...}
def constructStreetMap(crossStreetsToIntersection):
	streetMap = {}
	for crossStreet, coord in crossStreetsToIntersection.items():
		for street in crossStreet:
			# Adds intersection coordinate to street's set of intersections.
			currentSet = streetMap.get(street, set([]))
			currentSet.add(coord)
			streetMap[street] = currentSet

	return streetMap

# Finds the two nodes in setOfNodes that are closest (in distance) to currNode.
# --- setOfNodes is the set of nodes along a street.
def findTwoClosest(setOfNodes, currNode):
	minimum = sys.maxsize
	nextMin = sys.maxsize
	node1 = None
	node2 = None
	for coord in setOfNodes:
		if coord != currNode:
			distFromCurrToCoord = distance.distance(currNode, coord).m
			if distFromCurrToCoord < minimum:
				# Bumps down the 1st closest node to 2nd closet.
				nextMin = minimum
				node2 = node1
				# Sets the new 1st closest node.
				minimum = distFromCurrToCoord
				node1 = coord
			elif distFromCurrToCoord < nextMin:
				# Sets the new 2nd closest node.
				nextMin = distFromCurrToCoord
				node2 = coord
	return node1, node2

# Constructs a map between each intersection's cross streets to the set of all
# neighboring intersection nodes (coordinates).
def constructNeighborsMap(crossStreetsToIntersection, streetMap):
	neighborMap = {}
	for crossStreet, coord in crossStreetsToIntersection.items():
		for street in crossStreet:
			# Finds the two nodes on this street that are closest to the
			# intersection's coordinate --- these are our neighbors along this
			# street.
			node1, node2 = findTwoClosest(streetMap[street], coord)
			node1, node2 = checkAccuracyOfNeighbors(coord, node1, node2)
# <<<<<<< HEAD
# 			# if (node1 or node2 == None): print("foudn none, but adding to neighbormap nonetheless")

# 			#add these neighbors to map
# 			if node1 not None: neighborMap[crossStreet].add(node1)
# 			if node2 not None: neighborMap[crossStreet].add(node2)
# =======
# >>>>>>> 6f13f334cdb45bf1dbee88e8e35525ea49fafbaa

			# Adds these neighbors to our map (for this intersection's cross streets).
			currentSet = neighborMap.get(crossStreet, set([]))
			if node1 is not None: currentSet.add(node1)
			if node2 is not None: currentSet.add(node2)
			neighborMap[crossStreet] = currentSet
	return neighborMap


streetMap = constructStreetMap(crossStreetsToIntersection)
neighborMap = constructNeighborsMap(crossStreetsToIntersection, streetMap)

fnew1 = open("streetMap.pickle", "wb")
pickle.dump(streetMap, fnew1)

fnew2 = open("neighborMap.pickle", "wb")
pickle.dump(neighborMap, fnew2)
