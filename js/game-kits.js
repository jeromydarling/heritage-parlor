// Heritage Parlor — Printable Game Kits (Lulu Integration Front-End)
(function() {
'use strict';

var PRE_BUILT_KITS = [
  {
    id: 'rainy-day',
    title: 'Rainy Day Kit',
    icon: '\ud83c\udf27\ufe0f',
    description: '10 indoor parlor games perfect for when you\'re stuck inside.',
    filter: function(e) { return e.category === 'parlor-game' && e.playability === 'playable_now'; },
    count: 10
  },
  {
    id: 'restaurant',
    title: 'Restaurant Kit',
    icon: '\ud83c\udf7d\ufe0f',
    description: '8 no-equipment games for waiting at restaurants.',
    filter: function(e) {
      return (e.playability === 'playable_now') &&
        (!e.equipment_needed || e.equipment_needed.length === 0 || (e.equipment_needed.length === 1 && e.equipment_needed[0].toLowerCase().indexOf('none') !== -1));
    },
    count: 8
  },
  {
    id: 'road-trip',
    title: 'Road Trip Kit',
    icon: '\ud83d\ude97',
    description: '10 word and guessing games for the car.',
    filter: function(e) { return (e.category === 'word-game' || e.subcategory === 'guessing-game') && e.playability === 'playable_now'; },
    count: 10
  },
  {
    id: 'holiday-party',
    title: 'Holiday Party Kit',
    icon: '\ud83c\udf84',
    description: '12 group parlor games for holiday gatherings.',
    filter: function(e) { return e.category === 'parlor-game' && e.players && (e.players.indexOf('+') !== -1 || e.players.indexOf('6') !== -1 || e.players.indexOf('8') !== -1 || e.players.indexOf('10') !== -1); },
    count: 12
  },
  {
    id: 'brain-teaser',
    title: 'Brain Teaser Kit',
    icon: '\ud83e\udde0',
    description: '10 puzzles and brain-teasers to challenge your mind.',
    filter: function(e) { return e.category === 'puzzle' && e.playability === 'playable_now'; },
    count: 10
  }
];

var customKitGames = new Set();

window.openGameKits = function() {
  var modal = document.getElementById('kits-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'kits-modal';
    modal.className = 'picker-overlay';
    modal.addEventListener('click', function(evt) { if (evt.target === modal) closeGameKits(); });
    document.body.appendChild(modal);
  }
  renderKitsUI(modal);
  modal.classList.add('picker-overlay--open');
  document.body.style.overflow = 'hidden';
};

window.closeGameKits = function() {
  var modal = document.getElementById('kits-modal');
  if (modal) { modal.classList.remove('picker-overlay--open'); document.body.style.overflow = ''; }
};

function renderKitsUI(modal) {
  var html =
    '<div class="picker-panel kits-panel">' +
      '<button class="picker-panel__close" onclick="closeGameKits()" aria-label="Close">' +
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>' +
      '</button>' +
      '<div class="picker-panel__header">' +
        '<h2 class="picker-panel__title">\ud83d\udcda Printable Game Kits</h2>' +
        '<p class="picker-panel__subtitle">Curated bundles of games, printed as saddle-stitch booklets and shipped to your door.</p>' +
      '</div>' +
      '<div class="kits__grid">';

  PRE_BUILT_KITS.forEach(function(kit) {
    html +=
      '<div class="kits__card" onclick="previewKit(\'' + kit.id + '\')">' +
        '<div class="kits__card-icon">' + kit.icon + '</div>' +
        '<h3 class="kits__card-title">' + kit.title + '</h3>' +
        '<p class="kits__card-desc">' + kit.description + '</p>' +
        '<span class="kits__card-count">' + kit.count + ' games</span>' +
      '</div>';
  });

  html +=
      '<div class="kits__card kits__card--custom" onclick="showCustomKitBuilder()">' +
        '<div class="kits__card-icon">\u2702\ufe0f</div>' +
        '<h3 class="kits__card-title">Custom Kit</h3>' +
        '<p class="kits__card-desc">Pick your own games to create a personalized booklet.</p>' +
        '<span class="kits__card-count">You choose</span>' +
      '</div>';

  html +=
      '</div>' +
      '<div id="kit-preview" style="display:none;"></div>' +
      '<div id="kit-builder" style="display:none;"></div>' +
    '</div>';

  modal.innerHTML = html;
}

window.previewKit = function(kitId) {
  var kit = PRE_BUILT_KITS.find(function(k) { return k.id === kitId; });
  if (!kit) return;

  var games = window.ENTRIES.filter(kit.filter).slice(0, kit.count);
  var preview = document.getElementById('kit-preview');
  if (!preview) return;

  var html =
    '<div class="kits__preview">' +
      '<div class="kits__preview-header">' +
        '<button class="kits__back-btn" onclick="hideKitPreview()">\u2190 Back to Kits</button>' +
        '<h3>' + kit.icon + ' ' + kit.title + '</h3>' +
        '<p>' + games.length + ' games \u00b7 ' + (games.length * 2) + ' pages</p>' +
      '</div>' +
      '<div class="kits__preview-list">';

  games.forEach(function(g) {
    var cfg = window.CAT_CONFIG[g.category] || { icon: '', label: '' };
    html +=
      '<div class="kits__preview-item">' +
        '<img src="svgs/thumbnails/' + g.id + '.svg" alt="" class="kits__preview-thumb" loading="lazy" />' +
        '<div class="kits__preview-info">' +
          '<div class="kits__preview-title">' + cfg.icon + ' ' + g.title + '</div>' +
          '<div class="kits__preview-meta">' +
            (g.players ? g.players + ' players' : '') +
            (g.play_duration ? ' \u00b7 ' + g.play_duration : '') +
          '</div>' +
        '</div>' +
      '</div>';
  });

  html +=
      '</div>' +
      '<div class="kits__preview-actions">' +
        '<button class="kits__order-btn" onclick="orderKit(\'' + kitId + '\')">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>' +
          ' Order Printed Booklet' +
        '</button>' +
        '<button class="kits__download-btn" onclick="downloadKit(\'' + kitId + '\')">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>' +
          ' Download PDF (Free)' +
        '</button>' +
      '</div>' +
    '</div>';

  preview.innerHTML = html;
  preview.style.display = 'block';
  document.querySelector('.kits__grid').style.display = 'none';
};

window.hideKitPreview = function() {
  var preview = document.getElementById('kit-preview');
  if (preview) preview.style.display = 'none';
  var builder = document.getElementById('kit-builder');
  if (builder) builder.style.display = 'none';
  var grid = document.querySelector('.kits__grid');
  if (grid) grid.style.display = '';
};

window.showCustomKitBuilder = function() {
  customKitGames = new Set();
  var builder = document.getElementById('kit-builder');
  if (!builder) return;

  var entries = window.ENTRIES.filter(function(e) {
    return e.playability !== 'dangerous' && e.playability !== 'extinct_equipment';
  });

  var html =
    '<div class="kits__builder">' +
      '<div class="kits__preview-header">' +
        '<button class="kits__back-btn" onclick="hideKitPreview()">\u2190 Back to Kits</button>' +
        '<h3>\u2702\ufe0f Custom Kit</h3>' +
        '<p>Select 4\u201324 games for your custom booklet.</p>' +
      '</div>' +
      '<div class="kits__builder-search">' +
        '<input type="text" id="kit-search" placeholder="Search games\u2026" />' +
        '<span id="kit-selected-count">0 selected</span>' +
      '</div>' +
      '<div class="kits__builder-list" id="kit-game-list">';

  entries.forEach(function(g) {
    var cfg = window.CAT_CONFIG[g.category] || { icon: '', label: '' };
    html +=
      '<label class="kits__builder-item" data-title="' + g.title.toLowerCase() + '">' +
        '<input type="checkbox" value="' + g.id + '" onchange="toggleKitGame(this)" />' +
        '<span class="kits__builder-check"></span>' +
        '<span class="kits__builder-icon">' + cfg.icon + '</span>' +
        '<span class="kits__builder-name">' + g.title + '</span>' +
        '<span class="kits__builder-cat">' + cfg.label + '</span>' +
      '</label>';
  });

  html +=
      '</div>' +
      '<div class="kits__preview-actions">' +
        '<button class="kits__order-btn" id="custom-kit-order" disabled onclick="orderCustomKit()">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>' +
          ' Order Printed Booklet' +
        '</button>' +
        '<button class="kits__download-btn" id="custom-kit-download" disabled onclick="downloadCustomKit()">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>' +
          ' Download PDF (Free)' +
        '</button>' +
      '</div>' +
    '</div>';

  builder.innerHTML = html;
  builder.style.display = 'block';
  document.querySelector('.kits__grid').style.display = 'none';

  document.getElementById('kit-search').addEventListener('input', function() {
    var q = this.value.toLowerCase();
    document.querySelectorAll('.kits__builder-item').forEach(function(item) {
      item.style.display = item.dataset.title.indexOf(q) !== -1 ? '' : 'none';
    });
  });
};

window.toggleKitGame = function(checkbox) {
  if (checkbox.checked) customKitGames.add(checkbox.value);
  else customKitGames.delete(checkbox.value);
  var count = customKitGames.size;
  document.getElementById('kit-selected-count').textContent = count + ' selected';
  var valid = count >= 4 && count <= 24;
  document.getElementById('custom-kit-order').disabled = !valid;
  document.getElementById('custom-kit-download').disabled = !valid;
};

window.orderKit = function(kitId) {
  var kit = PRE_BUILT_KITS.find(function(k) { return k.id === kitId; });
  if (!kit) return;
  var games = window.ENTRIES.filter(kit.filter).slice(0, kit.count);
  showOrderConfirmation(kit.title, games.map(function(g) { return g.id; }));
};

window.orderCustomKit = function() {
  showOrderConfirmation('Custom Kit', Array.from(customKitGames));
};

window.downloadKit = function(kitId) {
  var kit = PRE_BUILT_KITS.find(function(k) { return k.id === kitId; });
  if (!kit) return;
  var games = window.ENTRIES.filter(kit.filter).slice(0, kit.count);
  printMultipleGames(games.map(function(g) { return g.id; }), kit.title);
};

window.downloadCustomKit = function() {
  printMultipleGames(Array.from(customKitGames), 'Custom Kit');
};

function printMultipleGames(gameIds, title) {
  var w = window.open('', '_blank');
  if (!w) {
    var toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = 'Please allow pop-ups to download the kit.';
    document.body.appendChild(toast);
    setTimeout(function() { toast.classList.add('toast--visible'); }, 10);
    setTimeout(function() { toast.classList.remove('toast--visible'); setTimeout(function() { toast.remove(); }, 300); }, 4000);
    return;
  }

  var base = location.href.replace(/\/[^/]*$/, '/');
  var games = gameIds.map(function(id) {
    return window.ENTRIES.find(function(e) { return e.id === id; });
  }).filter(Boolean);

  var totalPages = 2 + 1 + (games.length * 2) + 1; // cover + toc + game pages + back
  var currentPage = 0;

  // ── Victorian ornament SVGs ──
  var ornamentLine = '<svg viewBox="0 0 400 20" width="300" height="15" style="display:block;margin:0 auto;" xmlns="http://www.w3.org/2000/svg">' +
    '<line x1="0" y1="10" x2="170" y2="10" stroke="#8b4513" stroke-width="0.75" opacity="0.4"/>' +
    '<circle cx="180" cy="10" r="2" fill="#8b4513" opacity="0.5"/>' +
    '<circle cx="200" cy="10" r="3.5" fill="none" stroke="#8b4513" stroke-width="1" opacity="0.5"/>' +
    '<circle cx="220" cy="10" r="2" fill="#8b4513" opacity="0.5"/>' +
    '<line x1="230" y1="10" x2="400" y2="10" stroke="#8b4513" stroke-width="0.75" opacity="0.4"/>' +
  '</svg>';

  var cornerOrnament = function(pos) {
    var transforms = {
      tl: 'translate(40,40)',
      tr: 'translate(576,40) scale(-1,1)',
      bl: 'translate(40,732) scale(1,-1)',
      br: 'translate(576,732) scale(-1,-1)'
    };
    return '<g transform="' + transforms[pos] + '">' +
      '<path d="M0,0 Q15,-5 30,0 Q25,15 30,30" fill="none" stroke="#8b4513" stroke-width="1.2" opacity="0.3"/>' +
      '<circle cx="0" cy="0" r="2.5" fill="#8b4513" opacity="0.25"/>' +
      '<path d="M5,5 L20,5 M5,5 L5,20" stroke="#8b4513" stroke-width="0.5" opacity="0.2"/>' +
    '</g>';
  };

  var borderFrame = '<svg viewBox="0 0 616 792" width="100%" height="100%" style="position:absolute;top:0;left:0;" xmlns="http://www.w3.org/2000/svg">' +
    '<rect x="30" y="30" width="556" height="732" rx="3" fill="none" stroke="#8b4513" stroke-width="1.5" opacity="0.15"/>' +
    '<rect x="36" y="36" width="544" height="720" rx="2" fill="none" stroke="#8b4513" stroke-width="0.5" opacity="0.1"/>' +
    cornerOrnament('tl') + cornerOrnament('tr') + cornerOrnament('bl') + cornerOrnament('br') +
  '</svg>';

  // ── Shared page CSS ──
  var css =
    '@import url("https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..700;1,400..700&family=Source+Sans+3:wght@300..600&display=swap");' +
    '@page { size: letter; margin: 0; }' +
    '*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }' +
    '@media print { body { margin: 0; } .page { page-break-after: always; } .page:last-child { page-break-after: auto; } .no-print { display: none !important; } }' +
    'body { margin: 0; padding: 0; background: #fff; }' +
    '.page { width: 8.5in; height: 11in; position: relative; overflow: hidden; background: #faf6f0; }' +

    /* Cover page */
    '.cover { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 1.5in; }' +
    '.cover__ornament-top { margin-bottom: 0.4in; }' +
    '.cover__brand { font: 300 11px "Source Sans 3", sans-serif; letter-spacing: 6px; text-transform: uppercase; color: #8b4513; margin-bottom: 0.3in; }' +
    '.cover__title { font: 700 42px/1.1 "Playfair Display", Georgia, serif; color: #1a1a1a; margin-bottom: 0.15in; letter-spacing: 1px; }' +
    '.cover__subtitle { font: 300 16px/1.5 "Source Sans 3", sans-serif; color: #555; margin-bottom: 0.5in; max-width: 4in; }' +
    '.cover__meta { font: 400 13px "Source Sans 3", sans-serif; color: #8b4513; letter-spacing: 1px; }' +
    '.cover__ornament-bottom { margin-top: 0.5in; }' +
    '.cover__footer { position: absolute; bottom: 0.8in; left: 0; right: 0; text-align: center; font: 300 10px "Source Sans 3", sans-serif; color: #999; letter-spacing: 2px; }' +

    /* Table of contents */
    '.toc { padding: 1in 1.2in; }' +
    '.toc__heading { font: 700 28px "Playfair Display", Georgia, serif; color: #1a1a1a; text-align: center; margin-bottom: 0.12in; letter-spacing: 1px; }' +
    '.toc__sub { font: 300 12px "Source Sans 3", sans-serif; color: #555; text-align: center; margin-bottom: 0.5in; }' +
    '.toc__list { list-style: none; }' +
    '.toc__item { display: flex; align-items: baseline; padding: 7px 0; border-bottom: 1px dotted #d4c5a9; }' +
    '.toc__num { font: 400 11px "Source Sans 3", sans-serif; color: #8b4513; width: 28px; flex-shrink: 0; }' +
    '.toc__title { font: 600 13px "Playfair Display", Georgia, serif; color: #1a1a1a; flex: 1; }' +
    '.toc__cat { font: 400 10px "Source Sans 3", sans-serif; color: #888; margin-left: 8px; }' +
    '.toc__page { font: 400 11px "Source Sans 3", sans-serif; color: #8b4513; width: 28px; text-align: right; flex-shrink: 0; }' +

    /* Game pages wrapper */
    '.game-page { }' +
    '.game-page img { width: 100%; height: 100%; object-fit: contain; }' +

    /* Page number footer */
    '.page-num { position: absolute; bottom: 0.45in; left: 0; right: 0; text-align: center; font: 300 9px "Source Sans 3", sans-serif; color: #999; letter-spacing: 1px; }' +
    '.page-num span { background: #faf6f0; padding: 0 12px; position: relative; }' +
    '.page-num::before { content: ""; position: absolute; bottom: 4px; left: 1.2in; right: 1.2in; height: 0.5px; background: #d4c5a9; }' +

    /* Back cover */
    '.back { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 2in 1.5in; }' +
    '.back__brand { font: 700 24px "Playfair Display", Georgia, serif; color: #1a1a1a; margin-bottom: 0.15in; }' +
    '.back__tagline { font: italic 300 14px "Source Sans 3", sans-serif; color: #555; margin-bottom: 0.5in; max-width: 3.5in; line-height: 1.6; }' +
    '.back__url { font: 400 11px "Source Sans 3", sans-serif; color: #8b4513; letter-spacing: 2px; margin-bottom: 0.4in; }' +
    '.back__legal { font: 300 9px "Source Sans 3", sans-serif; color: #999; line-height: 1.6; max-width: 4in; }' +
    '.back__books { font: 300 9px/1.8 "Source Sans 3", sans-serif; color: #888; margin-top: 0.3in; max-width: 4.5in; }' +

    /* Toolbar */
    '.no-print { display: flex; align-items: center; justify-content: center; gap: 12px; padding: 14px; background: #f5f0e6; border-bottom: 1px solid #e8ddd0; font: 400 13px "Source Sans 3", Georgia, serif; color: #333; }' +
    '.no-print strong { font-family: "Playfair Display", Georgia, serif; }' +
    '.no-print button { font: 600 13px "Source Sans 3", sans-serif; background: #8b4513; color: #fff; border: none; padding: 8px 20px; border-radius: 6px; cursor: pointer; letter-spacing: 0.5px; }' +
    '.no-print button:hover { background: #6d360f; }';

  // ── Build pages ──
  var html = '';

  // Cover page
  currentPage++;
  html +=
    '<div class="page cover">' +
      borderFrame +
      '<div class="cover__ornament-top">' + ornamentLine + '</div>' +
      '<div class="cover__brand">HERITAGE PARLOR</div>' +
      '<div class="cover__title">' + title + '</div>' +
      '<div class="cover__subtitle">' + games.length + ' Victorian-era games, tricks &amp; puzzles curated from public domain books published between 1857 and 1917.</div>' +
      '<div class="cover__ornament-bottom">' + ornamentLine + '</div>' +
      '<div class="cover__meta">' + games.length + ' Games &middot; ' + (games.length * 2) + ' Pages</div>' +
      '<div class="cover__footer">ALL PUBLIC DOMAIN &middot; FREE FOREVER</div>' +
    '</div>';

  // Table of contents
  currentPage++;
  var tocItems = '';
  games.forEach(function(game, idx) {
    var cfg = window.CAT_CONFIG[game.category] || { label: '' };
    var gamePage = 3 + (idx * 2); // cover + toc + game pages
    tocItems +=
      '<li class="toc__item">' +
        '<span class="toc__num">' + (idx + 1) + '.</span>' +
        '<span class="toc__title">' + game.title + '</span>' +
        '<span class="toc__cat">' + cfg.label + '</span>' +
        '<span class="toc__page">' + gamePage + '</span>' +
      '</li>';
  });

  html +=
    '<div class="page toc">' +
      borderFrame +
      '<div class="toc__heading">Contents</div>' +
      '<div class="toc__sub">' + games.length + ' games in this collection</div>' +
      '<div style="margin-bottom:16px;">' + ornamentLine + '</div>' +
      '<ol class="toc__list">' + tocItems + '</ol>' +
      '<div class="page-num"><span>' + currentPage + '</span></div>' +
    '</div>';

  // Game pages
  games.forEach(function(game, idx) {
    // Page 1 — game board / diagram
    currentPage++;
    html +=
      '<div class="page game-page">' +
        '<img src="svgs/page1/' + game.id + '.svg" alt="' + game.title + ' \u2014 Game Board" />' +
        '<div class="page-num"><span>' + currentPage + '</span></div>' +
      '</div>';

    // Page 2 — instructions
    currentPage++;
    html +=
      '<div class="page game-page">' +
        '<img src="svgs/page2/' + game.id + '.svg" alt="' + game.title + ' \u2014 Instructions" />' +
        '<div class="page-num"><span>' + currentPage + '</span></div>' +
      '</div>';
  });

  // Back cover
  currentPage++;
  // Collect unique source books
  var sourceBooks = {};
  games.forEach(function(g) { sourceBooks[g.source_book + ' (' + g.source_year + ')'] = true; });
  var bookList = Object.keys(sourceBooks).sort().join(' &middot; ');

  html +=
    '<div class="page back">' +
      borderFrame +
      '<div style="margin-bottom:0.4in;">' + ornamentLine + '</div>' +
      '<div class="back__brand">Heritage Parlor</div>' +
      '<div class="back__tagline">502 parlor games, magic tricks, puzzles &amp; amusements from thirteen classic Victorian-era books \u2014 all in the public domain and free forever.</div>' +
      '<div class="back__url">HERITAGEPARLOR.COM</div>' +
      '<div style="margin-bottom:0.4in;">' + ornamentLine + '</div>' +
      '<div class="back__legal">This collection is drawn entirely from public domain works. No copyright is claimed. Print, share, and enjoy freely.</div>' +
      '<div class="back__books">Sources: ' + bookList + '</div>' +
    '</div>';

  w.document.write('<!DOCTYPE html><html><head>' +
    '<base href="' + base + '">' +
    '<meta charset="UTF-8">' +
    '<title>' + title + ' \u2014 Heritage Parlor</title>' +
    '<style>' + css + '</style>' +
    '</head><body>' +
    '<div class="no-print"><strong>' + title + '</strong> &mdash; ' + games.length + ' games, ' + currentPage + ' pages ' +
    '<button onclick="window.print()">Print Booklet</button>' +
    '<button onclick="window.close()">Close</button></div>' +
    html +
    '</body></html>');
  w.document.close();
}

function showOrderConfirmation(kitTitle, gameIds) {
  if (window.isSupabaseReady() && window.currentUser) {
    // Future: POST to Lulu API via Supabase Edge Function
    window.sb.from('lulu_orders').insert({
      user_id: window.currentUser.id,
      kit_type: kitTitle.toLowerCase().replace(/\s+/g, '_'),
      game_ids: gameIds,
      status: 'pending'
    }).then(function() {
      showKitConfirmation('Order placed! We\'ll email you when your booklet ships.');
    }).catch(function() {
      showKitConfirmation('Order could not be placed. Please try again later.');
    });
  } else {
    // Email fallback
    var subject = encodeURIComponent('Heritage Parlor Kit Order: ' + kitTitle);
    var body = encodeURIComponent(
      'Kit: ' + kitTitle + '\n' +
      'Games (' + gameIds.length + '):\n' +
      gameIds.join('\n') + '\n\n' +
      'Please send me information about ordering a printed booklet.'
    );
    window.open('mailto:' + window.FABRICA_CONFIG.email + '?subject=' + subject + '&body=' + body, '_self');
    showKitConfirmation('Your email client will open with the order details pre-filled.');
  }
}

function showKitConfirmation(message) {
  var preview = document.getElementById('kit-preview');
  var builder = document.getElementById('kit-builder');
  var target = (preview && preview.style.display !== 'none') ? preview : builder;
  if (!target) return;
  var actions = target.querySelector('.kits__preview-actions');
  if (actions) {
    actions.innerHTML = '<div class="kits__confirmation">\u2705 ' + message + '</div>';
  }
}

// Inject kits button into hero
document.addEventListener('data-loaded', function() {
  var heroContent = document.querySelector('.hero__content');
  if (!heroContent || document.getElementById('kits-hero-btn')) return;

  var btn = document.createElement('button');
  btn.id = 'kits-hero-btn';
  btn.className = 'picker-hero-btn kits-hero-btn';
  btn.innerHTML =
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>' +
    ' Order a Game Kit';
  btn.onclick = function() { window.openGameKits(); };

  var pickerBtn = document.getElementById('picker-hero-btn');
  if (pickerBtn) {
    pickerBtn.parentNode.insertBefore(btn, pickerBtn.nextSibling);
  } else {
    var desc = heroContent.querySelector('.hero__desc');
    if (desc) desc.parentNode.insertBefore(btn, desc.nextSibling);
  }
});

})();
