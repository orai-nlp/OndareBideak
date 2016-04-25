//data: Aldagai honetan daude nodo guztiak.
var data = ibilbide_data;

// Sortu mapa
var dataMap = data.reduce(function(map, node) {
    //node.id: id-ak erabiliko ditu loturak sortzeko.
    map[node.id] = node;
    return map;
}, {});

// Sortu zuhaitzaren array-a
var treeData = [];
data.forEach(function(node) {
    // Gehitu aitari
    var parent = dataMap[node.parent];
    if (parent) {
        //Sortu semeen array bat existitzen ez bada.
        (parent.children || (parent.children = []))
            // Gehitu nodoa seme array-era
            .push(node);
    } else {
        // Aita null edo ez dauka
        treeData.push(node);
    }
});

// ************** Sortu zuhaitz diagrama  *****************
var margin = {top: 20, right: 120, bottom: 20, left: 120},//marginak
    width = 800 - margin.right - margin.left,//svg-aren zabalera
    height = 600 - margin.top - margin.bottom;//svg-aren altuera    
var selectedNode = null; //Aukeratutako nodoa
var draggingNode = null; //Mugitzen ari garen nodoa
var panSpeed = 200; //abiadura
var panBoundary = 20;//Muga.
var duration = 750;//Transizioaren iraupena
var viewerWidth =  0; //nodoak zetratzeko zabalera
var viewerHeight = width; //nodoak zetratzeko altuera
var luzera = 40; //luzera = radio +10. Link-aren luzaera.
var i=0;

//Zuhaitza sortu
var tree = d3.layout.tree()
    .size([width,height]);
//Diagonala sortu
var diagonal = d3.svg.diagonal()
    .projection(function(d) { 
        return [d.y-luzera, d.x]; });

//svg-a sortu, path_boxes div-aren barruan.
var svg = d3.select("#path_boxes").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

//click funtzioa: klik egitean aukeratutako nodoaren zirkulua gorriz ezartzen du.
function click(d) {
    var p = d3.select(this);
    if (p.select("circle").classed("aukeratuta") == true){
        d3.selectAll("circle").style({stroke: 'steelblue'});
        p.select("circle").style({stroke: 'red'});
        p.select("circle").classed("aukeratuta",false);

    } else {
        p.select("circle").style({stroke: 'steelblue'});
        p.select("circle").classed("aukeratuta",true);
    }
}
//dblclick funtzioa: klik bikoitza egitean narrazioa gehitzeko textarea eta botoia gaitu egiten dira.
function dblclick(d){
    document.getElementById("narra_textarea").innerHTML = d.narrazioa;
    document.getElementById("narra_textarea").value = d.narrazioa;
    document.getElementById("narra_textarea").disabled = false;
    document.getElementById("narra_botoia").disabled = false;
    document.getElementById("narra_botoia").onclick = function () {
            d.narrazioa = document.getElementById("narra_textarea").value;
            document.getElementById("narra_textarea").disabled = true;    
            document.getElementById("narra_botoia").disabled = true;  
            document.getElementById("narra_textarea").value = " ";              
        };

}
//pan funtzioa:noaren posizioaren aldaketa
function pan(unekoNodoa, direction) {
    var speed = panSpeed;
    if (panTimer) {
        clearTimeout(panTimer);
        translateCoords = d3.transform(svgGroup.attr("transform"));
    if (direction == 'left' || direction == 'right') {
        translateX = direction == 'left' ? translateCoords.translate[0] + speed : translateCoords.translate[0] - speed;
        translateY = translateCoords.translate[1];
    } else if (direction == 'up' || direction == 'down') {
        translateX = translateCoords.translate[0];
        translateY = direction == 'up' ? translateCoords.translate[1] + speed : translateCoords.translate[1] - speed;
    }
        scaleX = translateCoords.scale[0];
        scaleY = translateCoords.scale[1];
        scale = zoomListener.scale();
        svgGroup.transition().attr("transform", "translate(" + translateX + "," + translateY + ")scale(" + scale + ")");
        d3.select(unekoNodoa).select('g.node').attr("transform", "translate(" + translateX + "," + translateY + ")");
        zoomListener.scale(zoomListener.scale());
        zoomListener.translate([translateX, translateY]);
        panTimer = setTimeout(function() {
        pan(unekoNodoa, speed, direction);
        }, 50);
    }
}
//zoom funtzioa:eskala haunditu edo txikitu egiten du.
function zoom() {
    svgGroup.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
}

// define the zoomListener which calls the zoom function on the "zoom" event constrained within the scaleExtents
var zoomListener = d3.behavior.zoom().scaleExtent([0.1, 3]).on("zoom", zoom);

//initiateDrag funtzioa: 
function initiateDrag(d, unekoNodoa) {
    draggingNode = d;
    d3.select(unekoNodoa).attr('pointer-events', 'none');
    d3.selectAll('.node').attr('class', 'node desactiveDrag');
    d3.select(unekoNodoa).attr('class', 'node activeDrag');
    svgGroup.selectAll("g.node").sort(function(a, b) { // select the parent and sort the path's
    if (a.id != draggingNode.id) return 1; // a is not the hovered element, send "a" to the back
        else return -1; // a is the hovered element, bring "a" to the front
    });
    // if nodes has children, remove the links and nodes
    if (nodorenzuhaitza.length > 1) {
        // remove link paths
        links = tree.links(nodorenzuhaitza);
        nodePaths = svgGroup.selectAll("path.link")
        .data(links, function(d) {
        return d.target.id;
        }).remove();
        // remove child nodes
        nodesExit = svgGroup.selectAll("g.node")
        .data(nodorenzuhaitza, function(d) {
        return d.id;
        }).filter(function(d, i) {
            if (d.id == draggingNode.id) {
                return false;
            }
                return true;
        }).remove();
    }
    // remove parent link
    parentLink = tree.links(tree.nodes(draggingNode.parent));
    svgGroup.selectAll('path.link').filter(function(d, i) {
    if (d.target.id == draggingNode.id) {
        return true;
    }
        return false;
    }).remove();
    dragStarted = null;
}

var updateTempConnector = function() {
    var data = [];
    if (draggingNode !== null && selectedNode !== null) {
    // have to flip the source coordinates since we did this for the existing connectors on the original tree
        data = [{
            source: {
                x: selectedNode.y0,
                y: selectedNode.x0
            },
            target: {
                x: draggingNode.y0,
                y: draggingNode.x0
            }
        }];
    }
    var link = svgGroup.selectAll(".templink").data(data);
    link.enter().append("path")
        .attr("class", "templink")
        .attr("d", d3.svg.diagonal())
        .attr('pointer-events', 'none');
    link.attr("d", d3.svg.diagonal());
    link.exit().remove();
};

function centerNode(source) {
    scale = zoomListener.scale();
    x = -source.y0;
    y = -source.x0;
    x = x * scale + viewerWidth / 2;
    y = y * scale + viewerHeight / 2;
    d3.select('g').transition()
        .duration(duration)
        .attr("transform", "translate(" + 0 + "," + 0 + ")scale(" + scale + ")");
    zoomListener.scale(scale);
    zoomListener.translate([x, y]);
}


function endDrag() {
    selectedNode = null;
    d3.selectAll('.node').attr('class', 'node desactiveDrag');
    d3.select(unekoNodoa).attr('class', 'node');
    // now restore the mouseover event or we won't be able to drag a 2nd time
    d3.select(unekoNodoa).attr('pointer-events', '');
    updateTempConnector();
    if (draggingNode !== null) {
        update(root);
        centerNode(draggingNode);
        draggingNode = null;
    }
}
    
var drag = d3.behavior.drag()
    .on("dragstart", function(d){
    //Nodoa root bada ezin da mugitu bestela nodoa mugitzen hasiko da.
        if (d == root) {
            var p = d3.select(this);
            p.select("circle").style({stroke: 'black'});
            return;
        }
        dragHasi = true;
        //nodorenzuhaitza:Aldagai honetan svg-an dauden nodo bakoitzaren zuhaitza agertzen da. Zein den bere aita eta semeak baditu zeintzuk dira bere semeak.
        nodorenzuhaitza = tree.nodes(d);
        d3.event.sourceEvent.stopPropagation();
    }).on("drag", function(d){
        if (d == root) {
            return;
        }
        if (dragHasi) {
            //unekonodoa= aukeratuta daugan nodoa da
            unekoNodoa = this;
            initiateDrag(d, unekoNodoa);
        }
        relCoords = d3.mouse($('svg').get(0));
        if (relCoords[0] < panBoundary) {
            panTimer = true;
            pan(this, 'left');
        } else if (relCoords[0] > ($('svg').width() - panBoundary)) {
            panTimer = true;
            pan(this, 'right');
        } else if (relCoords[1] < panBoundary) {
            panTimer = true;
            pan(this, 'up');
        } else if (relCoords[1] > ($('svg').height() - panBoundary)) {
            panTimer = true;
            pan(this, 'down');
        } else {
            try {
                clearTimeout(panTimer);
            } catch (e) {
            }
        }
        d.x0 += d3.event.dy;
        d.y0 += d3.event.dx;
        var node = d3.select(this);
        node.attr("transform", "translate(" + d.y0 + "," + d.x0 + ")");
        updateTempConnector();
    }).on("dragend", function(d) {
        if (d == root) {
            return;
        } 
        //draggingNode: Mugitzen ari garen nodoa.
        //selectedNode: Aukeratu dugun nodoa.
        //Mugitzen dugun nodoa, nodo bat ez dagoen lekuan ezartzen badugu, nodo hori zegoen lekura joango da.
        else if (draggingNode == selectedNode){
            endDrag();
        } else if (selectedNode.parent == draggingNode){
            var index = draggingNode.parent.children.indexOf(draggingNode);
            if (index > -1) {
                draggingNode.parent.children.splice(index, 1);
            }
            var dragAita = draggingNode.parent;
            selectedNode.parent = dragAita;
            draggingNode.parent = selectedNode;
            for (var i=0;i<draggingNode.children.length;i++){
                if (selectedNode.name == draggingNode.children[i].name){
                    draggingNode.children.splice(i, 1);
                }
            }
            if (selectedNode.children){
                selectedNode.children.push(draggingNode);
                selectedNode.parent.children.push(selectedNode);
                endDrag(); 
            } else {
                selectedNode.children = [];
                selectedNode.children.push(draggingNode);
                selectedNode.parent.children.push(selectedNode);
                endDrag();
            } 
        } else if (selectedNode.parent.parent == draggingNode || selectedNode.parent.parent.parent == draggingNode){
            var index = draggingNode.parent.children.indexOf(draggingNode);
            if (index > -1) {
                draggingNode.parent.children.splice(index, 1);
            }
            var index2 = selectedNode.parent.children.indexOf(selectedNode);
            if (index2 > -1) {
                selectedNode.parent.children.splice(index2, 1);
            }
            var dragAita = draggingNode.parent;
            selectedNode.parent = dragAita;
            draggingNode.parent = selectedNode;
            if (selectedNode.children){
                selectedNode.children.push(draggingNode);
                selectedNode.parent.children.push(selectedNode);
                endDrag(); 
            } else {
                selectedNode.children = [];
                selectedNode.children.push(draggingNode);
                selectedNode.parent.children.push(selectedNode);
            for (var c= 0;c<draggingNode.children;c++){
                var index3 = draggingNode.children[i].children.indexOf(selectedNode)
                if (index > -1) {
                    draggingNode.children[i].children.splice(index, 1);
                }
            }
            endDrag();
            }
        }  else {
            unekoNodoa = this;
            if (selectedNode) {
                var index = draggingNode.parent.children.indexOf(draggingNode);
                if (index > -1) {
                    draggingNode.parent.children.splice(index, 1);
                }
                if (typeof selectedNode.children !== 'undefined' || typeof selectedNode._children !== 'undefined') {
                    if (typeof selectedNode.children !== 'undefined') {
                        selectedNode.children.push(draggingNode);
                    } else {
                        selectedNode._children.push(draggingNode);
                    }
                } else {
                    selectedNode.children = [];
                    selectedNode.children.push(draggingNode);
                }
                // Make sure that the node being added to is expanded so user can see added node is correctly moved
                expand(selectedNode);
                endDrag();
            }
        }
    });

function expand(d) {
    if (d._children) {
        d.children = d._children;
        d.children.forEach(expand);
        d._children = null;
    }
} 

function collapse(d) {
    if (d.children) {
        d._children = d.children;
        d._children.forEach(collapse);
        d.children = null;
    }
}

var overCircle = function(d) {
    selectedNode = d;
    updateTempConnector();
};  
            

var svgGroup = svg.append("g");
root = treeData[0];
root.x0 = 0;
root.y0 = height/2;
update(root);
centerNode(root);

function update(source) {

    // kalkulatu zuhaitz layout berria: Nodoak eta link-ak.
    var nodes = tree.nodes(root).reverse(),
        links = tree.links(nodes);
        //ezabatu root nodoa
        nodes.pop();
        nodes.reverse();



        // Nodoen arteko distantzia
        nodes.forEach(function(d) { 
            d.y = d.depth * 100;});

    // Nodoak deklaratu
    var node = svg.selectAll("g.node")
        .data(nodes, function(d) { return d.id || (d.id = ++i); });

    // Nodoak sartu.
    var nodeEnter = node.enter().append("g")
        .call(drag)
        .attr("class", "node")
        .attr("transform", function(d) { 
            return "translate(" + d.y + "," + d.x + ")"; })
        .on('click', click)
        .on('dblclick', function(node) {
            dblclick(node);
        })
        .on("mouseover", function(node) {
            overCircle(node);
        });

        //Zakarrontzi irudia gehitu. Zakarrontzi honetan klik egiten baduzu nodoa ezabatu dezakezu.
        nodeEnter.append("image")
            .attr("id",function(d) { return d.id })
            .attr("xlink:href","http://findicons.com/files/icons/1580/devine_icons_part_2/128/trash_recyclebin_empty_closed.png")
            .attr("x", function(d) { return -40;})
            .attr("y", function(d) { return -20;})
            .attr("height", 15)
            .attr("width", 15)
            .on('click', function(d) { 
                if (d.parent.name == "ROOT"){
                    alert("Nodoa hau ezin da ezabatu");
                    return;
                } else {
                    var result = confirm(" Nodoa ezabatu nahi duzu? ");
                    if (result) {
                        var index = d.parent.children.indexOf(d);
                        if (index>-1){
                            d.parent.children.splice(index, 1);
                        }
                        if (d.children !=undefined){
                            var index2 = d.children.length;
                            for (var i=0;i<index2;i++){
                                d.children[i].parent = d.parent;
                                d.parent.children.push(d.children[i]);
                            }  
                        }
                        update(root);
                    } else {
                        alert("Nodoa ez da ezabatu.");
                    }            
                }
            });   

        //nodoari zirkulua gehitu
        nodeEnter.append("circle")
            .attr("id",function(d) {
                return 'nodo: '+d.name; })
            .attr("class", "aukeratuta")
            .attr("r", function(d){
                if (nodes.length>=10){
                    return 20;
                } else {
                    return 30;
                }
            })
            .style("fill", function(d) { 
                var ir = "#"+d.id;
                return  "url("+ir+")";});

        //nodoari background irudia ezarri.

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

                          
          
        //Nodoari testua gehitu. 
        nodeEnter.append("text")
            .attr("x", function(d) { 
                return d.children || d._children ? 30 : -30; })
            .attr("dy", function(d) {
                if (nodes.length>=10){
                    return d.children || d._children ?  35 : 35;
                } else {
                    return d.children || d._children ?  45 : 45;
                }
            })
            .attr("text-anchor", function(d) { 
                return d.children || d._children ? "end" : "start"; })
            .text(function(d) { return d.name; })
            .style("fill-opacity", 1);

        nodeEnter.append("text2")
            .text(function(d) { return d.narrazioa; })
            .style("hidden", true);


    //Nodoaren transizioaren posizioa.
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function(d) {
            if (nodes.length>=10){
                var a = d.y-10;
                return "translate(" + a + "," + d.x + ")";
            } else {
                return "translate(" + d.y + "," + d.x + ")";
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


    // link-ak deklaratu
    var link = svgGroup.selectAll("path.link")
        .data(links, function(d) { return d.target.id; });
        link.enter().insert("path", "g")
            .attr("class", "link")
            .style("opacity", function(link){ 
            //ROOT BADA IZKUTATUKO DU ETA BESTELA ERAKUTSIKO DU.
            if (link.source.name == "ROOT"){
                return 0;
            } else {
                return 1;
            } })
            .attr('stroke-width', 2)
            .attr("marker-end", "url(#arrowhead)")
            .attr("d", function(d) {
                var o = {
                    x: source.x0,
                    y: source.y0
                };
                //o= Object {x: NaN, y: NaN};
                return diagonal({
                    source: o,
                    target: o
                })
            }); 

        // Transizio linkak bere posizio berrira.
        link.transition()
            .duration(750)
            .attr("d", diagonal);

        //Transizioa existitzen diren nodoen bere aita berrien posiziora.
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

        //Nodo bakoitzaren d.x posizioa d.x0 izango da.
        //Nodo bakoitzaren d.y posizioa d.y0 izango da.   
        nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
        });

    //Gezia ezarri link-ari, hau da marker bat gehitu.
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