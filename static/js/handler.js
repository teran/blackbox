$(document).ready(function() {
    $(document).on('click', '.torrent-list-item', function(e) {
        alert($(this).html());
    });
    $(document).on('click', '.add-torrent-button', function(e) {
        $('#addTorrentModal').modal('show');
    });
    $('.add-torrent-submit').click(function() {
        $('#add-torrent-form').submit();
    });
});
