#from pyamaze import maze
#BFSm=maze()
#BFSm.CreateMaze(loopPercent=100)
#BFSm.run()

import random
from collections import deque

class Maze:
    def __init__(self, size, density):
        self.size = size
        self.density = density
        self.maze = [['.' for _ in range(size)] for _ in range(size)]
        self.start = self.maze[0][0] = 'S'

    def create_maze(self):
        self.start = 'S'
        goal_row, goal_col = random.randint(0, 9), random.randint(0, 9)
        self.maze[goal_row][goal_col] = 'G'

        num_obstacles = random.randint(10, 12)
        for _ in range(num_obstacles):
            obstacle_row, obstacle_col = random.randint(0, 9), random.randint(0, 9)
            while self.maze[obstacle_row][obstacle_col] != '.':
                obstacle_row, obstacle_col = random.randint(0, 9), random.randint(0, 9)
            self.maze[obstacle_row][obstacle_col] = 'x'
        return self.maze
    
    def print_maze(self):
        for row in self.maze:
            print(' '.join(row))

test = Maze(size=10, density=0.3)
test.create_maze()
test.print_maze()

'''def create_maze():
    maze = [['.' for _ in range(10)] for _ in range(10)]
    
    # Place the start state 's' in the top-left corner
    maze[0][0] = 'S'
    
    # Place the goal state 'g' at a random location
    goal_row, goal_col = random.randint(0, 9), random.randint(0, 9)
    maze[goal_row][goal_col] = 'G'
    
    # Place a random number of obstacles 'o' in random locations
    num_obstacles = random.randint(10, 12)
    for _ in range(num_obstacles):
        obstacle_row, obstacle_col = random.randint(0, 9), random.randint(0, 9)
        while maze[obstacle_row][obstacle_col] != '.':
            obstacle_row, obstacle_col = random.randint(0, 9), random.randint(0, 9)
        maze[obstacle_row][obstacle_col] = 'x'
    
    return maze

def print_maze(maze):
    for row in maze:
        print(' '.join(row))

def breadth_first_search(problem):
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = deque([node])
    explored = set()
    while frontier:
        node = frontier.popleft()
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                if problem.goal_test(child.state):
                    return child
                frontier.append(child)
    return None




maze = create_maze()
print_maze(maze)'''



