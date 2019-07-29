var PORT = 33333;
var HOST = '127.0.0.1';

var dgram = require('dgram');
var message = new Buffer.from("My Kungfu is Good");


var client = dgram.createSocket('udp4');

t_start = 0;
t = 0;
f = 0.5; // 0.5 Hz


setInterval(() => {
  // get value
  value = Math.round(512 * Math.sin(2 * Math.PI * f * (t/1000)) + 512);
  t += 10;

  var val_buf = new Buffer.from(value.toString());

  client.send(val_buf, 0, val_buf.length, PORT, HOST, function(err, bytes) {
    if (err) throw err;
    console.log('UDP message sent to ' + HOST +':'+ PORT);
  });

}, 10);



