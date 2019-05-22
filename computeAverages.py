import pickle

s = open("intersectionToCrimeWeight.pickle", "rb")
intersectionWeights = pickle.load(s)

n = open("edgeToCrimeWeight.pickle", "rb")
edgeToCrimeWeights = pickle.load(n)

def computeAverageValue(dictionary):
	totalWeight = 0
	for i in dictionary:
		totalWeight += dictionary[i]
	return float(totalWeight)/len(dictionary)

aveIntersectionWeight = computeAverageValue(intersectionWeights)
aveEdgeToCrimeWeight  = computeAverageValue(edgeToCrimeWeights) 

# print(aveIntersectionWeight)
# print(aveEdgeToCrimeWeight)