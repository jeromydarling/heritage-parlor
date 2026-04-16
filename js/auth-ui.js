// Heritage Parlor — Auth UI
(function() {
'use strict';

// ─── Auth Modal ───
function createAuthModal() {
  var modal = document.getElementById('auth-modal');
  if (modal) return modal;

  modal = document.createElement('div');
  modal.id = 'auth-modal';
  modal.className = 'auth-overlay';
  modal.addEventListener('click', function(evt) {
    if (evt.target === modal) closeAuthModal();
  });
  document.body.appendChild(modal);
  return modal;
}

function renderAuthForm(mode) {
  var modal = createAuthModal();
  var isSignUp = mode === 'signup';

  modal.innerHTML =
    '<div class="auth-panel">' +
      '<button class="auth-panel__close" onclick="closeAuthModal()" aria-label="Close">' +
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>' +
      '</button>' +
      '<div class="auth-panel__header">' +
        '<h2 class="auth-panel__title">' + (isSignUp ? 'Create Account' : 'Welcome Back') + '</h2>' +
        '<p class="auth-panel__subtitle">' + (isSignUp ? 'Join the Heritage Parlor community' : 'Sign in to your account') + '</p>' +
      '</div>' +
      '<form class="auth-panel__form" id="auth-form">' +
        (isSignUp ?
          '<div class="auth-panel__field">' +
            '<label for="auth-name">Display Name</label>' +
            '<input type="text" id="auth-name" required placeholder="Your name">' +
          '</div>'
        : '') +
        '<div class="auth-panel__field">' +
          '<label for="auth-email">Email</label>' +
          '<input type="email" id="auth-email" required placeholder="you@example.com">' +
        '</div>' +
        '<div class="auth-panel__field">' +
          '<label for="auth-password">Password</label>' +
          '<input type="password" id="auth-password" required minlength="6" placeholder="' + (isSignUp ? 'At least 6 characters' : 'Your password') + '">' +
        '</div>' +
        '<div class="auth-panel__error" id="auth-error" style="display:none;"></div>' +
        '<button type="submit" class="auth-panel__submit">' + (isSignUp ? 'Create Account' : 'Sign In') + '</button>' +
      '</form>' +
      '<div class="auth-panel__divider"><span>or</span></div>' +
      '<div class="auth-panel__social">' +
        '<button class="auth-panel__social-btn auth-panel__social-btn--google" onclick="socialLogin(\'google\')">' +
          '<svg width="18" height="18" viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>' +
          ' Continue with Google' +
        '</button>' +
        '<button class="auth-panel__social-btn auth-panel__social-btn--apple" onclick="socialLogin(\'apple\')">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.05 20.28c-.98.95-2.05.88-3.08.4-1.09-.5-2.08-.48-3.24 0-1.44.62-2.2.44-3.06-.4C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.32 2.32-2.11 4.45-3.74 4.25z"/></svg>' +
          ' Continue with Apple' +
        '</button>' +
      '</div>' +
      '<div class="auth-panel__magic">' +
        '<button class="auth-panel__magic-btn" onclick="showMagicLink()">' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>' +
          ' Sign in with magic link' +
        '</button>' +
      '</div>' +
      '<div class="auth-panel__toggle">' +
        (isSignUp
          ? 'Already have an account? <a href="#" onclick="openAuthModal(\'signin\'); return false;">Sign in</a>'
          : 'Don\'t have an account? <a href="#" onclick="openAuthModal(\'signup\'); return false;">Create one</a>'
        ) +
      '</div>' +
    '</div>';

  modal.classList.add('auth-overlay--open');
  document.body.style.overflow = 'hidden';

  // Attach form handler
  document.getElementById('auth-form').addEventListener('submit', function(evt) {
    evt.preventDefault();
    handleAuthSubmit(isSignUp);
  });
}

function handleAuthSubmit(isSignUp) {
  var email = document.getElementById('auth-email').value;
  var password = document.getElementById('auth-password').value;
  var errorEl = document.getElementById('auth-error');
  errorEl.style.display = 'none';

  if (!window.isSupabaseReady()) {
    errorEl.textContent = 'Authentication is not yet configured. Coming soon!';
    errorEl.style.display = 'block';
    return;
  }

  var submitBtn = document.querySelector('.auth-panel__submit');
  submitBtn.disabled = true;
  submitBtn.textContent = isSignUp ? 'Creating account\u2026' : 'Signing in\u2026';

  var promise;
  if (isSignUp) {
    var displayName = document.getElementById('auth-name').value;
    promise = window.sb.auth.signUp({
      email: email,
      password: password,
      options: { data: { display_name: displayName } }
    });
  } else {
    promise = window.sb.auth.signInWithPassword({ email: email, password: password });
  }

  promise.then(function(res) {
    if (res.error) {
      errorEl.textContent = res.error.message;
      errorEl.style.display = 'block';
      submitBtn.disabled = false;
      submitBtn.textContent = isSignUp ? 'Create Account' : 'Sign In';
    } else {
      closeAuthModal();
    }
  });
}

window.socialLogin = function(provider) {
  if (!window.isSupabaseReady()) {
    var errorEl = document.getElementById('auth-error');
    errorEl.textContent = 'Authentication is not yet configured. Coming soon!';
    errorEl.style.display = 'block';
    return;
  }
  window.sb.auth.signInWithOAuth({ provider: provider });
};

window.showMagicLink = function() {
  var modal = createAuthModal();
  modal.innerHTML =
    '<div class="auth-panel">' +
      '<button class="auth-panel__close" onclick="closeAuthModal()" aria-label="Close">' +
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>' +
      '</button>' +
      '<div class="auth-panel__header">' +
        '<h2 class="auth-panel__title">Magic Link</h2>' +
        '<p class="auth-panel__subtitle">We\'ll email you a sign-in link \u2014 no password needed.</p>' +
      '</div>' +
      '<form class="auth-panel__form" id="magic-form">' +
        '<div class="auth-panel__field">' +
          '<label for="magic-email">Email</label>' +
          '<input type="email" id="magic-email" required placeholder="you@example.com">' +
        '</div>' +
        '<div class="auth-panel__error" id="auth-error" style="display:none;"></div>' +
        '<button type="submit" class="auth-panel__submit">Send Magic Link</button>' +
      '</form>' +
      '<div class="auth-panel__toggle">' +
        '<a href="#" onclick="openAuthModal(\'signin\'); return false;">Back to sign in</a>' +
      '</div>' +
    '</div>';

  document.getElementById('magic-form').addEventListener('submit', function(evt) {
    evt.preventDefault();
    var email = document.getElementById('magic-email').value;
    var errorEl = document.getElementById('auth-error');

    if (!window.isSupabaseReady()) {
      errorEl.textContent = 'Authentication is not yet configured. Coming soon!';
      errorEl.style.display = 'block';
      return;
    }

    window.sb.auth.signInWithOtp({ email: email }).then(function(res) {
      if (res.error) {
        errorEl.textContent = res.error.message;
        errorEl.style.display = 'block';
      } else {
        document.getElementById('magic-form').innerHTML =
          '<div class="auth-panel__success">' +
            '<div class="auth-panel__success-icon">\u2709\ufe0f</div>' +
            '<h3>Check your email</h3>' +
            '<p>We sent a sign-in link to <strong>' + email + '</strong></p>' +
          '</div>';
      }
    });
  });
};

window.openAuthModal = function(mode) {
  renderAuthForm(mode || 'signin');
};

window.closeAuthModal = function() {
  var modal = document.getElementById('auth-modal');
  if (modal) {
    modal.classList.remove('auth-overlay--open');
    document.body.style.overflow = '';
  }
};

window.signOut = function() {
  if (window.isSupabaseReady()) {
    window.sb.auth.signOut();
  }
  window.currentUser = null;
  window.currentProfile = null;
  document.dispatchEvent(new CustomEvent('auth-changed', { detail: { user: null, profile: null } }));
  closeUserMenu();
};

// ─── Header Auth Button ───
function updateAuthButton(user, profile) {
  var btn = document.getElementById('auth-btn');
  var menu = document.getElementById('user-menu');
  if (!btn) return;

  if (user) {
    var name = (profile && profile.display_name) || user.email.split('@')[0];
    var initial = name.charAt(0).toUpperCase();
    btn.className = 'header__auth-btn header__auth-btn--user';
    btn.innerHTML = '<span class="header__avatar">' + initial + '</span> ' + name;
    btn.onclick = function() { toggleUserMenu(); };
  } else {
    btn.className = 'header__auth-btn';
    btn.innerHTML = 'Sign In';
    btn.onclick = function() { openAuthModal('signin'); };
    if (menu) menu.classList.remove('user-menu--open');
  }
}

function toggleUserMenu() {
  var menu = document.getElementById('user-menu');
  if (menu) menu.classList.toggle('user-menu--open');
}

function closeUserMenu() {
  var menu = document.getElementById('user-menu');
  if (menu) menu.classList.remove('user-menu--open');
}

// Close menu on outside click
document.addEventListener('click', function(evt) {
  var menu = document.getElementById('user-menu');
  var btn = document.getElementById('auth-btn');
  if (menu && btn && !menu.contains(evt.target) && !btn.contains(evt.target)) {
    menu.classList.remove('user-menu--open');
  }
});

// ─── Profile Page ───
function renderProfile(user, profile) {
  var section = document.getElementById('profile-section');
  if (!section) return;

  if (!user) {
    section.innerHTML =
      '<div class="container profile">' +
        '<div class="profile__empty">' +
          '<h2>Sign in to view your profile</h2>' +
          '<p>Create an account to track games, save favorites, and join the community.</p>' +
          '<button class="auth-panel__submit" onclick="openAuthModal(\'signup\')">Create Account</button>' +
        '</div>' +
      '</div>';
    return;
  }

  var name = (profile && profile.display_name) || user.email.split('@')[0];
  var initial = name.charAt(0).toUpperCase();
  var bio = (profile && profile.bio) || '';
  var gamesLogged = (profile && profile.games_logged) || 0;
  var contributions = (profile && profile.contribution_count) || 0;
  var favCats = (profile && profile.favorite_categories) || [];

  // Count badges from localStorage or Supabase
  var earnedBadges = [];
  try { earnedBadges = JSON.parse(localStorage.getItem('hp_badges') || '[]'); } catch(e) {}

  // Build favorite categories selector
  var catOptions = Object.keys(window.CAT_CONFIG).map(function(cat) {
    var cfg = window.CAT_CONFIG[cat];
    var checked = favCats.indexOf(cat) !== -1;
    return '<label class="profile__cat-option' + (checked ? ' profile__cat-option--active' : '') + '">' +
      '<input type="checkbox" value="' + cat + '"' + (checked ? ' checked' : '') + ' onchange="toggleFavoriteCategory(\'' + cat + '\')" />' +
      '<span>' + cfg.icon + ' ' + cfg.label + '</span>' +
    '</label>';
  }).join('');

  section.innerHTML =
    '<div class="container profile">' +
      '<div class="profile__header">' +
        '<div class="profile__avatar-large">' + initial + '</div>' +
        '<div class="profile__info">' +
          '<h2 class="profile__name">' + name + '</h2>' +
          '<p class="profile__email">' + user.email + '</p>' +
          (bio ? '<p class="profile__bio">' + bio + '</p>' : '') +
        '</div>' +
      '</div>' +
      '<div class="profile__stats">' +
        '<div class="profile__stat">' +
          '<div class="profile__stat-value">' + gamesLogged + '</div>' +
          '<div class="profile__stat-label">Games Logged</div>' +
        '</div>' +
        '<div class="profile__stat">' +
          '<div class="profile__stat-value">' + contributions + '</div>' +
          '<div class="profile__stat-label">Contributions</div>' +
        '</div>' +
        '<div class="profile__stat">' +
          '<div class="profile__stat-value">' + earnedBadges.length + '</div>' +
          '<div class="profile__stat-label">Badges</div>' +
        '</div>' +
      '</div>' +
      (earnedBadges.length > 0 ?
        '<div class="profile__section">' +
          '<h3 class="profile__section-title">\ud83c\udfc6 Earned Badges</h3>' +
          '<div class="profile__badges">' +
            earnedBadges.map(function(b) {
              return '<div class="profile__badge"><span class="profile__badge-icon">' + (b.icon || '\ud83c\udfc5') + '</span><span class="profile__badge-name">' + b.name + '</span></div>';
            }).join('') +
          '</div>' +
        '</div>'
      : '') +
      '<div class="profile__section">' +
        '<h3 class="profile__section-title">\u2764\ufe0f Favorite Categories</h3>' +
        '<p class="profile__section-desc">These are used by the Game Picker to recommend games you\'ll love.</p>' +
        '<div class="profile__cats">' + catOptions + '</div>' +
      '</div>' +
      '<div class="profile__actions">' +
        '<button class="profile__btn" onclick="signOut()">Sign Out</button>' +
      '</div>' +
    '</div>';
}

// ─── Listen for auth changes ───
document.addEventListener('auth-changed', function(evt) {
  var user = evt.detail.user;
  var profile = evt.detail.profile;
  updateAuthButton(user, profile);
  renderProfile(user, profile);

  // Show/hide auth-dependent nav items
  var loggedInItems = document.querySelectorAll('[data-auth="logged-in"]');
  var loggedOutItems = document.querySelectorAll('[data-auth="logged-out"]');
  loggedInItems.forEach(function(el) { el.style.display = user ? '' : 'none'; });
  loggedOutItems.forEach(function(el) { el.style.display = user ? 'none' : ''; });
});

window.toggleFavoriteCategory = function(cat) {
  var favCats = [];
  if (window.currentProfile && window.currentProfile.favorite_categories) {
    favCats = window.currentProfile.favorite_categories.slice();
  }
  var idx = favCats.indexOf(cat);
  if (idx === -1) favCats.push(cat);
  else favCats.splice(idx, 1);

  if (window.currentProfile) window.currentProfile.favorite_categories = favCats;

  if (window.isSupabaseReady() && window.currentUser) {
    window.sb.from('profiles').update({ favorite_categories: favCats }).eq('id', window.currentUser.id);
  } else {
    localStorage.setItem('hp_fav_cats', JSON.stringify(favCats));
  }

  // Toggle visual state
  document.querySelectorAll('.profile__cat-option').forEach(function(label) {
    var cb = label.querySelector('input');
    label.classList.toggle('profile__cat-option--active', cb && cb.checked);
  });
};

window.toggleUserMenu = toggleUserMenu;

})();
