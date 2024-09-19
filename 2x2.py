import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rubik's Cube 3x3")

# Cube Colors (white, green, red, blue, orange, yellow)
colors = [(255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0), (255, 255, 0)]

# Define the cube state (6 faces, each with 9 stickers)
cube_state = [
    [0] * 9,  # Front (white)
    [1] * 9,  # Back (green)
    [2] * 9,  # Left (red)
    [3] * 9,  # Right (blue)
    [4] * 9,  # Top (orange)
    [5] * 9,  # Bottom (yellow)
]

# Function to generate vertices for the entire cube
def generate_cube_vertices():
    vertices = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                vertices.append([x/1.5, y/1.5, z/1.5])
    return vertices

# Function to define faces of the cube
def define_cube_faces():
    faces = []
    # Front face
    faces.extend([(0,1,4,3), (1,2,5,4), (3,4,7,6), (4,5,8,7)])
    # Back face
    faces.extend([(18,19,22,21), (19,20,23,22), (21,22,25,24), (22,23,26,25)])
    # Left face
    faces.extend([(0,3,12,9), (3,6,15,12), (9,12,21,18), (12,15,24,21)])
    # Right face
    faces.extend([(2,11,14,5), (5,14,17,8), (11,20,23,14), (14,23,26,17)])
    # Top face
    faces.extend([(6,7,16,15), (7,8,17,16), (15,16,25,24), (16,17,26,25)])
    # Bottom face
    faces.extend([(0,9,10,1), (1,10,11,2), (9,18,19,10), (10,19,20,11)])
    return faces

vertices = generate_cube_vertices()
faces = define_cube_faces()

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
angle_x, angle_y, angle_z = math.pi/6, -math.pi/6, 0

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

    # Sort faces based on average z-coordinate (simple depth sorting)
    face_depths = []
    for i, face in enumerate(faces):
        avg_z = sum(rotated_vertices[v][2] for v in face) / 4
        face_depths.append((i, avg_z))
    face_depths.sort(key=lambda x: x[1], reverse=True)

    # Draw all faces
    for i, _ in face_depths:
        face = faces[i]
        points = [project(rotated_vertices[v], width, height, 256, 4) for v in face]
        face_index = i // 4
        color_index = cube_state[face_index][i % 4]
        pygame.draw.polygon(screen, colors[color_index], points)
        pygame.draw.polygon(screen, (0, 0, 0), points, 1)  # Draw black edges

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