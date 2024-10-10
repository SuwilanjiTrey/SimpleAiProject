import pygame
import random
import math

# initializing pygame
pygame.init()

#creating screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rubiks cube visual simulation")

#cube colors set creating array
#white, green, red, blue, orange, yellow in order
colors = [(255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0), (255, 255, 0)]

# the cube state (6 faces, each with 9 stickers)
cube_state = [
    [0] * 9, #front (white)
    [1] * 9, #back (green)
    [2] * 9, #left (red)
    [3] * 9, #right (blue)
    [4] * 9, #top (orange)
    [5] * 9, #bottom (yellow)
]

def apply_random_move():  #function that generates random moves to simulate the cube solving
    """Applying random move to simulate rotation."""
    move_face = random.choice(['U', 'D', 'L', 'R', 'F', 'B']) #Picks random face
    direction = random.choice([1, -1]) #rotates clockwise or anticlockwise
    print(f"Simulating move: {move_face} {'CW' if direction == 1 else 'ACW'}")
    #right now its just the move that has been implemented visual logic will be done afterwards
    
def visualize_ai_solving():  #function that applies 20 moves randomly
    """Simulating cube 'solving' through random moves."""
    for _ in range(20): #20 random moves
        apply_random_move()
        pygame.time.wait(500) #Waits 500 ms to visualize each move
        
    print("cube is now visually 'solved' just for practice no logic involved yet")
    

def run_visual_simulation(): #function that handles the game loop and visual simulation
    running = True
    while running:
        screen.fill((0, 0, 0)) # Clears screen with black background
        
        #simulate cube solving process
        visualize_ai_solving()
        
        #handling quitting the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        pygame.display.flip()
        
    pygame.quit()
    
#if file is executed, start visual simulation
if __name__ == "__main__":
    run_visual_simulation()
        