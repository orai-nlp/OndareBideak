var global_map;
    var layer_array = Array();
    var LeafIcon = L.Icon.extend({});    
    var markers = [];
   
    {% if non == 'itema_gehitu'  %}
        function load_map(map, options)
        {
        	
            global_map=map;
           
             // zentratu mapa erabiltzaileak 
             if(markers.length>0)
             {
                 map.panTo(new L.LatLng( markers[0].getLatLng().lat, markers[0].getLatLng().lng));
                 //document.getElementById("latitude").value = markers[0].getLatLng().lat;
                 //document.getElementById("longitude").value = markers[0].getLatLng().lng;
                 //alert(document.getElementById("longitude").value);
             }

            // maparen click eventoa 
            //map.on('click', function(e) {if(markers.length >0){map.removeLayer(markers[0]);markers=[];}; var marker = L.marker(e.latlng, { title: "Resource Location",alt: "Resource Location",riseOnHover: true,draggable: true}).on("click",function(e) {map.removeLayer(this);layer_array=jQuery.grep(layer_array, function(value) {return $(value).not([e.latlng.lat,e.latlng.lng]).length === 0 && $([e.latlng.lat,e.latlng.lng]).not(value).length === 0});}).addTo(map);layer_array.push([e.latlng.lat,e.latlng.lng]);markers.push(marker);});
			map.on('click', function(e) {if(markers.length >0){map.removeLayer(markers[0]);markers=[];}; var marker = L.marker(e.latlng, { title: "Resource Location",alt: "Resource Location",riseOnHover: true,draggable: true}).on("click",function(e) {map.removeLayer(this);layer_array=jQuery.grep(layer_array, function(value) {return $(value).not([e.latlng.lat,e.latlng.lng]).length === 0 && $([e.latlng.lat,e.latlng.lng]).not(value).length === 0});}).addTo(map);layer_array.push([e.latlng.lat,e.latlng.lng]);markers.push(marker);document.getElementById("latitude").value = e.latlng.lat;document.getElementById("longitude").value = e.latlng.lng;});
			
       		 
       	}
    {% else %}
        function load_map(map, options)
        {        	
           		map.panTo(new L.LatLng({{ geoloc_latitude|correct_float_format }}, {{ geoloc_longitude|correct_float_format }}));
           		L.marker([{{ geoloc_latitude|correct_float_format }}, {{ geoloc_longitude|correct_float_format }}]).addTo(map).openPopup();                
  		
        }
    {% endif %}
