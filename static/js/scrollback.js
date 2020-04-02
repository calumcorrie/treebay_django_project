$(document).ready( function(){
	$("a.scrollback").click( function(e){
		window.scrollTo({top: 0, behavior: 'smooth'});
		e.preventDefault();
	});
});