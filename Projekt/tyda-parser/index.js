var express = require('express');
var url = require('url');
var request = require('request');
var cheerio = require('cheerio');

var app = express();

app.get('/', function(req, res) {
  var url = 'http://tyda.se/search/' + req.query.word + "?lang[0]=" + req.query.from + "&lang[1]=" + req.query.to;
  request.get(url, function(error, body, response) {
    $ = cheerio.load(response);
    console.log($('h2').text());
  });

  res.json({
    "json": "response"
  });
});

app.listen(process.env.PORT || 8080);