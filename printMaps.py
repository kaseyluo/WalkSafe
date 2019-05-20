import pickle
def printCrossStreetsToCoord():
	f_new = open("crossStreetsToIntersections_financialDistrict.pickle", "rb")
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


printCrossStreetsToCoord()
# printNeighborsMaps()
# printEdgeToCrimeWeight()