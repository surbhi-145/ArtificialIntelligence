import sys

import numpy as np
from utils import *
from collections import *

from Search.utils import PriorityQueue

'''
Classes for basic implementation : 
    - Problem 
    - Node 
UnInformed Search :
    - Breadth First Search
    - Depth First Search
    - Iterative Deepening Search
    - Depth Limited Search 
    - Best First Search 
    - Uniform Cost Search 
    - Bidirectional Search (TODO)
Informed Search : 
    - Greedy Best First Search f(n) = h(n)    
    - A* Search
    - Recursive Best First Search
    
'''


class Problem:

    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1


class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self, action, next_state))
        return next_node

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def __lt__(self, node):
        return self.state < node.state


def breadth_first_search(problem):
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node

    frontier = deque([node])
    explored = set()

    while frontier:
        node = frontier.popleft()
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                if problem.goal_test(child.state):
                    return child
                frontier.append(child)
    return None


def depth_first_search(problem):
    node = Node(problem.initial)
    frontier = [node]  # stack
    explored = set()

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and child not in frontier)
    return None


def depth_limited_search(problem, limit=50):
    def recursive_dls(node, _problem, _limit):

        if _problem.goal_test(node.state):
            return node
        elif _limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(_problem):
                result = recursive_dls(child, _problem, _limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
                return 'cutoff' if cutoff_occurred else None

    return recursive_dls(Node(problem.initial), problem, limit)


def iterative_deepening_search(problem):
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result


def best_first_search(problem, f):
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del (frontier[child])
                    frontier.append(child)
    return None


def uniform_cost_search(problem):
    return best_first_search(problem, lambda node: node.path_cost)


def bidirectional_search(problem):
    raise NotImplementedError


def a_star_search(problem, h=None):
    return best_first_search(problem, lambda n: n.path_cost + h(n))


def recursive_best_first_search(problem, h=None):

    def RBFS(_problem, node, flimit):
        if _problem.goal_test(node.state):
            return node, 0
        successors = node.expand(_problem)
        if len(successors) == 0:
            return Node, np.inf
        for s in successors:
            s.f = max(s.path_cost + h(s), node.f)
        while True:
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > flimit:
                return None, np.inf
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = np.inf
            result, best.f = RBFS(_problem, best, min(flimit, alternative))
            if result is not None:
                return result, best.f

    node = Node(problem.initial)
    node.f = h(node)
    result, best_f = RBFS(problem, node, np.inf)
    return result