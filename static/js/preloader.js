class Preloader extends Phaser.Scene{
    constructor() {
        super('Preloader');
    }

    preload(){
        this.load.image('background', ".../assets/images/phaser-assets/background.png")
    }
    create(){
        this.scene.start('CharSelect')
        
    }
}