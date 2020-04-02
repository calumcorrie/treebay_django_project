function hideSmIfEmpty( table ){
	if( $("tbody tr:not(tr.visible)",table).length === 0 ){
		$("tfoot tr",table).hide();
	}
}

function showChunk( table ) {
	$("tbody tr:not(tr.visible)",table).slice(0,showchunksize).addClass("visible");
	hideSmIfEmpty( table );
}

$(document).ready( function(){

	$("table.expandingadtable").each( function() {
		showChunk( $(this) );
	});

	$("a.tableexpand").click( function(e) {
		e.preventDefault();
		showChunk( $(this).parents("table.expandingadtable") );
	});
});