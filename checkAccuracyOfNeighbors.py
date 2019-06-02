from geopy import distance

def checkAccuracyOfNeighbors(currNode, node1, node2):
	distToNode1 = distance.distance(currNode, node1).m
	distToNode2 = distance.distance(currNode, node2).m
	pathLength = distToNode1 + distToNode2
	distBetweenNeighbors = distance.distance(node1, node2).m
	if pathLength - distBetweenNeighbors >= min(2*distToNode1, 2*distToNode2): #if this occurs, that means that the neighbors found are an edge case, we should only return closest neighbor
		if (distToNode1 <= distToNode2): return node1, None
		else: return node2, None
	else:
		return node1, node2

