import random
from collections import deque
from queue import PriorityQueue
import time
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
        goal_row, goal_col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        self.goal = (goal_row, goal_col)

        num_obstacles = self.density
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
                elif row_index == self.goal[0] and col_index == self.goal[1]:
                    print('G', end=' ')
                else:
                    print(cell, end=' ')
            print()  # Move to the next line after printing each row
    
    def metadata(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            rv = func(*args, **kwargs)
            total_time = time.time() - start
            total_path = str(len(rv[0]))
            nodes_expanded = str(len(rv[2]))
            print(f'\nMeta Data for {func.__name__}: ', "\nTotal Time: ", total_time, "\nTotal path length: ", total_path, "\nNumber of nodes expanded: ", nodes_expanded, "\n")
            return rv
        return wrapper

    @metadata
    def breadth_first_search(self):
        frontier = deque([(self.start, [])])  # Initialize the queue with the start position and an empty path
        explored = set()  # Keep track of visited positions

        while frontier:
            current, path = frontier.popleft()
            row, col = current

            if current == self.goal:
                return path + [current], frontier, explored  # Return the path when the goal is reached

            if 0 <= row < self.size and 0 <= col < self.size and self.maze[row][col] == '.' and current not in explored:
                explored.add(current)
                frontier.append(((row + 1, col), path + [current]))
                frontier.append(((row - 1, col), path + [current]))
                frontier.append(((row, col + 1), path + [current]))
                frontier.append(((row, col - 1), path + [current]))

        return None
    
    @metadata
    def depth_first_search(self):
        frontier = [(self.start, [])] #using stack data structure
        explored = set()
        while frontier:
            current, path = frontier.pop()
            row, col = current

            if current == self.goal:
                return path + [current], frontier, explored
            
            if 0 <= row < self.size and 0 <= col < self.size and self.maze[row][col] == '.' and current not in explored:
                explored.add(current)
                frontier.append(((row + 1, col), path + [current]))
                frontier.append(((row - 1, col), path + [current]))
                frontier.append(((row, col + 1), path + [current]))
                frontier.append(((row, col - 1), path + [current]))
        return None
   
    def h(self,cell1,cell2):
        x1,y1=cell1
        x2,y2=cell2

        return abs(x1-x2) + abs(y1-y2)
    
    @metadata
    def astar(self):
        g_score = {(row, col): float('inf') for row in range(self.size) for col in range(self.size)}
        g_score[self.start] = 0 
        f_score = {(row, col): float('inf') for row in range(self.size) for col in range(self.size)}
        f_score[self.start] = 0 

        open=PriorityQueue()
        open.put((self.h(self.start, self.goal),self.h(self.start, self.goal),self.start))
        aPath={}
        explored = set()
    
        while not open.empty():
            currCell=open.get()[2]
            if currCell== self.goal:
                break
            eswn = self.get_neighbors(currCell)
            for d in eswn:
                row, col = currCell  # Extract row and column from the tuple
                if d[1] == 'E' and col + 1 < self.size and self.maze[row][col + 1] == '.':
                    childCell = (row, col + 1)
                elif d[1] == 'W' and col - 1 >= 0 and self.maze[row][col - 1] == '.':
                    childCell = (row, col - 1)
                elif d[1] == 'N' and row - 1 >= 0 and self.maze[row - 1][col] == '.':
                    childCell = (row - 1, col)
                elif d[1] == 'S' and row + 1 < self.size and self.maze[row + 1][col] == '.':
                    childCell = (row + 1, col)
                else:
                    continue

                temp_g_score=g_score[currCell]+1
                temp_f_score=temp_g_score+self.h(childCell, self.goal)

                if temp_f_score < f_score[childCell]:
                    g_score[childCell]= temp_g_score
                    f_score[childCell]= temp_f_score
                    open.put((temp_f_score,self.h(childCell, self.goal),childCell))
                    aPath[childCell]=currCell
                    explored.add(childCell)
               
        fwdPath=[]
        finalPath = [self.start]
        cell=self.goal
        while cell!=self.start:
            fwdPath.append(cell)
            cell=aPath[cell]

        for position in reversed(fwdPath):
            finalPath.append(position)

        return finalPath, aPath, explored
    
    def get_neighbors(self, cell):
        row, col = cell
        neighbors = []

        for dr, dc, direction in [(1, 0, 'S'), (-1, 0, 'N'), (0, 1, 'E'), (0, -1, 'W')]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.size and 0 <= new_col < self.size and self.maze[new_row][new_col] == '.':
                neighbors.append(((new_row, new_col), direction))

        return neighbors
    
    def maze_to_binary(self):
        binary_maze = [[1 if cell == 'x' else 0 for cell in row] for row in self.maze]
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == self.start:
                    binary_maze[i][j] = -1
                elif (i, j) == self.goal:
                    binary_maze[i][j] = 2
        return binary_maze


user_size = int(input("Enter the size: ").strip())
user_density = int(input("Enter an integer number of obstacles: ").strip())
test = Maze(size=user_size, density=user_density)
test.create_maze()
test.print_maze()

#bfs_start = time()
path = test.breadth_first_search()
#bfs_end = time()
#bfs_elapsed = bfs_end - bfs_start

#dfs_start = time()
path2 = test.depth_first_search()
#dfs_end = time()
#dfs_elapsed = dfs_end - dfs_start

#astar_start = time()
path3 = test.astar()
#astar_end = time()
#astar_elapsed = astar_end - astar_start

if path and path2 and path3:
    print("BFS:")
    for position in path[0]:
        print(position)
   # print("Breadth-first search runtime is: " + str(bfs_elapsed) + " seconds.")
  # print("BFS Path length: " + str(len(path)))
  
    print("DFS:")
    for position in path2[0]:
        print(position)
   # print("Depth-first search runtime is: " + str(dfs_elapsed) + " seconds.")
   # print("DFS Path length: " + str(len(path2)))
   
    print("A*:")
    for position in path3[0]:
        print(position)
   # print("A-star search runtime is: " + str(astar_elapsed) + " seconds.")
    # print("A* Path length: " + str(len(path3)))

else:
    print("No path found.")

#transform maze into binary form for matplotlib visualization
BFS_array = test.maze_to_binary()
DFS_array = test.maze_to_binary()
A_array = test.maze_to_binary()

#BFS visualization
fig_BFS, ax_BFS = plt.subplots(figsize=(12, 12))

if path:
    #set values for explored path
    for position in path[2]:
        row, col = position
        if BFS_array[row][col] != -1 and BFS_array[row][col] != 2:
            BFS_array[row][col] = -3
    #set values for final path
    for position in path[0]:
        row, col = position
        if BFS_array[row][col] != -1 and BFS_array[row][col] != 2:
            BFS_array[row][col] = -2    
            
color_map = plt.cm.plasma
ax_BFS.imshow(BFS_array, cmap=color_map, interpolation='nearest', vmin=-3.5, vmax=2.5)
ax_BFS.set_title("Maze Visualization - BFS")
bounds= [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
norm = mcolors.BoundaryNorm(bounds, color_map.N)
cbar_BFS = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=color_map), ax=ax_BFS, ticks=[-3, -2, -1, 0, 1, 2])
cbar_BFS.ax.set_yticklabels(['Explored Path', 'Final Path', 'Start', 'Open Path', 'Obstacle', 'Goal'])

#DFS visualization
fig_DFS, ax_DFS = plt.subplots(figsize=(12, 12))
if path2:
    #set values for explored path
    for position in path2[2]:
        row, col = position
        if DFS_array[row][col] != -1 and DFS_array[row][col] != 2:
            DFS_array[row][col] = -3
    #set values for final path
    for position in path2[0]:
        row, col = position
        if DFS_array[row][col] != -1 and DFS_array[row][col] != 2:
            DFS_array[row][col] = -2 
color_map = plt.cm.plasma
ax_DFS.imshow(DFS_array, cmap=color_map, interpolation='nearest', vmin=-3.5, vmax=2.5)
ax_DFS.set_title("Maze Visualization - DFS")
bounds= [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
norm = mcolors.BoundaryNorm(bounds, color_map.N)
cbar_DFS = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=color_map), ax=ax_DFS, ticks=[-3, -2, -1, 0, 1, 2])
cbar_DFS.ax.set_yticklabels(['Explored Path', 'Final Path', 'Start', 'Open Path', 'Obstacle', 'Goal'])

#A* visualization
fig_A, ax_A = plt.subplots(figsize=(12, 12))
if path3:
    #set values for explored path
    for position in path3[2]:
        row, col = position
        if A_array[row][col] != -1 and A_array[row][col] != 2:
            A_array[row][col] = -3
    #set values for final path
    for position in path3[0]:
        row, col = position
        if A_array[row][col] != -1 and A_array[row][col] != 2:
            A_array[row][col] = -2
color_map = plt.cm.plasma
ax_A.imshow(A_array, cmap=color_map, interpolation='nearest', vmin=-3.5, vmax=2)
ax_A.set_title("Maze Visualization - A*")
bounds= [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
norm = mcolors.BoundaryNorm(bounds, color_map.N)
cbar_A = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=color_map), ax=ax_A, ticks=[-3, -2, -1, 0, 1, 2])
cbar_A.ax.set_yticklabels(['Explored Path','Final Path', 'Start', 'Open Path', 'Obstacle', 'Goal'])

plt.show()