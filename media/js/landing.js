$(function() {
	$('#queryform').submit(
		function() {
			var query = $('input#query').val();
			if(query.length>0) {
				window.location = '/feed/' + encodeURIComponent(query);
			}
			return false;
		});
	
	$('input#query').focus(
		function() {
			if($(this).val() == '#djangodash') {
				$(this).val('');
			}
		});
	$('input#query').blur(
		function() {
			if($(this).val() == '') {
				$(this).val('#djangodash');
			}
		});
		
});