class Preloader extends Phaser.Scene{
    constructor() {
        super('Preloader');
    }

    preload(){
        this.load.image('background', "https://chaos-legacy-imgserve.s3.eu-north-1.amazonaws.com/backround.png")
        this.load.image('energybar', "https://chaos-legacy-imgserve.s3.eu-north-1.amazonaws.com/energybar.png")
        this.load.image('emptybar', "https://chaos-legacy-imgserve.s3.eu-north-1.amazonaws.com/EmptyBar.png")
        this.load.spritesheet(                                      // Load the spritesheet into the texture manager
            "spritesheet",                            // This is master player spritesheet, with 3 animations at 4 frames per
            "https://chaos-legacy-imgserve.s3.eu-north-1.amazonaws.com/animation-126x126.png",  // Load from assets directories
            {
                frameWidth: 126,                                    // Defining the size of the individual frames in
                frameHeight: 126                                    // the spritesheet.
            }
        );
    }
    create(){
        this.scene.start('CharSelect')

    }
}