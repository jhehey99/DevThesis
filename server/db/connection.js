var mysql = require("mysql");

// use this when nasa AWS na
var connection = mysql.createConnection({
    host     : 'aarnq4c7b25mbd.cdrbq3nncbgj.ap-southeast-1.rds.amazonaws.com',
    user     : 'thesisServerDB',
    password : 'jaspehehey99',
    port     : '3306',
    database : 'ebdb'
});

// for local development purposes
// var connection = mysql.createConnection({
//     host: "localhost",
//     user: "thesisdb_user",
//     password: "LrzuYb9xtdLKQbcz",
//     database: "thesisdb"
// });

module.exports = connection