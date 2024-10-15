import pygame
import sys
from queue import PriorityQueue

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Maze configuration
MAZE = [
    "####################",
    "#S#       #        #",
    "# # #####   ######## ",
    "#   #   # #        #",
    "# ### # # # ########",
    "#     #   #        #",
    "####### ########## #",
    "#     #          # #",
    "# ### ############ #",
    "#   #              #",
    "# # # ##############",
    "# #      #         #",
    "# ###### # #########",
    "#                 E#",
    "####################"
]

# Cell size
CELL_SIZE = 30

# Set up the display
WIDTH = len(MAZE[0]) * CELL_SIZE
HEIGHT = len(MAZE) * CELL_SIZE + 50  # Extra space for the button
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver with Start Button")

class Node:
    def __init__(self, position, g=0, h=0, parent=None):
        self.position = position
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

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

def a_star(maze, start, end):
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

def draw_maze(screen, maze):
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

def draw_ai(screen, position):
    x, y = position
    center = ((y + 0.5) * CELL_SIZE, (x + 0.5) * CELL_SIZE)
    pygame.draw.circle(screen, GREEN, center, CELL_SIZE // 3)

def draw_button(screen, text, position, size):
    font = pygame.font.Font(None, 36)
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    return button_rect

def main():
    start, end = find_start_end(MAZE)
    print(f"Start: {start}, End: {end}")  # Debug print
    
    if start is None or end is None:
        print("Start or end position not found in the maze!")
        return

    clock = pygame.time.Clock()
    solving = False
    path = None
    index = 0

    button_rect = draw_button(screen, "Start Solving", (WIDTH // 2 - 75, HEIGHT - 40), (150, 30))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos) and not solving:
                    solving = True
                    path = a_star(MAZE, start, end)
                    if path:
                        print(f"Path found: {path}")
                        index = 0
                    else:
                        print("No path found!")

        screen.fill(WHITE)
        draw_maze(screen, MAZE)
        button_rect = draw_button(screen, "Start Solving", (WIDTH // 2 - 75, HEIGHT - 40), (150, 30))

        if solving and path:
            if index < len(path):
                draw_ai(screen, path[index])
                index += 1
            else:
                draw_ai(screen, path[-1])  # Keep AI at the end position

        pygame.display.flip()
        clock.tick(5)  # Control the speed of AI movement

if __name__ == "__main__":
    main()
