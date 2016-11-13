$(document).ready(function(){
	var svg = d3.select("svg");
	var width = +svg.attr("width");
	var height = +svg.attr("height");

	var links = [];
	var nodes = [];
		
	$.get("/nodes", function(data) {
		var t = JSON.parse(data);
		for (var i = 0; i< t.length; i++) {
			nodes.push(t[i]);
		}
		console.log(nodes);
	});
	$.get("/topology", function(data) {
		var t = JSON.parse(data);
		for (var i = 0; i < t.length; i ++) {
			links.push(t[i]);
		}
		console.log(links);
	});
	$("button").click(function() {

	});
	
	var sim = d3.forceSimulation()
		.force("link", d3.forceLink().id(function(d) { return d.id; }))
		.force("charge", d3.forceManyBody())
		.force("center", d3.forceCenter(width/2, height/2));


	var node = svg.append("g")
		.attr("class", "nodes")
		.selectAll("circle")
		.data(nodes)
		.enter().append("circle")
			.attr("r", 30)
			.attr("class", "node");

	var link = svg.append("g")
		.attr("class", "links")
		.selectAll("line")
		.data(links)
		.enter().append("line")
			.attr("class", "link");

	sim.nodes(nodes).on("tick", tick);
	sim.force("link").links(links);

	function tick() {
		node.attr("cx", function(d) { return d.x; })
			.attr("cy", function(d) { return d.y; })

		link.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; })
	}

});
