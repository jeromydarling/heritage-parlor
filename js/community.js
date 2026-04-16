// Heritage Parlor — Community Ratings & Tips
(function() {
'use strict';

var ratingsCache = {};
var tipsCache = {};

function loadRatings(gameId) {
  if (window.isSupabaseReady()) {
    window.sb.from('community_ratings').select('vote').eq('game_id', gameId)
      .then(function(res) {
        var data = res.data || [];
        var up = data.filter(function(r) { return r.vote === 1; }).length;
        var down = data.filter(function(r) { return r.vote === -1; }).length;
        ratingsCache[gameId] = { up: up, down: down, total: data.length };
        renderRatingsInDetail(gameId);
      });
    window.sb.from('game_suggestions').select('*').eq('game_id', gameId).eq('status', 'approved')
      .order('upvotes', { ascending: false })
      .then(function(res) {
        tipsCache[gameId] = res.data || [];
        renderTipsInDetail(gameId);
      });
  } else {
    // Demo data
    ratingsCache[gameId] = ratingsCache[gameId] || { up: 0, down: 0, total: 0 };
    tipsCache[gameId] = tipsCache[gameId] || [];
    renderRatingsInDetail(gameId);
    renderTipsInDetail(gameId);
  }
}

function renderRatingsInDetail(gameId) {
  var container = document.getElementById('community-ratings');
  if (!container) return;
  var r = ratingsCache[gameId] || { up: 0, down: 0, total: 0 };
  var positiveRatio = r.total > 0 ? r.up / r.total : 0;
  var familyTested = r.total >= 10 && positiveRatio >= 0.7;

  container.innerHTML =
    '<div class="community-ratings">' +
      (familyTested ?
        '<div class="community-ratings__badge">' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>' +
          ' Family Tested' +
        '</div>'
      : '') +
      '<div class="community-ratings__votes">' +
        '<button class="community-ratings__vote-btn community-ratings__vote-btn--up" onclick="voteGame(\'' + gameId + '\', 1)">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>' +
          ' <span>' + r.up + '</span>' +
        '</button>' +
        '<button class="community-ratings__vote-btn community-ratings__vote-btn--down" onclick="voteGame(\'' + gameId + '\', -1)">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"/></svg>' +
          ' <span>' + r.down + '</span>' +
        '</button>' +
      '</div>' +
    '</div>';
}

function renderTipsInDetail(gameId) {
  var container = document.getElementById('community-tips');
  if (!container) return;
  var tips = tipsCache[gameId] || [];

  var html = '<div class="community-tips">';

  if (tips.length > 0) {
    html += '<h4 class="community-tips__heading">Community Tips</h4>';
    tips.forEach(function(tip) {
      var typeIcons = { tip: '\ud83d\udca1', variant: '\ud83c\udfb2', correction: '\u270f\ufe0f', house_rule: '\ud83c\udfe0' };
      html +=
        '<div class="community-tips__item">' +
          '<span class="community-tips__type">' + (typeIcons[tip.suggestion_type] || '\ud83d\udca1') + ' ' + (tip.suggestion_type || 'tip') + '</span>' +
          '<p class="community-tips__text">' + tip.suggestion_text + '</p>' +
        '</div>';
    });
  }

  // Tip submission form
  html +=
    '<div class="community-tips__submit">' +
      '<h4 class="community-tips__heading">Share a Tip</h4>' +
      '<form class="community-tips__form" id="tip-form-' + gameId + '">' +
        '<div class="community-tips__form-row">' +
          '<select class="community-tips__select" id="tip-type-' + gameId + '">' +
            '<option value="tip">Tip</option>' +
            '<option value="variant">Variant</option>' +
            '<option value="correction">Correction</option>' +
            '<option value="house_rule">House Rule</option>' +
          '</select>' +
          '<input type="text" class="community-tips__input" id="tip-text-' + gameId + '" placeholder="Your tip or variant\u2026" required>' +
          '<button type="submit" class="community-tips__btn">Submit</button>' +
        '</div>' +
      '</form>' +
      '<div class="community-tips__confirm" id="tip-confirm-' + gameId + '" style="display:none;">\u2705 Tip submitted for review!</div>' +
    '</div>';

  html += '</div>';
  container.innerHTML = html;

  // Attach form handler
  var form = document.getElementById('tip-form-' + gameId);
  if (form) {
    form.addEventListener('submit', function(evt) {
      evt.preventDefault();
      submitTip(gameId);
    });
  }
}

window.voteGame = function(gameId, vote) {
  if (window.isSupabaseReady() && window.currentUser) {
    window.sb.from('community_ratings').upsert({
      game_id: gameId,
      user_id: window.currentUser.id,
      vote: vote
    }, { onConflict: 'game_id,user_id' }).then(function() {
      loadRatings(gameId);
    });
  } else {
    // Demo: just increment locally
    var r = ratingsCache[gameId] || { up: 0, down: 0, total: 0 };
    if (vote === 1) r.up++;
    else r.down++;
    r.total++;
    ratingsCache[gameId] = r;
    renderRatingsInDetail(gameId);
  }
};

function submitTip(gameId) {
  var type = document.getElementById('tip-type-' + gameId).value;
  var text = document.getElementById('tip-text-' + gameId).value.trim();
  if (!text) return;

  if (window.isSupabaseReady() && window.currentUser) {
    window.sb.from('game_suggestions').insert({
      game_id: gameId,
      user_id: window.currentUser.id,
      suggestion_type: type,
      suggestion_text: text
    }).then(function() {
      document.getElementById('tip-form-' + gameId).style.display = 'none';
      document.getElementById('tip-confirm-' + gameId).style.display = 'block';
    });
  } else {
    document.getElementById('tip-form-' + gameId).style.display = 'none';
    document.getElementById('tip-confirm-' + gameId).style.display = 'block';
  }
}

// ─── Inject community section into detail view ───
var origOpenDetail = window.openDetail;
window.openDetail = function(id) {
  origOpenDetail(id);

  var body = document.querySelector('.detail__body');
  if (!body) return;

  // Insert community section before the suggestion form
  var suggestionSection = body.querySelector('.detail__suggestion');
  if (suggestionSection && !document.getElementById('community-ratings')) {
    var communityHtml =
      '<div class="detail__section detail__section--community">' +
        '<h3 class="detail__section-title">\ud83d\udc4d Community Rating</h3>' +
        '<div id="community-ratings"></div>' +
        '<div id="community-tips"></div>' +
      '</div>';
    suggestionSection.insertAdjacentHTML('beforebegin', communityHtml);
    loadRatings(id);
  }
};

})();
