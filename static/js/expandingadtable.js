
function hideSmIfEmpty( table ){
	/* Hide the show more row if there is no more to show */
	if( $("tbody tr:not(tr.visible)",table).length === 0 ){
		$("tfoot tr",table).hide();
	}
}

function showChunk( table ) {
	/* Show a chunk of hidden rows, according to django showchunksize (dchunk, inline, global) */
	$("tbody tr:not(tr.visible)",table).slice(0,showchunksize).addClass("visible");
	hideSmIfEmpty( table );
}

$(document).ready( function(){

	$("table.expandingadtable").each( function() {
		/* Show a chunk of each */
		showChunk( $(this) );
	});

	$("a.tableexpand").click( function(e) {
		/* Register onclick, prevent default link following */
		e.preventDefault();
		showChunk( $(this).parents("table.expandingadtable") );
	});
});