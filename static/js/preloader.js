class Preloader extends Phaser.Scene{
    constructor() {
        super('Preloader');
    }

    preload(){
        this.load.image('background', "https://chaos-legacy-imgserve.s3.eu-north-1.amazonaws.com/backround.png")
    }
    create(){
        this.scene.start('CharSelect')

    }
}