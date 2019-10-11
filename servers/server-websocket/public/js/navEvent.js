
function startRecording(startUrl, stopUrl, processData) {
    var start = confirm("Start Recording?");
    if (!start) {
        return;
    }

    // initialize time
    // var init_time = $('h4.record-time').text();
    var init_time = $('#text_time').val();
    console.log(init_time);
    var time = init_time;
    var record_id = $('h4.record-id').text();

    // start saving dun sa record na naka-set
    //TODO[1]: POST WITH the obtained the current record id
    // $.post("http://localhost:6969/startRecording"); // TODELETE

    // let the server know to start recording
    $.post(startUrl, { record_id: record_id, time: time }, function (data, status) {
        console.log("Data: " + data + "\nStatus: " + status);
    });

    // the timer to know when recording stopped
    var timer = setInterval(() => {
        if (time <= 0) {
            // let the server know to stop recording
            $.post(stopUrl, { record_id: record_id }, function (data, status) {
                alert(data + "\nStatus: " + status);
            });

            // increment record id
            // $.post("http://localhost:6969/newRecordId"); // TODELETE

            processData();
            clearInterval(timer);
            location.reload();
        } else {
            time--; // decrement the timer every second
            $('h4.record-time').text(time);
        }
    }, 1000);
}

function bpStartRecording_clicked() {
    //TODO DITO RIN ISEND SA POST DATA UNG RECORD ID
    startRecording("/startRecordingBP", "/stopRecordingBP",
        function () {
            $.post("http://localhost:6969/processppgarmdata");
            $.post("http://localhost:6969/processppglegdata");
        });
}

function bosStartRecording_clicked() {
    var record_id = $('h4.record-id').text();
    startRecording("/startRecordingBOS", "/stopRecordingBOS",
        function () {
            $.post("http://localhost:6969/processbosdata", { record_id: record_id }, function (data, status) {
                console.log(data + " " + status);
            });
        });
}

function onTextTime_changed() {
    $('h4.record-time').text($('#text_time').val());
}