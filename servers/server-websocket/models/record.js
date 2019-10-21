var mongoose = require('mongoose');
var Types = mongoose.Schema.Types;

var schema = mongoose.Schema({
    account_id: Types.ObjectId,
    file_record_id: Types.String,
    type: Types.String,
    data: Types.Mixed,
    date_recorded: Types.Date
});

var Record = mongoose.model('records', schema);
module.exports = Record;

// Example Usage
// type = "bp" or "bos"
/* Example Data
data: {
    value_name: "String", values: [Array]
}
*/



/*
Record.findOne(function (err, record) {
    if (err) return console.error(err);
    console.log(record);
});
*/
