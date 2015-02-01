var express = require('express');

// Constants
var PORT = 8080;

// App
var app = express();
app.get('/', function (req, res) {
  console.log('Request received');
  res.send('Yo, what up?\n');
});

app.listen(PORT);
console.log('Running on http://localhost:' + PORT);
