// Heritage Parlor — Data Loader
(function() {
'use strict';

window.ENTRIES = [];

// Show loading state
var grid = document.getElementById('card-grid');
if (grid) grid.innerHTML = '<div class="loading-state"><p>Loading 502 games\u2026</p></div>';

fetch('data/entries.json')
  .then(function(r) { return r.json(); })
  .then(function(data) {
    window.ENTRIES = data;
    document.dispatchEvent(new CustomEvent('data-loaded'));
  })
  .catch(function(err) {
    console.error('Failed to load entries:', err);
    if (grid) grid.innerHTML = '<div class="loading-state"><p>Failed to load games. Please refresh.</p></div>';
  });

})();
