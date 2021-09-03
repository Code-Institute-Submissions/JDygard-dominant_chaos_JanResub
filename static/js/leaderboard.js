namespace = '/test';
var socket = io(namespace);
let tableRows = document.getElementsByClassName("table-row"); // Get the table rows
if (tableRows.length < 11) { // If there aren't any rows after the top ten
    document.getElementById("table-extension").innerHTML = ""; // Then remove the html for the extension table
}
for (let i = 0; i < tableRows.length; i++) {
    tableRows[i].style.cursor = "pointer"; // Give all the rows a special pointer
    tableRows[i].onclick = function (){
        socket.emit('leaderboard', tableRows[i].childNodes[5].innerHTML); // And emit a signal to the backend when a row is clicked on
    };
}

// Socket definition and function

$(document).ready(function() {

    namespace = '/test';
    var socket = io(namespace);

    socket.on('connect', function() {
        socket.emit('leaderboard', "leaderboard connected");
    });
});
socket.on("redirect", function(x) {
    window.location.href = x;
    });