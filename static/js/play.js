class Play extends Phaser.Scene {
    constructor() {
        super ("Play");
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

    // This is the animationHandler(). As expected, it handles which animations should be played
    animationHandler(name, method, extra, duration){
        // Setting up some local variables
        let aggressor;
        let defender;
        let ch_class;
        let aggressorObj;

        // Making sure we are working with the correct character
        if (player1.name == name){
            aggressor = playerOne;
            defender = playerTwo;
            ch_class = player1.ch_class;
            aggressorObj = player1;
        } else {
            aggressor = playerTwo;
            defender = playerOne;
            ch_class = player2.ch_class;
            aggressorObj = player2;
        }

        // A separate statement for kicks
        if (method == "kick"){
            aggressor.anims.play({
                key: 'kick',
                repeat: 1,
                duration: duration
            });
        }

        // A for loop that checks for any of the combo-building moves used by the Fist class
        if (ch_class == "inward_fist"){
            let methods = ["shinkick", "jab", "spinkick", "knee", "elbow", "uppercut"]; // A list of moves to be iterated over
            for (let i in methods){
                if (method == methods[i]){ // If the method that activated the animation handler is found
                    aggressor.anims.play({ // Play the relevant animation (defined in the preload() method above)
                        key: methods[i],
                        repeat: 1,
                        duration: duration
                    });
                    if (extra) { // If it is a fist combo-building move, the extras part is the amount of Ki gained
                        aggressorObj.ki = extra; // So we will add that just as the animation plays for the illusion of continuity
                    }
                }
            }
        }

        // Various animations for the victim of the attack
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
            });
        } else {
            defender.anims.play({
                key: 'hit',
                repeat: 1,
                duration: duration
            });
        }

        // And some animations for executing auto attacks
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

    // The lexical parser takes the information sent from the backend and parses it into readable text in a combat log.
    lexicalParser(name, method, damage, extra){
        // Some useful local variables
        let verb = method;
        let message;
        let opponent;

        // Getting the name positions right.
        if (name == player1.name){
            opponent = player2.name;
        } else {
            opponent = player1.name;
        }

        // Picking the right verb
        if (method == "auto"){
            verb = "strike";
        }

        if (method == "kick"){
            verb = "kick";
        }

        // Some messages for 0 damage states
        if (damage == 0){
            if (extra == "miss"){
                message = `${name} attempts to ${verb} ${opponent}, but misses!`;
            }
            else if (extra == "dodge"){
                message = `${name} attempts to ${verb} ${opponent}, but they dodge it!`;
            }
            else if (extra == "block"){
                message = `${name} attempts to ${verb} ${opponent}, but they block it!`;
            }
            else if (extra == "parry"){
                message = `${name} attempts to ${verb} ${opponent}, but they parry it!`;
            }
            else {
                message = `${name} ${verb}s ${opponent}, oh so gently. (0)`;
            }
        }
        // And a message for successful attacks
        if (damage >= 1){
            message = `${name} ${verb}s ${opponent}. (${damage})`;
        }
        this.displayText(message); // Send it to the text display function
    }

    // This is the method that shows text in the combat log.
    displayText(message){
        let newText = this.add.text(20,630,message); // Pop a new message into place at the top
        for (let i = 0; i < textDisplay.length; i++){   // Iterate through current messages
            let oldPos = textDisplay[i].y;          // Move each message down a little to make space for the new one.
            textDisplay[i].setY(oldPos+30);
        }
        textDisplay.unshift(newText);                // And add the new text to the textDisplay array.
    }    
    
    // A text field for showing high priority messages like victory
    announceText(message){
        centerText.setText(message);
    }

    // This was an early solution for sending messages to the backend. There's a much more focused method of communication in place now, but this is still in use for initializing the combat
    socketData(message) {
        var socket = io(namespace);
        socket.emit('playdata', message);
    }

    queryData(){
        socket.emit('query', "empty");
    }

    // This creates a list of buttons from the abilities available to the character
    buttonListMaker(data){
        let iterator = 0;
        for (let i in data){
            let keyData = {};
            keyData[i] = data[i];
            buttonList[iterator] = keyData;
            iterator += 1;
        }
        // This should make an entirely separate list of values also, in order and formatted for display, to be used by buttonmaker()
        this.buttonMaker();
        
    }

    // This uses the list of buttons from the above method to create interactable buttons.
    buttonMaker(){
        let length = buttonList.length;
        let numberOfRows = Math.ceil(length / 4);
        let lastRow = length % 4;
        for (let i = 0; i < buttonList.length; i++){     // Loop through the saved commands
            let buttonX = (i % 4) * 200;
            let buttonY = ( Math.floor(i / 4) * 45 ) + 525;
            buttons[i] = this.add.sprite(buttonX, buttonY, 'button')
                .setScale(0.8)
                .setOrigin(0)
                .setInteractive();
            let string = Object.keys(buttonList[i])[0];  // Get the key string out
            this.add.text(buttonX, buttonY, string + ": " + buttonList[i][string]);
            buttons[i].on('pointerdown', function(){
                socket.emit('query', string);
            }, this);
        }
    }

    parseSocketData(data){  // A method for parsing and distrubiting data from the frontend
        if (data[0] != undefined)
            if (data[0].max_hp){ // Using the "max hp" key to identify the 'welcome package' containing
                player1 = data[0];  // data about the two combatants.
                player1.hp = player1.max_hp;   // Get an hp total for the UI
                if (player1.ch_class == "inward_fist"){
                    player1.ki = 0;
                }
                this.buttonListMaker(player1.abilities);

                player2 = data[1];
                player2.hp = player2.max_hp;
                if (player2.ch_class == "inward_fist"){
                    player2.ki = 0;
                }

        } else {    // All other data should be bulk data with attacks, so a for loop parses the data
            for (let i in data){  

                if (data[i].method == "victor"){ // I had to run the victory data through the autoattack queue in order to allow the UI a chance to catch up with the server before announcing the victory
                    victor = data[i].name;
                    reward = data[i].extra;
                    conclude = true;
                    setTimeout(function(){
                        scene.announceText(`${victor} wins, ${reward} exp awarded.`);
                    }, 1000);
                    setTimeout(function(){
                        restart = true;
                    }, 1500);
                }
                instructionQueue.push(data[i]);
            }
        }
    }

    // This method goes through the queue and unpacks it to its relevant sections
    queueHandler(){
        scene = this; // Establishing some context
        let intervalTimer = 5000 / instructionQueue.length; // This sets the amount of time each command should take, split up through the whole round.
        let tempQueue = instructionQueue;   // Gather the current queue
        instructionQueue = [];              // And empty it
        for (let i = 0; i < tempQueue.length; i++){ // Iterate through the commands
            setTimeout(function(){                  // Set a timeout
                scene.damageHandler(tempQueue[i].name, tempQueue[i].damage); // damage handler needs the name of the aggressor and the damage amount.
            }, intervalTimer * i);                  // each iteration has its timer multiplied by the number of iterations to evenly spread the commands out and give the illusion of continuous motion
            setTimeout(function(){
                scene.animationHandler(tempQueue[i].name, tempQueue[i].method, tempQueue[i].extra, intervalTimer); // animation handler needs the aggressor's name, the method of attack, and the extra info (For KI)
            }, intervalTimer * i);     
            setTimeout(function(){
                scene.lexicalParser(tempQueue[i].name, tempQueue[i].method, tempQueue[i].damage, tempQueue[i].extra); // The lexical parser needs all of the information
            }, intervalTimer * i); 
        }
    }

    // Damage handler controls the health bar for the player.
    damageHandler(name, damage){
        var stepWidth = (energyMask.displayWidth - 50) / player1.max_hp;  // Figure out how much the bar should move for each point based on the max value
        if (name == player2.name){
            energyMask.x -= damage * stepWidth;             // Move the mask
            player1.hp -= damage;
            let newText = `${player1.hp}/${player1.max_hp}`;
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
            .setScale(2);
        playerTwo = this.add.sprite(425, 400, 'idle')
            .setScale(2)
            .setFlip(true, false);
        playerOne.anims.play({
            key: 'idle',
            repeat: -1,
        });
        playerTwo.anims.play({
            key: 'idle',
            repeat: -1,
        });
        var namespace = "/test"; // Namespace used to identify which user this is
        var socket = io(namespace); // Establish socket variable


// ========================== Input listener ============================
// ===== This little block of code listens for keypresses and then ======
// ===== compares it to the list of user-customized command keys and ====
// ===== list of available abilities. It will emit a command to the =====
// ===== backend when it all matches.                               =====

        this.input.keyboard.on('keydown', function (event) { // Listen for any keypress
            for (let i = 0; i < buttonList.length; i++){     // Loop through the saved commands
                let string = Object.keys(buttonList[i])[0];  // Get the key string out
                if (event.keyCode == eval("Phaser.Input.Keyboard.KeyCodes." + buttonList[i][string]) ){ // Compare the keyCode to the one saved in the character profile
                    socket.emit("query", string); // Then send the command to the backend
                    break; // Break the for loop, because there's no such thing as a double-positive
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
        });

// ===================== Main timer ============================
// ===== This is the main function for controlling the game ====
// ===== temporally. The timing set here in half-second     ====
// ===== increments controls the flow of the game.
        timer = setInterval(function() { // Set the interval to a global variable
            roundTimer += 1;             // Increment to keep track of the rounds
            if (roundTimer == 10){        // When a round is over
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
            if (currentKi != player1.ki){    // If the amount of ki the player has is higher than the amount being displayed
                currentKi = player1.ki;      // Gather the current ki
                kiText.setText(currentKi);      // And display the correct amount
            }
    }
}