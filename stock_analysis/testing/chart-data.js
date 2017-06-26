
/**
@param {string} dataset
@param {function(error, data)}fn
*/
function getData(dataset, fn){
    if(dataset == "test"){
	return fn(0,parseCSV(`date,close
    1-May-12,58.13
    30-Apr-12,53.98
    27-Apr-12,67.00
    26-Apr-12,89.70
    25-Apr-12,99.00
    24-Apr-12,130.28
    23-Apr-12,166.70
    20-Apr-12,234.98
    19-Apr-12,345.44
    18-Apr-12,443.34
    17-Apr-12,543.70
    16-Apr-12,580.13
    13-Apr-12,605.23
    12-Apr-12,622.77
    11-Apr-12,626.20
    10-Apr-12,628.44
    9-Apr-12,636.23
    5-Apr-12,633.68
    4-Apr-12,624.31
    3-Apr-12,629.32
    2-Apr-12,618.63
    30-Mar-12,599.55
    29-Mar-12,609.86
    28-Mar-12,617.62
    27-Mar-12,614.48
    26-Mar-12,606.98`));
    }else{
	//console.log("here");
	fn(0,DataSet.encase(dataset));
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
	format[i] = format[i].trim();
    }
    this.format = format;
    return this;
};

DataSet.prototype.addItemCSV = function(item){
    this.size++;
    item = item.split(",");
    var object = {}, t, v;
    for(var i = 0; i < item.length; ++i){
	t = item[i].trim();
	v = parseFloat(t);
	if(v == v)
	    t = v;
	object[this.format[i]] = t;
    }
    this.data.push(object);
    return this;
};

DataSet.prototype.forEach = function(fn){
    for(var i = 0; i < this.data.length; ++i){
	fn(this.data[i]);
    }
    return this;
};
