from problem import SlidingPiecesProblem
from searchAlgorithm import uniformCostSearch, aStarSearch, iterativeDeepeningSearch, bidirectionalUCSearch
import json
import os
from dataBaseGenerator import generateDB_1_4, generateDB_5_8


def printUCS(problem):
    solution, nodesGenerated = uniformCostSearch(problem)
    route = solution.path()
    routeClean = " -> ".join([str(node.state) for node in route])
    print("========================================")
    print("Uniform Cost Search")
    print("========================================")
    print(f"1. Mejor ruta: {routeClean}")
    print(f"2. Costo total: {solution.pathCost}")
    print(f"3. Nodos generados: {nodesGenerated}\n\n")

def printAStar(problem, heuristic):
    solution, nodesGenerated = aStarSearch(problem, heuristic)
    route = solution.path()
    routeClean = " -> ".join([str(node.state) for node in route])
    print("========================================")
    print("Busqueda A*")
    print("========================================")
    print(f"1. Mejor ruta: {routeClean}")
    print(f"2. Costo total: {solution.pathCost}")
    print(f"3. Nodos generados: {nodesGenerated}\n\n")

def printIDS(problem):
    solution, nodesGenerated = iterativeDeepeningSearch(problem)
    route = solution.path()
    routeClean = " -> ".join([str(node.state) for node in route])
    print("========================================")
    print("Busqueda en Profundidad Iterativa")
    print("========================================")
    print(f"1. Mejor ruta: {routeClean}")
    print(f"2. Costo total: {solution.pathCost}")
    print(f"3. Nodos generados: {nodesGenerated}\n\n")

def printBIUCS(forwardProblem, backwardProblem):
    solution, nodesGenerated = bidirectionalUCSearch(forwardProblem, backwardProblem)
    route = solution.path()
    routeClean = " -> ".join([str(node.state) for node in route])
    print("========================================")
    print("Uniform Cost Search Bidireccional:")
    print("========================================")
    print(f"1. Mejor ruta: {routeClean}")
    print(f"2. Costo total: {solution.pathCost}")
    print(f"3. Nodos generados: {nodesGenerated}\n\n")

if __name__ == "__main__":

    initialState = (1, 2, 3, 5, 4, 0, 7, 6, 8)
    goalState = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    slidingPiecesProblem = SlidingPiecesProblem(initialState, goalState)

    manhattanHeuristic = slidingPiecesProblem.manhattanHeuristic()
    
    printAStar(slidingPiecesProblem, manhattanHeuristic)

    filePath_1_4 = "data/solutions_1_4.json"
    filePath_5_8 = "data/solutions_5_8.json"
    
    if not os.path.exists(filePath_1_4):
        generateDB_1_4()
    
    if not os.path.exists(filePath_5_8):
        generateDB_5_8()

    solutions_1_4 = json.load(open(filePath_1_4))
    solutions_5_8 = json.load(open(filePath_5_8))

    def DBheuristic(node):
        state_1_4 = tuple(tile if tile <= 4 else 0 for tile in node.state)
        state_5_8 = tuple(tile if tile >= 5 else 0 for tile in node.state)

        if str(state_1_4) not in solutions_1_4:
            raise ValueError(f"Unable to find match for {node.state} in 1-4 database")
        
        if str(state_5_8) not in solutions_5_8:
            raise ValueError(f"Unable to find match for {node.state} in 5-8 database")
        
        return solutions_1_4[str(state_1_4)] + solutions_5_8[str(state_5_8)]
    
    printAStar(slidingPiecesProblem, DBheuristic)
    






