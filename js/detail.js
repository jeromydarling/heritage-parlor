// Heritage Parlor — Detail View
(function() {
'use strict';

window.openDetail = function(id) {
  var e = window.ENTRIES.find(function(x) { return x.id === id; });
  if (!e) return;
  var cfg = window.CAT_CONFIG[e.category] || { icon: '\ud83d\udccb', label: e.category };
  var pcfg = window.PLAY_CONFIG[e.playability] || { icon: '\u2705', label: 'Unknown', color: '#888' };

  var panel = document.getElementById('detail-panel');

  // Build sourcing section
  var sourcingHtml = '';
  if (e.sourcing) {
    var s = e.sourcing;
    var links = '';
    if (s.buy_links && s.buy_links.length) {
      links += '<div class="detail__sourcing-group"><strong>Where to Buy</strong><ul>';
      s.buy_links.forEach(function(l) {
        links += '<li><a href="' + l.url + '" target="_blank" rel="noopener">' + l.name + '</a>' + (l.price_range ? ' \u2014 ' + l.price_range : '') + '</li>';
      });
      links += '</ul></div>';
    }
    if (s.build_links && s.build_links.length) {
      links += '<div class="detail__sourcing-group"><strong>How to Build</strong><ul>';
      s.build_links.forEach(function(l) {
        links += '<li><a href="' + l.url + '" target="_blank" rel="noopener">' + l.name + '</a></li>';
      });
      links += '</ul></div>';
    }
    if (s.notes) {
      links += '<p class="detail__sourcing-note">' + s.notes + '</p>';
    }
    if (links) {
      sourcingHtml = '<div class="detail__section detail__section--sourcing">' +
        '<h3 class="detail__section-title">\ud83d\uded2 Where to Find It</h3>' +
        links +
      '</div>';
    }
  }

  panel.innerHTML =
    '<div class="detail__top-bar">' +
      '<span class="detail__category" style="color:var(--color-cat-' + e.category.split('-')[0] + ')">' + cfg.icon + ' ' + cfg.label + '</span>' +
      '<button class="detail__close" onclick="closeDetail()" aria-label="Close">' +
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>' +
      '</button>' +
    '</div>' +
    '<div class="detail__body">' +
      '<h2 class="detail__title">' + e.title + '</h2>' +
      '<div class="detail__meta-row">' +
        '<span class="detail__meta-chip badge--' + e.difficulty + '">' + e.difficulty + '</span>' +
        (e.players ? '<span class="detail__meta-chip">\ud83d\udc65 ' + e.players + '</span>' : '') +
        '<span class="detail__meta-chip">\ud83d\udcd6 ' + e.source_year + '</span>' +
        (e.family_friendly ? '<span class="detail__meta-chip">\ud83d\udc68\u200d\ud83d\udc69\u200d\ud83d\udc67\u200d\ud83d\udc66 Family Friendly</span>' : '<span class="detail__meta-chip" style="color:#ef4444">\u26a0\ufe0f Adult Supervision</span>') +
        '<span class="detail__meta-chip" style="color:' + pcfg.color + '">' + pcfg.icon + ' ' + pcfg.label + '</span>' +
        (e.play_duration ? '<span class="detail__meta-chip">\u23f1 ' + e.play_duration + '</span>' : '') +
      '</div>' +
      '<div class="detail__actions">' +
        '<button class="detail__print-btn" onclick="printGame(\'' + e.id + '\')" title="Print this game">' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>' +
          ' Print Game' +
        '</button>' +
      '</div>' +

      (e.playability === 'extinct_equipment' ?
        '<div class="detail__warning">' +
          '<span>\ud83c\udfdb\ufe0f</span>' +
          '<div><strong>Extinct Equipment:</strong> ' + (e.playability_note || 'This game requires equipment that is no longer manufactured.') + '</div>' +
        '</div>'
      : '') +

      (e.playability === 'dangerous' ?
        '<div class="detail__warning detail__warning--danger">' +
          '<span>\u26a0\ufe0f</span>' +
          '<div><strong>Safety Warning:</strong> ' + (e.playability_note || 'This activity involves hazardous materials or fire. Do not attempt without proper safety equipment and expertise.') + '</div>' +
        '</div>'
      : '') +

      (e.equipment_needed && e.equipment_needed.length ?
        '<div class="detail__section">' +
          '<h3 class="detail__section-title">What You Need</h3>' +
          '<p>' + e.equipment_needed.join(', ') + '</p>' +
        '</div>'
      :
        '<div class="detail__section">' +
          '<h3 class="detail__section-title">What You Need</h3>' +
          '<p>Nothing \u2014 just willing players!</p>' +
        '</div>'
      ) +

      '<div class="detail__section">' +
        '<h3 class="detail__section-title">How to Play</h3>' +
        '<p>' + e.modern_explanation + '</p>' +
      '</div>' +

      '<div class="detail__section">' +
        '<h3 class="detail__section-title">Original Description</h3>' +
        '<div class="detail__original">' + e.original_description + '</div>' +
      '</div>' +

      (e.fun_fact ?
        '<div class="detail__fun-fact">' +
          '<span>\ud83d\udca1</span>' +
          '<div>' + e.fun_fact + '</div>' +
        '</div>'
      : '') +

      sourcingHtml +

      (e.build_guide && e.build_guide.available ?
        '<div class="detail__section detail__section--build">' +
          '<h3 class="detail__section-title">\ud83d\udd28 Build This Game</h3>' +
          '<p class="detail__build-intro">This game can be built as a family project or commissioned as a custom artisan piece.</p>' +
          '<div class="detail__build-buttons">' +
            '<a class="detail__build-btn detail__build-btn--family" href="' + e.build_guide.heritage_skills_url + '" target="_blank" rel="noopener">' +
              '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>' +
              ' Build It \u2014 Family Project' +
            '</a>' +
            (e.build_guide.fabrica ?
              '<button class="detail__build-btn detail__build-btn--commission" onclick="openCommission(\'' + e.id + '\')">' +
                '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>' +
                ' Commission a Custom Build' +
                '<span class="detail__build-price">' + (e.build_guide.fabrica.price_range || '') + '</span>' +
              '</button>'
            : '') +
          '</div>' +
          (e.build_guide.fabrica ?
            '<div class="detail__commission-preview">' +
              '<span class="detail__commission-tag">' + (e.build_guide.fabrica.complexity || '') + '</span>' +
              '<span class="detail__commission-materials">' + (e.build_guide.fabrica.materials ? e.build_guide.fabrica.materials.substring(0, 100) + (e.build_guide.fabrica.materials.length > 100 ? '\u2026' : '') : '') + '</span>' +
            '</div>'
          : '') +
        '</div>'
      : '') +

      (e.tags && e.tags.length ?
        '<div class="detail__section" style="margin-top:var(--space-6)">' +
          '<h3 class="detail__section-title">Tags</h3>' +
          '<div class="detail__tags">' +
            e.tags.map(function(t) { return '<span class="detail__tag">' + t + '</span>'; }).join('') +
          '</div>' +
        '</div>'
      : '') +

      '<div class="detail__suggestion">' +
        '<div class="detail__suggestion-header">' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>' +
          '<h3 class="detail__section-title" style="margin:0">Share Your Knowledge</h3>' +
        '</div>' +
        '<p class="detail__suggestion-desc">Know a variation, correction, or tip for <em>' + e.title + '</em>? We\'d love to hear from you.</p>' +
        '<a class="detail__suggestion-btn" href="mailto:jeromy.darling@gmail.com?subject=' + encodeURIComponent('Heritage Parlor suggestion: ' + e.title) + '&body=' + encodeURIComponent('Game: ' + e.title + '\n\nMy suggestion:\n\n') + '">' +
          '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>' +
          ' Send a Suggestion' +
        '</a>' +
      '</div>' +

      '<a class="detail__source-link" href="' + e.source_url + '" target="_blank" rel="noopener noreferrer">' +
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>' +
        ' Read source: ' + e.source_book + ' (' + e.source_year + ')' +
      '</a>' +
    '</div>';

  var overlay = document.getElementById('detail-overlay');
  overlay.classList.add('detail-overlay--open');
  document.body.style.overflow = 'hidden';

  panel.querySelector('.detail__close').focus();
};

window.closeDetail = function() {
  var overlay = document.getElementById('detail-overlay');
  overlay.classList.remove('detail-overlay--open');
  document.body.style.overflow = '';
};

})();
