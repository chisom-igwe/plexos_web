// function to display 
$('.connect').click(function (e) {
	$('#loader').show(); //<----here
})

// function to change url when tab is clicked 
$(function () {
	var hash = window.location.hash;
	hash && $('ul.nav a[href="' + hash + '"]').tab('show');

	$('.nav-tabs a').click(function (e) {
		$(this).tab('show');
		var scrollmem = $('body').scrollTop() || $('html').scrollTop();
		window.location.hash = this.hash;
		$('html,body').scrollTop(scrollmem);
	});
});

// function to make connect button diabaled until input fields are filled 
(function () {
	$('form > div > div > input').keyup(function () {

		var empty = false;
		$('form > div > div >input[required]').each(function () {
			if ($(this).val() === '') {
				empty = true;
			}
		});

		if (empty) {
			$('#connectServerConnectButton').attr('disabled', 'disabled');
		} else {

			$('#connectServerConnectButton').prop("disabled", false);
		}
	});
})();

