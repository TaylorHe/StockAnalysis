
function chain(request){
    this.links = [];
    //console.log(this.chain);
    this.chain(request);
    this.i = 0;
}

chain.prototype.chain = function(request){
    this.links.push(request);
    return this;
};

chain.prototype.exec = function(){
    if(this.i >= this.links.length) return;
    var req = this.links[this.i];
    var self = this;
    this.links[this.i] = null;
    this.i++;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
	if (xhr.readyState == XMLHttpRequest.DONE) {
	    if(req.fn)
		req.fn(xhr.responseText);
	    self.exec();
	}
    }
    xhr.open(req.method || "GET", req.url, true);
    xhr.send(req.data);
};

/*var mychain = new chain({
  data:JSON.stringify(files.testdata),
  url:'http://127.0.0.1:5000/datain',
  method:"POST",
  fn:function(x){
  console.log(JSON.parse(x));
  }
  }).chain({
  data:null,
  url:'http://127.0.0.1:5000/dataout',
  method:"GET",
  fn:function(x){
  var set = JSON.parse(x);
  for(var k in set){
  //console.log(x);
  loadGraph(set[k], k);
  }
  }
  });*/
twttr.events.bind('rendered', function (event) {
    var footer = event.target.contentDocument.querySelector('.footer');
    footer.parentNode.removeChild(footer);
    var follow = event.target.contentDocument.querySelector('.follow-button');
    follow.parentNode.removeChild(follow);
});

function loadGraph(stocks, tweets, key) {
    getData(stocks, tweets, key, function (error, data, sentiment) {
	var dummy = new Chart(500, 300, 0, 0);
	dummy.scaleAxisY(data, function(d) {
	    return d.close; 
	});
	var chrs = centsD(dummy.yaxis.x + dummy.yaxis.y) + "";
	BORDER_SIZE = chrs.length * MAGIC_NUMBER + MAGIC_CONSTANT;
	
	var chart = window.chart = new Chart(500, 300, BORDER_SIZE, BORDER_SIZE, data);
	document.body.appendChild(chart.canvas);
	
	chart.canvas.addEventListener("click", function(pt) {
	    var chartsize = chart.canvas.getBoundingClientRect();
	    var cx = pt.pageX - chartsize.left;
	    var cy = pt.pageY - chartsize.top;
	    for(var i = 0; i < birds.length; ++i){
		var x = birds[i][0], y = birds[i][1];
		if ((cx > x-10) && (cx < x + 10) && (cy > y-10) && (cy < y + 10)) {
		    var ID = birds[i][2];
		    var tw = document.getElementById("tweets");
		    tw.innerHTML = "";
		    twttr.widgets.createTweet(location.hash.substr(1) || ID, tw);
		}
	    }
	    
	});
	
	var i = 0;
	//console.log("asdf",data);
	chart.scaleAxisY(data, function(d) {
	    return d.close; 
	});

	chart.scaleAxisX(data, function(d) {
	    return d.date; 
	});
	
	chart.drawAxis(BORDER_SIZE, data, function(d) {
	    return {y:d.close, x:d.date};
	});
	
	i = 0;
	chart.plotLine(data, function(d){
	    return {y:d.close, x:d.date};
	});
	
	chart.plotBirds(sentiment, function(d){
	    return {x:d.date, z:d.sentiment, y:d.id};
	});
	

	
	/*
	  chart.ctx.strokeStyle = "red";
	  i = 0;
	  chart.plotLine(data, function(d){
	  return {y:d["High"], x:++i};
	  });
	  chart.ctx.strokeStyle = "blue";
	  i = 0;
	  chart.plotLine(data, function(d){
	  return {y:d["Low"], x:++i};
	  });
	*/
    });
}


window.addEventListener("message", receiveMessage, false);

//document.write("hi");
function receiveMessage(event)
{
    //console.log("hi");
    //var origin = event.origin || event.originalEvent.origin; // For Chrome, the origin property is in the event.originalEvent object.
    console.log(event.data);
    loadGraph(event.data.stocks, event.data.tweets, event.data.key);
}
