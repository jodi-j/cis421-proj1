import random
from collections import deque

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
        for row in self.maze:
            print(' '.join(row))

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

test = Maze(size=10, density=0.3)
test.create_maze()
test.print_maze()

path = test.breadth_first_search()

if path:
    print("Path found:")
    for position in path:
        print(position)
else:
    print("No path found.")

