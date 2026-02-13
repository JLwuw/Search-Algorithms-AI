# Algorithms used to explore search tree
# Current implementation assumes a consistent heuristic function for informed search algorithms

from queue import PriorityQueue, LifoQueue
from node import Node


def bestFirstSearch(problem, f):
    initialNode = Node(problem.initial)
    frontier = PriorityQueue()
    frontier.put((f(initialNode), initialNode))

    # Dictionary with Key = previously seen states and Value = least expensive associated node
    explored = {initialNode.state: initialNode}

    nodesGenerated = 0

    while not frontier.empty():
        _, node = frontier.get()  # pop node with the least cost

        # Goal state found
        if problem.goal_test(node.state):
            return node, nodesGenerated

        # Expand current node
        for child in node.expand(problem):
            nodesGenerated += 1
            if child.state not in explored or child.pathCost < explored[child.state].pathCost:
                explored[child.state] = child  # Add children to list of seen nodes
                frontier.put((f(child), child))

    return None


# Best First where f(n) = g(n)
def uniformCostSearch(problem):
    return bestFirstSearch(problem, lambda node: node.pathCost)


# Best First where f(n) = g(n) + h(n)
def aStarSearch(problem, h):
    return bestFirstSearch(problem, lambda node: node.pathCost + h(node))


# DFS with a maximum tree depth of l
def depthLimitedSearch(problem, l):
    initialNode = Node(problem.initial)

    frontier = LifoQueue()
    frontier.put(initialNode)
    result = "failure"

    nodesGenerated = 0

    while not frontier.empty():
        node = frontier.get()

        # Goal state found
        if problem.goal_test(node.state):
            return node, "success", nodesGenerated

        # Depth limit reached
        if node.depth > l:
            result = "cutoff"

        elif not node.inCycle():
            for child in node.expand(problem):
                nodesGenerated += 1
                frontier.put(child)

    return None, result, nodesGenerated


def iterativeDeepeningSearch(problem):
    l = 0
    totalNodesGenerated = 0
    while True:
        node, result, nodesGenerated = depthLimitedSearch(problem, l)
        totalNodesGenerated += nodesGenerated

        if result != "cutoff":
            return node, totalNodesGenerated
        l += 1


def bidirectionalBFSearch(problemForward, fForward, problemBackward, fBackward):
    # Once a solution is found, joins the forward and backward paths into a single path
    def joinNodes(forwardNode, backwardNode, problem):
        backwardPath = backwardNode.path()
        backwardPath.pop() # remove common node
        backwardPath.reverse()

        previousNode = forwardNode

        for node in backwardPath:
            newState = node.state
            newCost = problem.calcPathCost(previousNode, newState)
            newNode = Node(newState, parent=previousNode, action=newState, pathCost=newCost)
            previousNode = newNode
        
        return previousNode

    # Handles both Forward and Backward expansion. True = Forward. False = Backward
    def proceed(dir, problem, frontier, explored, f, otherExplored, solution, generatedNodes):
        _, node = frontier.get()

        for child in node.expand(problem):
            generatedNodes += 1
            if child.state not in explored or child.pathCost < explored[child.state].pathCost:
                explored[child.state] = child
                frontier.put((f(child), child))

                if child.state in otherExplored:
                    if dir:
                        newSolution = joinNodes(child, otherExplored[child.state], problem)
                    else:
                        newSolution = joinNodes(otherExplored[child.state], child, problem)

                    if solution is None or newSolution.pathCost < solution.pathCost:
                        solution = newSolution

        return solution, generatedNodes

    # Determines when the algorithm shoud stop
    def terminated(solution, frontierForward, frontierBackward):
        if frontierForward.empty() or frontierBackward.empty():
            return True
        if solution is None:
            return False
        if solution.pathCost <= frontierForward.queue[0][0] + frontierBackward.queue[0][0]:
            return True
        
        return False

    initialForward = Node(problemForward.initial)
    frontierForward = PriorityQueue()
    frontierForward.put((fForward(initialForward), initialForward))
    exploredForward = {initialForward.state: initialForward}


    initialBackward = Node(problemBackward.initial)
    frontierBackward = PriorityQueue()
    frontierBackward.put((fBackward(initialBackward), initialBackward))
    exploredBackward = {initialBackward.state: initialBackward}

    solution = None
    generatedNodes = 0

    while not terminated(solution, frontierForward, frontierBackward):
        if frontierForward.queue[0][0] < frontierBackward.queue[0][0]:
            solution, generatedNodes = proceed(True, problemForward, frontierForward, exploredForward, fForward, exploredBackward, solution, generatedNodes)
        else:
            solution, generatedNodes = proceed(False, problemBackward, frontierBackward, exploredBackward, fBackward, exploredForward, solution, generatedNodes)

    return solution, generatedNodes


def bidirectionalUCSearch(problemForward, problemBackward):
    return bidirectionalBFSearch(problemForward, lambda node: node.pathCost, problemBackward, lambda node: node.pathCost)

# Helper function to print contents of a PriorityQueue (for debugging purposes)
def print_pq(pq):
    for priority, node in pq.queue:
        print(f"priority={priority}, state={node.state}, g={node.pathCost}", end=" | ")
