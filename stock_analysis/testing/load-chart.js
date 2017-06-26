
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

var mychain = new chain({
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
	console.log(set);
	for(var k in set){
	    loadGraph(set[k], k);
	}
    }
});


function loadGraph(data){
    getData(data,function(error, data){
	var chart = new Chart(500, 300, 10, 10);
	
	var i = 0;
	//console.log("asdf",data);
	chart.scaleAxisY(data, function(d){
	    return d.close; 
	});

	chart.scaleAxisX(data, function(d){
	    return d.date; 
	});
	
	i = 0;
	chart.plotLine(data, function(d){
	    return {y:d.close, x:d.date};
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

window.addEventListener("load", function(){
    mychain.exec();
});


