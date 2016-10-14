/***************************
*    Utils
****************************/
// function to get multiline labels for d3 svg text elements
function insertLineBreaksD3(d) {
    var el = d3.select(this);
    el.attr("stroke", function(d) {
        return "black";
    });
    var words = d.split(/[_ ]/);
    el.text('');

    for (var i = 0; i < words.length; i++) {
        // if a word is too short (<3 chars) append it to the next element
        //if (words[i].length<3 && i< words.length-1){
        //    words[i+1]=words[i]+" "+words[i+1];
        //    continue;
        //}
        
	if (i>= words.length/2){
            var tspan = el.append('tspan').text(words[i]);
            if (i > 0)
		tspan.attr('x', 0).attr('dy', '15');
	}
    }
}

//function to unescape html entities
function htmlDecode(input){
  var e = document.createElement('div');
  var pre_cleaning = input.replace(/&amp;/g,"&").replace(/&amp;/g,"&");
  e.innerHTML = pre_cleaning;   
  var result ="";
  if (e.childNodes.length === 0)
  {
      return result;
  }
  else if (e.childNodes[0].nodeValue)
  {
      //console.log("arrunta "+e.childNodes[0].nodeValue);
      result = e.childNodes[0].nodeValue;      
      return result.replace(/http:\/\/www.http\/\//, "http://");
  }
  else
  {
      //console.log("aldaketarik ez");
      return input;
  }
}


//Maddalen: Nodoen titulutik etiketak garbitu eta Moztu 

function tituluaGarbitu (titulua,moztu){ 
        
    titulua=titulua.replace(/^\s+/,"");
    var tituluaJat=htmlDecode(titulua);
    titulua=tituluaJat;
    var titulu_es="";
    var titulu_en="";
    var titulu_eu="";
   
    //console.log(titulua);
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
    var match_en = myRegexpES.exec(titulua);     
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
    titulua=titulua.replace(/<div class=\"titulu_lg\">(.*?)<\/div>/, "$1");
    
    if (moztu==true && titulua.length>25){
        return titulua.substr(0,24)+"...";
    }
    else{
        return titulua;        
    }

}



/***************************
*    End of Utils
****************************/


var data = ibilbide_data;
//console.log(data);
var path_id = path_id;

// *********** Convert flat data into a nice tree ***************
// create a name: node map
var dataMap = data.reduce(function(map, node) {
    //node.id: id-ak erabiliko ditu loturak sortzeko.
    map[node.id] = node;
    return map;
}, {});

// create the tree array
var treeData = [];
data.forEach(function(node) {
    // add to parent

    var parent = dataMap[node.parent];
    if (parent) {
        // create child array if it doesn't exist
        (parent.children || (parent.children = []))
            // add node to child array
            .push(node);
    } else {
        // parent is null or missing
        treeData.push(node);
    }
});



// ************** Generate the tree diagram  *****************
//var divWidth = d3.select('#path_boxes_overview').style('width').substr(0,d3.select('#path_boxes_overview').style('width').length-2);
var divWidth = document.getElementById('path_boxes_overview').offsetWidth;
divWidth=900;
divWidth = divWidth-(divWidth*0.04);
//var divHeight = d3.select('#path_boxes_overview').style('height').substr(0,d3.select('#path_boxes_overview').style('height').length-2);
var divHeight = document.getElementById('path_boxes_overview').offsetHeight;
divHeight=600;
divHeight = divHeight-(divHeight*0.1);

var margintop = 0;
var marginbottom = 40;
var modal= document.getElementById('modaloverview');
if (modal != null)
{
    margintop=0;
    marginbottom=40;
}
//Maddalen: top:20 zegoen lehen, baina modalean ondo ikusteko aldatu dut
var margin = {top: margintop, right: 120, bottom: marginbottom, left: 40},
    width = divWidth - margin.right - margin.left,
    height = divHeight - margin.top - margin.bottom;
    //height = divHeight - 50 - 20;
    
var i = 0;
var duration = 750;
var viewerWidth =  0;
var viewerHeight = width;
var newHeight = 4;
//Nodoen tamaina
var radio = 20;
//Link-en luzera
var luzera = radio +20
//var luzera = 45;

var tree = d3.layout.tree()
    .size([width,height]);
console.log("w "+width+" -  h "+height);
console.log("path-overview - w "+divWidth+" -  h "+divHeight);
var diagonal = d3.svg.diagonal()
    .projection(function(d) { 
        return [d.y-luzera, d.x]; });

var svg = d3.select("#path_boxes_overview").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .attr("class","clearfix")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    function click() {
        /*////////////////////////////////////////////////////////////*/
      var p = d3.select(this);
      if (p.select("circle").classed("aukeratuta") == true){
        //NODOA EZ DAGO AUKERATUTA
        d3.selectAll("circle").style({stroke: 'steelblue'});
        p.select("circle").style({stroke: 'red'});
        p.select("circle").classed("aukeratuta",false);
      } else {
        p.select("circle").style({stroke: 'steelblue'});
        p.select("circle").classed("aukeratuta",true);
      }
      
      /*****************ONDO DOA**********************************/
      //falta da href
        /****************************************************************/
        }

    function zoom() {
        svgGroup.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    }


    // define the zoomListener which calls the zoom function on the "zoom" event constrained within the scaleExtents
    var zoomListener = d3.behavior.zoom().scaleExtent([0.1, 3]).on("zoom", zoom);

    function centerNode(source) {
        scale = zoomListener.scale();//0.4
        x = -source.y0;
        y = -source.x0;
        x = x * scale + divWidth / 2;
        y = y * scale + divHeight / 2;
        d3.select('g').transition()
            .duration(duration)
            .attr("transform", "translate(" + 0 + "," + 0 + ")scale(" + scale + ")");
        zoomListener.scale(scale);
        zoomListener.translate([x, y]);


    } 
            



/*
    if interfaceLang == "eu":
         
        if titulu_eu != "":
            return titulu_eu          
        else:        
            return titulua
    if interfaceLang == "es":
        if titulu_es != "":
            return titulu_es          
        else:        
            return titulua
                
    if interfaceLang == "en":
         
        if titulu_en != "":
            return titulu_en          
        else:        
            return titulua
	*/

//Root da zuhaitzaren aita

var svgGroup = svg.append("g");
root = treeData[0];
root.x0 = 0;
root.y0 = height/2;
update(root);
centerNode(root);

function update(source) {

  // Compute the new tree layout.
  var nodes = tree.nodes(root).reverse(),
      links = tree.links(nodes);
      //ezabatu root


      nodes.pop();
      nodes.reverse();


  // Normalize for fixed-depth.
  nodes.forEach(function(d) { 
    d.y = d.depth * 100;});

  // Nodoak deklaratu
    var node = svg.selectAll("g.node")
      .data(nodes, function(d) { return d.id || (d.id = ++i); });

  // Nodoak sartu.
  var nodeEnter = node.enter().append("g")
    .attr("class", "node")
      .attr("transform", function(d) {
                    var a = d.y-10;
                    return "translate(" + a + "," + d.x + ")";
            })
      .append("a")
      //nabigatu?path_id='+path_id+'&item_id='+node_id+'&autoplay=0'
        .attr("xlink:href", function(d) {
     return "/nabigatu?path_id="+path_id+"&item_id="+d.id; })
      .on('click', click);
      

  //Nodoen Gainean Sagua jarritakoan Nodoaren Titulu osoa erakutsiko da        
	nodeEnter.append("svg:title").text(function(d) {
                return tituluaGarbitu(d.name,false);  });
    
  nodeEnter.append("circle")
    .attr("id",function(d) {
     return 'nodo: '+tituluaGarbitu(d.name,false); }) //Maddalen
    .attr("class", "aukeratuta")
    .attr("r", function(d){
            return radio;
    })
    .style("stroke", function(d){ 
        var id_url = window.location.href.substr((window.location.href.indexOf("item_id=")+8),window.location.href.length);
            
        if (id_url.indexOf("&")>0){
            var id_url = id_url.substr(0,id_url.indexOf("&"));
        } else {

        }
        //ROOT-EN SEMEA BADA EDO URL-EAN ITEM_ID-RIK EZ BADAGO
        if (d.parent.name == "ROOT" && window.location.href.indexOf("item_id=")==-1){
        //URL-KO ITEM_ID-A NODOAREN ID-A BADA ORDUAN GORRIZ MARGOTUKO DU.    
                if (d.id == id_url){
                    return 'red';
                }
            
        } else {
        //URL-KO ITEM_ID-A NODOAREN ID-A BADA ORDUAN GORRIZ MARGOTUKO DU.
            if (d.id == id_url){
                return 'red';
            }
        }})            
        .style("fill", function(d) { 
            var ir = "#"+d.id;
            return  "url("+ir+")";});


        nodeEnter.append('defs')
            .append('pattern')
            .attr('id', function(d) { return (d.id);})
            .attr('width', 1)
            .attr('height', 1)
            .attr('patternContentUnits', 'objectBoundingBox')
            .append("svg:image")
                .attr("xlink:xlink:href", function(d) { return htmlDecode(d.irudia);}) // "icon" is my image url. It comes from json too. The double xlink:xlink is a necessary hack (first "xlink:" is lost...).
                .attr("x", 0)
                .attr("y", 0)
                .attr("height", 1)
                .attr("width", 1)
                .attr("preserveAspectRatio", "xMinYMin slice");                  
  
  //Testua gehitu  
  /*nodeEnter.append("text")
      .attr("x", function(d) { 
          return d.children || d._children ? (radio+luzera)/2 : -(radio+luzera)/2; }) // lehen 35: -35
      .attr("dy", function(d) {
            return d.children || d._children ?  (radio+15) : (radio+15); //lehen 30 : 30
    })
      .attr("text-anchor", function(d) { 
          return d.children || d._children ? "end" : "start"; })
      .text(function(d) { return tituluaGarbitu(d.name,true);}) //Maddalen
      .style("fill-opacity", 1);
*/
  nodeEnter.append("foreignObject")
      .attr("x", function(d) { 
          return -radio-luzera/2; }) // lehen 35: -35
      .attr("y", function(d) {
            return radio; //lehen 30 : 30
    })
      .attr("width",function ( d, i ) { return radio*2.1+luzera;})
      .attr("height",function ( d, i ) { return 38;})
      .attr("text-anchor", function(d) { 
          return d.children || d._children ? "end" : "start"; })
          .append("xhtml:body")
          .attr("xmlns","http://www.w3.org/1999/xhtml")
          .attr("title",function(d) { return tituluaGarbitu(d.name,false);})
          .style("background","transparent")
          .append("p")
            .text(function(d) { return tituluaGarbitu(d.name,true);}) //Maddalen
            .style("fill-opacity", 1)
                .attr("class","d3label");



        var nodeUpdate = node.transition()
            .duration(duration)
        .attr("transform", function(d) {
            if (d.parent.name == "ROOT"){
                var a = (d.y*0.8)-20;
                var b = d.x*0.8;
                return "translate(" + a + "," + b + ")scale(" + 0.8 + ")";
            } else if (nodes.length>=10){
                var a = (d.y*0.8)-10;
                var b = d.x*0.8;
                return "translate(" + a + "," + b + ")scale(" + 0.8 + ")"; 
            } else {
                var a = (d.y*0.8)-10;
                var b = d.x*0.8;
                return "translate(" + a + "," + b + ")scale(" + 0.8 + ")";
            }
        }); 

        nodeUpdate.select("text")
            .style("fill-opacity", 1);

         var nodeExit = node.exit().transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + source.y + "," + source.x + ")";
            })
            .remove();
            
               nodeExit.select("circle")
            .attr("r", 0);

        nodeExit.select("text")
            .style("fill-opacity", 0);                   


  // Estekak deklaratu
  var link = svgGroup.selectAll("path.link")
      .data(links, function(d) { return d.target.id; });
        link.enter().insert("path", "g")
            .attr("class", "link")
            .style("opacity", function(link){ 
                //ROOT BADA IZKUTATUKO DU ETA BESTELA ERAKUTSIKO DU.
                if (link.source.name == "ROOT" ){
                    return 0;
                } else {
                    return 1;
                } })
            .attr('stroke-width', 2)
            .attr("marker-end", "url(#arrowhead)")
            .attr("transform", "translate(" + 0 + "," + 0 + ")scale(" + 0.8 + ")"); 

        // Transition links to their new position.
        link.transition()
            .duration(750)
            .attr("d", diagonal);

        // Transition exiting nodes to the parent's new position.
        link.exit().transition()
            .duration(750)
            .attr("d", function(d) {
                var o = {
                    x: source.x,
                    y: source.y
                };
                return diagonal({
                    source: o,
                    target: o

                });
            })
            .remove();            

//NODOEN POSIZIOA (transform="translate(dx0,dy0)")
//PAUSO HONETAN NODOAK dx,dx0,dy eta dy0 baloreak ditu.
        nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
        });


//GEZIA jarri link-ari
        svg.append("defs").append("marker")
        .attr("id", "arrowhead")
        .attr("refX", 0)
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 4)
        .attr("viewBox", "0 -5 10 10")
        .attr("orient", "auto")
        .append("path")
            .attr("d", "M0,-5L10,0L0,5");

}
