from . import util

class ShortestPathProblem(util.SearchProblem):
    def __init__(self, startNode, endNode, moveCost, neighborsMap, coordToIntersection, alpha=1, beta=1):
        self.startNode = startNode
        self.endNode = endNode
        self.moveCost = moveCost
        self.neighborsMap = neighborsMap
        self.coordToIntersection = coordToIntersection
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
        intersection = self.coordToIntersection[tuple(currNode)] #returns a latitude longitude
        # print(intersection)
        neighbors = self.neighborsMap[intersection] #a set of neighbor nodes to the current node
        for n in neighbors:
        	if n == None: continue #TODO, FIX THIS
        	cost = self.moveCost(currNode, n, self.alpha, self.beta)
        	t = (n, n, cost)
        	results.append(t)
        return results

## Search Algorithm Functions return a path from startNode to endNode
def getGreedyPath(startNode, endNode, neighborsMap, coordToIntersection, getCost, alpha=1, beta=1):
    weight = 0
    path = []
    currNode = startNode
    visited = set()
    visited.add(startNode)

    while (currNode != endNode):
        # Explore neighbors of the currNode.
        neighbors = neighborsMap[coordToIntersection[currNode]]
        currWeight = float('inf')
        bestNeighbor = currNode
        for n in neighbors:
            if n == None: continue # TODO, FIX THIS
            if n not in visited:
                edge = (currNode, n)
                edge_cost = getCost(edge[0], edge[1], alpha, beta)
                if edge_cost < currWeight:
                    bestNeighbor = n
                    currWeight = edge_cost

        if bestNeighbor == currNode:
            print("getGreedyPath: No Path Found.")
            return []

        path.append(bestNeighbor)
        visited.add(bestNeighbor)
        currNode = bestNeighbor

    return path

def getUCSPath(startNode, endNode, neighborsMap, coordToIntersection, getCost, alpha=1, beta=1):
	ucs = util.UniformCostSearch(verbose=0)
	ucs.solve(ShortestPathProblem(startNode, endNode, getCost, neighborsMap, coordToIntersection, alpha, beta))
	actions = [startNode] + ucs.actions

	return actions

def getAStarPath(startNode, endNode, neighborsMap, coordToIntersection, getCost, alpha=1, beta=1):
	aStar = util.AStarSearch(verbose=0)
	aStar.solve(ShortestPathProblem(startNode, endNode, getCost, neighborsMap, coordToIntersection, alpha, beta), endNode, beta)
	actions = [startNode] + aStar.actions

	return actions
