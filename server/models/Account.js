var con = require('../db/connection');


var Account = function(account) {
    this.AccountId = account.AccountId;
    this.Username = account.Username;
    this.Password = account.Password;
    this.FirstName = account.FirstName;
    this.LastName = account.LastName;
    this.MiddleName = account.MiddleName;
    this.Sex = account.Sex;
    this.Email = account.Email;
    this.Contact = account.Contact;
    this.Birthday = account.Birthday;
    this.AccountType = account.AccountType;
}

Account.addAccount = function(account, callback) {
    con.query(`INSERT INTO Account(Username, Password, FirstName, LastName, MiddleName, \
                Sex, Email, Contact, Birthday, AccountType) \
                VALUES ("${account.Username}", "${account.Password}", "${account.FirstName}", \
                    "${account.LastName}", "${account.MiddleName}", "${account.Sex}", "${account.Email}", \
                    "${account.Contact}", "${account.Birthday}", "${account.AccountType}")`, 
                function(err, res) {
                    if(err) {
                        callback(err, null);
                    } else {
                        callback(null, res.insertId);
                    }
    });
}

Account.getAccounts = function(callback) {
    con.query(`SELECT * FROM Account`, function(err, res) {
        if (err) {
            callback(err, null);
        } else {
            callback(null, res);
        }
    })
}

Account.getAccountById = function(id, callback) {
    con.query(`SELECT * FROM Account WHERE AccountId = ${id}`, function(err, res) {
        if(err) {
            callback(err, null);
        } else {
            callback(null, res);
        }
    })
}


module.exports = Account
