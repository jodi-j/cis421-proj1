import random
from collections import deque
from queue import PriorityQueue

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
   
    def h(self,cell1,cell2):
        x1,y1=cell1
        x2,y2=cell2

        return abs(x1-x2) + abs(y1-y2)
    
    def astar(self):
        g_score = {(row, col): float('inf') for row in range(self.size) for col in range(self.size)}
        g_score[self.start] = 0 
        f_score = {(row, col): float('inf') for row in range(self.size) for col in range(self.size)}
        f_score[self.start] = 0 

        open=PriorityQueue()
        open.put((self.h(self.start, self.goal),self.h(self.start, self.goal),self.start))
        aPath={}
    
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
        fwdPath={}
        cell=self.goal
        while cell!=self.start:
            fwdPath[aPath[cell]]=cell
            cell=aPath[cell]
        return fwdPath
    
    def get_neighbors(self, cell):
        row, col = cell
        neighbors = []

        for dr, dc, direction in [(1, 0, 'S'), (-1, 0, 'N'), (0, 1, 'E'), (0, -1, 'W')]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.size and 0 <= new_col < self.size and self.maze[new_row][new_col] == '.':
                neighbors.append(((new_row, new_col), direction))

        return neighbors

test = Maze(size=10, density=0.3)
test.create_maze()
test.print_maze()

path = test.breadth_first_search()
path2 = test.depth_first_search()
path3 = test.astar()

if path and path2 and path3:
    print("BFS:")
    for position in path:
        print(position)
    print("DFS:")
    for position in path2:
        print(position)
    print("A*:")
    for position in path3:
        print(position)
else:
    print("No path found.")