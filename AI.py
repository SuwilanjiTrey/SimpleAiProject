import pygame
import sys
import random
from queue import PriorityQueue

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)

# Maze configurations
EASY_MAZE = [
    "####################################",
    "#S#       #        #               #",
    "# # ##### # ###### #               #",
    "#   #   # #      # #               #",
    "# ### # # # #### # #               #",
    "#     #   #    # # #               #",
    "####### ###### # # #               #",
    "#     #        # # #               #",
    "# ### ########## # #               #",
    "#   #            # #               #",
    "# # # ############ #               #",
    "# #      #         #               #",
    "# ###### # ####### #               #",
    "#        #       # #               #",
    "######## ####### # #               #",
    "#                # #               #",
    "# ############## # #               #",
    "#                # #               #",
    "################## #               #",
    "#                                 E#",
    "####################################"
]

NORMAL_MAZE = [
    "####################################",
    "#S#       #        #               #",
    "# # ##### # ###### # ###############",
    "#   #   # #      # #               #",
    "# ### # # # #### # # ###############",
    "#     #   #    # # #               #",
    "####### ###### # # # ###############",
    "#     #        # # #               #",
    "# ### ########## # # ###############",
    "#   #            # #               #",
    "# # # ############ # ###############",
    "# #      #         #               #",
    "# ###### # ####### # ###############",
    "#        #       # #               #",
    "######## ####### # # ###############",
    "#                # #               #",
    "# ############## # # ###############",
    "#                # #               #",
    "################## #################",
    "#                                 E#",
    "####################################"
]

CHALLENGING_MAZE = [
    "####################################",
    "#S#       #        #               #",
    "# # ##### # ###### # ###############",
    "#   #   # #      # #               #",
    "# ### # # # #### # # ###############",
    "#     #   #    # # #               #",
    "####### ###### # # # ###############",
    "#     #        # # #               #",
    "# ### ########## # # ###############",
    "#   #            # #               #",
    "# # # ############ # ###############",
    "# #      #         #               #",
    "# ###### # ####### # ###############",
    "#        #       # #               #",
    "######## ####### # # ###############",
    "#                # #               #",
    "# ############## # # ###############",
    "#                # #               #",
    "################## #################",
    "#                                 E#",
    "####################################"
]

# Cell size
CELL_SIZE = 25

# Set up the display
WIDTH = len(NORMAL_MAZE[0]) * CELL_SIZE
HEIGHT = len(NORMAL_MAZE) * CELL_SIZE + 80  # Extra space for buttons and score
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adaptive Maze Solver")

class Node:
    def __init__(self, position, g=0, h=0, parent=None):
        self.position = position
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

class Objective:
    def __init__(self, position, points, duration=None):
        self.position = position
        self.points = points
        self.creation_time = pygame.time.get_ticks()
        self.duration = duration

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(maze, node):
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_position = (node.position[0] + dx, node.position[1] + dy)
        if (0 <= new_position[0] < len(maze) and
            0 <= new_position[1] < len(maze[0]) and
            maze[new_position[0]][new_position[1]] != '#'):
            neighbors.append(new_position)
    return neighbors

def a_star(maze, start, end, objectives):
    start_node = Node(start, h=heuristic(start, end))
    open_list = PriorityQueue()
    open_list.put((start_node.f, id(start_node), start_node))
    closed_set = set()
    
    while not open_list.empty():
        current_node = open_list.get()[2]
        
        if current_node.position == end:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]
        
        closed_set.add(current_node.position)
        
        for neighbor_pos in get_neighbors(maze, current_node):
            if neighbor_pos in closed_set:
                continue
            
            neighbor = Node(neighbor_pos, 
                            g=current_node.g + 1,
                            h=heuristic(neighbor_pos, end),
                            parent=current_node)
            
            # Prioritize objectives
            for obj in objectives:
                if neighbor_pos == obj.position:
                    if obj.points > 0:
                        neighbor.h -= obj.points * 2  # Make positive objectives more attractive
                    else:
                        neighbor.h += abs(obj.points) * 3  # Make negative objectives less attractive

            if not any(node.position == neighbor.position for _, _, node in open_list.queue):
                open_list.put((neighbor.f, id(neighbor), neighbor))
    
    return None

def find_start_end(maze):
    start = end = None
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)
    return start, end

def get_empty_positions(maze):
    empty = []
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == ' ':
                empty.append((i, j))
    return empty

def draw_maze(screen, maze, objectives):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell == '#':
                pygame.draw.rect(screen, BLACK, rect)
            elif cell == 'S':
                pygame.draw.rect(screen, BLUE, rect)
            elif cell == 'E':
                pygame.draw.rect(screen, RED, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
    
    for obj in objectives:
        x, y = obj.position
        center = ((y + 0.5) * CELL_SIZE, (x + 0.5) * CELL_SIZE)
        if obj.points == 15:
            color = PURPLE
        elif obj.points == 5:
            color = YELLOW
        else:  # -5 points
            color = ORANGE
        pygame.draw.circle(screen, color, center, CELL_SIZE // 3)

def draw_ai(screen, position):
    x, y = position
    center = ((y + 0.5) * CELL_SIZE, (x + 0.5) * CELL_SIZE)
    pygame.draw.circle(screen, GREEN, center, CELL_SIZE // 3)

def draw_button(screen, text, position, size, color=GRAY):
    font = pygame.font.Font(None, 36)
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, color, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    return button_rect

def draw_score(screen, score):
    font = pygame.font.Font(None, 36)
    text_surf = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text_surf, (10, HEIGHT - 40))

def change_maze(maze, num_changes=5):
    new_maze = [list(row) for row in maze]
    empty_positions = get_empty_positions(new_maze)
    
    for _ in range(num_changes):
        if empty_positions:
            x, y = random.choice(empty_positions)
            empty_positions.remove((x, y))
            new_maze[x][y] = '#'
            
            # Ensure the maze remains solvable
            start, end = find_start_end(new_maze)
            if not a_star(new_maze, start, end, []):
                new_maze[x][y] = ' '
                empty_positions.append((x, y))
    
    return [''.join(row) for row in new_maze]

def main():
    current_maze = NORMAL_MAZE
    difficulty = "Normal"
    start, end = find_start_end(current_maze)
    empty_positions = get_empty_positions(current_maze)
    
    objectives = [Objective(random.choice(empty_positions), 5) for _ in range(6)]
    objectives.append(Objective(random.choice(empty_positions), 15))
    objectives.extend([Objective(random.choice(empty_positions), -5, duration=20000) for _ in range(3)])

    clock = pygame.time.Clock()
    solving = False
    path = None
    index = 0
    score = 0
    last_objective_time = pygame.time.get_ticks()
    last_maze_change_time = pygame.time.get_ticks()

    start_button = draw_button(screen, "Start Solving", (WIDTH // 2 - 75, HEIGHT - 70), (150, 30))
    easy_button = draw_button(screen, "Easy", (10, HEIGHT - 70), (100, 30))
    normal_button = draw_button(screen, "Normal", (120, HEIGHT - 70), (100, 30))
    challenging_button = draw_button(screen, "Challenging", (230, HEIGHT - 70), (150, 30))
    
    current_goal = end
    original_end = end

    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos) and not solving:
                    solving = True
                    path = a_star(current_maze, start, current_goal, objectives)
                    if path:
                        index = 0
                    else:
                        print("No path found!")
                elif easy_button.collidepoint(event.pos):
                    current_maze = EASY_MAZE
                    difficulty = "Easy"
                    solving = False
                    score = 0
                elif normal_button.collidepoint(event.pos):
                    current_maze = NORMAL_MAZE
                    difficulty = "Normal"
                    solving = False
                    score = 0
                elif challenging_button.collidepoint(event.pos):
                    current_maze = CHALLENGING_MAZE
                    difficulty = "Challenging"
                    solving = False
                    score = 0

                if not solving:
                    start, end = find_start_end(current_maze)
                    empty_positions = get_empty_positions(current_maze)
                    objectives = [Objective(random.choice(empty_positions), 5) for _ in range(6)]
                    objectives.append(Objective(random.choice(empty_positions), 15))
                    objectives.extend([Objective(random.choice(empty_positions), -5, duration=20000) for _ in range(3)])
                    current_goal = end
                    original_end = end

        # Update objectives
        if current_time - last_objective_time > random.randint(5000, 10000):
            objectives = [obj for obj in objectives if obj.points < 0 and (current_time - obj.creation_time) < obj.duration]
            objectives.extend([Objective(random.choice(empty_positions), 5) for _ in range(6)])
            objectives.append(Objective(random.choice(empty_positions), 15))
            if len([obj for obj in objectives if obj.points < 0]) < 3:
                objectives.extend([Objective(random.choice(empty_positions), -5, duration=20000) for _ in range(3 - len([obj for obj in objectives if obj.points < 0]))])
            last_objective_time = current_time

            # Recalculate path if we're not at the original end goal
            if solving and current_goal != original_end:
                current_position = path[index] if index < len(path) else path[-1]
                path = a_star(current_maze, current_position, current_goal, objectives)
                index = 0

        # Change maze for challenging difficulty
        if difficulty == "Challenging" and current_time - last_maze_change_time > 15000:  # Change maze every 15 seconds
            current_maze = change_maze(current_maze)
            last_maze_change_time = current_time
            if solving:
                current_position = path[index] if index < len(path) else path[-1]
                path = a_star(current_maze, current_position, current_goal, objectives)
                index = 0

# Remove expired negative objectives
        objectives = [obj for obj in objectives if obj.points >= 0 or (current_time - obj.creation_time) < obj.duration]

        screen.fill(WHITE)
        draw_maze(screen, current_maze, objectives)
        start_button = draw_button(screen, "Start Solving", (WIDTH // 2 - 75, HEIGHT - 70), (150, 30))
        easy_button = draw_button(screen, "Easy", (10, HEIGHT - 70), (100, 30), GREEN if difficulty == "Easy" else GRAY)
        normal_button = draw_button(screen, "Normal", (120, HEIGHT - 70), (100, 30), GREEN if difficulty == "Normal" else GRAY)
        challenging_button = draw_button(screen, "Challenging", (230, HEIGHT - 70), (150, 30), GREEN if difficulty == "Challenging" else GRAY)
        draw_score(screen, score)

        if solving and path:
            if index < len(path):
                current_position = path[index]
                draw_ai(screen, current_position)
                
                # Check if AI is on an objective
                for obj in objectives:
                    if obj.position == current_position:
                        score += obj.points
                        objectives.remove(obj)
                        # If we've collected a 15-pointer, recalculate path to the original end
                        if obj.points == 15 and current_goal != original_end:
                            current_goal = original_end
                            path = a_star(current_maze, current_position, current_goal, objectives)
                            index = 0
                            break
                
                index += 1
                
                # Check if AI has reached the current goal or needs to reroute
                if current_position == current_goal or index == len(path):
                    if current_goal == original_end and score >= 60:
                        print(f"Maze completed successfully! Final score: {score}")
                        solving = False
                    else:
                        # Find nearest 15-pointer
                        fifteen_pointers = [obj for obj in objectives if obj.points == 15]
                        if fifteen_pointers:
                            nearest_15 = min(fifteen_pointers, key=lambda obj: heuristic(current_position, obj.position))
                            current_goal = nearest_15.position
                        else:
                            current_goal = original_end
                        
                        path = a_star(current_maze, current_position, current_goal, objectives)
                        index = 0
            else:
                draw_ai(screen, path[-1])  # Keep AI at the last position

        pygame.display.flip()
        clock.tick(10)  # Control the speed of AI movement

if __name__ == "__main__":
    main()
