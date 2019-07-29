var express = require('express');
var app = express();

var server = require('http').createServer(app);
var io = require('socket.io')(server);

// options: default 'w' -writing, 'a' -appending, 'a+' -read and append
var fs = require("fs");
const path = require('path');



const pydir = __dirname + "../../../py/"

var t_start = 0;
var t_cur1 = 0;
var t_cur2 = 0;
var t_cur3 = 0;

var ecg_stream;
var ppgarm_stream;
var ppgleg_stream;

var record_id = 0;
var start_recording = false;

fs.readFile(__dirname + "/files/record_id", 'utf8', (err, data) => {
	if (err) throw err;
	record_id = data;
});

app.use(express.static(__dirname + '/public'));

// TODO: NAV BAR, PARA BUTTONS NALANG PAG NAVIGATE INSTEAD OF URL
app.get('/ecg', function(req, res){
	res.sendFile(__dirname + '/html/ecgdisplay.html');
});

app.get('/ppgarm', function(req, res) {
	res.sendFile(__dirname + '/html/ppgarmdisplay.html');
});

app.get('/ppgleg', function(req, res) {
	res.sendFile(__dirname + '/html/ppglegdisplay.html');
});

// ARM ARM ARM ARM ARM
app.post('/processppgarmdata', function(req, res) {
	// get record id of file to be processed
	rcrd = (parseInt(record_id) - 1).toString()
	if(rcrd < 0) {
		res.sendFile(__dirname + '/public/html/data/empty.html');
		return;
	}
	console.log("Processing PPG ARM: Record " + rcrd)

	// script arguments
	data_path = path.resolve(__dirname + "/files/ppgarm/" + rcrd)
	fn_figure = "ppg_arm_"

	// run the python script
	const { spawn } = require('child_process');
	var pyscript = path.resolve(pydir + "ppg_test/ppg_processing.py")
	var pyexec = path.resolve(pydir + "/venv/Scripts/python")
	const pythonProcess = spawn(pyexec,[pyscript, data_path, fn_figure]);

	// console.log(pyexec)
	// console.log(pyscript)
	// console.log(data_path)

	pythonProcess.stdout.on('data', (data) => {
		console.log(data.toString())
	});

	pythonProcess.stdout.on('close', (data) => {
		console.log("Python process exited...")
	});
	res.json("OK");
});

// Feature extraction results on the browser
app.get('/viewppgarmdata', function(req, res) {
	res.sendFile(__dirname + '/public/html/data/ppgarmdata.html');
});

// LEG LEG LEG LEG LEG
app.post('/processppglegdata', function(req, res) {
	// get record id of file to be processed
	rcrd = (parseInt(record_id) - 1).toString()
	if(rcrd < 0) {
		res.sendFile(__dirname + '/public/html/data/empty.html');
		return;
	}
	console.log("Processing PPG LEG: Record " + rcrd)

	// script arguments
	data_path = path.resolve(__dirname + "/files/ppgleg/" + rcrd)
	fn_figure = "ppg_leg_"

	// run the python script
	const { spawn } = require('child_process');
	var pyscript = path.resolve(pydir + "ppg_test/ppg_processing.py")
	var pyexec = path.resolve(pydir + "/venv/Scripts/python")
	const pythonProcess = spawn(pyexec,[pyscript, data_path, fn_figure]);

	// console.log(pyexec)
	// console.log(pyscript)
	// console.log(data_path)

	pythonProcess.stdout.on('data', (data) => {
		console.log(data.toString())
	});

	pythonProcess.stdout.on('close', (data) => {
		console.log("Python process exited...")
	});
	res.json("OK");
});

app.get('/viewppglegdata', function(req, res) {
	res.sendFile(__dirname + '/public/html/data/ppglegdata.html');
});

// ALL THE RAW SIGNALS
app.get('/raw', function(req, res) {
	res.sendFile(__dirname + '/public/html/raw.html');
});


// GET RECORD ID NUNG LATEST NA MAY RECORD NA
app.get('/recordedId', function(req,res) {
	fs.readFile(__dirname + "/files/record_id", 'utf8', (err, data) => {
		if (err) throw err;
		rcrded_id = parseInt(data) - 1
		if (rcrded_id < 0) {
			res.json("None");
		} else {
			res.json(rcrded_id.toString());
		}
	});
});

// GET RECORD ID NUNG LATEST NA MARERECORD
app.get('/recordId', function(req,res) {
	fs.readFile(__dirname + "/files/record_id", 'utf8', (err, data) => {
		if (err) throw err;
		record_id = data;
		res.json(record_id);
	});
});

// NEW RECORD ID
app.post('/newRecordId', function(req,res) {
	start_recording = false;
	record_id ++;
	fs.writeFile(__dirname + "/files/record_id", record_id, (err) => {
		if (err) throw err;
		res.status(200);
		console.log('Record Id Updated');
	});
});

// START RECORDING
app.post('/startRecording', function(req, res) {
	if(start_recording) {
		return;
	}

	console.log("Start Recording: " + record_id);

	ecg_stream = fs.createWriteStream(__dirname + "/files/ecg/" + record_id);
	ppgarm_stream = fs.createWriteStream(__dirname + "/files/ppgarm/" + record_id);
	ppgleg_stream = fs.createWriteStream(__dirname + "/files/ppgleg/" + record_id);
	start_recording = true;
});

function deleteFilesInDir(directory) {
	fs.readdir(directory, (err, files) => {
		if (err) throw err;
		
		for (const file of files) {
			fs.unlink(path.join(directory, file), err => {
				if (err) {
					console.log(err);
				}
			});
		}
	});
}

app.get('/reset', function(req, res) {
	deleteFilesInDir(__dirname + "/files/ecg");
	deleteFilesInDir(__dirname + "/files/ppgarm");
	deleteFilesInDir(__dirname + "/files/ppgleg");
	deleteFilesInDir(__dirname + "/public/result");
	fs.writeFile(__dirname + "/files/record_id", 0, (err) => {
		if (err) {
			console.log(err);
		}
	});
	res.json("OK");
});

io.on('connection', function(socket){
	console.log("a user has connected: " + socket.id );

	socket.on('send', function(msg) {
		// console.log(msg);
		// console.log(msg.split(','));

		splitted = msg.split(',');
		address = splitted[0];
		
		/*
			2 data points per send
			data = [
				{ time: splitted[1], value: splitted[2] },
				{ time: splitted[3], value: splitted[4] }
			];
		*/
		// 1 data point per send
		data = [
			{ time: splitted[1], value: splitted[2] }
		];
		
		file_entry = splitted[1] + ',' + splitted[2];

		// emit to the sockets
		switch(address) {
			case '1':
				io.emit('update ecg', { data: data });
				break;
			case '2':
				io.emit('update ppg arm', { data: data });
				break;
			case '3':
				io.emit('update ppg leg', { data: data });
				break;
		}

		// record the data
		
		if(start_recording) {
			switch(address) {
				case '1':
					ecg_stream.write(file_entry + "\n");
					break;
				case '2':
					ppgarm_stream.write(file_entry + "\n");
					break;
				case '3':
					ppgleg_stream.write(file_entry + "\n");
					break;
			}
		}



		// TODO: Start Message to indicate start plotting
		// TODO: Isave ung data
		// TODO: ung key para alam what the data is
		// setImmediate(function() {
		//     io.emit('display', { data: msg });
		// });
	});

	/*
	// test lang
	var interval = 100;
	setInterval(function () {
		var f = 0.1;
		var t = (t_cur1 - t_start) / 1000.0;
		var value = Math.round(512.0 * Math.sin(2 * Math.PI * f * t) + 512.0);
		var data = [
			{ time: t_cur1, value: value }
		];
		if(start_recording) {
			var ecg_wr = t_cur1 + ',' + value + "\n";
			ecg_stream.write(ecg_wr);
		}
		io.emit('update ecg', { data: data })
		t_cur1 += interval
	}, interval);


	setInterval(function () {
		var f = 0.1;
		var t = (t_cur2 - t_start) / 1000.0;
		var value2 = Math.round(512.0 * Math.sin(2 * Math.PI * f * 2 * t) + 512.0);
		var data2 = [
			{ time: t_cur2, value: value2 }
		];
		io.emit('update ppg arm', { data: data2 })
		t_cur2 += interval
	}, interval);

	setInterval(function () {
		var f = 0.1;
		var t = (t_cur3 - t_start) / 1000.0;
		value3 = Math.round(512.0 * Math.sin(2 * Math.PI * f * 4 * t) + 512.0);
		data3 = [
			{ time: t_cur3, value: value3 }
		];
		io.emit('update ppg leg', { data: data3 })
		t_cur3 += interval
	}, interval);
	*/
});

server.listen(6969, function(){
	console.log('listening on *:6969');
});

//TO RUN
// cd server-websocket
// node iosocket.js