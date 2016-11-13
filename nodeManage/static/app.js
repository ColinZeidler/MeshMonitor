$(document).ready(function(){
	$.get("/topology", function(data) {
		$("#map").html(data);
		console.log(JSON.parse(data))
	});
	$("button").click(function() {

	});
});
