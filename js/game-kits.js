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
  var pages = '';
  gameIds.forEach(function(id) {
    pages +=
      '<div class="page"><img src="svgs/page1/' + id + '.svg" alt="' + id + ' — Game Board" /></div>' +
      '<div class="page"><img src="svgs/page2/' + id + '.svg" alt="' + id + ' — Instructions" /></div>';
  });
  w.document.write('<!DOCTYPE html><html><head>' +
    '<base href="' + base + '">' +
    '<title>' + title + ' — Heritage Parlor</title>' +
    '<style>' +
    '  @page { size: letter; margin: 0; }' +
    '  @media print { body { margin: 0; } .page { page-break-after: always; } .page:last-child { page-break-after: auto; } .no-print { display: none; } }' +
    '  body { margin: 0; padding: 0; background: #fff; font-family: Georgia, serif; }' +
    '  .page { width: 8.5in; height: 11in; display: flex; align-items: center; justify-content: center; overflow: hidden; }' +
    '  .page img { width: 100%; height: 100%; object-fit: contain; }' +
    '  .no-print { text-align: center; padding: 12px; background: #f5f0e6; border-bottom: 1px solid #ddd; }' +
    '  .no-print button { font: 600 14px Georgia, serif; background: #8b4513; color: #fff; border: none; padding: 8px 24px; border-radius: 6px; cursor: pointer; margin: 0 4px; }' +
    '</style></head><body>' +
    '<div class="no-print"><strong>' + title + '</strong> \u2014 ' + gameIds.length + ' games, ' + (gameIds.length * 2) + ' pages ' +
    '<button onclick="window.print()">\ud83d\udda8 Print</button></div>' +
    pages +
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
