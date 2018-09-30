var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');
var imageObj = new Image();
var final_image;

imageObj.onload = start;
imageObj.src = '/static/images/arterias.jpg';

function start() {
  ctx.drawImage(imageObj, 0, 0, myCanvas.width, myCanvas.height);
  canvas.onmousemove = lines();
  // document.getElementById("image_data").value = canvas.toDataURL("image/png", 1);
};

function lines() {

    //Initialize mouse coordinates to 0,0
    var mouse = { x: 0, y: 0};

    //Paint includes line width, line cap, and color
    paint = function() {
        ctx.lineTo(mouse.x, mouse.y);
        ctx.lineWidth = lineWidthRange();
        ctx.lineJoin = 'round';
        ctx.lineCap = 'round';
        ctx.strokeStyle = 'red';
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

//Change line width
function lineWidthRange() {
    var widthLine = document.getElementById("myRange").value;
    return widthLine;
};

//Clear canvas
function erase() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(imageObj, 0, 0, myCanvas.width, myCanvas.height);

};

function saveImage() {
    final_image = canvas.toDataURL('image/png',1);
    document.getElementById('image_data').value=final_image;
//   var final_image = new Image();
//   final_image.src = canvas.toDataURL('image/png', 1)
 }







