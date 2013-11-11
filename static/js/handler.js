$(document).ready(function() {
    $(document).on('click', '.torrent-list-item', function(e) {
        var id = $(this).attr('data-id');
        $.getJSON('/api/transmission/'+id+'/info', function(data){
            items = [
                '<p>Name: '+data.name+'</p>',
                '<p>Status: '+data.status+'</p>',
                '<p>Actions: ' +
                    '<span class="glyphicon glyphicon-trash"></span> ' +
                    '<span class="glyphicon glyphicon-play"></span> ' +
                    '<span class="glyphicon glyphicon-stop"></span> '
            ];
            var files = ['<ul class="torrent-info-list">']
            $.each(data.files, function(key, val) {
                fn = val.split('/');
                files.push('<li class="torrent-info-item"><a href="'+val+'">'+fn[fn.length-1]+'<a></li>');
            });
            files.push('</ul>');
            $('.torrent-info-modal-body').html(items.join('')+files.join(''));
            $('#torrentInfoModal').modal('show');
        });
    });
    $(document).on('click', '.add-torrent-button', function(e) {
        $('#addTorrentModal').modal('show');
    });
    $('.add-torrent-submit').click(function() {
        $('#add-torrent-form').submit();
    });
});
