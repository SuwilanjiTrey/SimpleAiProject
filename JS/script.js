// script.js

// Scene, camera, and renderer setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Define colors for the cube faces
const colors = [
    0xffffff, // Front (white)
    0x00ff00, // Back (green)
    0xff0000, // Left (red)
    0x0000ff, // Right (blue)
    0xffa500, // Top (orange)
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
function createRubiksCube() {
    const cubletSize = 0.6; // Size of each individual cublet
    const cublets = []; // Store cublet meshes

    // Create the cublets in a 3D grid for each face
    for (let x = -1; x <= 1; x++) {
        for (let y = -1; y <= 1; y++) {
            for (let z = -1; z <= 1; z++) {
                // Skip the center cublet
                if (x === 0 && y === 0 && z === 0) continue;

                const geometry = new THREE.BoxGeometry(cubletSize, cubletSize, cubletSize);
                const materials = [
                    new THREE.MeshBasicMaterial({ color: colors[cubeState[0][getCubletIndex(x, y, z, 'front')] || 0], side: THREE.DoubleSide }), // Front
                    new THREE.MeshBasicMaterial({ color: colors[cubeState[1][getCubletIndex(x, y, z, 'back')] || 1], side: THREE.DoubleSide }), // Back
                    new THREE.MeshBasicMaterial({ color: colors[cubeState[2][getCubletIndex(x, y, z, 'left')] || 2], side: THREE.DoubleSide }), // Left
                    new THREE.MeshBasicMaterial({ color: colors[cubeState[3][getCubletIndex(x, y, z, 'right')] || 3], side: THREE.DoubleSide }), // Right
                    new THREE.MeshBasicMaterial({ color: colors[cubeState[4][getCubletIndex(x, y, z, 'top')] || 4], side: THREE.DoubleSide }), // Top
                    new THREE.MeshBasicMaterial({ color: colors[cubeState[5][getCubletIndex(x, y, z, 'bottom')] || 5], side: THREE.DoubleSide }) // Bottom
                ];

                const cublet = new THREE.Mesh(geometry, materials);
                // Position the cublet in the 3D space
                cublet.position.set(x * cubletSize, y * cubletSize, z * cubletSize);
                scene.add(cublet);
                cublets.push(cublet); // Store the cublet mesh
            }
        }
    }
    return cublets; // Return array of cublet meshes
}

// Function to get the index of a cublet based on its position
function getCubletIndex(x, y, z, face) {
    // Map positions to the cublet index for each face
    const indices = {
        front: { 0: 3, 1: 4, 2: 5, '-1': 6 }, // Front face colors
        back: { 0: 6, 1: 7, 2: 8, '-1': 0 }, // Back face colors
        left: { 0: 0, 1: 3, 2: 6, '-1': 2 }, // Left face colors
        right: { 0: 2, 1: 5, 2: 8, '-1': 1 }, // Right face colors
        top: { 0: 2, 1: 3, 2: 4, '-1': 1 }, // Top face colors
        bottom: { 0: 4, 1: 5, 2: 6, '-1': 3 } // Bottom face colors
    };

    return indices[face][y] || 0; // Get the index for the specified face
}

// Call the function to create the Rubik's Cube
let cublets = createRubiksCube();

// Set camera position

// Set camera position
camera.position.set(3, 3, 3); // Adjusted camera position for better view of the cube
camera.lookAt(1, 0, 0); // Look at the center of the cube


// Variables to track rotation on each axis
let rotationSpeed = 0.01;
let rotationX = 0;
let rotationY = 0;
let rotationZ = 0;

// UI setup for buttons
function createButtons() {
    const buttonContainer = document.createElement('div');
    buttonContainer.style.position = 'absolute';
    buttonContainer.style.top = '20px';
    buttonContainer.style.left = '20px';

    const aiButton = document.createElement('button');
    aiButton.innerText = 'Trigger AI';
    aiButton.style.margin = '5px';
    aiButton.onclick = () => {
        console.log('AI triggered'); // Placeholder for AI functionality
        // Call your AI rotation logic here
    };

    const randomizeButton = document.createElement('button');
    randomizeButton.innerText = 'Randomize Cube';
    randomizeButton.style.margin = '5px';
    randomizeButton.onclick = () => {
        console.log('Cube randomized'); // Shuffle the cube state
        randomizeCube();
    };

    buttonContainer.appendChild(aiButton);
    buttonContainer.appendChild(randomizeButton);
    document.body.appendChild(buttonContainer);
}

// Shuffle the cube state and update colors
function randomizeCube() {
    // Create a new shuffled cube state for all faces
    let newState = [
        shuffleArray(cubeState[0].slice()), // Shuffle Front face
        shuffleArray(cubeState[1].slice()), // Shuffle Back face
        shuffleArray(cubeState[2].slice()), // Shuffle Left face
        shuffleArray(cubeState[3].slice()), // Shuffle Right face
        shuffleArray(cubeState[4].slice()), // Shuffle Top face
        shuffleArray(cubeState[5].slice())  // Shuffle Bottom face
    ];

    // Update the cubeState with the new shuffled state
    cubeState = newState;

    // Update the materials of the cublets
    cublets.forEach((cublet, index) => {
        const x = Math.floor((index % 27) / 9) - 1; // -1, 0, 1 for x
        const y = (Math.floor(index % 9) - 1) * -1; // 1, 0, -1 for y
        const z = (index % 3) - 1; // -1, 0, 1 for z

        // Update cublet colors based on shuffled state
        cublet.material[0].color.set(colors[cubeState[0][getCubletIndex(x, y, z, 'front')] || 0]); // Front
        cublet.material[1].color.set(colors[cubeState[1][getCubletIndex(x, y, z, 'back')] || 1]); // Back
        cublet.material[2].color.set(colors[cubeState[2][getCubletIndex(x, y, z, 'left')] || 2]); // Left
        cublet.material[3].color.set(colors[cubeState[3][getCubletIndex(x, y, z, 'right')] || 3]); // Right
        cublet.material[4].color.set(colors[cubeState[4][getCubletIndex(x, y, z, 'top')] || 4]); // Top
        cublet.material[5].color.set(colors[cubeState[5][getCubletIndex(x, y, z, 'bottom')] || 5]); // Bottom
    });
}

// Function to get the index of a cublet based on its position
function getCubletIndex(x, y, z, face) {
    // Map positions to the cublet index for each face
    const indices = {
        front: { 0: 3, 1: 4, 2: 5, '-1': 6 }, // Front face colors
        back: { 0: 6, 1: 7, 2: 8, '-1': 0 }, // Back face colors
        left: { 0: 0, 1: 3, 2: 6, '-1': 2 }, // Left face colors
        right: { 0: 2, 1: 5, 2: 8, '-1': 1 }, // Right face colors
        top: { 0: 2, 1: 3, 2: 4, '-1': 1 }, // Top face colors
        bottom: { 0: 4, 1: 5, 2: 6, '-1': 3 } // Bottom face colors
    };

    return indices[face][y] || 0; // Get the index for the specified face
}


// Shuffle utility function
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]; // Swap elements
    }
    return array;
}

// Call the function to create buttons
createButtons();

// Animation loop
function animate() {
    requestAnimationFrame(animate);

    // Apply rotation to the entire cube based on the specified speeds
    scene.rotation.x += rotationX;
    scene.rotation.y += rotationY;
    scene.rotation.z += rotationZ;

    renderer.render(scene, camera);
}

// Mouse event to control rotation
document.addEventListener('mousemove', (event) => {
    // Adjust rotation based on mouse movement
    rotationX = (event.clientY / window.innerHeight - 0.5) * rotationSpeed;
    rotationY = (event.clientX / window.innerWidth - 0.5) * rotationSpeed;
});

// Start the animation loop
animate();
