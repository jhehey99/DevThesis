var con = require('../db/connection');


var Patient = function(patient) {
    this.AccountId = patient.AccountId;
    this.PatientId = patient.PatientId;
}

var addPatient = function(patient, callback) {
    con.query(`INSERT INTO Patient(AccountId, PatientId) \
                VALUES("${patient.AccountId}", "${patient.PatientId}")`, 
                function(err, result) {
                    if(err) {
                        callback(err, null);
                    } else {
                        callback(null,result);
                    }
                });
}
