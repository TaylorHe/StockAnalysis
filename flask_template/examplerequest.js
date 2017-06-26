var obj = {searchfor:"term"};

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       console.log(xhttp.responseText);
    }
};
xhttp.open("POST", "http://localhost:5000/senditback", true);
xhttp.send(obj);
