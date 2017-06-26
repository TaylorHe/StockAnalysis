
/**
   @param {string} dataset
   @param {function(error, data)}fn
*/
function getData(dataset, tweets, key, fn){
    if(dataset == "test"){
	return fn(0,parseCSV("date,close\
1483401600,225783\
1483488000,227075\
1483574400,226900\
1483660800,227697\
1483920000,226889\
1484006400,226889\
1484092800,227532\
1484179200,227043\
1484265600,227463\
1484611200,226788\
1484697600,227188\
1484784000,226368\
1484870400,227131\
1485129600,226519\
1485216000,228007\
1485302400,229837\
1485388800,229667\
1485475200,229468\
1485734400,228089\
1485820800,227887\
1485907200,227955\
1485993600,228085\
1486080000,229741\
1486339200,229256\
1486425600,229308\
1486512000,229466\
1486598400,230787\
1486684800,231610\
1486944000,232825\
1487030400,233758\
1487116800,234925\
1487203200,234721\
1487289600,235115\
1487635200,236537\
1487721600,236282\
1487808000,236381\
1487894400,236734\
1488153600,236972\
1488240000,236363\
1488326400,239595\
1488412800,238191\
1488499200,238312\
1488758400,237531\
1488844800,236838\
1488931200,236297\
1489017600,236487\
1489104000,237260\
1489363200,237346\
1489449600,236544\
1489536000,238526\
1489622400,238137\
1489708800,237825\
1489968000,237346\
1490054400,234402\
1490140800,234844\
1490227200,234595\
1490313600,234397\
1490572800,234159"),

		  parseCSV("date,sentiment,'id\
1484006400,-1.0,844235587980746752\
1486080000,1.0,844235587980746752\
1487116800,-0.1,844235587980746752\
1488844800,0.0,844235587980746752\
1490054400,0.1,844235587980746752"));
    }else{

	var h1 = document.getElementById("mytitle");
	h1.innerHTML = key;
	
	fn(0,DataSet.encase(dataset),DataSet.encase(tweets));

    }
}

function parseCSV(data){
    lines = data.split("\n");
    var dataset = new DataSet();
    dataset.setCSVFormat(lines[0]);
    for(var i = 1; i < lines.length; ++i){
	dataset.addItemCSV(lines[i]);
    }
    return dataset;
}

function DataSet(){
    this.format = null;
    this.size = 0;
    this.data = [];
    this.index = 0;
    this.casts = {};
}

DataSet.encase = function(data){
    //console.log("?",data);
    /*for(var i = 0; i < data.length; ++i){
      for(var k in data){
      var t = parseFloat(data[k]);
      if(t == t)
      data[k] = t;
      }
      }*/
    var set = new DataSet();
    set.data = data;
    set.size = data.length;
    return set;
};

DataSet.prototype.setCSVFormat = function(format){
    format = format.split(",");
    for(var i = 0; i < format.length; ++i){
	var form = format[i] = format[i].trim();
	if(form.charAt(0) == "'"){
	    form = format[i] = form.substring(1);
	    this.casts[form] = function(x){
		return x;
	    };
	}

    }
    this.format = format;
    return this;
};

function MaybeFloat(t){
    v = parseFloat(t);
    if(v == v)
	t = v;
    return t;
}

DataSet.prototype.addItemCSV = function(item){
    this.size++;
    item = item.split(",");
    var object = {}, t, v;
    for(var i = 0; i < item.length; ++i){
	t = item[i].trim();
	var conv = this.casts[this.format[i]] || MaybeFloat;
	object[this.format[i]] = conv(t);
    }
    this.data.push(object);
    return this;
};

DataSet.prototype.forEach = function(fn){
    for(var i = 0; i < this.data.length; ++i){
	if(fn(this.data[i]))
	    break;
    }
    return this;
};
