// Heritage Parlor — Filtering
(function() {
'use strict';

window.activeFilter = 'all';
window.activePlayFilter = 'all';
window.searchQuery = '';
window.visibleCount = window.PAGE_SIZE;

window.getFiltered = function() {
  var items = window.ENTRIES;
  if (window.activeFilter !== 'all') {
    items = items.filter(function(e) { return e.category === window.activeFilter; });
  }
  if (window.activePlayFilter !== 'all') {
    items = items.filter(function(e) { return e.playability === window.activePlayFilter; });
  }
  if (window.searchQuery) {
    var q = window.searchQuery.toLowerCase();
    items = items.filter(function(e) {
      return e.title.toLowerCase().includes(q) ||
        e.original_description.toLowerCase().includes(q) ||
        e.modern_explanation.toLowerCase().includes(q) ||
        (e.tags && e.tags.some(function(t) { return t.toLowerCase().includes(q); })) ||
        e.source_book.toLowerCase().includes(q) ||
        e.category.replace(/-/g, ' ').includes(q) ||
        (e.subcategory && e.subcategory.replace(/-/g, ' ').includes(q));
    });
  }
  return items;
};

window.renderFilters = function() {
  var row = document.getElementById('filter-row');
  var counts = {};
  window.ENTRIES.forEach(function(e) { counts[e.category] = (counts[e.category] || 0) + 1; });

  var html = '<button class="filter-pill ' + (window.activeFilter === 'all' ? 'filter-pill--active' : '') + '" onclick="setFilter(\'all\')">All <span class="filter-pill__count">' + window.ENTRIES.length + '</span></button>';

  var order = ['parlor-game','card-game','magic-trick','puzzle','word-game','physical-game','board-game','folk-game','scientific-recreation'];
  order.forEach(function(cat) {
    if (counts[cat]) {
      var cfg = window.CAT_CONFIG[cat] || {};
      html += '<button class="filter-pill ' + (window.activeFilter === cat ? 'filter-pill--active' : '') + '" onclick="setFilter(\'' + cat + '\')">' + (cfg.icon || '') + ' ' + (cfg.label || cat) + ' <span class="filter-pill__count">' + counts[cat] + '</span></button>';
    }
  });

  row.innerHTML = html;
};

window.renderPlayFilters = function() {
  var row = document.getElementById('play-filter-row');
  if (!row) return;
  var counts = {};
  var filtered = window.ENTRIES;
  if (window.activeFilter !== 'all') filtered = filtered.filter(function(e) { return e.category === window.activeFilter; });
  filtered.forEach(function(e) { counts[e.playability] = (counts[e.playability] || 0) + 1; });

  var html = '<button class="play-pill ' + (window.activePlayFilter === 'all' ? 'play-pill--active' : '') + '" onclick="setPlayFilter(\'all\')">All</button>';

  var order = ['playable_now','easy_to_source','craftable','specialty_needed','extinct_equipment','dangerous'];
  order.forEach(function(tier) {
    if (counts[tier]) {
      var cfg = window.PLAY_CONFIG[tier] || {};
      html += '<button class="play-pill ' + (window.activePlayFilter === tier ? 'play-pill--active' : '') + '" onclick="setPlayFilter(\'' + tier + '\')" style="--pill-color:' + cfg.color + '">' + cfg.icon + ' ' + cfg.label + ' <span class="play-pill__count">' + counts[tier] + '</span></button>';
    }
  });

  row.innerHTML = html;
};

})();
