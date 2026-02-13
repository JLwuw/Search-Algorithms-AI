# Algorithms used to explore search tree

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

    def joinNodes(forwardNode, backwardNode, problem):
        currentForwardNode = forwardNode
        currentBackwardNode = backwardNode

        while currentBackwardNode.parent is not None:
            backwardAncestor = currentBackwardNode.parent
            backwardAncestor.parent = forwardNode
            backwardAncestor.pathCost = problemForward.calcPathCost(currentForwardNode, backwardAncestor.state)

            currentForwardNode = backwardAncestor
            currentBackwardNode = backwardAncestor
            
        return currentBackwardNode.pathCost

    # Handles both Forward and Backward expansion. True = Forward. False = Backward
    def proceed(dir, problem, frontier, explored, f, otherExplored, solution):
        _, node = frontier.get()

        for child in node.expand(problem):
            if child.state not in explored or child.pathCost < explored[child.state].pathCost:
                explored[child.state] = child
                frontier.put(f(child), child)

                if child.state in otherExplored:
                    if dir:
                        newSolution = joinNodes(child, otherExplored[child.state], problem)
                    else:
                        newSolution = joinNodes(otherExplored[child.state], child, problem)

                    if solution is not None and solution.pathCost < solution.pathCost:
                        solution = newSolution

        return solution

    def terminated(solution, frontierForward, frontierBackward):
        if solution <= frontierForward.queue[0] + frontierBackward.queue[0]:
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

    while not terminated(solution, frontierForward, frontierBackward):
        if frontierForward.queue[0] < frontierBackward.queue[0]:
            solution = proceed(True, problemForward, frontierForward, exploredForward, fForward, exploredBackward, solution)
        else:
            solution = proceed(False, problemBackward, frontierBackward, exploredBackward, fBackward, exploredForward, solution)

    return solution