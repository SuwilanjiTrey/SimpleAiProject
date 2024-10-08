import pygame
import math
import random
#from visualize import run_visual_simulation
from Rotations import rotate_front_clockwise, rotate_front_counterclockwise, rotate_top_clockwise, rotate_top_counterclockwise, rotate_bottom_clockwise, rotate_bottom_counterclockwise, rotate_left_clockwise, rotate_left_counterclockwise, rotate_right_clockwise,  rotate_right_counterclockwise
from Rotations import rotate_back_clockwise, rotate_back_counterclockwise 

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

def randomize_state():
    global cube_state
    # Create a list of all stickers
    all_stickers = [color for face in cube_state for color in face]
    # Shuffle all stickers
    random.shuffle(all_stickers)
    # Redistribute shuffled stickers to faces
    for i in range(6):
        cube_state[i] = all_stickers[i*9:(i+1)*9]
    print("Cube state after randomization:")
    for i, face in enumerate(cube_state):
        print(f"Face {i}: {face}")

def is_solved():
    return all(len(set(face)) == 1 for face in cube_state)


def is_solved():
    return all(len(set(face)) == 1 for face in cube_state)

def get_current_face(angle_x, angle_y):
    # Determine which face is most visible based on rotation angles
    if abs(angle_y) < math.pi/4:
        return 0  # Front
    elif abs(angle_y - math.pi) < math.pi/4 or abs(angle_y + math.pi) < math.pi/4:
        return 1  # Back
    elif math.pi/4 < angle_y < 3*math.pi/4:
        return 3  # Right
    elif -3*math.pi/4 < angle_y < -math.pi/4:
        return 2  # Left
    elif angle_x > math.pi/4:
        return 5  # Bottom
    else:
        return 4  # Top

# Function to generate vertices for the entire cube
def generate_cube_vertices():
    vertices = []
    for x in [-1, -1/3, 1/3, 1]:
        for y in [-1, -1/3, 1/3, 1]:
            for z in [-1, -1/3, 1/3, 1]:
                vertices.append([x, y, z])
    return vertices

# Function to define faces of the cube
def define_cube_faces():
    faces = []
    # Helper function to get vertex indices
    def v(x, y, z):
        return 16 * x + 4 * y + z

    # Define faces for each side
    for side in range(6):
        for i in range(3):
            for j in range(3):
                if side == 0:  # Front
                    faces.append((v(i,j,3), v(i+1,j,3), v(i+1,j+1,3), v(i,j+1,3)))
                elif side == 1:  # Back
                    faces.append((v(i,j,0), v(i+1,j,0), v(i+1,j+1,0), v(i,j+1,0)))
                elif side == 2:  # Left
                    faces.append((v(0,j,i), v(0,j,i+1), v(0,j+1,i+1), v(0,j+1,i)))
                elif side == 3:  # Right
                    faces.append((v(3,j,i), v(3,j,i+1), v(3,j+1,i+1), v(3,j+1,i)))
                elif side == 4:  # Top
                    faces.append((v(i,3,j), v(i+1,3,j), v(i+1,3,j+1), v(i,3,j+1)))
                elif side == 5:  # Bottom
                    faces.append((v(i,0,j), v(i+1,0,j), v(i+1,0,j+1), v(i,0,j+1)))
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

def AI_start(cube_state):
    # This function will be implemented later with the AI logic
    # For now, it's just a placeholder
    pass

# Main loop
running = True
angle_x, angle_y, angle_z = math.pi/6, -math.pi/6, 0
ai_solving = False

while running:
    screen.fill((0, 0, 0))  # Clear screen with black background
    
    # Draw buttons
    draw_button(50, 100, 50, 50, "X+")
    draw_button(50, 150, 50, 50, "Y+")
    draw_button(50, 200, 50, 50, "Z+")
    draw_button(50, 250, 100, 50, "Randomize")
    draw_button(50, 300, 100, 50, "AI Solve")

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
        face_index = i // 9
        color_index = cube_state[face_index][i % 9]
        pygame.draw.polygon(screen, colors[color_index], points)
        pygame.draw.polygon(screen, (0, 0, 0), points, 1)  # Draw black edges

    # Display current face and solved state
    current_face = get_current_face(angle_x, angle_y)
    solved = is_solved()
    font = pygame.font.SysFont(None, 24)
    face_text = font.render(f"Current Face: {current_face}", True, (255, 255, 255))
    solved_text = font.render(f"Solved: {'Yes' if solved else 'No'}", True, (255, 255, 255))
    screen.blit(face_text, (50, 370))
    screen.blit(solved_text, (50, 400))

    # Handle events
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos

        # Example button positions for different face rotations
        if 50 <= x <= 150 and 100 <= y <= 150:  # Front face clockwise
            print("Front face clockwise rotation")
            rotate_front_clockwise(cube_state)
        elif 50 <= x <= 150 and 150 <= y <= 200:  # Front face counterclockwise
            print("Front face counterclockwise rotation")
            rotate_front_counterclockwise(cube_state)
        elif 200 <= x <= 300 and 100 <= y <= 150:  # Top face clockwise
            print("Top face clockwise rotation")
            rotate_top_clockwise(cube_state)
        elif 200 <= x <= 300 and 150 <= y <= 200:  # Top face counterclockwise
            print("Top face counterclockwise rotation")
            rotate_top_counterclockwise(cube_state)
        elif 350 <= x <= 450 and 100 <= y <= 150:  # Bottom face clockwise
            print("Bottom face clockwise rotation")
            rotate_bottom_clockwise(cube_state)
        elif 350 <= x <= 450 and 150 <= y <= 200:  # Bottom face counterclockwise
            print("Bottom face counterclockwise rotation")
            rotate_bottom_counterclockwise(cube_state)
        elif 500 <= x <= 600 and 100 <= y <= 150:  # Back face clockwise
            print("Back face clockwise rotation")
            rotate_back_clockwise(cube_state)
        elif 500 <= x <= 600 and 150 <= y <= 200:  # Back face counterclockwise
            print("Back face counterclockwise rotation")
            rotate_back_counterclockwise(cube_state)

        # Similarly, you can add buttons for left, right, and other faces
        elif 650 <= x <= 750 and 100 <= y <= 150:  # Left face clockwise
            print("Left face clockwise rotation")
            rotate_left_clockwise(cube_state)
        elif 650 <= x <= 750 and 150 <= y <= 200:  # Left face counterclockwise
            print("Left face counterclockwise rotation")
            rotate_left_counterclockwise(cube_state)
        elif 800 <= x <= 900 and 100 <= y <= 150:  # Right face clockwise
            print("Right face clockwise rotation")
            rotate_right_clockwise(cube_state)
        elif 800 <= x <= 900 and 150 <= y <= 200:  # Right face counterclockwise
            print("Right face counterclockwise rotation")
            rotate_right_counterclockwise(cube_state)


    if ai_solving:
        AI_start(cube_state)
        run_visual_simulation() #runs the visual represention when ai is triggered
        # You would update the cube state here based on AI moves
        # For now, we'll just set ai_solving back to False
        ai_solving = False

    # Update the screen
    pygame.display.flip()

pygame.quit()

