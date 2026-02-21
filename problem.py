# Definition of problem we are trying to solve
import math

# Abstract Problem Class
class Problem:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

        # State must define __hash__ and __lt__ functions for the search algorithms to work properly        
        self._validate_state(self.initial, "initial")
        if isinstance(self.goal, list):
            for idx, g in enumerate(self.goal):
                    self._validate_state(g, f"goal[{idx}]")
        else:
            self._validate_state(self.goal, "goal")

    def _validate_state(self, state, name):
        if state is None:
            raise ValueError(f"{name} state must not be None")
        
        try:
            hash(state)
        except TypeError:
            raise TypeError(f"{name} state must be hashable (implement __hash__)")

        try:
            _ = state < state
        except TypeError:
            raise TypeError(f"{name} state must implement ordering (define __lt__)")

    # Returns list of all possible actions from a given state
    def actions(self, state):
        raise NotImplementedError

    # Given a state and an action, returns the next state
    def result(self, state, action):
        raise NotImplementedError
    
    # Returns the path cost of the new node reached by using action from oldNode
    def calcPathCost(self, oldNode, action):
        raise NotImplementedError

    # Tests if the given state is among the goal states
    def goal_test(self, state):
        if isinstance(self.goal, list):
            return state in self.goal
        else:
            return state == self.goal


# Problem defined via graph (e.g. road map, social network, etc.)
# Graph must be expressed as a nested dictionary. (all vertex weights equal if unweighted graph)
# State is represented by the key of the node the graph dictionary (e.g. 'A', 'B', 'C', etc.)
# Action is represented by the key of the node to move to (e.g. 'A', 'B', 'C', etc.)
class GraphProblem(Problem):
    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)

        if not isinstance(graph, dict):
            raise ValueError("Graph must be a dictionary")
        
        if initial not in graph or goal not in graph:
            raise ValueError("Initial and Goal state must be a key in the graph")

        self.graph = graph

    # Returns list of all possible actions from a given state
    def actions(self, state):
        return list(self.graph.get(state, {}).keys())

    # Given a state and an action, returns the next state
    def result(self, state, action):
        return action

    # Calculates the path cost of the new node reached by using action from oldNode
    def calcPathCost(self, oldNode, action):
        return oldNode.pathCost + self.graph[oldNode.state][action]


# Sliding pieces problem
# Works for any n x n grid of pieces (e.g. 3x3 for 8-puzzle, 4x4 for 15-puzzle, etc.)
# State is represented as an tuple of ints (e.g. [1, 2, 3, 4, 0, 5, 7, 8, 6] for 8-puzzle) where 0 represents the blank piece
# Action is represented as the index of the blank piece and the piece to swap with (e.g. (blank_idx, swap_idx))
class SlidingPiecesProblem(Problem):
    def __init__(self, initial, goal):
        initial = tuple(initial)
        goal = tuple(goal)

        super().__init__(initial, goal)

        if len(initial) != len(goal):
            raise ValueError("Initial and Goal states must have the same dimensions for sliding pieces problem.")
        
        if len(initial) < 4:
            raise ValueError("Sliding pieces problem must have at least 4 pieces.")

        if not self.is_perfect_square(len(initial)):
            raise ValueError("Number of spaces in sliding pieces problem must be a perfect square (e.g. 4, 9, 16, etc.).")  
        
        # Check if both states have the same pieces
        initial_pieces = sorted(initial)
        goal_pieces = sorted(goal)
        
        if initial_pieces != goal_pieces:
            raise ValueError("Initial and Goal states must contain the same pieces for sliding pieces problem.")
        
        self.gridSize = math.isqrt(len(initial))
    
    # Returns list of all possible actions from a given state
    def actions(self, state):
        actions = []
        blank_idxs = [idx for idx, val in enumerate(state) if val == 0]

        for idx in blank_idxs:
            # Up
            if idx >= self.gridSize and state[idx - self.gridSize] != 0:
                actions.append((idx, idx - self.gridSize))
            # Down
            if idx < len(state) - self.gridSize and state[idx + self.gridSize] != 0:
                actions.append((idx, idx + self.gridSize))
            # Left
            if idx % self.gridSize != 0 and state[idx - 1] != 0:
                actions.append((idx, idx - 1))
            # Right
            if idx % self.gridSize != self.gridSize - 1 and state[idx + 1] != 0:
                actions.append((idx, idx + 1))

        return actions

    # Given a state and an action, returns the next state
    def result(self, state, action):
        new_state = list(state)
        blank_idx, swap_idx = action
        new_state[blank_idx] = new_state[swap_idx]
        new_state[swap_idx] = 0
        return tuple(new_state)
    
    # Returns the path cost of the new node reached by using action from oldNode
    def calcPathCost(self, oldNode, action):
        return oldNode.pathCost + 1
    
    # Returns a heuristic function calculated as the sum of Manhattan distances of each piece from its goal position
    def manhattanHeuristic(self):
        def heuristic(node):
            total = 0
            for idx, piece in enumerate(node.state):
                if piece != 0:
                    goal_idx = self.goal.index(piece)
                    total += abs(idx // self.gridSize - goal_idx // self.gridSize) + abs(idx % self.gridSize - goal_idx % self.gridSize)
            return total
        
        return heuristic

    @staticmethod
    def is_perfect_square(n):
        if n <= 0:
            return False
        root = math.isqrt(n)
        return root * root == n

