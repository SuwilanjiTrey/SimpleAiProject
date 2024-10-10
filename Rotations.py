
#creating definate face rotations for each face that is front, top, back, bottom and sides
#starting tp make clockwise movements
#FRONT
def rotate_front_clockwise():
    #rotates 90 degrees
    global cube_state
    
    cube_state[0] = [
        cube_state[0][6], cube_state[0][3], cube_state[0][0],
        cube_state[0][7], cube_state[0][4], cube_state[0][1],
        cube_state[0][8], cube_state[0][5], cube_state[0][2],
    ]
    # Rotate adjacent edge stickers (Top, Right, Bottom, Left)
    cube_state[4][6], cube_state[4][7], cube_state[4][8], cube_state[3][0], cube_state[3][3], cube_state[3][6], \
    cube_state[5][2], cube_state[5][1], cube_state[5][0], cube_state[2][8], cube_state[2][5], cube_state[2][2] = \
    cube_state[2][8], cube_state[2][5], cube_state[2][2], cube_state[4][6], cube_state[4][7], cube_state[4][8], \
    cube_state[3][0], cube_state[3][3], cube_state[3][6], cube_state[5][2], cube_state[5][1], cube_state[5][0]# Top -> Right
# the cube_state[0] represents the front face which is the first element in our list of faces
# the list rearranged so that the stickers are rotated 90 degrees clocwise e.g top left corner [0] moves to bottom left [6]

def rotate_front_counterclockwise():
    global cube_state
    #rotates the front face itself
    cube_state[0] = [
        cube_state[0][2], cube_state[0][5], cube_state[0][8],
        cube_state[0][1], cube_state[0][4], cube_state[0][7],
        cube_state[0][0], cube_state[0][3], cube_state[0][6],
    ]
    # Rotate adjacent edge stickers (Top, Left, Bottom, Right)
    cube_state[4][6], cube_state[4][7], cube_state[4][8], cube_state[2][8], cube_state[2][5], cube_state[2][2], \
    cube_state[5][2], cube_state[5][1], cube_state[5][0], cube_state[3][0], cube_state[3][3], cube_state[3][6] = \
    cube_state[3][0], cube_state[3][3], cube_state[3][6], cube_state[5][2], cube_state[5][1], cube_state[5][0], \
    cube_state[2][8], cube_state[2][5], cube_state[2][2], cube_state[4][6], cube_state[4][7], cube_state[4][8]
    
#TOP    
def rotate_top_clockwise():
    global cube_state
    # Rotate the top face itself
    cube_state[4] = [
        cube_state[4][6], cube_state[4][3], cube_state[4][0],
        cube_state[4][7], cube_state[4][4], cube_state[4][1],
        cube_state[4][8], cube_state[4][5], cube_state[4][2],
    ]
    # Rotate adjacent edge stickers (Front, Right, Back, Left)
    cube_state[0][0], cube_state[0][1], cube_state[0][2], cube_state[3][0], cube_state[3][1], cube_state[3][2], \
    cube_state[1][0], cube_state[1][1], cube_state[1][2], cube_state[2][0], cube_state[2][1], cube_state[2][2] = \
    cube_state[2][0], cube_state[2][1], cube_state[2][2], cube_state[0][0], cube_state[0][1], cube_state[0][2], \
    cube_state[3][0], cube_state[3][1], cube_state[3][2], cube_state[1][0], cube_state[1][1], cube_state[1][2]

def rotate_top_counterclockwise():
    global cube_state
    # Rotate the top face itself
    cube_state[4] = [
        cube_state[4][2], cube_state[4][5], cube_state[4][8],
        cube_state[4][1], cube_state[4][4], cube_state[4][7],
        cube_state[4][0], cube_state[4][3], cube_state[4][6],
    ]
    # Rotate adjacent edge stickers (Front, Left, Back, Right)
    cube_state[0][0], cube_state[0][1], cube_state[0][2], cube_state[2][0], cube_state[2][1], cube_state[2][2], \
    cube_state[1][0], cube_state[1][1], cube_state[1][2], cube_state[3][0], cube_state[3][1], cube_state[3][2] = \
    cube_state[3][0], cube_state[3][1], cube_state[3][2], cube_state[1][0], cube_state[1][1], cube_state[1][2], \
    cube_state[2][0], cube_state[2][1], cube_state[2][2], cube_state[0][0], cube_state[0][1], cube_state[0][2]

#NOW TO MAKE FUNCTIONS THAT ALL MOVE CLOCKWISE AND COUNTER CLOCKWISE
#BOTTOM
def rotate_bottom_clockwise():
    global cube_state
    # Rotate the bottom face itself
    cube_state[5] = [
        cube_state[5][6], cube_state[5][3], cube_state[5][0],
        cube_state[5][7], cube_state[5][4], cube_state[5][1],
        cube_state[5][8], cube_state[5][5], cube_state[5][2],
    ]
    # Rotate adjacent edge stickers (Front, Left, Back, Right)
    cube_state[0][6], cube_state[0][7], cube_state[0][8], cube_state[2][6], cube_state[2][7], cube_state[2][8], \
    cube_state[1][6], cube_state[1][7], cube_state[1][8], cube_state[3][6], cube_state[3][7], cube_state[3][8] = \
    cube_state[3][6], cube_state[3][7], cube_state[3][8], cube_state[0][6], cube_state[0][7], cube_state[0][8], \
    cube_state[2][6], cube_state[2][7], cube_state[2][8], cube_state[1][6], cube_state[1][7], cube_state[1][8]

def rotate_bottom_counterclockwise():
    global cube_state
    # Rotate the bottom face itself
    cube_state[5] = [
        cube_state[5][2], cube_state[5][5], cube_state[5][8],
        cube_state[5][1], cube_state[5][4], cube_state[5][7],
        cube_state[5][0], cube_state[5][3], cube_state[5][6],
    ]
    # Rotate adjacent edge stickers (Front, Right, Back, Left)
    cube_state[0][6], cube_state[0][7], cube_state[0][8], cube_state[3][6], cube_state[3][7], cube_state[3][8], \
    cube_state[1][6], cube_state[1][7], cube_state[1][8], cube_state[2][6], cube_state[2][7], cube_state[2][8] = \
    cube_state[2][6], cube_state[2][7], cube_state[2][8], cube_state[0][6], cube_state[0][7], cube_state[0][8], \
    cube_state[3][6], cube_state[3][7], cube_state[3][8], cube_state[1][6], cube_state[1][7], cube_state[1][8]
    
    
#LEFT
def rotate_left_clockwise():
    global cube_state
    # Rotate the left face itself
    cube_state[2] = [
        cube_state[2][6], cube_state[2][3], cube_state[2][0],
        cube_state[2][7], cube_state[2][4], cube_state[2][1],
        cube_state[2][8], cube_state[2][5], cube_state[2][2],
    ]
    # Rotate adjacent edge stickers (Top, Front, Bottom, Back)
    cube_state[4][0], cube_state[4][3], cube_state[4][6], cube_state[0][0], cube_state[0][3], cube_state[0][6], \
    cube_state[5][0], cube_state[5][3], cube_state[5][6], cube_state[1][8], cube_state[1][5], cube_state[1][2] = \
    cube_state[1][8], cube_state[1][5], cube_state[1][2], cube_state[4][0], cube_state[4][3], cube_state[4][6], \
    cube_state[0][0], cube_state[0][3], cube_state[0][6], cube_state[5][0], cube_state[5][3], cube_state[5][6]

def rotate_left_counterclockwise():
    global cube_state
    # Rotate the left face itself
    cube_state[2] = [
        cube_state[2][2], cube_state[2][5], cube_state[2][8],
        cube_state[2][1], cube_state[2][4], cube_state[2][7],
        cube_state[2][0], cube_state[2][3], cube_state[2][6],
    ]
    # Rotate adjacent edge stickers (Top, Back, Bottom, Front)
    cube_state[4][0], cube_state[4][3], cube_state[4][6], cube_state[1][8], cube_state[1][5], cube_state[1][2], \
    cube_state[5][0], cube_state[5][3], cube_state[5][6], cube_state[0][0], cube_state[0][3], cube_state[0][6] = \
    cube_state[0][0], cube_state[0][3], cube_state[0][6], cube_state[4][0], cube_state[4][3], cube_state[4][6], \
    cube_state[1][8], cube_state[1][5], cube_state[1][2], cube_state[5][0], cube_state[5][3], cube_state[5][6]
    
#RIGHT
def rotate_right_clockwise():
    global cube_state
    # Rotate the right face itself
    cube_state[3] = [
        cube_state[3][6], cube_state[3][3], cube_state[3][0],
        cube_state[3][7], cube_state[3][4], cube_state[3][1],
        cube_state[3][8], cube_state[3][5], cube_state[3][2],
    ]
    # Rotate adjacent edge stickers (Top, Back, Bottom, Front)
    cube_state[4][2], cube_state[4][5], cube_state[4][8], cube_state[1][6], cube_state[1][3], cube_state[1][0], \
    cube_state[5][2], cube_state[5][5], cube_state[5][8], cube_state[0][2], cube_state[0][5], cube_state[0][8] = \
    cube_state[0][2], cube_state[0][5], cube_state[0][8], cube_state[4][2], cube_state[4][5], cube_state[4][8], \
    cube_state[1][6], cube_state[1][3], cube_state[1][0], cube_state[5][2], cube_state[5][5], cube_state[5][8]

def rotate_right_counterclockwise():
    global cube_state
    # Rotate the right face itself
    cube_state[3] = [
        cube_state[3][2], cube_state[3][5], cube_state[3][8],
        cube_state[3][1], cube_state[3][4], cube_state[3][7],
        cube_state[3][0], cube_state[3][3], cube_state[3][6],
    ]
    # Rotate adjacent edge stickers (Top, Front, Bottom, Back)
    cube_state[4][2], cube_state[4][5], cube_state[4][8], cube_state[0][2], cube_state[0][5], cube_state[0][8], \
    cube_state[5][2], cube_state[5][5], cube_state[5][8], cube_state[1][6], cube_state[1][3], cube_state[1][0] = \
    cube_state[1][6], cube_state[1][3], cube_state[1][0], cube_state[4][2], cube_state[4][5], cube_state[4][8], \
    cube_state[0][2], cube_state[0][5], cube_state[0][8], cube_state[5][2], cube_state[5][5], cube_state[5][8]

#BACK
def rotate_back_clockwise():
    global cube_state
    # Rotate the back face itself (90 degrees clockwise)
    cube_state[1] = [
        cube_state[1][6], cube_state[1][3], cube_state[1][0],
        cube_state[1][7], cube_state[1][4], cube_state[1][1],
        cube_state[1][8], cube_state[1][5], cube_state[1][2],
    ]
    # Rotate adjacent edge stickers (Top, Right, Bottom, Left)
    cube_state[4][0], cube_state[4][1], cube_state[4][2], cube_state[3][8], cube_state[3][7], cube_state[3][6], \
    cube_state[5][8], cube_state[5][7], cube_state[5][6], cube_state[2][0], cube_state[2][1], cube_state[2][2] = \
    cube_state[2][0], cube_state[2][1], cube_state[2][2], cube_state[4][0], cube_state[4][1], cube_state[4][2], \
    cube_state[3][8], cube_state[3][7], cube_state[3][6], cube_state[5][8], cube_state[5][7], cube_state[5][6]

def rotate_back_counterclockwise():
    global cube_state
    # Rotate the back face itself (90 degrees counterclockwise)
    cube_state[1] = [
        cube_state[1][2], cube_state[1][5], cube_state[1][8],
        cube_state[1][1], cube_state[1][4], cube_state[1][7],
        cube_state[1][0], cube_state[1][3], cube_state[1][6],
    ]
    # Rotate adjacent edge stickers (Top, Left, Bottom, Right)
    cube_state[4][0], cube_state[4][1], cube_state[4][2], cube_state[2][0], cube_state[2][1], cube_state[2][2], \
    cube_state[5][8], cube_state[5][7], cube_state[5][6], cube_state[3][8], cube_state[3][7], cube_state[3][6] = \
    cube_state[3][8], cube_state[3][7], cube_state[3][6], cube_state[4][0], cube_state[4][1], cube_state[4][2], \
    cube_state[2][0], cube_state[2][1], cube_state[2][2], cube_state[5][8], cube_state[5][7], cube_state[5][6]

