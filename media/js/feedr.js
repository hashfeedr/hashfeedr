var width,height,c;

var framedelay=66;

var scene=[];
var transitions=[];

var campos=[0,0];
var camrot=0.0;

function catmullrom(t,x0,x1,x2,x3){
	var t2=t*t,t3=t2*t;
	return 0.5*((2*x1)+(-x0+x2)*t+(2*x0-5*x1+4*x2-x3)*t2+(-x0+3*x1-3*x2+x3)*t3);
}

function lerp(t,a,b) {
	return a+(b-a)*t;
}

/* easing stuff */
function easeinout(t) {
	return -0.5*(Math.cos(Math.PI*t)-1);
}

/** @constructor */
function Property(value) {
	this.length=value.length;
	this.value=value;
}

/** @constructor */
function Transition(property,start,end,duration) {
	this.start=start;
	this.end=end;
	this.property=property;
	this.time=0.0;
	this.step=1.0/duration;
	transitions.push(this);

	this.update=function() {
		this.time+=this.step;
		if (this.time>1.0) {
			this.property.value=this.end;
			return false;
		}
		for (var i=0;i<this.property.length;++i) {
			this.property.value[i]=lerp(easeinout(this.time),this.start[i],this.end[i]);
		}
		return true;
	}
}

/** @constructor */
function Tweet() {
	this.position=new Property([100,10]);
	this.draw=function() {
		c.shadowColor="rgba(0,0,0,0.4)";
		c.shadowOffsetX=2;
		c.shadowOffsetY=2;
		c.shadowBlur=4;
		c.fillStyle="#f0f";
		c.fillRect(this.position.value[0],this.position.value[1],20,20);
	};
}

function resizecanvas() {
	width=c.canvas.clientWidth;
	height=c.canvas.clientHeight;
	c.canvas.width=width;
	c.canvas.height=height;
}

function update() {
	for (var t=0;t<transitions.length;++t) {
		if (transitions[t].update()===false) {
			transitions.splice(t--,1);
		}
	}
	return true;
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
	new Transition(tweet.position,[0,0],[50,70],10);

//	draw(); // DEBUG

	setInterval(function(){
		if (update()) draw();
	},framedelay);
});

