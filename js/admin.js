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
        '<button class="admin__tab admin__tab--active" onclick="switchAdminTab(\'moderation\')">Moderation</button>' +
        '<button class="admin__tab" onclick="switchAdminTab(\'challenges\')">Challenges</button>' +
        '<button class="admin__tab" onclick="switchAdminTab(\'analytics\')">Analytics</button>' +
        '<button class="admin__tab" onclick="switchAdminTab(\'commerce\')">Commerce</button>' +
      '</div>' +
      '<div class="admin__content" id="admin-content"></div>' +
    '</div>';

  switchAdminTab('moderation');
}

window.switchAdminTab = function(tab) {
  document.querySelectorAll('.admin__tab').forEach(function(t) {
    t.classList.toggle('admin__tab--active', t.textContent.toLowerCase() === tab);
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
      '<h3>Pending Suggestions</h3>' +
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
        '<p class="admin__empty">Connect Supabase to manage challenges.</p>' +
      '</div>' +
      '<div id="admin-challenge-form" style="display:none;"></div>' +
    '</div>';
}

function renderAnalyticsTab(el) {
  el.innerHTML =
    '<div class="admin__analytics">' +
      '<div class="admin__stat-card">' +
        '<div class="admin__stat-card-value">' + window.ENTRIES.length + '</div>' +
        '<div class="admin__stat-card-label">Total Games</div>' +
      '</div>' +
      '<div class="admin__stat-card">' +
        '<div class="admin__stat-card-value">9</div>' +
        '<div class="admin__stat-card-label">Categories</div>' +
      '</div>' +
      '<div class="admin__stat-card">' +
        '<div class="admin__stat-card-value">36</div>' +
        '<div class="admin__stat-card-label">Build Guides</div>' +
      '</div>' +
      '<div class="admin__stat-card">' +
        '<div class="admin__stat-card-value">1,506</div>' +
        '<div class="admin__stat-card-label">SVG Assets</div>' +
      '</div>' +
    '</div>' +
    '<p class="admin__empty" style="margin-top:var(--space-6)">User analytics will be available once Supabase is connected.</p>';
}

function renderCommerceTab(el) {
  el.innerHTML =
    '<div class="admin__section">' +
      '<h3>Commission Pipeline</h3>' +
      '<div class="admin__pipeline">' +
        '<div class="admin__pipeline-stage"><div class="admin__pipeline-count">0</div><div class="admin__pipeline-label">Pending</div></div>' +
        '<div class="admin__pipeline-stage"><div class="admin__pipeline-count">0</div><div class="admin__pipeline-label">Paid</div></div>' +
        '<div class="admin__pipeline-stage"><div class="admin__pipeline-count">0</div><div class="admin__pipeline-label">In Progress</div></div>' +
        '<div class="admin__pipeline-stage"><div class="admin__pipeline-count">0</div><div class="admin__pipeline-label">Shipped</div></div>' +
        '<div class="admin__pipeline-stage"><div class="admin__pipeline-count">0</div><div class="admin__pipeline-label">Completed</div></div>' +
      '</div>' +
      '<p class="admin__empty">Commerce tracking requires Stripe Connect and Supabase.</p>' +
    '</div>';
}

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

document.addEventListener('auth-changed', function() { checkAdmin(); });

})();
