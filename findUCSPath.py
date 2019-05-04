import util
import sys
import pickle
from nodesToStreet import intersectionToCoord
from geopy import distance


#get edge to crimeWeight map
f_new = open("edgeToCrimeWeight.pickle", "rb")
edgeToCrimeWeight = pickle.load(f_new)

#get intersection to crimeWeight map
i_new = open("intersectionToCrimeWeight.pickle", "rb")
intersectionToCrimeWeight = pickle.load(i_new)

#get coord to crossStreet map
c_new = open("intersectionToCrossStreets_financialDistrict.pickle", "rb")
coordToIntersection = pickle.load(c_new)

#get neighbors map
n_new = open("neighborMap.pickle", "rb")
neighborsMap = pickle.load(n_new)



class ShortestPathProblem(util.SearchProblem):
    def __init__(self, startNode, endNode, moveCost, neighborsMap):
        self.startNode = startNode
        self.endNode = endNode
        self.moveCost = moveCost
        self.neighborsMap = neighborsMap

    def startState(self):
        start = self.startNode
        return start

    def isEnd(self, state):
        return state == self.endNode

    def succAndCost(self, state):
        results = []
        currNode = state
        intersection = coordToIntersection[currNode] #returns a latitude longitude
        neighbors = self.neighborsMap[intersection] #a set of neighbor nodes to the current node
        for n in neighbors:
        	if n == None: continue #TODO, FIX THIS
        	cost = self.moveCost(currNode, n)
        	t = (n, n, cost)
        	results.append(t)
        return results

def getCost(startNode, endNode):
	edge = (startNode, endNode)
	crimeWeightAtIntersection = 0
	if endNode in intersectionToCrimeWeight:
		crimeWeightAtIntersection = intersectionToCrimeWeight[endNode]

	#cost = crime at edge, crime at endNode if any, + distance from start to end
	return edgeToCrimeWeight[edge] + crimeWeightAtIntersection + distance.distance(startNode, endNode).m

def baselineGreedy(startNode, endNode, neighborsMap): #TODO, write this
	weight = 0
	path = []
	currNode = startNode
	while(currNode != endNode):
		#explore neighbors of the currNode
		neighbors = neighborsMap[currNode]

		currWeight = 1000000000 #TODO, make this max
		for n in neighbors:
			edge = (currNode, n)
			if edge not in edgeToCrimeWeight: edge = (n, currNode) #try both orders of edges

			

		#choose the neighbor with the smallest weight
		#add this neighbor to path

	return path

def findUSCPath(startNode, endNode, getCost):
	#get neighborNodes map
	ucs = util.UniformCostSearch(verbose=0)
	ucs.solve(ShortestPathProblem(startNode, endNode, getCost, neighborsMap))
	actions = ucs.actions
	print("Safest, shortest path: ")
	print(coordToIntersection[startNode])
	for a in actions:
		print(coordToIntersection[a])
	print("Total Cost: ", ucs.totalCost)

	# print(intersectionToCrimeWeight[('Broadway', 'John Street')])
	# nmap = neighborsMap[('Broadway', 'John Street')]
	# for n in nmap:
	# 	inter = coordToIntersection[n]
	# 	print("cost: ", intersectionToCrimeWeight[inter])
	# print(ucs.actions)
	# print(' '.join(ucs.actions))
	# return ' '.join(ucs.actions)

	return ucs.actions

def run():
	startIntersection = input("Start intersection? usage: (\'street name\', \'street name\') =   ")
	startIntersection = tuple(sorted(eval(startIntersection)))
	while startIntersection not in intersectionToCoord:
		print("Sorry, we don't have that intersection in our database, try again!")
		startIntersection = input("Start intersection? usage: (\'street name\', \'street name\') =   ")
		startIntersection = tuple(sorted(eval(startIntersection)))
	
	endIntersection = input("End intersection? usage: (\'street name\', \'street name\') =   ") 
	endIntersection   = tuple(sorted(eval(endIntersection)))
	while endIntersection not in intersectionToCoord:
		print("Sorry, we don't have that intersection in our database, try again!")
		endIntersection = input("End intersection? usage: (\'street name\', \'street name\') =   ") 
		endIntersection   = tuple(sorted(eval(endIntersection)))

	startNode = tuple(intersectionToCoord[startIntersection])
	endNode = tuple(intersectionToCoord[endIntersection])
	actions = findUSCPath(startNode, endNode, getCost)

run()















