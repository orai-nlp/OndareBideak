

var paper = null;
var el_counter=0;
var svgns = "http://www.w3.org/2000/svg";
var pb_box_w = 160;
var pb_box_h = 120;
var pb_box_space = 20;//
var paths_starts = [];
var connections = [];


function initialize(){
	
	//raphael martxan jartzeko
	set_pb();
	//kargatu workspaceko elementuak
	load_ws();
	//kargatu erabiltzailearen ibilbideak
	//load_paths_list(user_id);
	//Kargatu Ibilbide bozkatuenak
	load_most_voted_paths();
	//Kargatu Eguneko Itema
	load_eguneko_itema();
}
function initialize_notlogged(){
	
	//raphael martxan jartzeko
	set_pb();
	//Kargatu Ibilbide bozkatuenak
	load_most_voted_paths();
	//Kargatu Eguneko Itema
	load_eguneko_itema();
}

function hizkuntza_url_egokitu(linka){
	
    //Hizkuntza aukeraketa egiten duen formularioaren url helbidea egokitzen du
    var form=document.getElementById("hizkuntza_aukeraketa_id");
    var hizkuntza=linka.text.toLowerCase();
    form.name="setLang"+hizkuntza;
    document.getElementsByName("language")[0].value=hizkuntza;
    document.getElementsByName("setLang"+hizkuntza)[0].submit();
    return false;

}

//pantailaren albo batean erabiltzailearen path-ak kargatzeko
function load_paths_list(user_id){
	var paths_list_container = document.getElementById("nire_ibilbideak");
	if (paths_list_container){
		//ajax deia, kargatu kontainerrean zerrenda
		load_paths_list_request(paths_list_container, user_id);
	}
}


function load_paths_list_request(paths_list_container,user_id)
{
	
	var csrftoken = getCookie('csrftoken');
	var xmlHttp = createXmlHttpRequestObject();
	
	if (xmlHttp.readyState == 4 || xmlHttp.readyState == 0){ 
		
		$.ajaxSetup({
   			beforeSend: function(xhr, settings) {
       		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
           		xhr.setRequestHeader("X-CSRFToken", csrftoken);
       		}
   		 	}
		});
        xmlHttp.open("POST","../ajax_lortu_paths_list",true);
        xmlHttp.onreadystatechange = function (){
            load_paths_list_answer(xmlHttp,paths_list_container);                                                                   // Erantzuna jasotzean exekutatuko den deia
        };
        xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlHttp.send("user_id=" + user_id  + "&csrfmiddlewaretoken=" + csrftoken);                       // Eskaera bidali
    }
}

function load_paths_list_answer(xmlHttp,paths_list_container)
{
	
	if (xmlHttp.readyState == 4){
        if(xmlHttp.status == 200){
			var xml_answer = xmlHttp.responseXML;
			var xml_Document = xml_answer.documentElement;
			var paths = xml_Document.getElementsByTagName("path");
			
			for (var i=0;i<paths.length;i++){
				
				id = paths[i].getElementsByTagName("id")[0].firstChild.data;
				titulua="";
				if (paths[i].getElementsByTagName("titulua")[0].firstChild){
					titulua = paths[i].getElementsByTagName("titulua")[0].firstChild.data;
				}
				deskribapena="";
				if (paths[i].getElementsByTagName("deskribapena")[0].firstChild){
					deskribapena = paths[i].getElementsByTagName("deskribapena")[0].firstChild.data;
				}
				irudia = "";
				if (paths[i].getElementsByTagName("irudia")[0].firstChild){
					irudia = paths[i].getElementsByTagName("irudia")[0].firstChild.data;
				}
				add_path_to_list(id,titulua,deskribapena,irudia);
			}                                 
        }
    }
	
}

function add_path_to_list(id,titulua,deskribapena,irudia){
	
	var ibilbideak_div = document.getElementById("nire_ibilbideak");
    
    var p = document.createElement('p');
    
    var a = document.createElement('a');
	var linkText = document.createTextNode(titulua);
	a.appendChild(linkText);
	a.title = titulua;
	a.href = "editatu_ibilbidea?id="+id;
	ibilbideak_div.appendChild(p);
	ibilbideak_div.appendChild(a);
    
    
}


//pantailaren albo batean Ibilbide bozkatuenak kargatzeko
function load_most_voted_paths(){
	var paths_list_container = document.getElementById("ibilbide_bozkatuenak");
	if (paths_list_container){
		//ajax deia, kargatu kontainerrean zerrenda
		load_most_voted_paths_request(paths_list_container);
	}
}




function load_most_voted_paths_request(paths_list_container)
{
	
	var csrftoken = getCookie('csrftoken');
	var xmlHttp = createXmlHttpRequestObject();
	
	if (xmlHttp.readyState == 4 || xmlHttp.readyState == 0){ 
		
		$.ajaxSetup({
   			beforeSend: function(xhr, settings) {
       		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
           		xhr.setRequestHeader("X-CSRFToken", csrftoken);
       		}
   		 	}
		});
        xmlHttp.open("POST","../ajax_lortu_most_voted_paths",true);
        xmlHttp.onreadystatechange = function (){
            load_most_voted_paths_answer(xmlHttp,paths_list_container);                                                                   // Erantzuna jasotzean exekutatuko den deia
        };
        xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlHttp.send("csrfmiddlewaretoken=" + csrftoken);     // Eskaera bidali
    }
}

function load_most_voted_paths_answer(xmlHttp,paths_list_container)
{
	//alert("load_most_voted_paths_answer");	
	if (xmlHttp.readyState == 4){
        if(xmlHttp.status == 200){
			var xml_answer = xmlHttp.responseXML;
			var xml_Document = xml_answer.documentElement;
			var paths = xml_Document.getElementsByTagName("path");
			
			
			for (var i=0;i<paths.length;i++){
				
				id = paths[i].getElementsByTagName("id")[0].firstChild.data;
				
				titulua="";
				
				if (paths[i].getElementsByTagName("titulua")[0].firstChild){
					titulua = paths[i].getElementsByTagName("titulua")[0].firstChild.data;
														
				}
				/*
				deskribapena="";
				if (paths[i].getElementsByTagName("deskribapena")[0].firstChild){
					deskribapena = paths[i].getElementsByTagName("deskribapena")[0].firstChild.data;
				}
				irudia = "";
				if (paths[i].getElementsByTagName("irudia")[0].firstChild){
					irudia = paths[i].getElementsByTagName("irudia")[0].firstChild.data;
				}
				*/
				
				add_most_voted_path_to_list(id,titulua);
			}                                 
        }
    }
	
}

function add_most_voted_path_to_list(id,titulua){
	
	
	
	var ibilbideak_div = document.getElementById("ibilbide_bozkatuenak");
    
    var p = document.createElement('p');
    
    var a = document.createElement('a');
   
	var linkText = document.createTextNode(titulua);
	a.appendChild(linkText);
	
	a.title = titulua;
	a.href = "nabigazioa_hasi?path_id="+id;
	ibilbideak_div.appendChild(p);
	ibilbideak_div.appendChild(a);
    
    
}

//pantailaren albo batean eguneko itema erakusteko

function load_eguneko_itema()
{
	
	var eguneko_itema_container = document.getElementById("eguneko_itema");
	if (eguneko_itema_container){
		//ajax deia, kargatu kontainerrean zerrenda
		
		load_eguneko_itema_request(eguneko_itema_container);
	}
}
	
function load_eguneko_itema_request(eguneko_itema_container)
{
		
	var csrftoken = getCookie('csrftoken');
	var xmlHttp = createXmlHttpRequestObject();
	
	if (xmlHttp.readyState == 4 || xmlHttp.readyState == 0){ 
		
		$.ajaxSetup({
   			beforeSend: function(xhr, settings) {
       		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
           		xhr.setRequestHeader("X-CSRFToken", csrftoken);
       		}
   		 	}
		});
        xmlHttp.open("POST","../ajax_lortu_eguneko_itema",true);
        xmlHttp.onreadystatechange = function (){
            load_eguneko_itema_answer(xmlHttp,eguneko_itema_container);                                                                   // Erantzuna jasotzean exekutatuko den deia
        };
        xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlHttp.send("csrfmiddlewaretoken=" + csrftoken);     // Eskaera bidali
    }
}

function load_eguneko_itema_answer(xmlHttp,eguneko_itema_container)
{
	
	if (xmlHttp.readyState == 4){
		
        if(xmlHttp.status == 200){
        
			var xml_answer = xmlHttp.responseXML;
			var xml_Document = xml_answer.documentElement;
			var items = xml_Document.getElementsByTagName("item");
			
			
			//Eguneko item bat baino gehiago daudenean, random bidez aukeratu zein kargatu
			var randomNum = Math.floor(Math.random() * items.length);
			
			
			id = items[randomNum].getElementsByTagName("id")[0].firstChild.data;
			titulua = items[randomNum].getElementsByTagName("titulua")[0].firstChild.data;
			irudia = items[randomNum].getElementsByTagName("irudia")[0].firstChild.data;
			
			add_eguneko_itema_to_list(id,titulua,irudia);
			/*
			for (var i=0;i<items.length;i++){
				
				id = items[i].getElementsByTagName("id")[0].firstChild.data;
				
				titulua="";
				
				if (items[i].getElementsByTagName("titulua")[0].firstChild){
					titulua = items[i].getElementsByTagName("titulua")[0].firstChild.data;
														
				}
				irudia="";
				if (items[i].getElementsByTagName("irudia")[0].firstChild){
					irudia = items[i].getElementsByTagName("irudia")[0].firstChild.data;
														
				}
			
				
				add_eguneko_itema_to_list(id,titulua,irudia);
			} 
			*/                                
        }
    }
	
}

function add_eguneko_itema_to_list(id,titulua,irudia){
	
	
	//Random-a inplementatu
	var eguneko_itema_div = document.getElementById("eguneko_itema");
    
    var p = document.createElement('p');
    
    var a = document.createElement('a');
    
    var img = document.createElement("img");
	img.setAttribute("src", irudia);
   
	//var linkText = document.createTextNode(titulua);
	//a.appendChild(linkText);
	a.appendChild(img);
	//a.title = titulua;
	a.href = "erakutsi_item?id="+id;
	eguneko_itema_div.appendChild(p);
	eguneko_itema_div.appendChild(a);
    
    
}


function load_ws()
{
	
	load_ws_request();	
}

function load_ws_request(){
	
	
	var csrftoken = getCookie('csrftoken');
	var xmlHttp = createXmlHttpRequestObject();
	
	if (xmlHttp.readyState == 4 || xmlHttp.readyState == 0){ 
		
		$.ajaxSetup({
   			beforeSend: function(xhr, settings) {
       		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
           		xhr.setRequestHeader("X-CSRFToken", csrftoken);
       		}
   		 	}
		});
        xmlHttp.open("POST","../ajax_load_ws",true);
        xmlHttp.onreadystatechange = function (){
            load_ws_answer(xmlHttp);                                                                   // Erantzuna jasotzean exekutatuko den deia
        };
        xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        //xmlHttp.send("user_id=" + user_id +"&ws_id="+ ws_id + "&csrfmiddlewaretoken=" + csrftoken);
        xmlHttp.send("csrfmiddlewaretoken=" + csrftoken);                       // Eskaera bidali
    }
}

function load_ws_answer(xmlHttp){
	  if (xmlHttp.readyState == 4){
        if(xmlHttp.status == 200){
			var xml_answer = xmlHttp.responseXML;
			var xml_Document = xml_answer.documentElement;
			var items = xml_Document.getElementsByTagName("item");
			for (var i=0;i<items.length;i++){
				id = items[i].getElementsByTagName("id")[0].firstChild.data;
				titulua = items[i].getElementsByTagName("titulua")[0].firstChild.data;
				irudia = items[i].getElementsByTagName("irudia")[0].firstChild.data;
				//irudia hutsa baldin bada, defektuzkoa pasa
				if (irudia =="None")
				{
					irudia="/home/maddalen/Documents/Aptana Studio 3 Workspace/KULTURBIDEAK/src/KULTURBIDEAK/kulturbideak_app/media/uploads/NoIrudiItem.png";
				}
				add_workspace_box(id,titulua,irudia);
			}                                 
        }
    }
	
}

function allowDrop(ev) {
    ev.preventDefault();
}

//CSRF tokena kontrolatzeko funtzioak
// using jQuery :::csrftoken-a lortzeko
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}




function remove_me(element,item_id){
	//AJAX-HASI	
	start_loader("loader");
	create_remove_me_request(element,item_id);                                       	                                                           
	stop_loader("loader");                                                  
	
    //element.parentNode.removeChild(element);
}


function add_me_to_the_SVG(element,item_id){
if (document.getElementById("path_boxes").children[0].children[0].innerHTML == "Created with Raphaël 2.1.2"){
	document.getElementById("path_boxes").removeChild(document.getElementById("path_boxes").childNodes[0]);
	if (data.length == 0){
			var root = {"id":0 ,"name" : "ROOT" , "irudia": "http://obprototipoa.elhuyar.eus/uploads/festivalCineDonostia.jpeg", "parent":'' }
			data.push(root);
	}
	var id = element.id.substring(7,element.id.length);
	var irudia = element.children[2].src;
	var titulua = element.children[3].firstChild.data;
	var svg = document.getElementById("path_boxes").children;
	var obj={id: id, name: titulua , irudia: irudia, parent:0};
	data.push(obj);
	sortu(data);//funtzio hau d3ondarebideaksortu.js barruan dago.
	remove_me(element,item_id);
} else {
	var id = element.id.substring(7,element.id.length);
	var irudia = element.children[2].src;
	var titulua = element.children[3].firstChild.data;
	var svg = document.getElementById("path_boxes").children;
	var obj={id: id, name: titulua , irudia: irudia, parent:0};
	data.push(obj);
	sortu(data);
	remove_me(element,item_id);
	document.getElementById("path_boxes").removeChild(document.getElementById("path_boxes").childNodes[0]);

}
}


//create workspace_box request
function create_remove_me_request(element,item_id)
{
	//var csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	var csrftoken = getCookie('csrftoken');
	var xmlHttp = createXmlHttpRequestObject();
	
	if (xmlHttp.readyState == 4 || xmlHttp.readyState == 0){ 
		
		$.ajaxSetup({
   			beforeSend: function(xhr, settings) {
       		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
           		xhr.setRequestHeader("X-CSRFToken", csrftoken);
       		}
   		 	}
		});
		
        xmlHttp.open("POST","../ajax_workspace_item_borratu",true);
        xmlHttp.onreadystatechange = function (){
            create_remove_me_answer(xmlHttp,element);                                                                   
        };
        xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlHttp.send("item_id=" + item_id  + "&csrfmiddlewaretoken=" + csrftoken);                     
    }
	
	
}

//create remove_me answer
function create_remove_me_answer(xmlHttp,element){
    if (xmlHttp.readyState == 4){
        if(xmlHttp.status == 200){
    		var item_id = server_answer(xmlHttp);
            if (item_id){ 
            	element.parentNode.removeChild(element);           	
			}
			else{                                                                                               // Jaso beharreko emaitza lortu ez bada, errorea
				//show_message("default_error"); //AURRERAGO DIALOG BOX BAT adibidez
				alert ("default error");
			}
			stop_loader("loader");                                                                              // Emaitza ona edo txarra jaso bada, loaderra paratu
        }
    }
}

//workspace funtzioak
function toggle_workspace(){
	//Datu-basetik kargatu item-ak
	var ws = document.getElementById("workspace_boxes");
    if (ws.getAttribute("class") == "open"){
        ws.setAttribute("class","close");
    }
    else{
        ws.setAttribute("class","open");
    }
}

function create_workspace_box(index,user_id){
   	el_counter++;
    var item_id = document.getElementById("item_id_"+index).value;
    var titulua = document.getElementById("titulua_"+index).value;	
    var irudia = document.getElementById("irudia_"+index).value;
    
    //Titulua garbitu eta laburtu
    titulua=titulua.replace('<div class=\"titulu_es\">', ' ');
    titulua=titulua.replace('</div>', ' ');
    titulua=titulua.replace('<div class=\"titulu_en\">', ' ');
    titulua=titulua.replace('</div>', ' ');
    titulua=titulua.replace('<div class=\"titulu_eu\">', ' ');
    titulua=titulua.replace('</div>',' ');
    titulua=titulua.replace('<div class=\"titulu_lg\">', ' ');
    titulua=titulua.replace('</div>',' ');
   
    titulua_subs = titulua.substr(0, 20);  
    titulua = titulua_subs + "...";
    
    
    if (irudia == "" || irudia == "None"){
    	irudia="/uploads/NoIrudiItem.png";
   	}
    //Ondoren user id-aren arabera WS-id-a lortu
   	
    //var fk_workspace_id=user_id;  //EZ DAGO ONDO
    var uri="uri_"+item_id;
    var dc_source="Euskomedia";
    var dc_title=titulua;
    var dc_description="description";
    var type="argazkia";
    var paths_thumbnail=irudia;
   	//  workspace_item taula:item_id, item_uri, ws_id, item_dc_source, item_dc_title, item_dc_descriptioon, type, thumnail
  	
  	//AJAX
  	start_loader("loader");                             
	if (item_id.value != ""){		                                       
		create_workspace_box_request(item_id,uri,dc_source,dc_title,dc_description,type,paths_thumbnail);                                       //request!
	}
	else{                                                                                                       // baldintzak bete ez badira
		show_message("empty_workspace_box_error");                                                                  // (aukeran) errorea 
	stop_loader("loader");                                                                                      // loaderra gelditu
	}
   
	
    //add_workspace_box(item_id,titulua,irudia);
}



//create workspace_box request
function create_workspace_box_request(item_id,uri,dc_source,dc_title,dc_description,type,paths_thumbnail)
{
//var csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	var csrftoken = getCookie('csrftoken');
	var xmlHttp = createXmlHttpRequestObject();
	
	if (xmlHttp.readyState == 4 || xmlHttp.readyState == 0){ 
		
		$.ajaxSetup({
   			beforeSend: function(xhr, settings) {
       		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
           		xhr.setRequestHeader("X-CSRFToken", csrftoken);
       		}
   		 	}
		});
		
        xmlHttp.open("POST","../ajax_workspace_item_gehitu",true);
        xmlHttp.onreadystatechange = function (){
            create_workspace_box_answer(xmlHttp,item_id,dc_title,paths_thumbnail);                                                                   
        };
        xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlHttp.send("item_id="+item_id+ "&uri=" + uri + "&dc_source=" + dc_source + "&dc_title=" + dc_title + "&dc_description=" + dc_description + "&type=" + type + "&paths_thumbnail=" + paths_thumbnail + "&csrfmiddlewaretoken=" + csrftoken);                     
    }
	
	
}
//create workspace box answer
function create_workspace_box_answer(xmlHttp,item_id,titulua,irudia){
    
    if (xmlHttp.readyState == 4){
        if(xmlHttp.status == 200){
    		var item_id_server = server_answer(xmlHttp);
    		
            if (item_id_server){ 
            	
            	//Datu-basean sartu den Id-a nahi dut
            	add_workspace_box(item_id,titulua,irudia);
			}
			else{                                                                                               // Jaso beharreko emaitza lortu ez bada, errorea
				//show_message("default_error"); //AURRERAGO DIALOG BOX BAT adibidez
				alert ("default error");
			}
			stop_loader("loader");                                                                              // Emaitza ona edo txarra jaso bada, loaderra paratu
        }
    }
}

function add_workspace_box(box_id,text_value,image_value){
	
	
	var ws = document.getElementById("workspace_boxes");
    
    var ws_box = document.createElement("div");
    ws_box.setAttribute("id","ws_box_" + box_id);
    //ws_box.setAttribute("id", box_id); //aldaketa
    ws_box.setAttribute("class","ws_box");
    ws_box.setAttribute("draggable","true");
    ws_box.addEventListener('dragstart',drag);
    ws_box.addEventListener('dragenter',wsb_handleDragEnter);
    ws_box.addEventListener('dragleave',wsb_handleDragLeave);

    var wsb_button = document.createElement("span");
    wsb_button.setAttribute("class","wsb_button");
    wsb_button.setAttribute("onclick","remove_me(this.parentNode,"+box_id+");");
    wsb_button.appendChild(document.createTextNode("Ezabatu"));
    ws_box.appendChild(wsb_button);
    
    if (new RegExp("sortu_ibilbidea$").test(window.location.href) == true){
    	var wsb_button2 = document.createElement("span");
	    wsb_button2.setAttribute("class","wsb_button");
	    wsb_button2.setAttribute("onclick","add_me_to_the_SVG(this.parentNode,"+box_id+");");
	    wsb_button2.appendChild(document.createTextNode("Arbelera"));
	    ws_box.appendChild(wsb_button2);
    } else {  
    }
    var wsb_image = document.createElement("img");
    wsb_image.setAttribute("class","wsb_image");
    wsb_image.setAttribute("src",image_value);
    ws_box.appendChild(wsb_image);

    var wsb_title = document.createElement("span");
    wsb_title.setAttribute("class","wsb_title");
    wsb_title.appendChild(document.createTextNode(text_value));
    ws_box.appendChild(wsb_title);

    ws.appendChild(ws_box);
}


function ws_drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("id");
    var source = document.getElementById(data);
    if (source){
        if (ev.target.id == "workspace_boxes"){
            ev.target.appendChild(source);
        }
        else if (ev.target.classList.contains("ws_box")){
            ev.target.classList.remove('ws_box_over');
            ev.target.parentNode.insertBefore(source,ev.target.nextElementSibling);
        }
    }
}

function drag(ev) {
    ev.dataTransfer.setData("id", ev.target.id);
}

function wsb_handleDragEnter(ev) {
    ev.preventDefault();
    if (ev.target.classList){
        ev.target.classList.add('ws_box_over');
    }
}

function wsb_handleDragLeave(ev) {
    if (ev.target.classList){
        ev.target.classList.remove('ws_box_over');
    }
}

//path box funtzioak




/*
Ajax bidez irudi bat igotzeko adibidea da beheko jQuery-a. sortu_ibilbidea.html-etik deitzen da
 */
/*
$(document).ready(function(){
$('#form').submit(function(e) {

   var form = $(this);        
   var formdata = false;
   if(window.FormData){
     formdata = new FormData(form[0]);
                   
     }

   var formAction = form.attr('action');

                $.ajax({
                    type        : 'POST',
                    url         : '../ajax_path_irudia_gorde_proba',
                    cache       : false,
                    data        : formdata ? formdata : form.serialize(),
                    contentType : false,
                    processData : false,

                    success: function(response) {
                        if(response != 'error') {
                            //$('#messages').addClass('alert alert-success').text(response);
                            // OP requested to close the modal
                           
                             $('#myModal').modal('hide');
                        } else {
                            $('#messages').addClass('alert alert-danger').text(response);
                        }
                    }
                });
                e.preventDefault();
            });
   
});
*/

$(document).ready(function(){
$('#form2').submit(function(e) {

   var form = $(this);      
   var formdata = false;
   if(window.FormData){
     formdata = new FormData(form[0]);
                   
     }

   var formAction = form.attr('action');

                $.ajax({
                    type        : 'POST',
                    url         : '../ajax_path_irudia_gorde',
                    cache       : false,
                    data        : formdata ? formdata : form.serialize(),
                    contentType : false,
                    processData : false,

                    success: function(response) {
                        if(response != 'error') {
                            //$('#messages').addClass('alert alert-success').text(response);
                            // OP requested to close the modal
                            
                            //GAINONTZEKO METADATUAK GORDE : TITULUA, GAIA, DESK
                           create_path_on_db();
                           
                           //$('#myModal').modal('hide');
                        } else {
                            $('#messages').addClass('alert alert-danger').text(response);
                        }
                    }
                });
                e.preventDefault();
            });
   
});

//Ibilbidea eguneratzean irudia gordetzeko
$(document).ready(function(){
	
$('#formEguneratu').submit(function(e) {
 


   var path_id = document.getElementById("path_id").value;
   var form = $(this);  
   var formdata = false;
   if(window.FormData){
     formdata = new FormData(form[0]);                   
     }

   var formAction = form.attr('action');

                $.ajax({
                    type        : 'POST',
                    url         : '../ajax_path_irudia_eguneratu',
                    cache       : false,
                    data        : formdata ? formdata : form.serialize(),
                    contentType : false,
                    processData : false,

                    success: function(response) {
                        if(response != 'error') {
                            //$('#messages').addClass('alert alert-success').text(response);
                            // OP requested to close the modal
                            
                            //GAINONTZEKO METADATUAK GORDE : TITULUA, GAIA, DESK,HIZK
                           update_path_on_db(path_id);
                           
                           //$('#myModal').modal('hide');
                        } else {
                            $('#messages').addClass('alert alert-danger').text(response);
                        }
                    }
                });
                e.preventDefault();
            });
   
});

/*
 * 
 * IBILBIDEA SORTZEKO FUNTZIOAK
 * 
 */


function create_path_on_db()
{
		
	var dc_title = document.getElementById("path_titulua").value;
	var dc_description = document.getElementById("path_desk").value;
	var dc_subject = document.getElementById("path_gaia").value;
	var paths_thumbnail = document.getElementById("file2");
	var paths_thumbnail_name=paths_thumbnail.value;
	var hizkuntza =document.getElementById("hizkuntza").value;
	
	//alert(paths_thumbnail_name);
	
	start_loader("loader");  
	
	uri="urii";
   
    //paths_thumbnail = "";   //MEDIA_URL+edm_object           , parametro bezala pasa MEDIA_URL                                                                             // beharrezko baldintzak jaso
	
	//if (paths_starts.length > 0){
		                                            
		create_path_on_db_request(uri,dc_title,dc_subject,dc_description,paths_thumbnail_name,hizkuntza);                                  
	//}
	//else{                                                                                                       // baldintzak bete ez badira
		//alert("empty_path_error");                                                                  // (aukeran) errorea 
	//}
	stop_loader("loader");                                                                                      // loaderra gelditu

}

function create_path_on_db_request(uri,dc_title,dc_subject,dc_description,paths_thumbnail_name,hizkuntza)
{
	
	var csrftoken = getCookie('csrftoken');
	var xmlHttp = createXmlHttpRequestObject();
	
	if (xmlHttp.readyState == 4 || xmlHttp.readyState == 0){ 
		
		$.ajaxSetup({
   			beforeSend: function(xhr, settings) {
       		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
           		xhr.setRequestHeader("X-CSRFToken", csrftoken);
       		}
   		 	}
		});
		
        xmlHttp.open("POST","../ajax_path_berria_gorde",true);
        xmlHttp.onreadystatechange = function (){
            create_path_on_db_answer(xmlHttp);                                                                   
        };
        
       
     
        xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlHttp.send("uri="+uri+"&dc_title="+dc_title+"&dc_subject="+dc_subject+"&dc_description="+dc_description+"&paths_thumbnail="+paths_thumbnail_name+"&hizkuntza="+hizkuntza+"&csrfmiddlewaretoken=" + csrftoken);                     
    }
	
}


function create_path_on_db_answer(xmlHttp)
{
	if (xmlHttp.readyState == 4){
        if(xmlHttp.status == 200){
    		var path_id = server_answer(xmlHttp);
            if (path_id){ 
            
            	//ORAIN NODE TAULA EGUNERATU
            	create_path_nodes(path_id);
            	
            	//add_workspace_box(item_id,titulua,irudia);
			}
			else{                                                                                               // Jaso beharreko emaitza lortu ez bada, errorea
				//show_message("default_error"); //AURRERAGO DIALOG BOX BAT adibidez
				alert ("default error");
			}
			stop_loader("loader");                                                                              // Emaitza ona edo txarra jaso bada, loaderra paratu
        }
    }
	
}

function create_path_nodes(path_id)
{

    var json = [];
	if (root.children.length>-1){
		for (var i=0;i<root.children.length;i++){	
	   	var obj={id: root.children[i].id, name: root.children[i].name , irudia: root.children[i].irudia , narrazioa: root.children[i].narrazioa ,  parent:root.children[i].parent.id , children:root.children[i].children};
	   	json.push(obj);
	   	   	if (root.children[i].children == undefined){
	   	   	} else if (root.children[i].children.length>-1){
	   	   		for (var b=0;b<root.children[i].children.length;b++){
	   		   	var obj2={id: root.children[i].children[b].id, name: root.children[i].children[b].name , narrazioa: root.children[i].children[b].narrazioa , irudia: root.children[i].children[b].irudia, parent:root.children[i].children[b].parent.id,children:root.children[i].children[b].children};
	   	   		json.push(obj2);
	   	   			if (root.children[i].children[b].children == undefined){
	   	   			} else if (root.children[i].children[b].children.length>-1){
	   	   				for (var c=0;c<root.children[i].children[b].children.length;c++){
			   		   	var obj3={id: root.children[i].children[b].children[c].id, name: root.children[i].children[b].children[c].name , narrazioa: root.children[i].children[b].children[c].narrazioa , irudia: root.children[i].children[b].children[c].irudia, parent:root.children[i].children[b].children[c].parent.id,children:root.children[i].children[b].children[c].children};
	   	   				json.push(obj3);
	   	   					if (root.children[i].children[b].children[c].children == undefined){
	   	   					} else if (root.children[i].children[b].children[c].children.length>-1){
	   	   						for (var d=0;d<root.children[i].children[b].children[c].children.length;d++){
	   	   							var obj4={id: root.children[i].children[b].children[c].children[d].id, name: root.children[i].children[b].children[c].children[d].name , narrazioa: root.children[i].children[b].children[c].children[d].narrazioa , irudia: root.children[i].children[b].children[c].children[d].irudia, parent:root.children[i].children[b].children[c].children[d].parent.id,children:root.children[i].children[b].children[c].children[d].children};
	   	   							json.push(obj4);
	   	   						}
	   	   					}
	   	   				}
	   	   			}//if (root.children[i].children[b].children.length>-1){

	   	   		}//for (var b=0;b<root.children[i].children.length;b++){
	    	} else {

	    	}//if (root.children[i].children.length>-1){
		}//for (var i=0;i<root.children.length;i++){
	} else {
	}//if (root.children.length>-1){  

	//for bat semeak zein diren jakiteko eta semeen array-a string batean bihurtzen du..

	for (var i=0;i<json.length;i++){
		if (json[i].children == undefined){
		} else {
			var zenbat = json[i].children.length;
			for (var z=0;z<zenbat;z++){
				json[i].children.push(json[i].children[z].id);
			}
			json[i].children.splice(0,zenbat);
		}
	}
	//console.log(json);

	//NODE BAKOITZEKO
	start_loader("loader");
	//Erroak
	for(var i = 0; i < json.length; i++) {
		if (json[i].parent.id == 0){
			paths_starts.push(json[i]);
		}
		
	}
	//Erroak
	var nodes = paths_starts;
	for(var i = 0; i < json.length; i++) {
		var item_id= json[i].id;
		var uri="uri_"+json[i].id;
		var dc_source="Euskomedia";
		//var dc_description="desc";
		var type ="argazkia";
		var paths_thumbnail=json[i].irudia;
		
		//MAD
		var dc_description=json[i].narrazioa;
		
		if (json[i].parent == 0){
			var paths_prev = "pb_"; //ez dauka aitarik, bera da aita nagusia
			var paths_start = 1; //root da
		} else {
			var paths_prev = "pb_"+json[i].parent; //
			var paths_start = 0; //ez da root 
		}
		var dc_title =json[i].name;
			if (json[i].children == undefined){
				var semeak = '';
				var paths_next = 'pb_';
			} else {
				var semeak =json[i].children;
				var paths_next=json[i].children.join();
				nodes = nodes.concat(semeak);
			}		
		create_path_nodes_request(path_id,item_id,uri,dc_source,dc_title,dc_description,type,paths_thumbnail,paths_prev,paths_next,paths_start);
		//nodes = nodes.concat(semeak);
	}

	stop_loader("loader");           
}


function create_path_nodes_request(path_id,item_id,uri,dc_source,dc_title,dc_description,type,paths_thumbnail,paths_prev,paths_next,paths_start)
{
	
	var csrftoken = getCookie('csrftoken');
	var xmlHttp = createXmlHttpRequestObject();
	
	if (xmlHttp.readyState == 4 || xmlHttp.readyState == 0){ 
		
		$.ajaxSetup({
   			beforeSend: function(xhr, settings) {
       		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
           		xhr.setRequestHeader("X-CSRFToken", csrftoken);
       		}
   		 	}
		});
		
        xmlHttp.open("POST","../ajax_path_node_gorde",true);
        xmlHttp.onreadystatechange = function (){
            create_path_node_answer(xmlHttp);                                                                   
        };
      
        xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlHttp.send("path_id="+path_id+"&item_id="+item_id.replace("pb_","")+"&uri="+uri+"&dc_source="+dc_source+"&dc_title="+dc_title+"&dc_description="+dc_description+"&type="+type+"&paths_thumbnail="+paths_thumbnail+"&paths_prev="+paths_prev.replace("pb_","")+"&paths_next="+paths_next.replace("pb_","")+"&paths_start="+paths_start+"&csrfmiddlewaretoken=" + csrftoken); 																																			

    }
}

function create_path_node_answer(xmlHttp)
{
	
	if (xmlHttp.readyState == 4){
        if(xmlHttp.status == 200){
    		var path_node_id = server_answer(xmlHttp);
            if (path_node_id){
            	//alert ("gorde da nodea:"+path_node_id);
            	//console.log("gorde da nodea:"+path_node_id);
            	
            	
            	//leiho modaleko botoia desgaitu
            	//document.getElementById("botSortu").setAttribute("disabled","disabled");
            	//leiho modaletik irten
            	//jQuery.noConflict();
               	$('#modalwindow').modal('hide'); //JQUERY      	
            	//pantaila nagusiko botoia desgaitu
            	document.getElementById("create_path_button").setAttribute("disabled","disabled");
            	
			}
			else{                                                                                               // Jaso beharreko emaitza lortu ez bada, errorea
				//show_message("default_error"); //AURRERAGO DIALOG BOX BAT adibidez
				alert ("default error");
			}
			stop_loader("loader");                                                                              // Emaitza ona edo txarra jaso bada, loaderra paratu
        }
    }
}


/*
 * IBILBIDEA EGUNERATZEKO FUNTZIOAK
 * 
 */

function update_path_on_db(path_id)
{
	
	var dc_title = document.getElementById("path_titulua").value;
	var dc_description = document.getElementById("path_desk").value;
	var dc_subject = document.getElementById("path_gaia").value;
	var paths_thumbnail = document.getElementById("file2");
	var paths_thumbnail_name=paths_thumbnail.value;	
	var hizkuntza =document.getElementById("hizkuntza").value;
	
	
	
	start_loader("loader");
	//if (paths_starts.length > 0){		                                            
		update_path_on_db_request(path_id,dc_title,dc_subject,dc_description,paths_thumbnail_name,hizkuntza);                                  
	//}
	//else{                                                                                                      
	//	alert("empty_path_error");                                                                
	//}
	//stop_loader("loader");   
}

function update_path_on_db_request(path_id,dc_title,dc_subject,dc_description,paths_thumbnail_name,hizkuntza)
{
	var csrftoken = getCookie('csrftoken');
	var xmlHttp = createXmlHttpRequestObject();
	
	if (xmlHttp.readyState == 4 || xmlHttp.readyState == 0){ 
		
		$.ajaxSetup({
   			beforeSend: function(xhr, settings) {
       		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
           		xhr.setRequestHeader("X-CSRFToken", csrftoken);
       		}
   		 	}
		});
		
        xmlHttp.open("POST","../ajax_path_eguneratu",true);
        xmlHttp.onreadystatechange = function (){
            update_path_on_db_answer(xmlHttp,path_id);                                                                   
        };
      
        xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlHttp.send("path_id="+path_id+"&dc_title="+dc_title+"&dc_subject="+dc_subject+"&dc_description="+dc_description+"&paths_thumbnail="+paths_thumbnail_name+"&hizkuntza="+hizkuntza+"&csrfmiddlewaretoken=" + csrftoken);                     
    }
	
}


function update_path_on_db_answer(xmlHttp,path_id)
{
	if (xmlHttp.readyState == 4){
        if(xmlHttp.status == 200){
    		var path_id = server_answer(xmlHttp);
            if (path_id){ 
            
            	//ORAIN NODE TAULA EGUNERATU
            	update_path_nodes(path_id);
            	
            	
			}
			else{                                                                                               // Jaso beharreko emaitza lortu ez bada, errorea
				//show_message("default_error"); //AURRERAGO DIALOG BOX BAT adibidez
				alert ("default error");
			}
			stop_loader("loader");                                                                              // Emaitza ona edo txarra jaso bada, loaderra paratu
        }
    }
	
}


/* Ibilbidea eguneratzean, ibilbideko nodo bakoitzaren eguneraketa burutzen da ajax bidez jarraian
 dauden funtzioekin */

function update_path_nodes(path_id)
{
	//zuhaitza , json formatura pasa.
   var root = treeData[0];
   var json = [];

if (root.children.length>-1){
	console.log(0);
	for (var i=0;i<root.children.length;i++){	
   	var obj={id: root.children[i].id, name: root.children[i].name , irudia: root.children[i].irudia , narrazioa: root.children[i].narrazioa ,  parent:root.children[i].parent.id , children:root.children[i].children};
   	json.push(obj);
   	   	if (root.children[i].children == undefined){
   	   		console.log(1);
   	   	} else if (root.children[i].children.length>-1){
   	   		for (var b=0;b<root.children[i].children.length;b++){
   		   	var obj2={id: root.children[i].children[b].id, name: root.children[i].children[b].name , narrazioa: root.children[i].children[b].narrazioa , irudia: root.children[i].children[b].irudia, parent:root.children[i].children[b].parent.id,children:root.children[i].children[b].children};
   	   		json.push(obj2);
   	   			if (root.children[i].children[b].children == undefined){
   	   				console.log(2);
   	   			} else if (root.children[i].children[b].children.length>-1){
   	   				for (var c=0;c<root.children[i].children[b].children.length;c++){
		   		   	var obj3={id: root.children[i].children[b].children[c].id, name: root.children[i].children[b].children[c].name , narrazioa: root.children[i].children[b].children[c].narrazioa , irudia: root.children[i].children[b].children[c].irudia, parent:root.children[i].children[b].children[c].parent.id,children:root.children[i].children[b].children[c].children};
   	   				json.push(obj3);
   	   					if (root.children[i].children[b].children[c].children == undefined){
   	   						console.log(3);
   	   					} else if (root.children[i].children[b].children[c].children.length>-1){
   	   						for (var d=0;d<root.children[i].children[b].children[c].children.length;d++){
   	   							var obj4={id: root.children[i].children[b].children[c].children[d].id, name: root.children[i].children[b].children[c].children[d].name , narrazioa: root.children[i].children[b].children[c].children[d].narrazioa , irudia: root.children[i].children[b].children[c].children[d].irudia, parent:root.children[i].children[b].children[c].children[d].parent.id,children:root.children[i].children[b].children[c].children[d].children};
   	   							json.push(obj4);
   	   							if (root.children[i].children[b].children[c].children[d].children == undefined){
   	   								console.log(4);
   	   							} else if (root.children[i].children[b].children[c].children[d].children.length>-1){
   	   								for (var e=0;e<root.children[i].children[b].children[c].children[d].length;e++){
   	   									var obj5={id: root.children[i].children[b].children[c].children[d].children[e].id, name: root.children[i].children[b].children[c].children[d].children[e].name , narrazioa: root.children[i].children[b].children[c].children[d].children[e].narrazioa , irudia: root.children[i].children[b].children[c].children[d].children[e].irudia, parent:root.children[i].children[b].children[c].children[d].children[e].parent.id,children:root.children[i].children[b].children[c].children[d].children[e].children};
   	   									console.log(obj5);
   	   									json.push(obj5);
   	   								}//for (var e=0;e<root.children[i].children[b].children[c].children[d].length;e++){
   	   							}//if (root.children[i].children[b].children[c].children[d].children.length>-1){
   	   						}//for (var d=0;d<root.children[i].children[b].children[c].children.length;d++){
   	   					}//if (root.children[i].children[b].children[c].children.length>-1){
   	   				}//for (var c=0;c<root.children[i].children[b].children.length;c++){
   	   			}//if (root.children[i].children[b].children.length>-1){

   	   		}//for (var b=0;b<root.children[i].children.length;b++){
    	} else {
    		console.log(6);
    	}//if (root.children[i].children.length>-1){
	}//for (var i=0;i<root.children.length;i++){
} else {
}//if (root.children.length>-1){


//for bat semeak zein diren jakiteko eta semeen array-a string batean bihurtzen du..

for (var i=0;i<json.length;i++){
	if (json[i].children == undefined){
	} else {
		var zenbat = json[i].children.length;
		for (var z=0;z<zenbat;z++){
			json[i].children.push(json[i].children[z].id);
		}
		json[i].children.splice(0,zenbat);
	}
}
//console.log(json);

	//NODE BAKOITZEKO
	start_loader("loader");
	//Erroak
	for(var i = 0; i < json.length; i++) {
		if (json[i].parent.id == 0){
			paths_starts.push(json[i]);
		}
		
	}
	var nodes = paths_starts;
	for(var i = 0; i < json.length; i++) {
		var item_id= json[i].id;
		var uri="uri_"+json[i].id;
		var dc_source="Euskomedia";
		var type ="argazkia";
		var paths_thumbnail=json[i].irudia;
		var dc_description=json[i].narrazioa;
		
		if (json[i].parent == 0){
			var paths_prev = "pb_"; //ez dauka aitarik, bera da aita nagusia
			var paths_start = 1; //root da
		} else {
			var paths_prev = "pb_"+json[i].parent; //
			var paths_start = 0; //ez da root 
		}
		var dc_title =json[i].name;
			if (json[i].children == undefined){
				var semeak = '';
				var paths_next = 'pb_';
			} else {
				var semeak =json[i].children;
				var paths_next=json[i].children.join();
				nodes = nodes.concat(semeak);
			}		
		update_path_nodes_request(path_id,item_id,uri,dc_source,dc_title,dc_description,type,paths_thumbnail,paths_prev,paths_next,paths_start);
		//nodes = nodes.concat(semeak);
	}

	stop_loader("loader");           
	
	

	
}
function update_path_nodes_request(path_id,item_id,uri,dc_source,dc_title,dc_description,type,paths_thumbnail,paths_prev,paths_next,paths_start)
{
	
	var csrftoken = getCookie('csrftoken');
	var xmlHttp = createXmlHttpRequestObject();
	
	if (xmlHttp.readyState == 4 || xmlHttp.readyState == 0){ 
		
		$.ajaxSetup({
   			beforeSend: function(xhr, settings) {
       		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
           		xhr.setRequestHeader("X-CSRFToken", csrftoken);
       		}
   		 	}
		});
		
        xmlHttp.open("POST","../ajax_path_node_eguneratu",true);
        xmlHttp.onreadystatechange = function (){
            update_path_node_answer(xmlHttp);                                                                   
        };
      
        xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
       // xmlHttp.send("path_id="+path_id+"&item_id="+item_id+"&uri="+uri+"&dc_source="+dc_source+"&dc_title="+dc_title+"&dc_description="+dc_description+"&type="+type+"&paths_thumbnail="+paths_thumbnail+"&paths_prev="+paths_prev+"&paths_next="+paths_next+"&paths_start="+paths_start+"&csrfmiddlewaretoken=" + csrftoken); 																																			
        xmlHttp.send("path_id="+path_id+"&item_id="+item_id.replace("pb_","")+"&uri="+uri+"&dc_source="+dc_source+"&dc_title="+dc_title+"&dc_description="+dc_description+"&type="+type+"&paths_thumbnail="+paths_thumbnail+"&paths_prev="+paths_prev.replace("pb_","")+"&paths_next="+paths_next.replace("pb_","")+"&paths_start="+paths_start+"&csrfmiddlewaretoken=" + csrftoken); 																																			
    }
}

function update_path_node_answer(xmlHttp)
{
	
	if (xmlHttp.readyState == 4){
        if(xmlHttp.status == 200){
    		var path_node_id = server_answer(xmlHttp);
            if (path_node_id){
            	//alert ("gorde da nodea:"+path_node_id);
            	//console.log("gorde da nodea:"+path_node_id);
            	
            	
            	//leiho modaleko botoia desgaitu
            	//document.getElementById("botSortu").setAttribute("disabled","disabled");
            	//leiho modaletik irten
               	 $('#modalwindow').modal('hide'); //JQUERY      	
            	//pantaila nagusiko botoia desgaitu
            	document.getElementById("update_path_button").setAttribute("disabled","disabled");
            	
			}
			else{                                                                                               // Jaso beharreko emaitza lortu ez bada, errorea
				//show_message("default_error"); //AURRERAGO DIALOG BOX BAT adibidez
				alert ("default error");
			}
			stop_loader("loader");                                                                              // Emaitza ona edo txarra jaso bada, loaderra paratu
        }
    }
}



//ibilbideak sortzeko arbela
function set_pb(){
    if (document.getElementById("path_boxes") && (document.getElementById("path_boxes").children.length == 0)){
        paper = Raphael(document.getElementById("path_boxes"), "100%", "100%");
    }
}
//Maddalen: hasierako pantailan eguneko ibilbidea marrazteko
function set_pb_egunekoa(){
    if (document.getElementById("path_boxes_egunekoa") && (document.getElementById("path_boxes_egunekoa").children.length == 0)){
        paper = Raphael(document.getElementById("path_boxes_egunekoa"), "100%", "100%");
    }
}
//Maddalen: Ibilbidearen eskema orokorra eta momentuko itema nabamenduta marrazteko
function set_pb_overview(){
    if (document.getElementById("path_boxes_overview") && (document.getElementById("path_boxes_overview").children.length == 0)){
        paper = Raphael(document.getElementById("path_boxes_overview"), "100%", "25%");
    }
}

function get_x(pos){
    return (pb_box_space + pos*(pb_box_space + pb_box_w));
}

function get_y(pos){
    return (pb_box_space + pos*(pb_box_space + pb_box_h));
}

function get_x_pos(x){
    return parseInt((x - pb_box_space)/(pb_box_space + pb_box_w));
}

function get_y_pos(y){
    return parseInt((y - pb_box_space)/(pb_box_space + pb_box_h));
}

function pb_drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("id");
    var source = document.getElementById(data);
    if ((ev.target.parentNode.id == "path_boxes") && source && source.getAttribute("class") == "ws_box") {
        var image_value = source.children[1].src;
        var text_value = source.children[2].firstChild.data;
        pb_new_element(data,text_value,image_value);
        //alert(data);//ws_box_1
        var item_id=data.replace("ws_box_", ""); 
        remove_me(source,item_id);
    }
}
//Maddalen
/*
function pb_drop_egunekoa(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("id");
    var source = document.getElementById(data);
    if ((ev.target.parentNode.id == "path_boxes_egunekoa") && source && source.getAttribute("class") == "ws_box") {
        var image_value = source.children[1].src;
        var text_value = source.children[2].firstChild.data;
        pb_new_element_egunekoa(data,text_value,image_value);
        //alert(data);//ws_box_1
        var item_id=data.replace("ws_box_", ""); 
        remove_me(source,item_id);
    }
}
*/
function pb_window_resize(){
    var svg = paper.canvas;
    var svgBBox = paper.canvas.getBBox();
    var container = svg.parentNode;
    if (svgBBox.height < container.offsetHeight){
        svg.style.height = (container.offsetHeight + pb_box_space) + "px";
    }
    else{
        svg.style.height = (svgBBox.height + (pb_box_space + pb_box_h)) + "px";
    }
    if (svgBBox.width < container.offsetWidth){
        svg.style.width = (container.offsetWidth + pb_box_space) + "px";
    }
    else{
        svg.style.width = (svgBBox.width + (pb_box_space + pb_box_w)) + "px";
    }

}

/*
Elementua sortu path box-ean
*/



function pb_new_element(data_id,text_value,image_value){
	//console.log("data_id:"+data_id);
	//console.log("text_value:"+text_value);
	//console.log("image_value:"+image_value);
	
    //kokapen berria aurkitu
    var y_position = 0;
    if (paths_starts.length > 0){
        y_position = get_new_y(paper.getById(paths_starts[paths_starts.length-1]));
    }

    var back_rect = paper.rect(get_x(0), get_y(y_position), pb_box_w,pb_box_h, 5);
    back_rect.node.setAttribute("class","pb_box_back");
    back_rect.id = data_id + "_back";

    //azpi elementuak sortu
    if (text_value.length > 15){
        text_value = text_value.substring(0,12) + "...";
    }
    var text = paper.text(get_x(0)+60, get_y(y_position)+100, text_value);
    text.id = data_id + "_title";
    text.node.setAttribute("class","pb_box_title");

    var image = paper.image(image_value, get_x(0)+10, get_y(y_position)+15, pb_box_w -20, pb_box_h - 50)
    image.id = data_id + "_image";
    image.node.setAttribute("class","pb_box_image");

    var rect = paper.rect(get_x(0), get_y(y_position), pb_box_w,pb_box_h, 5);
    rect.node.setAttribute("class","pb_box");
    
    //maddalen: Modal window-a zabaltzeko gehitu ditut ondorengo bi lerroak
    //rect.node.setAttribute("data-toggle","modal");
    //rect.node.setAttribute("data-target","#myModal");
    
    rect.id = data_id;
    //beharrezko informazioa hemen gorde
    rect.data("text_value",text_value);
    rect.data("image_value",image_value);
    //diagramaren kudeaketarako beharrezko balioak
    rect.data("parent_id",null);
    rect.data("children",[]);
    rect.drag(onmove, onstart, onend);
    paths_starts.push(rect.id);
    
    var delete_button = paper.text(get_x(0)+pb_box_w-10, get_y(y_position)+10, "X");
    delete_button.id = data_id + "_delete_button";
    delete_button.node.setAttribute("class","pb_box_delete_button");
    delete_button.data("id_value",data_id);
    delete_button.click(pb_remove_me);
    
    
    /*
    //NARRAZIOA GEHITZEKO  PROMT BIDEZ
  	rect.attr({
    cursor: 'pointer',
	}).dblclick(function(e) {
    
    //var path_item_description = document.getElementById("path_item_description").value;
  	//alert("pb_new_element:"+path_item_description);
    
    var path_item_description = prompt("Itemaren narrazioa:", "");
    rect.data("item_narrazioa",path_item_description);
	}); 
	*/
	
	// NARRAZIOA GEHITZEKO Klik bikoitzaz
	rect.attr({
    cursor: 'pointer',
	}).dblclick(function(e) {
    	
    	/*
  		var narra_div = document.getElementById("narrazioa");
        
    	var input = document.createElement("textarea");
		var button = document.createElement("button");
		input.name = "textarea";
		input.id = "narra_textarea";
		input.maxLength = "5000";
		input.cols = "87";
		input.rows = "5";
	
		narra_div.appendChild(input); //appendChild
		var t = document.createTextNode("Gorde");       // Create a text node
		button.appendChild(t);
		narra_div.appendChild(button);
	*/
	
			
		//document.getElementById("narra_textarea").setAttribute("disabled","false");
        //document.getElementById("narra_botoia").setAttribute("disabled","false");   
        
        document.getElementById("narra_p").innerHTML = "Momentuko itema: "+text_value;
        
        $("[name='narra_textarea']").prop("disabled", false);
        $("[name='narra_textarea']").prop("value", '');
		$("[name='narra_botoia']").prop("disabled", false);
		
		
		
		var button = document.getElementById("narra_botoia");
		
		button.onclick = function () {
  	  		var balioa=$.trim($("textarea").val());
  			
  			//Raphael-en rect-aaren data-n gorde
  			rect.data("item_narrazioa",balioa);
			
			//kendu pantailatik textArea eta botoia
			//DIV-a ez borratu!!!! document.getElementById('narra_textarea')
			//$('#narrazioa').remove();	
			
			document.getElementById("narra_textarea").setAttribute("disabled","disabled");
        	document.getElementById("narra_botoia").setAttribute("disabled","disabled");  
			
			//Path-eko nodo hau zelabait markatu narrazioa duela jakiteko
			
			/*
			paper.rect(get_x(0), get_y(y_position), pb_box_w,pb_box_h, 5).attr({
			//fill: "red", 
			stroke: "rgb(200,100,77)",
			"stroke-width": 5
			});*/
		};
	}); 
	
	//N botoia
/*
    var narra_button = paper.text(get_x(0)+pb_box_w-30, get_y(y_position)+10, "N");
    narra_button.id = data_id + "_narra_button";
    narra_button.node.setAttribute("class","pb_box_delete_button");
    narra_button.data("id_value",data_id);
    //narra_button.click(pb_narra_me);
    
    
    narra_button.click(function(e){
    	//pb_narra_me
    
    	var narra_div = document.getElementById("narrazioa");
        
    	var input = document.createElement("textarea");
		var button = document.createElement("button");
		input.name = "textarea";
		input.maxLength = "5000";
		input.cols = "87";
		input.rows = "5";
	
		narra_div.appendChild(input); //appendChild
		var t = document.createTextNode("Gorde");       // Create a text node
		button.appendChild(t);
		narra_div.appendChild(button);
	
		button.onclick = function () {
  	  		var balioa=$.trim($("textarea").val());
  			alert(balioa);
  			//Raphael-en rect-aaren data-n gorde
  			rect.data("item_narrazioa",balioa);
			
			//kendu pantailatik textArea eta botoia
			$('#narrazioa').remove();	
			
			//Path-eko nodo hau zelabait markatu narrazioa duela jakiteko
			
			
//			paper.rect(get_x(0), get_y(y_position), pb_box_w,pb_box_h, 5).attr({
			//fill: "red", 
//			stroke: "rgb(200,100,77)",
//			"stroke-width": 5
//			});
		};
    	
    });
    */
   
    pb_window_resize();
}

//Maddalen, aurreko funtzioaren kopia bat da, baina X botoia ez du sortzen ezta narrazioa
//Gainera, Ibilbideen nabigaziorako beahrrezkoa diren datuak gordeko ditugu .data-n: path_id

function pb_new_element_egunekoa(data_id,text_value,image_value,path_id,item_id){
	
	
    //kokapen berria aurkitu
    var y_position = 0;
    if (paths_starts.length > 0){
        y_position = get_new_y(paper.getById(paths_starts[paths_starts.length-1]));
    }

    var back_rect = paper.rect(get_x(0), get_y(y_position), pb_box_w,pb_box_h, 5);
    back_rect.node.setAttribute("class","pb_box_back");
    back_rect.id = data_id + "_back";

    //azpi elementuak sortu
    if (text_value.length > 15){
        text_value = text_value.substring(0,12) + "...";
    }
    var text = paper.text(get_x(0)+60, get_y(y_position)+100, text_value);
    text.id = data_id + "_title";
    text.node.setAttribute("class","pb_box_title");

    var image = paper.image(image_value, get_x(0)+10, get_y(y_position)+15, pb_box_w -20, pb_box_h - 50)
    image.id = data_id + "_image";
    image.node.setAttribute("class","pb_box_image");

    var rect = paper.rect(get_x(0), get_y(y_position), pb_box_w,pb_box_h, 5);
    rect.node.setAttribute("class","pb_box");
    
        
    rect.id = data_id;
    //beharrezko informazioa hemen gorde
    rect.data("text_value",text_value);
    rect.data("image_value",image_value);
    //diagramaren kudeaketarako beharrezko balioak
    rect.data("parent_id",null);
    rect.data("children",[]);
    
    //Nabigaziorako beharrezkoak diren datuak kargatu
    /*
    rect.data("path_id",path_id);
    rect.data("narrazioa",narrazioa);
    rect.data("hurrengoak_id",hurrengoak_id);
    rect.data("hasieraDa",hasieraDa);
    */
    //var node_id = data_id.replace("pb_", "");
    //rect.data("node_id",node_id);
    
    //rect.drag(onmove, onstart, onend); //MAddalen: ez utzi erabiltzaileari nodoak mugitzen
    paths_starts.push(rect.id);
    
    
    // NABIGAZIOA GEHITZEKO
	rect.attr({
    cursor: 'pointer',
	}).click(function(e) {
    	
    	
    	var url = 'nabigazio_item';
    	
    	//window.location.href=url; //get moduan bidaltzeko
		
		
		var form = $('<form action="' + url + '" method="post">' +
		//'<input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">'+
		'<input type="hidden" name="csrfmiddlewaretoken" value="'+ csrf_token+'">'+
  		'<input type="hidden" name="path_id" value="' + path_id + '" />'+
  		//'<input type="hidden" name="titulua" value="' + text_value + '" />'+
  		//'<input type="hidden" name="irudia" value="' + image_value + '" />'+
  		//'<input type="hidden" name="narrazioa" value="' + narrazioa + '" />'+
  		//'<input type="hidden" name="hurrengoak_id" value="' + hurrengoak_id + '" />'+
  		//'<input type="hidden" name="hasieraDa" value="' + hasieraDa + '" />'+
  		'<input type="hidden" name="item_id" value="' + item_id + '" />'+
 		 '</form>');
		$('body').append(form);
		form.submit();
    
   	});
   
    pb_window_resize();
}

////Hemen:pb_new_element_overview 
function pb_new_element_overview(data_id,text_value,path_id,item_id,nabarmentzeko_id)
{
	
	//kokapen berria aurkitu
    var y_position = 0;
    if (paths_starts.length > 0){
        y_position = get_new_y(paper.getById(paths_starts[paths_starts.length-1]));
    }
	//Maddalen: heigh-70, width-30
    var back_rect = paper.rect(get_x(0), get_y(y_position), pb_box_w-30,pb_box_h-70, 5);
    
    if (item_id==nabarmentzeko_id)
    {
    	back_rect.node.setAttribute("class","pb_box_back_nabarmendu");
    }
    else
    {
    	back_rect.node.setAttribute("class","pb_box_back_overview");
    }
    back_rect.id = data_id + "_back";

    //azpi elementuak sortu
    if (text_value.length > 15){
        text_value = text_value.substring(0,12) + "...";
    }
    //Maddalen:y+30
    var text = paper.text(get_x(0)+60, get_y(y_position)+30, text_value);
    text.id = data_id + "_title";
    text.node.setAttribute("class","pb_box_title");

	//Maddalen:heigh-70, width-30
    var rect = paper.rect(get_x(0), get_y(y_position), pb_box_w-30,pb_box_h-70, 5);
    rect.node.setAttribute("class","pb_box_overview");
    
    
    //MOMENTUKO NODEA NABARMENDU (BESTE KOLORE BAT EMAN ADIBIDEZ)
        
    rect.id = data_id;
    //beharrezko informazioa hemen gorde
    rect.data("text_value",text_value);
    //diagramaren kudeaketarako beharrezko balioak
    rect.data("parent_id",null);
    rect.data("children",[]);
    
    paths_starts.push(rect.id);
    
    
    // NABIGAZIOA GEHITZEKO
	rect.attr({
    cursor: 'pointer',
	}).click(function(e) {   	
    	
    	var url = 'nabigazio_item'; 
    	
    	//window.location.href=url; //get moduan bidaltzeko				
		var form = $('<form action="' + url + '" method="post">' +
		//'<input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">'+
		'<input type="hidden" name="csrfmiddlewaretoken" value="'+ csrf_token+'">'+
  		'<input type="hidden" name="path_id" value="' + path_id + '" />'+  		
  		'<input type="hidden" name="item_id" value="' + item_id + '" />'+
 		 '</form>');
		$('body').append(form);
		form.submit();
    
   	});
   
    pb_window_resize();
	
}


function nabigatu(path_id,node_id)
{

	//ALA nabigazio_item-era zuzenean?
	var url = 'nabigatu?path_id='+path_id+'&item_id='+node_id+'&autoplay=0';   	
    window.location.href=url;
	
}

//get new element y size
function get_new_y(el){
    if (el){
        var children = el.data("children");
        if (children && (children.length > 0)){
            return get_new_y(paper.getById(children[children.length-1]));
        }
        else{
            return get_y_pos(el.attr("y")) + 1;
        }
    }
    return 0;
}

//geziak eguneratu
function update_arrows(pb_box){
    if (pb_box){
        for (var i = connections.length; i--;) {
            if ((connections[i].to == pb_box) || (connections[i].from == pb_box)){
                paper.connection(connections[i]);
            }
        }
    }
    else{
        for (var i = connections.length; i--;) {
            paper.connection(connections[i]);
        }
    }
}

function onmove(dx,dy,x0,y0,ev){
    //elementua mugitu
    this.attr({x: this.ox + dx, y: this.oy + dy});
    //azpi elementuak mugitu
    var back = paper.getById(this.id + "_back");
    back.attr({x: back.ox + dx, y: back.oy + dy});
    var text = paper.getById(this.id + "_title");
    text.attr({x: text.ox + dx, y: text.oy + dy});
    var image = paper.getById(this.id + "_image");
    image.attr({x: image.ox + dx, y: image.oy + dy});
    var delete_button = paper.getById(this.id + "_delete_button");
    delete_button.attr({x: delete_button.ox + dx, y: delete_button.oy + dy});
    var rect = document.getElementById("path_boxes").getBoundingClientRect();
    var x = x0 - rect.left - window.pageXOffset + paper.canvas.parentNode.scrollLeft, y = y0 - rect.top - window.pageYOffset + paper.canvas.parentNode.scrollTop;
    var me = this;
    var found = false;
    paper.getElementsByPoint(x, y).forEach(function(e){
            if (e.node.classList.contains("pb_box") && (e.id != me.id)){
                me.data("hover_id",e.id);
                paper.getById(e.id + "_back").node.classList.add("pb_box_back_moving");
                found = true;
            }
    });
    if (!found){
        if (this.data("hover_id")){
            paper.getById(this.data("hover_id") + "_back").node.classList.remove("pb_box_back_moving");
            me.removeData("hover_id");
        }
    }
    update_arrows();
}

function onstart(x,y,ev){
    //azpi elementuak aurrera bota
    var back = paper.getById(this.id + "_back");
    back.ox = back.attr("x");
    back.oy = back.attr("y");
    back.toFront();
    var text = paper.getById(this.id + "_title");
    text.ox = text.attr("x");
    text.oy = text.attr("y");
    text.toFront();
    var image = paper.getById(this.id + "_image");
    image.ox = image.attr("x");
    image.oy = image.attr("y");
    image.toFront();
    //elementua aurrera bota
    this.ox = this.attr("x");
    this.oy = this.attr("y");
    this.toFront();
    //ezabatzeko botoia aurrera bota
    var delete_button = paper.getById(this.id + "_delete_button");
    delete_button.ox = delete_button.attr("x");
    delete_button.oy = delete_button.attr("y");
    delete_button.toFront();
    paper.getById(this.id + "_back").node.classList.add("pb_box_back_moving");
}

function onend(ev){
    var old_parent_id = this.data("parent_id");
    if (this.data("hover_id") && (old_parent_id != paper.getById(this.data("hover_id")).id)){
        var new_parent = paper.getById(this.data("hover_id"));
        pb_remove_box(this,false);
        pb_add_son(new_parent,this);
        paper.getById(new_parent.id + "_back").node.classList.remove("pb_box_back_moving");
        paper.getById(this.id + "_back").node.classList.remove("pb_box_back_moving");
    }
    else{
        //elementua mugitu
        this.attr({x: this.ox, y: this.oy});
        //azpi elementuak mugitu
        var back = paper.getById(this.id + "_back");
        back.attr({x: back.ox, y: back.oy});
        var text = paper.getById(this.id + "_title");
        text.attr({x: text.ox, y: text.oy});
        var image = paper.getById(this.id + "_image");
        image.attr({x: image.ox, y: image.oy});
        var delete_button = paper.getById(this.id + "_delete_button");
        delete_button.attr({x: delete_button.ox, y: delete_button.oy});
        paper.getById(this.id + "_back").node.classList.remove("pb_box_back_moving");
        update_arrows(this);
        //itzala kendu
        if (this.data("hover_id")){
            paper.getById(this.data("hover_id") + "_back").node.classList.remove("pb_box_back_moving");
            this.removeData("hover_id");
        }
    }
    pb_window_resize();
}

/*
Ezabatu bere burua
*/
function pb_remove_me(){
    pb_remove_box(paper.getById(this.data("id_value")),true);
    pb_window_resize();
}
/*
Narrazioa gehitzeko funtzioa
*/
/*
function pb_narra_me(){
	alert("pb_narra_me");
	alert(this.data("id_value"));

	//pb_remove_box(paper.getById(this.data("id_value")),true);
    //pb_window_resize();
    
    var narra_div = document.getElementById("narrazioa");
        
    var input = document.createElement("textarea");
	var button = document.createElement("button");
	input.name = "textarea";
	input.maxLength = "5000";
	input.cols = "87";
	input.rows = "5";
	
	narra_div.appendChild(input); //appendChild
	var t = document.createTextNode("Gorde");       // Create a text node
	button.appendChild(t);
	narra_div.appendChild(button);
	
	button.onclick = function () {
  		alert("blabla");
  		var balioa=$.trim($("textarea").val());
  		alert(balioa);
  		//Raphael-en rect-aaren data-n gorde
  		//this.rect.data("item_narrazioa",balioa);
  		//paper.getById(this.data("id_value")).rect.data("item_narrazioa",balioa);
  		
	};
    
    
   
  
}
*/

/*
Ezabatu elementua:
    
    elementua workspacera bidaltzen du
    erlazionaturiko gezi guztiak ezabatu
    azpi elementuak ezabatzen ditu
    bere burua ezabatzen du

aparte egin beharrekoa:
    
    azpian dauden elementuak maila bat igo
*/
function pb_remove_box(pb_box,delete_element){
    var old_parent_id = pb_box.data("parent_id");
    var children = pb_box.data("children");
    if (old_parent_id){
        var old_parent = paper.getById(old_parent_id);
        if (children.length > 0){
            pb_children_left(pb_box);
        }
        else if (old_parent.data("children").length > 1){
            pb_brothers_up(pb_box);
        }
        old_parent.data("children").splice(old_parent.data("children").indexOf(pb_box.id),1);
        for (var i = connections.length; i--;) {
            if ((connections[i].to == pb_box)){
                connections[i].line.remove();
                connections.splice(i,1);
                break;
            }
        }
    }
    else{
        if (children.length > 0){
            pb_children_left(pb_box);
        }
        else{
            pb_brothers_up(pb_box);
        }
        paths_starts.splice(paths_starts.indexOf(pb_box.id),1);
    }
    update_arrows();
    if (delete_element){
        //workspace-an sortu elementua
        var box_id = pb_box.id;
        var text_value = pb_box.data("text_value");
        var image_value = pb_box.data("image_value");
        add_workspace_box(box_id,text_value,image_value);
        //ezabatu azpi elementuak
        paper.getById(pb_box.id + "_back").remove();
        paper.getById(pb_box.id + "_title").remove();
        paper.getById(pb_box.id + "_image").remove();
        paper.getById(pb_box.id + "_delete_button").remove();
        //ezabatu elementua
        pb_box.remove();
    }
}


/*
Semeak ezkerretara mugitu:
    guraso berria esleitu edo erro bezala ezarri
    pb_move_left funtzioa aplikatu elementuari
    elementu eta azpi-elementu guztiak ezkerrera mugitu
    geziak eguneratu
*/
function pb_children_left(parent){
    var children = parent.data("children");
    parent.data("children",[]);
    for (var c=0;c<children.length; c++){
        var child = paper.getById(children[c]);
        //gurasoak gurasorik badu, elementuaren guraso berria bihurtuko da
        if (parent.data("parent_id")){
            //geziak ezabatu
            for (var i = connections.length; i--;) {
                if ((connections[i].to == child) && (connections[i].from == parent)){
                    connections[i].line.remove();
                    connections.splice(i,1);
                    break;
                }
            }
            var new_parent = paper.getById(parent.data("parent_id"));
            var connection = paper.connection(new_parent,child, "#000");
            connections.push(connection);
            new_parent.data("children").splice(new_parent.data("children").indexOf(parent.id),0,child.id);
            child.data("parent_id",new_parent.id);
        }
        //bestela erro elementua bihurtuko da
        else{
            //geziak ezabatu
            for (var i = connections.length; i--;) {
                if ((connections[i].to == child) && (connections[i].from == parent)){
                    connections[i].line.remove();
                    connections.splice(i,1);
                    break;
                }
            }
            paths_starts.splice(paths_starts.indexOf(parent.id),0,child.id);
            child.data("parent_id",null);
        }
        //elementua eta azpi elementuak mugitu
        pb_move_left(child);
    }
    update_arrows();
}

/*
Elementuak ezkerretara mugitu:
    x - 1 aplikatu elementuei
    seme bakoitzari ere deia aplikatu
*/
function pb_move_left(pb_box){
    //elementua mugitu
    pb_box.attr({x: pb_box.attr("x") - (pb_box_space + pb_box_w), y: pb_box.attr("y")});
    //azpi elementuak mugitu
    var back = paper.getById(pb_box.id + "_back");
    back.attr({x: back.attr("x") - (pb_box_space + pb_box_w), y: back.attr("y")});
    var text = paper.getById(pb_box.id + "_title");
    text.attr({x: text.attr("x") - (pb_box_space + pb_box_w), y: text.attr("y")});
    var image = paper.getById(pb_box.id + "_image");
    image.attr({x: image.attr("x") - (pb_box_space + pb_box_w), y: image.attr("y")});
    var delete_button = paper.getById(pb_box.id + "_delete_button");
    delete_button.attr({x: delete_button.attr("x") - (pb_box_space + pb_box_w), y: delete_button.attr("y")});
    var children = pb_box.data("children");
    for (var c=0;c<children.length; c++){
        pb_move_left(paper.getById(children[c]));
    }
}

/*
Elementu anaiak igo:
    anaiei pb_move_up aplikatu continue false
    gurasoak azpi-anairik duen konprobatu, hauei pb_move_up aplikatu continue false
    guraso gabeko azken gurasoa hartzean, erro zerrendatik hurrengo elementuak hartu eta hauei pb_move_up aplikatu
*/

function pb_brothers_up(pb_box){
    var parent_id = pb_box.data("parent_id");
    if (parent_id){
        var parent = paper.getById(parent_id);
        var next_children = parent.data("children").slice(parent.data("children").indexOf(pb_box.id)+1);
        for (var c=0;c<next_children.length; c++) {
            pb_move_up(paper.getById(next_children[c]));
        }
        pb_brothers_up(parent);
    }
    else{
        var next_paths_starts = paths_starts.slice(paths_starts.indexOf(pb_box.id)+1);
        for (var c=0;c<next_paths_starts.length; c++) {
            pb_move_up(paper.getById(next_paths_starts[c]));
        }
    }
}

function pb_brothers_up_egunekoa(pb_box){
    var parent_id = pb_box.data("parent_id");
    if (parent_id){
        var parent = paper.getById(parent_id);
        var next_children = parent.data("children").slice(parent.data("children").indexOf(pb_box.id)+1);
        for (var c=0;c<next_children.length; c++) {
            pb_move_up_egunekoa(paper.getById(next_children[c]));
        }
        pb_brothers_up_egunekoa(parent);
    }
    else{
        var next_paths_starts = paths_starts.slice(paths_starts.indexOf(pb_box.id)+1);
        for (var c=0;c<next_paths_starts.length; c++) {
            pb_move_up_egunekoa(paper.getById(next_paths_starts[c]));
        }
    }
}

function pb_brothers_up_overview(pb_box){
    var parent_id = pb_box.data("parent_id");
    if (parent_id){
        var parent = paper.getById(parent_id);
        var next_children = parent.data("children").slice(parent.data("children").indexOf(pb_box.id)+1);
        for (var c=0;c<next_children.length; c++) {
            pb_move_up_overview(paper.getById(next_children[c]));
        }
        pb_brothers_up_overview(parent);
    }
    else{
        var next_paths_starts = paths_starts.slice(paths_starts.indexOf(pb_box.id)+1);
        for (var c=0;c<next_paths_starts.length; c++) {
            pb_move_up_overview(paper.getById(next_paths_starts[c]));
        }
    }
}

/*
Elementuak gora:
    errekurtsiboa da.
    y - 1 aplikatu elementuei
    seme bakoitzari ere deia aplikatu
*/
function pb_move_up(pb_box){
    //elementuak mugitu
    pb_box.attr({x: pb_box.attr("x"), y: pb_box.attr("y") - (pb_box_space + pb_box_h)});
    //azpi elementuak mugitu
    var back = paper.getById(pb_box.id + "_back");
    back.attr({x: back.attr("x"), y: back.attr("y") - (pb_box_space + pb_box_h)});
    var text = paper.getById(pb_box.id + "_title");
    text.attr({x: text.attr("x"), y: text.attr("y") - (pb_box_space + pb_box_h)});
    var image = paper.getById(pb_box.id + "_image");
    image.attr({x: image.attr("x"), y: image.attr("y") - (pb_box_space + pb_box_h)});
    var delete_button = paper.getById(pb_box.id + "_delete_button");
    delete_button.attr({x: delete_button.attr("x"), y: delete_button.attr("y") - (pb_box_space + pb_box_h)});
    var children = pb_box.data("children");
    for (var c=0;c<children.length; c++){
        pb_move_up(paper.getById(children[c]));
    }
}

function pb_move_up_egunekoa(pb_box){
    //elementuak mugitu
    pb_box.attr({x: pb_box.attr("x"), y: pb_box.attr("y") - (pb_box_space + pb_box_h)});
    //azpi elementuak mugitu
    var back = paper.getById(pb_box.id + "_back");
    back.attr({x: back.attr("x"), y: back.attr("y") - (pb_box_space + pb_box_h)});
    var text = paper.getById(pb_box.id + "_title");
    text.attr({x: text.attr("x"), y: text.attr("y") - (pb_box_space + pb_box_h)});
    var image = paper.getById(pb_box.id + "_image");
    image.attr({x: image.attr("x"), y: image.attr("y") - (pb_box_space + pb_box_h)});
    var children = pb_box.data("children");
    for (var c=0;c<children.length; c++){
        pb_move_up_egunekoa(paper.getById(children[c]));
    }
}

function pb_move_up_overview(pb_box){
    //elementuak mugitu
    pb_box.attr({x: pb_box.attr("x"), y: pb_box.attr("y") - (pb_box_space + pb_box_h)});
    //azpi elementuak mugitu
    var back = paper.getById(pb_box.id + "_back");
    back.attr({x: back.attr("x"), y: back.attr("y") - (pb_box_space + pb_box_h)});
    var text = paper.getById(pb_box.id + "_title");
    text.attr({x: text.attr("x"), y: text.attr("y") - (pb_box_space + pb_box_h)});
    //var image = paper.getById(pb_box.id + "_image");
    //image.attr({x: image.attr("x"), y: image.attr("y") - (pb_box_space + pb_box_h)});
    var children = pb_box.data("children");
    for (var c=0;c<children.length; c++){
        pb_move_up_overview(paper.getById(children[c]));
    }
}


function pb_add_new_son(parent_id,data_id,text_value,image_value){
    var parent = paper.getById(parent_id);
    pb_new_element(data_id,text_value,image_value);
    var new_son = paper.getById(data_id);
    pb_brothers_up(new_son);
    paths_starts.splice(paths_starts.indexOf(data_id),1);
    pb_add_son(parent,new_son);
}

function pb_add_new_son_egunekoa(parent_id,data_id,text_value,image_value,path_id,node_id){
    var parent = paper.getById(parent_id);
    pb_new_element_egunekoa(data_id,text_value,image_value,path_id,node_id); //nabigaziorako 
    var new_son = paper.getById(data_id);
    pb_brothers_up_egunekoa(new_son);
    paths_starts.splice(paths_starts.indexOf(data_id),1);
    pb_add_son_egunekoa(parent,new_son);
}

function pb_add_new_son_overview(parent_id,data_id,text_value,path_id,node_id,nabarmentzeko_id){
    var parent = paper.getById(parent_id);
    pb_new_element_overview(data_id,text_value,path_id,node_id,nabarmentzeko_id); 
    var new_son = paper.getById(data_id);
    pb_brothers_up_overview(new_son);
    paths_starts.splice(paths_starts.indexOf(data_id),1);
    pb_add_son_overview(parent,new_son);
}

/*
Semea gehitu:
    semea gehitu eta dagokion marra
    esleitu gurasoa
    anaiak baditu:
        gurasoak azpi-anairik badu jaitsi +1 eta honen semeei errekurtsiboki
        guraso gabeko azken gurasoa hartzena, erro zerrendatik hurrengo elementuak hartu eta hauei pb_move_down aplikatu
*/
function pb_add_son(parent,pb_box){
    var back = paper.getById(pb_box.id + "_back");
    var text = paper.getById(pb_box.id + "_title");
    var image = paper.getById(pb_box.id + "_image");
    var delete_button = paper.getById(pb_box.id + "_delete_button");
    if (parent.data("children").length > 0){
        pb_brothers_down(parent);
        update_arrows();
        var last_son = paper.getById(parent.data("children")[parent.data("children").length-1]);
        y_position = get_new_y(last_son);
        //elementua mugitu
        pb_box.attr({x: last_son.attr("x"), y: get_y(y_position)});
        //azpi elementuak mugitu
        back.attr({x: last_son.attr("x"), y: get_y(y_position)});
        text.attr({x: last_son.attr("x") + 60, y: get_y(y_position) + 100});
        image.attr({x: last_son.attr("x") + 5, y: get_y(y_position) + 5});
        delete_button.attr({x: last_son.attr("x")+pb_box_w-10, y: get_y(y_position) + 10});
    }
    else{
        //elementua mugitu
        pb_box.attr({x: parent.attr("x") + (pb_box_space + pb_box_w), y: parent.attr("y")});
        //azpi elementuak mugitu
        back.attr({x: parent.attr("x") + (pb_box_space + pb_box_w), y: parent.attr("y")});
        text.attr({x: parent.attr("x") + (pb_box_space + pb_box_w) + 60, y: parent.attr("y") + 100});
        image.attr({x: parent.attr("x") + (pb_box_space + pb_box_w) + 5, y: parent.attr("y") + 5});
        delete_button.attr({x: parent.attr("x") + (pb_box_space + pb_box_w) + pb_box_w -10, y: parent.attr("y") + 10});
    }
    parent.data("children").push(pb_box.id);
    pb_box.data("parent_id",parent.id);
    var connection = paper.connection(parent,pb_box, "#000");
    connections.push(connection);
}

//MAddalen
function pb_add_son_egunekoa(parent,pb_box){
    var back = paper.getById(pb_box.id + "_back");
    var text = paper.getById(pb_box.id + "_title");
    var image = paper.getById(pb_box.id + "_image");
    
    if (parent.data("children").length > 0){
        pb_brothers_down_egunekoa(parent);
        update_arrows();
        var last_son = paper.getById(parent.data("children")[parent.data("children").length-1]);
        y_position = get_new_y(last_son);
        //elementua mugitu
        pb_box.attr({x: last_son.attr("x"), y: get_y(y_position)});
        //azpi elementuak mugitu
        back.attr({x: last_son.attr("x"), y: get_y(y_position)});
        text.attr({x: last_son.attr("x") + 60, y: get_y(y_position) + 100});
        image.attr({x: last_son.attr("x") + 5, y: get_y(y_position) + 5});
       
    }
    else{
        //elementua mugitu
        pb_box.attr({x: parent.attr("x") + (pb_box_space + pb_box_w), y: parent.attr("y")});
        //azpi elementuak mugitu
        back.attr({x: parent.attr("x") + (pb_box_space + pb_box_w), y: parent.attr("y")});
        text.attr({x: parent.attr("x") + (pb_box_space + pb_box_w) + 60, y: parent.attr("y") + 100});
        image.attr({x: parent.attr("x") + (pb_box_space + pb_box_w) + 5, y: parent.attr("y") + 5});
        
    }
    parent.data("children").push(pb_box.id);
    pb_box.data("parent_id",parent.id);
    var connection = paper.connection(parent,pb_box, "#000");
    connections.push(connection);
}

function pb_add_son_overview(parent,pb_box){
    var back = paper.getById(pb_box.id + "_back");
    var text = paper.getById(pb_box.id + "_title");
    
    
    if (parent.data("children").length > 0){
        pb_brothers_down_overview(parent);
        update_arrows();
        var last_son = paper.getById(parent.data("children")[parent.data("children").length-1]);
        y_position = get_new_y(last_son);
        //elementua mugitu
        pb_box.attr({x: last_son.attr("x"), y: get_y(y_position)});
        //azpi elementuak mugitu
        back.attr({x: last_son.attr("x"), y: get_y(y_position)});
        //Maddalen: +30
        text.attr({x: last_son.attr("x") + 60, y: get_y(y_position) + 30});
        
       
    }
    else{
        //elementua mugitu
        pb_box.attr({x: parent.attr("x") + (pb_box_space + pb_box_w), y: parent.attr("y")});
        //azpi elementuak mugitu
        back.attr({x: parent.attr("x") + (pb_box_space + pb_box_w), y: parent.attr("y")});
        //Maddalen: +30
        text.attr({x: parent.attr("x") + (pb_box_space + pb_box_w) + 60, y: parent.attr("y") + 30});
       
    }
    parent.data("children").push(pb_box.id);
    pb_box.data("parent_id",parent.id);
    var connection = paper.connection(parent,pb_box, "#000");
    connections.push(connection);
}

/*
Anaiak eta hurrengoak behera mugitu
*/
function pb_brothers_down(pb_box){
    var parent_id = pb_box.data("parent_id");
    if (parent_id){
        var parent = paper.getById(parent_id);
        var next_children = parent.data("children").slice(parent.data("children").indexOf(pb_box.id)+1);
        for (var c=0;c<next_children.length; c++) {
            pb_move_down(paper.getById(next_children[c]));
        }
        pb_brothers_down(parent);
    }
    else{
        var next_paths_starts = paths_starts.slice(paths_starts.indexOf(pb_box.id)+1);
        for (var c=0;c<next_paths_starts.length; c++) {
            pb_move_down(paper.getById(next_paths_starts[c]));
        }
    }
}

function pb_brothers_down_egunekoa(pb_box){
    var parent_id = pb_box.data("parent_id");
    if (parent_id){
        var parent = paper.getById(parent_id);
        var next_children = parent.data("children").slice(parent.data("children").indexOf(pb_box.id)+1);
        for (var c=0;c<next_children.length; c++) {
            pb_move_down_egunekoa(paper.getById(next_children[c]));
        }
        pb_brothers_down_egunekoa(parent);
    }
    else{
        var next_paths_starts = paths_starts.slice(paths_starts.indexOf(pb_box.id)+1);
        for (var c=0;c<next_paths_starts.length; c++) {
            pb_move_down_egunekoa(paper.getById(next_paths_starts[c]));
        }
    }
}

function pb_brothers_down_overview(pb_box){
    var parent_id = pb_box.data("parent_id");
    if (parent_id){
        var parent = paper.getById(parent_id);
        var next_children = parent.data("children").slice(parent.data("children").indexOf(pb_box.id)+1);
        for (var c=0;c<next_children.length; c++) {
            pb_move_down_overview(paper.getById(next_children[c]));
        }
        pb_brothers_down_overview(parent);
    }
    else{
        var next_paths_starts = paths_starts.slice(paths_starts.indexOf(pb_box.id)+1);
        for (var c=0;c<next_paths_starts.length; c++) {
            pb_move_down_overview(paper.getById(next_paths_starts[c]));
        }
    }
}

/*
Elementuak gora:
    errekurtsiboa da.
    y + 1 aplikatu elementuei
    seme bakoitzari ere deia aplikatu
*/
function pb_move_down(pb_box){
    pb_box.attr({x: pb_box.attr("x"), y: pb_box.attr("y") + (pb_box_space + pb_box_h)});
    var back = paper.getById(pb_box.id + "_back");
    back.attr({x: back.attr("x"), y: back.attr("y") + (pb_box_space + pb_box_h)});
    var text = paper.getById(pb_box.id + "_title");
    text.attr({x: text.attr("x"), y: text.attr("y") + (pb_box_space + pb_box_h)});
    var image = paper.getById(pb_box.id + "_image");
    image.attr({x: image.attr("x"), y: image.attr("y") + (pb_box_space + pb_box_h)});
    var delete_button = paper.getById(pb_box.id + "_delete_button");
    delete_button.attr({x: delete_button.attr("x"), y: delete_button.attr("y") + (pb_box_space + pb_box_h)});
    var children = pb_box.data("children");
    for (var c=0;c<children.length; c++){
        pb_move_down(paper.getById(children[c]));
    }
}

//Maddalen, aurreko funtzioaren kopia da
function pb_move_down_egunekoa(pb_box){
    pb_box.attr({x: pb_box.attr("x"), y: pb_box.attr("y") + (pb_box_space + pb_box_h)});
    var back = paper.getById(pb_box.id + "_back");
    back.attr({x: back.attr("x"), y: back.attr("y") + (pb_box_space + pb_box_h)});
    var text = paper.getById(pb_box.id + "_title");
    text.attr({x: text.attr("x"), y: text.attr("y") + (pb_box_space + pb_box_h)});
    var image = paper.getById(pb_box.id + "_image");
    image.attr({x: image.attr("x"), y: image.attr("y") + (pb_box_space + pb_box_h)});
    var children = pb_box.data("children");
    for (var c=0;c<children.length; c++){
        pb_move_down_egunekoa(paper.getById(children[c]));
    }
}

function pb_move_down_overview(pb_box){
    pb_box.attr({x: pb_box.attr("x"), y: pb_box.attr("y") + (pb_box_space + pb_box_h)});
    var back = paper.getById(pb_box.id + "_back");
    back.attr({x: back.attr("x"), y: back.attr("y") + (pb_box_space + pb_box_h)});
    var text = paper.getById(pb_box.id + "_title");
    text.attr({x: text.attr("x"), y: text.attr("y") + (pb_box_space + pb_box_h)});
    //var image = paper.getById(pb_box.id + "_image");
    //image.attr({x: image.attr("x"), y: image.attr("y") + (pb_box_space + pb_box_h)});
    var children = pb_box.data("children");
    for (var c=0;c<children.length; c++){
        pb_move_down_overview(paper.getById(children[c]));
    }
}



/*Raphael.fn.connection = function (obj1, obj2, line, bg) {
    if (obj1.line && obj1.from && obj1.to) {
        line = obj1;
        obj1 = line.from;
        obj2 = line.to;
    }
    var bb1 = obj1.getBBox(),
        bb2 = obj2.getBBox(),
        p = [{x: bb1.x + bb1.width / 2, y: bb1.y - 1},
        {x: bb1.x + bb1.width / 2, y: bb1.y + bb1.height + 1},
        {x: bb1.x - 1, y: bb1.y + bb1.height / 2},
        {x: bb1.x + bb1.width + 1, y: bb1.y + bb1.height / 2},
        {x: bb2.x + bb2.width / 2, y: bb2.y - 1},
        {x: bb2.x + bb2.width / 2, y: bb2.y + bb2.height + 1},
        {x: bb2.x - 1, y: bb2.y + bb2.height / 2},
        {x: bb2.x + bb2.width + 1, y: bb2.y + bb2.height / 2}],
        d = {}, dis = [];
    for (var i = 0; i < 4; i++) {
        for (var j = 4; j < 8; j++) {
            var dx = Math.abs(p[i].x - p[j].x),
                dy = Math.abs(p[i].y - p[j].y);
            if ((i == j - 4) || (((i != 3 && j != 6) || p[i].x < p[j].x) && ((i != 2 && j != 7) || p[i].x > p[j].x) && ((i != 0 && j != 5) || p[i].y > p[j].y) && ((i != 1 && j != 4) || p[i].y < p[j].y))) {
                dis.push(dx + dy);
                d[dis[dis.length - 1]] = [i, j];
            }
        }
    }
    if (dis.length == 0) {
        var res = [0, 4];
    } else {
        res = d[Math.min.apply(Math, dis)];
    }
    var x1 = p[res[0]].x,
        y1 = p[res[0]].y,
        x4 = p[res[1]].x,
        y4 = p[res[1]].y;
    dx = Math.max(Math.abs(x1 - x4) / 2, 10);
    dy = Math.max(Math.abs(y1 - y4) / 2, 10);
    var x2 = [x1, x1, x1 - dx, x1 + dx][res[0]].toFixed(3),
        y2 = [y1 - dy, y1 + dy, y1, y1][res[0]].toFixed(3),
        x3 = [0, 0, 0, 0, x4, x4, x4 - dx, x4 + dx][res[1]].toFixed(3),
        y3 = [0, 0, 0, 0, y1 + dy, y1 - dy, y4, y4][res[1]].toFixed(3);
    var path = ["M", x1.toFixed(3), y1.toFixed(3), "C", x2, y2, x3, y3, x4.toFixed(3), y4.toFixed(3)].join(",");
    if (line && line.line) {
        line.bg && line.bg.attr({path: path});
        line.line.attr({path: path});
    } else {
        var color = typeof line == "string" ? line : "#000";
        return {
            bg: bg && bg.split && this.path(path).attr({stroke: bg.split("|")[0], fill: "none", "stroke-width": bg.split("|")[1] || 3}),
            line: this.path(path).attr({stroke: color, fill: "none"}),
            from: obj1,
            to: obj2
        };
    }
};
*/
function ibilbidea_kargatu(path_id)
{
	
	var path_id=path_id;
	//Datu-basetik erroak direnak lortu ->pb_new_element
	
	//Datu-basetik semeak lortzen joan ->pb_add_new_son
	/*
	  pb_new_element("box_1","Aita Donostiari omenaldia : ikonografi erreportaia","http://hedatuz.euskomedia.org/7031/1/03109132.pdf.png");
        pb_add_new_son("box_1","box_2","Legendarias regatas de traineras: las primeras décadas en el asentamiento del deporte de Remo de Banco Fijo en el Cantábrico (1844-1871)","http://hedatuz.euskomedia.org/8432/1/33341360.pdf.png");
        pb_new_element("box_3","Aquarium: 100 años de Historia","http://www.euskomedia.org/MusicGaler/foto/74_aquarium.jpg");
        pb_add_new_son("box_3","box_4","Celebración de la Tamborrada en Donostia-San Sebastián (Gipuzkoa) la madrugada del 20 de enero.","http://www.euskomedia.org/MusicGaler/foto/v000070.jpg");
        pb_add_new_son("box_3","box_5","Gran Casino Kursaal","http://www.euskomedia.org/ImgsGaler/onati/OAA00220.jpg");
        
	 */
}

function egunekoaGehituEtabilaketaFiltratu(item_id)
{
	var radios = document.getElementsByName('hizkRadio');
	var galdera = document.getElementById('search_input').value;
	

	for (var i = 0, length = radios.length; i < length; i++) 
	{
   	    if (radios[i].checked)
        {
            // do whatever you want with the checked radio
            hizkR=radios[i].value;
            // only one radio can be logically checked, don't check the rest
            break;
        }
	}



	var hizkuntzakF_ar = []; 
	var hornitzaileakF_ar = [];
	var motaF_ar = [];
	var ordenaF_ar = [];
	var lizentziaF_ar = [];
	var besteF_ar = [];
	
	//Hizkuntzak
	var EuhizkElement = document.getElementById('hizkuntza1F');
	var EshizkElement = document.getElementById('hizkuntza2F');
	var EnhizkElement = document.getElementById('hizkuntza3F');
	
	//Hornitzaileak
	var EkmHorniElement = document.getElementById('hornitzaile1F');
	var ArruntaHorniElement = document.getElementById('hornitzaile2F');
	
	//Mota
	var textMotaElement = document.getElementById('mota1F');
	var audioMotaElement = document.getElementById('mota2F');
	var videoMotaElement = document.getElementById('mota3F');
	var imgMotaElement = document.getElementById('mota4F');
	
	//Ordena
	var dataOrdenaElement = document.getElementById('ordena1F');
	var data2OrdenaElement = document.getElementById('ordena3F');
	var botoOrdenaElement = document.getElementById('ordena2F');
	
	//Lizentzia
	var lizentziaLibreElement =document.getElementById('lizentzia1F');
	var lizentziaCommonsElement =document.getElementById('lizentzia2F');
	var lizentziaCopyElement =document.getElementById('lizentzia3F');
	
	//Beste batzuk
	var egunekoaElement = document.getElementById('egunekoaF');
	var proposatutakoaElement = document.getElementById('proposatutakoaF');
	var wikifikatuaElement = document.getElementById('wikifikatuaF');
	var irudiaDuElement = document.getElementById('irudiaDuF');
	var irudiaEzDuElement = document.getElementById('irudiaEzDuF');
	
	var balioa;
	//HIZKUNTZAK
	if (EuhizkElement.checked == true)
	 {
	 	balioa=EuhizkElement.value;
	 	hizkuntzakF_ar.push(balioa);
	 }
	 if (EshizkElement.checked == true)
	 {
	 	balioa=EshizkElement.value;
	 	hizkuntzakF_ar.push(balioa);
	 
	 }
	 if (EnhizkElement.checked == true)
	 {
	 	balioa=EnhizkElement.value;
	 	hizkuntzakF_ar.push(balioa);
	 
	 }
	 //HORNITZAILEAK
	 if(EkmHorniElement.checked == true)
	 {
	 	balioa=EkmHorniElement.value;
	 	hornitzaileakF_ar.push(balioa);
	 }
	 if(ArruntaHorniElement.checked == true)
	 {
	 	balioa=ArruntaHorniElement.value;
	 	hornitzaileakF_ar.push(balioa);
	 }
	 //MOTA
	 if(textMotaElement.checked == true)
	 {
	 	balioa=textMotaElement.value;
	 	motaF_ar.push(balioa);
	 }
	 if(audioMotaElement.checked == true)
	 {
	 	balioa=audioMotaElement.value;
	 	motaF_ar.push(balioa);
	 }
	 if(videoMotaElement.checked == true)
	 {
	 	balioa=videoMotaElement.value;
	 	motaF_ar.push(balioa);
	 }
	 if(imgMotaElement.checked == true)
	 {
	 	balioa=imgMotaElement.value;
	 	motaF_ar.push(balioa);
	 }
	 //ORDENA
	 if(dataOrdenaElement.checked == true)
	 {
	 	balioa=dataOrdenaElement.value;
	 	ordenaF_ar.push(balioa);
	 }
	 if(data2OrdenaElement.checked == true)
	 {
	 	balioa=data2OrdenaElement.value;
	 	ordenaF_ar.push(balioa);
	 }
	 if(botoOrdenaElement.checked == true)
	 {
	 	balioa=botoOrdenaElement.value;
	 	ordenaF_ar.push(balioa);
	 }
	 //LIZENTZIA
	 if(lizentziaLibreElement.checked == true)
	 {
	 	balioa=lizentziaLibreElement.value;
	 	lizentziaF_ar.push(balioa);	 	
	 }
	  if(lizentziaCommonsElement.checked == true)
	 {
	 	balioa=lizentziaCommonsElement.value;
	 	lizentziaF_ar.push(balioa);	 	
	 }
	  if(lizentziaCopyElement.checked == true)
	 {
	 	balioa=lizentziaCopyElement.value;
	 	lizentziaF_ar.push(balioa);	 	
	 }
	 //Beste batzuk
	  if(egunekoaElement.checked == true)
	 {
	 	balioa=egunekoaElement.value;
	 	besteF_ar.push(balioa);
	 }
	 if(proposatutakoaElement.checked == true)
	 {
	 	balioa=proposatutakoaElement.value;
	 	besteF_ar.push(balioa);
	 }
	  if(wikifikatuaElement.checked == true)
	 {
	 	balioa=wikifikatuaElement.value;
	 	besteF_ar.push(balioa);
	 }
	  if(irudiaDuElement.checked == true)
	 {
	 	balioa=irudiaDuElement.value;
	 	besteF_ar.push(balioa);
	 }
	  if(irudiaEzDuElement.checked == true)
	 {
	 	balioa=irudiaEzDuElement.value;
	 	besteF_ar.push(balioa);
	 }
	 
	 
	 var hizkuntzakF=hizkuntzakF_ar.toString(); 
	 var hornitzaileakF=hornitzaileakF_ar.toString(); 
	 var motakF=motaF_ar.toString();
	 var ordenakF=ordenaF_ar.toString();
	 var lizentziakF=lizentziaF_ar.toString();
	 var besteakF =besteF_ar.toString();
	 
	var url = 'eguneko_itema_gehitu?hizkRadio='+hizkR+'&search_input='+galdera+'&hizkuntzakF='+hizkuntzakF+'&hornitzaileakF='+hornitzaileakF+'&motakF='+motakF+'&ordenakF='+ordenakF+'&lizentziakF='+lizentziakF+'&besteakF='+besteakF+'&id='+item_id+'&nondik=bilaketa';   	
    window.location.href=url;
	
}

function egunekoaKenduEtabilaketaFiltratu(item_id)
{
	var radios = document.getElementsByName('hizkRadio');
	var galdera = document.getElementById('search_input').value;
	

	for (var i = 0, length = radios.length; i < length; i++) 
	{
   	    if (radios[i].checked)
        {
            // do whatever you want with the checked radio
            hizkR=radios[i].value;
            // only one radio can be logically checked, don't check the rest
            break;
        }
	}



	var hizkuntzakF_ar = []; 
	var hornitzaileakF_ar = [];
	var motaF_ar = [];
	var ordenaF_ar = [];
	var lizentziaF_ar = [];
	var besteF_ar = [];
	
	//Hizkuntzak
	var EuhizkElement = document.getElementById('hizkuntza1F');
	var EshizkElement = document.getElementById('hizkuntza2F');
	var EnhizkElement = document.getElementById('hizkuntza3F');
	
	//Hornitzaileak
	var EkmHorniElement = document.getElementById('hornitzaile1F');
	var ArruntaHorniElement = document.getElementById('hornitzaile2F');
	
	//Mota
	var textMotaElement = document.getElementById('mota1F');
	var audioMotaElement = document.getElementById('mota2F');
	var videoMotaElement = document.getElementById('mota3F');
	var imgMotaElement = document.getElementById('mota4F');
	
	//Ordena
	var dataOrdenaElement = document.getElementById('ordena1F');
	var data2OrdenaElement = document.getElementById('ordena3F');
	var botoOrdenaElement = document.getElementById('ordena2F');
	
	//Lizentzia
	var lizentziaLibreElement =document.getElementById('lizentzia1F');
	var lizentziaCommonsElement =document.getElementById('lizentzia2F');
	var lizentziaCopyElement =document.getElementById('lizentzia3F');
	
	//Beste batzuk
	var egunekoaElement = document.getElementById('egunekoaF');
	var proposatutakoaElement = document.getElementById('proposatutakoaF');
	var wikifikatuaElement = document.getElementById('wikifikatuaF');
	var irudiaDuElement = document.getElementById('irudiaDuF');
	var irudiaEzDuElement = document.getElementById('irudiaEzDuF');
	
	var balioa;
	//HIZKUNTZAK
	if (EuhizkElement.checked == true)
	 {
	 	balioa=EuhizkElement.value;
	 	hizkuntzakF_ar.push(balioa);
	 }
	 if (EshizkElement.checked == true)
	 {
	 	balioa=EshizkElement.value;
	 	hizkuntzakF_ar.push(balioa);
	 
	 }
	 if (EnhizkElement.checked == true)
	 {
	 	balioa=EnhizkElement.value;
	 	hizkuntzakF_ar.push(balioa);
	 
	 }
	 //HORNITZAILEAK
	 if(EkmHorniElement.checked == true)
	 {
	 	balioa=EkmHorniElement.value;
	 	hornitzaileakF_ar.push(balioa);
	 }
	 if(ArruntaHorniElement.checked == true)
	 {
	 	balioa=ArruntaHorniElement.value;
	 	hornitzaileakF_ar.push(balioa);
	 }
	 //MOTA
	 if(textMotaElement.checked == true)
	 {
	 	balioa=textMotaElement.value;
	 	motaF_ar.push(balioa);
	 }
	 if(audioMotaElement.checked == true)
	 {
	 	balioa=audioMotaElement.value;
	 	motaF_ar.push(balioa);
	 }
	 if(videoMotaElement.checked == true)
	 {
	 	balioa=videoMotaElement.value;
	 	motaF_ar.push(balioa);
	 }
	 if(imgMotaElement.checked == true)
	 {
	 	balioa=imgMotaElement.value;
	 	motaF_ar.push(balioa);
	 }
	 //ORDENA
	 if(dataOrdenaElement.checked == true)
	 {
	 	balioa=dataOrdenaElement.value;
	 	ordenaF_ar.push(balioa);
	 }
	 if(data2OrdenaElement.checked == true)
	 {
	 	balioa=data2OrdenaElement.value;
	 	ordenaF_ar.push(balioa);
	 }
	 if(botoOrdenaElement.checked == true)
	 {
	 	balioa=botoOrdenaElement.value;
	 	ordenaF_ar.push(balioa);
	 }
	 //LIZENTZIA
	 if(lizentziaLibreElement.checked == true)
	 {
	 	balioa=lizentziaLibreElement.value;
	 	lizentziaF_ar.push(balioa);	 	
	 }
	  if(lizentziaCommonsElement.checked == true)
	 {
	 	balioa=lizentziaCommonsElement.value;
	 	lizentziaF_ar.push(balioa);	 	
	 }
	  if(lizentziaCopyElement.checked == true)
	 {
	 	balioa=lizentziaCopyElement.value;
	 	lizentziaF_ar.push(balioa);	 	
	 }
	 //Beste batzuk
	  if(egunekoaElement.checked == true)
	 {
	 	balioa=egunekoaElement.value;
	 	besteF_ar.push(balioa);
	 }
	 if(proposatutakoaElement.checked == true)
	 {
	 	balioa=proposatutakoaElement.value;
	 	besteF_ar.push(balioa);
	 }
	  if(wikifikatuaElement.checked == true)
	 {
	 	balioa=wikifikatuaElement.value;
	 	besteF_ar.push(balioa);
	 }
	  if(irudiaDuElement.checked == true)
	 {
	 	balioa=irudiaDuElement.value;
	 	besteF_ar.push(balioa);
	 }
	  if(irudiaEzDuElement.checked == true)
	 {
	 	balioa=irudiaEzDuElement.value;
	 	besteF_ar.push(balioa);
	 }
	 
	 
	 var hizkuntzakF=hizkuntzakF_ar.toString(); 
	 var hornitzaileakF=hornitzaileakF_ar.toString(); 
	 var motakF=motaF_ar.toString();
	 var ordenakF=ordenaF_ar.toString();
	 var lizentziakF=lizentziaF_ar.toString();
	 var besteakF =besteF_ar.toString();
	 
	var url = 'eguneko_itema_kendu?hizkRadio='+hizkR+'&search_input='+galdera+'&hizkuntzakF='+hizkuntzakF+'&hornitzaileakF='+hornitzaileakF+'&motakF='+motakF+'&ordenakF='+ordenakF+'&lizentziakF='+lizentziakF+'&besteakF='+besteakF+'&id='+item_id+'&nondik=bilaketa';   	
    window.location.href=url;
	
}
function bilaketaFiltratu()
{
	
	var radios = document.getElementsByName('hizkRadio');
	var galdera = document.getElementById('search_input').value;
	
	for (var i = 0, length = radios.length; i < length; i++) 
	{
   	    if (radios[i].checked)
        {
            // do whatever you want with the checked radio
            hizkR=radios[i].value;
            // only one radio can be logically checked, don't check the rest
            break;
        }
	}



	var hizkuntzakF_ar = []; 
	var hornitzaileakF_ar = [];
	var motaF_ar = [];
	var ordenaF_ar = [];
	var lizentziaF_ar = [];
	var besteF_ar = [];
	
	//Hizkuntzak
	var EuhizkElement = document.getElementById('hizkuntza1F');
	var EshizkElement = document.getElementById('hizkuntza2F');
	var EnhizkElement = document.getElementById('hizkuntza3F');
	
	//Hornitzaileak
	var EkmHorniElement = document.getElementById('hornitzaile1F');
	var ArruntaHorniElement = document.getElementById('hornitzaile2F');
	
	//Mota
	var textMotaElement = document.getElementById('mota1F');
	var audioMotaElement = document.getElementById('mota2F');
	var videoMotaElement = document.getElementById('mota3F');
	var imgMotaElement = document.getElementById('mota4F');
	
	//Ordena
	var dataOrdenaElement = document.getElementById('ordena1F');
	var data2OrdenaElement = document.getElementById('ordena3F');
	var botoOrdenaElement = document.getElementById('ordena2F');
	
	//Lizentzia
	var lizentziaLibreElement =document.getElementById('lizentzia1F');
	var lizentziaCommonsElement =document.getElementById('lizentzia2F');
	var lizentziaCopyElement =document.getElementById('lizentzia3F');
	
	//Beste batzuk
	var egunekoaElement = document.getElementById('egunekoaF');
	var proposatutakoaElement = document.getElementById('proposatutakoaF');
	var wikifikatuaElement = document.getElementById('wikifikatuaF');
	var irudiaDuElement = document.getElementById('irudiaDuF');
	var irudiaEzDuElement = document.getElementById('irudiaEzDuF');
	
	var balioa;
	//HIZKUNTZAK
	if (EuhizkElement.checked == true)
	 {
	 	balioa=EuhizkElement.value;
	 	hizkuntzakF_ar.push(balioa);
	 }
	 if (EshizkElement.checked == true)
	 {
	 	balioa=EshizkElement.value;
	 	hizkuntzakF_ar.push(balioa);
	 
	 }
	 if (EnhizkElement.checked == true)
	 {
	 	balioa=EnhizkElement.value;
	 	hizkuntzakF_ar.push(balioa);
	 
	 }
	 //HORNITZAILEAK
	 if(EkmHorniElement.checked == true)
	 {
	 	balioa=EkmHorniElement.value;
	 	hornitzaileakF_ar.push(balioa);
	 }
	 if(ArruntaHorniElement.checked == true)
	 {
	 	balioa=ArruntaHorniElement.value;
	 	hornitzaileakF_ar.push(balioa);
	 }
	 //MOTA
	 if(textMotaElement.checked == true)
	 {
	 	balioa=textMotaElement.value;
	 	motaF_ar.push(balioa);
	 }
	 if(audioMotaElement.checked == true)
	 {
	 	balioa=audioMotaElement.value;
	 	motaF_ar.push(balioa);
	 }
	 if(videoMotaElement.checked == true)
	 {
	 	balioa=videoMotaElement.value;
	 	motaF_ar.push(balioa);
	 }
	 if(imgMotaElement.checked == true)
	 {
	 	balioa=imgMotaElement.value;
	 	motaF_ar.push(balioa);
	 }
	 //ORDENA
	 if(dataOrdenaElement.checked == true)
	 {
	 	balioa=dataOrdenaElement.value;
	 	ordenaF_ar.push(balioa);
	 }
	 if(data2OrdenaElement.checked == true)
	 {
	 	balioa=data2OrdenaElement.value;
	 	ordenaF_ar.push(balioa);
	 }
	 if(botoOrdenaElement.checked == true)
	 {
	 	balioa=botoOrdenaElement.value;
	 	ordenaF_ar.push(balioa);
	 }
	 //LIZENTZIA
	 if(lizentziaLibreElement.checked == true)
	 {
	 	balioa=lizentziaLibreElement.value;
	 	lizentziaF_ar.push(balioa);	 	
	 }
	  if(lizentziaCommonsElement.checked == true)
	 {
	 	balioa=lizentziaCommonsElement.value;
	 	lizentziaF_ar.push(balioa);	 	
	 }
	  if(lizentziaCopyElement.checked == true)
	 {
	 	balioa=lizentziaCopyElement.value;
	 	lizentziaF_ar.push(balioa);	 	
	 }
	 //Beste batzuk
	  if(egunekoaElement.checked == true)
	 {
	 	balioa=egunekoaElement.value;
	 	besteF_ar.push(balioa);
	 }
	 if(proposatutakoaElement.checked == true)
	 {
	 	balioa=proposatutakoaElement.value;
	 	besteF_ar.push(balioa);
	 }
	  if(wikifikatuaElement.checked == true)
	 {
	 	balioa=wikifikatuaElement.value;
	 	besteF_ar.push(balioa);
	 }
	  if(irudiaDuElement.checked == true)
	 {
	 	balioa=irudiaDuElement.value;
	 	besteF_ar.push(balioa);
	 }
	  if(irudiaEzDuElement.checked == true)
	 {
	 	balioa=irudiaEzDuElement.value;
	 	besteF_ar.push(balioa);
	 }
	 
	 
	 var hizkuntzakF=hizkuntzakF_ar.toString(); 
	 var hornitzaileakF=hornitzaileakF_ar.toString(); 
	 var motakF=motaF_ar.toString();
	 var ordenakF=ordenaF_ar.toString();
	 var lizentziakF=lizentziaF_ar.toString();
	 var besteakF =besteF_ar.toString();
	 
	var url = 'filtro_search?hizkRadio='+hizkR+'&search_input='+galdera+'&hizkuntzakF='+hizkuntzakF+'&hornitzaileakF='+hornitzaileakF+'&motakF='+motakF+'&ordenakF='+ordenakF+'&lizentziakF='+lizentziakF+'&besteakF='+besteakF;   	
    window.location.href=url;
}
	
/* BILATZAILEAREN FILTROEN FUNTZIOAK*/

$(document).ready(function(){
    $("#hideBF").click(function(){
        $("#besteFiltroak").hide();
        $("#hideBF").hide();
        $("#showBF").show();
    });
    $("#showBF").click(function(){
        $("#besteFiltroak").show();
        $("#showBF").hide();
        $("#hideBF").show();
    });
    $("#hideLF").click(function(){
        $("#lizentziaFiltroak").hide();
        $("#hideLF").hide();
        $("#showLF").show();
    });
    $("#showLF").click(function(){
        $("#lizentziaFiltroak").show();
        $("#showLF").hide();
        $("#hideLF").show();
    });
    $("#hideOF").click(function(){
        $("#ordenaFiltroak").hide();
        $("#hideOF").hide();
        $("#showOF").show();
    });
    $("#showOF").click(function(){
        $("#ordenaFiltroak").show();
        $("#showOF").hide();
        $("#hideOF").show();
    });
    $("#hideMF").click(function(){
        $("#motaFiltroak").hide();
        $("#hideMF").hide();
        $("#showMF").show();
    });
    $("#showMF").click(function(){
        $("#motaFiltroak").show();
        $("#showMF").hide();
        $("#hideMF").show();
    });
    $("#hideHF").click(function(){
        $("#horFiltroak").hide();
        $("#hideHF").hide();
        $("#showHF").show();
    });
    $("#showHF").click(function(){
        $("#horFiltroak").show();
        $("#showHF").hide();
        $("#hideHF").show();
    });
    $("#hideHiF").click(function(){
        $("#hizkFiltroak").hide();
        $("#hideHiF").hide();
        $("#showHiF").show();
    });
    $("#showHiF").click(function(){
        $("#hizkFiltroak").show();
        $("#showHiF").hide();
        $("#hideHiF").show();
    });
});
