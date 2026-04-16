// Heritage Parlor — Favorites
(function() {
'use strict';

var favorites = new Set();

function loadFavorites() {
  if (window.isSupabaseReady() && window.currentUser) {
    window.sb.from('favorites').select('game_id')
      .eq('user_id', window.currentUser.id)
      .then(function(res) {
        favorites = new Set((res.data || []).map(function(r) { return r.game_id; }));
        updateAllHearts();
      });
  } else {
    try { favorites = new Set(JSON.parse(localStorage.getItem('hp_favorites') || '[]')); } catch(e) { favorites = new Set(); }
    updateAllHearts();
  }
}

function saveFavorite(gameId) {
  favorites.add(gameId);
  if (window.isSupabaseReady() && window.currentUser) {
    window.sb.from('favorites').insert({ user_id: window.currentUser.id, game_id: gameId });
  } else {
    localStorage.setItem('hp_favorites', JSON.stringify(Array.from(favorites)));
  }
}

function removeFavorite(gameId) {
  favorites.delete(gameId);
  if (window.isSupabaseReady() && window.currentUser) {
    window.sb.from('favorites').delete().eq('user_id', window.currentUser.id).eq('game_id', gameId);
  } else {
    localStorage.setItem('hp_favorites', JSON.stringify(Array.from(favorites)));
  }
}

window.toggleFavorite = function(gameId, evt) {
  if (evt) { evt.stopPropagation(); evt.preventDefault(); }
  if (favorites.has(gameId)) {
    removeFavorite(gameId);
  } else {
    saveFavorite(gameId);
  }
  updateAllHearts();
};

window.isFavorite = function(gameId) {
  return favorites.has(gameId);
};

function updateAllHearts() {
  document.querySelectorAll('[data-fav-id]').forEach(function(btn) {
    var id = btn.dataset.favId;
    var isFav = favorites.has(id);
    btn.classList.toggle('fav-btn--active', isFav);
    btn.innerHTML = isFav
      ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>'
      : '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>';
    btn.title = isFav ? 'Remove from favorites' : 'Add to favorites';
  });
}

// ─── Inject hearts into card grid ───
var origRenderCards = window.renderCards;
window.renderCards = function() {
  origRenderCards();
  // Add heart buttons to each card
  document.querySelectorAll('.card').forEach(function(card) {
    var gameId = card.dataset.gameId;
    if (!gameId) return;
    if (card.querySelector('.fav-btn')) return;

    var btn = document.createElement('button');
    btn.className = 'fav-btn' + (favorites.has(gameId) ? ' fav-btn--active' : '');
    btn.dataset.favId = gameId;
    btn.title = favorites.has(gameId) ? 'Remove from favorites' : 'Add to favorites';
    btn.innerHTML = favorites.has(gameId)
      ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>'
      : '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>';
    btn.addEventListener('click', function(evt) { window.toggleFavorite(gameId, evt); });
    card.style.position = 'relative';
    card.appendChild(btn);
  });
};

document.addEventListener('auth-changed', function() { loadFavorites(); });
document.addEventListener('data-loaded', function() { loadFavorites(); });

})();
