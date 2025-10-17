from src.nodeClass import Node
from queue import PriorityQueue

nodeColors = {
    "start": "red",
    "goal": "green",
    "frontier": "orange",
    "expanded": "pink"
}


# ======================================================
#   UNIFORM COST SEARCH  (Best-First with f(n) = g(n))
# ======================================================
def BestFirstSearchAgentProgram(f=None):
    """
    Uniform Cost Search (Best-First Search using path cost)
    """
    def program(problem):
        node = Node(problem.initial)
        node.color = nodeColors["start"]

        frontier = PriorityQueue()
        frontier.put((0, node))
        reached = {problem.initial: node}

        print(f"Starting Uniform Cost Search from {problem.initial} → {problem.goal}")

        while not frontier.empty():
            cost, node = frontier.get()
            node.color = nodeColors["expanded"]

            print(f"Expanding {node.state} with path cost {node.path_cost}")

            if problem.goal_test(node.state):
                node.color = nodeColors["goal"]
                print(f"✅ Goal reached: {node.state}")
                return node

            for child in node.expand(problem):
                if (child.state not in reached or 
                        child.path_cost < reached[child.state].path_cost):
                    reached[child.state] = child
                    frontier.put((child.path_cost, child))
                    child.color = nodeColors["frontier"]
                    print(f"  Added to frontier: {child.state} (cost={child.path_cost})")

        print("❌ No path found (UCS)")
        return None

    return program



# ======================================================
#   ITERATIVE DEEPENING SEARCH (Depth-Limited + Repeat)
# ======================================================
def IDSearchAgentProgram(f=None):
    """
    Iterative Deepening Search (IDS)
    """
    def program(problem):

        def depth_limited_search(node, problem, limit):
            """
            Recursive helper for depth-limited search.
            """
            print(f"Visiting {node.state} at depth {node.depth}")

            if problem.goal_test(node.state):
                print(f"✅ Goal found: {node.state}")
                return node

            elif limit == 0:
                return "cutoff"

            cutoff_occurred = False
            for child in node.expand(problem):
                result = depth_limited_search(child, problem, limit - 1)
                if result == "cutoff":
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return "cutoff" if cutoff_occurred else None


        # Iteratively deepen until goal is found
        depth = 0
        while True:
            print(f"\nStarting depth-limited search with limit = {depth}")
            root = Node(problem.initial)
            result = depth_limited_search(root, problem, depth)

            if result == "cutoff":
                depth += 1  # increase limit
            elif result is not None:
                print(f"Goal reached at depth {depth}: {result.state}")
                return result
            else:
                print("❌ No solution found.")
                return None

    return program
