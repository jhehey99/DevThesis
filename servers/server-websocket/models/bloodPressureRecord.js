var mongoose = require('mongoose');
var Types = mongoose.Schema.Types;

var schema = mongoose.Schema({
    account_id: Types.ObjectId,
    record_id: Types.String,
    ecg_id: Types.Number,
    ppg_arm_id: Types.Number,
    ppg_leg_id: Types.Number,
    pulse_transit_times: Types.Mixed,
    date_recorded: Types.Date
});

var BloodPressureRecord = mongoose.model('blood_pressure_records', schema);
module.exports = BloodPressureRecord;

// Example Usage

/*
BloodPressureRecord.findOne(function (err, record) {
    if (err) return console.error(err);
    console.log(record);
});
*/
