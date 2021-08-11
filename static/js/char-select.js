class CharSelect extends Phaser.Scene{
    constructor() {
        super('CharSelect');
    }

    preload(){
    }

    socketData(message) {
        var socket = io(namespace);
        socket.on('connect', function() {
            socket.emit('message', message);
        });
    }

    displayCharacters(data){
        for (let i = 0; i < data.length; i++){
            text[i] = this.add.text(400, (120 * (i + 1)), data[i].name + ": " + data[i].chclass).setOrigin(0.5).setFontSize(40)
            char[i] = {
                "name": data[i].name,
                "loc": 120 * (i + 1)
            }
        }
        this.input.on('pointerdown', function(pointer){
            for (var i = 0; i < text.length; i++){
                let loc = (char[i]["loc"])
                if (pointer.y > loc - 50 && pointer.y < loc + 50){
                    var socket = io(namespace);
                    socket.emit('chardata', char[i]["name"]);
                }
            }
        })
    }

    create(){
        var scene = this
        this.socketData("requestcharacterlist")
        var namespace = '/test';
        var socket = io(namespace);
        socket.on('response', function(message) {
            var data = JSON.parse(message)
            scene.displayCharacters(data)
            }
        )
        socket.on('character', function(data){
            if (data == "prepared"){
                scene.scene.start('Play')
            }
        })

    }
    
}