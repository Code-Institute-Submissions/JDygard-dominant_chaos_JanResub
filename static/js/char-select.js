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

    /* FIXME 
    
    Capitalize names
    Style that shit up
    
    */

    displayCharacters(data){
        var char = []
        var text = []
        var scene = this
        for (let i = 0; i < data.length; i++){
            console.log(data[i])
            let chname = data[i].name
            text[i] = this.add.text(400, (120 * (i + 1)), data[i].name + ": " + data[i].chclass).setOrigin(0.5).setFontSize(40)
            char[i] = {
                "name": data[i].name,
                "loc": 120 * (i + 1)
            }
        }
        this.input.on('pointerdown', function(pointer){
            for (var i = 0; i < text.length; i++)
                console.log(char[i]["name"]);
                let loc = (char[i]["name"])
                console.log(loc)
                if (pointer.y > loc - 50 && pointer.y < loc + 50){
                    var socket = io(namespace);
                    console.log(char.name)
                    socket.emit('chardata', char[i]["name"]);
                }
        })
    }

    create(){
        let background = this.add.image(0, 0, 'background').setOrigin(0).setScale(0.8)
        this.socketData("requestcharacterlist")
        namespace = '/test';
        var socket = io(namespace);
        var scene = this
        socket.on('response', function(message) {
            var data = JSON.parse(message)
            scene.displayCharacters(data)
            }
        )

    }
    
}