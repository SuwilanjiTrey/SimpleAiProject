#this code shall use the breadth-first search and depth-first search algorithms
#bfs guaranties the shortest solution in terms of moves and dfs uses less memory and can find solutions quickly in certain cases
from collections import deque #imports the deque (double eneded queue) class from collections module, allows appending and popping elements from both ends
from Rotations import rotate_right_clockwise, rotate_right_counterclockwise, rotate_left_clockwise, rotate_left_counterclockwise, rotate_front_clockwise, rotate_front_counterclockwise, rotate_top_clockwise, rotate_top_counterclockwise, rotate_bottom_clockwise, rotate_bottom_counterclockwise, rotate_back_clockwise, rotate_back_counterclockwise

def bfs_solve(cube_state):
    #creating queue and geting from imported source
    queue = deque() #intializes an empty queue to keep track of the cube
    visited = set() #initializes an empty set to keep track of the states already visited to prevent revisiting and getting stuck in loops
    queue.append((cube_state, [])) #(current state of cube, path to reach this state)
    #append adds an item into the queue, hence adds a tuple where first element is the initial cube state and second element is an empty list that holds the moves taken to reach that state 
    
    while queue: #creating loop to continue as long as there are states in the queue to explore
        current_state, path = queue.popleft() #this removes and returns leftmost element from the queue, path contains the moves take to get the state
        
        if is_solved(current_state): #checks for solutions, if the current state is solved with the is_solved function, path is returned and path contains moves leading to solution
            return path #returns the moves that made or led to the solution
        
        #getting all possible moves from current state
        for move in get_all_possible_moves(current_state): #retrieves all possible moves from current state using thee get_all_possible_moves function and iterates over them 
            next_state = apply_move(current_state, move) #for each move, generate the next_state by applying that move to the current state using apply_move function
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [move])) #we append new state and updated path to the queue
                
                
    return None # no solutions found

def is_solved(state):
    # the is solved logic here
    pass

def get_all_possible_moves(state):
    #logic to return a list of all possible moves from the current state
    moves = []
    #add moves for rotating each face in both clockwise and counterclockwise
    
    #upper face rotation as u and u'
    moves.append(('U', 'clockwise'))
    moves.append(('U_prime', 'counterclockwise'))
    
    #down face rotation as D and D'
    moves.append(('D', 'clockwise'))
    moves.append(('D_prime', 'counterclockwise'))
    
    #left face rotation as L and L'
    moves.append(('L', 'clockwise'))
    moves.append(('L_prime', 'counterclockwise'))
    
    #right as R and R'
    moves.append(('R', 'clockwise'))
    moves.append(('R_prime', 'counterclockwise'))
    
    #front F and F' 
    moves.append(('F', 'clockwise'))
    moves.append(('F_prime', 'counterclockwise'))
    
    #back B and B'
    moves.append(('B', 'clockwise'))
    moves.append(('B_prime', 'counterclockwise'))
    
    return moves
    

def apply_move(state, move):
    # logic to apply a move to the state and return the new state
    if move == 'R':
        rotate_right_clockwise()
    elif move == 'R_prime':
        rotate_right_counterclockwise()
    elif move == 'L':
        rotate_left_clockwise()
    elif move == 'L_prime':
        rotate_left_counterclockwise()
    elif move == 'F':
        rotate_front_clockwise()
    elif move == 'F_prime':
        rotate_front_counterclockwise()
    elif move == 'U':
        rotate_top_clockwise()
    elif move == 'U_prime':
        rotate_top_counterclockwise()
    elif move == 'D':
        rotate_bottom_clockwise()
    elif move == 'D_prime':
        rotate_bottom_counterclockwise()
    elif move == 'B':
        rotate_back_clockwise()
    elif move == 'B_prime':
        rotate_back_counterclockwise()
    else:
        print("Invalid move")
    
    # Return the updated state (assuming your rotation functions modify a global cube_state)
    return state
