$(document).ready( function(){
	$('#plstar').click(function() {
		/* On star clicked, indicate */
		if(state == 0){
			$(this).css("color","gold");
		} else {
			$(this).html("&#9734;");
		}
		
		/* Do async request */
		$.get( target,
			/* Get variables from django (global, inline) */
			{ 'id':pid, 'action':(1-state) },
			function(data){
				if(data==1){
					/* Now starred */
					state = 1;
					$('#plstar').addClass("starred");
					$('#plstar').html("&#9733;");
				} else {
					/* Now not starred */
					/* Note we err on the side of caution if data gives -1 (error) */
					state = 0;
					$('#plstar').removeClass("starred");
					$('#plstar').css("color","unset");
				}
			}
		);
	});
});