$('document').ready(function() {
    setInterval(function() {
        $.getJSON('/api/transmission/list.json', function(data) {
            items = [];
            $.each( data, function( key, val ) {
                items.push(
                    '<li class="torrent-list-item">' +
                        '<a href="#">' + val.name +
                        '<div class="progress progress-striped">' +
                            '<div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: '+val.progress+'%">' +
                                val.progress + '% complete' +
                            '</div>' +
                        '</div></a>'+
                    '</li>'
                );
            });
            $('.torrent-list-container').html(
            $( "<ul/>", {
                "class": "torrent-list",
                html: items.join( "" )
            }));
        })
    }, 1000);
});
