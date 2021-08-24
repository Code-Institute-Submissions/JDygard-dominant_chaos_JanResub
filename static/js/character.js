 function numberShortener(data) {
    let numArray = Array.from(data)
    let display = "";
    if (numArray.length > 3){
        if (numArray.length > 3 && numArray.length < 7) {
            let decimal;
            for (i = 0; i < 3; i++) {
                decimal = numArray.pop();
            }
            for (i = 0; i < numArray.length; i++){
                display = display + numArray[i]
            }
            display = display + "." + decimal + "K";
        }
        else if (numArray.length > 6 && numArray.length < 10) {
            let decimal;
            for (i = 0; i < 6; i++) {
                decimal = numArray.pop();
            }
            for (i = 0; i < numArray.length; i++){
                display = display + numArray[i]
            }
            display = display + "." + decimal + "mil";
        }
        return display;
    } else {
        return data
    }
}
document.getElementById("current-exp-string").innerHTML = numberShortener(document.getElementById("current-exp-string").innerHTML);
document.getElementById("spent-exp-string").innerHTML = numberShortener(document.getElementById("spent-exp-string").innerHTML);
        