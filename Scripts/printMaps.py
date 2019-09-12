import pickle
def printCrossStreetsToCoord():
	f_new = open("crossStreetsToIntersection.pickle", "rb")
	intersectionToCoordMap = pickle.load(f_new)
	for f in intersectionToCoordMap:
		print(f, ": ", intersectionToCoordMap[f])

def printEdgeToCrimeWeight():
	e_new = open("edgeToCrimeWeight.pickle", "rb")
	edgeToCrimeWeight = pickle.load(e_new)
	for f in edgeToCrimeWeight:
		print(f, ": ", edgeToCrimeWeight[f])

def printNeighborsMaps():
	n_new = open("neighborMap.pickle", "rb")
	nmap = pickle.load(n_new)
	for f in nmap:
		print(f, ": ", nmap[f])

def printIntersectionToCrimeWeight():
	s = open("intersectionToCrimeWeight.pickle", "rb")
	mapp = pickle.load(s)
	v2 = open("intersectionToCrimeWeightV2.pickle", "rb")
	mappV2 = pickle.load(v2)
	for a in mapp:
		print("old weight: ", a, ": ", mapp[a])
		print("new weight: ", a, ": ", mappV2[a])
		print(" ")

printCrossStreetsToCoord()
# printNeighborsMaps()
# printEdgeToCrimeWeight()
# printIntersectionToCrimeWeight()
