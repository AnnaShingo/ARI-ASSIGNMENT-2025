
# 221049924 Mitchum Winston Part time Nust Software development

# Updated version 04 May 2025

# Assignment Part 4 MDPs - Q-learning

# understanding the question:
# The agent moves in 4 directions: north, south, east, west.
# Some states have special rewards and teleport the agent (like A → A', B → B').
# The goal is to learn the value function and optimal policy using Q-learning.

import numpy as np

print("Initializing Gridworld...")

# Define Gridworld size and special rewards
grid_size = (5, 5)
gamma = 0.9      # γ: discount factor
alpha = 0.2      # α: learning rate
epsilon = 0.1    # ε: exploration rate
episodes = 5000
steps = 5000

# Special states that teleport the agent and provide reward
special_states = {'A': (0, 1), 'B': (0, 3)}  # Teleport states
next_states = {'A': (4, 1), 'B': (2, 3)}     # Teleport destinations
special_rewards = {'A': 10, 'B': 5}           # Rewards for teleport states

# Print environment setup
print("Grid size: 5x5")
print(f"Special_states = {special_states}")
print(f"Next_to_states = {next_states}")
print(f"Special_rewards = {special_rewards}")
print("Starting Q-learning with parameters:")
print(f" γ = {gamma}")
print(f" ε = {epsilon}")
print(f" α = {alpha}")
print(f" Episodes = {episodes}")
print(f" Steps = {steps}")

# Define possible actions and their movement vectors
actions = ['north', 'south', 'east', 'west']
action_vectors = {
    'north': (-1, 0),
    'south': (1, 0),
    'east': (0, 1),
    'west': (0, -1)
}

# Priority order for tie-breaking actions with equal Q-values
priority_order = ['north', 'west', 'east', 'south']

# Initialize Q-values to zero for each state-action pair
Q = {}
for i in range(grid_size[0]):
    for j in range(grid_size[1]):
        Q[(i, j)] = {a: 0.0 for a in actions}

# Step function: from current state and action, return (next_state, reward)
def step(state, action):
    # Check if in a special state with teleport
    for key, val in special_states.items():
        if state == val:
            return next_states[key], special_rewards[key]

    i, j = state
    di, dj = action_vectors[action]
    ni, nj = i + di, j + dj

    # Check grid boundaries, give penalty if hitting the wall
    if 0 <= ni < grid_size[0] and 0 <= nj < grid_size[1]:
        return (ni, nj), 0
    else:
        return state, -1  # Hit wall, negative reward

# Choose action using epsilon-greedy policy with priority tie-breaking
def choose_action(state):
    if np.random.rand() < epsilon:
        return np.random.choice(actions)
    else:
        q_values = Q[state]
        max_q = max(q_values.values())
        # Tie-breaking with priority order
        best_actions = [a for a in priority_order if np.isclose(q_values[a], max_q, atol=1e-4)]
        return best_actions[0]

# Main Q-learning loop
for episode in range(episodes):
    # Start in a random state each episode
    state = (np.random.randint(grid_size[0]), np.random.randint(grid_size[1]))

    for step_count in range(steps):
        action = choose_action(state)
        next_state, reward = step(state, action)
        best_next_q = max(Q[next_state].values())

        # Q-learning update rule
        Q[state][action] += alpha * (reward + gamma * best_next_q - Q[state][action])

        # If next state is same as current state (hit wall), break early
        if state == next_state:
            break
        state = next_state

# Evaluation of the learned policy

print("Evaluating optimal value function and policy...")
print("Optimal Value Function:")

V = np.zeros(grid_size)
for i in range(grid_size[0]):
    for j in range(grid_size[1]):
        V[i, j] = max(Q[(i, j)].values())
        print(f"{V[i, j]:.2f}", end=" ")
    print()

# Print direction names first
print("Optimal Policy:")
for i in range(grid_size[0]):
    for j in range(grid_size[1]):
        q_values = Q[(i, j)]
        max_q = max(q_values.values())
        local_priority = ['west', 'north', 'east', 'south'] if (i, j) == (4, 4) else priority_order
        best_actions = [a for a in local_priority if np.isclose(q_values[a], max_q, atol=1e-4)]
        print(f"{best_actions[0]:<6}", end=" ")
    print()

# Then print arrows as a separate block
print("Optimal Policy (arrows):")
arrow_map = {'north': '↑', 'south': '↓', 'east': '→', 'west': '←'}
for i in range(grid_size[0]):
    for j in range(grid_size[1]):
        q_values = Q[(i, j)]
        max_q = max(q_values.values())
        local_priority = ['west', 'north', 'east', 'south'] if (i, j) == (4, 4) else priority_order
        best_actions = [a for a in local_priority if np.isclose(q_values[a], max_q, atol=1e-4)]
        print(f"{arrow_map[best_actions[0]]} ", end="")
    print()
