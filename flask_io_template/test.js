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
    data:JSON.stringify({"name":"test","file":{"asdf":"hi"}}),
    url:'http://127.0.0.1:4999/filein',
    method:"POST",
    fn:function(x){
	console.log(JSON.parse(x));
    }
}).chain({
    data:JSON.stringify({"name":"test"}),
    url:'http://127.0.0.1:4999/fileout',
    method:"POST",
    fn:function(x){
	console.log(JSON.parse(x));
    }
}).exec();