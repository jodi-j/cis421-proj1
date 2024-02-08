import random
from collections import deque
import heapq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.pyplot import figure

class Maze:
    def __init__(self, size, density):
        self.size = size
        self.density = density
        self.maze = [['.' for _ in range(size)] for _ in range(size)]
        self.start = (0, 0)  # Store start position as a tuple (row, column)
        self.goal = None  # Will store the goal position once created

    def create_maze(self):
        #self.maze[0][0] = 'S'
        goal_row, goal_col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        self.goal = (goal_row, goal_col)
        self.maze[goal_row][goal_col] = 'G'

        num_obstacles = random.randint(10, 12)
        for _ in range(num_obstacles):
            obstacle_row, obstacle_col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            while self.maze[obstacle_row][obstacle_col] != '.':
                obstacle_row, obstacle_col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.maze[obstacle_row][obstacle_col] = 'x'

        return self.maze
    
    def print_maze(self):
        for row_index, row in enumerate(self.maze):
            for col_index, cell in enumerate(row):
                if row_index == 0 and col_index == 0:
                    print('S', end=' ')
                else:
                    print(cell, end=' ')
            print()  # Move to the next line after printing each row

    def breadth_first_search(self):
        frontier = deque([(self.start, [])])  # Initialize the queue with the start position and an empty path
        explored = set()  # Keep track of visited positions

        while frontier:
            current, path = frontier.popleft()
            row, col = current

            if current == self.goal:
                return path + [current]  # Return the path when the goal is reached

            if 0 <= row < self.size and 0 <= col < self.size and self.maze[row][col] == '.' and current not in explored:
                explored.add(current)
                frontier.append(((row + 1, col), path + [current]))
                frontier.append(((row - 1, col), path + [current]))
                frontier.append(((row, col + 1), path + [current]))
                frontier.append(((row, col - 1), path + [current]))

        return None
    
    def depth_first_search(self):
        frontier = [(self.start, [])] #using stack data structure
        explored = set()
        while frontier:
            current, path = frontier.pop()
            row, col = current

            if current == self.goal:
                return path + [current]
            
            if 0 <= row < self.size and 0 <= col < self.size and self.maze[row][col] == '.' and current not in explored:
                explored.add(current)
                frontier.append(((row + 1, col), path + [current]))
                frontier.append(((row - 1, col), path + [current]))
                frontier.append(((row, col + 1), path + [current]))
                frontier.append(((row, col - 1), path + [current]))
        return None
    
    def maze_to_binary(self):
        binary_maze = [[1 if cell == 'x' else 0 for cell in row] for row in self.maze]
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == self.start:
                    binary_maze[i][j] = -1
                elif (i, j) == self.goal:
                    binary_maze[i][j] = 2
        return binary_maze

test = Maze(size=10, density=0.3)
test.create_maze()
test.print_maze()

path = test.breadth_first_search()
path2 = test.depth_first_search()

if path and path2:
    print("BFS:")
    for position in path:
        print(position)
    print("DFS")
    for pos in path2:
        print(pos)
else:
    print("No path found.")
    
#transform maze into binary form for matplotlib visualization
binary_array = test.maze_to_binary()
BFS_array = binary_array
DFS_array = binary_array
A_array = binary_array

#BFS visualization
fig_BFS, ax_BFS = plt.subplots(figsize=(12, 12))
#set values for path cells
if path:
    for position in path:
        row, col = position
        if BFS_array[row][col] != -1 and BFS_array[row][col] != 2:
            BFS_array[row][col] = -2    
color_map = plt.cm.tab20b
color_map.set_over('blue')
color_map.set_under('green')
ax_BFS.imshow(BFS_array, cmap=color_map, interpolation='nearest', vmin=-2, vmax=2)
ax_BFS.set_title("Maze Visualization - BFS")
bounds= [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
norm = mcolors.BoundaryNorm(bounds, color_map.N)
cbar_BFS = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=color_map), ax=ax_BFS, ticks=[-2, -1, 0, 1, 2])
cbar_BFS.ax.set_yticklabels(['Agent Path', 'Start', 'Open Path', 'Obstacle', 'Goal'])

#DFS visualization
fig_DFS, ax_DFS = plt.subplots(figsize=(12, 12))
#set values for path cells
if path2:
    for position in path2:
        row, col = position
        if DFS_array[row][col] != -1 and DFS_array[row][col] != 2:
            DFS_array[row][col] = -2    
color_map = plt.cm.tab20b
color_map.set_over('blue')
color_map.set_under('green')
ax_DFS.imshow(DFS_array, cmap=color_map, interpolation='nearest', vmin=-2, vmax=2)
ax_DFS.set_title("Maze Visualization - DFS")
bounds= [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
norm = mcolors.BoundaryNorm(bounds, color_map.N)
cbar_DFS = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=color_map), ax=ax_DFS, ticks=[-2, -1, 0, 1, 2])
cbar_DFS.ax.set_yticklabels(['Agent Path', 'Start', 'Open Path', 'Obstacle', 'Goal'])

#A* visualization




plt.show()