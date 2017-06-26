var files = {};

function HTMLObject(type, className, innerHTML) {
  var thing = document.createElement(type);
  if (className)
    thing.className = className;
  if (innerHTML)
    thing.innerHTML = innerHTML;
  this.container = thing;
}

HTMLObject.prototype.append = function (other) {
  this.container.appendChild(other.container);
};

function TestResult(name, result, message, prefix) {
  this.prefix = prefix || TestResult.prefix;
  HTMLObject.call(this, "div", "testcase " + result);
  if (this.prefix)
    name = this.prefix + "." + name;
  this.name = new HTMLObject("div", "name", name);
  this.append(this.name);
  if (message) {
    this.message = new HTMLObject("div", "message", message);
    this.append(this.message);
  }
}

TestResult.prototype = Object.create(HTMLObject.prototype);
TestResult.prototype.constructor = TestResult;

TestResult.PASSING = "pass";
TestResult.FAILING = "fail";

TestResult.prefix = null;

function chain(request) {
  this.links = [];
  //console.log(this.chain);
  this.chain(request);
  this.i = 0;
}

chain.prototype.chain = function (request) {
  this.links.push(request);
  return this;
};

chain.prototype.exec = function () {
  if (this.i >= this.links.length) return;
  var req = this.links[this.i];
  var self = this;
  this.links[this.i] = null;
  this.i++;
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      if (req.fn)
        req.fn(xhr.responseText);
      self.exec();
    }
  }
  xhr.open(req.method || "GET", req.url, true);
  xhr.send(req.data);
};

var Page = new HTMLObject("div");
document.body.appendChild(Page.container);