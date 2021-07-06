class Play extends Phaser.Scene {
    constructor() {
        super ("Play")
    }

    preload(){
        
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

    create(){
        let background = this.add.image(0, 0, 'background').setOrigin(0).setScale(0.8); // Show and orient the background image
        this.socketData("play init")
        var namespace = "/test"
        var socket = io(namespace);
        var scene = this;
        socket.on('reply', function(message) {
            console.log(message)
            console.log("tick")
            for (let i = 0; i < message.length; i++) {
                //let newText = scene.add.text(0,0,message.method + ' (' + message.damage + ")")
                scene.displayText(message[i]["method"] + ' (' + message[i]["damage"] + ")")
            }
            socket.emit('query', '');
            /*
            for (let i = 0; i < textDisplay.length; i++){
                let oldPos = textDisplay[i].y;
                textDisplay[i].setY(oldPos+30);
            }
            textDisplay.unshift(newText)
            }
        )*/
        })
        this.queryData()
    }

    
    /*

    Maybe the character collector should be in here, fed by the select screen.

    Set up a message log system.

    set up communication with Flask.

    Put in our placeholder graphics.
    This should have its own preloader because ventually I should be feeding in commands on what graphics to load.

    Set up the fight.

    Figure out how to get the animations to trigger from socket commands.


    */
}