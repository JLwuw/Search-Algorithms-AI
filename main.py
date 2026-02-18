from argparse import ArgumentError
from enum import IntEnum, auto
from problem import GraphProblem
from searchAlgorithm import uniformCostSearch, aStarSearch, iterativeDeepeningSearch, bidirectionalUCSearch

# Define problem graph
class City(IntEnum):
    ELMIRA = auto()
    ITHACA = auto()
    BINGHAMTON = auto()
    SYRACUSE = auto()
    ALBANY = auto()
    STROUDSBURG = auto()
    PATERSON = auto()
    NEW_YORK_CITY = auto()
    NEWARK = auto()
    TRENTON = auto()
    PHILADELPHIA = auto()
    LANCASTER = auto()
    HARRISBURG = auto()
    WILLIAMSPORT = auto()
    SCRANTON = auto()
    WILKES_BARRE = auto()
    ALLENTOWN = auto()

graph = {
    City.ELMIRA: {
        City.ITHACA: 60,
        City.WILLIAMSPORT: 80,
    },
    City.ITHACA: {
        City.ELMIRA: 60,
        City.BINGHAMTON: 80,
    },
    City.BINGHAMTON: {
        City.ITHACA: 80,
        City.SYRACUSE: 110,
        City.ALBANY: 220,
        City.SCRANTON: 95,
    },
    City.SYRACUSE: {
        City.BINGHAMTON: 110,
        City.ALBANY: 200,
    },
    City.ALBANY: {
        City.SYRACUSE: 200,
        City.BINGHAMTON: 220,
        City.STROUDSBURG: 190,
    },
    City.SCRANTON: {
        City.BINGHAMTON: 95,
        City.WILKES_BARRE: 30,
        City.WILLIAMSPORT: 140,
        City.HARRISBURG: 175,
        City.ALLENTOWN: 120,
    },
    City.WILKES_BARRE: {
        City.SCRANTON: 30,
        City.STROUDSBURG: 105,
        City.ALLENTOWN: 95,
    },
    City.STROUDSBURG: {
        City.WILKES_BARRE: 105,
        City.ALBANY: 190,
        City.PATERSON: 90,
    },
    City.PATERSON: {
        City.STROUDSBURG: 90,
        City.NEW_YORK_CITY: 35,
    },
    City.NEW_YORK_CITY: {
        City.PATERSON: 35,
        City.NEWARK: 25,
        City.TRENTON: 95
    },
    City.NEWARK: {
        City.NEW_YORK_CITY: 25,
        City.ALLENTOWN: 130,
    },
    City.ALLENTOWN: {
        City.WILKES_BARRE: 95,
        City.SCRANTON: 120,
        City.NEWARK: 130,
        City.TRENTON: 80,
        City.PHILADELPHIA: 90,
    },
    City.TRENTON: {
        City.ALLENTOWN: 80,
        City.NEW_YORK_CITY: 95,
        City.PHILADELPHIA: 50,
    },
    City.PHILADELPHIA: {
        City.TRENTON: 50,
        City.ALLENTOWN: 90,
        City.LANCASTER: 110,
        City.HARRISBURG: 160
    },
    City.LANCASTER: {
        City.PHILADELPHIA: 110,
        City.HARRISBURG: 60,
    },
    City.HARRISBURG: {
        City.LANCASTER: 60,
        City.WILLIAMSPORT: 135,
        City.SCRANTON: 175,
        City.PHILADELPHIA: 160
    },
    City.WILLIAMSPORT: {
        City.ELMIRA: 80,
        City.SCRANTON: 140,
        City.HARRISBURG: 135,
    },
}

# Define heuristic function for A star search
# h(n) = the straight line distance between node.state and New York City. For a different goal, you must define a new function
def heuristic(node):
    if  node.state == City.ELMIRA:
        return 166
    elif node.state == City.ITHACA:
        return 144
    elif node.state == City.BINGHAMTON:
        return 119
    elif node.state == City.SYRACUSE:
        return 104
    elif node.state == City.ALBANY:
        return 63
    elif node.state == City.SCRANTON:
        return 121
    elif node.state == City.WILKES_BARRE:
        return 73
    elif node.state == City.ALLENTOWN:
        return 53
    elif node.state == City.STROUDSBURG:
        return 46
    elif node.state == City.PATERSON:
        return 21
    elif node.state == City.NEWARK:
        return 25
    elif node.state == City.TRENTON:
        return 45
    elif node.state == City.PHILADELPHIA:
        return 63
    elif node.state == City.LANCASTER:
        return 110
    elif node.state == City.HARRISBURG:
        return 117
    elif node.state == City.WILLIAMSPORT:
        return 134
    elif node.state == City.NEW_YORK_CITY:
        return 0
    else:
        raise ArgumentError(f"Straight line distance from {node.state} to City.NEW_YORK_CITY not defined in heuristic")

def printUCS(problem):
    solution, nodesGenerated = uniformCostSearch(problem)
    route = solution.path()
    routeClean = " -> ".join([node.state.name for node in route])
    print("========================================")
    print("Uniform Cost Search")
    print("========================================")
    print(f"1. Mejor ruta: {routeClean}")
    print(f"2. Costo total: {solution.pathCost} km")
    print(f"3. Nodos generados: {nodesGenerated}\n\n")

def printAStar(problem, heuristic):
    solution, nodesGenerated = aStarSearch(problem, heuristic)
    route = solution.path()
    routeClean = " -> ".join([node.state.name for node in route])
    print("========================================")
    print("Busqueda A*")
    print("========================================")
    print(f"1. Mejor ruta: {routeClean}")
    print(f"2. Costo total: {solution.pathCost} km")
    print(f"3. Nodos generados: {nodesGenerated}\n\n")

def printIDS(problem):
    solution, nodesGenerated = iterativeDeepeningSearch(problem)
    route = solution.path()
    routeClean = " -> ".join([node.state.name for node in route])
    print("========================================")
    print("Busqueda en Profundidad Iterativa")
    print("========================================")
    print(f"1. Mejor ruta: {routeClean}")
    print(f"2. Costo total: {solution.pathCost} km")
    print(f"3. Nodos generados: {nodesGenerated}\n\n")

def printBIUCS(forwardProblem, backwardProblem):
    solution, nodesGenerated = bidirectionalUCSearch(forwardProblem, backwardProblem)
    route = solution.path()
    routeClean = " -> ".join([node.state.name for node in route])
    print("========================================")
    print("Uniform Cost Search Bidireccional:")
    print("========================================")
    print(f"1. Mejor ruta: {routeClean}")
    print(f"2. Costo total: {solution.pathCost} km")
    print(f"3. Nodos generados: {nodesGenerated}\n\n")

if __name__ == "__main__":
    initial = City.ELMIRA
    goal = City.NEW_YORK_CITY
    problem = GraphProblem(initial, goal, graph)
    backwardProblem = GraphProblem(goal, initial, graph)  # For bidirectional search, we need a problem definition for the backward search as well

    # printUCS(problem)
    printIDS(problem)
    printBIUCS(problem, backwardProblem)
    printAStar(problem, heuristic)

