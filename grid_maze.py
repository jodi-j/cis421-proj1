'''CIS 479 Project 1: Maze Generation and Search Algorithms
    Authors: Huda Hussaini, Jodi Joven, Shams Ahson'''
import random
from collections import deque
from queue import PriorityQueue
import time
import heapq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.pyplot import figure

class Maze: #defines a Maze object
    def __init__(self, size, density):
        '''This is the initialization function that defines a maze's size, density, start, goal and defintion.'''
        self.size = size #customizable size
        self.density = density #customizable density
        self.maze = [['.' for _ in range(size)] for _ in range(size)] #generate maze
        self.start = (0, 0)  #store start position as a tuple (row, column)
        self.goal = None  

    def create_maze(self):
        '''This function creates the maze based on initialization and sets a random goal state.'''
        goal_row, goal_col = random.randint(0, self.size - 1), random.randint(0, self.size - 1) #generate random goal placement
        self.goal = (goal_row, goal_col) #assign to goal state

        num_obstacles = self.density #customizable density
        for _ in range(num_obstacles): #generating obstacles randomly based on density
            obstacle_row, obstacle_col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            while self.maze[obstacle_row][obstacle_col] != '.':
                obstacle_row, obstacle_col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.maze[obstacle_row][obstacle_col] = 'x'

        return self.maze
    
    def print_maze(self):
        '''This function displays the generated maze with the start, goal, obstacles and empty spaces.'''
        for row_index, row in enumerate(self.maze):
            for col_index, cell in enumerate(row):
                if row_index == 0 and col_index == 0: #print S for starting cell
                    print('S', end=' ')
                elif row_index == self.goal[0] and col_index == self.goal[1]: #print G for goal cell
                    print('G', end=' ')
                else:
                    print(cell, end=' ')
            print()  #move to the next line after printing each row
    
    def metadata(func):
        def wrapper(*args, **kwargs):
            '''This wrapper function defines the metadata (total number of nodes in final path, 
            total number of nodes expanded and total time of execution for each algorithm).'''
            start = time.time()
            try:
                rv = func(*args, **kwargs)
                total_path = str(len(rv[0]))
                nodes_expanded = str(len(rv[2]))
                total_time = time.time() - start
                print(f'\nMeta Data for {func.__name__}: ', "\nTotal path length: ", total_path, "\nNumber of nodes expanded: ", nodes_expanded, "\nTotal Time: ", total_time, "\n")
                return rv
            except:
                print("\nNo Meta Data") #for "No path found" cases
        return wrapper

    @metadata #assigning result to metadata wrapper
    def breadth_first_search(self):
        '''This function performs the breadth-first search algorithm on the maze,
        finding the final path and returning all expanded nodes.'''
        frontier = deque([(self.start, [])])  #initialize the double queue frontier with the start and empty path
        explored = set()  #keep track of visited positions (nodes expanded)

        while frontier:
            current, path = frontier.popleft() #get current node and path to it from frontier
            row, col = current

            if current == self.goal: #goal state reached
                return path + [current], frontier, explored  #return path

            if 0 <= row < self.size and 0 <= col < self.size and self.maze[row][col] == '.' and current not in explored: #check if in correct conditions
                explored.add(current) #add to nodes expanded
                frontier.append(((row + 1, col), path + [current])) #explore child nodes and add to frontier
                frontier.append(((row - 1, col), path + [current]))
                frontier.append(((row, col + 1), path + [current]))
                frontier.append(((row, col - 1), path + [current]))

        return None #no path found case
    
    @metadata #assigning result to metadata wrapper
    def depth_first_search(self):
        '''This function performs the depth-first search algorithm on the maze,
        finding the final path and returning all expanded nodes.'''
        frontier = [(self.start, [])] #using stack data structure as frontier and initializing with start, empty path 
        explored = set() #keep track of visited positions (nodes expanded)
        
        while frontier:
            current, path = frontier.pop() #get current node and path to it from frontier
            row, col = current

            if current == self.goal: #goal state reached 
                return path + [current], frontier, explored #return path
            
            if 0 <= row < self.size and 0 <= col < self.size and self.maze[row][col] == '.' and current not in explored: #check if in correct conditions
                explored.add(current) #add to nodes expanded
                frontier.append(((row + 1, col), path + [current])) #explore child nodes and add to frontier
                frontier.append(((row - 1, col), path + [current]))
                frontier.append(((row, col + 1), path + [current]))
                frontier.append(((row, col - 1), path + [current]))

        return None #no path found case
   
    def h(self,cell1,cell2): 
        '''This is the heuristic function used in the A-Star algorithm. 
        It calculates the Manhattan distance between cells.'''
        x1,y1=cell1
        x2,y2=cell2

        return abs(x1-x2) + abs(y1-y2) #Mahattan distance returned
    
    @metadata #assigning result to metadata wrapper
    def astar(self): 
        '''This function performs the a-star heuristic search algorithm on the maze,
        finding the final path and returning all expanded nodes.'''

        g_score = {(row, col): float('inf') for row in range(self.size) for col in range(self.size)} #g score is distance of current node from start
        g_score[self.start] = 0 #initialize to 0
        f_score = {(row, col): float('inf') for row in range(self.size) for col in range(self.size)} #f score is the total cost to reach the next node
        f_score[self.start] = 0 #initialize to 0

        open=PriorityQueue() #using a priority queue data structure
        open.put((self.h(self.start, self.goal),self.h(self.start, self.goal),self.start)) #calculate h(current node) and add to queue
        aPath={} #create nodes expanded dictionary 
        explored = set() #keep track of visited positions (nodes expanded)
    
        while not open.empty():
            currCell=open.get()[2] #get current node 
            if currCell == self.goal: #goal state reached
                break
            eswn = self.get_neighbors(currCell) #explore children (neighbors) using helper function
            for d in eswn:
                row, col = currCell 
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

                temp_g_score=g_score[currCell]+1 #calculate child's g score
                temp_f_score=temp_g_score+self.h(childCell, self.goal) #calculate child's f score

                if temp_f_score < f_score[childCell]: #if the child's f score is lower than previous child's f score
                    g_score[childCell]= temp_g_score #update g and f scores 
                    f_score[childCell]= temp_f_score
                    open.put((temp_f_score,self.h(childCell, self.goal),childCell)) #add child to 
                    aPath[childCell]=currCell #add {child, current pair}
                    explored.add(childCell) #add child to expanded node set
               
        fwdPath=[] #inverted final path
        finalPath = [self.start] #include starting node
        cell=self.goal
        while cell!=self.start: 
            fwdPath.append(cell) #appending to final path
            try:
                cell=aPath[cell] #get cell's key unless exception occurs
            except Exception as e:
                print(e)

        for position in reversed(fwdPath): #reverse the path to get the final path
            finalPath.append(position)

        return finalPath, aPath, explored
    
    def get_neighbors(self, cell):
        '''This is a helper function for the astar method. It retrieves neighbor (child) nodes for exploration.'''
        row, col = cell
        neighbors = [] #create list

        for dr, dc, direction in [(1, 0, 'S'), (-1, 0, 'N'), (0, 1, 'E'), (0, -1, 'W')]: #label directions to explore
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.size and 0 <= new_col < self.size and self.maze[new_row][new_col] == '.': #check conditions
                neighbors.append(((new_row, new_col), direction)) #return all possible neighbors (children)
        return neighbors
    
    def maze_to_binary(self):
        '''This helper function is fo visualization in matplotlib. It transforms the maze into a binary format.'''
        binary_maze = [[1 if cell == 'x' else 0 for cell in row] for row in self.maze]
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == self.start:
                    binary_maze[i][j] = -1
                elif (i, j) == self.goal:
                    binary_maze[i][j] = 2
        return binary_maze
    


def main(): 
    '''The main function calls each algorithm and builds the visualization.'''

    def print_path(print_path):
        '''This helper function is used to print the paths for each maze.'''
        if print_path:
            if print_path == 'path':
                print("BFS:")
            elif print_path == 'path 2':
                print("DFS:" )
            elif print_path == 'path 3':
                print("A*:" )
            for position in path[0]:
                print(position)
        else:
            print("No path found ")
    
    user_size = int(input("Enter the size: ").strip()) #allow user to enter maze size
    user_density = int(input("Enter an integer number of obstacles: ").strip()) #allow user to enter maze density
    test = Maze(size=user_size, density=user_density) #create test maze
    test.create_maze()
    test.print_maze()

    path = test.breadth_first_search() #perform and display BFS
    print_path(path)

    path2 = test.depth_first_search() #perform and display DFS
    print_path(path2)

    path3 = test.astar() #perform and display A-Star
    print_path(path3)

    #transform maze into binary form for matplotlib visualization
    BFS_array = test.maze_to_binary()
    DFS_array = test.maze_to_binary()
    A_array = test.maze_to_binary()

    #BFS visualization
    fig_BFS, ax_BFS = plt.subplots(figsize=(user_size, user_size))
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
    fig_DFS, ax_DFS = plt.subplots(figsize=(user_size, user_size))
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
    fig_A, ax_A = plt.subplots(figsize=(user_size, user_size))
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

    plt.show() #display all three visualizations

if __name__ == '''___main___''':
    main()