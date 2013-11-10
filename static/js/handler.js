$(document).ready(function() {
    $(document).on('click', '.torrent-list-item', function(e) {
        alert($(this).html());
    });
});
