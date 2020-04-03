$(document).ready(function(){
	var l = $("#headerleft");
	var c = $("#headercentre");

	$(window).on('resize', function() {
		if( l.offset().left + l.innerWidth() >= c.offset().left ){
			c.css("visibility","hidden");
		} else {
			c.css("visibility","visible");
		}
	});
});
