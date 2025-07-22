import random

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [['#'] * width for _ in range(height)]
        self.visited = [[False] * width for _ in range(height)]

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_wall(self, x, y):
        return self.grid[y][x] == '#'
    
    def generate(self):
        def carve(x, y):
            dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and not self.visited[ny][nx]:
                    self.grid[y + dy // 2][x + dx // 2] = ' '
                    self.grid[ny][nx] = ' '
                    self.visited[ny][nx] = True
                    carve(nx, ny)
        
        self.visited[1][1] = True
        self.grid[1][1] = ' '
        carve(1, 1)

        return self.grid
    
    # @:pacman, G: goal, P: penalty
    def place_items(self, items=['@', 'G', 'P']):
        # 先清理旧物品
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] in items:
                    self.grid[y][x] = ' '

        empty = [(i, j) for i in range(self.height) for j in range(self.width) if self.grid[i][j] == ' ']
        chosen = random.sample(empty, len(items))
        for pos, item in zip(chosen, items):
            x, y = pos
            self.grid[y][x] = item
        return self.grid

class MazeEnv:
    ACTIONS = {
        0: (0, -1),  # Up
        1: (1, 0),   # Right
        2: (0, 1),   # Down
        3: (-1, 0)   # Left
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.generator = MazeGenerator(width, height)
        self.reset()
    
    def reset(self):
        self.grid = self.generator.generate()
        self.grid = self.generator.place_items()
        self.pacman_pos = self.find_pacman()
        self.step_count = 0
        return self.pacman_pos
    
    def find_pacman(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == '@':
                    return (x, y)
        return None
    
    def move(self, action):
        dx, dy = self.ACTIONS[action]
        x, y = self.pacman_pos
        nx, ny = x + dx, y + dy

        # Check bounds and walls
        if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height or self.grid[ny][nx] == '#':
            return False
        
        # Move Pacman
        self.grid[y][x] = ' '
        self.grid[ny][nx] = '@'
        self.pacman_pos = (nx, ny)
        return True
    
    def step(self, action):
        self.step_count += 1
        dx, dy = self.ACTIONS[action]
        x, y = self.pacman_pos
        nx, ny = x + dx, y + dy

        if not (0 <= nx < self.width and 0 <= ny < self.height) or self.grid[ny][nx] == '#':
            reward = -1
            done = False
            return (x,y), reward, done
        
        target_cell = self.grid[ny][nx]

        # init reward and done
        reward = -0.1
        done = False

        if target_cell == 'G':  # Goal
            reward = 10
            done = True
        elif target_cell == 'P':  # Penalty
            reward = -10
            done = True

        # Move Pacman
        self.grid[y][x] = ' '
        self.grid[ny][nx] = '@'
        self.pacman_pos = (nx, ny)

        return (nx, ny), reward, done
    
    def render(self):
        for row in self.grid:
            print(''.join(row))
        print()

import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')        
    
if __name__ == "__main__":
    env = MazeEnv(11, 11)
    env.reset()

    done = False
    while not done:
        clear_screen()
        env.render()
        action = random.choice([0,1,2,3])
        state, reward, done = env.step(action)
        print(f"Step: {env.step_count}, 动作: {action}, 奖励: {reward}, 结束: {done}")
        time.sleep(0.3)