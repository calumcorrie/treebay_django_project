// Toggle between hiding and showing the dropdown contents on each click
function toggle() {
	$("#myDropdown").toggleClass("show")
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
	$("div.dropdown-content").removeClass("show");
  }
};