// Heritage Parlor — Navigation & Event Handlers
(function() {
'use strict';

// ─── Header scroll shadow ───
var header = document.getElementById('header');
window.addEventListener('scroll', function() {
  header.classList.toggle('header--scrolled', window.scrollY > 10);
}, { passive: true });

// ─── Navigation ───
var currentPage = 'home';

window.navigateTo = function(page) {
  currentPage = page;

  document.querySelectorAll('[data-nav]').forEach(function(b) {
    b.classList.toggle('header__nav-btn--active', b.dataset.nav === page);
  });
  document.querySelectorAll('[data-mob]').forEach(function(b) {
    b.classList.toggle('mobile-nav__btn--active', b.dataset.mob === page);
  });

  var heroSection = document.getElementById('hero-section');
  var searchSection = document.querySelector('.search-section');
  var filtersSection = document.querySelector('.filters');
  var entriesSection = document.getElementById('entries-section');
  var aboutSection = document.getElementById('about-section');
  var gameNightsSection = document.getElementById('game-nights-section');
  var submitSection = document.getElementById('submit-section');

  // Hide all secondary sections first
  aboutSection.classList.remove('about-section--visible');
  if (gameNightsSection) gameNightsSection.classList.remove('about-section--visible');
  if (submitSection) submitSection.classList.remove('about-section--visible');

  // Hide Phase 2 sections
  var phase2Sections = ['profile-section','game-log-section','admin-section','leaderboard-section'];
  phase2Sections.forEach(function(sid) {
    var el = document.getElementById(sid);
    if (el) el.classList.remove('about-section--visible');
  });

  if (page === 'home') {
    heroSection.style.display = '';
    searchSection.style.display = '';
    filtersSection.style.display = '';
    entriesSection.style.display = '';
  } else {
    heroSection.style.display = 'none';
    searchSection.style.display = 'none';
    filtersSection.style.display = 'none';
    entriesSection.style.display = 'none';
    if (page === 'about') {
      aboutSection.classList.add('about-section--visible');
    } else if (page === 'game-nights' && gameNightsSection) {
      gameNightsSection.classList.add('about-section--visible');
    } else if (page === 'submit' && submitSection) {
      submitSection.classList.add('about-section--visible');
    } else {
      // Phase 2 sections
      var target = document.getElementById(page + '-section');
      if (target) target.classList.add('about-section--visible');
    }
  }

  window.scrollTo(0, 0);
};

// ─── Filter handlers ───
window.setFilter = function(cat) {
  window.activeFilter = cat;
  window.visibleCount = window.PAGE_SIZE;
  window.renderFilters();
  window.renderPlayFilters();
  window.renderCards();
};

window.setPlayFilter = function(tier) {
  window.activePlayFilter = tier;
  window.visibleCount = window.PAGE_SIZE;
  window.renderPlayFilters();
  window.renderCards();
};

window.setSortMode = function(mode) {
  window.sortMode = mode;
  window.visibleCount = window.PAGE_SIZE;
  window.renderCards();
};

// ─── Search with debounce ───
var searchTimeout;
document.getElementById('search-input').addEventListener('input', function(evt) {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(function() {
    window.searchQuery = evt.target.value.trim();
    window.visibleCount = window.PAGE_SIZE;
    window.renderCards();
  }, 200);
});

// ─── Load more ───
document.getElementById('load-more-btn').addEventListener('click', function() {
  window.visibleCount += window.PAGE_SIZE;
  window.renderCards();
});

// ─── Close detail on overlay click ───
document.getElementById('detail-overlay').addEventListener('click', function(evt) {
  if (evt.target === evt.currentTarget) window.closeDetail();
});

// ─── Keyboard handlers ───
document.addEventListener('keydown', function(evt) {
  if (evt.key === 'Escape') window.closeDetail();
});

document.addEventListener('keydown', function(evt) {
  if (evt.key === 'Enter' && evt.target.classList.contains('card')) {
    evt.target.click();
  }
});

// ─── Initialize on data load ───
document.addEventListener('data-loaded', function() {
  window.renderFilters();
  window.renderPlayFilters();
  window.renderCards();
});

})();
