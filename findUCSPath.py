import util
import sys
import pickle
import time
import json
from nodesToStreet import intersectionToCoord
from geopy import distance
from computeAverages import aveIntersectionWeight, aveEdgeToCrimeWeight, aveIntersectionWeightV2

averageBlockInMeters = 177.


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

#get neighbors map
s_new = open("intersectionToCrimeWeightV2.pickle", "rb")
intersectionToCrimeWeightV2 = pickle.load(s_new)

i_new = open("crossStreetsToIntersections_financialDistrict.pickle", "rb")
intersectionToLatLog = pickle.load(i_new)



class ShortestPathProblem(util.SearchProblem):
    def __init__(self, startNode, endNode, moveCost, neighborsMap, alpha=1, beta=1):
        self.startNode = startNode
        self.endNode = endNode
        self.moveCost = moveCost
        self.neighborsMap = neighborsMap
        self.alpha = alpha
        self.beta = beta

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
        	cost = self.moveCost(currNode, n, self.alpha, self.beta) 
        	t = (n, n, cost)
        	results.append(t)
        return results

def getCost(startNode, endNode, alpha, beta, normalize=True, useSecondaryWeights=False):
	edge = tuple(sorted(list((startNode, endNode))))
	crimeWeightAtIntersection = 0
	if endNode in intersectionToCrimeWeight:
		crimeWeightAtIntersection = intersectionToCrimeWeight[endNode]

	#cost = crime at edge, crime at endNode if any, + distance from start to end
	# print("cimre: ", edgeToCrimeWeight[edge] + crimeWeightAtIntersection, "dist: ", distance.distance(startNode, endNode).m)
	if normalize:
		if not useSecondaryWeights: 
			# print("running old weights")
			cost = alpha*(edgeToCrimeWeight[edge]/aveEdgeToCrimeWeight + crimeWeightAtIntersection/aveIntersectionWeight) + beta*(distance.distance(startNode, endNode).m/averageBlockInMeters)
			# print(cost)
			return cost
		else:
			# print("running new weights")
			return alpha*intersectionToCrimeWeightV2[endNode]/aveIntersectionWeightV2 + beta*(distance.distance(startNode, endNode).m/averageBlockInMeters)
	return edgeToCrimeWeight[edge] + crimeWeightAtIntersection + distance.distance(startNode, endNode).m

# the distance between the inputted start and end node
def getHeuristic(startNode, endNode):
	return distance.distance(startNode, endNode).m

def baselineGreedy(startNode, endNode, neighborsMap, alpha=1, beta=1): #TODO, write this
	weight = 0
	path = []
	currNode = startNode
	visited = set()
	visited.add(startNode)
	cost = 0

	while(currNode != endNode):
		#explore neighbors of the currNode
		neighbors = neighborsMap[coordToIntersection[currNode]]
		currWeight = float('inf') #TODO, make this max
		bestNeighbor = currNode
		for n in neighbors:
			if n == None: continue #TODO, FIX THIS
			if n not in visited:
				edge = (currNode, n)
				if edge not in edgeToCrimeWeight: 
					edge = (n, currNode) #try both orders of edges
					#ASK are we garuenteed there is an edge?
				if getCost(edge[0], edge[1], alpha, beta) < currWeight:
					bestNeighbor = n
					currWeight = getCost(edge[0], edge[1], alpha, beta)
		if bestNeighbor == currNode:
			print("No Path Found.")
			return []
			
		path.append(bestNeighbor)
		visited.add(bestNeighbor)
		cost += currWeight
		currNode = bestNeighbor
				
		#choose the neighbor with the smallest weight
		#add this neighbor to path
	print("Greedy Path: ")
	for p in path:
		print(coordToIntersection[p])
	print("Rel Cost: ", cost)
	return path

def findUCSPath(startNode, endNode, getCost, alpha=1, beta=1):
	#get neighborNodes map
	ucs = util.UniformCostSearch(verbose=0)
	ucs.solve(ShortestPathProblem(startNode, endNode, getCost, neighborsMap, alpha, beta))
	actions = ucs.actions
	print("Safest path, UCS: ")
	print(coordToIntersection[startNode])
	for a in actions:
		print(coordToIntersection[a])
	print("Rel Cost: ", ucs.totalCost)
	return ucs.actions

def findAStarPath(startNode, endNode, getCost, alpha=1, beta=1):
	#get neighborNodes map
	ucs = util.AStarSearch(verbose=0)
	ucs.solve(ShortestPathProblem(startNode, endNode, getCost, neighborsMap, alpha, beta), endNode, beta)
	actions = ucs.actions
	print("Safest, shortest path, A*: ")
	print(coordToIntersection[startNode])
	for a in actions:
		print(coordToIntersection[a])
	print("Rel Cost: ", ucs.totalCost)
	return ucs.actions

#Start intersection? usage: ('street name', 'street name') =   ('Edgar Street', 'Trinity Place')
#End intersection? usage: ('street name', 'street name') =   ('Rector Street', 'Washington Street')

def getSafetyScore(actions):
	safety = 0
	#add weight at start node, if applicable
	if len(actions) == 0: return safety 
	if actions[0] in intersectionToCrimeWeight: safety += intersectionToCrimeWeight[actions[0]]
	for i in range(len(actions) - 1):
		edge = (actions[i], actions[i+1])
		edge = tuple(sorted(list(edge)))
		if edge in edgeToCrimeWeight: safety += edgeToCrimeWeight[edge]

	#add weight at end node, if applicable
	if actions[len(actions) - 1] in intersectionToCrimeWeight: safety += intersectionToCrimeWeight[actions[len(actions)-1]]
	return safety

def getLatLongOfPath(actions):
	for action in actions:
		print(intersectionToLatLog[action])


def getDistance(actions):
	totalDistance = 0
	for i in range(len(actions) - 1):
		totalDistance += distance.distance(actions[i], actions[i+1]).m
	return totalDistance

def outputToJSON(actions, pathName):
	with open(pathName, 'w') as outfile:
		json.dump(actions, outfile)

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

	alpha = float(input("Safety weight? "))
	beta = float(input("Distance weight? "))

	startTimeUCS = time.time()
	actionsUCS = findUCSPath(startNode, endNode, getCost, alpha, beta)
	print(actionsUCS)
	outputToJSON(actionsUCS, "outputPathUCS.json")
	endTimeUCS = time.time()
	print("Safety Score: " , getSafetyScore(actionsUCS))
	print("Distance Score: ", getDistance(actionsUCS))
	print("Time to run UCS: ", endTimeUCS - startTimeUCS)

	startTimeAStar = time.time()
	actionsAStar = findAStarPath(startNode, endNode, getCost, alpha, beta)
	endTimeAStar = time.time()
	print("Safety Score: " , getSafetyScore(actionsAStar))
	print("Distance Score: ", getDistance(actionsAStar))
	print("Time to run A*: ", endTimeAStar - startTimeAStar)

	startTimeGreedy = time.time()
	actionsGreedy = baselineGreedy(startNode, endNode, neighborsMap, alpha, beta)
	outputToJSON(actionsUCS, "outputPathGreedy.json")
	endTimeGreedy = time.time()
	print("Safety Score: " , getSafetyScore(actionsGreedy))
	print("Distance Score: ", getDistance(actionsGreedy))
	print("Time to run Greedy: ", endTimeGreedy - startTimeGreedy)

run()















