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
        socket.emit('query', 'empty from JS');
    }

    parseSocketData(data){  
        if (data[0]["max_hp"]){
            player1 = data[0];
            player1["hp"] = player1["max_hp"]
            player2 = data[1];
            player2["hp"] = player2["max_hp"]
        
        } else {
            console.log("data pushed to queue:")
            console.log(data)
            for (let i in data){
                if (data[i]["method"] == "victor"){
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
        var stepWidth = (energyMask.displayWidth - 50) / player1["max_hp"];  // Figure out how much the bar should move for each point based on the max value
        if (name == player2["name"]){
            energyMask.x -= damage * stepWidth;             // Move the mask
            player1["hp"] -= damage
            let newText = `${player1["hp"]}/${player1["max_hp"]}`
            hpText.setText(newText); 
        }
    }

    animationHandler(name, method){

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