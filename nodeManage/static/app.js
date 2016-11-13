$(document).ready(function(){
	var width = 960;
	var height = 500;

	var links = [];
	var nodes = [];
	
	var force = d3.layout.force()
		.nodes(nodes)
		.links(links)
		.charge(-400)
		.linkDistance(120)
		.size([width, height])
		.on("tick", tick);

	var svg = d3.select("#map").append("svg")
		.attr("width", width)
		.attr("height", height);

	var node = svg.selectAll(".node");
	var link = svg.selectAll(".link");

	function tick() {
		node.attr("cx", function(d) { return d.x; })
			.attr("cy", function(d) { return d.y; })

		link.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; })
	}

	function start() {
		link = link.data(force.links(), function(d) { return d.source.id + "-" + d.target.id; });
		link.enter().insert("line", ".node").attr("class", "link");
		link.exit().remove();

		node = node.data(force.nodes(), function(d) { return d.id; });
		node.enter().append("circle").attr("class", "node").attr("r", 30);
		node.exit().remove();

		force.start();
	}
		
	$.get("/nodes", function(data) {
		nodes.push(JSON.parse(data))
		console.log(nodes);
		start();
	});
	$.get("/topology", function(data) {
		links.push(JSON.parse(data));
		console.log(links);
		start();
	});
	$("button").click(function() {

	});
});
