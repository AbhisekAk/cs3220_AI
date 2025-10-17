import streamlit as st
from pyvis.network import Network
import numpy as np
from src.asteroid_environment import AsteroidEnvironment

st.set_page_config(page_title="Asteroid Search Visualization", layout="wide")

st.title("🪐 Asteroid Environment Visualizer (PyVis)")

# --- Sidebar Controls ---
st.sidebar.header("Environment Settings")
grid_size = st.sidebar.slider("Grid Size", 5, 15, 7)
asteroid_ratio = st.sidebar.slider("Asteroid Density", 0.0, 0.5, 0.25)
enemy_ratio = st.sidebar.slider("Enemy Density", 0.0, 0.3, 0.1)
seed = st.sidebar.number_input("Random Seed (optional)", value=0, step=1)

# Generate Environment
if st.sidebar.button("Generate Environment"):
    st.session_state.env = AsteroidEnvironment(
        size=grid_size,
        asteroid_ratio=asteroid_ratio,
        enemy_ratio=enemy_ratio,
        seed=seed if seed != 0 else None
    )

# Display environment
if "env" in st.session_state:
    env = st.session_state.env
    st.subheader("Generated Grid Matrix")
    st.write(env.grid)

    # --- Build PyVis Graph ---
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
    net.barnes_hut(gravity=-80000, central_gravity=0.3, spring_length=75)

    rows, cols = env.grid.shape

    for r in range(rows):
        for c in range(cols):
            node_id = f"{r},{c}"
            cell = env.grid[r, c]

            if cell == 1:  # asteroid
                color = "gray"
                label = "🪨"
            elif cell == 2:  # enemy
                color = "red"
                label = f"👾 ({env.enemies[(r,c)].power})"
            elif cell == 3:  # goal
                color = "green"
                label = "🏁 Goal"
            elif cell == 4:  # start
                color = "blue"
                label = "🚀 Start"
            else:
                color = "white"
                label = ""

            net.add_node(
                node_id,
                label=label,
                title=f"({r}, {c})",
                color=color,
                size=20
            )

    # --- Connect adjacent (non-asteroid) cells ---
    for r in range(rows):
        for c in range(cols):
            if env.grid[r, c] == 1:
                continue
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < rows and 0 <= nc < cols and env.grid[nr, nc] != 1:
                    net.add_edge(f"{r},{c}", f"{nr},{nc}", color="#555555")

    # --- Render PyVis HTML in Streamlit ---
    net.save_graph("graph.html")
    st.components.v1.html(open("graph.html", "r", encoding="utf-8").read(), height=620)

else:
    st.info("👈 Adjust settings in the sidebar and click **Generate Environment** to visualize.")
