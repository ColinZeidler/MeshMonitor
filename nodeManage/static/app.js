var svg = d3.select("svg");
var width = +svg.attr("width");
var height = +svg.attr("height");

var sim = d3.forceSimulation()
	.force("link", d3.forceLink().id(function(d) { return d.id; }))
	.force("charge", d3.forceManyBody())
	.force("center", d3.forceCenter(width/2, height/2));

d3.json("/nodes", function(error, n) {
	d3.json("/topology", function(error, t) {
	console.log(n)
	console.log(t)
	var link = svg.append("g")
		.attr("class", "links")
		.selectAll("line")
		.data(t)
		.enter().append("line")
			.attr("class", "link");

	var node = svg.append("g")
		.attr("class", "nodes")
		.selectAll("circle")
		.data(n)
		.enter().append("circle")
			.attr("r", 5)
			.attr("class", "node").on("click", node_click).text(function(d) { return d.name; });
		node.append("name").text(function(d) { return d.name; });

		sim.nodes(n).on("tick", tick);
		sim.force("link").links(t);
		
	function tick() {
		console.log("tick");
		node.attr("cx", function(d) { return d.x; })
			.attr("cy", function(d) { return d.y; });

		link.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
	}
	});
});


function node_click(d) {
	alert(d.name);
}
