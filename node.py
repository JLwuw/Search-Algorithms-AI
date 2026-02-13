# Node in search tree

class Node:
    def __init__(self, state, parent=None, action=None, pathCost=0):
        self.state = state # state of the problem
        self.parent = parent # previous node in search tree
        self.action = action # action used to reach this node
        self.pathCost = pathCost # g(n)

        # Depth in the search tree
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

    # Given the problem definition, returns all reachable nodes from this node
    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in
                problem.actions(self.state)]

    # Given an action and the problem definition, returns the next node
    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.calcPathCost(self, action))
        return next_node

    # Returns the path from the initial node to this node
    def path(self):
        node, path_back = self, []
        while node is not None:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # Verifies if current search path is a cycle
    def inCycle(self):
        ancestor = self.parent
        while ancestor is not None:
            if ancestor.state == self.state:
                return True
            ancestor = ancestor.parent
        return False

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    # Tiebreaker in case of equal path cost values
    def __lt__(self, node):
        return self.state.value < node.state.value

    def __hash__(self):
        return hash(self.state)
