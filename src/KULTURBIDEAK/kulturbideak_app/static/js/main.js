/* main.js */

//create httprequestobject
function createXmlHttpRequestObject(){
    var xmlHttp;
    if (window.XMLHttpRequest){
        try{xmlHttp = new XMLHttpRequest(); }
        catch (e) {xmlHttp = false;}
    }
    else if (window.ActiveXObject){
        try {xmlHttp = new ActiveXObject("MSXML2.XMLHTTP");}
        catch (e) {
            try{xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");}
            catch (e) {xmlHttp = false;}
        }
    }
    if (!xmlHttp)
        alert("Error creating an XMLHttpRequest object!");
    else
        return xmlHttp;
}

//generic server answer
function server_answer(xmlHttp){
	xml_answer = xmlHttp.responseXML;
	if (xml_answer){
		xml_Document = xml_answer.documentElement;
		var data = xml_Document.getElementsByTagName("request_answer");
		if (data.length > 0){
			return (data[0].firstChild.data);
		}
	}
	return false;
}

//start loader
function start_loader(loader){
    if (!loader) loader = "loader";
    var loader_element = document.getElementById(loader);
    if (loader_element){
        loader_element.style.visibility = "visible";
    }
}

//stop loader
function stop_loader(loader){
    if (!loader) loader = "loader";
    if (document.getElementById(loader) !=null)
        setTimeout("document.getElementById('" + loader + "').style.visibility = 'hidden';",500);
}
