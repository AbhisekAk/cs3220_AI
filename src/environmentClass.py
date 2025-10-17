"""
A base class representing an abstract Environment.
The environment keeps a list of agents.
Each agent has a performance measure.
"""

class Environment:
    def __init__(self):
        self.agents = []

    def percept(self, agent):
        """Return what the agent perceives (the current state)."""
        return agent.state

    def execute_action(self, agent, action):
      # The action is a Node object like <Node (x, y)>
      if hasattr(action, 'state'):
          new_position = action.state
      elif isinstance(action, tuple):
          new_position = action
      else:
          print("⚠️ Invalid action:", action)
          return

      print(f"🎯 Agent decided to take action: {new_position}")
      agent.location = new_position  # ✅ update the agent's position
      print(f"🚀 Agent moved to {agent.location}")

  

    def default_location(self, thing):
        """Default location to place a new thing."""
        return None

    def is_done(self):
        """We're done when no agents are alive."""
        return not any(agent.alive for agent in self.agents)

    def step(self):
        """Have each agent perceive and act once."""
        print("\n🌍 Environment taking a step...")
        for agent in self.agents:
            if not agent.alive:
                continue
            percept = self.percept(agent)
            
            action = agent(percept)
            if action is not None:
                print(f"🎯 Agent decided to take action: {action}")
                self.execute_action(agent, action)

    def run(self, steps=10):
        """Run the Environment for a given number of steps."""
        for step in range(steps):
            if self.is_done():
                print("✅ All agents done.")
                return
            print(f"\nstep {step + 1}:")
            self.step()

    def add_thing(self, thing, location=None):
        """Add an agent or object to the environment."""
        from src.problemSolvingAgentProgramClass import SimpleProblemSolvingAgentProgram

        if thing in self.agents:
            print("⚠️ Can't add the same agent twice")
        else:
            if isinstance(thing, SimpleProblemSolvingAgentProgram):
                thing(thing.state)
                print(f"✅ Added {thing.__class__.__name__} at {thing.state} with performance {thing.performance}")
                self.agents.append(thing)

    def delete_thing(self, thing):
        if thing in self.agents:
            self.agents.remove(thing)
