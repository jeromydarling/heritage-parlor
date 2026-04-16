// Heritage Parlor — Game Night Events
(function() {
'use strict';

var events = [];

function loadEvents() {
  if (window.isSupabaseReady()) {
    window.sb.from('game_night_events').select('*, event_rsvps(user_id, status)')
      .eq('is_public', true)
      .gte('event_date', new Date().toISOString())
      .order('event_date', { ascending: true })
      .limit(20)
      .then(function(res) {
        events = res.data || [];
        renderEventsSection();
      });
  } else {
    renderEventsSection();
  }
}

function renderEventsSection() {
  var section = document.getElementById('game-nights-events');
  if (!section) return;

  if (events.length === 0) {
    section.innerHTML =
      '<div class="events-empty">' +
        '<p>No upcoming community game nights yet.</p>' +
        '<p>Be the first to host one!</p>' +
      '</div>';
  } else {
    var html = '<div class="events-list">';
    events.forEach(function(evt) {
      var date = new Date(evt.event_date);
      var dateStr = date.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' });
      var timeStr = date.toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' });
      var rsvpCount = (evt.event_rsvps || []).filter(function(r) { return r.status === 'going'; }).length;
      var locationIcons = { in_person: '\ud83c\udfe0', virtual: '\ud83d\udcbb', hybrid: '\ud83c\udf10' };

      html +=
        '<div class="events-list__item">' +
          '<div class="events-list__date">' +
            '<div class="events-list__date-day">' + date.getDate() + '</div>' +
            '<div class="events-list__date-month">' + date.toLocaleDateString(undefined, { month: 'short' }) + '</div>' +
          '</div>' +
          '<div class="events-list__info">' +
            '<div class="events-list__title">' + evt.title + '</div>' +
            '<div class="events-list__meta">' +
              '<span>' + (locationIcons[evt.location_type] || '') + ' ' + (evt.location_type || '').replace('_', ' ') + '</span>' +
              '<span>\u00b7 ' + timeStr + '</span>' +
              '<span>\u00b7 ' + rsvpCount + ' going</span>' +
              (evt.max_attendees ? '<span>\u00b7 max ' + evt.max_attendees + '</span>' : '') +
            '</div>' +
            (evt.description ? '<div class="events-list__desc">' + evt.description + '</div>' : '') +
          '</div>' +
          '<div class="events-list__actions">' +
            '<button class="events-list__rsvp" onclick="rsvpEvent(\'' + evt.id + '\', \'going\')">Going</button>' +
            '<button class="events-list__share" onclick="shareEvent(\'' + evt.id + '\')" title="Copy invite link">' +
              '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>' +
            '</button>' +
          '</div>' +
        '</div>';
    });
    html += '</div>';
    section.innerHTML = html;
  }
}

window.rsvpEvent = function(eventId, status) {
  if (!window.currentUser) {
    window.openAuthModal('signin');
    return;
  }
  if (window.isSupabaseReady()) {
    window.sb.from('event_rsvps').upsert({
      event_id: eventId,
      user_id: window.currentUser.id,
      status: status
    }, { onConflict: 'event_id,user_id' }).then(function() {
      loadEvents();
    }).catch(function(err) {
      console.error('RSVP failed:', err);
    });
  }
};

window.showCreateEventForm = function() {
  if (!window.currentUser) {
    window.openAuthModal('signin');
    return;
  }

  var section = document.getElementById('create-event-form');
  if (!section) return;

  section.style.display = 'block';
  section.innerHTML =
    '<form class="event-form" id="event-form">' +
      '<h3 class="event-form__title">Host a Game Night</h3>' +
      '<div class="event-form__field">' +
        '<label>Event Title</label>' +
        '<input type="text" id="evt-title" required placeholder="Friday Victorian Game Night">' +
      '</div>' +
      '<div class="event-form__field">' +
        '<label>Description</label>' +
        '<textarea id="evt-desc" rows="2" placeholder="What\'s the plan?"></textarea>' +
      '</div>' +
      '<div class="event-form__row">' +
        '<div class="event-form__field">' +
          '<label>Date & Time</label>' +
          '<input type="datetime-local" id="evt-date" required>' +
        '</div>' +
        '<div class="event-form__field">' +
          '<label>Location Type</label>' +
          '<select id="evt-location">' +
            '<option value="in_person">In Person</option>' +
            '<option value="virtual">Virtual</option>' +
            '<option value="hybrid">Hybrid</option>' +
          '</select>' +
        '</div>' +
        '<div class="event-form__field">' +
          '<label>Max Attendees</label>' +
          '<input type="number" id="evt-max" min="2" max="100" placeholder="10">' +
        '</div>' +
      '</div>' +
      '<div class="event-form__field">' +
        '<label>Select Games (optional)</label>' +
        '<div class="event-form__game-picker">' +
          '<input type="text" id="evt-game-search" placeholder="Search and add games\u2026" />' +
          '<div id="evt-game-results" class="event-form__game-results" style="display:none;"></div>' +
          '<div id="evt-selected-games" class="event-form__selected-games"></div>' +
        '</div>' +
      '</div>' +
      '<div class="event-form__actions">' +
        '<button type="submit" class="event-form__submit">Create Event</button>' +
        '<button type="button" class="event-form__cancel" onclick="hideCreateEventForm()">Cancel</button>' +
      '</div>' +
    '</form>';

  // Game search for event
  var selectedEventGames = [];
  window._eventSelectedGames = selectedEventGames;

  document.getElementById('evt-game-search').addEventListener('input', function() {
    var q = this.value.toLowerCase();
    var results = document.getElementById('evt-game-results');
    if (!q || q.length < 2) { results.style.display = 'none'; return; }
    var matches = (window.ENTRIES || []).filter(function(e) {
      return e.title.toLowerCase().indexOf(q) !== -1 && selectedEventGames.indexOf(e.id) === -1;
    }).slice(0, 8);
    if (matches.length === 0) { results.style.display = 'none'; return; }
    results.style.display = 'block';
    results.innerHTML = matches.map(function(g) {
      var cfg = window.CAT_CONFIG[g.category] || { icon: '' };
      return '<div class="event-form__game-result" onclick="addEventGame(\'' + g.id + '\')">' + cfg.icon + ' ' + g.title + '</div>';
    }).join('');
  });

  document.getElementById('event-form').addEventListener('submit', function(evt) {
    evt.preventDefault();
    submitEvent();
  });
};

window.addEventGame = function(gameId) {
  var selected = window._eventSelectedGames || [];
  if (selected.indexOf(gameId) !== -1) return;
  selected.push(gameId);
  document.getElementById('evt-game-search').value = '';
  document.getElementById('evt-game-results').style.display = 'none';
  renderSelectedEventGames();
};

window.removeEventGame = function(gameId) {
  var selected = window._eventSelectedGames || [];
  var idx = selected.indexOf(gameId);
  if (idx !== -1) selected.splice(idx, 1);
  renderSelectedEventGames();
};

function renderSelectedEventGames() {
  var container = document.getElementById('evt-selected-games');
  var selected = window._eventSelectedGames || [];
  if (!container) return;
  container.innerHTML = selected.map(function(id) {
    var game = (window.ENTRIES || []).find(function(e) { return e.id === id; });
    var cfg = game ? (window.CAT_CONFIG[game.category] || { icon: '' }) : { icon: '' };
    return '<span class="event-form__selected-tag">' +
      cfg.icon + ' ' + (game ? game.title : id) +
      ' <button type="button" onclick="removeEventGame(\'' + id + '\')">\u00d7</button>' +
    '</span>';
  }).join('');
}

function submitEvent() {
  var title = document.getElementById('evt-title').value.trim();
  var desc = document.getElementById('evt-desc').value.trim();
  var date = document.getElementById('evt-date').value;
  var locType = document.getElementById('evt-location').value;
  var maxAtt = parseInt(document.getElementById('evt-max').value) || null;
  var gameIds = window._eventSelectedGames || [];

  if (window.isSupabaseReady() && window.currentUser) {
    window.sb.from('game_night_events').insert({
      host_user_id: window.currentUser.id,
      title: title,
      description: desc,
      event_date: date,
      location_type: locType,
      max_attendees: maxAtt,
      game_ids: gameIds,
      is_public: true
    }).then(function() {
      hideCreateEventForm();
      loadEvents();
    });
  } else {
    hideCreateEventForm();
  }
}

window.shareEvent = function(eventId) {
  var url = window.location.origin + window.location.pathname + '?event=' + eventId;
  if (navigator.clipboard) {
    navigator.clipboard.writeText(url).then(function() {
      var toast = document.createElement('div');
      toast.className = 'toast';
      toast.textContent = 'Invite link copied!';
      document.body.appendChild(toast);
      setTimeout(function() { toast.classList.add('toast--visible'); }, 10);
      setTimeout(function() { toast.classList.remove('toast--visible'); setTimeout(function() { toast.remove(); }, 300); }, 3000);
    });
  }
};

window.hideCreateEventForm = function() {
  var section = document.getElementById('create-event-form');
  if (section) { section.style.display = 'none'; section.innerHTML = ''; }
};

// ─── Inject events section into game nights page ───
document.addEventListener('data-loaded', function() {
  var gnSection = document.getElementById('game-nights-section');
  if (!gnSection) return;

  // Check if we already injected
  if (document.getElementById('game-nights-events')) return;

  var eventsBlock = document.createElement('div');
  eventsBlock.className = 'container';
  eventsBlock.style.marginTop = 'var(--space-8)';
  eventsBlock.innerHTML =
    '<div class="events-header">' +
      '<h2 class="events-header__title">Community Game Nights</h2>' +
      '<button class="picker-hero-btn" style="font-size:var(--text-sm);padding:10px 20px;" onclick="showCreateEventForm()">+ Host a Game Night</button>' +
    '</div>' +
    '<div id="create-event-form" style="display:none;"></div>' +
    '<div id="game-nights-events"></div>';

  gnSection.appendChild(eventsBlock);
  loadEvents();
});

})();
