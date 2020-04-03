$(document).ready(function(){
	var l = $("#headerleft");
	var c = $("#headercentre");
	/* On window resize, vanish header title if undersize */
	$(window).on('resize', function() {
		if( l.offset().left + l.innerWidth() >= c.offset().left ){
			c.css("visibility","hidden");
		} else {
			c.css("visibility","visible");
		}
	});
});
