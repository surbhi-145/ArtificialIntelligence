from Search.setup import *
import random


class EightPuzzle(Problem):

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['LEFT', 'RIGHT', 'UP', 'DOWN']
        blank_square = self.find_blank_square(state)

        if blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if blank_square >= 6:
            possible_actions.remove('DOWN')
        if blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if blank_square <= 2:
            possible_actions.remove('UP')

        return possible_actions

    def result(self, state, action):
        blank_square = self.find_blank_square(state)
        new_state = list(state)

        delta = {'LEFT': -1, 'RIGHT': 1, 'UP': -3, 'DOWN': 3}  # to calculate new indices of the blank square
        neighbour = blank_square + delta[action]
        new_state[blank_square], new_state[neighbour] = new_state[neighbour], new_state[blank_square]
        return tuple(new_state)

    def check_solvability(self, state):
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] > state[j] != 0 and state[i] != 0:
                    inversion += 1
        return inversion % 2 == 0


def print_problem():
    print("The 8 Puzzle Problem consists of a 3x3 tray in which the goal is to get the initial configuration to the "
          "goal state by shifting the numbered tiles into the blank space.")


def printSolution(path):
    for x in path:
        print(x.state)


if __name__ == '__main__':
    print_problem()
    initial_state = (2, 4, 3, 1, 5, 6, 7, 8, 0)
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    puzzle = EightPuzzle(initial_state,goal_state)
    if puzzle.check_solvability(initial_state):
        solution = uniform_cost_search(puzzle)
        if solution:
            printSolution(solution.path())

