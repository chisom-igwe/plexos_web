$('#connectServerConnectButton').click(function (e) {
    $('#loader').show(); //<----here
    $.ajax({
            success: function(result) {
                $('#loader').hide();  //<--- hide again
            }
    })
})

$('#datasetDivLink'.click(function() {
	$("#datasetInfo").slideToggle();
});