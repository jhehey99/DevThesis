function startRecording_clicked() {
    var start = confirm("Start Recording?");
    if(!start) {
        return;
    }

    // initialize time
    // var init_time = $('h4.record-time').text();
    var init_time = $('#text_time').val();
    console.log(init_time);
    var time = init_time;

    // start saving dun sa record na naka-set
    $.post("http://localhost:6969/startRecording");

    var timer = setInterval(() => {
        if (time <= 0) {
            // increment record id
            $.post("http://localhost:6969/newRecordId");
            $.post("http://localhost:6969/processppgarmdata");
            $.post("http://localhost:6969/processppglegdata");
            clearInterval(timer);
            alert("Record has been saved");
            location.reload();
        } else {
            time--;
            $('h4.record-time').text(time);
        }
    }, 1000);
}

function onTextTime_changed() {
    $('h4.record-time').text($('#text_time').val());
}