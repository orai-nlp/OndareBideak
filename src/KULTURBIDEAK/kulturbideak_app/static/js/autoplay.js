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
	setTimeout(function(){window.location = url;}, sec);
}
