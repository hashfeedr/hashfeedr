var width,height,c;

var framedelay=66;

var scene=[];

/** @constructor */
function Tweet() {
	this.draw=function() {
		c.fillStyle="#f0f";
		c.fillRect(50,50,20,20);
	};
}

function resizecanvas() {
	width=c.canvas.clientWidth;
	height=c.canvas.clientHeight;
	c.canvas.width=width;
	c.canvas.height=height;
}

function update() {
	return false;
}

function draw() {
	c.clearRect(0,0,width,height);
	c.fillStyle="#f00";
	c.fillRect(10,10,100,100);
	for (var e in scene) {
		c.save();
		scene[e].draw();
		c.restore();
	}
}

$(function(){
	c=$("#thecanvas").get(0).getContext("2d");

	resizecanvas();
	$(window).resize(resizecanvas);

	tweet=new Tweet();
	scene.push(tweet);

	draw(); // DEBUG

	setInterval(function(){
		if (update()) draw();
	},framedelay);
});

