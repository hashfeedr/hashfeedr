var width,height,c;

var framedelay=60;
var fontsize=26;
var linelength=20;
var fontface="DroidSansRegular";

var scene=[];
var transitions=[];
var tweets=[];

var placementx=100.0;

var campos=[0,0];
var camrot=0.0;

//var backdrop=new Image();
//backdrop.src="/media/images/feedbackdrop.jpg";

function catmullrom(t,x0,x1,x2,x3){
	var t2=t*t,t3=t2*t;
	return 0.5*((2.0*x1)+(-x0+x2)*t+(2.0*x0-5.0*x1+4.0*x2-x3)*t2+(-x0+3.0*x1-3.0*x2+x3)*t3);
}

function lerp(t,a,b) {
	return a+(b-a)*t;
}

function placement(x) {
	var t=x*0.006;
	return (Math.sin(t)*2.0+Math.sin(2.232*t)+Math.sin(9.876*t)*5.0+Math.sin(18.888*t))*50.0;
}

function calcangle() {
	var dy=placement(placementx+1.0)-placement(placementx);
	return Math.max(Math.min(Math.tan(dy)*0.1,0.1),-0.1);
}

function boxintersect(x1,y1,w1,h1,x2,y2,w2,h2) {
	return (x1 <= x2+w2 &&
          x2 <= x1+w1 &&
          y1 <= y2+h2 &&
          y2 <= y1+h1);
}

function eradicate() {
	for (var i=0;i<tweets.length;++i) {
		if (tweets[i][0].position.value[0]<placementx-2000) {
			tweets[i][0].release();
			delete tweets[i][0];
			tweets.splice(i--,1);
		}
	}
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
			if (boxintersect(x,y,w,h,tweets[i][0].position.value[0],tweets[i][0].position.value[1],tweets[i][0].width,tweets[i][0].height)) {
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
		c.translate(width*0.5,height*0.5+128);
		c.rotate(this.position.value[2]);
		c.translate(-this.position.value[0],-this.position.value[1]);
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
function PictureBox(src,tweetpos) {
	this.position=new Property([0,0]);
	this.image=new Image();
	this.image.src=src;
	this.loaded=false;
	this.width=0;
	this.height=0;
	this.margin=16;
	this.padding=8;
	this.tweetpos=tweetpos;

	var self=this;
	this.image.onload=function() {
		self.loaded=true;
		self.width=this.width+self.margin*2+self.padding*2;
		self.height=this.height+self.margin*2+self.padding*2;
		findnewpos(self);
		tweets[tweets.length]=[self];
		scene[scene.length]=[new TweetLine([self.position.value[0]+self.width*0.5,self.position.value[1]+self.width*0.5],self.tweetpos)];
	};

	this.release=function() {
		delete this.image;
		delete this.position;
	};

	this.draw=function() {
		if (self.loaded) {
			c.save();
			c.translate(this.position.value[0],this.position.value[1]);
			c.fillStyle="rgba(0,0,0,1.0)";
			c.fillRect(this.margin,this.margin,this.width-this.margin*2,this.height-this.margin*2);
			c.strokeStyle="rgba(255,255,255,0.6)";
			c.strokeRect(this.margin,this.margin,this.width-this.margin*2,this.height-this.margin*2);
			c.drawImage(this.image,this.margin+this.padding,this.margin+this.padding);
			c.restore();
		}
	};
}

/** @constructor */
function Tweet(message,avatar,username) {
	this.position=new Property([100,10]);
	this.charpos=new Property([0]);
	this.margin=16;
	this.padding=8;
	this.message=message;
	this.username=username;
	
	var l=this.message.split(" ");
	var s="",n=0;
	for (var i=0;i<l.length;++i) {
		s+=l[i]+" ";
		n+=l[i].length;
		if (n>linelength) {
			s+="\n";
			n=0;
		}
	}
	this.message=s;

	c.font=fontsize+"px "+fontface;
	var exts=textmetrics(fontsize,this.message);
	this.width=64+this.padding*3+exts[0]+2*this.margin;
	this.height=Math.max(exts[1],64)+2*this.padding+2*this.margin+fontsize;
	findnewpos(this);

	this.avatar=new Image();
	this.avatar.src=avatar.replace(/normal.jpg$/,"bigger.jpg");

	new Transition(this.charpos,[0],[this.message.length],10);
	
	this.release=function() {
		delete this.avatar;
		delete this.position;
		delete this.charpos;
	};
	
	this.draw=function() {
		c.shadowColor="rgba(0,0,0,0.0)";
		c.shadowOffsetX=0;
		c.shadowOffsetY=0;
		c.shadowBlur=16;

		c.save();
		c.translate(this.position.value[0],this.position.value[1]);
		
		c.fillStyle="#040a14";
		c.fillRect(this.margin,this.margin,this.width-this.margin*2,this.height-this.margin*2);
		c.strokeStyle="rgba(255,255,255,0.8)";
		c.strokeRect(this.margin,this.margin,this.width-this.margin*2,this.height-this.margin*2);
		
		if (this.avatar.complete==true) {
			c.shadowBlur=0;
			try {
				c.drawImage(this.avatar,this.margin+this.padding,this.margin+this.padding,64,64);
			} catch(err) {
				// fail silently :)
			}
		}

		c.fillStyle="#79a631";
		c.textAlign="right";
		c.textBaseline="bottom";
		c.font=fontsize+"px DroidSansBold";
		c.fillText(this.username,this.width-this.margin-this.padding*2,this.height-this.margin-this.padding);
		c.fillStyle="#fff";
		c.textBaseline="top";
		c.textAlign="left";
		c.shadowColor="rgba(0,0,0,0.0)";
		c.shadowOffsetX=2;
		c.shadowOffsetY=2;
		c.shadowBlur=4;
		c.font=fontsize+"px "+fontface;
		filltext(fontsize,this.message.substr(0,this.charpos.value[0]),this.margin+this.padding*2+64,this.margin+this.padding-4);
		c.restore();
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

/** @constructor */
function TweetLine(p0,p1) {
	this.p0=new Property([p0[0],p0[1]]);
	this.p1=new Property([p1[0],p1[1]]);
	new Transition(this.p0,[p1[0],p1[1]],[p0[0],p0[1]],20);

	scene[scene.length]=[this];

	this.draw=function() {
		c.strokeStyle="#ccc";
		c.beginPath();
		c.lineWidth=10;
		c.moveTo(this.p0.value[0],this.p0.value[1]);
		c.lineTo(this.p1.value[0],this.p1.value[1]);
		c.stroke();
	};
}

//scene[scene.length]=[new TweetLine([0,0],[200,200])];

function resizecanvas() {
	width=c.canvas.clientWidth;
	height=c.canvas.clientHeight;
	c.canvas.width=width;
	c.canvas.height=height;
	c.textBaseline="top";
	draw();
}

function update() {
	for (var t=0;t<transitions.length;++t) {
		if (transitions[t].update()===false) {
			transitions.splice(t--,1);
		}
	}
	if (transitions.length>0) {
		eradicate();
		return true;
	} else {
		return false;
	}
}

function draw() {
//	if (backdrop.complete==true) {
//		c.drawImage(backdrop,0,0,width,height);
//	}
	c.fillStyle="#0b1d3a";
	c.fillRect(0,0,width,height);
	c.save();
	c.scale(0.8,0.8);
	cam.activate();
//	c.strokeStyle="#fff";
//	c.beginPath();
//	for (var i=0;i<1000.0;i+=1) {
//		c.lineTo(i,placement(i));
//	}
//	c.stroke();
	for (var e=0;e<scene.length;e++) {
		c.save();
		scene[e][0].draw();
		c.restore();
	}
	for (var e=0;e<tweets.length;e++) {
		c.save();
		tweets[e][0].draw();
		c.restore();
	}
	c.restore();

	c.fillText("#tweets: "+tweets.length,0,0);
}

function parsemessage(msg) {
	var data=$.parseJSON(msg);
	tweets[tweets.length]=([new Tweet(data.tweet.text,data.tweet.user.profile_image_url,data.tweet.user.screen_name)]);
	var t=tweets[tweets.length-1];
	new Transition(cam.position,cam.position.value,[t[0].position.value[0]+t[0].width*0.5,t[0].position.value[1]+t[0].height*0.5,calcangle()],20.0);
	if ("image" in data) {
		new PictureBox(data.image,[t[0].position.value[0]+t[0].width*0.5,t[0].position.value[1]+t[0].height*0.5]);
	}
}

$(function(){
	c=$("#thecanvas").get(0).getContext("2d");

	resizecanvas();
	$(window).resize(resizecanvas);

	$("#thecanvas").click(function(){
//		var t=new Tweet("RT justin bieber was a freaking lolcat abuser, he totally biebered them ololololol bla bla blah! 12345");
//		scene.push(t);
//		new Transition(cam.position,cam.position.value,[t.position.value[0]+t.width*0.5,t.position.value[1]+t.height*0.5,calcangle()],20.0);
	});
//	scene[scene.length]=[new GrowArrow([-100.0,10.0],[100.0,100.0],[400.0,400.0],[500.0,300.0])];
//	new Transition(tweet.position,[0,0],[50,70],10.0);
//	new Transition(cam.position,[0.0,20.0,0.0],[200.0,0.0,1.0],100.0);

	setInterval(function(){
		if (update()) draw();
	},framedelay);
      
	var ws = new WebSocket(websocket_url);
	ws.onmessage = function(e) {
		parsemessage(e.data);
	};
});

