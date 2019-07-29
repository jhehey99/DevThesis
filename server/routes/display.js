var express = require('express');
var router = express.Router();
var Sample = require('../models/Sample');

/* GET users listing. */
router.get('/', async function(req, res, next) {

  // var results = await Sample.find().sort({$natural:-1}).limit(50).sort({$natural:1}).exec();


  console.log("ETO UNG COUNT");
  var count = await Sample.countDocuments().exec();
  console.log(count);

  data_points = 50;
  skip_point = count - data_points;
  if(skip_point <= 0)
    skip_point = count

  var results = await Sample.find().skip(skip_point).exec();

  values = [];
  times = [];
  results.forEach(function(result) {

    // console.log(result.times);
    result.values.forEach(function(value) {
      values.push(value);
    });

    result.times.forEach(function(time) {
      times.push(time);
    });
  });


  // console.log(values);
  // console.log(times);
  // results = {
  //   times: [1,2,3,4,5],
  //   values: [2,4,6,9,10]
  // };
  // console.log(results);

  // res.render('display', {title: "Display Sample Chart"});
  res.render('test', {
    title: "Display Sample Chart", 
    times: times,
    values: values
  });
});

router.post('/', function(req, res, next) {
  data = req.body.data;
  id = 1;

  var sample = new Sample({
    id: 1,
    times: data.times,
    values: data.values,
    startTime: new Date().toUTCString()
  });

  sample.save(function (err, sample) {
    if (err) return console.error(err);
    // console.log(sample);
  });
  res.send("OKAY");
});



module.exports = router;
