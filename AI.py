import random
import math

def get_cube_state(cube_state, message):

    if message == "proceed":
        print(message)
        print("AI HAS STARTED SOLVING:")
        # Iterate through each face
        
        for i, face in enumerate(cube_state):
            print(f"Face {i}: {face}")
            
            # Access and print specific stickers (1st, 3rd, 4th)
            #print(f"Sticker at position 1 on face {i}: {face[1]}")
            #print(f"Sticker at position 3 on face {i}: {face[3]}")
            #print(f"Sticker at position 4 on face {i}: {face[4]}")
            #print(f"Sticker at position 4 on face {i}: {face[5]}")
            #print(f"Sticker at position 4 on face {i}: {face[7]}")
            # Modify the stickers (for example, set them to a new value, say 9)
            
            first_algorithm = [  #daisy
                face[1] == 0,
                face[3] == 0,
                face[4] == 5,
                face[5] == 0,
                face[7] == 0
            ] 

            
                

            if face[4] == 5:
                #print("yellow Sticker found on face")
                count_white = 0
            
                # Check specific positions for white stickers (0) around the yellow center
                if face[1] == 0:
                    #print(f"White sticker found at position 1 on face {i}")
                    count_white += 1
                if face[3] == 0:
                    #print(f"White sticker found at position 3 on face {i}")
                    count_white += 1
                if face[5] == 0:
                    #print(f"White sticker found at position 5 on face {i}")
                    count_white += 1
                if face[7] == 0:
                    #print(f"White sticker found at position 7 on face {i}")
                    count_white += 1

                # Output the total count of white stickers found around the yellow center
                print(f"Total number of white stickers around the yellow center on face {i}: {count_white} white sticker")

                current_face = face[i]
                mind(current_face)
            

            
    
   
pass

def reshuffle(cube_state):
    print("Ai Re-shuffling.......")
    all_stickers = [color for face in cube_state for color in face]
                # Shuffle all stickers
    random.shuffle(all_stickers)
                # Redistribute shuffled stickers to faces
    for i in range(6):
        cube_state[i] = all_stickers[i*9:(i+1)*9]
    print("Cube state after randomization:")
    for i, face in enumerate(cube_state):
        print(f"Face {i}: {face}")
    message = "reshuffled, proceed"
    get_cube_state(cube_state,message)

def mind(recieved):
    if recieved:
        send_message = "rotate"
        print(send_message)
        #rotate_point(message=True)
    pass
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
    