var mongoose = require('mongoose');
// mongoose.connect("mongodb+srv://monggo:monggo@cluster0-b8ubw.gcp.mongodb.net/test?retryWrites=true&w=majority", {useNewUrlParser: true});
mongoose.connect("mongodb://localhost:27017/thesismongo", {useNewUrlParser: true});
var Schema = mongoose.Schema;

var SampleSchema = new Schema({
    id: Number,
    times: Array,
    values: Array,
    startTime: String
});


module.exports = mongoose.model('Sample', SampleSchema);