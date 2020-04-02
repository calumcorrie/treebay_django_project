$(document).ready( function(){
	$("#sortby").change( function() {
		window.location.href = "?orderBy=" + $(this).val();
	});
});