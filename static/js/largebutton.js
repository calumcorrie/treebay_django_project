$(document).ready( function() {
	$("div.largebutton").click( function(){
		/* Expands function of a to whole button */
		window.location.href = $(this).children("a").attr("href");
	});
});