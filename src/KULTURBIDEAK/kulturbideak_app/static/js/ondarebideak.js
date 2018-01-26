
/***************************
*    Global variables
****************************/

var serverUrl = "https://www.ondarebideak.eus"

/***************************
*    Utils
****************************/

//function to unescape html entities
function htmlDecode(input){
  var e = document.createElement('div');
  e.innerHTML = input;  
  if (e.childNodes.length === 0)
  {
      return "";
  }
  else if (e.childNodes[0].nodeValue)
  {
      //console.log("arrunta "+e.childNodes[0].nodeValue);
      return e.childNodes[0].nodeValue;
  }
  else
  {
      //console.log("aldaketarik ez");
      return input;
  }
}


//Nodoen titulutik etiketak garbitu eta Moztu 

function tituluaGarbitu (titulua,moztu){ 
            
    //console.log("garbitu hasiera - "+titulua);
    titulua=titulua.replace(/^\s+/,"");
    var tituluaJat=htmlDecode(titulua);   
    titulua=tituluaJat;
    var titulu_es="";
    var titulu_en="";
    var titulu_eu="";
   
    //espresio erregularrak erabilita hizkuntza desberdinetako tituluak atera 
    var myRegexpES = new RegExp("<div class=\"titulu_es\">(.*?)</div>");
    //var myRegexpES = /<div class=\"titulu_es\">(.*?)</div>/g;
    var match_es = myRegexpES.exec(titulua);
   
    if (match_es){      
        titulu_es=match_es[1]; //0 posizioan jatorrizkoa dago
       }
    else{
        titulu_es="";
       }
    
    var myRegexpEN = new RegExp("<div class=\"titulu_en\">(.*?)</div>");
    var match_en = myRegexpEN.exec(titulua);     
    if (match_en){
        titulu_en=match_en[1];
       }
    else{
        titulu_en="";
    }
 
    var myRegexpEU = new RegExp("<div class=\"titulu_eu\">(.*?)</div>");
    var match_eu = myRegexpEU.exec(titulua);  
    if (match_eu){
        titulu_eu=match_eu[1];
       }
    else{
        titulu_eu="";
    }
  
    //titulua= !!!erabaki defektuzkoa zein den eu,en,es
    if (titulu_eu){
        titulua=titulu_eu;
     }
    else if (titulu_es){
        titulua=titulu_es;
       }
    else{
        titulua=titulu_en;
       }
   
    //DBko tituluak hizkuntza kontrola ez baldin badu edo lg bada
    if (titulua ==""){
        titulua=tituluaJat;                
    }
    titulua=titulua.replace(/<div class=\"?titulu_lg\"?>(.*?)<\/div>/, "$1");
    
    if (moztu==true && titulua.length>25){
        return titulua.substr(0,24)+"...";
    }
    else{
        return titulua;        
    }

}

function getBrowserInfo()
{
	var ua = navigator.userAgent, tem,
	M = ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
	if(/trident/i.test(M[1]))
	{
		tem=  /\brv[ :]+(\d+)/g.exec(ua) || [];
		return 'IE '+(tem[1] || '');
	}
	if(M[1]=== 'Chrome')
	{
		tem= ua.match(/\b(OPR|Edge)\/(\d+)/);
		if(tem!= null) return tem.slice(1).join(' ').replace('OPR', 'Opera');
	}
	M = M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
	if((tem= ua.match(/version\/(\d+)/i))!= null) 
		M.splice(1, 1, tem[1]);
	return M.join(' ');
}



function correctCssJs(elem,url)
{	
	if (url.indexOf("DBKVisorBibliotecaWEB") !== -1){
		var toreplc = elem.contentDocument.head.innerHTML;
		var newhead = toreplc.replace(/\/WAS\/CORP\/DBKVisorBibliotecaWEB/g, "/kanpora/w390w.gipuzkoa.net/WAS/CORP/DBKVisorBibliotecaWEB/");
		elem.document.head.innerHTML=newhead;
	}
}

/***************************
*    End of Utils
****************************/

var paper = null;
var el_counter=0;
var svgns = "http://www.w3.org/2000/svg";
var pb_box_w = 160;
var pb_box_h = 120;
var pb_box_space = 20;//
var paths_starts = [];
var connections = [];

/* initalizations for logged and not logged users */
function initialize(){
	
	//svg-a martxan jartzeko
	set_pb();

	//kargatu workspaceko elementuak
	load_ws();
	
}
function initialize_notlogged(){
	
	//svg-a martxan jartzeko
	set_pb();
}
/* END initalizations */

function hizkuntza_url_egokitu(linka){
	
    //Hizkuntza aukeraketa egiten duen formularioaren url helbidea egokitzen du
    var form=document.getElementById("hizkuntza_aukeraketa_id");
    var hizkuntza=linka.text.toLowerCase();
    form.name="setLang"+hizkuntza;
    document.getElementsByName("language")[0].value=hizkuntza;
    document.getElementsByName("setLang"+hizkuntza)[0].submit();
    if (/cross_search/.test(window.location.href)){
    	var bilaketa=document.getElementById("search_input");
    	sdfsa 
    }
    
    return false;

}

/*workspace*/
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
				mota = items[i].getElementsByTagName("mota")[0].firstChild.data;
				//irudia hutsa baldin bada, defektuzkoa pasa
				if (irudia =="None")
				{
					irudia="/uploads/NoIrudiItem.png";
				}
				add_workspace_box(id,titulua,irudia,mota);
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
	
//if (document.getElementById("path_boxes").children[0].children[0].innerHTML == "Created with Raphaël 2.1.2"){
    if (document.getElementById("path_boxes").children[0].innerHTML == "emptySVG"){

	document.getElementById("path_boxes").removeChild(document.getElementById("path_boxes").childNodes[0]);
	if (data.length == 0){
			var root = {"id":0 ,"name" : "ROOT" , "irudia": serverUrl+"/uploads/NoIrudiItem.png", "parent":'' };
			data.push(root);
	}
	var id = element.id.substring(7,element.id.length);
	var irudia = element.children[3].src;// ws_box-ei type irudia gehitu aurretik children[2]
	var titulua = element.children[4].firstChild.data; // ws_box-ei motaren irudia gehitu aurretik children[3]
	
	var mota = element.children[1].firstChild.attributes[1].nodeValue;	
	mota = mota.split("/").pop().split(".")[0].toUpperCase();
	
	//var svg = document.getElementById("path_boxes").children;
	var obj={id: id, name: titulua , irudia: irudia, parent:0, mota: mota};
	data.push(obj);
	sortu(data);//funtzio hau d3ondarebideaksortu.js barruan dago.
	remove_me(element,item_id);
} else {
	
    var id = element.id.substring(7,element.id.length);
	var irudia = element.children[3].src;// ws_box-ei motaren irudia gehitu aurretik children[2]
	var titulua = element.children[4].firstChild.data;//children[3]
	
	var mota = element.children[1].firstChild.attributes[1].nodeValue;
	mota = mota.split("/").pop().split(".")[0].toUpperCase();
	
	//var svg = document.getElementById("path_boxes").children;
	var obj={id: id, name: titulua , irudia: irudia, parent:0, mota: mota};
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
    var mota = document.getElementById("mota_"+index).value;
    
    //Titulua garbitu eta laburtu
    titulua=tituluaGarbitu(titulua,false);  
      
   	//Titulua laburtu?
    //titulua_subs = titulua.substr(0, 20);  
    //titulua = titulua_subs + "...";
    
    
    if (irudia == "" || irudia == "None"){
    	irudia="/uploads/NoIrudiItem.png";
   	}
    //Ondoren user id-aren arabera WS-id-a lortu
   	
    var uri="uri_"+item_id;
    var dc_source="kk";
    var dc_title=titulua;
    var dc_description="description";
    var type=mota;
    //alert (type);
    var paths_thumbnail=irudia;
   	//  workspace_item taula:item_id, item_uri, ws_id, item_dc_source, item_dc_title, item_dc_descriptioon, type, thumnail
  	
  	//AJAX
  	start_loader("loader");                             
	if (item_id != ""){		                                       
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
            create_workspace_box_answer(xmlHttp,item_id,dc_title,paths_thumbnail,type);                                                                   
        };
        xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlHttp.send("item_id="+item_id+ "&uri=" + uri + "&dc_source=" + dc_source + "&dc_title=" + encodeURIComponent(dc_title) + "&dc_description=" + encodeURIComponent(dc_description) + "&type=" + type + "&paths_thumbnail=" + encodeURIComponent(paths_thumbnail) + "&csrfmiddlewaretoken=" + csrftoken);                     
    }
	
	
}
//create workspace box answer
function create_workspace_box_answer(xmlHttp,item_id,titulua,irudia,mota){
    
    if (xmlHttp.readyState == 4){
        if(xmlHttp.status == 200){
    		var item_id_server = server_answer(xmlHttp);
    		
            if (item_id_server !=0 ){ //WS-an Errepikatua sartzean saiatzen denean 0 izango da  
         
            	//Datu-basean sartu den Id-a nahi dut
            	add_workspace_box(item_id,titulua,irudia,mota);
			}
			else{
				//Jadanik sartu duela esan erabiltzaileari                                                                                            // Jaso beharreko emaitza lortu ez bada, errorea
				var mytext = "Jadanik sartu duzu item hau";
				//document.getElementById("errepikatua").innerHTML = "Jadanik sartu duzu item hau!";
				//alert("Jadanik sartu duzu item hau");
			}
			stop_loader("loader");                                                                              // Emaitza ona edo txarra jaso bada, loaderra paratu
        }
    }
}

function add_workspace_box(box_id,text_value,image_value,mota){
	
	
	var ws = document.getElementById("workspace_boxes");
	
    //KONPROBATU ID BERDINA DUEN ITEMA JADANIK MARRAZTUTA EZ DAGOELA!!
    var checkId="ws_box_"+box_id;
    var myElem = document.getElementById("ws_box_"+box_id);
    
    if (myElem === null)
    {
    var ws_box = document.createElement("div");
    ws_box.setAttribute("id","ws_box_" + box_id);
    //ws_box.setAttribute("id", box_id); //aldaketa
    ws_box.setAttribute("class","ws_box");
    ws_box.setAttribute("title",text_value); //onMouseOver titulu osoa erakusteko
    ws_box.setAttribute("draggable","true");
    ws_box.addEventListener('dragstart',drag);
    ws_box.addEventListener('dragenter',wsb_handleDragEnter);
    ws_box.addEventListener('dragleave',wsb_handleDragLeave);

    
    //Motaren arabera irudia agertzeko    
    var wsb_typeImage = document.createElement("div");
    wsb_typeImage.setAttribute("class","wsb_typeImage");
    var typei=document.createElement("i");
    typei.setAttribute("class","icon-ob-"+mota.toLowerCase()+" kolore-"+mota.toLowerCase());
    wsb_typeImage.appendChild(typei);
    ws_box.appendChild(wsb_typeImage);
    
    var wsb_button = document.createElement("span");
    wsb_button.setAttribute("class","wsb_button");
    wsb_button.setAttribute("onclick","remove_me(this.parentNode,"+box_id+");");
    wsb_button.setAttribute("title","Ezabatu");
    var trashglyph = document.createElement("span");
    trashglyph.setAttribute("class","icon-ob-trash");
    trashglyph.setAttribute("aria-hidden","true");
    wsb_button.appendChild(trashglyph);
    /*wsb_button.appendChild(document.createTextNode("Ezabatu"));*/
    ws_box.appendChild(wsb_button);
    
   
    
    
    if ((new RegExp("sortu_ibilbidea$").test(window.location.href) == true) || (new RegExp("editatu_ibilbidea").test(window.location.href) == true)){
    	var wsb_button2 = document.createElement("span");
	wsb_button2.setAttribute("class","wsb_button");
	wsb_button2.setAttribute("onclick","add_me_to_the_SVG(this.parentNode,"+box_id+");");
	wsb_button2.setAttribute("title","Arbelera");
	/*wsb_button2.appendChild(document.createTextNode("Arbelera"));*/
	var arrowglyph = document.createElement("span");
	arrowglyph.setAttribute("class","glyphicon glyphicon-arrow-down");
	arrowglyph.setAttribute("aria-hidden","true");
	wsb_button2.appendChild(arrowglyph);

	    ws_box.appendChild(wsb_button2);
    } else {  
    }
    var wsb_image = document.createElement("img");
    wsb_image.setAttribute("class","wsb_image border-"+mota.toLowerCase());
    var image_value2=image_value.replace("http://www.http","http"); //konponketa
    image_value=image_value2;
    wsb_image.setAttribute("src",image_value);
   
    ws_box.appendChild(wsb_image);

    var wsb_title = document.createElement("span");
    wsb_title.setAttribute("class","wsb_title");
   
    //Titulua Garbitu eta Laburtu
    text_value = tituluaGarbitu(text_value,true);  
   
    wsb_title.appendChild(document.createTextNode(text_value));
    ws_box.appendChild(wsb_title);

    ws.appendChild(ws_box);
    }//Bi aldiz ez marrazteko elementu berdina (batzutan behin klikatuta 2 aldiz marrazten da eta)
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


/**
 * Hainbat funtzio orria kargatutakoan exekutatu beharrekoak
 * */

//Ibilbidearen edizio aukerak AJAX bidez aldatzen ditu datu-basean
$(document).ready(function(){
	
$('#pathEdizioAukerakEguneratu').submit(function(e) {

   var path_id = document.getElementById("pathId").value;
   var edizioZbk = document.getElementById("acces").value;
  
   var form = $(this);      
   var formdata = false;
   if(window.FormData){
     formdata = new FormData(form[0]);
                   
     }
	
   var formAction = form.attr('action');

                $.ajax({
                    type        : 'POST',
                    url         : '../ajax_path_edizio_aukerak_aldatu',
                    cache       : false,
                    data        : formdata ? formdata : form.serialize(),
                    contentType : false,
                    processData : false,
					dataType	: 'html',
					
                    success: function(data,status,xhr)  {
                        if(response != 'error') {
                           
                            var response = $(data+" p").text();
                         
                           
                           $('#modalEdizioAukerak').modal('hide');
                        } else {
                            $('#messages').addClass('alert alert-danger').text(response);
                        }
                    }
                });
                e.preventDefault();          
 });
   
});




$(document).ready(function(){
   $(".announce").click(function(){ // Click to only happen on announce links
   	 
     $("#pathId").val($(this).data('id'));
     $('#modalEdizioAukerak').modal('show');
  
   });
});

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
					dataType	: 'html',
					
                    success: function(data,status,xhr)  {
                        if(response != 'error') {
                            //$('#messages').addClass('alert alert-success').text(response);
                            // OP requested to close the modal
                            var response = $(data+" p").text();
                            //GAINONTZEKO METADATUAK GORDE : TITULUA, GAIA, DESK
                           create_path_on_db(response);
                           //Mezua idatzi pantailan
                           $('.info').prepend("<div id='interaction_message' class='alert alert-info'> Ibilbidea ongi sortu da</div>");
                          	
                           
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
		    		dataType	: 'html',

                    success: function(data,status,xhr) { //response
                        if(response != 'error') {
                            //$('#messages').addClass('alert alert-success').text(response);
                            // OP requested to close the modal
                            var response = $(data+" p").text();
                            //GAINONTZEKO METADATUAK GORDE : TITULUA, GAIA, DESK,HIZK
                           update_path_on_db(path_id,response);                           
                          	$('.info').prepend("<div id='interaction_message' class='alert alert-info'> Ibilbidea ongi eguneratu da</div>");
                          	//window.location.reload(true);
                          	document.getElementById("create_path_button").setAttribute("disabled","disabled");
                           //$('#myModal').modal('hide');
                        } else {
                            $('#messages').addClass('alert alert-danger').text(response);
                        }
                    }
                });
                e.preventDefault();
            });
   
});


//Autocomplete-aren leihoa ongi kokatzeko.
$(document).ready(function(){
	pos = $("#search-box").offset();
	$("#autocomplete-container").css({
		left: (pos.left-10) + "px"		
	});/*not sure why but the autocomplete-container is shown 10px to the right. Thus the correction*/
	//console.log("autocomplete lehioaren posizioa aldatuta:"+$("#autocomplete-container").css('left'));
});


/**
 * 
 * IBILBIDEA SORTZEKO FUNTZIOAK
 * 
 */


function create_path_on_db(paths_thumbnail_name)
{
		
	var dc_title = document.getElementById("path_titulua").value;
	var dc_description = document.getElementById("path_desk").value;
	var dc_subject = document.getElementById("path_gaia").value;
	//var paths_thumbnail = document.getElementById("file2");
	//var paths_thumbnail_name=paths_thumbnail.value;
	var hizkuntza =document.getElementById("hizkuntza").value;
	var acces =document.getElementById("acces").value; //1,2,3,4
	
	
	
	start_loader("loader");  
	
	uri="urii";
   
    //paths_thumbnail = "";   //MEDIA_URL+edm_object           , parametro bezala pasa MEDIA_URL                                                                             // beharrezko baldintzak jaso
	
	//if (paths_starts.length > 0){
		                                            
		create_path_on_db_request(uri,dc_title,dc_subject,dc_description,paths_thumbnail_name,hizkuntza,acces);                                  
	//}
	//else{                                                                                                       // baldintzak bete ez badira
		//alert("empty_path_error");                                                                  // (aukeran) errorea 
	//}
	stop_loader("loader");                                                                                      // loaderra gelditu

}

function create_path_on_db_request(uri,dc_title,dc_subject,dc_description,paths_thumbnail_name,hizkuntza,acces)
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
        xmlHttp.send("uri="+uri+"&dc_title="+dc_title+"&dc_subject="+dc_subject+"&dc_description="+dc_description+"&paths_thumbnail="+paths_thumbnail_name+"&hizkuntza="+hizkuntza+"&acces="+acces+"&csrfmiddlewaretoken=" + csrftoken);                     
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
	var toprocess=new Array();
	toprocess.push.apply(toprocess,root.children);
	while (toprocess.length>0){	
	    var currentN = toprocess.shift();
	    var obj={id: currentN.id, name: currentN.name , irudia: currentN.irudia , narrazioa: currentN.narrazioa ,  parent:currentN.parent.id , children:currentN.children};
	    json.push(obj);
	    if (currentN.children != null && typeof currentN.children == 'object')
	    {
		toprocess.push.apply(toprocess,currentN.children);
	    }
	}
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
		var dc_source="";
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
        xmlHttp.send("path_id="+path_id+"&item_id="+item_id.replace("pb_","")+"&uri="+uri+"&dc_source="+dc_source+"&dc_title="+encodeURIComponent(dc_title)+"&dc_description="+encodeURIComponent(dc_description)+"&type="+type+"&paths_thumbnail="+encodeURIComponent(paths_thumbnail)+"&paths_prev="+paths_prev.replace("pb_","")+"&paths_next="+paths_next.replace("pb_","")+"&paths_start="+paths_start+"&csrfmiddlewaretoken=" + csrftoken); 																																			

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
               	//HEMEN node_tmp-ko tuplak ezbatu beharko lirateke
            	
            	
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

function update_path_on_db(path_id,paths_thumbnail_name)
{
	
	var dc_title = document.getElementById("path_titulua").value;
	var dc_description = document.getElementById("path_desk").value;
	var dc_subject = document.getElementById("path_gaia").value;
	//var paths_thumbnail = document.getElementById("file2");
	//var paths_thumbnail_name=paths_thumbnail.value;	
	var hizkuntza =document.getElementById("hizkuntza").value;
	var acces =document.getElementById("acces").value;
	
	
	start_loader("loader");
	//if (paths_starts.length > 0){		                                            
		update_path_on_db_request(path_id,dc_title,dc_subject,dc_description,paths_thumbnail_name,hizkuntza,acces);                                  
	//}
	//else{                                                                                                      
	//	alert("empty_path_error");                                                                
	//}
	//stop_loader("loader");   
}

function update_path_on_db_request(path_id,dc_title,dc_subject,dc_description,paths_thumbnail_name,hizkuntza,acces)
{
	var csrftoken = getCookie('csrftoken');
	var xmlHttp = createXmlHttpRequestObject();
	//alert(paths_thumbnail_name);
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
        xmlHttp.send("path_id="+path_id+"&dc_title="+dc_title+"&dc_subject="+dc_subject+"&dc_description="+dc_description+"&paths_thumbnail="+paths_thumbnail_name+"&hizkuntza="+hizkuntza+"&acces="+acces+"&csrfmiddlewaretoken=" + csrftoken);                     
    	
    
    }
	
}


function update_path_on_db_answer(xmlHttp,path_id)
{
	if (xmlHttp.readyState == 4){
        if(xmlHttp.status == 200){
    		var path_id = server_answer(xmlHttp);
            if (path_id){ 
            
            	//ORAIN NODE TAULA EGUNERATU
            	//update_path_nodes(path_id);
				create_path_nodes(path_id);
            	
            	
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
		alert("nodoa eguneratuuu");
		
		alert(dc_description);
		
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
        document.getElementById("path_boxes").innerHTML="<svg>emptySVG</svg>";
        
    }
}

/**
 *  * END ibilbidea sortzeko funtzioak
 *  * 
 * **/



function nabigatu(path_id,node_id)
{

	//ALA nabigazio_item-era zuzenean?
	var url = 'nabigatu?path_id='+path_id+'&item_id='+node_id+'&autoplay=0';   	
    window.location.href=url;
	
}


/**
 *  Eguneko item/pathak kargatzeko funtzioa (cross_search.html)
 *   
 * **/

function ajax_egunekoak_lortu(){
	// load from AJAX
    $.ajax({
        method : 'GET',
        url : '/ajax_egunekoak',
        dataType : 'html',
        data : {
        }
    }).done(function(data) {
        $("#modalEgunekoak").html(data);                
        $("#modalEgunekoak").modal('show');
    });
}


/** END Eguneko item/pathak kargatzeko funtzioa (cross_search.html) */


/**
 * 
 * Eguneko item/path-en aldaketak ajax bidez
 * 
 * */

function egunekoaAldatu(item_id,aldaketa,type)
{
	$('#loading_modal').modal('show');
	// load from AJAX
    $.ajax({
        method : 'GET',
        url : '/ajax_egunekoa_aldatu_item',
        dataType : 'html',
        data : {
            id : item_id,
            aldaketa: aldaketa,
            itype: type
        }
    }).done(function(data) {
    	//var response = $($.parseHTML(data));
    	//var buttonLi = response[0].innerHTML;
    	var bckclass=$('#eguneko_button_'+item_id).attr('class').split(/\s+/)[0];
    	var bckCircle=$('#eguneko_button_'+item_id+' span[class^=ob-fire-overlay]')
		.attr('class').split(/\s+/)[0];
    	$('#eguneko_button_'+item_id).html(data);
    	$('#eguneko_button_'+item_id+' span.square-back-vert-padding').addClass(bckclass);
    	var plusminus = $('#eguneko_button_'+item_id+' span.backgrnd-txuria.kolore-gris-lau')
    	var current=plusminus.attr('class');
    	var addto = bckCircle+' '+current;
    	plusminus.attr('class',addto);
        if (aldaketa == "gehitu"){
        	$('#chosen-item-mark').show();
        }
        else {
        	$('#chosen-item-mark').hide();
        }
        $('#loading_modal').modal('hide');
    });
	
}    

function egunekoaAldatu_ibilb(path_id,aldaketa)
{
	$('#loading_modal').modal('show');
	// load from AJAX
    $.ajax({
        method : 'GET',
        url : '/ajax_egunekoa_aldatu_path',
        dataType : 'html',
        data : {
            id : path_id,
            aldaketa: aldaketa
        }
    }).done(function(data) {
    	//var response = $($.parseHTML(data))
    	//var buttonLi = response[0].innerHTML;
    	var bckclass=$('#eguneko_button_'+path_id).attr('class').split(/\s+/)[0];   
    	var bckCircle=$('#eguneko_button_'+path_id+' span[class^=ob-fire-overlay]')
    					.attr('class').split(/\s+/)[0];
        $('#eguneko_button_'+path_id).html(data);
    	$('#eguneko_button_'+path_id+' span.square-back-vert-padding').addClass(bckclass);
    	var plusminus = $('#eguneko_button_'+path_id+' span.backgrnd-txuria.kolore-gris-lau')
    	var current=plusminus.attr('class');
    	var addto = bckCircle+' '+current;
    	plusminus.attr('class',addto);
        if (aldaketa == "gehitu"){
        	$('#chosen-item-mark').show();
        }
        else {
        	$('#chosen-item-mark').hide();
        }
        $('#loading_modal').modal('hide');
    });
	
}    

/** END Eguneko item/path-en aldaketak bertsio berria ajax bidez */


function bilaketaFiltratu_db()
{
	$('#loading_modal').modal('show');
	var search_lang = document.getElementById('search_lang')
	var hizkR=search_lang.value;
	var galdera = document.getElementById('search_input').value;
	var hornitzailea = document.getElementById('hornitzailea_username').value;
	var hornitzailea_user_id = document.getElementById('hornitzaile_search').value;
	var nireak = document.getElementById('nireak').value;

	//Momentuan aktibo dagoen tab-a zein den jakiteko
	var tabText=$('.nav-tabs .active').text();	
	var z="";
	if (tabText.includes("item") || tabText.includes("Items") || tabText.includes("Itemak") ){
		//hizkuntza desberdinetan egon daiteke: Kultur itemak, Cultural items, Items culturales, Items culturelles
	 	z= "i";
	}
	else if (tabText.includes("Ibilbide") || tabText.includes("Recorridos") ||tabText.includes("Paths") || tabText.includes("Itin")){
	 	z= "p";
	}
	else{
	 	z= "h";
	}
	
	var hizkuntzakF_ar = []; 
	var hornitzaileakF_ar = [];
	var motaF_ar = [];
	var ordenaF_ar = [];
	var lizentziaF_ar = [];
	var besteF_ar = [];
	
	//Hizkuntzak
	var EuhizkElement = document.getElementById('hizkuntza-eu');
	var EshizkElement = document.getElementById('hizkuntza-es');
	var EnhizkElement = document.getElementById('hizkuntza-en');
			
	//Ordena
	var dataOrdenaElement = document.getElementById('ordena-dataDesc');
	var data2OrdenaElement = document.getElementById('ordena-dataAsc');
	var botoOrdenaElement = document.getElementById('ordena-botoak');
	
	
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
	 db_hornitzaileak_text=document.getElementById('db_hornitzaileak_text').value;
	 db_hornitzaileak=db_hornitzaileak_text.split("_");
	 for (var i = 0, length = db_hornitzaileak.length; i < length; i++) 
		{
			horniId=db_hornitzaileak[i];			
			var horniElement=document.getElementById(horniId);
			
			if(horniElement.checked == true)
	 		{ 			
	 			balioa=horniElement.value;
	 			hornitzaileakF_ar.push(balioa);
	 		}
			
   	 	}
   	 
	 //MOTA
	 db_motak_text=document.getElementById('db_motak_text').value;
	 db_motak=db_motak_text.split("_");
	 for (var i = 0, length = db_motak.length; i < length; i++) 
		{
			motaId=db_motak[i];
			var motaElement=document.getElementById(motaId);
			if(motaElement.checked == true)
	 		{	 			
	 			balioa=motaElement.value;
	 			motaF_ar.push(balioa);
	 		}
			
   	 	}
   	 //LIZENTZIA
	 db_lizentziak_text=document.getElementById('db_lizentziak_text').value;
	 db_lizentziak=db_lizentziak_text.split("_");
	 
	 for (var i = 0, length = db_lizentziak.length; i < length; i++) 
		{
			lizentziaId=db_lizentziak[i];	
			var lizentziaElement=document.getElementById(lizentziaId);
			
			if(lizentziaElement.checked == true)
	 		{	 	
	 			balioa=lizentziaElement.value;
	 			lizentziaF_ar.push(balioa);
	 			
	 		}
				
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
	
	
	var url = 'filtro_search?hornitzailea_user_id='+hornitzailea_user_id+'&hornitzailea='+hornitzailea+'&z='+z+'&search_lang='+hizkR+'&search_input='+galdera+'&hizkuntzakF='+hizkuntzakF+'&hornitzaileakF='+hornitzaileakF+'&motakF='+motakF+'&ordenakF='+ordenakF+'&lizentziakF='+lizentziakF+'&besteakF='+besteakF+'&nireak='+nireak;   	
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

//Ibilbidea eta itema ezbatzeko funtzioak
function deletePath(id){
    var conf = confirm("Ziur zaude ibilbidea ezabatu nahi duzula?");
    if(conf == true){
        alert("Ados...ibilbidea ezabatuko da ");
        var url = 'ezabatu_ibilbidea?id='+id;   	
    	window.location.href=url;
    }
}
function deleteItem(id){
    var conf = confirm("Ziur zaude kultur itema ezabatu nahi duzula?");
    if(conf == true){
    	$.ajax({
            method : 'GET',
            url : '/ezabatu_itema',
            dataType : 'html',
            data : {
                id : id
            }
        }).done(function(data) {
        	var msgdiv = "<div class=\"alert alert-info col-xs-12 col-md-8 col-md-offset-2\" role=\"alert\">" +
        			"<strong>"+data[0]+".</strong>" +
        			"<a id=\"alert-close-button\" type=button " +
        			"onClick=\"$(this).parent().slideUp();return False;\">" +
        			"<i class=\"icon-ob-times eskuma\"></i></a></div>";
            $('#content-div').prepend(msgdiv);
        });
        //alert("Ados...itema ezabatuko da ");
        //var url = 'ezabatu_itema?id='+id;   	
    }
}

//"intermitente " efektua emateko elementu bati
setInterval(function(){blink()}, 1000);


    function blink() {
    	//.fadeTo(100, 0.1).fadeTo(200, 1.0);
        $("#div_you_want_to_blink").fadeTo(1000, 0.5).fadeTo(2000, 1.0);
    }
    
    
/**
 * ADMIN : berria edition modal opening
 */
function load_berria_form(id) {
    // load from AJAX
    $.ajax({
        method : 'GET',
        url : '/berria_form',
        dataType : 'html',
        data : {
            id : id
        }
    }).done(function(data) {
        $('.erabmodal-container').parent().html(data);
    });
}    


/**
 * ADMIN : user edition modal opening
 */
function load_erab_form(id) {
	// load from AJAX
    $.ajax({
        method : 'GET',
        url : '/erab_form',
        dataType : 'html',
        data : {
            id : id
        }
    }).done(function(data) {
        $('.erabmodal-container').parent().html(data);
    });
}    
    
/**
 * ADMIN : user password reseting opening
 */
function load_changePass_confirmation(id) {
 	
 	var conf = confirm("Ziur zaude erabiltzaile honen pasahitza berrasieratu nahi duzula?");
    if(conf == true){
        alert("Ados...pasahitz berria sortuko da eta erabiltzaileari postaz abisatuko zaio ");
        var url = 'admin_reset_user_password?id='+id;   	
    	window.location.href=url;
    }
}  

/**
*ADMIN: aldatu hornitzailearen eguneko egoera
*/

function aldatu_hornitzaile_egoera(id)
{
	var url = 'admin_eguneko_hornitzaileak_kudeatu?id='+id;   	
    window.location.href=url;
}





