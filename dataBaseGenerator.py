# Generate database for 8 piece puzzle subproblems
# We will define two subproblems: one board with just pieces 1-4 and one board with just pieces 5-8

from itertools import combinations, permutations
from problem import SlidingPiecesProblem
from searchAlgorithm import aStarSearch
import json
import os

def exportToJSON(database, filename, folder="data"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    
    with open(filepath, 'w') as f:
        json.dump(database, f, indent=4)
    
    print(f"Exported {len(database)} solutions to {filepath}")


def generateDB_1_4():
    # Generate all initial states for 1-4 subproblem
    goal_1_4 = (1, 2, 3, 4, 0, 0, 0, 0, 0)
    initial_1_4 = []
    for positions in combinations(range(9), 4):
        for pieces_perm in permutations([1, 2, 3, 4]):
            state = [0] * 9
            for pos, piece in zip(positions, pieces_perm):
                state[pos] = piece
            initial_1_4.append(tuple(state))

    # Calculate costs for 1-4 subproblem
    database_1_4 = {}
    for initial in initial_1_4:
        problem = SlidingPiecesProblem(initial, goal_1_4)
        heuristic = problem.manhattanHeuristic()
        solution, _ = aStarSearch(problem, heuristic)
        
        if solution:
            database_1_4[str(initial)] = solution.pathCost
        else:
            database_1_4[str(initial)] = float('inf')
    
    exportToJSON(database_1_4, "solutions_1_4.json")


def generateDB_5_8():
    # Generate all initial states for 5-8 subproblem
    goal_5_8 = (0, 0, 0, 0, 5, 6, 7, 8, 0)
    initial_5_8 = []
    for positions in combinations(range(9), 4):
        for pieces_perm in permutations([5, 6, 7, 8]):
            state = [0] * 9
            for pos, piece in zip(positions, pieces_perm):
                state[pos] = piece
            initial_5_8.append(tuple(state))

    # Calculate costs for 5-8 subproblem
    database_5_8 = {}
    for initial in initial_5_8:
        problem = SlidingPiecesProblem(initial, goal_5_8)
        heuristic = problem.manhattanHeuristic()
        solution, _ = aStarSearch(problem, heuristic)
        
        if solution:
            database_5_8[str(initial)] = solution.pathCost
        else:
            database_5_8[str(initial)] = float('inf')
    
    exportToJSON(database_5_8, "solutions_5_8.json")