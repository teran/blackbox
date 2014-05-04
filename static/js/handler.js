$(document).ready(function() {
    $(document).on('click', '.torrent-list-item', function(e) {
        var hash = $(this).attr('data-id');
        $.getJSON('/api/transmission/'+hash+'/info', function(data){
            items = [
                '<p>Name: <input type="text" class="torrent-info-name-field" data-id="'+data.hash+'" value="'+data.name+'" /></p>',
                '<p>Status: '+data.status+'</p>',
                '<p>Magnet: '+'<input type="text" class="max-width" value="'+data.magnetLink+'" /></p>',
                '<p>Actions: ' +
                    '<a href="#" class="torrent-delete-button" data-id="'+data.hash+'"><span class="glyphicon glyphicon-trash"></span></a> ' +
                    '<a href="#" class="torrent-resume-button" data-id="'+data.hash+'"><span class="glyphicon glyphicon-play"></span></a> ' +
                    '<a href="#" class="torrent-stop-button" data-id="'+data.hash+'"><span class="glyphicon glyphicon-stop"></span></a> ' +
                    '<a href="#" class="torrent-verify-button" data-id="'+data.hash+'"><span class="glyphicon glyphicon-check"></span></a> '
            ];
            var files = ['<ul class="torrent-info-list">']
            $.each(data.files, function(key, val) {
                if(data.progress == 100) {
                    html = '<li class="torrent-info-item">';
                    if(val.viewed == 1) {
                        html += '<span class="glyphicon glyphicon-ok-circle"> </span> ';
                    }
                    html += '<a href="'+val.link+'">'+val.filename+'<a></li>';
                    files.push(html);
                } else {
                    files.push('<li class="torrent-info-item">'+val.filename+'</li>');
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
    $(document).on('click', '.torrent-delete-button', function(e) {
        e.preventDefault();
        $.post('/api/transmission/'+$(this).attr('data-id')+'/delete', {})
            .done(function(){
                $('#torrentInfoModal').modal('toggle');
            })
            .fail(function(){
                alert('Error executing AJAX request!');
            });
    });
    $(document).on('click', '.torrent-resume-button', function(e) {
        e.preventDefault();
        $.post('/api/transmission/'+$(this).attr('data-id')+'/start', {})
            .done(function(){
                $('#torrentInfoModal').modal('toggle');
            })
            .fail(function(){
                alert('Error executing AJAX request!');
            });
    });
    $(document).on('click', '.torrent-stop-button', function(e) {
        e.preventDefault();
        $.post('/api/transmission/'+$(this).attr('data-id')+'/stop', {})
            .done(function(){
                $('#torrentInfoModal').modal('toggle');
            })
            .fail(function(){
                alert('Error executing AJAX request!');
            });
    });
    $(document).on('click', '.torrent-verify-button', function(e) {
        e.preventDefault();
        $.post('/api/transmission/'+$(this).attr('data-id')+'/verify', {})
            .done(function(){
                $('#torrentInfoModal').modal('toggle');
            })
            .fail(function(){
                alert('Error executing AJAX request!');
            });
    });
    $(document).on('keypress', '.torrent-info-name-field', function(e) {
        if(e.which == 13) {
            $.post('/api/transmission/'+$(this).attr('data-id')+'/info', {'name': $(this).val()})
                .done(function() {

                })
                .fail(function() {

                });
        }
    });
    $(document).on('submit', '.searchform', function(e) {
        e.preventDefault();
        query = $('.searchfield').val();
        if(query == '') {
            $('body').data('listUrl', '/api/transmission/list');
        } else {
            $('body').data('listUrl', '/api/transmission/list?filter='+query);
        }
    });
});
