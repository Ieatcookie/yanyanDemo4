function auth_register() {
    var req = new XMLHttpRequest();
    var url = "/auth_register";
    
    data = "";
    var email = document.getElementById('email').value;
    data += "email="+email;
    var fname = document.getElementById('fname').value;
    data += "&name_first="+fname;
    var lname = document.getElementById('lname').value;
    data += "&name_last="+lname;
    var password = document.getElementById('password').value;
    data += "&password="+password;

    req.open("POST",url,false);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send(data)
}

function sendRequest(url,data,type) {
    var request = new XMLHttpRequest();
    if(type == "POST"){
        request.open(type,url,false);
        request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        request.send(data);
    } else if(type == "GET") {
        request.open(type,url+"?" + data,false);
        request.send();
    }
    var response = request.response;
    return response;
}

function parseData(data,type) {
    if(type == "json"){
        console.log(data);
        return JSON.parse(data);
    }
    return data;
}

function addCookies(key,value){
    document.cookie = key+"="+value+";"
    console.log(document.cookie);
}


function getCookies(key){
    var name = key+"=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var value = decodedCookie.split(';');
    for(var i = 0; i <value.length; i++) {
        var c = value[i];
        while (c.charAt(0) == ' ') {
          c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
        }
      }
      return "";        
}
