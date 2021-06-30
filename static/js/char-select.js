class CharSelect extends Phaser.Scene{
    constructor() {
        super('CharSelect');
    }

    preload(){
    }

    showText(message, duration){            // A method for displaying text with the message and duration variables
        if (timer == false){                // Check if there is currently a message being displayed
            timer = true;                   // Show that there is current a message being displayed
            gameText.setText(message);      // Display the message
            this.tweens.add({               // Start a tween
                targets: gameText,          // Targeting the evolve image
                alpha: 1,                   // Go from 0 to 1 alpha
                duration: 600,              // Over 600ms
                yoyo: true,                 // "Yoyo" the message
                hold: duration,             // Hold it on display for the designated time
            });
            let scene = this;               // Maintain context for the timeout function
            setTimeout(() => {              // Make a timeout
                timer = false;              // Show that the message has been cleared from the screen
            }, duration + 1200);            // After the hold duration and both sides of the animation duration
        }
    }

    create(){
        let background = this.add.image(0, 0, 'background')
        let gameText = this.add.text(400, 300, '', {fontFamily: 'sans serif'})        
        gameText                // The text object
            .setScrollFactor(0) // Make the text fixed in the viewport
            .setOrigin(0.5)     // Set the origin in the middle so it displays cleanly
            .setFontSize(40)    // Set the font size to a visible size
            .setColor(0xe60022) // The color for the text
            .setDepth(5)        // Set the depth to 5 so it appears in front of everything
            .setAlpha(0);       // Make it start invisible
    }
}