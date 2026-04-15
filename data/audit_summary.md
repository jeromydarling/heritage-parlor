# Heritage Parlor Game Database — Audit Summary

**Total entries audited:** 362

---

## Task 1: Playability Audit

### Counts by Playability Tier

| Tier | Count | Description |
|------|-------|-------------|
| `playable_now` | **249** | No special equipment needed; common household items |
| `easy_to_source` | **69** | Needs standard game equipment easily purchased |
| `craftable` | **18** | Equipment can be made at home or drawn on paper |
| `specialty_needed` | **15** | Requires specific items from specialty suppliers |
| `extinct_equipment` | **9** | Requires Victorian-era manufactured items no longer available |
| `dangerous` | **2** | Involves open flame, fire, or chemical hazards |

### Playability by Category

| Category | playable_now | easy_to_source | craftable | specialty_needed | extinct_equipment | dangerous | Total |
|----------|:-----------:|:--------------:|:---------:|:---------------:|:-----------------:|:---------:|:-----:|
| **board-game** | 2 | 8 | 5 | 0 | 1 | 0 | 16 |
| **card-game** | 0 | 39 | 0 | 0 | 3 | 0 | 42 |
| **magic-trick** | 27 | 14 | 1 | 11 | 3 | 2 | 58 |
| **parlor-game** | 70 | 0 | 0 | 2 | 0 | 0 | 72 |
| **physical-game** | 26 | 3 | 0 | 2 | 2 | 0 | 33 |
| **puzzle** | 87 | 5 | 12 | 0 | 0 | 0 | 104 |
| **word-game** | 37 | 0 | 0 | 0 | 0 | 0 | 37 |

---

### All `extinct_equipment` Entries

These entries require Victorian-era manufactured items that almost certainly no longer exist or cannot be reasonably replicated.

- **Spelicans** (`spelicans`)
  - Equipment: ['set of spelicans']
  - Reason: Spelican set — Victorian ivory/bone stick game requiring precision manufacture; straws are a rough modern substitute but authentic spelicans are extinct

- **The Inexhaustible Bottle** (`the-inexhaustible-bottle`)
  - Equipment: ['specially divided bottle']
  - Reason: Specially divided bottle — Victorian magic apparatus with internal chambers, no modern equivalent

- **The Passe-Passe Bottle and Glass** (`the-passe-passe-bottle-and-glass`)
  - Equipment: ['2 cardboard tubes', 'special bottle and glass']
  - Reason: Special bottle and glass set — Victorian magic apparatus, custom-made for the trick

- **The Magic Mill** (`the-magic-mill`)
  - Equipment: ['small magic mill toy']
  - Reason: The Magic Mill toy — specific Victorian manufactured mechanical toy, extinct

- **Faro** (`faro`)
  - Equipment: ['faro layout board', 'standard deck', 'betting chips']
  - Reason: Faro layout board and dealing box — specific Victorian casino gambling apparatus, obsolete

- **Pope Joan** (`pope-joan`)
  - Equipment: ['standard deck minus one card', 'chips', 'Pope Joan board']
  - Reason: Pope Joan board — circular compartmentalized Victorian board game, no longer manufactured

- **Spelicans (Pick-up Sticks)** (`spelicans-pick-up-sticks`)
  - Equipment: ['spelican set or straws']
  - Reason: Spelican set — Victorian ivory/bone stick game; straws are a rough substitute but authentic spelicans are extinct

- **Pope Joan (Full Rules)** (`pope-joan-full-rules`)
  - Equipment: ['48-card deck (remove 8 of diamonds)', 'Pope Joan board', 'chips']
  - Reason: Pope Joan board — circular compartmentalized Victorian board game, no longer manufactured

- **Dice (Chuck-a-Luck)** (`dice-chuck-a-luck`)
  - Equipment: ['3 dice', 'birdcage or cup', 'betting layout']
  - Reason: Chuck-a-Luck birdcage and betting layout — specific Victorian casino gambling apparatus

---

### All `dangerous` Entries

These entries involve fire, open flames, or chemical/physical hazards.

- **Fire Eating** (`fire-eating`)
  - Equipment: []
  - Reason: Fire eating with burning alcohol on tongue — serious burn/fire risk, do not attempt

- **Carrying Fire in the Hands** (`carrying-fire-in-the-hands`)
  - Equipment: ['surgical spirit', 'damp hands']
  - Reason: Burning surgical spirit (alcohol) on hands — fire hazard; requires expert fire safety measures

---

## Task 2: Illustration Source Mapping

### Counts by Illustration Approach

| Approach | Count | Description |
|----------|-------|-------------|
| `has_original` | **141** | Source book likely contained an original engraving/diagram for this entry |
| `text_sufficient` | **115** | Entry can be fully understood from text alone; no illustration needed |
| `needs_generated` | **106** | Would benefit from an illustration, but source has none or entry has no illustrated source |

### Illustration by Category

| Category | has_original | text_sufficient | needs_generated | Total |
|----------|:-----------:|:---------------:|:---------------:|:-----:|
| **board-game** | 4 | 0 | 12 | 16 |
| **card-game** | 2 | 37 | 3 | 42 |
| **magic-trick** | 58 | 0 | 0 | 58 |
| **parlor-game** | 51 | 20 | 1 | 72 |
| **physical-game** | 18 | 0 | 15 | 33 |
| **puzzle** | 8 | 21 | 75 | 104 |
| **word-game** | 0 | 37 | 0 | 37 |

### Categories: Text-Sufficient vs. Illustration-Needed

**Mostly text-sufficient:**
- `word-game` — All 37 are verbal/written games; no visual diagram ever needed
- `card-game` — Card game rules convey well in text; Foster's Complete Hoyle (the main source) has no illustrations
- `parlor-game` — Social, acting, and guessing games are almost entirely text-sufficient

**Mostly illustration-needed:**
- `magic-trick` — All 58 benefit from apparatus and hand-position diagrams; all from illustrated books (Modern Magic, Every Boy's Book)
- `board-game` — All 16 need board layout diagrams; sourced from both illustrated and non-illustrated books
- `puzzle` — Spatial/arrangement puzzles need diagrams; arithmetic puzzles are text-sufficient. Split roughly evenly
- `physical-game` — Formation/movement games benefit from diagrams; sourced from both illustrated (Every Boy's Book) and non-illustrated books

### Source Books and Illustration Coverage

| Source Book | has_original | text_sufficient | needs_generated | Total | Illustrated? |
|-------------|:-----------:|:---------------:|:---------------:|:-----:|:------------:|
| Amusements in Mathematics | 0 | 18 | 45 | 63 | No |
| Cassell's Book of In-door Amusements, Card Games, and Fireside Fun | 51 | 22 | 4 | 77 | Yes |
| Every Boy's Book | 38 | 2 | 0 | 40 | Yes |
| Foster's Complete Hoyle | 0 | 34 | 11 | 45 | No |
| Modern Magic | 52 | 0 | 0 | 52 | Yes |
| My Book of Indoor Games | 0 | 36 | 16 | 52 | No |
| The Canterbury Puzzles | 0 | 3 | 30 | 33 | No |

---

## Classification Notes

### Playability Decisions

- **Spelicans** (`extinct_equipment`): Authentic Victorian spelicans were precisely shaped ivory or bone sticks. Pick-up sticks (Mikado) are a rough modern analogue, but the authentic set is extinct. Appears as two entries (basic rules and extended rules).
- **Pope Joan board** (`extinct_equipment`): A specific circular board divided into labeled compartments for the card game Pope Joan. No longer commercially manufactured. Appears in two entries.
- **Faro** (`extinct_equipment`): Required a dealing box (the "tiger"), faro layout cloth, case keeper, and betting equipment — an entire specialized apparatus now obsolete.
- **Chuck-a-Luck** (`extinct_equipment`): Requires a Chuck-a-Luck birdcage (rotating wire cage) and casino betting layout — both obsolete gambling apparatus.
- **The Inexhaustible Bottle** and **The Passe-Passe Bottle and Glass** (`extinct_equipment`): Both require specifically manufactured bottles with internal dividers/chambers. No modern replica.
- **The Magic Mill** (`extinct_equipment`): The `the-magic-mill` entry requires a Victorian manufactured mechanical toy. Note: `the-magic-mill-trick` is a *different* entry (paper folding) classified `playable_now`.
- **Fire Eating** and **Carrying Fire in the Hands** (`dangerous`): Both involve applying an open flame to the body. Flagged as dangerous regardless of claimed safety preparations.
- **Invisible Writing Revealed** (`playable_now`): Lemon juice invisible ink is a widely practiced, safe household science experiment. Candle heat is used briefly from a safe distance.
- **Chinese Pictures Water Trick** (`craftable`): The modern explanation uses wax-resist watercolor — standard art materials. The original Victorian method may have used chemical solutions, but the modern equivalent is safe.
- **The Fifteen Puzzle** (`easy_to_source`): The 15-tile sliding puzzle is still manufactured and widely sold.
- **Reversi/Othello** (`easy_to_source`): Othello sets are widely available; can also be made from cardboard.
- **Towers of Hanoi** (`craftable`): The stacked discs can be made from cardboard circles of graduated sizes.