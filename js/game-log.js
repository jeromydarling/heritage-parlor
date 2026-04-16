// Heritage Parlor — Game Log
(function() {
'use strict';

// Local cache of log entries (populated from Supabase or localStorage fallback)
var logEntries = [];

// ─── Load log entries ───
function loadLog() {
  if (window.isSupabaseReady() && window.currentUser) {
    window.sb.from('game_log').select('*')
      .eq('user_id', window.currentUser.id)
      .order('played_at', { ascending: false })
      .then(function(res) {
        logEntries = res.data || [];
        renderGameLogPage();
      });
  } else {
    // localStorage fallback for demo
    try { logEntries = JSON.parse(localStorage.getItem('hp_game_log') || '[]'); } catch(e) { logEntries = []; }
    renderGameLogPage();
  }
}

function saveLogEntry(entry) {
  if (window.isSupabaseReady() && window.currentUser) {
    return window.sb.from('game_log').insert({
      user_id: window.currentUser.id,
      game_id: entry.game_id,
      played_at: entry.played_at,
      rating: entry.rating,
      player_count: entry.player_count,
      duration_minutes: entry.duration_minutes,
      notes: entry.notes,
      would_play_again: entry.would_play_again
    }).then(function(res) {
      if (res.data) logEntries.unshift(res.data[0]);
      return res;
    });
  } else {
    // localStorage fallback
    entry.id = 'local_' + Date.now();
    entry.played_at = entry.played_at || new Date().toISOString();
    logEntries.unshift(entry);
    localStorage.setItem('hp_game_log', JSON.stringify(logEntries));
    return Promise.resolve({ data: [entry] });
  }
}

function deleteLogEntry(id) {
  if (window.isSupabaseReady() && window.currentUser) {
    return window.sb.from('game_log').delete().eq('id', id).then(function() {
      logEntries = logEntries.filter(function(e) { return e.id !== id; });
      renderGameLogPage();
    });
  } else {
    logEntries = logEntries.filter(function(e) { return e.id !== id; });
    localStorage.setItem('hp_game_log', JSON.stringify(logEntries));
    renderGameLogPage();
    return Promise.resolve();
  }
}

// ─── Inline log form in detail modal ───
window.showLogForm = function(gameId) {
  var container = document.getElementById('log-form-container');
  if (!container) return;

  var today = new Date().toISOString().split('T')[0];

  container.innerHTML =
    '<form class="log-form" id="log-form">' +
      '<h4 class="log-form__title">Log This Game</h4>' +
      '<div class="log-form__row">' +
        '<div class="log-form__field">' +
          '<label>Date</label>' +
          '<input type="date" id="log-date" value="' + today + '">' +
        '</div>' +
        '<div class="log-form__field">' +
          '<label>Players</label>' +
          '<input type="number" id="log-players" min="1" max="100" placeholder="4">' +
        '</div>' +
        '<div class="log-form__field">' +
          '<label>Duration (min)</label>' +
          '<input type="number" id="log-duration" min="1" max="999" placeholder="30">' +
        '</div>' +
      '</div>' +
      '<div class="log-form__field">' +
        '<label>Rating</label>' +
        '<div class="log-form__stars" id="log-stars">' +
          '<button type="button" class="log-form__star" data-rating="1">\u2606</button>' +
          '<button type="button" class="log-form__star" data-rating="2">\u2606</button>' +
          '<button type="button" class="log-form__star" data-rating="3">\u2606</button>' +
          '<button type="button" class="log-form__star" data-rating="4">\u2606</button>' +
          '<button type="button" class="log-form__star" data-rating="5">\u2606</button>' +
        '</div>' +
      '</div>' +
      '<div class="log-form__field">' +
        '<label>Notes</label>' +
        '<textarea id="log-notes" rows="2" placeholder="How was it?"></textarea>' +
      '</div>' +
      '<div class="log-form__field log-form__field--toggle">' +
        '<label>Would play again?</label>' +
        '<button type="button" class="log-form__toggle" id="log-again" data-value="true">' +
          '<span class="log-form__toggle-track"><span class="log-form__toggle-thumb"></span></span>' +
          ' Yes' +
        '</button>' +
      '</div>' +
      '<div class="log-form__actions">' +
        '<button type="submit" class="log-form__submit">Save to Log</button>' +
        '<button type="button" class="log-form__cancel" onclick="hideLogForm()">Cancel</button>' +
      '</div>' +
    '</form>';

  container.style.display = 'block';

  // Star rating interaction
  var selectedRating = 0;
  var stars = container.querySelectorAll('.log-form__star');
  stars.forEach(function(star) {
    star.addEventListener('click', function() {
      selectedRating = parseInt(this.dataset.rating);
      stars.forEach(function(s, i) {
        s.textContent = i < selectedRating ? '\u2605' : '\u2606';
        s.classList.toggle('log-form__star--active', i < selectedRating);
      });
    });
  });

  // Toggle interaction
  var toggleBtn = document.getElementById('log-again');
  toggleBtn.addEventListener('click', function() {
    var current = this.dataset.value === 'true';
    this.dataset.value = (!current).toString();
    this.classList.toggle('log-form__toggle--on', !current);
    this.querySelector('span:last-child') || null;
    // Update text
    var text = this.childNodes[this.childNodes.length - 1];
    text.textContent = !current ? ' Yes' : ' No';
  });
  toggleBtn.classList.add('log-form__toggle--on');

  // Form submission
  document.getElementById('log-form').addEventListener('submit', function(evt) {
    evt.preventDefault();
    var entry = {
      game_id: gameId,
      played_at: document.getElementById('log-date').value || today,
      rating: selectedRating || null,
      player_count: parseInt(document.getElementById('log-players').value) || null,
      duration_minutes: parseInt(document.getElementById('log-duration').value) || null,
      notes: document.getElementById('log-notes').value.trim() || null,
      would_play_again: document.getElementById('log-again').dataset.value === 'true'
    };

    saveLogEntry(entry).then(function() {
      container.innerHTML =
        '<div class="log-form__success">' +
          '<span>\u2705</span> Logged! <a href="#" onclick="navigateTo(\'game-log\'); closeDetail(); return false;">View Game Log</a>' +
        '</div>';
      setTimeout(function() { container.style.display = 'none'; }, 3000);
    });
  });
};

window.hideLogForm = function() {
  var container = document.getElementById('log-form-container');
  if (container) { container.style.display = 'none'; container.innerHTML = ''; }
};

// ─── Game Log Page ───
function renderGameLogPage() {
  var section = document.getElementById('game-log-section');
  if (!section) return;

  // Calculate stats
  var totalGames = logEntries.length;
  var totalMinutes = logEntries.reduce(function(sum, e) { return sum + (e.duration_minutes || 0); }, 0);
  var totalHours = Math.round(totalMinutes / 60 * 10) / 10;
  var avgRating = totalGames > 0
    ? (logEntries.reduce(function(sum, e) { return sum + (e.rating || 0); }, 0) / logEntries.filter(function(e) { return e.rating; }).length).toFixed(1)
    : '0';

  // Find most played game
  var gameCounts = {};
  logEntries.forEach(function(e) {
    gameCounts[e.game_id] = (gameCounts[e.game_id] || 0) + 1;
  });
  var mostPlayed = Object.keys(gameCounts).sort(function(a, b) { return gameCounts[b] - gameCounts[a]; })[0];
  var mostPlayedEntry = mostPlayed ? window.ENTRIES.find(function(e) { return e.id === mostPlayed; }) : null;

  var html =
    '<div class="container game-log">' +
      '<h2 class="game-log__heading">My Game Log</h2>' +
      '<div class="game-log__stats">' +
        '<div class="game-log__stat">' +
          '<div class="game-log__stat-value">' + totalGames + '</div>' +
          '<div class="game-log__stat-label">Games Played</div>' +
        '</div>' +
        '<div class="game-log__stat">' +
          '<div class="game-log__stat-value">' + totalHours + 'h</div>' +
          '<div class="game-log__stat-label">Total Time</div>' +
        '</div>' +
        '<div class="game-log__stat">' +
          '<div class="game-log__stat-value">' + avgRating + '</div>' +
          '<div class="game-log__stat-label">Avg Rating</div>' +
        '</div>' +
        '<div class="game-log__stat">' +
          '<div class="game-log__stat-value">' + (mostPlayedEntry ? mostPlayedEntry.title : '\u2014') + '</div>' +
          '<div class="game-log__stat-label">Most Played</div>' +
        '</div>' +
      '</div>';

  if (totalGames === 0) {
    html +=
      '<div class="game-log__empty">' +
        '<p>No games logged yet. Open any game and click "Log This Game" to start tracking!</p>' +
        '<button class="auth-panel__submit" onclick="navigateTo(\'home\')">Browse Games</button>' +
      '</div>';
  } else {
    html += '<div class="game-log__list">';
    logEntries.forEach(function(entry) {
      var game = window.ENTRIES.find(function(e) { return e.id === entry.game_id; });
      var title = game ? game.title : entry.game_id;
      var cat = game ? window.CAT_CONFIG[game.category] || {} : {};
      var date = entry.played_at ? new Date(entry.played_at).toLocaleDateString() : '';
      var stars = '';
      for (var i = 1; i <= 5; i++) stars += i <= (entry.rating || 0) ? '\u2605' : '\u2606';

      html +=
        '<div class="game-log__entry">' +
          '<div class="game-log__entry-left">' +
            (game ? '<img src="svgs/thumbnails/' + game.id + '.svg" alt="" class="game-log__thumb" loading="lazy" />' : '') +
            '<div class="game-log__entry-info">' +
              '<div class="game-log__entry-title" onclick="openDetail(\'' + entry.game_id + '\')">' + (cat.icon || '') + ' ' + title + '</div>' +
              '<div class="game-log__entry-meta">' +
                '<span>' + date + '</span>' +
                (entry.player_count ? '<span>\u00b7 ' + entry.player_count + ' players</span>' : '') +
                (entry.duration_minutes ? '<span>\u00b7 ' + entry.duration_minutes + ' min</span>' : '') +
              '</div>' +
              (entry.notes ? '<div class="game-log__entry-notes">' + entry.notes + '</div>' : '') +
            '</div>' +
          '</div>' +
          '<div class="game-log__entry-right">' +
            '<div class="game-log__entry-stars">' + stars + '</div>' +
            (entry.would_play_again ? '<div class="game-log__entry-again">\ud83d\udd01 Play again</div>' : '') +
            '<button class="game-log__entry-delete" onclick="deleteGameLogEntry(\'' + entry.id + '\')" title="Remove">\u00d7</button>' +
          '</div>' +
        '</div>';
    });
    html += '</div>';
  }

  html += '</div>';
  section.innerHTML = html;
}

window.deleteGameLogEntry = function(id) {
  deleteLogEntry(id);
};

// ─── Inject log button into detail view ───
var origOpenDetail = window.openDetail;
window.openDetail = function(id) {
  origOpenDetail(id);
  // Inject log button after the print button
  var actions = document.querySelector('.detail__actions');
  if (actions && !document.getElementById('log-form-container')) {
    var logBtn = document.createElement('button');
    logBtn.className = 'detail__log-btn';
    logBtn.innerHTML =
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>' +
      ' Log This Game';
    logBtn.onclick = function() { window.showLogForm(id); };
    actions.appendChild(logBtn);

    var container = document.createElement('div');
    container.id = 'log-form-container';
    container.style.display = 'none';
    actions.parentNode.insertBefore(container, actions.nextSibling);
  }
};

// ─── Initialize ───
document.addEventListener('auth-changed', function() { loadLog(); });
document.addEventListener('data-loaded', function() { loadLog(); });

})();
