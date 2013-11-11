$(document).ready(function() {
    setInterval(function() {
        $.getJSON('/api/transmission/list', function(data) {
            var items = ['<div class="navbar transmission-meta"><button class="btn btn-primary add-torrent-button">Add torrent</button></div>'];
            $.each(data, function(key, val) {
                var percents = Math.round(val.progress);
                switch (val.status) {
                    case 'downloading':
                        style = 'progress-bar-downloading';
                        break;
                    case 'seeding':
                        style = 'progress-bar-seeding';
                        break;
                    case 'stopped':
                        style = 'progress-bar-stopped';
                        break;
                    case 'checking':
                        style = 'progress-bar-checking';
                        percents = Math.round(val.recheckProgress);
                        break;
                    default:
                        style = 'progress-bar-default';
                        break;
                }
                items.push(
                    '<li class="torrent-list-item" data-id="'+val.id+'">' +
                        val.name + '  (' + percents + '% complete' + ')' +
                        '<div class="progress">' +
                            '<div class="progress-bar '+style+'" role="progressbar" aria-valuenow="' + percents + '" aria-valuemin="0" aria-valuemax="100" style="width: ' + percents + '%">' +
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
