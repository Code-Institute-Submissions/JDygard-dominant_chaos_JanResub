const config = {
    type: Phaser.AUTO,          // Lets the game select the graphics engine based on the device automatically
    width: 800,                // Set the canvas width
    height: 1000,                // Set the canvas width
    pixelArt: false,            // Tell the graphics engine not to blur or anti-alias, in order to preserve the pixel art effect
    scale: {
        autoCenter: Phaser.Scale.CENTER_BOTH    // Center the canvas
    },
    physics: {              // Selects a physics engine
        default: 'arcade',  // A physics engine with collisions and complex material interaction
    },
    scene: [                    // Declaring the key names for scenes
        Preloader,
        CharSelect,              // Declare the preloader scene
        Play,               // declare the gameplay scene
    ]
};

var buttonList = [];
var kiText;
var currentKi = 0;
var punch;
var playerOne;
var playerTwo;
var centerText;
var reward;
var victor;
var hpText;
var referenceHP;
var energyMask;
var roundTimer = -1;
var conclude = false;
var scene = this;
var timer;
var textDisplay = []; //Build an array to house text display objects
var char = [];
var text = [];
var instructionQueue = [];
var game = new Phaser.Game(config);         // Uses the config object keys to set the start conditions for the game
var namespace = "/test";
var socket = io(namespace);
var player1;
var player2;