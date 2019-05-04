import pickle
def printCrossStreetsToCoord():
	f_new = open("crossStreetsToIntersections_financialDistrict.pickle", "rb")
	intersectionToCoordMap = pickle.load(f_new)
	for f in intersectionToCoordMap:
		print(f, ": ", intersectionToCoordMap[f])




printCrossStreetsToCoord()