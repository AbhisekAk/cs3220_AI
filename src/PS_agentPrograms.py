from src.navigation_search import uniform_cost_search, iterative_deepening_search

def BestFirstSearchAgentProgram():
    def program(problem):
        return uniform_cost_search(problem)
    return program

def IDSearchAgentProgram():
    def program(problem):
        return iterative_deepening_search(problem)
    return program
