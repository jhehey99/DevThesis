var express = require('express');
var router = express.Router();
var con = require('../db/connection');
var Account = require('../models/Account');

// // GET - test mysql connect
router.get('/mysqltest', function(req, res, next) {
    con.query('SELECT * FROM account', function(error, results, fields) {
        if(error) {
            res.send("DATABASE ERROR " + error.stack);
            return;
        }

        res.json(results);
    })
});

// GET - new account test
router.get('/new', function(req, res, next) {
    res.send("NEW ACCOUNT");
});

// POST - new account - /
router.post('/new', function(req, res, next) {
    var account = req.body;
    Account(req.body);
    Account.addAccount(account, function(err, result) {
        if(err) {
            res.json(err);
        } else {
            res.send("no error");
        }
    });
});

// GET - get accounts - /
router.get('/', function(req, res, next) {
    Account.getAccounts(function(err, result) {
        if(err) {
            res.send("error");
        } else {
            res.json(result);
        }
    })
});

// GET - get account by id
router.get('/:id', function(req, res, next) {
    var id = req.params.id;
    Account.getAccountById(id, function(err, result) {
        if(err) {
            res.send('error');
        } else {
            res.json(result);
        }
    })
});

module.exports = router;
