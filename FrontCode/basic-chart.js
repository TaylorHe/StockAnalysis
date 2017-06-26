

function Vector(x, y) {
    this.x = x || 0;
    this.y = y || 0;
};

function Chart(width, height, borderX, borderY, dataset) {
    this.canvas = document.createElement("canvas");
	
	this.dataset = dataset;
    this.canvas.width = width;
    this.canvas.height = height;
    this.ctx = this.canvas.getContext("2d");
    this.xaxis = new Vector(0, 1);
    this.yaxis = new Vector(0, 1);
    this.area = new Vector(width - borderX * 2, height - borderY * 2);
    this.border = new Vector(borderX, borderY);
    this.size = new Vector(width, height);
	
	var mt = 1;
	if(Chart.IS_HIGH_DEF) mt = 2;
    this.canvas.width = "" + this.size.x*mt;
    this.canvas.height = "" + this.size.y*mt;
	this.canvas.style.width = this.size.x + "px";
	this.canvas.style.height = this.size.y + "px";
	if(Chart.IS_HIGH_DEF) this.ctx.scale(2,2);
}

Chart.IS_HIGH_DEF = ((window.matchMedia && (window.matchMedia('only screen and (min-resolution: 124dpi), only screen and (min-resolution: 1.3dppx), only screen and (min-resolution: 48.8dpcm)').matches || window.matchMedia('only screen and (-webkit-min-device-pixel-ratio: 1.3), only screen and (-o-min-device-pixel-ratio: 2.6/2), only screen and (min--moz-device-pixel-ratio: 1.3), only screen and (min-device-pixel-ratio: 1.3)').matches)) || (window.devicePixelRatio && window.devicePixelRatio > 1.3));


Chart.prototype.scaledAxis = function (dataset, getter) {
    var first = true;
    var axis = new Vector(0, 0);
    dataset.forEach(function (pt) {
        var v = getter(pt);
        if (first) {
            first = false;
            axis.x = v;
            axis.y = v;
        } else {
            if (v < axis.x) {
                axis.x = v;
            } else if (v > axis.y) {
                axis.y = v;
            }
        }
    });
    axis.y -= axis.x;
    return axis;
};

Chart.prototype.scaleAxisX = function (dataset, getter) {
    this.xaxis = this.scaledAxis(dataset, getter);
    return this;
};

Chart.prototype.scaleAxisY = function (dataset, getter) {
    this.yaxis = this.scaledAxis(dataset, getter);
    return this;
};

Chart.prototype.scalePoint = function (pt) {
    return new Vector(
        (((pt.x - this.xaxis.x) / this.xaxis.y)) * this.area.x + this.border.x, 
        (1 - ((pt.y - this.yaxis.x) / this.yaxis.y)) * this.area.y + this.border.y
    );
};

Chart.prototype.drawAxis = function (x, dataset, getter) {
	drawLine(x, x, x, this.size.y-x);
	drawLine(x, this.size.y-x, this.size.x-x, this.size.y-x);
	var rxy = x;
	var start = convertDate(firstDate(dataset, getter));
	var pointsy = 5.01;
	//var pointsx = 7.01;
	var maxy = (this.yaxis.x + this.yaxis.y);//maxY(dataset, getter));
	var miny = (this.yaxis.x);
	var mdif = Math.floor((maxy - miny) / pointsy + 1);
	for (var ryy = BORDER_SIZE; ryy < this.size.y-x; ryy += (this.size.y-(x*2))/pointsy) {
	    this.ctx.fillText((maxy/100 | 0) + "." + (maxy%100), 0, ryy);
		this.ctx.fillRect(rxy-1.5, ryy-1.5, 3, 3);
		maxy -= mdif;
	}
	var points = [];
	var px, py;
	var ryx = this.size.y-BORDER_SIZE;
	return this;
	
};

Chart.prototype.plotBirds = function (sentiment, getter) {
	sentiment.forEach(function (s) {
		var dsi = getter(s);
		var dat = dsi.x;
		var sent = dsi.z;
		var id = dsi.y;
		plotDate(dat, id, sent);
	});
};

function plotPoint(x,y, id, sent){
	var img = document.getElementById('twitter');
	chart.ctx.drawImage(img, x-10, y-10, 1139/50|0, 926/50|0);
	birds.push([x,y, id]);
	if (sent == 0.0) {
		chart.ctx.fillStyle = "rgb(243,230,0)";
		chart.ctx.fillRect(x+11, y-3, 6, 4);
	}
	var color = "rgb(";
	var r = Math.floor(255 - 255 * sent);
	if (r > 255) {
		r = 255;
	}
	if (r < 0) {
		r = 0;
	}
	var g = Math.floor(220 + 220 * sent);
	if (g >= 220) {
		g = 218;
	}
	if (g <= 0) {
		g = 0;
	}
	var b = Math.floor(50*sent);
	if (b < 0) {
		b = 0;
	}
	if (b > 50) {
		b = 50;
	}
	color = color + String(r) + "," + String(g) + "," + String(b) + ")";
	if(sent > 0) {
		drawArrow(x+13, y, x+13, y-3, color);
		//drawArrow(x+12, y-3, x+12, y-15, color);
	} else if (sent < 0) {
		drawArrow(x+14, y-3, x+14, y+3, color);
		//drawArrow(x+12, y-3, x+12, y+10, color);
	}	
};

function drawArrow(fromx, fromy, tox, toy, color){
	//variables to be used when creating the arrow
	var headlen = 5;//2;
	var angle = Math.atan2(toy-fromy,tox-fromx);
	//starting path of the arrow from the start square to the end square and drawing the stroke
//	chart.ctx.beginPath();
//	chart.ctx.moveTo(fromx, fromy);
//	chart.ctx.lineTo(tox, toy);
//	chart.ctx.strokeStyle = color;
//	chart.ctx.lineWidth = 3;
//	chart.ctx.stroke();
	//starting a new path from the head of the arrow to one of the sides of the point
	chart.ctx.beginPath();
	chart.ctx.moveTo(tox, toy);
	chart.ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),toy-headlen*Math.sin(angle-Math.PI/7));
	
	//path from the side point of the arrow, to the other side point
	chart.ctx.lineTo(tox-headlen*Math.cos(angle+Math.PI/7),toy-headlen*Math.sin(angle+Math.PI/7));
	//path from the side point back to the tip of the arrow, and then again to the opposite side point
	chart.ctx.lineTo(tox, toy);
	chart.ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),toy-headlen*Math.sin(angle-Math.PI/7));
	//draws the paths created above
	chart.ctx.strokeStyle = color;
	chart.ctx.lineWidth = 3;
	chart.ctx.stroke();
	chart.ctx.fillStyle = color;
	chart.ctx.fill();
};

function plotDate(date, id, sent){
	var before = null;
	var after = null;
	chart.dataset.forEach(function(x){
		before = after;
		after = x;
		if(x.date >= date) return true;
    });
	var x = 0;
	var y = 0;
	if(!before){
		x = after.date;
		y = after.close;
    }else if(!after){
		x = after.date;
		y = after.close;
    }else{
		var percent = (date - before.date)/(after.date - before.date);
		x = date;
		y = before.close + percent*(after.close - before.close);
    }
	var pt = chart.scalePoint({x:x, y:y});
	plotPoint(pt.x,pt.y, id, sent);
}

function firstDate(dataset, getter) {
	var start;
	dataset.forEach(function (d) {
		start = d.x;
	});
	return start;
};

function drawLine(x1, y1, x2, y2) {
	chart.ctx.beginPath();
	chart.ctx.moveTo(x1, y1);
	chart.ctx.lineTo(x2, y2);
	chart.ctx.stroke();
};

function convertDate(n) {
	var utcSeconds = n;
	var d = new Date(0);
	d.setUTCSeconds(utcSeconds);
	return d;
};

function numChars(dataset, getter) {
	var maxn = 0;
	dataset.forEach(function (d) {
		var n = d.x;
		var nums = 0;
		while (n != 0) {
			nums++;
			n = Math.floor(n/10);
		}
		if (nums > maxn) {
			maxn = nums;
		}
	});
	return maxn;
};

function yPlacement(n) {
	var txtposx = BORDER_SIZE;
};

function centsD(c) {
	var doll = c/100;
	return doll;
};

function getMonth(d) {
	var month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"];
	var m = d.getMonth();
	return month[m];
};

function getDay(d) {
	var day = d.getDate();
	return day;
};

Chart.prototype.plotLine = function (dataset, getter) {
    var self = this;
    var first = true;
    this.ctx.beginPath();
	var mon;
	var year;
    dataset.forEach(function (d) {
		var dc = getter(d);
		var c = (dc.y / 100);
		var dat = convertDate(dc.x);
		var m = getMonth(dat);
		var y = dat.getFullYear();
		var day = getDay(dat);
		var pt = self.scalePoint(getter(d));
		if (first) {
			first = false;
			self.ctx.moveTo(pt.x, pt.y);
			self.ctx.fillText(m, BORDER_SIZE, self.size.y-BORDER_SIZE+10);
			self.ctx.fillText(y, BORDER_SIZE/3, self.size.y-BORDER_SIZE+10);
			self.ctx.fillRect(pt.x-1.5, self.size.y-BORDER_SIZE-1.5, 3, 3);
			mon = m;
			year = y;
		} else {
			self.ctx.lineTo(pt.x, pt.y);
			
			if (mon != m) {
				mon = m;
				self.ctx.fillText(m, pt.x-10, self.size.y-BORDER_SIZE+10);
				self.ctx.fillRect(pt.x-1.5, self.size.y-BORDER_SIZE-1.5, 3, 3);
			}
			if (year != y) {
				year = y;
				self.ctx.fillText(y, pt.x-20, self.size.y-BORDER_SIZE+10);
			}
		}
    });
    this.ctx.stroke();
    return this;
};
