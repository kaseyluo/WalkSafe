import util
import sys
import pickle
import time
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

class AStarShortestPathProblem(util.SearchProblem):
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
        	cost = self.moveCost(currNode, n) + distance.distance(n, self.endNode).m
        	t = (n, n, cost)
        	results.append(t)
        return results

def getCost(startNode, endNode):
	edge = (startNode, endNode)
	crimeWeightAtIntersection = 0
	if endNode in intersectionToCrimeWeight:
		crimeWeightAtIntersection = intersectionToCrimeWeight[endNode]

	#cost = crime at edge, crime at endNode if any, + distance from start to end
	# print("cimre: ", edgeToCrimeWeight[edge] + crimeWeightAtIntersection, "dist: ", distance.distance(startNode, endNode).m)
	return edgeToCrimeWeight[edge] + crimeWeightAtIntersection + distance.distance(startNode, endNode).m

# the distance between the inputted start and end node
def getHeuristic(startNode, endNode):
	return distance.distance(startNode, endNode).m

def baselineGreedy(startNode, endNode, neighborsMap): #TODO, write this
	weight = 0
	path = []
	currNode = startNode
	visited = set()
	visited.add(startNode)
	cost = 0

	while(currNode != endNode):
		# print("currNode: ", currNode)
		# print("currNode: ", coordToIntersection[currNode])
		#explore neighbors of the currNode
		neighbors = neighborsMap[coordToIntersection[currNode]]
		currWeight = float('inf') #TODO, make this max
		bestNeighbor = currNode
		for n in neighbors:
			if n == None: continue #TODO, FIX THIS
			# print("n: ", coordToIntersection[n])
			# print("in for loop")
			if n not in visited:
				edge = (currNode, n)
				if edge not in edgeToCrimeWeight: 
					edge = (n, currNode) #try both orders of edges
					#ASK are we garuenteed there is an edge?

				if getCost(edge[0], edge[1]) < currWeight:
					bestNeighbor = n
					currWeight = getCost(edge[0], edge[1])
		if bestNeighbor == currNode:
			print("found nothing")
			return "Sorry explored everything"
			
		path.append(bestNeighbor)
		visited.add(bestNeighbor)
		cost += currWeight
		currNode = bestNeighbor
				

		#choose the neighbor with the smallest weight
		#add this neighbor to path
	print("Greedy Path: ")
	for p in path:
		print(coordToIntersection[p])
	print("Total Cost: ", cost)
	return path

def findUCSPath(startNode, endNode, getCost):
	#get neighborNodes map
	ucs = util.UniformCostSearch(verbose=0)
	ucs.solve(ShortestPathProblem(startNode, endNode, getCost, neighborsMap))
	actions = ucs.actions
	print("Safest path, UCS: ")
	print(coordToIntersection[startNode])
	for a in actions:
		print(coordToIntersection[a])
	print("Total Cost: ", ucs.totalCost)
	return ucs.actions

def findAStarPath(startNode, endNode, getCost):
	#get neighborNodes map
	ucs = util.UniformCostSearch(verbose=0)
	ucs.solve(AStarShortestPathProblem(startNode, endNode, getCost, neighborsMap))
	actions = ucs.actions
	print("Safest, shortest path, A*: ")
	print(coordToIntersection[startNode])
	for a in actions:
		print(coordToIntersection[a])
	print("Total Cost: ", ucs.totalCost)
	return ucs.actions

#Start intersection? usage: ('street name', 'street name') =   ('Edgar Street', 'Trinity Place')
#End intersection? usage: ('street name', 'street name') =   ('Rector Street', 'Washington Street')

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

	startTimeUCS = time.time()
	actionsUCS = findUCSPath(startNode, endNode, getCost)
	endTimeUCS = time.time()
	print("Time to run UCS: ", endTimeUCS - startTimeUCS)

	startTimeAStar = time.time()
	actionsAStar = findAStarPath(startNode, endNode, getCost)
	endTimeAStar = time.time()
	print("Time to run A*: ", endTimeAStar - startTimeAStar)

	startTimeGreedy = time.time()
	actionsGreedy = baselineGreedy(startNode, endNode, neighborsMap)
	endTimeGreedy = time.time()
	print("Time to run Greedy: ", endTimeGreedy - startTimeGreedy)

run()















