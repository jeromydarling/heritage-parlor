// Heritage Parlor — Leaderboard
(function() {
'use strict';

var leaderboardData = [];
var activeTab = 'all-time';

function loadLeaderboard() {
  if (window.isSupabaseReady()) {
    window.sb.from('profiles').select('id, display_name, contribution_count, games_logged')
      .order('contribution_count', { ascending: false })
      .limit(50)
      .then(function(res) {
        leaderboardData = (res.data || []).map(function(p, i) {
          return {
            rank: i + 1,
            name: p.display_name || 'Anonymous',
            initial: (p.display_name || 'A').charAt(0).toUpperCase(),
            points: (p.contribution_count || 0) + (p.games_logged || 0),
            contributions: p.contribution_count || 0,
            gamesLogged: p.games_logged || 0
          };
        });
        renderLeaderboard();
      });
  } else {
    // Demo data
    leaderboardData = [
      { rank: 1, name: 'Victorian Enthusiast', initial: 'V', points: 42, contributions: 12, gamesLogged: 30 },
      { rank: 2, name: 'Parlor Gamer', initial: 'P', points: 35, contributions: 5, gamesLogged: 30 },
      { rank: 3, name: 'Game Historian', initial: 'G', points: 28, contributions: 18, gamesLogged: 10 }
    ];
    renderLeaderboard();
  }
}

function renderLeaderboard() {
  var section = document.getElementById('leaderboard-section');
  if (!section) return;

  var rankIcons = ['\ud83e\udd47', '\ud83e\udd48', '\ud83e\udd49'];

  var html =
    '<div class="container leaderboard">' +
      '<h2 class="leaderboard__heading">Community Contributors</h2>' +
      '<p class="leaderboard__subtitle">Top players and contributors in the Heritage Parlor community.</p>' +
      '<div class="leaderboard__tabs">' +
        '<button class="leaderboard__tab ' + (activeTab === 'all-time' ? 'leaderboard__tab--active' : '') + '" onclick="setLeaderboardTab(\'all-time\')">All Time</button>' +
        '<button class="leaderboard__tab ' + (activeTab === 'monthly' ? 'leaderboard__tab--active' : '') + '" onclick="setLeaderboardTab(\'monthly\')">This Month</button>' +
      '</div>' +
      '<div class="leaderboard__scoring">' +
        '<span>\ud83d\udca1 Approved suggestions: 1pt</span>' +
        '<span>\ud83c\udfae Submitted games: 5pts</span>' +
        '<span>\ud83d\udccb Games logged: 1pt</span>' +
      '</div>';

  if (leaderboardData.length === 0) {
    html += '<div class="leaderboard__empty"><p>No contributors yet. Be the first!</p></div>';
  } else {
    html += '<div class="leaderboard__list">';
    leaderboardData.forEach(function(entry, idx) {
      html +=
        '<div class="leaderboard__entry">' +
          '<div class="leaderboard__rank">' + (idx < 3 ? rankIcons[idx] : entry.rank) + '</div>' +
          '<div class="leaderboard__avatar">' + entry.initial + '</div>' +
          '<div class="leaderboard__info">' +
            '<div class="leaderboard__name">' + entry.name + '</div>' +
            '<div class="leaderboard__breakdown">' +
              entry.gamesLogged + ' games \u00b7 ' + entry.contributions + ' contributions' +
            '</div>' +
          '</div>' +
          '<div class="leaderboard__points">' + entry.points + ' pts</div>' +
        '</div>';
    });
    html += '</div>';
  }

  html += '</div>';
  section.innerHTML = html;
}

window.setLeaderboardTab = function(tab) {
  activeTab = tab;
  if (tab === 'monthly' && window.isSupabaseReady()) {
    // Reload with monthly filter
    var now = new Date();
    var monthStart = new Date(now.getFullYear(), now.getMonth(), 1).toISOString();
    window.sb.from('profiles').select('id, display_name, contribution_count, games_logged')
      .gte('joined_at', monthStart)
      .order('contribution_count', { ascending: false })
      .limit(50)
      .then(function(res) {
        leaderboardData = (res.data || []).map(function(p, i) {
          return {
            rank: i + 1,
            name: p.display_name || 'Anonymous',
            initial: (p.display_name || 'A').charAt(0).toUpperCase(),
            points: (p.contribution_count || 0) + (p.games_logged || 0),
            contributions: p.contribution_count || 0,
            gamesLogged: p.games_logged || 0
          };
        });
        renderLeaderboard();
      });
  } else if (tab === 'all-time') {
    loadLeaderboard();
  } else {
    renderLeaderboard();
  }
};

// Add leaderboard nav item
document.addEventListener('data-loaded', function() { loadLeaderboard(); });
document.addEventListener('auth-changed', function() { loadLeaderboard(); });

})();
