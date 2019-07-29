var PORT = 33333;
var HOST = '192.168.41.1';

var dgram = require('dgram');
var udp_socket = dgram.createSocket('udp4');

const io = require('socket.io-client');

// var fs = require('fs');
var socket = io('http://192.168.41.1:6969');

// TODO: try io.connect
// udp_socket.on('listening', function() {
//   var address = udp_socket.address();
// //  console.log('UDP udp_socket listening on ' + address.address + ':' + address.port);
// });

udp_socket.on('message', function(message, remote) {
  // console.log(remote.address + ':' + remote.port +' - ' + message);
  // bago mag send ng stream
  // sa webpage, dun i-se-set kung babaguhin na ung key ng bawat sensor node

  // kukuha ng key si nodemcu sa api para malaman kung saan i-se-save
  // ^ every node startup to

  // pag may key na si nodemcu, mag stream na sya sa udp server
  // using the key, dun malalaman where i-sesave and what kind of sensor sya
  // pagka kuha mo ng message, i-save mo sa file na associated para dun

  socket.emit('display ecg', message);

  // fs.appendFile('../files/file1.txt', message + '\n', function(err) {
  //   if(err) throw err;
  // });
});

// fs.writeFile('../files/file1.txt', '', function(err) {
//   if(err) throw err;
//   console.log("Created File");
// })

setInterval(() => {
  socket.emit('send', "69");
}, 1000);

setInterval(() => {
  socket.emit('receive', "69");
}, 1000);

udp_socket.bind(PORT, HOST);
