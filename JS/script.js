
// script.js

// Scene, camera, and renderer setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Define colors for the cube faces
const colors = [
    0x00ff00, // Front (green)
    0x0000ff, // Back (blue)
    0xffa500, // Left (orange)
    0xff0000, // Right (red)
    0xffffff, // Top (white)
    0xffff00  // Bottom (yellow)
];


// Create an array to represent the cube's state
let cubeState = [
    Array(9).fill(0), // Front
    Array(9).fill(1), // Back
    Array(9).fill(2), // Left
    Array(9).fill(3), // Right
    Array(9).fill(4), // Top
    Array(9).fill(5)  // Bottom
];

// Create a function to generate the Rubik's Cube based on the current state

const cubletSize = 1;
const spacing = 0.1;
const cubeSize = 3 * cubletSize + 2 * spacing;

let isAnimating = false;


// Create the Rubik's Cube
function createRubiksCube() {
    const cube = new THREE.Group();
    const cublets = [];

    for (let x = -1; x <= 1; x++) {
        for (let y = -1; y <= 1; y++) {
            for (let z = -1; z <= 1; z++) {
                const cublet = createCublet(x, y, z);
                cube.add(cublet);
                cublets.push(cublet);
            }
        }
    }

    scene.add(cube);
    return { cube, cublets };
}



// Update the createCublet function
function createCublet(x, y, z) {
    const geometry = new THREE.BoxGeometry(cubletSize, cubletSize, cubletSize);
    const materials = colors.map(color => new THREE.MeshBasicMaterial({ color }));
    const cublet = new THREE.Mesh(geometry, materials);
    cublet.position.set(
        x * (cubletSize + spacing),
        y * (cubletSize + spacing),
        z * (cubletSize + spacing)
    );
    cublet.userData.originalPosition = new THREE.Vector3(x, y, z);
    return cublet;
}

const { cube, cublets } = createRubiksCube();

// Function to get the index of a cublet based on its position
function getCubletIndex(x, y, z, face) {
    const indices = {
        front: [6, 7, 8, 3, 4, 5, 0, 1, 2],
        back: [2, 1, 0, 5, 4, 3, 8, 7, 6],
        left: [0, 3, 6, 1, 4, 7, 2, 5, 8],
        right: [8, 5, 2, 7, 4, 1, 6, 3, 0],
        top: [6, 3, 0, 7, 4, 1, 8, 5, 2],
        bottom: [2, 5, 8, 1, 4, 7, 0, 3, 6]
    };
    
    const index = (y + 1) * 3 + (x + 1);
    return indices[face][index];
}



// Set camera position
camera.position.set(3, 3, 3);
camera.lookAt(0, 0, 0);

// Variables to track rotation
let rotationSpeed = 0.01;
let rotationX = 0;
let rotationY = 0;

// Modify the randomizeCube function
let moveQueue = [];

// Modify the randomizeCube function to send the state after shuffling
async function randomizeCube() {
    if (isAnimating) return;
    isAnimating = true;

    const shuffleSequence = await requestShuffleSequence();
    moveQueue = shuffleSequence;

    await processMoveQueue();
    await sendCubeState();  // Send the new state to the AI
    isAnimating = false;
}


async function processMoveQueue() {
    while (moveQueue.length > 0) {
        const move = moveQueue.shift();
        await performMove(move);
    }
}

function getColorName(colorIndex) {
    const colorMap = {
        0: 'white',
        1: 'green',
        2: 'red',
        3: 'blue',
        4: 'orange',
        5: 'yellow'
    };
    return colorMap[colorIndex] || 'unknown';
}



// Add this function to request a shuffle sequence from the server
async function requestShuffleSequence(numMoves = 20) {
    try {
        const response = await fetch(`http://localhost:5000/shuffle?moves=${numMoves}`);
        const data = await response.json();
        return data.moves;
    } catch (error) {
        console.error('Error fetching shuffle sequence:', error);
        return [];
    }
}

// Add this function to send the current cube state to the server
// Modify the sendCubeState function to include color information
async function sendCubeState() {
    const colorState = cubeState.map(face => 
        face.map(colorIndex => getColorName(colorIndex))
    );
    
    try {
        const response = await fetch('http://localhost:5000/update_state', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ state: colorState }),
        });
        const data = await response.json();
        console.log(data.message);
    } catch (error) {
        console.error('Error sending cube state:', error);
    }
}

// Add this function to check for a specific pattern
async function checkPattern(patternName) {
    try {
        const response = await fetch(`http://localhost:5000/check_pattern?pattern=${patternName}`);
        const data = await response.json();
        console.log(`Pattern check (${patternName}):`, data.result, '-', data.message);
        return data.result;
    } catch (error) {
        console.error('Error checking pattern:', error);
        return false;
    }
}

// Call processMoveQueue in your main loop or after user interactions
// Call fixCubletPositions after each move or periodically
function update() {
    if (!isAnimating && moveQueue.length > 0) {
        processMoveQueue().then(() => {
            fixCubletPositions();
        });
    }
    requestAnimationFrame(update);
}
update();

// Add this function to solve the cube
async function solveCube() {
    if (isAnimating) return;
    isAnimating = true;

    const { moves, messages } = await requestSolve();
    console.log('AI messages:', messages);
    moveQueue = moves;

    await processMoveQueue();
    isAnimating = false;
}

// Add this function to request solving moves from the server
async function requestSolve() {
    try {
        const response = await fetch('http://localhost:5000/solve');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching solve sequence:', error);
        return { moves: [], messages: ['Error communicating with server'] };
    }
}

// Function to perform a move
async function performMove(move) {
    const [face, modifier] = move.split('');
    const clockwise = modifier !== "'";
    let axis, layer;

    switch (face) {
        case 'F': axis = 'z'; layer = 1; break;
        case 'B': axis = 'z'; layer = -1; break;
        case 'L': axis = 'x'; layer = -1; break;
        case 'R': axis = 'x'; layer = 1; break;
        case 'U': axis = 'y'; layer = 1; break;
        case 'D': axis = 'y'; layer = -1; break;
    }

    const angle = clockwise ? Math.PI/2 : -Math.PI/2;

    await rotateFace(axis, layer, angle);

    
    await rotateFace(axis, layer, angle);
    await sendCubeState();  
}

// Update the updateCubeState function to use these new functions
function updateCubeState(axis, layer, clockwise) {
    const faceIndex = axis === 'x' ? (layer > 0 ? 3 : 2) :
                      axis === 'y' ? (layer > 0 ? 4 : 5) :
                      (layer > 0 ? 0 : 1);
    
    // Rotate the face
    rotateFaceState(faceIndex, clockwise);
    
    // Rotate adjacent edges
    const adjacentFaces = getAdjacentFaces(axis, layer);
    rotateAdjacentEdges(adjacentFaces, clockwise);
}

function getAdjacentFaces(axis, layer) {
    // Assuming the faces are numbered as follows:
    // 0: Front, 1: Back, 2: Left, 3: Right, 4: Top, 5: Bottom
    switch(axis) {
        case 'x':
            return layer > 0 ? [0, 4, 1, 5] : [0, 5, 1, 4];
        case 'y':
            return layer > 0 ? [0, 3, 1, 2] : [0, 2, 1, 3];
        case 'z':
            return layer > 0 ? [4, 3, 5, 2] : [4, 2, 5, 3];
    }
}

function rotateFaceState(faceIndex, clockwise) {
    const face = cubeState[faceIndex];
    const newFace = [...face];
    if (clockwise) {
        [newFace[0], newFace[1], newFace[2], newFace[3], newFace[5], newFace[6], newFace[7], newFace[8]] = 
        [newFace[6], newFace[3], newFace[0], newFace[7], newFace[1], newFace[8], newFace[5], newFace[2]];
    } else {
        [newFace[0], newFace[1], newFace[2], newFace[3], newFace[5], newFace[6], newFace[7], newFace[8]] = 
        [newFace[2], newFace[5], newFace[8], newFace[1], newFace[7], newFace[0], newFace[3], newFace[6]];
    }
    cubeState[faceIndex] = newFace;
}


// Functions to rotate adjacent faces
function rotateAdjacentEdges(adjacentFaces, clockwise) {
    const [f1, f2, f3, f4] = adjacentFaces;
    let temp;
    if (clockwise) {
        temp = [cubeState[f1][2], cubeState[f1][5], cubeState[f1][8]];
        [cubeState[f1][2], cubeState[f1][5], cubeState[f1][8]] = [cubeState[f4][2], cubeState[f4][5], cubeState[f4][8]];
        [cubeState[f4][2], cubeState[f4][5], cubeState[f4][8]] = [cubeState[f3][2], cubeState[f3][5], cubeState[f3][8]];
        [cubeState[f3][2], cubeState[f3][5], cubeState[f3][8]] = [cubeState[f2][2], cubeState[f2][5], cubeState[f2][8]];
        [cubeState[f2][2], cubeState[f2][5], cubeState[f2][8]] = temp;
    } else {
        temp = [cubeState[f1][2], cubeState[f1][5], cubeState[f1][8]];
        [cubeState[f1][2], cubeState[f1][5], cubeState[f1][8]] = [cubeState[f2][2], cubeState[f2][5], cubeState[f2][8]];
        [cubeState[f2][2], cubeState[f2][5], cubeState[f2][8]] = [cubeState[f3][2], cubeState[f3][5], cubeState[f3][8]];
        [cubeState[f3][2], cubeState[f3][5], cubeState[f3][8]] = [cubeState[f4][2], cubeState[f4][5], cubeState[f4][8]];
        [cubeState[f4][2], cubeState[f4][5], cubeState[f4][8]] = temp;
    }
}

function rotateAdjacentToBack(clockwise) {
    let temp;
    if (clockwise) {
        temp = [cubeState[4][0], cubeState[4][1], cubeState[4][2]];
        [cubeState[4][0], cubeState[4][1], cubeState[4][2]] = [cubeState[3][2], cubeState[3][5], cubeState[3][8]];
        [cubeState[3][2], cubeState[3][5], cubeState[3][8]] = [cubeState[5][8], cubeState[5][7], cubeState[5][6]];
        [cubeState[5][8], cubeState[5][7], cubeState[5][6]] = [cubeState[2][6], cubeState[2][3], cubeState[2][0]];
        [cubeState[2][6], cubeState[2][3], cubeState[2][0]] = temp;
    } else {
        temp = [cubeState[4][0], cubeState[4][1], cubeState[4][2]];
        [cubeState[4][0], cubeState[4][1], cubeState[4][2]] = [cubeState[2][6], cubeState[2][3], cubeState[2][0]];
        [cubeState[2][6], cubeState[2][3], cubeState[2][0]] = [cubeState[5][8], cubeState[5][7], cubeState[5][6]];
        [cubeState[5][8], cubeState[5][7], cubeState[5][6]] = [cubeState[3][2], cubeState[3][5], cubeState[3][8]];
        [cubeState[3][2], cubeState[3][5], cubeState[3][8]] = temp;
    }
}

function rotateAdjacentToLeft(clockwise) {
    let temp;
    if (clockwise) {
        temp = [cubeState[0][0], cubeState[0][3], cubeState[0][6]];
        [cubeState[0][0], cubeState[0][3], cubeState[0][6]] = [cubeState[5][0], cubeState[5][3], cubeState[5][6]];
        [cubeState[5][0], cubeState[5][3], cubeState[5][6]] = [cubeState[1][8], cubeState[1][5], cubeState[1][2]];
        [cubeState[1][8], cubeState[1][5], cubeState[1][2]] = [cubeState[4][0], cubeState[4][3], cubeState[4][6]];
        [cubeState[4][0], cubeState[4][3], cubeState[4][6]] = temp;
    } else {
        temp = [cubeState[0][0], cubeState[0][3], cubeState[0][6]];
        [cubeState[0][0], cubeState[0][3], cubeState[0][6]] = [cubeState[4][0], cubeState[4][3], cubeState[4][6]];
        [cubeState[4][0], cubeState[4][3], cubeState[4][6]] = [cubeState[1][8], cubeState[1][5], cubeState[1][2]];
        [cubeState[1][8], cubeState[1][5], cubeState[1][2]] = [cubeState[5][0], cubeState[5][3], cubeState[5][6]];
        [cubeState[5][0], cubeState[5][3], cubeState[5][6]] = temp;
    }
}

function rotateAdjacentToRight(clockwise) {
    let temp;
    if (clockwise) {
        temp = [cubeState[0][2], cubeState[0][5], cubeState[0][8]];
        [cubeState[0][2], cubeState[0][5], cubeState[0][8]] = [cubeState[4][2], cubeState[4][5], cubeState[4][8]];
        [cubeState[4][2], cubeState[4][5], cubeState[4][8]] = [cubeState[1][6], cubeState[1][3], cubeState[1][0]];
        [cubeState[1][6], cubeState[1][3], cubeState[1][0]] = [cubeState[5][2], cubeState[5][5], cubeState[5][8]];
        [cubeState[5][2], cubeState[5][5], cubeState[5][8]] = temp;
    } else {
        temp = [cubeState[0][2], cubeState[0][5], cubeState[0][8]];
        [cubeState[0][2], cubeState[0][5], cubeState[0][8]] = [cubeState[5][2], cubeState[5][5], cubeState[5][8]];
        [cubeState[5][2], cubeState[5][5], cubeState[5][8]] = [cubeState[1][6], cubeState[1][3], cubeState[1][0]];
        [cubeState[1][6], cubeState[1][3], cubeState[1][0]] = [cubeState[4][2], cubeState[4][5], cubeState[4][8]];
        [cubeState[4][2], cubeState[4][5], cubeState[4][8]] = temp;
    }
}

function rotateAdjacentToUp(clockwise) {
    let temp;
    if (clockwise) {
        temp = [cubeState[0][0], cubeState[0][1], cubeState[0][2]];
        [cubeState[0][0], cubeState[0][1], cubeState[0][2]] = [cubeState[3][0], cubeState[3][1], cubeState[3][2]];
        [cubeState[3][0], cubeState[3][1], cubeState[3][2]] = [cubeState[1][0], cubeState[1][1], cubeState[1][2]];
        [cubeState[1][0], cubeState[1][1], cubeState[1][2]] = [cubeState[2][0], cubeState[2][1], cubeState[2][2]];
        [cubeState[2][0], cubeState[2][1], cubeState[2][2]] = temp;
    } else {
        temp = [cubeState[0][0], cubeState[0][1], cubeState[0][2]];
        [cubeState[0][0], cubeState[0][1], cubeState[0][2]] = [cubeState[2][0], cubeState[2][1], cubeState[2][2]];
        [cubeState[2][0], cubeState[2][1], cubeState[2][2]] = [cubeState[1][0], cubeState[1][1], cubeState[1][2]];
        [cubeState[1][0], cubeState[1][1], cubeState[1][2]] = [cubeState[3][0], cubeState[3][1], cubeState[3][2]];
        [cubeState[3][0], cubeState[3][1], cubeState[3][2]] = temp;
    }
}

function rotateAdjacentToDown(clockwise) {
    let temp;
    if (clockwise) {
        temp = [cubeState[0][6], cubeState[0][7], cubeState[0][8]];
        [cubeState[0][6], cubeState[0][7], cubeState[0][8]] = [cubeState[2][6], cubeState[2][7], cubeState[2][8]];
        [cubeState[2][6], cubeState[2][7], cubeState[2][8]] = [cubeState[1][6], cubeState[1][7], cubeState[1][8]];
        [cubeState[1][6], cubeState[1][7], cubeState[1][8]] = [cubeState[3][6], cubeState[3][7], cubeState[3][8]];
        [cubeState[3][6], cubeState[3][7], cubeState[3][8]] = temp;
    } else {
        temp = [cubeState[0][6], cubeState[0][7], cubeState[0][8]];
        [cubeState[0][6], cubeState[0][7], cubeState[0][8]] = [cubeState[3][6], cubeState[3][7], cubeState[3][8]];
        [cubeState[3][6], cubeState[3][7], cubeState[3][8]] = [cubeState[1][6], cubeState[1][7], cubeState[1][8]];
        [cubeState[1][6], cubeState[1][7], cubeState[1][8]] = [cubeState[2][6], cubeState[2][7], cubeState[2][8]];
        [cubeState[2][6], cubeState[2][7], cubeState[2][8]] = temp;
    }
}


// Update the rotateFace function
function rotateFace(axis, layer, angle) {
    return new Promise((resolve) => {
        const rotationGroup = new THREE.Group();
        const layerValue = layer * (cubletSize + spacing);
        
        // Collect all cublets in the layer
        const cublets = cube.children.filter(cublet => {
            const position = cublet.position[axis];
            return Math.abs(position - layerValue) < 0.1;
        });
        
        // Attach cublets to the rotation group
        cublets.forEach(cublet => {
            rotationGroup.attach(cublet);
        });

        scene.add(rotationGroup);

        new TWEEN.Tween(rotationGroup.rotation)
            .to({ [axis]: angle }, 500)
            .easing(TWEEN.Easing.Quadratic.Out)
            .onComplete(() => {
                // Reattach cublets to the main cube
                while (rotationGroup.children.length) {
                    const cublet = rotationGroup.children[0];
                    cube.attach(cublet);
                    
                    // Update the cublet's position and rotation
                    cublet.updateMatrixWorld(true);
                    const worldPos = new THREE.Vector3();
                    cublet.getWorldPosition(worldPos);
                    
                    // Round the position to the nearest grid point
                    cublet.position.x = Math.round(worldPos.x / (cubletSize + spacing)) * (cubletSize + spacing);
                    cublet.position.y = Math.round(worldPos.y / (cubletSize + spacing)) * (cubletSize + spacing);
                    cublet.position.z = Math.round(worldPos.z / (cubletSize + spacing)) * (cubletSize + spacing);
                    
                    // Update the cublet's rotation
                    const rotation = new THREE.Euler().setFromRotationMatrix(cublet.matrixWorld);
                    cublet.rotation.copy(rotation);
                }
                scene.remove(rotationGroup);
                updateCubeState(axis, layer, angle > 0);
                resolve();
            })
            .start();
    });
}
// Add a function to check and fix cublet positions
function fixCubletPositions() {
    cube.children.forEach(cublet => {
        const originalPos = cublet.userData.originalPosition;
        const currentPos = cublet.position.clone().divideScalar(cubletSize + spacing).round();
        
        if (!currentPos.equals(originalPos)) {
            console.log('Fixing cublet position:', originalPos, 'to', currentPos);
            cublet.position.copy(currentPos.multiplyScalar(cubletSize + spacing));
        }
    });
}



function resetCube() {
    cube.children.forEach((cublet, index) => {
        const x = (index % 3) - 1;
        const y = Math.floor((index / 3) % 3) - 1;
        const z = Math.floor(index / 9) - 1;
        
        cublet.position.set(
            x * (cubletSize + spacing),
            y * (cubletSize + spacing),
            z * (cubletSize + spacing)
        );
        cublet.rotation.set(0, 0, 0);
    });
    
    // Reset the cube state
    cubeState = [
        Array(9).fill(0), // Front
        Array(9).fill(1), // Back
        Array(9).fill(2), // Left
        Array(9).fill(3), // Right
        Array(9).fill(4), // Top
        Array(9).fill(5)  // Bottom
    ];
}




// Add this function to log the cube state in a more readable format
function logCubeState() {
    console.log("Current Cube State:");
    const faceNames = ['Front', 'Back', 'Left', 'Right', 'Top', 'Bottom'];
    cubeState.forEach((face, index) => {
        console.log(`${faceNames[index]}:`);
        for (let i = 0; i < 9; i += 3) {
            console.log(face.slice(i, i + 3).join(' '));
        }
    });
}

// Call this function after createRubiksCube and after randomizeCube
logCubeState();




// UI setup for randomize button
// Modify the createButtons function to include a "Log Cube State" button
function createButtons() {
    const buttonContainer = document.createElement('div');
    buttonContainer.style.position = 'absolute';
    buttonContainer.style.top = '20px';
    buttonContainer.style.left = '20px';

    const randomizeButton = document.createElement('button');
    randomizeButton.innerText = 'Randomize Cube';
    randomizeButton.style.margin = '5px';
    randomizeButton.onclick = randomizeCube;

    const logStateButton = document.createElement('button');
    logStateButton.innerText = 'Log Cube State';
    logStateButton.style.margin = '5px';
    logStateButton.onclick = logCubeState;

    const resetButton = document.createElement('button');
    resetButton.innerText = 'Reset Cube';
    resetButton.style.margin = '5px';
    resetButton.onclick = resetCube;

    const floatButton = document.createElement('button');
    floatButton.innerText = 'Toggle Float';
    floatButton.style.margin = '5px';
    floatButton.onclick = toggleFloating;

    
    const aiShuffleButton = document.createElement('button');
    aiShuffleButton.innerText = 'AI Shuffle';
    aiShuffleButton.style.margin = '5px';
    aiShuffleButton.onclick = randomizeCube;

    const checkSolvedButton = document.createElement('button');
    checkSolvedButton.innerText = 'Check if Solved';
    checkSolvedButton.style.margin = '5px';
    checkSolvedButton.onclick = () => checkPattern('solved');


    const aiSolveButton = document.createElement('button');
    aiSolveButton.innerText = 'AI Solve';
    aiSolveButton.style.margin = '5px';
    aiSolveButton.onclick = solveCube;

    buttonContainer.appendChild(checkSolvedButton);
    buttonContainer.appendChild(aiSolveButton);
    buttonContainer.appendChild(aiShuffleButton);
    buttonContainer.appendChild(randomizeButton);
    buttonContainer.appendChild(logStateButton);
    buttonContainer.appendChild(resetButton);
    buttonContainer.appendChild(floatButton);
    document.body.appendChild(buttonContainer);
}


createButtons();

// Animation loop
let isFloating = false;
let floatSpeed = 0.01;

// Modify the animate function
function animate(time) {
    requestAnimationFrame(animate);
    TWEEN.update(time);
    
    // Only apply rotation when floating is enabled
    if (isFloating) {
        cube.rotation.x += rotationX;
        cube.rotation.y += rotationY;
    }
    
    renderer.render(scene, camera);
}

// Add a function to toggle floating
function toggleFloating() {
    isFloating = !isFloating;
    // Reset rotation when floating is disabled
    if (!isFloating) {
        cube.rotation.set(0, 0, 0);
    }
}

// Modify the mouse event listener to only update rotation values when floating
document.addEventListener('mousemove', (event) => {
    if (isFloating) {
        rotationX = (event.clientY / window.innerHeight - 0.5) * floatSpeed;
        rotationY = (event.clientX / window.innerWidth - 0.5) * floatSpeed;
    }
});
// Start the animation loop
animate();
