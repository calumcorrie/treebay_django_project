$(document).ready( function(){
	$("div.slidecontainer span.pan").click( function(){
		var container = $(this).parent("div.slidecontainer");
		var kids = container.children("div");
		var firstchild = kids.first();
		var fullmv = firstchild.outerWidth();
		
		var vp_left = 0;
		var vp_right = vp_left + container.outerWidth();
		
		var first_L_pos = firstchild.position().left;
		var	last_R_pos = (fullmv * kids.length) + first_L_pos;
		
		var scrollleft = $(this).attr("class") == "pan panLeft";
		var mv = 0;
		
		if(scrollleft){
			if( vp_left <= first_L_pos ){
				//We are at left end, do nothing
				mv = 0;
			} else if( vp_left <= (first_L_pos + fullmv) ){
				//We are within one width of the left end
				mv = vp_left - first_L_pos;
			} else {
				mv = fullmv;
			}
		} else {
			if( last_R_pos <= vp_right ){
				//We at right end, do nothing
				mv = 0;
			} else if( (last_R_pos - fullmv) <= vp_right ){
				//We are within a width... add 5 margin
				mv = last_R_pos - vp_right + 5;
			} else {
				mv = fullmv;
			}
			mv *= -1;
		}
		
		var new_p = first_L_pos + mv;
		
		kids.animate({left:new_p+"px"},"slow");
	});
});