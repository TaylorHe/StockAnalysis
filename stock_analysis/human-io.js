var files = {};

function loadFn(){
    console.log(files.testdata);
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
	if (xhr.readyState == XMLHttpRequest.DONE) {
	    console.log("response:", JSON.parse(xhr.responseText));
	}
    }
    xhr.open('POST', 'http://127.0.0.1:5000/human-io', true);
    xhr.send(JSON.stringify(files.testdata));
}

window.addEventListener("load", loadFn);



