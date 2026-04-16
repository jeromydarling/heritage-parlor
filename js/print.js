// Heritage Parlor — Print Game
(function() {
'use strict';

window.printGame = function(id) {
  var w = window.open('', '_blank');
  if (!w) { alert('Please allow pop-ups to print.'); return; }
  var e = window.ENTRIES.find(function(x) { return x.id === id; });
  var base = location.href.replace(/\/[^/]*$/, '/');
  w.document.write('<!DOCTYPE html>' +
'<html><head>' +
'<base href="' + base + '">' +
'<title>Print: ' + (e ? e.title : id) + '</title>' +
'<style>' +
'  @page { size: letter; margin: 0; }' +
'  @media print { body { margin: 0; } .page { page-break-after: always; } .page:last-child { page-break-after: auto; } }' +
'  body { margin: 0; padding: 0; background: #fff; font-family: Georgia, serif; }' +
'  .page { width: 8.5in; height: 11in; display: flex; align-items: center; justify-content: center; overflow: hidden; }' +
'  .page img { width: 100%; height: 100%; object-fit: contain; }' +
'  .no-print { text-align: center; padding: 12px; background: #f5f0e6; border-bottom: 1px solid #ddd; }' +
'  .no-print button { font: 600 14px Georgia, serif; background: #8b4513; color: #fff; border: none; padding: 8px 24px; border-radius: 6px; cursor: pointer; }' +
'  @media print { .no-print { display: none; } }' +
'</style>' +
'</head><body>' +
'<div class="no-print"><button onclick="window.print()">\ud83d\udda8 Print This Game</button></div>' +
'<div class="page"><img src="svgs/page1/' + id + '.svg" alt="Page 1 \u2014 Game Board" /></div>' +
'<div class="page"><img src="svgs/page2/' + id + '.svg" alt="Page 2 \u2014 Instructions" /></div>' +
'</body></html>');
  w.document.close();
  setTimeout(function() { w.print(); }, 600);
};

})();
