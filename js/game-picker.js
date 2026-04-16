// Heritage Parlor — Tonight's Game Picker
(function() {
'use strict';

var pickerState = {
  players: null,
  maxDuration: null,
  categories: [],
  difficulty: 'all',
  mode: 'single'
};

window.openGamePicker = function() {
  var modal = document.getElementById('picker-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'picker-modal';
    modal.className = 'picker-overlay';
    modal.addEventListener('click', function(evt) { if (evt.target === modal) closeGamePicker(); });
    document.body.appendChild(modal);
  }
  renderPickerUI(modal);
  modal.classList.add('picker-overlay--open');
  document.body.style.overflow = 'hidden';
};

window.closeGamePicker = function() {
  var modal = document.getElementById('picker-modal');
  if (modal) { modal.classList.remove('picker-overlay--open'); document.body.style.overflow = ''; }
};

function renderPickerUI(modal) {
  var cats = Object.keys(window.CAT_CONFIG);

  modal.innerHTML =
    '<div class="picker-panel">' +
      '<button class="picker-panel__close" onclick="closeGamePicker()" aria-label="Close">' +
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>' +
      '</button>' +
      '<div class="picker-panel__header">' +
        '<h2 class="picker-panel__title">Tonight\'s Game</h2>' +
        '<p class="picker-panel__subtitle">Tell us about your group and we\'ll find the perfect game.</p>' +
      '</div>' +
      '<div class="picker-panel__filters">' +
        '<div class="picker-panel__field">' +
          '<label>How many players?</label>' +
          '<input type="number" id="picker-players" min="1" max="100" placeholder="e.g. 4">' +
        '</div>' +
        '<div class="picker-panel__field">' +
          '<label>Max duration (minutes)</label>' +
          '<input type="number" id="picker-duration" min="5" max="300" placeholder="e.g. 30">' +
        '</div>' +
        '<div class="picker-panel__field">' +
          '<label>Difficulty</label>' +
          '<select id="picker-difficulty">' +
            '<option value="all">Any</option>' +
            '<option value="beginner">Beginner</option>' +
            '<option value="intermediate">Intermediate</option>' +
            '<option value="advanced">Advanced</option>' +
          '</select>' +
        '</div>' +
        '<div class="picker-panel__field">' +
          '<label>Categories</label>' +
          '<div class="picker-panel__cats" id="picker-cats">' +
            cats.map(function(cat) {
              var cfg = window.CAT_CONFIG[cat];
              return '<label class="picker-panel__cat-check"><input type="checkbox" value="' + cat + '" checked> ' + cfg.icon + ' ' + cfg.label + '</label>';
            }).join('') +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div class="picker-panel__modes">' +
        '<button class="picker-panel__mode picker-panel__mode--active" id="mode-single" onclick="setPickerMode(\'single\')">Single Game</button>' +
        '<button class="picker-panel__mode" id="mode-evening" onclick="setPickerMode(\'evening\')">Plan an Evening</button>' +
      '</div>' +
      '<button class="picker-panel__go" onclick="pickGame()">' +
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>' +
        ' Pick a Game!' +
      '</button>' +
      '<div class="picker-panel__result" id="picker-result"></div>' +
    '</div>';
}

window.setPickerMode = function(mode) {
  pickerState.mode = mode;
  document.getElementById('mode-single').classList.toggle('picker-panel__mode--active', mode === 'single');
  document.getElementById('mode-evening').classList.toggle('picker-panel__mode--active', mode === 'evening');
};

window.pickGame = function() {
  var players = parseInt(document.getElementById('picker-players').value) || null;
  var maxDuration = parseInt(document.getElementById('picker-duration').value) || null;
  var difficulty = document.getElementById('picker-difficulty').value;

  var checkedCats = [];
  document.querySelectorAll('#picker-cats input:checked').forEach(function(cb) {
    checkedCats.push(cb.value);
  });

  // Get recently played game IDs to exclude
  var recentlyPlayed = {};
  try {
    var log = JSON.parse(localStorage.getItem('hp_game_log') || '[]');
    var twoWeeksAgo = Date.now() - (14 * 24 * 60 * 60 * 1000);
    log.forEach(function(entry) {
      if (entry.played_at && new Date(entry.played_at).getTime() > twoWeeksAgo) {
        recentlyPlayed[entry.game_id] = true;
      }
    });
  } catch(e) {}

  // Get favorite categories for weighting
  var favCats = [];
  try { favCats = JSON.parse(localStorage.getItem('hp_fav_cats') || '[]'); } catch(e) {}
  if (window.currentProfile && window.currentProfile.favorite_categories) {
    favCats = window.currentProfile.favorite_categories;
  }

  // Filter entries
  var pool = window.ENTRIES.filter(function(e) {
    if (checkedCats.length && checkedCats.indexOf(e.category) === -1) return false;
    if (difficulty !== 'all' && e.difficulty !== difficulty) return false;
    if (e.playability === 'dangerous' || e.playability === 'extinct_equipment') return false;
    return true;
  });

  // Exclude recently played (but keep them if pool would be too small)
  var freshPool = pool.filter(function(e) { return !recentlyPlayed[e.id]; });
  if (freshPool.length >= 4) pool = freshPool;

  if (pool.length === 0) {
    document.getElementById('picker-result').innerHTML =
      '<div class="picker-result__empty">No games match those filters. Try widening your search!</div>';
    return;
  }

  // Weight: playable_now > easy_to_source > craftable > specialty_needed
  // Boost favorite categories
  var weights = { playable_now: 4, easy_to_source: 3, craftable: 2, specialty_needed: 1 };
  var weighted = [];
  pool.forEach(function(e) {
    var w = weights[e.playability] || 1;
    if (favCats.length && favCats.indexOf(e.category) !== -1) w += 2;
    for (var i = 0; i < w; i++) weighted.push(e);
  });

  var resultEl = document.getElementById('picker-result');

  if (pickerState.mode === 'single') {
    var pick = weighted[Math.floor(Math.random() * weighted.length)];
    renderPickResult([pick], resultEl);
  } else {
    // Evening mode: mix one active/physical, one brain, one social/parlor, one wildcard
    var selected = [];
    var shuffled = weighted.sort(function() { return Math.random() - 0.5; });
    var target = Math.min(4, pool.length);

    var slots = [
      { label: 'active', cats: ['physical-game', 'folk-game'], picked: false },
      { label: 'brain', cats: ['puzzle', 'word-game', 'board-game', 'scientific-recreation'], picked: false },
      { label: 'social', cats: ['parlor-game', 'magic-trick', 'card-game'], picked: false }
    ];

    // First pass: fill each slot with a matching game
    slots.forEach(function(slot) {
      for (var i = 0; i < shuffled.length; i++) {
        var game = shuffled[i];
        if (slot.cats.indexOf(game.category) !== -1 && selected.indexOf(game) === -1) {
          selected.push(game);
          slot.picked = true;
          break;
        }
      }
    });

    // Second pass: fill remaining with any unique category
    var usedCategories = {};
    selected.forEach(function(g) { usedCategories[g.category] = true; });
    for (var i = 0; i < shuffled.length && selected.length < target; i++) {
      var game = shuffled[i];
      if (selected.indexOf(game) === -1 && !usedCategories[game.category]) {
        selected.push(game);
        usedCategories[game.category] = true;
      }
    }

    // Third pass: just fill if still short
    for (var j = 0; j < shuffled.length && selected.length < target; j++) {
      if (selected.indexOf(shuffled[j]) === -1) {
        selected.push(shuffled[j]);
      }
    }
    renderPickResult(selected, resultEl);
  }
};

function renderPickResult(games, container) {
  var html = '';
  if (games.length === 1) {
    html += '<div class="picker-result__reveal">';
  } else {
    html += '<div class="picker-result__evening"><h3>Your Evening Plan</h3>';
  }

  games.forEach(function(game, idx) {
    var cfg = window.CAT_CONFIG[game.category] || { icon: '', label: '' };
    var pcfg = window.PLAY_CONFIG[game.playability] || { icon: '', label: '', color: '#888' };
    html +=
      '<div class="picker-result__card" style="animation-delay:' + (idx * 0.15) + 's">' +
        '<div class="picker-result__card-thumb">' +
          '<img src="svgs/thumbnails/' + game.id + '.svg" alt="" loading="lazy" />' +
        '</div>' +
        '<div class="picker-result__card-info">' +
          '<div class="picker-result__card-cat" style="color:' + (pcfg.color || 'inherit') + '">' + cfg.icon + ' ' + cfg.label + '</div>' +
          '<h4 class="picker-result__card-title">' + game.title + '</h4>' +
          '<p class="picker-result__card-desc">' + (game.modern_explanation.length > 120 ? game.modern_explanation.substring(0, 120) + '\u2026' : game.modern_explanation) + '</p>' +
          '<div class="picker-result__card-meta">' +
            (game.players ? '<span>\ud83d\udc65 ' + game.players + '</span>' : '') +
            (game.play_duration ? '<span>\u23f1 ' + game.play_duration + '</span>' : '') +
            '<span>' + pcfg.icon + ' ' + pcfg.label + '</span>' +
          '</div>' +
        '</div>' +
        '<button class="picker-result__card-open" onclick="closeGamePicker(); openDetail(\'' + game.id + '\')">View Game</button>' +
      '</div>';
  });

  html += '</div>';
  html += '<button class="picker-panel__reroll" onclick="pickGame()">\ud83c\udfb2 Pick Again</button>';
  container.innerHTML = html;
}

// ─── Inject picker button into hero ───
document.addEventListener('data-loaded', function() {
  var heroContent = document.querySelector('.hero__content');
  if (!heroContent || document.getElementById('picker-hero-btn')) return;

  var btn = document.createElement('button');
  btn.id = 'picker-hero-btn';
  btn.className = 'picker-hero-btn';
  btn.innerHTML =
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>' +
    ' Pick Tonight\'s Game';
  btn.onclick = function() { window.openGamePicker(); };

  var desc = heroContent.querySelector('.hero__desc');
  if (desc) desc.parentNode.insertBefore(btn, desc.nextSibling);
});

})();
