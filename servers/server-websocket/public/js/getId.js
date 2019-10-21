$.ajax({
    type: 'GET',
    url: 'http://localhost:6969/recordId',
    dataType: 'json',
    success: function (data) {
        $('h4.record-id').text(data);
    }
});