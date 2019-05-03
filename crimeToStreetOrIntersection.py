from multiprocessing.dummy import Pool as ThreadPool
from collections import defaultdict
from geopy import distance
import geocoder
import threading
import json
import sys

#IMPORT STREET: INTERSECTIONS MAP HERE
#streetIntersections = 

#distance from crime to intersection to be considered part of an intersection rather than edge, in meters
DIST_TO_INTERSECTION = 5 

# if CRIMEFILE:
with open("crimeData.json", 'r') as f:
    crimeMap = json.load(f)
print(len(crimeMap))

intersectionWeights = defaultdict(int)
edgeWeights = defaultdict(int)


def getStreet(latLong):
	g = geocoder.osm(latLong, method="reverse")
	street = g.street
	return street

def test():
	latLong = "(40.706911764, -73.770286)"
	print(getStreet(latLong))


def assignCrimeToLocation(crimeMap):
	for latLong in crimeMap:
		street = getStreet(latLong)
		crimeWeight = crimeMap[latLong]

		#if within DIST_TO_INTERSECTION to an intersection
		#for i in intersections:
		#	distFromCrimeToNode = distance.distance(eval(latLong), eval(i)).m
		#	if distFromCrimeToNode < DIST_TO_INTERSECTION:
		#		intersectionWeights[latLong] += crimeWeight
		#		break

		#ELSE: all the rest of this
		#otherwise, we need to find the two closest nodes to the crime, that will be the edge which we assign the weight to
		# intersections = streetIntersections[street]

		#min = sys.maxint
		#node1 = None
		#nextMin = syst.maxint
		#node2 = None

		#for i in intersections
		#	distFromCrimeToNode = distance.distance(eval(latLong), eval(i)).m
		#	if distFromCrimeToNode < min: 
			# 	nextMin = min
			#	node2 = node1
			# 	min = distFromCrimeToNode
			#	node1 = i
			# elif distFromCrimeToNode < nextMin:
			# 	nextMin = distFromCrimeToNode
			#	node2 = i

		#edge = (node1, node2) <-- sorted?

		edgeWeights[edge] += crimeWeight

		#find edge

test()	


# t = threading.Thread(target=getStreet, args=(latLong,))
# threads.append(t)
# t.start()
# for t in threads:
# 	t.join()


	# g = geocoder.geocodefarm(latLong, method="reverse")
	# street = g.street
	# print(street)

# 	intersections = streetIntersections[]
# 	for intersection in intersections:
		
		#if latLong is within DIST_TO_INTERSECTION of intersection, add to intersectionWeights

        