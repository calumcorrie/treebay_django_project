$(document).ready( function(){
	$('#plstar').click(function() {
		if(state == 0){
			$(this).css("color","gold");
		} else {
			$(this).html("&#9734;");
		}
		
		$.get( target,
			{ 'id':pid, 'action':(1-state) },
			function(data){
				if(data==1){
					state = 1;
					$('#plstar').addClass("starred");
					$('#plstar').html("&#9733;");
				} else {
					state = 0;
					$('#plstar').removeClass("starred");
					$('#plstar').css("color","unset");
				}
			}
		);
	});
});