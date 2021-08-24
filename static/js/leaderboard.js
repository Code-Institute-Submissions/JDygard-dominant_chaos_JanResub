namespace = '/test';
var socket = io(namespace);
let tableRows = document.getElementsByClassName("table-row")
if (tableRows.length < 11) {
    document.getElementById("table-extension").innerHTML = ""
}
for (let i = 0; i < tableRows.length; i++) {
    tableRows[i].style.cursor = "pointer";
    tableRows[i].onclick = function (){
        socket.emit('leaderboard', tableRows[i].childNodes[5].innerHTML);
    }
}

$(document).ready(function() {

    namespace = '/test';
    var socket = io(namespace);

    socket.on('connect', function() {
        socket.emit('leaderboard', "leaderboard connected");
    });
});
socket.on("redirect", function(x) {
    window.location.href = x;
    })