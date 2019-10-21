function refresh() {
    $.ajax({
        type: 'GET',
        url: '/refresh',
        dataType: 'json',
        success: function (data, status) {
            console.log(data + " " + status);
        }
    });
}

window.onbeforeunload = refresh;