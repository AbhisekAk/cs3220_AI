from src.environmentClass import Environment
from src.asteroid_environment import AsteroidEnvironment
from src.asteroidProblemSolvingAgentSMART import AsteroidProblemSolvingAgentSMART
from src.PS_agentPrograms import BestFirstSearchAgentProgram, IDSearchAgentProgram

def run_agent(env, agent, label):
    print(f"\n🚀 Running {label} Agent...")
    environment = Environment()
    environment.add_thing(agent)

    step = 0
    max_steps = 100  # Safety limit in case of infinite loops

    while agent.alive and step < max_steps:
        step += 1
        print(f"\nstep {step}:\n")
        environment.step()

        # ✅ Check the agent's position in the environment
        if hasattr(agent, "location") and agent.location == env.goal:
            print(f"🏁 {label} Agent reached the goal at {agent.location} in {step} steps!")
            break

    else:
        print(f"⚠️ {label} Agent did not reach the goal within {max_steps} steps.")


def main():
    env = AsteroidEnvironment()
    print("\n🪐 Environment Generated:")
    print(env.grid)
    print(f"🚩 Start: {env.start} | 🎯 Goal: {env.goal}")

    # UCS Agent
    UCS_program = BestFirstSearchAgentProgram()
    agent_ucs = AsteroidProblemSolvingAgentSMART(
        initial_state=env.start,
        environment=env,
        goal=env.goal,
        program=UCS_program
    )

    # IDS Agent
    IDS_program = IDSearchAgentProgram()
    agent_ids = AsteroidProblemSolvingAgentSMART(
        initial_state=env.start,
        environment=env,
        goal=env.goal,
        program=IDS_program
    )

    # Run both agents
    run_agent(env, agent_ucs, "UCS")
    run_agent(env, agent_ids, "IDS")


if __name__ == "__main__":
    main()
