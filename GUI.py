import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rubik's Cube")

# Cube Colors (white, green, red, blue, orange, yellow)
colors = [(255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0), (255, 255, 0)]

# Proper Cube Vertices
vertices = [
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1,  1],
    [-1,  1,  1]
]

# Edges connecting vertices
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Faces of the cube, each defined by four vertices
faces = [
    (0, 1, 2, 3),  # Front face
    (4, 5, 6, 7),  # Back face
    (0, 1, 5, 4),  # Bottom face
    (2, 3, 7, 6),  # Top face
    (0, 3, 7, 4),  # Left face
    (1, 2, 6, 5)   # Right face
]

# Function to handle the rotation
def rotate_point(point, angle_x, angle_y, angle_z):
    # Rotation around X-axis
    y = point[1] * math.cos(angle_x) - point[2] * math.sin(angle_x)
    z = point[1] * math.sin(angle_x) + point[2] * math.cos(angle_x)
    point[1], point[2] = y, z

    # Rotation around Y-axis
    x = point[0] * math.cos(angle_y) + point[2] * math.sin(angle_y)
    z = -point[0] * math.sin(angle_y) + point[2] * math.cos(angle_y)
    point[0], point[2] = x, z

    # Rotation around Z-axis
    x = point[0] * math.cos(angle_z) - point[1] * math.sin(angle_z)
    y = point[0] * math.sin(angle_z) + point[1] * math.cos(angle_z)
    point[0], point[1] = x, y

# Function to project 3D points to 2D space
def project(point, screen_width, screen_height, fov, viewer_distance):
    factor = fov / (viewer_distance + point[2])
    x = point[0] * factor + screen_width / 2
    y = -point[1] * factor + screen_height / 2
    return (int(x), int(y))

# Function to draw buttons
def draw_button(x, y, width, height, text):
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height))
    font = pygame.font.SysFont(None, 24)
    img = font.render(text, True, (0, 0, 0))
    screen.blit(img, (x + 10, y + 10))

# Main loop
running = True
angle_x, angle_y, angle_z = 0, 0, 0

while running:
    screen.fill((0, 0, 0))  # Clear screen with black background
    
    # Draw buttons
    draw_button(50, 100, 50, 50, "X+")
    draw_button(50, 150, 50, 50, "Y+")
    draw_button(50, 200, 50, 50, "Z+")

    rotated_vertices = []
    for vertex in vertices:
        rotated_vertex = list(vertex)
        rotate_point(rotated_vertex, angle_x, angle_y, angle_z)
        rotated_vertices.append(rotated_vertex)  

    # Draw the faces with colors
    for i, face in enumerate(faces):
        points = []
        for vertex in face:
            points.append(project(rotated_vertices[vertex], width, height, 256, 4))
        pygame.draw.polygon(screen, colors[i], points)

    # Draw the edges over the faces for better visibility
    for edge in edges:
        points = []
        for vertex in edge:
            points.append(project(rotated_vertices[vertex], width, height, 256, 4))
        pygame.draw.line(screen, (0, 0, 0), points[0], points[1], 2)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 50 <= x <= 100:
                if 100 <= y <= 150:
                    angle_x += math.pi / 16
                elif 150 <= y <= 200:
                    angle_y += math.pi / 16
                elif 200 <= y <= 250:
                    angle_z += math.pi / 16

    # Update the screen
    pygame.display.flip()

pygame.quit()
