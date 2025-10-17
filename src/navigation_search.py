from src.nodeClass import Node
import heapq

# ✅ Uniform Cost Search (UCS)
def uniform_cost_search(problem):
    frontier = []
    start_node = Node(problem.initial)
    heapq.heappush(frontier, (0, start_node))
    explored = {}

    while frontier:
        cost, node = heapq.heappop(frontier)

        # Skip if already explored cheaper
        if node.state in explored and explored[node.state] <= cost:
            continue

        explored[node.state] = cost

        # ✅ Goal check
        if problem.goal_test(node.state):
            node.path_cost = cost
            return node  # ✅ Return goal node

        # Expand children
        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            new_cost = problem.path_cost(node.path_cost, node.state, action, child_state)
            child_node = Node(child_state, node, action, new_cost)
            heapq.heappush(frontier, (new_cost, child_node))

    return None  # No solution


# ✅ Iterative Deepening Search (IDS)
def iterative_deepening_search(problem):
    def depth_limited_search(node, limit):
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return None
        else:
            for action in problem.actions(node.state):
                child_state = problem.result(node.state, action)
                child = Node(child_state, node, action)
                result = depth_limited_search(child, limit - 1)
                if result is not None:
                    return result
        return None

    depth = 0
    while True:
        result = depth_limited_search(Node(problem.initial), depth)
        if result is not None:
            return result  # ✅ Return goal node (for path + cost tracking)
        depth += 1
