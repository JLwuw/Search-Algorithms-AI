# Definition of problem we are trying to solve

# Abstract Problem Class
class Problem:
    def __init__(self, initial, goal):  # Constructor
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

    # Returns list of all reachable states from a given state
    def actions(self, state):
        raise NotImplementedError

    # Given a state and an action, returns the next state
    def result(self, state, action):
        raise NotImplementedError
    
    # Returns the path cost of a new node reached by using action from oldNode
    def calcPathCost(self, oldNode, action):
        raise NotImplementedError

    # Tests if the given state is among the goal states
    def goal_test(self, state):
        if isinstance(self.goal, list):
            return state in self.goal
        else:
            return state == self.goal


# Problem defined via graph
class GraphProblem(Problem):
    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        # Graph must be expressed as a nested dictionary. (all vertex weights = 1 if unweighted graph)
        self.graph = graph

    # Returns list of all reachable states from a given state
    def actions(self, state):
        return list(self.graph.get(state, {}).keys())

    # Given a state and an action, returns the next state
    def result(self, state, action):
        return action

    # Calculates the path cost of a new node reached by using action from oldNode
    def calcPathCost(self, oldNode, action):
        return oldNode.pathCost + self.graph[oldNode.state][action]