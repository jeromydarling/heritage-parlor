// Heritage Parlor — Commission Modal (Fabrica / Stripe Connect)
(function() {
'use strict';

window.openCommission = function(gameId) {
  var e = window.ENTRIES.find(function(x) { return x.id === gameId; });
  if (!e || !e.build_guide || !e.build_guide.fabrica) return;
  var fab = e.build_guide.fabrica;

  var modal = document.getElementById('commission-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'commission-modal';
    modal.className = 'commission-overlay';
    document.body.appendChild(modal);
    modal.addEventListener('click', function(evt) {
      if (evt.target === modal) window.closeCommission();
    });
  }

  modal.innerHTML =
    '<div class="commission-panel">' +
      '<button class="commission-panel__close" onclick="closeCommission()" aria-label="Close">' +
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>' +
      '</button>' +
      '<div class="commission-panel__header">' +
        '<h2 class="commission-panel__title">' + (fab.title || e.title + ' \u2014 Custom Commission') + '</h2>' +
        '<div class="commission-panel__price">' + (fab.price_range || '') + '</div>' +
      '</div>' +
      '<div class="commission-panel__specs">' +
        '<div class="commission-panel__spec">' +
          '<div class="commission-panel__spec-label">Complexity</div>' +
          '<div class="commission-panel__spec-value">' + (fab.complexity || 'Standard') + '</div>' +
        '</div>' +
        '<div class="commission-panel__spec">' +
          '<div class="commission-panel__spec-label">Dimensions</div>' +
          '<div class="commission-panel__spec-value">' + (fab.dimensions || 'Per game specifications') + '</div>' +
        '</div>' +
      '</div>' +
      '<div class="commission-panel__section">' +
        '<h3>Materials</h3>' +
        '<p>' + (fab.materials || 'Premium hardwood construction') + '</p>' +
      '</div>' +
      (fab.finish_notes ?
        '<div class="commission-panel__section">' +
          '<h3>Finish</h3>' +
          '<p>' + fab.finish_notes + '</p>' +
        '</div>'
      : '') +
      (fab.pieces ?
        '<div class="commission-panel__section">' +
          '<h3>Game Pieces</h3>' +
          '<p>' + fab.pieces + '</p>' +
        '</div>'
      : '') +
      '<div class="commission-panel__section commission-panel__section--note">' +
        '<p>Each commission is handcrafted by an independent artisan through Fabrica. Typical lead time is 3\u20136 weeks. Final pricing depends on wood selection and customization options.</p>' +
      '</div>' +
      '<form class="commission-panel__form" onsubmit="submitCommission(event, \'' + e.id + '\')">' +
        '<div class="commission-panel__field">' +
          '<label for="comm-name">Your Name</label>' +
          '<input type="text" id="comm-name" required placeholder="Name">' +
        '</div>' +
        '<div class="commission-panel__field">' +
          '<label for="comm-email">Email</label>' +
          '<input type="email" id="comm-email" required placeholder="you@example.com">' +
        '</div>' +
        '<div class="commission-panel__field">' +
          '<label for="comm-notes">Customization Notes <span style="opacity:0.5">(optional)</span></label>' +
          '<textarea id="comm-notes" rows="3" placeholder="Wood preference, size adjustments, engraving requests..."></textarea>' +
        '</div>' +
        '<button type="submit" class="commission-panel__submit">' +
          (window.FABRICA_CONFIG.stripeEnabled ? 'Proceed to Checkout' : 'Request This Commission') +
        '</button>' +
      '</form>' +
      '<div class="commission-panel__confirm" id="commission-confirm" style="display:none;">' +
        '<div class="commission-panel__confirm-icon">\u2713</div>' +
        '<h3>Commission Request Sent</h3>' +
        '<p>We\'ll be in touch within 48 hours with a detailed quote and timeline for your ' + e.title + ' build.</p>' +
      '</div>' +
      '<div class="commission-panel__footer">' +
        '<span>Powered by Fabrica</span>' +
        '<span>\u00b7</span>' +
        '<span>Secure payments via Stripe</span>' +
      '</div>' +
    '</div>';

  modal.classList.add('commission-overlay--open');
  document.body.style.overflow = 'hidden';
};

window.closeCommission = function() {
  var modal = document.getElementById('commission-modal');
  if (modal) {
    modal.classList.remove('commission-overlay--open');
    document.body.style.overflow = '';
  }
};

window.submitCommission = async function(evt, gameId) {
  evt.preventDefault();
  var e = window.ENTRIES.find(function(x) { return x.id === gameId; });
  var fab = e.build_guide.fabrica;
  var name = document.getElementById('comm-name').value;
  var email = document.getElementById('comm-email').value;
  var notes = document.getElementById('comm-notes').value;

  if (window.FABRICA_CONFIG.stripeEnabled) {
    try {
      var resp = await fetch(window.FABRICA_CONFIG.apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          game_id: gameId,
          game_title: e.title,
          commission_title: fab.title,
          price_range: fab.price_range,
          materials: fab.materials,
          dimensions: fab.dimensions,
          customer_name: name,
          customer_email: email,
          customization_notes: notes
        })
      });
      var data = await resp.json();
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        throw new Error(data.error || 'Failed to create checkout session');
      }
    } catch (err) {
      alert('Commission request failed: ' + err.message + '\nPlease try again or email us directly.');
    }
  } else {
    var subject = encodeURIComponent('Fabrica Commission: ' + fab.title);
    var body = encodeURIComponent(
      'COMMISSION REQUEST\n' +
      '\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n\n' +
      'Game: ' + e.title + '\n' +
      'Commission: ' + fab.title + '\n' +
      'Price Range: ' + fab.price_range + '\n' +
      'Complexity: ' + fab.complexity + '\n\n' +
      'CUSTOMER\n' +
      'Name: ' + name + '\n' +
      'Email: ' + email + '\n\n' +
      'CUSTOMIZATION NOTES\n' +
      (notes || '(none)') + '\n\n' +
      'SPECIFICATIONS\n' +
      'Materials: ' + fab.materials + '\n' +
      'Dimensions: ' + fab.dimensions + '\n' +
      (fab.finish_notes ? 'Finish: ' + fab.finish_notes + '\n' : '') +
      (fab.pieces ? 'Pieces: ' + fab.pieces + '\n' : '')
    );
    window.open('mailto:' + window.FABRICA_CONFIG.email + '?subject=' + subject + '&body=' + body, '_self');

    document.querySelector('.commission-panel__form').style.display = 'none';
    document.getElementById('commission-confirm').style.display = 'block';
  }
};

})();
