# Definition of problem we are trying to solve

# Abstract Problem Class
class Problem:
    def __init__(self, initial, goal=None):  # Constructor
        self.initial = initial
        self.goal = goal

    # Returns list of all reachable states from a given state
    def actions(self, state):
        raise NotImplementedError

    # Given a state and an action, returns the next state
    def result(self, state, action):
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