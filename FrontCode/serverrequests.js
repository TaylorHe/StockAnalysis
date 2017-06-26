




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

function clearCharts(){
    document.getElementById("chartmaster").innerHTML = "";
}

function execServerPredictRequest(){
    var asdf = document.getElementById("mySearch").value;
    console.log(JSON.stringify(asdf.split(",")));
    (new chain({data:JSON.stringify({predictive:true, requests:asdf.split(","), name:"analysis"}),
		url:'http://127.0.0.1:5001/fileout',
		method:"POST",
		fn:function(x){
		    
		    console.log(x);
		    clearCharts();
		    var set = JSON.parse(x)[1];
		    if(set.constructor == String) return;
		    var stocks = set.stocks;
		    var tweets = set.tweets;
		    
		    for(var k in stocks){
			makeFrame(stocks[k], k, tweets);
		    }

		}
	       }
	       
	      )).exec();
}

function execServerRequest(){
    
    (new chain({data:JSON.stringify({requests:document.getElementById("mySearch").value.split(","), name:"analysis"}),
		url:'http://127.0.0.1:5001/fileout',
		method:"POST",
		fn:function(x){
		    //console.log(x);
		    clearCharts();
		    var set = JSON.parse(x)[1];
		    if(set.constructor == String) return;
		    var stocks = set.stocks;
		    var tweets = set.tweets;
		    console.log(stocks);
		    
		    for(var k in stocks){
			makeFrame(stocks[k], k, tweets);
		    }
		}
	       }
	       
	      )).exec();
}
