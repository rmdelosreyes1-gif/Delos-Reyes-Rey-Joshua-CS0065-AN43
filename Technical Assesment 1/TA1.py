import agentpy as ap
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -------- Get user input from console --------

num_agents = int(input("Enter number of agents: "))
grid_size = int(input("Enter grid size (e.g., 10 for 10x10): "))
num_steps = int(input("Enter number of steps: "))

# -------- Agent Definition -----------

class RandomWalker(ap.Agent):
    def step(self):
        # Task 2: Change movement rules
        # The agent can now move in 8 possible directions:
        # up, down, left, right, and the 4 diagonal directions.
        direction = random.choice([
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ])

        # Get the agent's current position.
        x, y = self.position

        # Move the agent based on the chosen direction.
        # The max and min functions keep the agent inside the grid boundaries.
        x = max(0, min(self.model.p.grid_size[0] - 1, x + direction[0]))
        y = max(0, min(self.model.p.grid_size[1] - 1, y + direction[1]))

        # Update the agent's position.
        self.position = (x, y)

        # Task 1: Track agent paths
        # Store the new position so the full path can be drawn later.
        self.path.append(self.position)

# -------- Model Definition -----------

class RandomWalkModel(ap.Model):
    def setup(self):
        # Create the agents.
        self.agents = ap.AgentList(self, self.p.agents, RandomWalker)

        # Give each agent a random starting position inside the grid.
        for agent in self.agents:
            agent.position = (
                random.randint(0, self.p.grid_size[0] - 1),
                random.randint(0, self.p.grid_size[1] - 1)
            )

            # Task 1: Track agent paths
            # Each agent's path begins with its starting position.
            agent.path = [agent.position]

        # Create the grid and place the agents on it.
        self.grid = ap.Grid(self, self.p.grid_size, torus=False)
        self.grid.add_agents(self.agents)

    def step(self):
        # During each model step, every agent takes one movement step.
        for agent in self.agents:
            agent.step()

# -------- Parameters from user input -----------

parameters = {
    'agents': num_agents,
    'grid_size': (grid_size, grid_size),
    'steps': num_steps
}

# -------- Run Model -----------

model = RandomWalkModel(parameters)
model.setup()

# -------- Interactive Animation -----------

fig, ax = plt.subplots()

# Set the visible area of the grid.
ax.set_xlim(0, model.p.grid_size[0])
ax.set_ylim(0, model.p.grid_size[1])

# Show grid lines for every cell.
ax.set_xticks(range(model.p.grid_size[0] + 1))
ax.set_yticks(range(model.p.grid_size[1] + 1))
ax.grid(True)

# Scatter plot used to display the current positions of the agents.
scat = ax.scatter([], [], s=200)

# Task 1: Track agent paths
# Create one line for each agent to show where it has moved.
path_lines = [
    ax.plot([], [], linewidth=1)[0]
    for agent in model.agents
]

def update(frame):
    # Move all agents one step.
    model.step()

    # Get the current x and y positions of all agents.
    x = [agent.position[0] for agent in model.agents]
    y = [agent.position[1] for agent in model.agents]

    # Update the scatter plot with the agents' current positions.
    scat.set_offsets(list(zip(x, y)))

    # Task 1: Track agent paths
    # Update each path line using the saved positions of each agent.
    for line, agent in zip(path_lines, model.agents):
        path_x = [pos[0] for pos in agent.path]
        path_y = [pos[1] for pos in agent.path]
        line.set_data(path_x, path_y)

    # Return all animated objects.
    return [scat] + path_lines

ani = animation.FuncAnimation(
    fig,
    update,
    frames=model.p.steps,
    blit=True,
    repeat=False
)

plt.show()