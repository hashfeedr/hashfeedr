var width,height,c;

var framedelay=60;
var fontsize=26;
var linelength=20;
var fontface="DroidSansRegular";
var scalefactor=1.0;
var aspect=1.0;

var scene=[];
var transitions=[];
var tweets=[];

var placementx=100.0;

var campos=[0,0];
var camrot=0.0;

// new
var vp,scene;

function catmullrom(t,x0,x1,x2,x3){
	var t2=t*t,t3=t2*t;
	return 0.5*((2.0*x1)+(-x0+x2)*t+(2.0*x0-5.0*x1+4.0*x2-x3)*t2+(-x0+3.0*x1-3.0*x2+x3)*t3);
}

function lerp(t,a,b) {
	return a+(b-a)*t;
}

function placement(x) {
//	var t=x*0.006;
//	return (Math.sin(t)*2.0+Math.sin(2.232*t)+Math.sin(9.876*t)*5.0+Math.sin(18.888*t))*50.0;
	var t=x*0.002;
	return (Math.sin(t)*2.0+Math.sin(2.232*t)+Math.sin(9.876*t)*5.0+Math.sin(18.888*t))*40.0;
}

function calcangle() {
	var dy=placement(placementx+1.0)-placement(placementx);
	return Math.max(Math.min(Math.tan(dy)*0.1,0.1/aspect),-0.1/aspect);
}

function boxintersect(x1,y1,w1,h1,x2,y2,w2,h2) {
	return (x1 <= x2+w2 &&
          x2 <= x1+w1 &&
          y1 <= y2+h2 &&
          y2 <= y1+h1);
}

function breaktext(str, linelength) {
	var l=str.split(" ");
	var s="",n=0;
	for (var i=0;i<l.length;++i) {
		s+=l[i]+" ";
		n+=l[i].length;
		if (n>linelength) {
			s+="<br/>";
			n=0;
		}
	}
	return s;
}

function findnewpos_old(tw) {
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

function findnewpos(w,h) {
	var found=false,x=0,y=0;
	while (!found) {
		found=true;
		placementx+=1.0;
		x=placementx-w*0.5;
		y=placement(placementx)-h*0.5;
		for (var i=0;i<tweets.length;++i) {
			if (boxintersect(x,y,w,h,tweets[i].x,tweets[i].y,tweets[i].width,tweets[i].height)) {
				found=false;
				break;
			}
		}
	}
	return [x,y];
}

/** @constructor */
function Camera() {
	this.x=0;
	this.y=0;
	this.angle=0;

	// TODO: uniform scaling

	this.activate = function() {
		scene.css("-webkit-transform","rotate("+this.angle+"deg) translate3d("+((width*0.5)-this.x)+"px,"+((height*0.5)-this.y)+"px,0)");
	};

	this.move = function(x,y,angle) {
		this.x=x;
		this.y=y;
		this.angle=angle;
	};
}
var cam=new Camera();

/* easing stuff */
function easeinout(t) {
	return -0.5*(Math.cos(Math.PI*t)-1);
}

function resizescene() {
	width=$("#viewport").width();
	height=$("#viewport").height();

	scalefactor=parseFloat(height)/1000.0;
	aspect=parseFloat(width)/parseFloat(height);

	// TODO: reapply camera
}

function addtweet(txt,image,screenname) {
//	var txt="'Tulp' het hoogtepunt van mijn #nzon10? Kris en Lex Vesseur hebben het voor de neus van Mads weten weg te pikken. Een 9. #Formatgava.";
//	txt=txt.slice(0,Math.random()*txt.length);

	txt=breaktext(txt,25);
	image=image.replace(/normal(\.\w{3})$/,"bigger$1");
	addobj("tweet","<img src=\""+image+"\"/><p>"+txt+"</p><p class=\"username\">"+screenname+"</p>");
}

function addobj(cls, html) {
	var count=tweets.length+1;
	scene.append("<div class=\""+cls+"\" id=\"obj"+count+"\">"+html+"</div>");
	var t=$("#obj"+count);
	var w=t.outerWidth(); // This also forces a reflow of the layout, applying the initial css so that the transition occurs
	var h=t.outerHeight();
	var pos=findnewpos(w+16,h+16);
	t.css({"-webkit-transform":"translate("+pos[0]+"px,"+pos[1]+"px)","-webkit-transitxion":"all .8s ease-out"});
	t.css({"visibility":"visible"});
	cam.move(pos[0]+w*0.5,pos[1]+h*0.5,Math.random()*20.0-10.0);
	cam.activate();
	tweets.push({x:pos[0],y:pos[1],width:w+16,height:h+16,id:"#obj"+count});
	//t.css({"-webkit-transform":"rotate(30deg)"});
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

function parsemessage(msg) {
	var data=$.parseJSON(msg);
//	tweets[tweets.length]=([new Tweet(data.tweet.text,data.tweet.user.profile_image_url,data.tweet.user.screen_name)]);
//	var t=tweets[tweets.length-1];
//	new Transition(cam.position,cam.position.value,[t[0].position.value[0]+t[0].width*0.5,t[0].position.value[1]+t[0].height*0.5,calcangle()],20.0);
//	if ("image" in data) {
//		new PictureBox(data.image,[t[0].position.value[0]+t[0].width*0.5,t[0].position.value[1]+t[0].height*0.5]);
//	}
	addtweet(data.tweet.text,data.tweet.user.profile_image_url,data.tweet.user.screen_name);
}

$(function(){
	vp=$("#viewport");
	scene=$("#scene");

	resizescene();
	$(window).resize(resizescene);
	scene.css("-webkit-transform","translate3d("+(width*0.5)+"px,"+(height*0.5)+"px,0)");

	vp.click(function(){
		addtweet();
		//cam.move(200,200,Math.random()*40.0-20.0);
//		cam.move(200,200,0);
//		cam.activate();
//		var t=new Tweet("RT justin bieber was a freaking lolcat abuser, he totally biebered them ololololol bla bla blah! 12345");
//		scene.push(t);
//		new Transition(cam.position,cam.position.value,[t.position.value[0]+t.width*0.5,t.position.value[1]+t.height*0.5,calcangle()],20.0);
	});
//	scene[scene.length]=[new GrowArrow([-100.0,10.0],[100.0,100.0],[400.0,400.0],[500.0,300.0])];
//	new Transition(tweet.position,[0,0],[50,70],10.0);
//	new Transition(cam.position,[0.0,20.0,0.0],[200.0,0.0,1.0],100.0);

	setInterval(function(){
//		if (update()) draw();
	},framedelay);
      
	var ws = new WebSocket(websocket_url);
	ws.onmessage = function(e) {
		parsemessage(e.data);
	};
});

