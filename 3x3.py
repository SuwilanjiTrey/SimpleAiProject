import pygame
import math
import random
from AI import get_cube_state, rotate_point


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
    [3] * 9,  # Front (blue)
    [1] * 9,  # Back (green)
    [2] * 9,  # Left (red)
    [4] * 9,  # Right (orange)
    [0] * 9,  # Top (white)
    [5] * 9,  # Bottom (yellow)
]

def randomize_state():
    global cube_state
    # Extract the center stickers (5th sticker in each face)
    centers = [face[4] for face in cube_state]

    # Create a list of all stickers excluding the center stickers
    all_stickers = []
    for face in cube_state:
        all_stickers.extend(face[:4] + face[5:])  # Skip the center sticker
    
    # Shuffle the remaining stickers
    random.shuffle(all_stickers)
    
    # Redistribute shuffled stickers to faces while keeping the center static
    for i in range(6):
        cube_state[i] = all_stickers[i*8:(i+1)*8][:4] + [centers[i]] + all_stickers[i*8:(i+1)*8][4:]

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

def AI_start(cube_state, message):
    get_cube_state(cube_state, message)
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
            if 50 <= x <= 100:
                if 100 <= y <= 150:
                    angle_x += math.pi / 16
                    #print("X+ button pressed")
                elif 150 <= y <= 200:
                    angle_y += math.pi / 16
                    #print("Y+ button pressed")
                elif 200 <= y <= 250:
                    angle_z += math.pi / 16
                    #print("Z+ button pressed")
                elif 50 <= x <= 150:
                    if 250 <= y <= 300:
                        print("Randomize button pressed")
                        randomize_state()
                    elif 300 <= y <= 350:
                        print("AI Solve button pressed")
                        ai_solving = True

    if ai_solving:
        message = "proceed"
        AI_start(cube_state, message)
        # You would update the cube state here based on AI moves
        # For now, we'll just set ai_solving back to False
        ai_solving = False

    # Update the screen
    pygame.display.flip()

pygame.quit()

