from Search.SearchGraph import SearchGraph
from Search.SearchAlgorithms import getGreedyPath, getUCSPath, getAStarPath
import pickle

def askForInput():
    # Input is configured for Manhattan, New York.
    ny_crossStreetsToIntersection_pickle = open("Data/crossStreetsToIntersection.pickle", "rb")
    ny_crossStreetsToIntersection = pickle.load(ny_crossStreetsToIntersection_pickle)

    requestList = input("List all intersections? (y/n): ")
    if requestList == "y":
        for crossStreet in ny_crossStreetsToIntersection.keys():
            print(crossStreet)
    print(" ")

    startIntersection = input("Start intersection? usage: (\'street name\', \'street name\') =   ")
    startIntersection = tuple(sorted(eval(startIntersection)))
    while startIntersection not in ny_crossStreetsToIntersection:
        print("Sorry, we don't have that intersection in our database, try again!")
        startIntersection = input("Start intersection? usage: (\'street name\', \'street name\') =   ")
        startIntersection = tuple(sorted(eval(startIntersection)))

    endIntersection = input("End intersection? usage: (\'street name\', \'street name\') =   ")
    endIntersection = tuple(sorted(eval(endIntersection)))
    while endIntersection not in ny_crossStreetsToIntersection:
        print("Sorry, we don't have that intersection in our database, try again!")
        endIntersection = input("End intersection? usage: (\'street name\', \'street name\') =   ")
        endIntersection = tuple(sorted(eval(endIntersection)))

    startNode = tuple(ny_crossStreetsToIntersection[startIntersection])
    endNode = tuple(ny_crossStreetsToIntersection[endIntersection])

    alpha = float(input("Safety Weight? "))
    beta = float(input("Distance weight? "))
    print(" ")

    return startNode, endNode, alpha, beta


def main():
    startNode, endNode, alpha, beta = askForInput()

    ## Initialize NY Graph (of Manhattan)
    ny_neighborsMap_pickle = open("Data/neighborMap.pickle", "rb")
    ny_neighborsMap = pickle.load(ny_neighborsMap_pickle)

    ny_coordToIntersection_pickle = open("Data/intersectionToCrossStreets.pickle", "rb")
    ny_coordToIntersection = pickle.load(ny_coordToIntersection_pickle)

    ny_intersectionToCrimeWeight_pickle = open("Data/intersectionToCrimeWeight.pickle", "rb")
    ny_intersectionToCrimeWeight = pickle.load(ny_intersectionToCrimeWeight_pickle)

    ny_intersectionToCrimeWeightV2_pickle = open("Data/intersectionToCrimeWeightV2.pickle", "rb")
    ny_intersectionToCrimeWeightV2 = pickle.load(ny_intersectionToCrimeWeightV2_pickle)

    ny_edgeToCrimeWeight_pickle = open("Data/edgeToCrimeWeight.pickle", "rb")
    ny_edgeToCrimeWeight = pickle.load(ny_edgeToCrimeWeight_pickle)

    ny_graph = SearchGraph(ny_neighborsMap, ny_coordToIntersection,
                                       ny_intersectionToCrimeWeight,
                                       ny_intersectionToCrimeWeightV2,
                                       ny_edgeToCrimeWeight)

    ## -- UCS Search --
    ucs_path, ucs_time = ny_graph.findPathAndSearchTime(getUCSPath,
                                                        startNode, endNode,
                                                        alpha, beta)

    print("Safety Score for UCS: ", ny_graph.getSafetyScore(ucs_path))
    print("Distance Score for UCS: ", ny_graph.getDistance(ucs_path))
    print("Time to run for UCS: ", ucs_time)
    print(" ")

    ## -- A* Search --
    aStar_path, aStar_time = ny_graph.findPathAndSearchTime(getAStarPath,
                                                            startNode, endNode,
                                                            alpha, beta)

    print("Safety Score for A*: " , ny_graph.getSafetyScore(aStar_path))
    print("Distance Score for A*: ", ny_graph.getDistance(aStar_path))
    print("Time to run for A*: ", aStar_time)
    print(" ")

    ## -- Greedy Search --
    greedy_path, greedy_time = ny_graph.findPathAndSearchTime(getGreedyPath,
                                                              startNode, endNode,
                                                              alpha, beta)

    print("Safety Score: " , ny_graph.getSafetyScore(greedy_path))
    print("Distance Score: ", ny_graph.getDistance(greedy_path))
    print("Time to run Greedy: ", greedy_time)



if __name__ == "__main__":
    main()
