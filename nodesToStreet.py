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
		# TO DO ITERATE THROUGH THE CROSS STREETS
		# for street 
		st1 = crossStreet[0]
		st2 = crossStreet[1]
		streetMap[st1].add(tuple(coord))
		streetMap[st2].add(tuple(coord))
		# print(crossStreet)
		# print(coord)
		# print(" ")

	return streetMap

def findTwoClosest(setOfNodes, currNode): #set of nodes on a street, latLong of the currNode 
	# if (len(setOfNodes) == 0): print("SET IS EMPTY")
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
			# if len(streetMap[street]) == 0:
				# print("Street {} was not found in streetMap".format(street))
				# print("Street {} is taken from the list {} from intersectionToCoord".format(street, crossStreet))
				# print(" ")
			#find two closest nodes on this street
			node1, node2 = findTwoClosest(streetMap[street], coord)
			# if (node1 or node2 == None): print("foudn none, but adding to neighbormap nonetheless")

			#add these neighbors to map
			neighborMap[crossStreet].add(node1)
			neighborMap[crossStreet].add(node2)

	return neighborMap


#UNCOMMENT WHEN YOU WANT TO REMAKE THE STREET MAP AND NEIGHBOR MAP
streetMap = constructStreetMap(intersectionToCoord)
neighborMap = constructNeighborsMap(intersectionToCoord, streetMap)
# s = open("streetMap.pickle", "wb")
# pickle.dump(streetMap, s)

# n = open("neighborMap.pickle", "wb")
# pickle.dump(neighborMap, n)



#CODE TO PRINT OUT MAPS
# for s in streetMap:
# 	print(s, ": ", streetMap[s])
# for n in neighborMap:
# 	print(n, ": ", neighborMap[n])












