class Play extends Phaser.Scene {
    constructor() {
        super ("Play")
    }

    preload(){
        
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
        let newText = this.add.text(0,0,message)
        for (let i = 0; i < textDisplay.length; i++){
            let oldPos = textDisplay[i].y;
            textDisplay[i].setY(oldPos+30);
        }
        textDisplay.unshift(newText)
    }    
    
    socketData(message) {
        var socket = io(namespace);
        socket.emit('playdata', message);
    }

    queryData(){
        socket.emit('query', 'empty from JS');
    }

    parseSocketData(data){  
        if (data[0]["max_hp"]){
            player1 = data[0];
            player2 = data[1];
        } else {
            console.log("data pushed to queue:")
            console.log(data)
            for (let i in data){
                instructionQueue.push(data[i]);
            }
        }
    }

    queueHandler(){
        scene = this
        let intervalTimer = 3000 / instructionQueue.length;
        let tempQueue = instructionQueue;
        console.log("Temp queue:")
        console.log(tempQueue)
        console.log("----------")
        instructionQueue = [];
        console.log("Emptied queue:")
        console.log(instructionQueue)
        console.log("--------------")
        for (let i = 0; i < tempQueue.length; i++){
            setTimeout(function(){                                                          // Wait for a moment
                scene.damageHandler(tempQueue[i]["name"], tempQueue[i]["damage"]);                                                           // before removing the tint
            }, intervalTimer * i);    
            setTimeout(function(){                                                          // Wait for a moment
                scene.animationHandler(tempQueue[i]["name"], tempQueue[i]["method"]);                                                           // before removing the tint
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

    }

    animationHandler(name, method){

    }

    create(){
        /*
        Healthbar mask system from evo.
        let energyBar = this.add.sprite(207, 90, 'energybar')   // Make an energy bar
            .setDepth(6)                                        // Set the depth so it appears on top of everything
            .setScrollFactor(0)                                 // Fix it in viewport
            .setScale(1.5);                                     // Make it a little bigger :)
        energyMask = this.add.sprite(207, 90, 'energybar')      // Make a mask to hide some of the bar when the health is below max
            .setDepth(6)                                        // Set the depth so it appears on top of everything                                    
            .setScrollFactor(0)                                 // Fix it in viewport
            .setScale(1.5);                                     // Make it a little bigger :)
        energyMask.visible = false;                             // Make it invisble
        energyBar.mask = new Phaser.Display.Masks.BitmapMask(this, energyMask); // Make the mask act like a mask

        if (playerHP >= 1){                                     // If the player has hp left
            stepWidth = energyMask.displayWidth / playerMaxHP;  // Figure out how much the bar should move for each point based on the max value
            if (playerHP !== referenceHP){                      // If the hp has changed since last update
                let lostHP = referenceHP - playerHP;            // Figure out how much it has changed
                referenceHP = playerHP;                         // Reset the expected hp
                energyMask.x -= lostHP * stepWidth;             // Move the mask
            }
        */
        var scene = this; // Establish context
        let background = this.add.image(0, 0, 'background').setOrigin(0).setScale(0.8); // Show and orient the background image
        var namespace = "/test"; // Namespace used to identify which user this is
        var socket = io(namespace); // Establish socket variable

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
                console.log("queuehandler fires")
                scene.queueHandler();
                roundTimer = 0;
            }
            if (conclude == true){
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