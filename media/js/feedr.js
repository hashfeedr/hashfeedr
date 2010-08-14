var width,height,c;

var framedelay=66;

var scene=[];
var transitions=[];
var tweets=[];

var placementx=100.0;

var campos=[0,0];
var camrot=0.0;

var backdrop=new Image();
backdrop.src="/media/images/feedbackdrop.jpg";

function catmullrom(t,x0,x1,x2,x3){
	var t2=t*t,t3=t2*t;
	return 0.5*((2.0*x1)+(-x0+x2)*t+(2.0*x0-5.0*x1+4.0*x2-x3)*t2+(-x0+3.0*x1-3.0*x2+x3)*t3);
}

function lerp(t,a,b) {
	return a+(b-a)*t;
}

function placement(x) {
	var t=x*0.001;
	return (Math.sin(t)+Math.sin(2.232*t)+Math.sin(9.876*t)+Math.sin(8.888*t))*50.0+100.0;
}

function boxintersect(x1,y1,w1,h1,x2,y2,w2,h2) {
	return (x1 <= x2+w2 &&
          x2 <= x1+w1 &&
          y1 <= y2+h2 &&
          y2 <= y1+h1);
return !(x2 > x1+w1 || 
		x2+w2 < x1 || 
		y2 > y1+h1 ||
		y2+h2 < y1);
}

function findnewpos(tw) {
	var found=false,x=0,y=0;
	var w=tw.width;
	var h=tw.height;
	while (!found) {
		found=true;
		placementx+=1.0;
		x=placementx-tw.width*0.5;
		y=placement(placementx)-tw.height*0.5;
		for (var i=0;i<tweets.length;++i) {
			if (boxintersect(x,y,w,h,tweets[i].position.value[0],tweets[i].position.value[1],tweets[i].width,tweets[i].height)) {
				found=false;
				break;
			}
		}
	}
	tw.position.value=[x,y];
}

function textmetrics(fsize,s) {
	var lines=s.split("\n");
	var w=0,h=0;
	for (var i in lines) {
		w=Math.max(c.measureText(lines[i]).width,w);
		h+=fsize;
	}
	return [w,h];
}

function filltext(fsize,s,x,y) {
	var lines=s.split("\n");
	var h=0;
	for (var i in lines) {
		c.fillText(lines[i],x,y+h);
		h+=fsize;
	}
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
function Tweet(data) {
	this.position=new Property([100,10]);

	this.message=data;
		
	c.font="50px Gesta-1";
	var exts=textmetrics(50,this.message);
	this.width=exts[0];
	this.height=exts[1];
	findnewpos(this);
	tweets.push(this);
	
	this.draw=function() {
		c.shadowColor="rgba(0,0,0,0.4)";
		c.shadowOffsetX=2;
		c.shadowOffsetY=2;
		c.shadowBlur=4;
//		c.fillStyle="#f0f";
//		c.fillRect(this.position.value[0],this.position.value[1],20,20);

		c.font="50px Gesta-1";
		c.fillStyle="#f0f";
		c.fillRect(this.position.value[0],this.position.value[1],this.width,this.height);
		c.fillStyle="#000";
		filltext(50,this.message,this.position.value[0],this.position.value[1]);
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
			c.lineTo(catmullrom(t,this.p0.value[0],this.p1.value[0],this.p2.value[0],this.p3.value[0]),
			         catmullrom(t,this.p0.value[1],this.p1.value[1],this.p2.value[1],this.p3.value[1]));
		}
		c.stroke();
	}
}

function resizecanvas() {
	width=c.canvas.clientWidth;
	height=c.canvas.clientHeight;
	c.canvas.width=width;
	c.canvas.height=height;
	c.textBaseline="top";
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
	c.drawImage(backdrop,0,0,width,height);
	c.save();
	cam.activate();
	c.strokeStyle="#fff";
	c.beginPath();
	for (var i=0;i<1000.0;i+=1) {
		c.lineTo(i,placement(i));
	}
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


	scene.push(new Tweet("foo"));
	scene.push(new Tweet("bar"));
	scene.push(new Tweet("justin bieber"));
	scene.push(new Tweet("foo"));
	scene.push(new Tweet("bar"));
	scene.push(new Tweet("justin bieber"));
	scene.push(new Tweet("foo"));
	scene.push(new Tweet("bar"));
	scene.push(new Tweet("justin bieber"));
	scene.push(new Tweet("foo"));
	scene.push(new Tweet("bar"));
	scene.push(new Tweet("justin bieber"));
	scene.push(new GrowArrow([-100.0,10.0],[100.0,100.0],[400.0,400.0],[500.0,300.0]));
//	new Transition(tweet.position,[0,0],[50,70],10.0);
//	new Transition(cam.position,[0.0,20.0,0.0],[200.0,0.0,1.0],100.0);

	setInterval(function(){
		if (update()) draw();
	},framedelay);
      
//	var ws = new WebSocket("ws://hashfeedr.com:8338/websession");
//		ws.onmessage = function(e) {
//		scene.push(new Tweet(e.data));
//	}
});

