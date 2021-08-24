function calculateCost(number, iterations) {
    let initialValue = parseInt(number) + 1;
    let result = 0;
    for (let i = 0; i < iterations; i++) {
        result += Math.sqrt(initialValue) * 1500;
        initialValue++;
    }
    return Math.round(result);
}

if (discipline < 10) {
    document.getElementById("discipline-cost").innerHTML = (discipline + 1) * 500000
} else {
    document.getElementById("disc-card-action").innerHTML = "You have reached max discipline"
}
//                                     Body Training Card Generator 
//                                   ===============================
// This is here to build the four training card tabs in the bodytraining frame. The two arrays contain the variables/strings.
// This is needed to display experience cost per point, how many points they would like to train, and the total experience cost.
// It is also what provides the number in the field read by Flask. The backend verifies whatever information is submitted to prevent
// any bad faith POST attempts.

bodyTraining = [torso, hands, arms, legs];      // Tied to the variables declared above, taken directly from the DB
bodyString = ["torso", "hands", "arms", "legs"] // contains strings for navigating the DOM and buildings other strings
for (let i = 0; i < bodyTraining.length; i++) { // A for loop for going through the arrays
    if (bodyTraining[i] >= 100) {               // If the body training is already at maximum, we tell the user and lock out the training
        document.getElementById("action-" + bodyString[i]).innerHTML = "<h3> Your " + bodyString[i] + " are trained to maximum </h3>" // The message
    } else {                                                                                                                            // Otherwise
    document.getElementById("cost-" + bodyString[i]).innerHTML = calculateCost(bodyTraining[i], 1)                                      // Set the cost field for the cost of the next point
    document.getElementById("train-" + bodyString[i]).addEventListener("click", function(){                                             // And listen for the click
        if (parseInt(bodyTraining[i]) + parseInt(document.getElementById("field-" + bodyString[i]).innerHTML) >= 100) {                 // Determine if the amount they are training would push them above maximum
            document.getElementById("max-" + bodyString[i]).innerHTML = " Maximum level reached."                                       // And prevent them from further queuing trainings
        } else{
            let current = parseInt(document.getElementById("field-" + bodyString[i]).innerHTML);  // This is the field that is read by Flask. It also displays how many points the player wants to train at a time
            document.getElementById("field-" + bodyString[i]).innerHTML = parseInt(current) + 1;  // The field from a line above
            document.getElementById("flask-" + bodyString[i]).value = parseInt(current) + 1;
            let next = calculateCost(parseInt(bodyTraining[i]) + current + 1, 1);                                             // Adjust the cost field on click
            document.getElementById("cost-" + bodyString[i]).innerHTML = next;                    // the field for the cost
            let totalExperience = calculateCost(bodyTraining[i], current + 1);                    // Calculate how much the entire batch of points would cost
            document.getElementById("total-" + bodyString[i]).innerHTML = totalExperience;        // And display to the user
        }
        })
    }
}
//                                  Move Active
//                                 =============
// This function responds to clicks on each of the tabs. It first hides the current tab, then
//              displays the chosen tab. It also cycles the pictures.

function moveActive() {
    parent = event.target.parentNode.parentNode.firstElementChild;
    while (parent){
        if (parent.className == "active") {
            parent.className = "waves-effect"
            let childText = parent.firstElementChild.innerHTML.toLowerCase()
            let hideIt = document.getElementsByClassName(childText)
            let hideItToo = document.getElementsByClassName(childText + "-image")
            hideIt[0].style.display = "none"
            hideItToo[0].style.display = "none"
        } else {
            parent = parent.nextElementSibling
        }
    }
    
    if (event.target.parentNode.className !== "active") {
        event.target.parentNode.className = "active"
        let childText = event.target.innerHTML.toLowerCase() 
        let showIt = document.getElementsByClassName(childText)
        let showItToo = document.getElementsByClassName(childText + "-image")
        showItToo[0].style.display = "block"
        showItToo[0].style.height = "100%"
        showItToo[0].style.width = "100%"
        showItToo[0].style["object-fit"] = "cover"
        showIt[0].style.display = "block"
    }
}

//                      Icon Selection

namespace = '/test';
var socket = io(namespace)
$(document).ready(function() {
    namespace = '/test';
    var socket = io(namespace);

    socket.on('connect', function() {
        socket.emit('character', "character connected");
    });
});

let iconMenu = document.getElementById("hidden-menu")
let newIcon = document.getElementById("new-icon")
let hideSelection = document.getElementById("hide-selection")

hideSelection.onclick = function () {
    iconMenu.style.visibility = "hidden"
}

newIcon.onclick = function (){
    iconMenu.style.visibility = "visible"
}

let icons = document.getElementById("icon-selection").children
let currentIcon = document.getElementById("current-icon")
for (let i = 0; i < icons.length; i++) {
    icons[i].style.cursor = "pointer";
    icons[i].onclick = function (){
        iconMenu.style.visibility = "hidden"
        submit = [icons[i].getAttribute("src"), "{{ charactername.name }}"];
        currentIcon.src = submit[0];
        socket.emit('character', submit);
    }
}

let deleteBtn = document.getElementById("delete-char-btn");
let deleteChar = document.getElementById("delete-char-row");
var height = 0;
var interval;

function frame() {
    if (height >= 185) {
        clearInterval(interval)
    } else if (height <= 20 || height >= 165) {
        height += 0.5;
        deleteChar.style.height = height + 'px';
        window.scrollBy(0,1);
    } else if (height <= 165){
        height++;
        deleteChar.style.height = height + 'px';
        window.scrollBy(0,1);
    }
}

deleteBtn.onclick = function (){
    deleteBtn.style.display = "none";
    deleteChar.style.display = "block";
    interval = setInterval(frame, 5);
}
