// Heritage Parlor — Seasonal Challenges
(function() {
'use strict';

var activeChallenge = null;
var progress = {};

function loadChallenge() {
  if (window.isSupabaseReady()) {
    window.sb.from('seasonal_challenges').select('*').eq('is_active', true)
      .gte('ends_at', new Date().toISOString())
      .lte('starts_at', new Date().toISOString())
      .limit(1).single()
      .then(function(res) {
        activeChallenge = res.data || null;
        if (activeChallenge && window.currentUser) {
          loadProgress();
        }
        renderChallengeBanner();
      });
  } else {
    // Demo challenge
    activeChallenge = {
      id: 'demo-challenge',
      title: 'Spring Parlor Revival',
      description: 'Play 5 classic parlor games this month and earn the Spring Revival badge!',
      theme: 'spring',
      game_ids: ['acting-proverbs', 'twenty-questions', 'charades', 'consequences', 'sardines'],
      starts_at: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString(),
      ends_at: new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).toISOString(),
      badge_name: 'Spring Revival',
      is_active: true
    };
    renderChallengeBanner();
  }
}

function loadProgress() {
  if (!activeChallenge || !window.currentUser) return;
  if (window.isSupabaseReady()) {
    window.sb.from('challenge_progress').select('game_id')
      .eq('user_id', window.currentUser.id)
      .eq('challenge_id', activeChallenge.id)
      .then(function(res) {
        progress = {};
        (res.data || []).forEach(function(r) { progress[r.game_id] = true; });
        renderChallengeBanner();
      });
  }
}

function renderChallengeBanner() {
  var banner = document.getElementById('challenge-banner');
  if (!banner) {
    // Create banner element after hero
    var hero = document.getElementById('hero-section');
    if (!hero) return;
    banner = document.createElement('div');
    banner.id = 'challenge-banner';
    hero.parentNode.insertBefore(banner, hero.nextSibling);
  }

  if (!activeChallenge) {
    banner.style.display = 'none';
    return;
  }

  var gameIds = activeChallenge.game_ids || [];
  var completed = gameIds.filter(function(id) { return progress[id]; }).length;
  var total = gameIds.length;
  var pct = total > 0 ? Math.round(completed / total * 100) : 0;

  var endsAt = new Date(activeChallenge.ends_at);
  var now = new Date();
  var daysLeft = Math.max(0, Math.ceil((endsAt - now) / (1000 * 60 * 60 * 24)));

  var themeIcons = { spring: '\ud83c\udf38', summer: '\u2600\ufe0f', autumn: '\ud83c\udf42', winter: '\u2744\ufe0f', holiday: '\ud83c\udf84', spooky: '\ud83c\udf83' };
  var icon = themeIcons[activeChallenge.theme] || '\ud83c\udfc6';

  banner.className = 'challenge-banner';
  banner.style.display = '';
  banner.innerHTML =
    '<div class="container challenge-banner__inner">' +
      '<div class="challenge-banner__icon">' + icon + '</div>' +
      '<div class="challenge-banner__content">' +
        '<div class="challenge-banner__title">' + activeChallenge.title + '</div>' +
        '<div class="challenge-banner__desc">' + (activeChallenge.description || '') + '</div>' +
        '<div class="challenge-banner__progress">' +
          '<div class="challenge-banner__bar">' +
            '<div class="challenge-banner__bar-fill" style="width:' + pct + '%"></div>' +
          '</div>' +
          '<span class="challenge-banner__count">' + completed + '/' + total + ' games</span>' +
        '</div>' +
      '</div>' +
      '<div class="challenge-banner__meta">' +
        '<span class="challenge-banner__days">' + daysLeft + ' days left</span>' +
        '<button class="challenge-banner__details-btn" onclick="showChallengeDetail()">View Games</button>' +
      '</div>' +
    '</div>';
}

window.showChallengeDetail = function() {
  if (!activeChallenge) return;

  var modal = document.getElementById('challenge-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'challenge-modal';
    modal.className = 'auth-overlay';
    modal.addEventListener('click', function(evt) { if (evt.target === modal) closeChallengeDetail(); });
    document.body.appendChild(modal);
  }

  var gameIds = activeChallenge.game_ids || [];
  var gamesHtml = gameIds.map(function(gid) {
    var game = window.ENTRIES.find(function(e) { return e.id === gid; });
    var done = progress[gid];
    if (!game) return '';
    var cfg = window.CAT_CONFIG[game.category] || { icon: '', label: '' };
    return '<div class="challenge-detail__game ' + (done ? 'challenge-detail__game--done' : '') + '">' +
      '<span class="challenge-detail__check">' + (done ? '\u2705' : '\u2b1c') + '</span>' +
      '<img src="svgs/thumbnails/' + game.id + '.svg" alt="" class="challenge-detail__thumb" loading="lazy" />' +
      '<div class="challenge-detail__game-info">' +
        '<div class="challenge-detail__game-title">' + cfg.icon + ' ' + game.title + '</div>' +
        '<div class="challenge-detail__game-desc">' + (game.modern_explanation.length > 80 ? game.modern_explanation.substring(0, 80) + '\u2026' : game.modern_explanation) + '</div>' +
      '</div>' +
      '<button class="challenge-detail__play-btn" onclick="closeChallengeDetail(); openDetail(\'' + game.id + '\')">Play</button>' +
    '</div>';
  }).join('');

  modal.innerHTML =
    '<div class="auth-panel" style="max-width:520px">' +
      '<button class="auth-panel__close" onclick="closeChallengeDetail()" aria-label="Close">' +
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>' +
      '</button>' +
      '<div class="auth-panel__header">' +
        '<h2 class="auth-panel__title">' + activeChallenge.title + '</h2>' +
        '<p class="auth-panel__subtitle">' + (activeChallenge.description || '') + '</p>' +
      '</div>' +
      '<div class="challenge-detail__games">' + gamesHtml + '</div>' +
    '</div>';

  modal.classList.add('auth-overlay--open');
  document.body.style.overflow = 'hidden';
};

window.closeChallengeDetail = function() {
  var modal = document.getElementById('challenge-modal');
  if (modal) { modal.classList.remove('auth-overlay--open'); document.body.style.overflow = ''; }
};

document.addEventListener('data-loaded', function() { loadChallenge(); });
document.addEventListener('auth-changed', function() {
  if (activeChallenge && window.currentUser) loadProgress();
});

})();
