// Heritage Parlor — Supabase Client Stub
// Lovable.app will fill in SUPABASE_URL and SUPABASE_ANON_KEY
(function() {
'use strict';

// ─── Configuration (to be set by Lovable) ───
var SUPABASE_URL = '';
var SUPABASE_ANON_KEY = '';

window.currentUser = null;
window.currentProfile = null;

window.isSupabaseReady = function() {
  return !!(SUPABASE_URL && SUPABASE_ANON_KEY && window.sb);
};

// Initialize Supabase client if credentials are provided
if (SUPABASE_URL && SUPABASE_ANON_KEY && window.supabase) {
  window.sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

  // Listen for auth state changes
  window.sb.auth.onAuthStateChange(function(event, session) {
    window.currentUser = session ? session.user : null;
    if (window.currentUser) {
      // Fetch profile
      window.sb.from('profiles').select('*').eq('id', window.currentUser.id).single()
        .then(function(res) {
          window.currentProfile = res.data || null;
          document.dispatchEvent(new CustomEvent('auth-changed', { detail: { user: window.currentUser, profile: window.currentProfile } }));
        });
    } else {
      window.currentProfile = null;
      document.dispatchEvent(new CustomEvent('auth-changed', { detail: { user: null, profile: null } }));
    }
  });
} else {
  // No Supabase configured — fire event with null user so UI initializes correctly
  window.sb = null;
  console.info('[Heritage Parlor] Supabase not configured. Running in demo mode with localStorage fallback. Set SUPABASE_URL and SUPABASE_ANON_KEY to connect.');
  function fireAuthNull() {
    document.dispatchEvent(new CustomEvent('auth-changed', { detail: { user: null, profile: null } }));
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fireAuthNull);
  } else {
    fireAuthNull();
  }
}

})();
