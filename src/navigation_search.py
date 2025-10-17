
from src.asteroid_environment import AsteroidEnvironment
from src.asteroid_problem import AsteroidMazeProblem
from src.satellite_agent import SatelliteAgent
from src.PS_agentPrograms import BestFirstSearchAgentProgram, IDSearchAgentProgram
import matplotlib.pyplot as plt




def simulate(agent, env, path):
    """Move agent through environment, handling enemies."""
    for step in path[1:]:
        agent.move(step)
        if step in env.enemies:
            enemy = env.enemies[step]
            alive = agent.encounter_enemy(enemy)
            if not alive:
                print(f"Agent destroyed by enemy (power={enemy.power}) at {step}")
                break


def main():
    env = AsteroidEnvironment()
    problem = AsteroidMazeProblem(env)

    total_nodes = env.rows * env.cols
    initial_performance = int(0.5 * total_nodes)

    # Agents
    agent_ucs = SatelliteAgent(env.start, initial_performance)
    agent_ids = SatelliteAgent(env.start, initial_performance)

    # Agent programs
    UCS_program = BestFirstSearchAgentProgram()
    IDS_program = IDSearchAgentProgram()

    # Run search
    node_ucs = UCS_program(problem)
    node_ids = IDS_program(problem)

    # Reconstruct paths
    path_ucs = []
    n = node_ucs
    while n:
        path_ucs.append(n.state)
        n = n.parent
    path_ucs.reverse()

    path_ids = []
    n = node_ids
    while n:
        path_ids.append(n.state)
        n = n.parent
    path_ids.reverse()

    # Simulate
    simulate(agent_ucs, env, path_ucs)
    simulate(agent_ids, env, path_ids)

    print("\n--- RESULTS ---")
    print(f"UCS Path Length: {len(path_ucs)} | Performance: {agent_ucs.performance:.2f} | Alive: {agent_ucs.alive}")
    print(f"IDS Path Length: {len(path_ids)} | Performance: {agent_ids.performance:.2f} | Alive: {agent_ids.alive}")

    env.visualize(path_ucs, title="Uniform Cost Search Path")
    env.visualize(path_ids, title="Iterative Deepening Search Path")

if __name__ == "__main__":
    main()