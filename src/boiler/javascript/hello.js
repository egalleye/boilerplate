#!/usr/bin/env nodejs
/*
Run: Need two terminals

## First terminal ##
 # Make file executable
  chmod +x hello.js
 # Run script
  ./hello.js

## Second terminal ##
 # Get info from the local host on port 8080 
  curl http://localhost:8080

*/

var http = require('http');
http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Hello World\n');
}).listen(8080, 'localhost');
console.log('Server running at http://localhost:8080/');
