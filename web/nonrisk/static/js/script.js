var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');
var imageObj = new Image();
var layer = new Image();
var final_image;

imageObj.onload = start;
layer.onload = start;
imageObj.src = '/static/images/arteries.png';
layer.src = '/static/images/layer.png';

function start() {
  ctx.drawImage(imageObj, 0, 0, myCanvas.width, myCanvas.height);
  canvas.onmousemove = lines('Done');
};

function lines(id) {
    var x = document.getElementById(id);
    //Initialize mouse coordinates to 0,0
    var mouse = { x: 0, y: 0};

    //Paint includes line width, line cap, and color
    paint = function() {
        ctx.lineTo(mouse.x, mouse.y);
        ctx.lineWidth = lineWidthRange();
        ctx.lineJoin = 'round';
        ctx.lineCap = 'round';
        ctx.strokeStyle = 'yellow';
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
        //uncheck 'Done'
        x.checked = false;
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
function erase(id) {
    var x = document.getElementById(id);
    x.checked = false;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(imageObj, 0, 0, myCanvas.width, myCanvas.height);

};

function saveImage() {
    ctx.drawImage(layer, 0, 0, myCanvas.width, myCanvas.height);
    ctx.closePath();
    ctx.beginPath();

    ctx.font = "16px Arial";
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 2;
    
    areaderecha = document.getElementById("areaderecha").value;
    areaizquierda = document.getElementById("areaizquierda").value;
    areatotal = Number(areaderecha) + Number(areaizquierda);
    
    areaderecha = areaderecha.toString();
    areaizquierda = areaizquierda.toString();
    areatotal = areatotal.toString();

    ctx.globalAlpha = 0.5;
    if (areaderecha > 0){
        ctx.rect(500, 440, 200, 60); //right
    }
    if (areaizquierda > 0){
        ctx.rect(5, 440, 200, 60); //left
    }
    ctx.fillStyle = "white";
    ctx.fill();
    ctx.globalAlpha = 1.0;

    ctx.fillStyle = "black";
    if (areaizquierda>0){
        ctx.fillText("Área de placa Izquierda:", 15, 465);
        ctx.fillText( areaizquierda +'(mm²)', 65, 485);
        ctx.fillText( '___________', 35, 487);
    }

    if(areaderecha>0){
        ctx.fillText("Área de placa Derecha:", 510, 465);
        ctx.fillText(areaderecha +'(mm²)', 555, 485);
        ctx.fillText( '___________', 535, 487);
    }
    ctx.stroke();

    ctx.font = "bold 18px Arial";
    if(areaizquierda>0 || areaderecha>0){
        ctx.fillText("Área de placa", 470, 25);
        ctx.fillText("total: "+ areatotal+ "(mm²)" , 470, 45);
        ctx.stroke();

        ctx.font = "10px Arial";
        ctx.fillText("_____________________" , 465, 47);
    }




    
    final_image = canvas.toDataURL('image/png',1);
    document.getElementById('image_data').value=final_image;
 }







