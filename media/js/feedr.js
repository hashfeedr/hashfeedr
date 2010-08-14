var width,height,c;

var framedelay=66;

var scene=[];
var transitions=[];

var campos=[0,0];
var camrot=0.0;

function catmullrom(t,x0,x1,x2,x3){
	var t2=t*t,t3=t2*t;
	return 0.5*((2.0*x1)+(-x0+x2)*t+(2.0*x0-5.0*x1+4.0*x2-x3)*t2+(-x0+3.0*x1-3.0*x2+x3)*t3);
}

function lerp(t,a,b) {
	return a+(b-a)*t;
}

/** @constructor */
function Camera() {
	this.position=new Property([0.0,0.0,0.0]); // x,y,angle
	
	this.activate=function() {
		c.translate(this.position.value[0],this.position.value[1]);
		c.rotate(this.position.value[2]);
	}
}
var cam=new Camera();

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

/** @constructor */
function GrowArrow(p0,p1,p2,p3) {
	this.p0=new Property(p0);
	this.p1=new Property(p1);
	this.p2=new Property(p2);
	this.p3=new Property(p3);
	this.steps=new Property([0]);
	new Transition(this.steps,[0],[25],20);
	this.maxsteps=25.0;
	this.increment=1.0/this.maxsteps;

	this.draw=function() {
		c.strokeStyle="#000";
		c.lineWidth=10;
		c.shadowBlur=40;
		c.shadowColor="#f00";
		c.beginPath();
		for (var i=0;i<this.steps.value[0];++i) {
			var t=i*this.increment;
			c.lineTo(catmullrom(t,this.p0.value[0],this.p1.value[0],this.p2.value[0],this.p3.value[0]),catmullrom(t,this.p0.value[1],this.p1.value[1],this.p2.value[1],this.p3.value[1]));
		}
		c.stroke();
	}
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
	return transitions.length>0?true:false;
}

function draw() {
	c.clearRect(0,0,width,height);
	c.save();
//	cam.activate();
	c.beginPath();
	c.stokeStyle="#0f0";
	c.lineTo(200,200);
	c.lineTo(200,300);
	c.stroke();
	c.fillStyle="#f00";
	c.fillRect(10,10,100,100);
	for (var e in scene) {
		c.save();
		scene[e].draw();
		c.restore();
	}
	c.restore();
}

$(function(){
	c=$("#thecanvas").get(0).getContext("2d");

	resizecanvas();
	$(window).resize(resizecanvas);

	tweet=new Tweet();
	scene.push(tweet);
	scene.push(new GrowArrow([-100.0,10.0],[100.0,100.0],[400.0,400.0],[500.0,300.0]));
	new Transition(tweet.position,[0,0],[50,70],10.0);
	new Transition(cam.position,[0.0,20.0,0.0],[200.0,0.0,1.0],100.0);

	setInterval(function(){
		if (update()) draw();
	},framedelay);
});

