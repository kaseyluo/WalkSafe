import time
import json
import math
from geopy import distance

# TODO: make constants clear.
averageBlockInMeters = 177.

class SearchGraph():
    def __init__(self, neighborsMap, coordToIntersection, intersectionToCrimeWeight,
                 intersectionToCrimeWeightV2, edgeToCrimeWeight):
        # Mapping from every intersection node to its neighbors.
        self.neighborsMap = neighborsMap
        # Mapping from every coordinate to its street intersection tuple node.
        self.coordToIntersection = coordToIntersection
        # Mapping from every intersection to its computed crime weight.
        self.intersectionToCrimeWeight = intersectionToCrimeWeight
        # Mappving from every intersection to its computed crime weight (version 2).
        self.intersectionToCrimeWeightV2 = intersectionToCrimeWeightV2
        # Mapping from every edge to its computed crime weight.
        self.edgeToCrimeWeight = edgeToCrimeWeight
        # Average crime weight of an intersection.
        self.aveIntersectionWeight = self.__computeAverageValue(intersectionToCrimeWeight)
        # Average crime weight of an edge.
        self.aveEdgeToCrimeWeight = self.__computeAverageValue(edgeToCrimeWeight)
        # Average crime weight (V2 weights) of an intersection.
        self.aveIntersectionWeightV2 = self.__computeAverageValue(intersectionToCrimeWeightV2)


    def findPath(self, searchAlgorithmFunc, startNode, endNode, alpha, beta):
        return searchAlgorithmFunc(startNode, endNode, self.neighborsMap,
                                     self.coordToIntersection, self.__getCost,
                                     alpha, beta)


    def findPathAndSearchTime(self, searchAlgorithmFunc, startNode, endNode, alpha, beta):
        startTime = time.time()
        actions = self.findPath(searchAlgorithmFunc, startNode, endNode, alpha, beta)
        endTime = time.time()
        return actions, endTime - startTime

    def getSafetyAndDistanceScores(self, actions):
        return self.getSafetyScore(actions), self.getDistance(actions)

    def getSafetyScore(self, actions):
        safety = 0
        if len(actions) == 0: return safety

        # Add weight at start node, if applicable.
        if actions[0] in self.intersectionToCrimeWeight:
            safety += self.intersectionToCrimeWeight[actions[0]]

        # Add weight of every edge along the path.
        for i in range(len(actions) - 1):
            edge = (actions[i], actions[i + 1])
            edge = tuple(sorted(list(edge)))
            if edge in self.edgeToCrimeWeight:
                safety += self.edgeToCrimeWeight[edge]

        # Add weight at end node, if applicable.
        if actions[len(actions) - 1] in self.intersectionToCrimeWeight:
            safety += self.intersectionToCrimeWeight[actions[len(actions) - 1]]

        return safety

    def getDistance(self, actions):
        totalDistance = 0
        for i in range(len(actions) - 1):
            totalDistance += distance.distance(actions[i], actions[i + 1]).m
        return totalDistance

    def outputToJSON(self, actions, fileName):
        newActions = actions
        if len(actions) > 23:
            newActions = [actions[0]]
            increment = math.ceil((len(actions) - 2) / 21.0)
            i = 1
            while i < len(actions) - 1:
                newActions.append(actions[i])
                i+= increment
            newActions += [actions[len(actions) - 1]]
        with open(fileName, 'w') as outfile:
            json.dump(newActions, outfile)

    ## Cost function returns the cost between any two adjacent nodes.
    def __getCost(self, startNode, endNode, alpha, beta, normalize=True, useSecondaryWeights=False):
        edge = tuple(sorted([startNode, endNode]))

        crimeWeightAtIntersection = 0
        if endNode in self.intersectionToCrimeWeight:
            crimeWeightAtIntersection = self.intersectionToCrimeWeight[endNode]

        if normalize:
            if useSecondaryWeights:
                alpha_term = self.intersectionToCrimeWeightV2[endNode] / self.aveIntersectionWeightV2
                beta_term = distance.distance(startNode, endNode).m / averageBlockInMeters
                return alpha * alpha_term + beta * beta_term
            else:
                alpha_term = self.edgeToCrimeWeight[edge] / self.aveEdgeToCrimeWeight + crimeWeightAtIntersection / self.aveIntersectionWeight
                beta_term = distance.distance(startNode, endNode).m / averageBlockInMeters
                return alpha * alpha_term + beta * beta_term

        # Basic Cost = the sum of (1) the crime weight of the edge between
        # startNode and endNode, (2) the crime weight of the endNode (if any),
        # and (3) the distance from start to end.
        return edgeToCrimeWeight[edge] + crimeWeightAtIntersection + distance.distance(startNode, endNode).m

    def __computeAverageValue(self, dictionary):
        totalWeight = 0
        for i in dictionary:
            totalWeight += dictionary[i]
        return float(totalWeight) / len(dictionary)

# the distance between the inputted start and end node
def getHeuristic(startNode, endNode):
	return distance.distance(startNode, endNode).m

def getLatLongOfPath(actions):
	for action in actions:
		print(intersectionToLatLog[action])
