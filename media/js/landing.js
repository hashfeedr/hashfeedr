$(function() {
	return false;
	$('#queryform').submit(
		function() {
			var query = $('input#query').val();
			if(query.length>0) {
				window.location = '/feed/' + encodeURIComponent(query);
			}
			return false;
		});
});