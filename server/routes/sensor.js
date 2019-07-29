var express = require('express');
var router = express.Router();
var fs = require('fs');

var Account = require('../models/Account');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.json({SENSOR: "SENSOR"});
});

// Arduino will send post request to this route
router.post('/send', function(req, res, next) {
    // Time - Voltage - Sensor Type [ECG, PPG ARM, PPG LEG]
    // 3 Sensors
    // sensors will get analog voltage for 30 seconds
    // arduino will get 30 seconds worth of signal from each sensor
    // then send to server
    // res.json(req.body)
    
    var data = req.body;

    fs.writeFile("files/temps.txt", JSON.stringify(data), function(err) {
        if (err) console.log(err);
        res.json("Successfully Written to File.")
    });
});

// from the mobile app kailangan may way din para makuha ung sensor data
// Get - /:patientId/:ung latest -> use this pag update from app
// Get - /:patientId/:range from latest -> use this pag first load nung app


router.get('/test', function(req, res, next) {
  res.json("ETO UNG DATA");
})


module.exports = router;
