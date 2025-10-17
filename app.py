import streamlit as st
import numpy as np
import pandas as pd
from src.asteroid_environment import AsteroidEnvironment
from src.asteroidProblemSolvingAgentSMART import AsteroidProblemSolvingAgentSMART
from src.PS_agentPrograms import BestFirstSearchAgentProgram, IDSearchAgentProgram
from src.environmentClass import Environment

st.set_page_config(page_title="Asteroid Navigation Agents", page_icon="🪐", layout="wide")

st.title("🪐 Asteroid Navigation Simulator")
st.markdown("### Compare UCS and IDS Path-Finding Agents in a Random Environment")

# --- Generate Environment ---
grid_size = st.slider("Grid Size", 5, 10, 7)
if st.button("🎲 Generate New Environment"):
    st.session_state.env = AsteroidEnvironment(size=grid_size)
    st.session_state.generated = True

if "generated" not in st.session_state or not st.session_state.generated:
    st.warning("Click the button above to generate an asteroid field.")
    st.stop()

env = st.session_state.env

st.subheader("🌍 Generated Environment")
st.write(pd.DataFrame(env.grid))
st.write(f"🚩 **Start:** {env.start} | 🎯 **Goal:** {env.goal}")

# --- Run UCS ---
if st.button("🚀 Run UCS Agent"):
    UCS_program = BestFirstSearchAgentProgram()
    agent_ucs = AsteroidProblemSolvingAgentSMART(
        initial_state=env.start,
        environment=env,
        goal=env.goal,
        program=UCS_program
    )

    environment = Environment()
    environment.add_thing(agent_ucs)

    step = 0
    max_steps = 100
    path = []

    while agent_ucs.alive and step < max_steps:
        step += 1
        environment.step()
        path.append(agent_ucs.location)
        if agent_ucs.location == env.goal:
            break

    st.session_state.ucs_path = path
    st.session_state.ucs_steps = step
    st.session_state.ucs_reached = (agent_ucs.location == env.goal)
    st.success(f"✅ UCS reached goal in {step} steps!")

# --- Run IDS ---
if st.button("🛰 Run IDS Agent"):
    IDS_program = IDSearchAgentProgram()
    agent_ids = AsteroidProblemSolvingAgentSMART(
        initial_state=env.start,
        environment=env,
        goal=env.goal,
        program=IDS_program
    )

    environment = Environment()
    environment.add_thing(agent_ids)

    step = 0
    max_steps = 100
    path = []

    while agent_ids.alive and step < max_steps:
        step += 1
        environment.step()
        path.append(agent_ids.location)
        if agent_ids.location == env.goal:
            break

    st.session_state.ids_path = path
    st.session_state.ids_steps = step
    st.session_state.ids_reached = (agent_ids.location == env.goal)
    st.success(f"✅ IDS reached goal in {step} steps!")

# --- Display Results ---
if "ucs_path" in st.session_state or "ids_path" in st.session_state:
    st.subheader("📊 Results Comparison")

    col1, col2 = st.columns(2)
    if "ucs_path" in st.session_state:
        with col1:
            st.markdown("#### 🚀 UCS Agent Path")
            st.write(st.session_state.ucs_path)
            st.metric("Steps", st.session_state.ucs_steps)
            st.metric("Reached Goal", "✅ Yes" if st.session_state.ucs_reached else "❌ No")

    if "ids_path" in st.session_state:
        with col2:
            st.markdown("#### 🛰 IDS Agent Path")
            st.write(st.session_state.ids_path)
            st.metric("Steps", st.session_state.ids_steps)
            st.metric("Reached Goal", "✅ Yes" if st.session_state.ids_reached else "❌ No")
