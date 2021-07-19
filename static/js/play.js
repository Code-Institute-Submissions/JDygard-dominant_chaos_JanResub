class Play extends Phaser.Scene {
    constructor() {
        super ("Play")
    }

    preload(){
        this.anims.create({                                                 // Creating our punch animation
            key: "punch1",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 0, end: 1 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our punch animation
            key: "punch2",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 8, end: 9 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our kick animation
            key: "kick",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 32, end: 35 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our idle animation
            key: "idle",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 24, end: 25 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our dodge animation
            key: "dodge",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 40, end: 41 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our block animation
            key: "block",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 48, end: 49 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our parry animation
            key: "parry",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 16, end: 17 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our shinkick animation
            key: "shinkick",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 12, end: 13 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our jab animation
            key: "jab",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 0, end: 1 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our spinkick animation
            key: "spinkick",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 56, end: 57 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our knee animation
            key: "knee",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 4, end: 5 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our elbow animation
            key: "elbow",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 20, end: 21 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our uppercut animation
            key: "uppercut",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 28, end: 29 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our uppercut animation
            key: "hit",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 60, end: 61 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
    }

    animationHandler(name, method, extra, duration){
        let aggressor;
        let defender;
        let ch_class;
        let aggressorObj;
        if (player1["name"] == name){
            aggressor = playerOne
            defender = playerTwo
            ch_class = player1["ch_class"]
            aggressorObj = player1
        } else {
            aggressor = playerTwo
            defender = playerOne
            ch_class = player2["ch_class"]
            aggressorObj = player2
        }

        if (method == "kick"){
            aggressor.anims.play({
                key: 'kick',
                repeat: 1,
                duration: duration
            });
        }
        if (ch_class == "inward_fist"){
            let methods = ["shinkick", "jab", "spinkick", "knee", "elbow", "uppercut"];
            let aggressorKi = aggressorObj["ki"];
            for (let i in methods){
                if (method == methods[i]){
                    aggressor.anims.play({
                        key: methods[i],
                        repeat: 1,
                        duration: duration
                    });
                    aggressorObj["ki"] = aggressorKi + extra;
                    console.log(methods[i])
                }
            }
        }

        if (extra == "dodge"){
            defender.anims.play({
                key: 'dodge',
                repeat: 1,
                duration: duration
            });
        } else if (extra == "block"){
            defender.anims.play({
                key: 'block',
                repeat: 1,
                duration: duration
            });
        } else if (extra == "parry"){
            defender.anims.play({
                key: 'parry',
                repeat: 1,
                duration: duration
            });
        } else if (extra == "miss"){
            defender.anims.play({
                key: 'idle',
                repeat: 1,
                duration: duration
            })
        } else {
            defender.anims.play({
                key: 'hit',
                repeat: 1,
                duration: duration
            })
        }

        if (method == "auto"){
            if (punch == 0){
                aggressor.anims.play({
                    key: 'punch1',
                    repeat: 1,
                    duration: duration
                });
                punch = 1;
            } else {
                aggressor.anims.play({
                    key: 'punch2',
                    repeat: 1,
                    duration: duration
                });
                punch = 0;
            }
        }
    }

    lexicalParser(name, method, damage, extra){
        let verb = method;
        let message;
        let opponent;

        if (name == player1["name"]){
            opponent = player2["name"];
        } else {
            opponent = player1["name"];
        }

        if (method == "auto"){
            verb = "strike"
        }

        if (method == "kick"){
            verb = "kick"
        }


        if (damage == 0){
            if (extra == "miss"){
                message = `${name} attempts to ${verb} ${opponent}, but misses!`
            }
            else if (extra == "dodge"){
                message = `${name} attempts to ${verb} ${opponent}, but they dodge it!`
            }
            else if (extra == "block"){
                message = `${name} attempts to ${verb} ${opponent}, but they block it!`
            }
            else if (extra == "parry"){
                message = `${name} attempts to ${verb} ${opponent}, but they parry it!`
            }
            else {
                message = `${name} ${verb}s ${opponent}, oh so gently. (0)`
            }
        }
        if (damage >= 1){
            message = `${name} ${verb}s ${opponent}. (${damage})`
        }
        this.displayText(message)
    }

    displayText(message){
        let newText = this.add.text(20,630,message)
        for (let i = 0; i < textDisplay.length; i++){
            let oldPos = textDisplay[i].y;
            textDisplay[i].setY(oldPos+30);
        }
        textDisplay.unshift(newText)
    }    
    
    announceText(message){
        centerText.setText(message)
    }

    socketData(message) {
        var socket = io(namespace);
        socket.emit('playdata', message);
    }

    queryData(){
        socket.emit('query', "empty");
    }

    buttonListMaker(data){
        let iterator = 0
        for (let i in data){
            let keyData = {}
            keyData[i] = data[i]
            buttonList[iterator] = keyData
            iterator += 1
        }
        this.buttonMaker()
        
    }

    buttonMaker(){
        let length = buttonList.length;
        let numberOfRows = Math.ceil(length / 4);
        let lastRow = length % 4;
        for (let i = 0; i < buttonList.length; i++){     // Loop through the saved commands
            buttons[i] = this.add.sprite(5,475, 'button')
            console.log("button2")
            let string = Object.keys(buttonList[i])[0]  // Get the key string out
            buttons[i].on('pointerdown', function(){
                socket.emit('query', string)
                console.log("button")
            })
        }
    }

    parseSocketData(data){  // A method for parsing and distrubiting data from the frontend
        if (data[0] != undefined)
            if (data[0]["max_hp"]){ // Using the "max hp" key to identify the 'welcome package' containing
                player1 = data[0];  // data about the two combatants.
                player1["hp"] = player1["max_hp"]   // Get an hp total for the UI
                if (player1["ch_class"] == "inward_fist")
                    player1["ki"] = 0
                this.buttonListMaker(player1["abilities"])

                player2 = data[1];
                player2["hp"] = player2["max_hp"]
                if (player2["ch_class"] == "inward_fist")
                    player2["ki"] = 0
        
        } else {    // All other data should be bulk data with attacks, so a for loop parses the data
            for (let i in data){  

                if (data[i]["method"] == "victor"){ // I had to run the victory data through the autoattack queue in order to allow the UI a chance to catch up with the server before announcing the victory
                    victor = data[i]["name"];
                    reward = data[i]["extra"];
                    conclude = true;
                    setTimeout(function(){
                        scene.announceText(`${victor} wins, ${reward} exp awarded.`);
                    }, 1000);
                }
                instructionQueue.push(data[i]);
            }
        }
    }

    queueHandler(){
        scene = this
        let intervalTimer = 5000 / instructionQueue.length;
        let tempQueue = instructionQueue;
        instructionQueue = [];
        for (let i = 0; i < tempQueue.length; i++){
            setTimeout(function(){                                                          // Wait for a moment
                scene.damageHandler(tempQueue[i]["name"], tempQueue[i]["damage"]);                                                           // before removing the tint
            }, intervalTimer * i);    
            setTimeout(function(){                                                          // Wait for a moment
                scene.animationHandler(tempQueue[i]["name"], tempQueue[i]["method"], tempQueue[i]["extra"], intervalTimer);                                                           // before removing the tint
            }, intervalTimer * i);     
            setTimeout(function(){                                                          // Wait for a moment
                scene.lexicalParser(tempQueue[i]["name"], tempQueue[i]["method"], tempQueue[i]["damage"], tempQueue[i]["extra"]);                                                           // before removing the tint
            }, intervalTimer * i); 

            /* 
            read extras, we will work with that when shields come
            */

        }
    }

    damageHandler(name, damage){
        var stepWidth = (energyMask.displayWidth - 50) / player1["max_hp"];  // Figure out how much the bar should move for each point based on the max value
        if (name == player2["name"]){
            energyMask.x -= damage * stepWidth;             // Move the mask
            player1["hp"] -= damage
            let newText = `${player1["hp"]}/${player1["max_hp"]}`
            hpText.setText(newText); 
        }
    }


    create(){
        var scene = this; // Establish context
        // Healthbar mask system from evo.
        centerText = this.add.text(400, 300, "")
            .setFontSize(30)
            .setDepth(10)
            .setOrigin(0.5);

        hpText = this.add.text(207, 90, "")
            .setFontSize(18)
            .setDepth(10);

        kiText = this.add.text(350, 90, "Ki: 0")
            .setFontSize(18)
            .setDepth(10);
            
        let emptyBar = this.add.sprite(207, 90, 'emptybar')
            .setDepth(6)                                        // Set the depth so it appears on top of everything
            .setScale(1.5);                                     // Make it a little bigger :)
        let energyBar = this.add.sprite(207, 90, 'energybar')   // Make an energy bar
            .setDepth(6)                                        // Set the depth so it appears on top of everything
            .setScale(1.5);                                     // Make it a little bigger :)
        energyMask = this.add.sprite(207, 90, 'energybar')      // Make a mask to hide some of the bar when the health is below max
            .setDepth(6)                                        // Set the depth so it appears on top of everything       
            .setScale(1.5);                                     // Make it a little bigger :)
        energyMask.visible = false;                             // Make it invisble
        energyBar.mask = new Phaser.Display.Masks.BitmapMask(this, energyMask); // Make the mask act like a mask

        let background = this.add.image(0, 0, 'background')
            .setOrigin(0)
            .setScale(0.8); // Show and orient the background image
        playerOne = this.add.sprite(325, 400, 'idle')
            .setScale(2)
        playerTwo = this.add.sprite(425, 400, 'idle')
            .setScale(2)
            .setFlip(true, false)
        playerOne.anims.play({
            key: 'idle',
            repeat: -1,
        })
        var namespace = "/test"; // Namespace used to identify which user this is
        var socket = io(namespace); // Establish socket variable


// ========================== Input listener ============================
// ===== This little block of code listens for keypresses and then ======
// ===== compares it to the list of user-customized command keys and ====
// ===== list of available abilities. It will emit a command to the =====
// ===== backend when it all matches.                               =====

        this.input.keyboard.on('keydown', function (event) { // Listen for any keypress
            for (let i = 0; i < buttonList.length; i++){     // Loop through the saved commands
                let string = Object.keys(buttonList[i])[0]  // Get the key string out
                if (event.keyCode == eval("Phaser.Input.Keyboard.KeyCodes." + buttonList[i][string]) ){ // Compare the keyCode to the one saved in the character profile
                    socket.emit("query", string); // Then send the command to the backend
                    break // Break the for loop, because there's no such thing as a double-positive
                }
            }
        });

// ====================== Main socket listener ====================
// ===== This is the socket listener that sends and receives ======
// ===== socket information to and from the backend.         ======

        socket.on('query', function(message) { // Listen for incoming data
            if (message == "conclude") { // If the script says someone won
                conclude = true;         // Set the fight to end
            }
            else if (message !== "empty"){ // Otherwise, we know it's data
                scene.parseSocketData(message);  // So pass it to the data handler
            }
        })

// ===================== Main timer ============================
// ===== This is the main function for controlling the game ====
// ===== temporally. The timing set here in half-second     ====
// ===== increments controls the flow of the game.
        timer = setInterval(function() { // Set the interval to a global variable
            roundTimer += 1;             // Increment to keep track of the rounds
            if (roundTimer == 6){        // When a round is over
                scene.queueHandler();    // Call the queue handler to process the data for the next round
                roundTimer = 0;          // Reset the round timer
            }
            if (conclude == true){       // If the variable for conclude has been set
                scene.queueHandler();    // Run the last bits of the queue
                clearInterval(timer);    // And dump this interval
            }
            socket.emit("query", 'empty'); // Empty queries are requests for information
        },500);

        this.socketData("play init"); // Call the backend to start the show
    }

    update(){
        var scene = this; // Establish context
        if (player1 != undefined)   // Only run this when the player1 object has been established from the backend
            if (currentKi != player1["ki"]){    // If the amount of ki the player has is higher than the amount being displayed
                currentKi = player1["ki"];      // Gather the current ki
                kiText.setText(currentKi);      // And display the correct amount
            }
    }
}

/* Read var for button locations:
    -Make it adjustable
    -Make it appear in order
Visuals:
    Commands list:
        Displays items as they are entered
        Eliminates items as they are executed
    Rounds timer visual
        -this is the bracketed display that shows round timing
        -use a phaser group to move them in concert
        -put bars on it to show timing
        -Can a user submit a command in the interim between the server round and the client round so that the display show it incorrectly?
        -You could have the server to deliver a handshake that sets the timing for the display
        -You could sync the rounds with a failsafe that adjusts the round timing after a desync
            -this could replace the "empty" part of the query message from the client
        -The server queue emitter itself could append a round timing message when submitting the display queue to the client.
        
*/