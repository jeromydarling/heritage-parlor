// Heritage Parlor — Submit Game Form
(function() {
'use strict';

window.handleGameSubmit = function(evt) {
  evt.preventDefault();
  var f = evt.target;
  var name = f.querySelector('#sg-name').value.trim();
  var category = f.querySelector('#sg-category').value;
  var description = f.querySelector('#sg-description').value.trim();
  var howtoplay = f.querySelector('#sg-howtoplay').value.trim();
  var source = f.querySelector('#sg-source').value.trim();
  var yourname = f.querySelector('#sg-yourname').value.trim();
  var email = f.querySelector('#sg-email').value.trim();

  var subject = encodeURIComponent('Heritage Parlor Game Submission: ' + name);
  var body = 'HERITAGE PARLOR GAME SUBMISSION\n';
  body += '================================\n\n';
  body += 'Game Name: ' + name + '\n';
  if (category) body += 'Category: ' + category + '\n';
  if (description) body += '\nDescription:\n' + description + '\n';
  if (howtoplay) body += '\nHow to Play:\n' + howtoplay + '\n';
  if (source) body += '\nSource: ' + source + '\n';
  if (yourname) body += '\nSubmitted by: ' + yourname + '\n';
  if (email) body += 'Contact email: ' + email + '\n';

  var mailto = 'mailto:jeromy.darling@gmail.com?subject=' + subject + '&body=' + encodeURIComponent(body);
  window.location.href = mailto;

  f.style.display = 'none';
  document.getElementById('submit-confirm').style.display = 'block';
};

})();
