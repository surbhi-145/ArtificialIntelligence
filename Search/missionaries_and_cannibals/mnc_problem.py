'''
class MCObject:
    def __init__(self, left, right, direction):
        self.left = left
        self.right = right
        self.direction = direction
'''


class MnCProblem(Problem):
    def actions(self, state):
        possible_actions = [[1, 0, 1], [2, 0, 1], [1, 1, 1], [0, 2, 1], [0, 1, 1]]
        valid_actions = []
        for action in possible_actions:

            if state[2] == 1:
                if (state[0] - action[0] >= 0) and (state[1] - action[1] >= 0):
                    rm = state[0] - action[0]
                    rc = state[1] - action[1]
                    lm = 3 - rm
                    lc = 3 - rc
                    if (rm == 0 and lm >= lc) or (lm == 0 and rm >= rc) or ((rm >= rc) and (lm >= lc)):
                        valid_actions.append(action)
            else:
                if (state[0] + action[0] <= 3) and (state[1] + action[1] <= 3):
                    rm = state[0] + action[0]
                    rc = state[1] + action[1]
                    lm = 3 - rm
                    lc = 3 - rc
                    if (rm == 0 and lm >= lc) or (lm == 0 and rm >= rc) or ((rm >= rc) and (lm >= lc)):
                        valid_actions.append(action)

        return valid_actions

    def result(self, state, action):
        state = list(state)
        if state[2] == 1:
            state[0] = state[0] - action[0]
            state[1] = state[1] - action[1]
            state[2] = 0
        else:
            state[0] = state[0] + action[0]
            state[1] = state[1] + action[1]
            state[2] = 1

        self.state = tuple(state)
        return self.state


def print_problem():
    print("Three missionaries and three cannibals are on one side of the river(let's assume right side), along with a "
          "boat that can hold one or two people.")
    print("We must find a way to get everyone on the other side(i.e left side) without ever leaving missionaries "
          "outnumbered by cannibals.\n")


def printSolution(path):
    print("Left    |    Right\n")
    for x in path:
        print('(' + str(3 - x.state[0]) + ',' + str(3 - x.state[1]) + ')    |    (' + str(x.state[0]) + ',' + str(
            x.state[1]) + ')')


if __name__ == '__main__':
    print_problem()
    initial_state = tuple([3, 3, 1])
    goal_state = tuple([0, 0, 0])
    problem = MnCProblem(initial_state, goal_state)
    s = breadth_first_search(problem)
    if s:
        printSolution(s.path())

    else:
        print("No solution . You are wrong.")
