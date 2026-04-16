// Heritage Parlor — Configuration & Constants
(function() {
'use strict';

window.PAGE_SIZE = 24;

window.CAT_CONFIG = {
  "parlor-game":        { icon: "\ud83c\udfad", label: "Parlor Games" },
  "card-game":          { icon: "\ud83c\udccf", label: "Card Games" },
  "magic-trick":        { icon: "\u2728",       label: "Magic Tricks" },
  "puzzle":             { icon: "\ud83e\udde9", label: "Puzzles" },
  "word-game":          { icon: "\ud83d\udcdd", label: "Word Games" },
  "physical-game":      { icon: "\ud83c\udfc3", label: "Physical Games" },
  "board-game":         { icon: "\u265f\ufe0f", label: "Board Games" },
  "folk-game":          { icon: "\ud83c\udfb6", label: "Folk Games" },
  "scientific-recreation": { icon: "\ud83d\udd2c", label: "Science" }
};

window.PLAY_CONFIG = {
  "playable_now":      { icon: "\u2705",       label: "Play Tonight",       color: "#22c55e" },
  "easy_to_source":    { icon: "\ud83d\uded2", label: "Easy to Source",     color: "#3b82f6" },
  "craftable":         { icon: "\ud83d\udd28", label: "Craftable",          color: "#f59e0b" },
  "specialty_needed":  { icon: "\ud83d\udd0e", label: "Specialty Needed",   color: "#f97316" },
  "extinct_equipment": { icon: "\ud83c\udfdb\ufe0f", label: "Extinct Equipment", color: "#ef4444" },
  "dangerous":         { icon: "\u26a0\ufe0f", label: "Dangerous",          color: "#dc2626" }
};

window.FABRICA_CONFIG = {
  stripeEnabled: false,
  apiUrl: 'https://api.fabrica.example.com/commissions',
  stripeKey: '',
  email: 'jeromy.darling@gmail.com'
};

})();
