import random
import numpy as np
import pacman_Qlearning
from pacman_Env import MazeEnv, MazeGenerator

class QLearningAgent:
    def __init__(self, state_size, action_size, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = np.zeros((state_size, action_size))
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(range(self.q_table.shape[1]))
        return np.argmax(self.q_table[state])
    
    def learn(self, state, action, reward, next_state):
        predict = self.q_table[state, action]
        target = reward + self.gamma * np.max(self.q_table[next_state])
        self.q_table[state, action] += self.alpha * (target - predict)

def state_to_index(state, width):
    return state[0] * width + state[1]

if __name__ == "__main__":
    width, height = 11, 11
    env = MazeEnv(width, height)
    agent = QLearningAgent(state_size=width * height, action_size=len(env.ACTIONS))

    episodes = 200

    for episode in range(episodes):
        state = env.reset()
        state_idx = state_to_index(state, width)
        step = 0
        total_reward = 0
        done = False

        while not done:
            action = agent.choose_action(state_idx)
            next_state, reward, done = env.step(action)
            next_state_idx = state_to_index(next_state, width)

            agent.learn(state_idx, action, reward, next_state_idx)

            state_idx = next_state_idx
            total_reward += reward
            step += 1

            env.render(episode=episode)
            