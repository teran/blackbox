$(document).ready(function() {
    $(document).on('click', '.torrent-list-item', function(e) {
        var id = $(this).attr('data-id');
        $('.torrent-info-modal-body').html(
            'LOL'
        );
        $('#torrentInfoModal').modal('show');
    });
    $(document).on('click', '.add-torrent-button', function(e) {
        $('#addTorrentModal').modal('show');
    });
    $('.add-torrent-submit').click(function() {
        $('#add-torrent-form').submit();
    });
});
