$(document).ready(function(){
	$.get("/topology", function(data) {
		$("#map").text = data;
		console.log(JSON.parse(data))
	});
	$("button").click(function() {

	});
});
