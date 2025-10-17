import streamlit as st
import matplotlib.pyplot as plt
from src.asteroid_environment import AsteroidEnvironment
from src.asteroid_problem import AsteroidMazeProblem
from src.satellite_agent import SatelliteAgent
from src.PS_agentPrograms import BestFirstSearchAgentProgram, IDSearchAgentProgram
from src.navigation_search import simulate

st.set_page_config(page_title="Asteroid Maze Navigation", page_icon="🛰️", layout="wide")

st.title("🛰️ Satellite Navigation in Asteroid Maze")
st.write("""
This simulation compares two AI search agents navigating through an asteroid field:  
- **Uniform Cost Search (UCS)** — a cost-based best-first search.  
- **Iterative Deepening Search (IDS)** — a depth-limited search approach.
""")

# --- Controls ---
cols = st.columns(2)
with cols[0]:
    seed = st.number_input("Random Seed", min_value=0, max_value=9999, value=42, step=1)
    size = st.slider("Grid Size", 5, 10, 7)
with cols[1]:
    asteroid_ratio = st.slider("Asteroid Ratio", 0.1, 0.5, 0.25)
    enemy_ratio = st.slider("Enemy Ratio", 0.0, 0.3, 0.1)

# --- Environment ---
env = AsteroidEnvironment(size=(size, size), asteroid_ratio=asteroid_ratio, enemy_ratio=enemy_ratio, seed=seed)
problem = AsteroidMazeProblem(env)

total_nodes = env.rows * env.cols
initial_performance = int(0.5 * total_nodes)

agent_ucs = SatelliteAgent(env.start, initial_performance)
agent_ids = SatelliteAgent(env.start, initial_performance)

# --- Show environment ---
st.subheader("🌌 Generated Asteroid Maze")
fig, ax = plt.subplots()
ax.imshow(env.grid, cmap="tab10", origin="upper")
ax.set_title("Initial Maze Configuration")
ax.set_xticks([])
ax.set_yticks([])

# Mark start and goal
ax.text(env.start[1], env.start[0], "S", color="white", ha="center", va="center", fontsize=12, fontweight="bold")
ax.text(env.goal[1], env.goal[0], "G", color="white", ha="center", va="center", fontsize=12, fontweight="bold")
st.pyplot(fig)

# --- Simulation ---
if st.button("🚀 Run Search Simulation"):
    UCS_program = BestFirstSearchAgentProgram()
    IDS_program = IDSearchAgentProgram()

    node_ucs = UCS_program(problem)
    node_ids = IDS_program(problem)

    path_ucs = [n.state for n in node_ucs.path()] if node_ucs else None
    path_ids = [n.state for n in node_ids.path()] if node_ids else None

    if path_ucs:
        simulate(agent_ucs, env, path_ucs)
    if path_ids:
        simulate(agent_ids, env, path_ids)

    # --- Results ---
    st.subheader("📊 Agent Performance")

    if path_ucs:
        st.write(f"**UCS Path Length:** {len(path_ucs)} | Performance: {agent_ucs.performance:.2f} | Alive: {agent_ucs.alive}")
    else:
        st.warning("⚠️ UCS could not find a path.")

    if path_ids:
        st.write(f"**IDS Path Length:** {len(path_ids)} | Performance: {agent_ids.performance:.2f} | Alive: {agent_ids.alive}")
    else:
        st.warning("⚠️ IDS could not find a path.")

    # --- Determine winner ---
    st.subheader("🏆 Winner")
    if agent_ucs.alive and not agent_ids.alive:
        st.success("🏆 UCS Agent Wins!")
    elif agent_ids.alive and not agent_ucs.alive:
        st.success("🏆 IDS Agent Wins!")
    elif agent_ucs.alive and agent_ids.alive:
        winner = "UCS" if agent_ucs.performance >= agent_ids.performance else "IDS"
        st.success(f"Both survived! Winner: {winner}")
    else:
        st.error("💀 Both agents destroyed!")

    # --- Visualize both paths ---
    st.subheader("🛰️ Path Visualization")

    fig, ax = plt.subplots()
    ax.imshow(env.grid, cmap="tab10", origin="upper")
    ax.set_xticks([])
    ax.set_yticks([])

    # UCS path (yellow)
    if path_ucs:
        pr, pc = zip(*path_ucs)
        ax.plot(pc, pr, color="yellow", linewidth=2, label="UCS Path")

    # IDS path (purple)
    if path_ids:
        pr, pc = zip(*path_ids)
        ax.plot(pc, pr, color="purple", linewidth=2, linestyle="--", label="IDS Path")

    # Mark start and goal
    ax.text(env.start[1], env.start[0], "S", color="white", ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(env.goal[1], env.goal[0], "G", color="white", ha="center", va="center", fontsize=12, fontweight="bold")

    ax.legend(loc="upper right")
    st.pyplot(fig)
