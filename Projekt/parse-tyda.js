$(document).ready(function() {
  var lang = "en";
  lang_results = $('.box.box-searchresult:has(h2[id^="' + lang + '"])');
  var translations = lang_results.find(".list.list-translations>li.item>a");
  translations = $.map(translations, function(item) {
    return item.textContent;
  });

  console.log("Föreslagna översättningar: " + translations);
});