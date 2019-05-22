import pickle

s = open("intersectionToCrimeWeight.pickle", "rb")
intersectionWeights = pickle.load(s)

n = open("edgeToCrimeWeight.pickle", "rb")
edgeToCrimeWeights = pickle.load(n)

#get neighbors map
s_new = open("intersectionToCrimeWeightV2.pickle", "rb")
intersectionToCrimeWeightV2 = pickle.load(s_new)


def computeAverageValue(dictionary):
	totalWeight = 0
	for i in dictionary:
		totalWeight += dictionary[i]
	return float(totalWeight)/len(dictionary)

aveIntersectionWeight = computeAverageValue(intersectionWeights)
aveEdgeToCrimeWeight  = computeAverageValue(edgeToCrimeWeights) 
aveIntersectionWeightV2 = computeAverageValue(intersectionToCrimeWeightV2)

# print(aveIntersectionWeight)
# print(aveEdgeToCrimeWeight)