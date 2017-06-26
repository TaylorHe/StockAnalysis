

function makeFrame(stocks,key,tweets){
    
    var frame = document.createElement("iframe");
    //frame.innerHTML = contents;
    frame.src = "charts.html";
    document.getElementById("chartmaster").appendChild(frame);
    setTimeout(function(){
	console.log(stocks, "XXX", key, "XXX", tweets);
	frame.contentWindow.postMessage(
	{"stocks":stocks, "tweets":tweets, "key":key}, "*"
    )}, 500);
}

