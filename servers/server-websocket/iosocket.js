var express = require('express');
var app = express();
var bodyParser = require('body-parser');


var server = require('http').createServer(app);
var io = require('socket.io')(server);

var mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/thesisDB', { useNewUrlParser: true, useUnifiedTopology: true });

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function () {
	// we're connected!
	console.log("connected to the database");
});

// require the models
var Account = require('./models/account');
var BloodPressureRecord = require('./models/bloodPressureRecord');
var Record = require("./models/record");

var uniqid = require('uniqid');

console.log(uniqid());

//TODO ADD A GET LAST RECORDEDID ROUTE TO VIEW LATEST SIGNAL

// options: default 'w' -writing, 'a' -appending, 'a+' -read and append
var fs = require("fs");
const path = require('path');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(__dirname + '/public'));
app.set('view engine', 'ejs');


const pydir = __dirname + "../../../py/"

var t_start = 0;
var t_cur1 = 0;
var t_cur2 = 0;
var t_cur3 = 0;

var ecg_stream;
var ppgarm_stream;
var ppgleg_stream;
var ppgarmred_stream;

var bp_write_streams = [];
var bos_write_streams = [];

var record_id = 0;
var start_recording = false;
var recording_bp = false;
var recording_bos = false;
var nodemcu_id = 0;
var nodemcu_verified = false;

var PpgArmStateEnum = {
	NULL: 0,
	IR: 1,
	RED: 2
}

var ppgarm_state = PpgArmStateEnum.NULL

function onIRtoRED() {
	console.log("onIRtoRED");
}

function onREDtoIR() {
	console.log("onREDtoIR");
	clearDataStreams();
}

function updatePpgArmState(address) {
	// update state of the ppg arm node
	if (address == '1') {
		if (ppgarm_state == PpgArmStateEnum.RED) {
			// RED -> IR
			onREDtoIR();
		}
		ppgarm_state = PpgArmStateEnum.IR;
	} else if (address == '4') {
		if (ppgarm_state == PpgArmStateEnum.IR) {
			// IR -> RED
			onIRtoRED();
		}
		ppgarm_state = PpgArmStateEnum.RED;
	}
}

var ModeEnum = {
	BloodPressure: 1,
	OxygenSaturation: 2
};

var parameter_mode = ModeEnum.BloodPressure;

// TODO: NAV BAR, PARA BUTTONS NALANG PAG NAVIGATE INSTEAD OF URL
app.get('/ecg', function (req, res) {
	res.sendFile(__dirname + '/html/ecgdisplay.html');
});

app.get('/ppgarm', function (req, res) {
	res.sendFile(__dirname + '/html/ppgarmdisplay.html');
});

app.get('/ppgleg', function (req, res) {
	res.sendFile(__dirname + '/html/ppglegdisplay.html');
});

//TODO PALITAN UNG PAG PROCESS NG FILES
// ARM ARM ARM ARM ARM
app.post('/processppgarmdata', function (req, res) {
	// get record id of file to be processed
	rcrd = (parseInt(record_id) - 1).toString()
	if (rcrd < 0) {
		res.sendFile(__dirname + '/public/html/data/empty.html');
		return;
	}
	console.log("Processing PPG ARM: Record " + rcrd)

	// script arguments
	data_path = path.resolve(__dirname + "/files/ppgarm/" + rcrd)

	// run the python script
	const { spawn } = require('child_process');
	var pyscript = path.resolve(pydir + "ppg/ppg_processing.py")
	// var pyscript = path.resolve(pydir + "ppg_test/ppg_processing.py")
	var pyexec = path.resolve(pydir + "/venv/Scripts/python")
	const pythonProcess = spawn(pyexec, [pyscript, data_path]);

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
app.get('/viewppgarmdata', function (req, res) {
	res.sendFile(__dirname + '/public/html/data/ppgarmdata.html');
});

// LEG LEG LEG LEG LEG
app.post('/processppglegdata', function (req, res) {
	// get record id of file to be processed
	rcrd = (parseInt(record_id) - 1).toString()
	if (rcrd < 0) {
		res.sendFile(__dirname + '/public/html/data/empty.html');
		return;
	}
	console.log("Processing PPG LEG: Record " + rcrd)

	// script arguments
	data_path = path.resolve(__dirname + "/files/ppgleg/" + rcrd)

	// run the python script
	const { spawn } = require('child_process');
	var pyscript = path.resolve(pydir + "ppg/ppg_processing.py")
	// var pyscript = path.resolve(pydir + "ppg_test/ppg_processing.py")
	var pyexec = path.resolve(pydir + "/venv/Scripts/python")
	const pythonProcess = spawn(pyexec, [pyscript, data_path]);

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

app.get('/viewppglegdata', function (req, res) {
	res.sendFile(__dirname + '/public/html/data/ppglegdata.html');
});

// BOS BOS BOS BOS BOS IR AND RED LED SIGNALS
app.post('/processbosdata', function (req, res) {

	//TODO GET RECOIRD ID FROM THE POST BODY
	var id = req.body.record_id;
	//TODO FIND IF RECORD ID EXIST
	console.log("Processing BOS DATA: Record " + id);

	// script arguments
	var ir_data_path = path.resolve(__dirname + "/files/raw/bos/ppgarmir/" + id);
	var red_data_path = path.resolve(__dirname + "/files/raw/bos/ppgarmred/" + id);
	var result_path = path.resolve(__dirname + "/files/result/bos/" + id);

	// run the python script
	const { spawn } = require('child_process');
	var pyscript = path.resolve(pydir + "bos/bos_processing.py");
	var pyexec = path.resolve(pydir + "/venv/Scripts/python");
	const pythonProcess = spawn(pyexec, [pyscript, ir_data_path, red_data_path, result_path]);

	pythonProcess.stdout.on('data', (data) => {
		console.log(data.toString());
		// TODO: dito mo kunin ung mga data like components average and ratio then idisplay mo sa html file para lng makita hehe
	});

	pythonProcess.stdout.on('close', (data) => {
		console.log("Python process exited...");
	});
	res.json("OK");
});

// app.get('/viewbosdata', function (req, res) {
// 	res.sendFile(__dirname + '/public/html/data/bosdata.html');
// });

//TODO RESET FIGS, DELETES ALL FIGURES IN THE public/result folder
app.get('/viewlatestbosdata', function (req, res) {
	// get the latest data acc
	Record.find({ type: "bos" }).sort({ date_recorded: -1 }).limit(1).then((records) => {
		var file_record_id = records[0].file_record_id;
		console.log("Viewing bos data of " + file_record_id);
		var src_ir = path.resolve(__dirname + "/files/result/bos/" + file_record_id + "_ir.svg");
		var src_red = path.resolve(__dirname + "/files/result/bos/" + file_record_id + "_red.svg");
		var dest_ir = path.resolve(__dirname + "/public/result/bos/bos_ir.svg");
		var dest_red = path.resolve(__dirname + "/public/result/bos/bos_red.svg");

		//if file exists copy the svg files to result dir and rename
		if (fs.existsSync(src_ir) && fs.existsSync(src_red)) {
			fs.copyFileSync(src_ir, dest_ir);
			fs.copyFileSync(src_red, dest_red);
		} else {
			console.log("BOS Data for " + file_record_id + " doesn't exists");
			return res.sendFile(__dirname + '/public/html/data/empty.html');
		}
	}).catch((err) => {
		console.log(err);
		return res.sendFile(__dirname + '/public/html/data/empty.html');
	});

	var ir_fig = "/result/bos/bos_ir.svg";
	var red_fig = "/result/bos/bos_red.svg";
	res.render('viewBosData', { ir_fig: ir_fig, red_fig: red_fig });
});


// ALL THE RAW SIGNALS
app.get('/bp', function (req, res) {
	// FOR BLOOD PRESSURE
	parameter_mode = ModeEnum.BloodPressure;
	if (nodemcu_verified) {
		console.log("set mode to bp");
		io.to(`${nodemcu_id}`).emit('bp', nodemcu_id);
	}
	res.sendFile(__dirname + '/public/html/bp.html');
});

app.get('/bos', function (req, res) {
	// FOR BLOOD OXYGEN SATURATION
	parameter_mode = ModeEnum.OxygenSaturation;
	if (nodemcu_verified) {
		console.log("set mode to bos");
		io.to(`${nodemcu_id}`).emit('bos', nodemcu_id);
	}
	res.sendFile(__dirname + '/public/html/bos.html');
});

// GET RECORD ID NUNG LATEST NA MARERECORD
app.get('/recordId', function (req, res) {
	res.json(uniqid());
});

app.get('/recordId2', function (req, res) {
	//TODELETE
	fs.readFile(__dirname + "/files/record_id", 'utf8', (err, data) => {
		if (err) throw err;
		record_id = data;
		res.json(record_id);
	});
});

// NEW RECORD ID
app.post('/newRecordId', function (req, res) {
	//TODELETE
	start_recording = false;
	record_id++;
	fs.writeFile(__dirname + "/files/record_id", record_id, (err) => {
		if (err) throw err;
		res.status(200);
		console.log('Record Id Updated');
	});
});

// START RECORDING
function recordingTimeout(time, type) {
	console.log(time);
	setTimeout(function () {
		if (type == "bp" && recording_bp) {
			recording_bp = false;
			console.log("Recording BP Timeout");
		}
		if (type == "bos" && recording_bos) {
			recording_bos = false;
			console.log("Recording BOS Timeout");
		}
	}, time);
}

app.post('/startRecordingBP', function (req, res) {
	if (recording_bp) {
		return;
	}
	var id = req.body.record_id;
	var time = req.body.time;
	console.log("Start Recording Blood Pressure: " + id);

	// clear the streams array then create new streams
	bp_write_streams = [];
	bp_write_streams.push(fs.createWriteStream(__dirname + "/files/raw/bp/ecg/" + id));
	bp_write_streams.push(fs.createWriteStream(__dirname + "/files/raw/bp/ppgarm/" + id));
	bp_write_streams.push(fs.createWriteStream(__dirname + "/files/raw/bp/ppgleg/" + id));

	// recordingTimeout(time, "bp");
	recording_bp = true;
	res.send("recording started");
});

app.post('/startRecordingBOS', function (req, res) {
	if (recording_bos) {
		return;
	}
	var id = req.body.record_id;
	var time = req.body.time;
	console.log("Start Recording Blood Oxygen Saturation: " + id);

	// clear the streams array then create new streams
	bos_write_streams = [];
	bos_write_streams.push(fs.createWriteStream(__dirname + "/files/raw/bos/ppgarmir/" + id));
	bos_write_streams.push(fs.createWriteStream(__dirname + "/files/raw/bos/ppgarmred/" + id));

	// recordingTimeout(time, "bos");
	recording_bos = true;
	res.send("recording started");
});

app.post('/startRecording', function (req, res) {
	// TODELETE
	//TODO[1]: get the record id from the post data
	if (start_recording) {
		return;
	}
	console.log("Start Recording: " + record_id);

	ecg_stream = fs.createWriteStream(__dirname + "/files/ecg/" + record_id);
	ppgarm_stream = fs.createWriteStream(__dirname + "/files/ppgarm/" + record_id);
	ppgleg_stream = fs.createWriteStream(__dirname + "/files/ppgleg/" + record_id);
	ppgarmred_stream = fs.createWriteStream(__dirname + "/files/ppgarmred/" + record_id);
	start_recording = true;

	res.send("hello");
});

// STOP RECORDING
// TODO SAVE SA DATABASE
app.post('/stopRecordingBP', function (req, res) {
	// get the record id from the body
	var id = req.body.record_id;
	console.log("Stop  Recording Blood Pressure: " + id);

	// save the record to the database
	Account.findOne({ username: "test" }, function (err_find, account) {
		if (err_find) {
			res.status(500);
			console.error(err_find);
			return res.send("Error! Account record not found...");
		}
		console.log(account);
		//TODO ETONG NEW RECORD AUSIN UNG VALUES
		var account_id = account._id;
		var new_record = new Record({
			account_id: account_id,
			file_record_id: id,
			type: "bp",
			data: [{
				value_type: "pulse transit time", values: [1, 2, 3, 4, 5]
			}],
			date_recorded: Date.now()
		});
		new_record.save(function (err_save) {
			if (err_save) {
				res.status(500);
				console.error(err_save);
				return res.send("Error! Record can't be saved...");
			}
			return console.log("Record " + id + " has been saved to account id: " + account_id);
		});
	});

	recording_bp = false;
	res.status(200);
	res.send("BP Recording Stopped");
});

app.post('/stopRecordingBOS', function (req, res) {
	var id = req.body.record_id;
	console.log("Stop  Recording Blood Oxygen Saturation: " + id);

	// save the record to the database
	Account.findOne({ username: "test" }, function (err_find, account) {
		if (err_find) {
			res.status(500);
			console.error(err_find);
			return res.send("Error! Account record not found...");
		}
		// console.log(account);
		//TODO ETONG NEW RECORD AUSIN UNG VALUES
		var account_id = account._id;
		var new_record = new Record({
			account_id: account_id,
			file_record_id: id,
			type: "bos",
			data: [{
				value_type: "ac dc ratio", values: [6, 7, 8, 9, 10]
			}],
			date_recorded: Date.now()
		});
		new_record.save(function (err_save) {
			if (err_save) {
				res.status(500);
				console.error(err_save);
				return res.send("Error! Record can't be saved...");
			}
			return console.log("Record " + id + " has been saved to account id: " + account_id);
		});
	});

	recording_os = false;
	res.status(200);
	res.send("BOS Recording Stopped");
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

app.get('/reset', function (req, res) {
	// raw files
	deleteFilesInDir(__dirname + "/files/raw/bp/ecg");
	deleteFilesInDir(__dirname + "/files/raw/bp/ppgarm");
	deleteFilesInDir(__dirname + "/files/raw/bp/ppgleg");
	deleteFilesInDir(__dirname + "/files/raw/bos/ppgarmir");
	deleteFilesInDir(__dirname + "/files/raw/bos/ppgarmred");

	// result files
	deleteFilesInDir(__dirname + "/files/result/bp");
	deleteFilesInDir(__dirname + "/files/result/bos");

	// public svg files
	deleteFilesInDir(__dirname + "/public/result/bp");
	deleteFilesInDir(__dirname + "/public/result/bos");

	// delete db collections
	Record.deleteMany({}, (err) => {
		if (err) res.json(err);
	});

	res.json("Ok");
});

app.get('/reset2', function (req, res) {
	//TODELETE
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

const maxEntryCount = 250;
//TODELETE
// var DataStream = {
// 	count: 0,
// 	times: [],
// 	values: [],
// 	push: function (time, value) {
// 		this.times.push(time);
// 		this.values.push(value);
// 		this.count++;
// 	},
// 	shift: function () {
// 		this.times.shift();
// 		this.values.shift();
// 		this.count++;
// 	}
// };

// var ppgarm_data = Object.create(DataStream);

function DataStream() {
	this.count = 0;
	this.times = [];
	this.values = [];
	this.push = function (time, value) {
		this.times.push(time);
		this.values.push(value);
		this.count++;
	};
	this.shift = function () {
		this.times.shift();
		this.values.shift();
		this.count--;
	};
	this.clear = function () {
		this.count = 0;
		this.times = [];
		this.values = [];
	};
}

// Create the data streams
var data_streams = []
for (var i = 0; i < 4; i++) {
	data_streams.push(new DataStream());
}
clearDataStreams();
function clearDataStreams() {
	console.log("clear data streams");
	data_streams.forEach((stream) => {
		stream.clear();
	});
}

// REFRESH DATA STREAMS
app.get('/refresh', function (req, res) {
	console.log("refresh");
	clearDataStreams();
	recording_bp = false;
	recording_bos = false;
	res.json("Ok");
});

io.on('connection', function (socket) {
	console.log("a user has connected: " + socket.id);

	socket.on('disconnect', function () {
		if (socket.id == nodemcu_id) {
			nodemcu_id = 0;
			nodemcu_verified = false;
			console.log("Nodemcu was disconnected...");
		}
	});

	socket.on('verify', function (msg) {
		if (msg == "nodemcu" && !nodemcu_verified) {
			nodemcu_id = socket.id;
			nodemcu_verified = true;
			io.to(`${nodemcu_id}`).emit('verified', nodemcu_id);
			console.log("Nodemcu verified with id: " + nodemcu_id);
		}
	})

	socket.on('send', function (msg) {
		// console.log(msg);
		splitted = msg.split(',');
		address = splitted[0];
		t = splitted[1];
		v = splitted[2];
		data = [
			{ time: splitted[1], value: splitted[2] }
		];

		file_entry = t + ',' + v;

		// use data_streams for emitting to the sockets and displaying the data
		address_int = parseInt(address) - 1;
		if (address_int >= 0 || address_int < data_streams.length) {
			data_streams[address_int].push(t, v);
			if (data_streams[address_int].count > 200) {
				data_streams[address_int].shift();
			}
		}


		// record the data for blood pressure
		if (recording_bp) {
			bp_write_streams[address_int].write(file_entry + "\n");
		}

		// record the data for blood oxygen saturation
		if (recording_bos) {
			var bos_index = 0;
			if (address == '4') {
				bos_index = 1;
			}
			bos_write_streams[bos_index].write(file_entry + "\n");
		}

		updatePpgArmState(address);

		// switch (address) {
		// 	case '1':
		// 		io.emit('update ecg', { data: data });
		// 		break;
		// 	case '2':
		// 		// i-store lang ung data dito
		// 		// ppgarm_data.push(data[0]);
		// 		ppgarm_data.push(t, v);

		// 		if (ppgarm_data.count > 200) {
		// 			ppgarm_data.shift();
		// 		}

		// 		// then may set interval na every 500ms, ginagawa ung ff:
		// 		// run py script to filter
		// 		// get filter output
		// 		// clear ppgarm_data
		// 		// emit the filter output to client 
		// 		// io.emit('update ppg arm', { data: data });

		// 		break;
		// 	case '3':
		// 		io.emit('update ppg leg', { data: data });
		// 		break;
		// 	case '4':
		// 		io.emit('update ppg arm red', { data: data });
		// 		break;
		// }



		// if (start_recording) {
		// 	switch (address) {
		// 		case '1':
		// 			ecg_stream.write(file_entry + "\n");
		// 			break;
		// 		case '2':
		// 			ppgarm_stream.write(file_entry + "\n");
		// 			break;
		// 		case '3':
		// 			ppgleg_stream.write(file_entry + "\n");
		// 			break;
		// 		case '4':
		// 			ppgarmred_stream.write(file_entry + "\n");
		// 			break;
		// 	}
		// }
	});
});

// IO EMIT Interval
var emit_list = [
	'update ecg',
	'update ppg arm',
	'update ppg leg',
	'update ppg arm red'
];

setInterval(function () {
	data_streams.forEach(function (data_stream, index) {
		io.emit(emit_list[index], { data: data_stream })
	});
}, 500);

server.listen(6969, function () {
	console.log('listening on *:6969');
});

//TO RUN
// cd server-websocket
// node iosocket.js