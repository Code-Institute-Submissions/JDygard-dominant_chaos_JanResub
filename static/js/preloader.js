class Preloader extends Phaser.Scene{
    constructor() {
        super('Preloader');
    }

    preload(){
        this.load.image('background', "https://chaos-legacy-imgserve.s3.eu-north-1.amazonaws.com/backround.png")
        this.load.image('energybar', "https://chaos-legacy-imgserve.s3.eu-north-1.amazonaws.com/energybar.png")
        this.load.image('emptybar', "https://chaos-legacy-imgserve.s3.eu-north-1.amazonaws.com/EmptyBar.png")
    }
    create(){
        this.scene.start('CharSelect')

    }
}