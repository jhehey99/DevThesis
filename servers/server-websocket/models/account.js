var mongoose = require('mongoose');
var Types = mongoose.Schema.Types;
var schema = mongoose.Schema({
	username: Types.String,
	password: Types.String,
	name: Types.String
});

var Account = mongoose.model('accounts', schema);
module.exports = Account;

// Example Usages
// require the models
// var Account = require('./models/account');

/* SAVING AN ACCOUNT
var test = new Account({
	username: "test",
	password: "test",
	name: "test"
});

test.save(function (err) {
	if (err) return console.error(err);
	console.log("account saved");
});

test user id: 5d81e191c0535630a8f3b733

*/

/* FINDING ALL ACCOUNTS
Account.find(function (err, accounts) {
	if (err) return console.error(err);
	console.log(accounts);
});
*/

/* FINDING AN ACCOUNT BY USERNAME
Account.findOne({ username: "user1", }, function (err, account) {
	if (err) return console.error(err);
	console.log(account);
});
*/

