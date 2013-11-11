$(document).ready(function() {
    $(document).on('click', '.torrent-list-item', function(e) {
        var id = $(this).attr('data-id');
        $.getJSON('/api/transmission/'+id+'/info', function(data){
            items = [
                '<p>Name: '+data.name+'</p>',
                '<p>Status: '+data.status+'</p>',
                '<p>Actions: ' +
                    '<a href="#" class="torrent-delete-button" data-id="'+data.id+'"><span class="glyphicon glyphicon-trash"></span></a> ' +
                    '<a href="#" class="torrent-resume-button" data-id="'+data.id+'"><span class="glyphicon glyphicon-play"></span></a> ' +
                    '<a href="#" class="torrent-stop-button" data-id="'+data.id+'"><span class="glyphicon glyphicon-stop"></span></a> '
            ];
            var files = ['<ul class="torrent-info-list">']
            $.each(data.files, function(key, val) {
                fn = val.split('/');
                if(data.progress == 100) {
                    files.push('<li class="torrent-info-item"><a href="'+val+'">'+fn[fn.length-1]+'<a></li>');
                } else {
                    files.push('<li class="torrent-info-item">'+fn[fn.length-1]+'</li>');
                }
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
    $('.torrent-delete-button').click(function(e) {
        e.preventDefault();
    });
    $('.torrent-resume-button').click(function(e) {
        e.preventDefault();
    });
    $('.torrent-stop-button').click(function(e) {
        e.preventDefault();
    });
});
