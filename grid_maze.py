#from pyamaze import maze
#BFSm=maze()
#BFSm.CreateMaze(loopPercent=100)
#BFSm.run()

import random

def create_maze():
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

maze = create_maze()
print_maze(maze)



