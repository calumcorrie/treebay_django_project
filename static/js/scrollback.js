$(document).ready( function(){
	$("a.scrollback").click( function(e){
		/* Scroll to the top, prevent <a> following */
		window.scrollTo({top: 0, behavior: 'smooth'});
		e.preventDefault();
	});
});