var express = require('express');
var url = require('url');
var request = require('request');
var cheerio = require('cheerio');

var app = express();

function getTranslations(query, callback) {
  var url = 'http://tyda.se/search/' + query.word + "?lang[0]=" + query.from + "&lang[1]=" + query.to;
  request.get(url, function(error, body, response) {
    $ = cheerio.load(response);
    var translations = $('.box.box-searchresult:has(h2[id^="' + query.from + '"])')
      .find(".list.list-translations>li.item>a")
      .map(function(i, item) {
        var t = $(this).text();
        console.log(t);
        return t;
      })
      .toArray();
    callback(translations);
  });
};

app.get('/', function(req, res) {
  getTranslations(req.query, function(translations) {
    res.json({
      "translations": translations
    });
  });
});

app.listen(process.env.PORT || 8080);