// Heritage Parlor — Admin Dashboard
(function() {
'use strict';

var isAdmin = false;

function checkAdmin() {
  isAdmin = window.currentProfile && window.currentProfile.is_admin === true;
  var adminNav = document.querySelector('[data-nav="admin"]');
  if (adminNav) adminNav.style.display = isAdmin ? '' : 'none';
  if (isAdmin) renderAdminDashboard();
}

function renderAdminDashboard() {
  var section = document.getElementById('admin-section');
  if (!section) return;

  section.innerHTML =
    '<div class="container admin">' +
      '<h2 class="admin__heading">Admin Dashboard</h2>' +
      '<div class="admin__tabs">' +
        '<button class="admin__tab admin__tab--active" data-tab="moderation" onclick="switchAdminTab(\'moderation\')">Moderation</button>' +
        '<button class="admin__tab" data-tab="challenges" onclick="switchAdminTab(\'challenges\')">Challenges</button>' +
        '<button class="admin__tab" data-tab="games" onclick="switchAdminTab(\'games\')">Games</button>' +
        '<button class="admin__tab" data-tab="users" onclick="switchAdminTab(\'users\')">Users</button>' +
        '<button class="admin__tab" data-tab="analytics" onclick="switchAdminTab(\'analytics\')">Analytics</button>' +
        '<button class="admin__tab" data-tab="commerce" onclick="switchAdminTab(\'commerce\')">Commerce</button>' +
      '</div>' +
      '<div class="admin__content" id="admin-content"></div>' +
    '</div>';

  switchAdminTab('moderation');
}

window.switchAdminTab = function(tab) {
  document.querySelectorAll('.admin__tab').forEach(function(t) {
    t.classList.toggle('admin__tab--active', t.dataset.tab === tab);
  });

  var content = document.getElementById('admin-content');
  if (!content) return;

  switch (tab) {
    case 'moderation':
      renderModerationTab(content);
      break;
    case 'challenges':
      renderChallengesTab(content);
      break;
    case 'games':
      renderGamesTab(content);
      break;
    case 'users':
      renderUsersTab(content);
      break;
    case 'analytics':
      renderAnalyticsTab(content);
      break;
    case 'commerce':
      renderCommerceTab(content);
      break;
  }
};

function renderModerationTab(el) {
  el.innerHTML =
    '<div class="admin__section">' +
      '<div style="display:flex;justify-content:space-between;align-items:center;">' +
        '<h3>Pending Suggestions</h3>' +
        '<div class="admin__bulk-actions" id="suggestions-bulk" style="display:none;">' +
          '<button class="admin__approve-btn" onclick="bulkModerateSuggestions(\'approved\')">\u2705 Approve All</button>' +
          '<button class="admin__reject-btn" onclick="bulkModerateSuggestions(\'rejected\')">\u274c Reject All</button>' +
        '</div>' +
      '</div>' +
      '<div class="admin__queue" id="admin-suggestions-queue">' +
        '<p class="admin__empty">No pending suggestions.</p>' +
      '</div>' +
    '</div>' +
    '<div class="admin__section">' +
      '<h3>Submitted Games</h3>' +
      '<div class="admin__queue" id="admin-games-queue">' +
        '<p class="admin__empty">No pending game submissions.</p>' +
      '</div>' +
    '</div>';

  if (window.isSupabaseReady()) {
    // Load pending suggestions
    window.sb.from('game_suggestions').select('*').eq('status', 'pending')
      .order('created_at', { ascending: false }).limit(50)
      .then(function(res) {
        var data = res.data || [];
        var queue = document.getElementById('admin-suggestions-queue');
        if (!queue || data.length === 0) return;
        var bulk = document.getElementById('suggestions-bulk');
        if (bulk && data.length > 1) bulk.style.display = '';
        queue.innerHTML = data.map(function(s) {
          return '<div class="admin__queue-item">' +
            '<div class="admin__queue-item-info">' +
              '<strong>' + s.game_id + '</strong> \u2014 ' + s.suggestion_type + ': ' + s.suggestion_text +
            '</div>' +
            '<div class="admin__queue-item-actions">' +
              '<button class="admin__approve-btn" onclick="moderateSuggestion(\'' + s.id + '\', \'approved\')">\u2705 Approve</button>' +
              '<button class="admin__reject-btn" onclick="moderateSuggestion(\'' + s.id + '\', \'rejected\')">\u274c Reject</button>' +
            '</div>' +
          '</div>';
        }).join('');
      });

    // Load pending games
    window.sb.from('submitted_games').select('*').eq('status', 'pending')
      .order('created_at', { ascending: false }).limit(50)
      .then(function(res) {
        var data = res.data || [];
        var queue = document.getElementById('admin-games-queue');
        if (!queue || data.length === 0) return;
        queue.innerHTML = data.map(function(g) {
          return '<div class="admin__queue-item">' +
            '<div class="admin__queue-item-info">' +
              '<strong>' + g.title + '</strong>' +
              (g.category ? ' (' + g.category + ')' : '') +
              '<p>' + (g.description || '').substring(0, 200) + '</p>' +
            '</div>' +
            '<div class="admin__queue-item-actions">' +
              '<button class="admin__approve-btn" onclick="moderateGame(\'' + g.id + '\', \'approved\')">\u2705 Approve</button>' +
              '<button class="admin__reject-btn" onclick="moderateGame(\'' + g.id + '\', \'rejected\')">\u274c Reject</button>' +
            '</div>' +
          '</div>';
        }).join('');
      });
  }
}

function renderChallengesTab(el) {
  el.innerHTML =
    '<div class="admin__section">' +
      '<div style="display:flex;justify-content:space-between;align-items:center;">' +
        '<h3>Seasonal Challenges</h3>' +
        '<button class="log-form__submit" style="padding:8px 16px;font-size:var(--text-sm);" onclick="showCreateChallengeForm()">+ New Challenge</button>' +
      '</div>' +
      '<div id="admin-challenges-list">' +
        '<p class="admin__empty">Loading challenges\u2026</p>' +
      '</div>' +
      '<div id="admin-challenge-form" style="display:none;"></div>' +
    '</div>';

  if (window.isSupabaseReady()) {
    window.sb.from('seasonal_challenges').select('*')
      .order('starts_at', { ascending: false }).limit(20)
      .then(function(res) {
        var data = res.data || [];
        var list = document.getElementById('admin-challenges-list');
        if (!list) return;
        if (data.length === 0) {
          list.innerHTML = '<p class="admin__empty">No challenges yet. Create one above!</p>';
          return;
        }
        list.innerHTML = data.map(function(ch) {
          var status = ch.is_active ? '\u2705 Active' : '\u23f8 Inactive';
          return '<div class="admin__queue-item">' +
            '<div class="admin__queue-item-info">' +
              '<strong>' + ch.title + '</strong> \u2014 ' + status +
              '<br><span style="font-size:var(--text-xs);color:var(--color-text-muted);">' +
                ch.theme + ' \u00b7 ' + (ch.game_ids || []).length + ' games \u00b7 ' +
                new Date(ch.starts_at).toLocaleDateString() + ' \u2013 ' + new Date(ch.ends_at).toLocaleDateString() +
              '</span>' +
            '</div>' +
            '<div class="admin__queue-item-actions">' +
              '<button class="admin__' + (ch.is_active ? 'reject' : 'approve') + '-btn" onclick="toggleChallenge(\'' + ch.id + '\', ' + !ch.is_active + ')">' +
                (ch.is_active ? 'Deactivate' : 'Activate') +
              '</button>' +
            '</div>' +
          '</div>';
        }).join('');
      }).catch(function() {
        var list = document.getElementById('admin-challenges-list');
        if (list) list.innerHTML = '<p class="admin__empty">Failed to load challenges.</p>';
      });
  } else {
    var list = document.getElementById('admin-challenges-list');
    if (list) list.innerHTML = '<p class="admin__empty">Connect Supabase to manage challenges.</p>';
  }
}

function renderAnalyticsTab(el) {
  var entries = window.ENTRIES || [];
  var catCount = Object.keys(window.CAT_CONFIG || {}).length;
  var buildCount = entries.filter(function(e) { return e.build_guide && e.build_guide.available; }).length;
  var svgCount = entries.length * 3;

  el.innerHTML =
    '<div class="admin__analytics">' +
      '<div class="admin__stat-card">' +
        '<div class="admin__stat-card-value">' + entries.length + '</div>' +
        '<div class="admin__stat-card-label">Total Games</div>' +
      '</div>' +
      '<div class="admin__stat-card">' +
        '<div class="admin__stat-card-value">' + catCount + '</div>' +
        '<div class="admin__stat-card-label">Categories</div>' +
      '</div>' +
      '<div class="admin__stat-card">' +
        '<div class="admin__stat-card-value">' + buildCount + '</div>' +
        '<div class="admin__stat-card-label">Build Guides</div>' +
      '</div>' +
      '<div class="admin__stat-card">' +
        '<div class="admin__stat-card-value">' + svgCount.toLocaleString() + '</div>' +
        '<div class="admin__stat-card-label">SVG Assets</div>' +
      '</div>' +
    '</div>' +
    '<p class="admin__empty" style="margin-top:var(--space-6)">User analytics will be available once Supabase is connected.</p>';
}

function renderCommerceTab(el) {
  var stages = ['pending', 'paid', 'in_progress', 'shipped', 'completed'];
  var labels = { pending: 'Pending', paid: 'Paid', in_progress: 'In Progress', shipped: 'Shipped', completed: 'Completed' };

  el.innerHTML =
    '<div class="admin__section">' +
      '<h3>Commission Pipeline</h3>' +
      '<div class="admin__pipeline" id="admin-pipeline">' +
        stages.map(function(s) {
          return '<div class="admin__pipeline-stage"><div class="admin__pipeline-count" id="pipeline-' + s + '">0</div><div class="admin__pipeline-label">' + labels[s] + '</div></div>';
        }).join('') +
      '</div>' +
      '<p class="admin__empty" id="commerce-status">Commerce tracking requires Stripe Connect and Supabase.</p>' +
    '</div>';

  if (window.isSupabaseReady()) {
    document.getElementById('commerce-status').textContent = 'Loading commission data\u2026';
    window.sb.from('commissions').select('status').then(function(res) {
      var data = res.data || [];
      var counts = {};
      data.forEach(function(c) { counts[c.status] = (counts[c.status] || 0) + 1; });
      stages.forEach(function(s) {
        var countEl = document.getElementById('pipeline-' + s);
        if (countEl) countEl.textContent = counts[s] || 0;
      });
      document.getElementById('commerce-status').textContent = data.length > 0
        ? data.length + ' total commissions'
        : 'No commissions yet.';
    }).catch(function() {
      document.getElementById('commerce-status').textContent = 'Failed to load commerce data.';
    });
  }
}

window.toggleChallenge = function(id, active) {
  if (window.isSupabaseReady()) {
    window.sb.from('seasonal_challenges').update({ is_active: active }).eq('id', id)
      .then(function() { switchAdminTab('challenges'); });
  }
};

window.moderateSuggestion = function(id, status) {
  if (window.isSupabaseReady()) {
    window.sb.from('game_suggestions').update({ status: status }).eq('id', id)
      .then(function() { switchAdminTab('moderation'); });
  }
};

window.moderateGame = function(id, status) {
  if (window.isSupabaseReady()) {
    window.sb.from('submitted_games').update({ status: status }).eq('id', id)
      .then(function() { switchAdminTab('moderation'); });
  }
};

window.showCreateChallengeForm = function() {
  var form = document.getElementById('admin-challenge-form');
  if (!form) return;
  form.style.display = 'block';
  form.innerHTML =
    '<form class="event-form" style="margin-top:var(--space-4);" id="challenge-create-form">' +
      '<div class="event-form__field"><label>Title</label><input type="text" id="ch-title" required placeholder="Spring Parlor Revival"></div>' +
      '<div class="event-form__field"><label>Description</label><textarea id="ch-desc" rows="2" placeholder="Challenge description"></textarea></div>' +
      '<div class="event-form__row">' +
        '<div class="event-form__field"><label>Theme</label><select id="ch-theme"><option>spring</option><option>summer</option><option>autumn</option><option>winter</option><option>holiday</option><option>spooky</option></select></div>' +
        '<div class="event-form__field"><label>Start Date</label><input type="date" id="ch-start" required></div>' +
        '<div class="event-form__field"><label>End Date</label><input type="date" id="ch-end" required></div>' +
      '</div>' +
      '<div class="event-form__field"><label>Game IDs (comma-separated)</label><input type="text" id="ch-games" required placeholder="acting-proverbs, twenty-questions, charades"></div>' +
      '<div class="event-form__field"><label>Badge Name</label><input type="text" id="ch-badge" placeholder="Spring Revival"></div>' +
      '<div class="event-form__actions">' +
        '<button type="submit" class="log-form__submit">Create Challenge</button>' +
        '<button type="button" class="log-form__cancel" onclick="document.getElementById(\'admin-challenge-form\').style.display=\'none\'">Cancel</button>' +
      '</div>' +
    '</form>';

  document.getElementById('challenge-create-form').addEventListener('submit', function(evt) {
    evt.preventDefault();
    if (!window.isSupabaseReady()) return;
    var gameIds = document.getElementById('ch-games').value.split(',').map(function(s) { return s.trim(); });
    window.sb.from('seasonal_challenges').insert({
      title: document.getElementById('ch-title').value,
      description: document.getElementById('ch-desc').value,
      theme: document.getElementById('ch-theme').value,
      starts_at: document.getElementById('ch-start').value,
      ends_at: document.getElementById('ch-end').value,
      game_ids: gameIds,
      badge_name: document.getElementById('ch-badge').value,
      is_active: true
    }).then(function() {
      form.style.display = 'none';
      switchAdminTab('challenges');
    });
  });
};

// ─── Bulk moderation ───
window.bulkModerateSuggestions = function(status) {
  if (!window.isSupabaseReady()) return;
  window.sb.from('game_suggestions').update({ status: status }).eq('status', 'pending')
    .then(function() { switchAdminTab('moderation'); })
    .catch(function(err) { console.error('Bulk moderate failed:', err); });
};

// ─── Games Editor Tab ───
function renderGamesTab(el) {
  el.innerHTML =
    '<div class="admin__section">' +
      '<h3>Edit Game Entries</h3>' +
      '<div class="admin__search">' +
        '<input type="text" id="admin-game-search" placeholder="Search by title or ID\u2026" class="admin__search-input" />' +
      '</div>' +
      '<div id="admin-games-list" class="admin__queue"></div>' +
      '<div id="admin-game-editor" style="display:none;"></div>' +
    '</div>';

  var entries = window.ENTRIES || [];
  renderGamesList(entries.slice(0, 20));

  document.getElementById('admin-game-search').addEventListener('input', function() {
    var q = this.value.toLowerCase();
    var filtered = entries.filter(function(e) {
      return e.title.toLowerCase().indexOf(q) !== -1 || e.id.indexOf(q) !== -1;
    });
    renderGamesList(filtered.slice(0, 20));
  });
}

function renderGamesList(games) {
  var list = document.getElementById('admin-games-list');
  if (!list) return;
  if (games.length === 0) {
    list.innerHTML = '<p class="admin__empty">No games match your search.</p>';
    return;
  }
  list.innerHTML = games.map(function(g) {
    var cfg = window.CAT_CONFIG[g.category] || { icon: '', label: '' };
    return '<div class="admin__queue-item">' +
      '<div class="admin__queue-item-info">' +
        '<strong>' + cfg.icon + ' ' + g.title + '</strong>' +
        '<br><span style="font-size:var(--text-xs);color:var(--color-text-muted);">' +
          g.id + ' \u00b7 ' + cfg.label + ' \u00b7 ' + g.difficulty + ' \u00b7 ' + g.source_year +
        '</span>' +
      '</div>' +
      '<div class="admin__queue-item-actions">' +
        '<button class="admin__approve-btn" onclick="editGameEntry(\'' + g.id + '\')">\u270f\ufe0f Edit</button>' +
      '</div>' +
    '</div>';
  }).join('');
}

window.editGameEntry = function(gameId) {
  var entry = window.ENTRIES.find(function(e) { return e.id === gameId; });
  if (!entry) return;
  var editor = document.getElementById('admin-game-editor');
  if (!editor) return;

  var cats = Object.keys(window.CAT_CONFIG).map(function(c) {
    return '<option value="' + c + '"' + (c === entry.category ? ' selected' : '') + '>' + window.CAT_CONFIG[c].label + '</option>';
  }).join('');

  var diffs = ['beginner','intermediate','advanced'].map(function(d) {
    return '<option value="' + d + '"' + (d === entry.difficulty ? ' selected' : '') + '>' + d + '</option>';
  }).join('');

  editor.style.display = 'block';
  editor.innerHTML =
    '<form class="event-form" style="margin-top:var(--space-4);" id="game-edit-form">' +
      '<h3 style="margin-bottom:var(--space-3);">Editing: ' + entry.title + '</h3>' +
      '<div class="event-form__field"><label>Title</label><input type="text" id="ge-title" value="' + entry.title.replace(/"/g, '&quot;') + '" required></div>' +
      '<div class="event-form__row">' +
        '<div class="event-form__field"><label>Category</label><select id="ge-category">' + cats + '</select></div>' +
        '<div class="event-form__field"><label>Difficulty</label><select id="ge-difficulty">' + diffs + '</select></div>' +
        '<div class="event-form__field"><label>Players</label><input type="text" id="ge-players" value="' + (entry.players || '') + '"></div>' +
        '<div class="event-form__field"><label>Duration</label><input type="text" id="ge-duration" value="' + (entry.play_duration || '') + '"></div>' +
      '</div>' +
      '<div class="event-form__field"><label>Modern Explanation</label><textarea id="ge-modern" rows="4">' + entry.modern_explanation + '</textarea></div>' +
      '<div class="event-form__field"><label>Equipment Needed (comma-separated)</label><input type="text" id="ge-equipment" value="' + (entry.equipment_needed || []).join(', ') + '"></div>' +
      '<div class="event-form__field"><label>Fun Fact</label><input type="text" id="ge-funfact" value="' + (entry.fun_fact || '').replace(/"/g, '&quot;') + '"></div>' +
      '<div class="event-form__actions">' +
        '<button type="submit" class="event-form__submit">Save Changes</button>' +
        '<button type="button" class="event-form__cancel" onclick="document.getElementById(\'admin-game-editor\').style.display=\'none\'">Cancel</button>' +
      '</div>' +
    '</form>';

  document.getElementById('game-edit-form').addEventListener('submit', function(evt) {
    evt.preventDefault();
    // Update local entry
    entry.title = document.getElementById('ge-title').value;
    entry.category = document.getElementById('ge-category').value;
    entry.difficulty = document.getElementById('ge-difficulty').value;
    entry.players = document.getElementById('ge-players').value || null;
    entry.play_duration = document.getElementById('ge-duration').value || null;
    entry.modern_explanation = document.getElementById('ge-modern').value;
    entry.equipment_needed = document.getElementById('ge-equipment').value.split(',').map(function(s) { return s.trim(); }).filter(Boolean);
    entry.fun_fact = document.getElementById('ge-funfact').value || null;

    editor.innerHTML = '<div class="kits__confirmation">\u2705 Changes saved locally. Supabase sync will persist changes when connected.</div>';
    setTimeout(function() { editor.style.display = 'none'; }, 2000);
  });
};

// ─── Users Tab ───
function renderUsersTab(el) {
  el.innerHTML =
    '<div class="admin__section">' +
      '<h3>User Management</h3>' +
      '<div id="admin-users-list" class="admin__queue">' +
        '<p class="admin__empty">Loading users\u2026</p>' +
      '</div>' +
    '</div>';

  if (window.isSupabaseReady()) {
    window.sb.from('profiles').select('*').order('joined_at', { ascending: false }).limit(50)
      .then(function(res) {
        var data = res.data || [];
        var list = document.getElementById('admin-users-list');
        if (!list) return;
        if (data.length === 0) {
          list.innerHTML = '<p class="admin__empty">No users yet.</p>';
          return;
        }
        list.innerHTML = data.map(function(u) {
          var initial = (u.display_name || 'A').charAt(0).toUpperCase();
          return '<div class="admin__queue-item">' +
            '<div class="admin__queue-item-info">' +
              '<div style="display:flex;align-items:center;gap:var(--space-2);">' +
                '<span class="header__avatar" style="width:28px;height:28px;font-size:var(--text-xs);">' + initial + '</span>' +
                '<div>' +
                  '<strong>' + (u.display_name || 'Anonymous') + '</strong>' +
                  (u.is_admin ? ' <span style="color:var(--color-primary);font-size:var(--text-xs);">ADMIN</span>' : '') +
                  '<br><span style="font-size:var(--text-xs);color:var(--color-text-muted);">' +
                    'Joined ' + new Date(u.joined_at).toLocaleDateString() +
                    ' \u00b7 ' + (u.games_logged || 0) + ' games \u00b7 ' + (u.contribution_count || 0) + ' contributions' +
                  '</span>' +
                '</div>' +
              '</div>' +
            '</div>' +
            '<div class="admin__queue-item-actions">' +
              (u.is_admin ? '' : '<button class="admin__reject-btn" onclick="banUser(\'' + u.id + '\')">\u26d4 Ban</button>') +
            '</div>' +
          '</div>';
        }).join('');
      }).catch(function() {
        var list = document.getElementById('admin-users-list');
        if (list) list.innerHTML = '<p class="admin__empty">Failed to load users.</p>';
      });
  } else {
    var list = document.getElementById('admin-users-list');
    if (list) list.innerHTML = '<p class="admin__empty">Connect Supabase to manage users.</p>';
  }
}

window.banUser = function(userId) {
  if (!window.isSupabaseReady() || !confirm('Ban this user? This will remove their profile.')) return;
  window.sb.from('profiles').delete().eq('id', userId)
    .then(function() { switchAdminTab('users'); })
    .catch(function(err) { console.error('Ban failed:', err); });
};

// ─── Revenue section in commerce tab ───
// (Revenue dashboard is rendered as part of renderCommerceTab when Supabase data is available)

document.addEventListener('auth-changed', function() { checkAdmin(); });

})();
