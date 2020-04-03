
function onkey( context, ev="eval" ) {
	/* Key event handler. ev to differentiate setup from key event */
	var tablerow = context.parents("#addedittable tr");
	
	/* Get the validity div */
	var valid = $("td",tablerow).children("div.valid");
	var validfeedb = valid.children();
	
	var field = valid.attr("id");
	
	if(field === "Price" ){
		if( ev == "eval" ){
			if( !( /^\d{1,4}\.?\d{0,2}$/g.test( context.val() ) ) ){
				validfeedb.eq(0).css("visibility","visible");
				validfeedb.eq(0).text("Invalid price");
			} else {
				validfeedb.eq(0).css("visibility","hidden");
			}
		}
	} else if( valid.children().length >= 2 && tablerow.hasClass("monitor")){
		var len = context.val().length;
		/* Get limits from django (inline) */
		var lim = limits[field];
		validfeedb.eq(1).text( len + "/" + lim );
		if( len > lim ){
			validfeedb.eq(1).css("color","red");
			validfeedb.eq(0).css("visibility","visible");
			validfeedb.eq(0).text("Exceeded character limit");
		} else {
			validfeedb.eq(1).css("color","unset");
			validfeedb.eq(0).css("visibility","hidden");
		}
	}
}

function refreshCallbacks() {
	/* Re-register onclick remove callbacks, in case of new tags */
	$("div.tagholder > span").click( function() {
		$(this).remove();
		var torem = $(this).text().slice(1);
		/* Remove it from the hidden input field */
		$("#tgsel > select > option:contains("+torem+")").prop("selected",false);
	});
}

function addSelected(){
	/* Add button trigger */
	add( $("#tagselect option:selected").text() );
}

function add( toadd ){
	/* We must be valid - non empty */
	$("#tagged").css("border-color","unset");
	
	/* Don't add tag if present */
	if( ! $("#tagged > span:contains(" + toadd + ")").length ){
		$("#tagged").append("<span>#"+toadd+"</span> ");
	}
	
	/* Update the underlying hidden input */
	$("#tgsel > select > option:contains("+toadd+")").prop("selected",true).attr("selected","selected");
	
	refreshCallbacks();
}

function resetToBase(){	
	/* Set the tag container equal to the underlying select */
	$("#tagged > span").remove();
	$("#tgsel > select > option:selected").each( function() {
		add( $(this).text() );
	});
}
	

$(document).ready( function() {
	/* Monitored inputs */
	var inputs = $("#addedittable tr.monitor input, #addeditmain tr.monitor textarea");

	inputs.each( function() {
		/* Setup */
		onkey($(this),"setup");
	});

	inputs.keyup( function(){
		/* OnKey */
		onkey($(this));
	});

	/* Resets tagcontainer to underlying select */
	resetToBase();
	
	/* Failsafe in case of meddling */
	$("#tgsel > select").change( resetToBase );
	
	/* Set up add select */
	$("#tgsel").parent().children("select").html( $("#tgsel > select").html() );

	$("#tagadd").click( function( e ){
		/* Add button callback */
		e.preventDefault();
		addSelected();
	});

	refreshCallbacks();
	
	$("#subbttn").click( function(e){
		if($("textarea").val().length >  limits["Description"]){
			/* Prevent submit if Description oversize, feedback will already be present */
			e.preventDefault();
		} else if($("#tgsel > select > option:selected").length == 0){
			/* Replace hidden validation */
			/*Doesnt override default action*/
			$("#tagged").css("border-color","red");
		}
	});
	
	/* Nasty little fix to get rid of Currently part of django modelfield form object */
	var s = $("#picture-clear_id").parent();
	s.html( s.html().match( /<input[\s\S]*/g ) );
});