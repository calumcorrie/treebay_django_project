function onkey( context, ev="eval" ) {
	var tablerow = context.parents("#addedittable tr");
	var valid = $("td",tablerow).children("div.valid");
	var validfeedb = valid.children();
	var field = valid.attr("id");
	if(field === "Price" ){
		if( ev == "eval" ){
			//alert( context.val() + /^\d{1,4}\.?\d{0,2}$/g.test( context.val() ) );
			if( !( /^\d{1,4}\.?\d{0,2}$/g.test( context.val() ) ) ){
				validfeedb.eq(0).css("visibility","visible");
				validfeedb.eq(0).text("Invalid price");
			} else {
				validfeedb.eq(0).css("visibility","hidden");
			}
		}
	} else if( valid.children().length >= 2 && tablerow.hasClass("monitor")){
		var len = context.val().length;
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
	$("div.tagholder > span").click( function() {
		$(this).remove();
		var torem = $(this).text().slice(1);
		$("#tgsel > select > option:contains("+torem+")").prop("selected",false);
	});
}

function addSelected(){
	add( $("#tagselect option:selected").text() );
}

function add( toadd ){
	$("#tagged").css("border-color","unset");
	if( ! $("#tagged > span:contains(" + toadd + ")").length ){
		$("#tagged").append("<span>#"+toadd+"</span> ");
	}
	$("#tgsel > select > option:contains("+toadd+")").prop("selected",true).attr("selected","selected");
	refreshCallbacks();
}

function resetToBase(){	
	$("#tagged > span").remove();
	$("#tgsel > select > option:selected").each( function() {
		add( $(this).text() );
	});
}
	

$(document).ready( function() {
	var inputs = $("#addedittable tr.monitor input, #addeditmain tr.monitor textarea");

	inputs.each( function() {
		onkey($(this),"setup");
	});

	inputs.keyup( function(){
		onkey($(this));
	});

	/* Resets tagcontainer to underlying select */
	resetToBase();
	
	/* Failsafe in case of meddling */
	$("#tgsel > select").change( resetToBase );
	
	/* Set up add select */
	$("#tgsel").parent().children("select").html( $("#tgsel > select").html() );

	$("#tagadd").click( function( e ){
		e.preventDefault();
		addSelected();
	});

	refreshCallbacks();
	
	$("#subbttn").click( function(e){
		if($("textarea").val().length >  limits["Description"]){
			e.preventDefault();
		} else if($("#tgsel > select > option:selected").length == 0){
			/*Doesnt override default action*/
			$("#tagged").css("border-color","red");
		}
	});
	
	/* Nasty little fix to get rid of Currently part of django modelfield form object */
	var s = $("#picture-clear_id").parent();
	s.html( s.html().match( /<input[\s\S]*/g ) );
});