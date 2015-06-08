//create interview
function create_interview(){
	start_loader("loader");                                                                                     // start loader
	var uploaded_file = document.getElementById("uploaded_file");                                               // beharrezko baldintzak jaso
	if (uploaded_file.value != ""){
		var informant_id = document.getElementById("informant_id");                                             // beharrezko ez diren baldintzak jaso
		create_interview_request(informant_id.value,uploaded_file.value);                                       //request!
	}
	else{                                                                                                       // baldintzak bete ez badira
		show_message("empty_interview_error");                                                                  // (aukeran) errorea 
	stop_loader("loader");                                                                                      // loaderra gelditu
	}
}

//create interview request
function create_interview_request(informant_id,uploaded_file){
	var xmlHttp = createXmlHttpRequestObject();
	if (xmlHttp.readyState == 4 || xmlHttp.readyState == 0){ 
        xmlHttp.open("POST",SITE_URL + "php/interviews/create_interview.php",true);
        xmlHttp.onreadystatechange = function (){
            create_interview_answer(xmlHttp);                                                                   // Erantzuna jasotzean exekutatuko den deia
        };
        xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlHttp.send("informant_id=" + informant_id + "&uploaded_file=" + uploaded_file);                       // Eskaera bidali
    }
}

//create interview answer
function create_interview_answer(xmlHttp){
    if (xmlHttp.readyState == 4){
        if(xmlHttp.status == 200){
            if (server_answer(xmlHttp)){                                                                        // Erantzun generikoa!!
				var upload_interview_container = document.getElementById("upload_interview_container");         // Egin beharrekoa egin
				var uploaded_interview_container = document.getElementById("uploaded_interview_container");
				upload_interview_container.setAttribute("class","hidden");
				uploaded_interview_container.removeAttribute("class");
			}
			else{                                                                                               // Jaso beharreko emaitza lortu ez bada, errorea
				show_message("default_error");
			}
			stop_loader("loader");                                                                              // Emaitza ona edo txarra jaso bada, loaderra paratu
        }
    }
}
