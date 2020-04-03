$(document).ready( function(){
	/* Get sort parameter from sort select value */
	$("#sortby").change( function() {
		window.location.href = "?orderBy=" + $(this).val();
	});
});