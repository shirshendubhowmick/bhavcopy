var renderTopStocksData = function(response) {
    response = response.replace(/"/g, '');
    response = response.replace(/'/g, '"');
    var jsonobj = JSON.parse(response);
    for(var row in jsonobj) {
        if (parseFloat(jsonobj[row]['OPEN']) < parseFloat(jsonobj[row]['CLOSE'])) {
            node = "<tr><td class=\"green-text\">" + jsonobj[row]['SC_CODE'] + "</td><td class=\"green-text\">" + jsonobj[row]['SC_NAME'] + "</td><td>" + 
            jsonobj[row]['OPEN'] + "</td><td>" + jsonobj[row]['HIGH'] + "</td><td>" + jsonobj[row]['LOW'] + "</td><td>" + jsonobj[row]['CLOSE'] + "</td><tr>";
        }
        else if (parseFloat(jsonobj[row]['OPEN']) === parseFloat(jsonobj[row]['CLOSE'])) {
            node = "<tr><td class=\"black-text\">" + jsonobj[row]['SC_CODE'] + "</td><td class=\"black-text\">" + jsonobj[row]['SC_NAME'] + "</td><td>" + 
            jsonobj[row]['OPEN'] + "</td><td>" + jsonobj[row]['HIGH'] + "</td><td>" + jsonobj[row]['LOW'] + "</td><td>" + jsonobj[row]['CLOSE'] + "</td><tr>";
        }
        else {
            node = "<tr><td class=\"red-text\">" + jsonobj[row]['SC_CODE'] + "</td><td class=\"red-text\">" + jsonobj[row]['SC_NAME'] + "</td><td>" + 
            jsonobj[row]['OPEN'] + "</td><td>" + jsonobj[row]['HIGH'] + "</td><td>" + jsonobj[row]['LOW'] + "</td><td>" + jsonobj[row]['CLOSE'] + "</td><tr>";
        }
        document.querySelector(".table-div table").innerHTML += node;
    }
};

var fetchTopStocksData = function () {
    xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            renderTopStocksData(this.responseText);
       }
       else if(this.readyState == 4 && this.status != 200) {
           alert("Error fetching data from server");
       }
    };

    xmlhttp.open("GET", "/toptenstocks", true);
    xmlhttp.send();
};

fetchTopStocksData();

document.querySelector(".navbar-search_box form").addEventListener("submit", function(event) {
    event.preventDefault();
    document.querySelector("#scripsearchbutton").click();
});

document.querySelector("#resettablebutton").addEventListener("click", function(event) {
    document.querySelector(".table-div").style.display = "block";
    document.querySelector(".error-text").style.display = "none";
    clearTableChild();
    fetchTopStocksData();
});

var clearTableChild = function() {
    var childLength = document.querySelector(".table-div table").children.length;
    for(i=childLength - 1 ; i > 0; i--) {
        document.querySelector(".table-div table").removeChild(document.querySelector(".table-div table").children[i]);
    }
};

var renderSingleStockData = function (response) {
    var jsonobj = JSON.parse(response);
    clearTableChild();
    if(jsonobj["SC_CODE"] !== undefined) {
        document.querySelector(".table-div").style.display = "block";
        document.querySelector(".error-text").style.display = "none";
        if (parseFloat(jsonobj['OPEN']) < parseFloat(jsonobj['CLOSE'])) {
            node = "<tr><td class=\"green-text\">" + jsonobj['SC_CODE'] + "</td><td class=\"green-text\">" + jsonobj['SC_NAME'] + "</td><td>" + 
            jsonobj['OPEN'] + "</td><td>" + jsonobj['HIGH'] + "</td><td>" + jsonobj['LOW'] + "</td><td>" + jsonobj['CLOSE'] + "</td><tr>";
        }
        else if (parseFloat(jsonobj['OPEN']) === parseFloat(jsonobj['CLOSE'])){
            node = "<tr><td class=\"black-text\">" + jsonobj['SC_CODE'] + "</td><td class=\"black-text\">" + jsonobj['SC_NAME'] + "</td><td>" + 
            jsonobj['OPEN'] + "</td><td>" + jsonobj['HIGH'] + "</td><td>" + jsonobj['LOW'] + "</td><td>" + jsonobj['CLOSE'] + "</td><tr>";
        }
        else {
            node = "<tr><td class=\"red-text\">" + jsonobj['SC_CODE'] + "</td><td class=\"red-text\">" + jsonobj['SC_NAME'] + "</td><td>" + 
            jsonobj['OPEN'] + "</td><td>" + jsonobj['HIGH'] + "</td><td>" + jsonobj['LOW'] + "</td><td>" + jsonobj['CLOSE'] + "</td><tr>";
        }
        document.querySelector(".table-div table").innerHTML += node;
    }
    else {
        document.querySelector(".table-div").style.display = "none";
        document.querySelector(".error-text").style.display = "block";
    }
};

document.querySelector("#scripsearchbutton").addEventListener("click", function() {
    var stockName = document.querySelector("input[name=scripsearch]").value;
    xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            renderSingleStockData(this.responseText)
       }
       else if(this.readyState == 4 && this.status != 200) {
           alert("Error fetching data from server");
       }
    };

    xmlhttp.open("GET", "/getstockdata?name=" + stockName.toUpperCase(), true);
    xmlhttp.send();
});