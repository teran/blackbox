$(document).ready(function() {
    setInterval(function() {
        $.getJSON('/api/transmission/list', function(data) {
            var items = ['<div class="navbar transmission-meta"><button class="btn btn-primary add-torrent-button">Add torrent</button></div>'];
            $.each(data, function(key, val) {
                items.push(
                    '<li class="torrent-list-item" data-id="'+val.id+'">' +
                        val.name +
                        '<div class="progress">' +
                            '<div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: '+val.progress+'%">' +
                                Math.round(val.progress) + '% complete' +
                            '</div>' +
                        '</div>' +
                    '</li>'
                );
            });
            $('.torrent-list-container').html(
            $('<ul/>', {
                'class': 'torrent-list',
                'html': items.join('')
            }));
        })
    }, 1000);
});
