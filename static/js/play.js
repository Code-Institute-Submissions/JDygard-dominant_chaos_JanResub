class Play extends Phaser.Scene {
    constructor() {
        super ("Play")
    }

    preload(){
        this.anims.create({                                                 // Creating our water animation
            key: "punch1",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 0, end: 1 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our water animation
            key: "punch2",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 8, end: 9 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our water animation
            key: "kick",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 32, end: 35 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our water animation
            key: "idle",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 24, end: 25 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our water animation
            key: "dodge",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 40, end: 41 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our water animation
            key: "block",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 48, end: 49 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our water animation
            key: "parry",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 16, end: 17 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our water animation
            key: "shinkick",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 12, end: 13 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our water animation
            key: "jab",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 0, end: 1 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our water animation
            key: "spinkick",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 56, end: 57 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our water animation
            key: "knee",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 4, end: 5 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our water animation
            key: "elbow",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 20, end: 21 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
        this.anims.create({                                                 // Creating our water animation
            key: "uppercut",                                          // Declaring the key to which it will be referred
            frames: this.anims.generateFrameNumbers("spritesheet", { start: 28, end: 29 }), // Getting the spritesheet and numbering the frames for the array
            frameRate: 3,                                                   // Speed at which the frames are cycled
        });
    }

    lexicalParser(name, method, damage, extra){
        let verb;
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

    parseSocketData(data){  // A method for parsing and distrubiting data from the frontend
        if (data[0]["max_hp"]){ // Using the "max hp" key to identify the 'welcome package' containing
            player1 = data[0];  // data about the two combatants.
            player1["hp"] = player1["max_hp"]   // Get an hp total for the UI
            if (player1["ch_class"] == "inward_fist")
                player1["ki"] = 0
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
        let intervalTimer = 3000 / instructionQueue.length;
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

    animationHandler(name, method, extra, duration){
        let aggressor;
        let defender;
        if (player1["name"] == name){
            aggressor = playerOne
            defender = playerTwo
        } else {
            aggressor = playerTwo
            defender = playerOne
        }

        if (method == "kick"){
            aggressor.anims.play({
                key: 'kick',
                repeat: 1,
                duration: duration
            });
        }
        console.log(aggressor["ch_class"])
        if (aggressor["ch_class"] == "inward_fist"){
            console.log("checking fist animations")
            let methods = ["shinkick", "jab", "spinkick", "knee", "elbow", "uppercut"];
            let aggressorKi = aggressor["ki"];
            for (i in methods){
                if (method == i){
                    aggressor.anims.play({
                        key: i,
                        repeat: 1,
                        duration: duration
                    });
                    aggressor["ki"] = aggressorKi + extra;
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

        let background = this.add.image(0, 0, 'background').setOrigin(0).setScale(0.8); // Show and orient the background image
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
        
        // I'm putting a bunch of variables here that could later be converted to be customizable for the user.
        var kick = Phaser.Input.Keyboard.KeyCodes.A
        var shinkick = Phaser.Input.Keyboard.KeyCodes.ONE
        var jab = Phaser.Input.Keyboard.KeyCodes.TWO
        var spinkick = Phaser.Input.Keyboard.KeyCodes.THREE
        var knee = Phaser.Input.Keyboard.KeyCodes.FOUR
        var elbow = Phaser.Input.Keyboard.KeyCodes.FIVE
        var uppercut = Phaser.Input.Keyboard.KeyCodes.SIX

        this.input.keyboard.on('keydown', function (event) {

            if (event.keyCode === kick)
            {
                socket.emit("query", "kick");
            }

            if (event.keyCode === shinkick)
            {
                socket.emit("query", "shinkick");
            }
    

            if (event.keyCode === jab)
            {
                socket.emit("query", "jab");
            }
    

            if (event.keyCode === spinkick)
            {
                socket.emit("query", "spinkick");
            }
    

            if (event.keyCode === knee)
            {
                socket.emit("query", "knee");
            }
    

            if (event.keyCode === elbow)
            {
                socket.emit("query", "elbow");
            }
    

            if (event.keyCode === uppercut)
            {
                socket.emit("query", "uppercut");
                console.log("uppercut")
            }
    
    
        });


        socket.on('query', function(message) { // Listen for incoming data
            if (message == "conclude") { // If the script says someone won
                conclude = true;         // Set the fight to end
            }
            else if (message !== "empty"){ // Otherwise, we know it's data
                scene.parseSocketData(message);  // So pass it to the data handler
            }
        })

        timer = setInterval(function() {
            roundTimer += 1;
            if (roundTimer == 6){
                scene.queueHandler();
                roundTimer = 0;
            }
            if (conclude == true){
                scene.queueHandler();
                clearInterval(timer);
            }
            socket.emit("query", 'empty');
        },500);

        this.socketData("play init");
    }
    
    /*

    Put in our placeholder graphics.
    This should have its own preloader because ventually I should be feeding in commands on what graphics to load.

    Set up the fight.

    Figure out how to get the animations to trigger from socket commands.

    */
}