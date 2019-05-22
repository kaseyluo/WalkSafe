from multiprocessing.dummy import Pool as ThreadPool
from collections import defaultdict
from geopy import distance
from nodesToStreet import findTwoClosest
import pickle
import geocoder
import threading
import json
import sys

#IMPORT STREET: INTERSECTIONS MAP HERE
#streetIntersections = 

#distance from crime to intersection to be considered part of an intersection rather than edge, in meters
DIST_TO_INTERSECTION = 5 

#Variables for using the mapBox API
REQUEST_LIMIT = 30000
KEY1 = "pk.eyJ1IjoiYWphamFqYWoiLCJhIjoiY2p2eXdiNG5vMDdrOTQ2bGN0YjZqMm5pdSJ9.DjmakmkyZbIY-AKxd9sq5Q"
KEY2 = "pk.eyJ1Ijoic3V0dHRlciIsImEiOiJjanZ5d2NlbjYwa2U5NDl0ODJrZmQ5d2x4In0.DLIHuaZiV0rWZYoWQKBwbw"
KEY3 = "pk.eyJ1IjoiYnVla2pyIiwiYSI6ImNqdnl3ZHJuaDBrYW80NG1pNTBxOXF5czIifQ.zI0GRc3dQwwwPmzDPLR0Pw"


#Reading in the streetMap dictionary, maps street to all intersections on the street
f_new = open("streetMap.pickle", "rb")
streetMap = pickle.load(f_new)
with open("crimeData.json", 'r') as f:
# with open("crimeDataMiniMini.json", 'r') as f:
    crimeMap = json.load(f)
print(len(crimeMap))



def getStreet(latLong, key):
	g = geocoder.mapbox(latLong, method="reverse", key=key)
	g_json = g.json
	if g_json == None: return
	if 'raw' not in g_json: return
	if 'text' not in g_json['raw']: return
	# if 'raw' in g_json and 'text' in g_json['raw']:
	street = g_json['raw']['text'] 
	return street

def test():
	latLong = "(40.706911764, -73.770286)"
	print(getStreet(latLong))

def assignCrimeToLocation(crimeMap):
	intersectionWeights = defaultdict(float)
	edgeWeights = defaultdict(float)
	numReqs = 0
	for latLong in crimeMap:
		street = ""
		print(numReqs)
		if numReqs <= REQUEST_LIMIT:
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

		assigned = False
		for i in intersections:
			distFromCrimeToNode = distance.distance(eval(latLong), i).m
			if distFromCrimeToNode < DIST_TO_INTERSECTION: #if within DIST_TO_INTERSECTION to an intersection
				intersectionWeights[latLong] += crimeWeight
				assigned = True
				break
		if not assigned:
			node1, node2 = findTwoClosest(intersections, eval(latLong))
			if node1 == None or node2 == None: continue
			edge = (node1, node2)
			# print(type(edge))
			edge = tuple(sorted(list(edge)))
			edgeWeights[edge] += crimeWeight
		numReqs += 1
	return intersectionWeights, edgeWeights

intersectionWeights, edgeWeights = assignCrimeToLocation(crimeMap)



print("LENGHT INTERSECTION WEIGHTS: ", len(intersectionWeights))
print("LENGHT edgeWeights : ", len(edgeWeights))
print("PRINTING MAP: ")
for s in intersectionWeights:
	print(s, ": ", intersectionWeights[s])
for n in edgeWeights:
	print(n, ": ", edgeWeights[n])

#LENGHT INTERSECTION WEIGHTS:  33
#LENGHT edgeWeights :  212


s = open("intersectionToCrimeWeight.pickle", "wb")
pickle.dump(intersectionWeights, s)

n = open("edgeToCrimeWeight.pickle", "wb")
pickle.dump(edgeWeights, n)

        