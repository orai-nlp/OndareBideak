var autoplayTimeout;

function Redirect(url) 
{  
	window.location=url; 
} 
//document.write("You will be redirected to a new page in 5 seconds"); 
//setTimeout('Redirect()', 5000);   

function doSetTimeOutAutoplay(url,sec)
{
	//alert("doSetTimeOutAutoplay");
	//alert(url);
	//setTimeout('Redirect('+url+')', sec);
	autoplayTimeout= setTimeout(function(){window.location = url;}, sec);
}

function stopTimeOutAutoplay(){


    $('#autoplay-icon').className='glyphicon glyphicon-play';
    //$('#autoplay')="<span id=\"autoplay-icon\" class=\"glyphicon glyphicon-play\" aria-hidden=\"true\"></span> AUTOPLAY";
     clearTimeout(autoplayTimeout);    
}
