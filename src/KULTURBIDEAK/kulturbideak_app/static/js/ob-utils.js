
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



/***************************
*    End of Utils
****************************/



function hizkuntza_url_egokitu(linka){
	
    //Hizkuntza aukeraketa egiten duen formularioaren url helbidea egokitzen du
    var form=document.getElementById("hizkuntza_aukeraketa_id");
    var hizkuntza=linka.text.toLowerCase();
    form.name="setLang"+hizkuntza;
    document.getElementsByName("language")[0].value=hizkuntza;
    document.getElementsByName("setLang"+hizkuntza)[0].submit();
    return false;

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




function nabigatu(path_id,node_id)
{

	//ALA nabigazio_item-era zuzenean?
	var url = 'nabigatu?path_id='+path_id+'&item_id='+node_id+'&autoplay=0';   	
    window.location.href=url;
	
}


function correctCssJs(elem,url)
{
	if (url.contains("DBKVisorBibliotecaWEB")){
		var toreplc = $(elem).document.head.innerHTML();
		var newhead = toreplc.replace(/\/WAS\/CORP\/DBKVisorBibliotecaWEB/g, "/kanpora/w390w.gipuzkoa.net/WAS/CORP/DBKVisorBibliotecaWEB/");
		$(elem).document.head.innerHTML(newhead);
	}
}

