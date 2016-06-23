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
var divWidth = d3.select('#path_boxes_overview').style('width').substr(0,d3.select('#path_boxes_overview').style('width').length-2);
var divWidth = divWidth-(divWidth*0.04);
var divHeight = d3.select('#path_boxes_overview').style('height').substr(0,d3.select('#path_boxes_overview').style('height').length-2);
var divHeight = divHeight-(divHeight*0.1);

//Maddalen: top:20 zegoen lehen, baina modalean ondo ikusteko aldatu dut
var margin = {top: 200, right: 120, bottom: 20, left: 120},
    width = divWidth - margin.right - margin.left,
    height = divHeight - margin.top - margin.bottom;
    
    var i = 0;
    var duration = 750;
    var viewerWidth =  0;
    var viewerHeight = width;
    var newHeight = 4;
    //luzera = radio +10
    var luzera = 45;
var tree = d3.layout.tree()
    .size([width,height]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { 
        return [d.y-luzera, d.x]; });

var svg = d3.select("#path_boxes_overview").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
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

  //Borobila sortu
  var radio = 30;

  nodeEnter.append("circle")
    .attr("id",function(d) {
     return 'nodo: '+d.name; })
    .attr("class", "aukeratuta")
    .attr("r", function(d){
            return 15;
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
                .attr("xlink:xlink:href", function(d) { return (d.irudia);}) // "icon" is my image url. It comes from json too. The double xlink:xlink is a necessary hack (first "xlink:" is lost...).
                .attr("x", 0)
                .attr("y", 0)
                .attr("height", 1)
                .attr("width", 1)
                .attr("preserveAspectRatio", "xMinYMin slice");                  
  
  //Testua gehitu  
  nodeEnter.append("text")
      .attr("x", function(d) { 
          return d.children || d._children ? 35 : -35; })
      .attr("dy", function(d) {
            return d.children || d._children ?  30 : 30;
    })
      .attr("text-anchor", function(d) { 
          return d.children || d._children ? "end" : "start"; })
      .text(function(d) { return d.name; })
      .style("fill-opacity", 1);

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