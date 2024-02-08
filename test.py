import random
from time import time

class Maze:
    def __init__(self, size, density):
        self.size = size
        self.density = density
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        self.start = (0, 0)  # Starting point
        self.goal = (size - 1, size - 1)  # Goal point

    def generate_maze(self):
        # Place obstacles randomly based on density
        for row in range(self.size):
            for col in range(self.size):
                if random.random() < self.density and (row, col) not in [self.start, self.goal]:
                    self.grid[row][col] = 'X'

    def display_maze(self):
        for row in self.grid:
            print(' '.join(row))
        print()

# Example usage:
maze = Maze(size=10, density=0.3)
maze.generate_maze()
maze.display_maze()

from collections import deque

def bfs(maze):
    start = (0, 0)
    queue = deque([(start, [start])])
    visited = set([start])

    while queue:
        current, path = queue.popleft()
        row, col = current

        if current == maze.goal:
            return path

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            neighbor = (new_row, new_col)

            if (
                0 <= new_row < maze.size
                and 0 <= new_col < maze.size
                and neighbor not in visited
                and maze.grid[new_row][new_col] != 'X'
            ):
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

# Example usage:
bfs_path = bfs(maze)
print("BFS Path:", bfs_path)

def dfs(maze, current, visited, path):
    row, col = current
    if current == maze.goal:
        return True

    visited[row][col] = True

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if (
            0 <= new_row < maze.size
            and 0 <= new_col < maze.size
            and not visited[new_row][new_col]
            and maze.grid[new_row][new_col] != 'X'
        ):
            path.append((new_row, new_col))
            if dfs(maze, (new_row, new_col), visited, path):
                return True
            path.pop()  # Backtrack

    return False

visited = [[False] * maze.size for _ in range(maze.size)]
path = [(0, 0)]  # Starting point
dfs(maze, (0, 0), visited, path)
print("DFS Path:", path)
