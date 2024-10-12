import random
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



class RubiksCubeAI:
    def __init__(self):
        self.moves = ['F', 'B', 'L', 'R', 'U', 'D', "F'", "B'", "L'", "R'", "U'", "D'"]
        self.current_state = None
        self.color_map = {
            'green': 0,
            'blue': 1,
            'orange': 2,
            'red': 3,
            'white': 4,
            'yellow': 5
        }
        self.inverse_color_map = {v: k for k, v in self.color_map.items()}

    def shuffle_cube(self, num_moves=20):
        shuffle_sequence = [random.choice(self.moves) for _ in range(num_moves)]
        return shuffle_sequence

    def update_state(self, new_state):
        self.current_state = [[self.color_map[color] for color in face] for face in new_state]

    def orient_cube(self):
        yellow_face = next(i for i, face in enumerate(self.current_state) if face[4] == self.color_map['yellow'])
        if yellow_face != 0:  # If yellow is not on the front face
            rotation_moves = {
                1: ['U', 'U'],  # Back to front
                2: ["U'"],  # Left to front
                3: ['U'],  # Right to front
                4: ['F', 'F'],  # Top to front
                5: ["B", "B"]  # Bottom to front
            }
            solution = rotation_moves[yellow_face]
            for move in solution:
                self.apply_move(move)
            return solution
        return []

    def solve_cube(self):
        if self.current_state is None:
            return [], "Cube state not available"

        solution = []
        messages = []

        print("Current cube state:", self.current_state)
       
        if self.is_solved():
            return solution, ["Cube is already solved"]

        # Orient the cube with yellow center on front face
        orient_moves = self.orient_cube()
        solution.extend(orient_moves)
        messages.append("Cube oriented with yellow center on front face")

        # Solve white cross (daisy pattern)
        daisy_solution, daisy_messages = self.solve_daisy()
        solution.extend(daisy_solution)
        messages.extend(daisy_messages)

        # TODO: Implement further solving steps

        return solution, messages
    

    def is_solved(self):
        if self.current_state is None:
            return False
        return all(all(color == face[0] for color in face) for face in self.current_state)



    def solve_daisy(self):
        solution = []
        messages = []
        
        if self.has_daisy():
            messages.append("Daisy pattern already formed")
            return solution, messages

        messages.append("Attempting to form daisy pattern")
        
        # Find white edges and move them to the top face
        for _ in range(4):  # We need to place 4 white edges
            white_edge = self.dfs_search('white', exclude_face=4)  # Exclude top face
            if white_edge:
                face, edge = white_edge
                moves = self.move_white_edge_to_top(face, edge)
                solution.extend(moves)
                for move in moves:
                    self.apply_move(move)

        messages.append("Daisy pattern formed")
        return solution, messages

    def has_daisy(self):
        if self.current_state is None:
            return False
        top_face = self.current_state[4]  # Top face
        return (top_face[1] == top_face[3] == top_face[5] == top_face[7] == self.color_map['white'])

    def dfs_search(self, target_color, exclude_face=None):
        # Keep track of visited faces and edges to prevent infinite recursion
        visited = set()

        def dfs(face, edge):
            # Skip the excluded face
            if face == exclude_face:
                return None

            # Check if the current (face, edge) has already been visited
            if (face, edge) in visited:
                return None
            
            # Mark the current (face, edge) as visited
            visited.add((face, edge))

            # Base case: if the current face's edge has the target color, return it
            if self.current_state[face][edge] == self.color_map[target_color]:
                return (face, edge)

            # Recursively check neighboring faces (avoiding the current face)
            for next_face in range(6):
                if next_face != face:
                    result = dfs(next_face, edge)
                    if result:
                        return result

            return None

        # Start DFS from the front face (0) and search for the target color on the edges
        for edge in [1, 3, 5, 7]:  # Iterate over relevant edges (ignoring corners)
            result = dfs(0, edge)
            if result:
                return result

        return None


    def move_white_edge_to_top(self, face, edge):
        moves = []
        # Map of edge indices to their names
        edge_names = {1: 'top', 3: 'left', 5: 'right', 7: 'bottom'}
        edge_name = edge_names[edge]

        if face == 0:  # Front face
            if edge_name == 'top':
                moves = ["F", "R", "U'", "R'"]
            elif edge_name == 'left':
                moves = ["L'", "U'", "L"]
            elif edge_name == 'right':
                moves = ["R", "U", "R'"]
            elif edge_name == 'bottom':
                moves = ["F", "F", "U", "R", "U'", "R'"]
        elif face == 1:  # Back face
            if edge_name == 'top':
                moves = ["B", "L", "U'", "L'"]
            elif edge_name == 'left':
                moves = ["L", "U", "L'"]
            elif edge_name == 'right':
                moves = ["R'", "U'", "R"]
            elif edge_name == 'bottom':
                moves = ["B", "B", "U", "L", "U'", "L'"]
        elif face == 2:  # Left face
            if edge_name == 'top':
                moves = ["L", "F", "U'", "F'"]
            elif edge_name == 'left':
                moves = ["B'", "U'", "B"]
            elif edge_name == 'right':
                moves = ["F", "U", "F'"]
            elif edge_name == 'bottom':
                moves = ["L", "L", "F", "U'", "F'"]
        elif face == 3:  # Right face
            if edge_name == 'top':
                moves = ["R", "B", "U'", "B'"]
            elif edge_name == 'left':
                moves = ["F'", "U'", "F"]
            elif edge_name == 'right':
                moves = ["B", "U", "B'"]
            elif edge_name == 'bottom':
                moves = ["R", "R", "B", "U'", "B'"]
        elif face == 5:  # Bottom face
            if edge_name == 'top':
                moves = ["F", "F"]
            elif edge_name == 'left':
                moves = ["L", "L", "U"]
            elif edge_name == 'right':
                moves = ["R", "R", "U'"]
            elif edge_name == 'bottom':
                moves = ["B", "B", "U", "U"]

        return moves

    def apply_move(self, move):
        # Define the faces affected by each move
        affected_faces = {
            'F': ([0, 2, 4, 3], [6, 3, 0, 1, 2, 5, 8, 7]),
            'B': ([1, 3, 4, 2], [2, 5, 8, 1, 0, 3, 6, 7]),
            'L': ([2, 0, 4, 1], [0, 3, 6, 1, 2, 5, 8, 7]),
            'R': ([3, 1, 4, 0], [8, 5, 2, 1, 0, 3, 6, 7]),
            'U': ([4, 2, 1, 3], [2, 5, 8, 1, 0, 3, 6, 7]),
            'D': ([5, 3, 1, 2], [6, 3, 0, 1, 2, 5, 8, 7])
        }
        
        face, ring = affected_faces[move[0]]
        turns = 1 if len(move) == 1 else 3  # 3 turns for counterclockwise (e.g., F')

        # Rotate the face
        self.rotate_face(face[0], turns)
        
        # Now add a loop to properly access each face[i] and ring[i]
        for i in range(8):
            print(f"Face index: {face[i % 4]}, Ring index: {ring[i]}")
            print(f"Current state: {self.current_state[face[i % 4]]}")

        # Rotate the ring
        ring_values = [self.current_state[face[i % 4]][ring[i]] for i in range(8)]
        ring_values = ring_values[-2*turns:] + ring_values[:-2*turns]
        for i in range(8):
            self.current_state[face[i % 4]][ring[i]] = ring_values[i]

    
    def rotate_face(self, face, turns):
        for _ in range(turns):
            self.current_state[face] = [
                self.current_state[face][6], self.current_state[face][3], self.current_state[face][0],
                self.current_state[face][7], self.current_state[face][4], self.current_state[face][1],
                self.current_state[face][8], self.current_state[face][5], self.current_state[face][2]
            ]




    # Additional helper methods can be added here as needed
ai = RubiksCubeAI()

@app.route('/shuffle', methods=['GET'])
def shuffle():
    num_moves = request.args.get('moves', default=20, type=int)
    shuffle_sequence = ai.shuffle_cube(num_moves)
    return jsonify({'moves': shuffle_sequence})

@app.route('/update_state', methods=['POST'])
def update_state():
    new_state = request.json['state']
    ai.update_state(new_state)
    return jsonify({'message': 'State updated successfully'})

@app.route('/solve', methods=['GET'])
def solve():
    solution, messages = ai.solve_cube()
    return jsonify({'moves': solution, 'messages': messages})

if __name__ == '__main__':
    app.run(debug=True)
