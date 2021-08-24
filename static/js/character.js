 // A function for abbreviating large numbers for experience
 function numberShortener(data) { // The data variable is the number in the field
    let numArray = Array.from(data) // Make an array of the digits in the number
    let display = "";   // Make a variable set as an empty string
    if (numArray.length > 3){       // If the number is 4 or more digits
        if (numArray.length > 3 && numArray.length < 7) {   // And between 4-6 digits
            let decimal;                                    // Next three lines knock the last three digits off of the number but save the one closest to the saved numbers
            for (i = 0; i < 3; i++) {
                decimal = numArray.pop();
            }
            for (i = 0; i < numArray.length; i++){          // This loop takes the remaining numbers in the array and builds a string of them.
                display = display + numArray[i]             // For example, 99999 first becomes [9,9] before coming to this loop, and now display = "99"
            }
            display = display + "." + decimal + "K";        // Now we add the decimal and a K to indicate thousands. i.e. 99.9K
        }
        else if (numArray.length > 6 && numArray.length < 10) { // This set of statements does the same thing except for millions.
            let decimal;
            for (i = 0; i < 6; i++) {
                decimal = numArray.pop();
            }
            for (i = 0; i < numArray.length; i++){
                display = display + numArray[i]
            }
            display = display + "." + decimal + "mil";
        }
        return display;                                     // If we've processed anything, it is in the display variable ready to be returned
    } else {
        return data                                         // If the number was too short, just give the data back.
    }
}

let charBio = document.getElementById("char-bio").innerHTML;
if (charBio == ""){
    document.getElementById("char-bio").innerHTML = "A generic adventurer, this character has done stuff and things, but nothing that the user felt like writing about."
}

// These are the two elements on the page that are being parsed like this. They are the experience fields, as they can easily range into the millions.
document.getElementById("current-exp-string").innerHTML = numberShortener(document.getElementById("current-exp-string").innerHTML); 
document.getElementById("spent-exp-string").innerHTML = numberShortener(document.getElementById("spent-exp-string").innerHTML);
        