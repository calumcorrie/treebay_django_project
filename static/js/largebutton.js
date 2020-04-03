$("div.largebutton").click( function(e){
	/* Expands function of a to whole button */
	window.location.href = $(this).children("a").attr("href");
});