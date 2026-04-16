// Heritage Parlor — Card Grid Rendering
(function() {
'use strict';

window.renderCards = function() {
  var grid = document.getElementById('card-grid');
  var items = window.getFiltered();
  var showing = items.slice(0, window.visibleCount);

  if (items.length === 0) {
    grid.innerHTML = '';
    document.getElementById('empty-state').style.display = 'block';
    document.getElementById('load-more-wrap').style.display = 'none';
    document.getElementById('search-count').textContent = 'No results';
    return;
  }

  document.getElementById('empty-state').style.display = 'none';
  document.getElementById('search-count').textContent = window.searchQuery || window.activeFilter !== 'all' || window.activePlayFilter !== 'all'
    ? 'Showing ' + Math.min(window.visibleCount, items.length) + ' of ' + items.length + ' entries'
    : '';

  grid.innerHTML = showing.map(function(e, i) {
    var cfg = window.CAT_CONFIG[e.category] || { icon: '\ud83d\udccb', label: e.category };
    var pcfg = window.PLAY_CONFIG[e.playability] || { icon: '\u2705', label: 'Unknown', color: '#888' };
    return '<article class="card" onclick="openDetail(\'' + e.id + '\')" tabindex="0" role="button" aria-label="View ' + e.title.replace(/'/g, '&#39;') + '" style="animation-delay:' + Math.min(i, 5) * 0.05 + 's">' +
      '<div class="card__thumb">' +
        '<img src="svgs/thumbnails/' + e.id + '.svg" alt="" class="card__thumb-img" loading="lazy" />' +
      '</div>' +
      '<div class="card__header">' +
        '<div class="card__icon card__icon--' + e.category + '">' + cfg.icon + '</div>' +
        '<div class="card__meta">' +
          '<span class="card__badge badge--' + e.difficulty + '">' + e.difficulty + '</span>' +
          '<span class="card__badge card__badge--play" style="color:' + pcfg.color + '">' + pcfg.icon + '</span>' +
        '</div>' +
      '</div>' +
      '<h3 class="card__title">' + e.title + '</h3>' +
      '<p class="card__desc">' + e.modern_explanation + '</p>' +
      '<div class="card__footer">' +
        '<span class="card__source">' + (e.source_book.length > 30 ? e.source_book.substring(0, 28) + '\u2026' : e.source_book) + ' (' + e.source_year + ')</span>' +
        '<span class="card__footer-right">' +
          (e.play_duration ? '<span class="card__duration">\u23f1 ' + e.play_duration + '</span>' : '') +
          (e.players ? '<span class="card__players"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg> ' + e.players + '</span>' : '') +
        '</span>' +
      '</div>' +
    '</article>';
  }).join('');

  var wrap = document.getElementById('load-more-wrap');
  if (window.visibleCount < items.length) {
    wrap.style.display = 'block';
    document.getElementById('load-more-btn').textContent = 'Show More (' + (items.length - window.visibleCount) + ' remaining)';
  } else {
    wrap.style.display = 'none';
  }
};

})();
