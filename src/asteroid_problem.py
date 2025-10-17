from collections import namedtuple

Action = namedtuple("Action", ["name", "delta", "cost"])

ACTIONS = {
    0: Action("left", (0, -1), 2),
    1: Action("up", (-1, 0), 4),
    2: Action("right", (0, 1), 2),
    3: Action("down", (1, 0), 1)
}

class AsteroidMazeProblem:
    """Defines the search problem for the agent."""
    def __init__(self, environment):
        self.env = environment
        self.initial = environment.start
        self.goal = environment.goal

    def actions(self, state):
        r, c = state
        possible = []
        for k, a in ACTIONS.items():
            nr, nc = r + a.delta[0], c + a.delta[1]
            if self.env.is_free(nr, nc):
                possible.append(k)
        return possible

    def result(self, state, action):
        a = ACTIONS[action]
        r, c = state
        return (r + a.delta[0], c + a.delta[1])

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, cost_so_far, state1, action, state2):
        a = ACTIONS[action]
        return cost_so_far + a.cost
