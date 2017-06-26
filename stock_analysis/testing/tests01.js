var TIME_OUT_BASE_MS = 1000,
  prefix = "StockAnalysis";

function fallbackFailure(testname, sourcename) {
  Page.append(new TestResult(testname, TestResult.FAILING, "Test failed due to failure of: " + sourcename, prefix));
}

function timeoutFailure(testname) {
  Page.append(new TestResult(testname, TestResult.FAILING, "Test failed due to timeout.", prefix));
}

function dependencyFailureList (source, fail_list) {
  for (var i = 0; i < fail_list.length; i++) {
    fallbackFailure(fail_list[i], source);
  }
};

var timeouts = {};

timeouts.ServerInput = setTimeout(function () {
  timeoutFailure("ServerInput");
  dependencyFailureList("ServerInput", ["ServerOutput"]);
  timeouts.ServerInput = null;
}, TIME_OUT_BASE_MS);

var mychain = new chain({
  data: JSON.stringify(files.testdata),
  url: 'http://127.0.0.1:5000/datain',
  method: "POST",
  fn: function (x) {
    if(timeouts.ServerInput == null)
      return;
    clearTimeout(timeouts.ServerInput);
    try{
      var set = JSON.parse(x);
      var strt = x.substring(0, 24);
      if(strt != '[true, "All Good!"]')
        throw new Error("bad return value");
      Page.append(new TestResult("ServerInput", TestResult.PASSING, "Recieved: " + strt, prefix));
    }catch(e){
      Page.append(new TestResult("ServerInput", TestResult.FAILING, "Error:" + e.toString(), prefix));
    }
    timeouts.ServerOutput = setTimeout(function () {
      timeoutFailure("ServerOutput");
      timeouts.ServerOutput = null;
    }, TIME_OUT_BASE_MS);
  }

}).chain({
  data: null,
  url: 'http://127.0.0.1:5000/dataout',
  method: "GET",
  fn: function (x) {
    if(timeouts.ServerOutput == null)
      return;
    clearTimeout(timeouts.ServerOutput);
    try{
      var set = JSON.parse(x);
      var strt = x.substring(0, 24);
      if(strt != '{"%5eGSPC": [{"close": 2')
        throw new Error("bad return value");
      Page.append(new TestResult("ServerOutput", TestResult.PASSING, "Recieved: " + strt, prefix));
    }catch(e){
      Page.append(new TestResult("ServerOutput", TestResult.FAILING, "Error:" + e.toString(), prefix));
    }
  }
});
mychain.exec();