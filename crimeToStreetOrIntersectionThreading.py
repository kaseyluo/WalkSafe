from multiprocessing.pool import ThreadPool
from threading import Lock
from collections import defaultdict
from geopy import distance
from nodesToStreet import findTwoClosest
import pickle
import geocoder
import threading
import json
import sys
import time

#IMPORT STREET: INTERSECTIONS MAP HERE
#streetIntersections = 

#distance from crime to intersection to be considered part of an intersection rather than edge, in meters
DIST_TO_INTERSECTION = 5 

#Variables for using the mapBox API
REQUEST_LIMIT = 30000
KEY1 = "pk.eyJ1IjoibWljYWxpc2FiYWRib2kiLCJhIjoiY2p3ZW9vajdwMTN5YjQ5bnVpMGpoaTJrcCJ9.LOwN7SdJ1z-MHIaG6EB0Pg"
KEY2 = "pk.eyJ1IjoiYmxha3NqbGtqIiwiYSI6ImNqd2VvcGg2ZTB4N2I0NXMycXNvMWU4MGgifQ.H4pmpD9ZcTj5DclDbbg9NA"
KEY3 = "pk.eyJ1IjoiYXNka2ZqZmxrcyIsImEiOiJjandlb3FmdnYweGhxNDBzMjc4MWlrZTJkIn0.WaHwFejhqUp6H5qRSYSNpw"


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
	mutex = Lock()
	pool = ThreadPool(processes=3)
	for latLong in crimeMap:
		street = ""
		print(numReqs)
		if numReqs <= REQUEST_LIMIT:
			result = pool.apply_async(getStreet, (latLong, KEY1))
			street = result.get() 
		elif numReqs <= 2*REQUEST_LIMIT:
			result = pool.apply_async(getStreet, (latLong, KEY2))
			street = result.get() 
		elif numReqs <= 3*REQUEST_LIMIT:
			result = pool.apply_async(getStreet, (latLong, KEY3))
			street = result.get() 

		crimeWeight = crimeMap[latLong]
		if street not in streetMap: 
			# print("NOT IN STREET MAP {}".format(street))
			mutex.acquire()
			numReqs += 1
			mutex.release()
			continue
		intersections = streetMap[street]

		assigned = False
		for i in intersections:
			distFromCrimeToNode = distance.distance(eval(latLong), i).m
			if distFromCrimeToNode < DIST_TO_INTERSECTION: #if within DIST_TO_INTERSECTION to an intersection
				intersectionWeights[i] += crimeWeight
				assigned = True
				break
		if not assigned:
			node1, node2 = findTwoClosest(intersections, eval(latLong))
			if node1 == None or node2 == None: continue
			edge = (node1, node2)
			# print(type(edge))
			edge = tuple(sorted(list(edge)))
			edgeWeights[edge] += crimeWeight
		mutex.acquire()
		numReqs += 1
		mutex.release()
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

        