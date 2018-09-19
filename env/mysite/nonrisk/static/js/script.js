//Create canvas
var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');

//Set background
ctx.fillStyle = "white";
ctx.fillRect(0, 0, 700, 500);

//Lines is default
lines();

var removeRectangleInLine = 0;

function lines() {
    //painting = false;
    //Remove event listeners so line won't draw rectangle
    if (removeRectangleInLine == 1) {
        canvas.removeEventListener('mousedown', rectMouseDown);
        canvas.removeEventListener('mouseup', rectMouseUp);
        canvas.removeEventListener('mousemove', rectMouseMove);
        canvas.removeEventListener('mouseout', rectMouseout);
    };

    //Initialize mouse coordinates to 0,0
    var mouse = { x: 0, y: 0};

    //Paint includes line width, line cap, and color
    paint = function() {
        ctx.lineTo(mouse.x, mouse.y);
        ctx.lineWidth = lineWidthRange();
        ctx.lineJoin = 'round';
        ctx.lineCap = brushstyle;
        ctx.strokeStyle = colors;
        ctx.stroke();
    };

    //Find mouse coordinates relative to canvas
    linesMousemove = function(e){
        mouse.x = e.pageX - this.offsetLeft;
        mouse.y = e.pageY - this.offsetTop;
    };

    //User clicks down on canvas to trigger paint
    linesMousedown = function(){
        ctx.beginPath();
        ctx.moveTo(mouse.x, mouse.y);
        canvas.addEventListener('mousemove', paint, false);
    };

    //When mouse lifts up, line stops painting
    linesMouseup = function(){
        canvas.removeEventListener('mousemove', paint, false);
    };

    //When mouse leaves canvas, line stops painting
    linesMouseout = function() {
        canvas.removeEventListener('mousemove', paint, false);
    };

    //Event listeners that will trigger the paint functions when
    //mousedown, mousemove, mouseup, mouseout
    canvas.addEventListener('mousedown', linesMousedown, false);
    canvas.addEventListener('mousemove', linesMousemove, false);
    canvas.addEventListener('mouseup', linesMouseup, false);
    canvas.addEventListener('mouseout', linesMouseout, false);

};

//Color palette
var colors = "red";

//Change brush style
var brushstyle = "round";

//Change line width
function lineWidthRange() {
    var widthLine = document.getElementById("myRange").value;
    return widthLine;
};

//Clear canvas
function erase() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
};

//Save image
var button = document.getElementById('dwnld');
button.addEventListener('click', function (e) {
var dataURL = canvas.toDataURL('image/png');
button.href = dataURL;

});



