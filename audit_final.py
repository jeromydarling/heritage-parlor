#!/usr/bin/env python3
"""
Heritage Parlor Game Database Audit - Final Version
Task 1: Playability / Equipment Tier
Task 2: Illustration Source Mapping
"""

import json
from collections import Counter, defaultdict

with open('/home/user/workspace/heritage_parlor/data/entries.json') as f:
    data = json.load(f)

# ============================================================
# ILLUSTRATED BOOKS
# ============================================================
ILLUSTRATED_BOOKS = {
    "Modern Magic",
    "The Magician's Own Book",
    "Hoffmann's Puzzles Old and New",
    "Cassell's Book of In-door Amusements, Card Games, and Fireside Fun",
    "Every Boy's Book",
    "The Sociable",
}

def get_book_short(source_book):
    if 'Modern Magic' in source_book:
        return 'Modern Magic'
    elif "Magician's Own" in source_book or 'Magicians Own' in source_book:
        return "The Magician's Own Book"
    elif 'Hoffmann' in source_book or 'Puzzles Old and New' in source_book:
        return "Hoffmann's Puzzles Old and New"
    elif "Cassell" in source_book:
        return "Cassell's Book of In-door Amusements, Card Games, and Fireside Fun"
    elif 'Every Boy' in source_book:
        return "Every Boy's Book"
    elif 'Sociable' in source_book:
        return "The Sociable"
    return source_book

# ============================================================
# COMMON HOUSEHOLD ITEMS (playable_now)
# ============================================================
HOUSEHOLD_ITEMS = {
    'paper', 'pencils', 'pencil', 'coin', 'coins', 'chairs', 'chair', 'table',
    'handkerchief', 'knotted handkerchief', 'soft ball or knotted handkerchief',
    'blindfold', 'string', 'button', 'candle', 'scissors', 'water', 'glass of water',
    'empty glass', 'wine glass', 'newspaper', 'cloth', 'ring', 'finger ring',
    'small hidden object', 'small object', 'various small objects',
    'optional costumes', 'costumes', 'props', 'paper strips', 'paper strip',
    'paper sheets', 'paper to track amounts', 'paper grid', 'stiff paper',
    'stiff paper or card', 'slate or paper', 'chalk or charcoal', 'chalk or pencil',
    'small coin or pebble', 'ruler', 'slipper', 'cushion or hassock',
    'tokens', 'numbered tokens', 'matchsticks or counters',
    'small weights', 'eggs', 'bowl', 'ball or knotted cloth', 'rubber ball',
    'small balls', '4 small balls', 'large feather', 'tray', 'cup or cover',
    '3 cups', 'cloth bag', 'long cord', 'cord', 'long string or cord',
    'loop of string about 1m long', 'two loops of string', 'dark thread',
    'fine thread', 'orange', 'stamps', 'bell', 'broomstick', 'stick or staff',
    'stick or wand', 'thin stick or taper', 'music', 'piano', 'piano or instrument',
    'pianist or musician', 'tissue paper', 'paper disc with holes',
    'paper cylinder', '2 cardboard tubes', 'playing card',
    '3 playing cards', 'dried wishbone from poultry',
    'small bread roll', 'small plate or disc', 'damp hands', 'glue',
    'lemon juice', 'magic wand or pencil',
    'blown egg', 'cherry on string', 'lamp',
    'score pad', 'white sheet', 'candle heat',
    'red vegetable juice or dye', 'paper pellets', 'stiff paper',
    '10 coins', '13 tokens', '20 tokens', '24 tokens',
    '8 tokens', '9 tokens', '8 numbered tokens', '9 numbered counters',
    '4 counters', '13 geese pieces', '1 fox piece', '9 arrows or tokens',
    '10 tokens', '18 labeled cards',
    'knotted handkerchief', 'soft ball or knotted handkerchief',
    'long cord', 'ring or thimble',
    'weighted bottles',  # bottles filled with water/sand
    'beaded necklace',   # common jewelry
    'long string or cord',
}

def classify_playability(entry):
    """Return (tier, note)"""
    equip_raw = entry.get('equipment_needed', [])
    equip = [e.lower().strip() for e in equip_raw]
    desc = (entry.get('original_description', '') + ' ' + 
            entry.get('modern_explanation', '') + ' ' +
            entry.get('title', '')).lower()
    category = entry.get('category', '')
    entry_id = entry.get('id', '')

    # ---- DANGEROUS FIRST ----
    # Fire eating: swallowing fire - genuinely dangerous
    # Carrying fire in hands: open flame on skin
    # Chinese pictures: chemical solutions
    # Invisible writing: lemon juice + candle heat - borderline, but candle near paper is fire risk
    dangerous_ids = {
        'fire-eating',
        'carrying-fire-in-the-hands',
    }
    if entry_id in dangerous_ids:
        return ('dangerous', 'Open flame / fire-swallowing stunt — serious burn risk')

    # Chemical solutions equipment
    for eq in equip:
        if eq == 'chemical solutions':
            return ('dangerous', 'Requires unspecified chemical solutions — hazard unclear but flagged')
        if eq == 'surgical spirit' and 'fire' in desc:
            return ('dangerous', 'Burns surgical spirit (alcohol) on skin — fire hazard')

    # Check lemon juice + candle — this is a mild fire risk but very common magic trick
    # We'll classify it as specialty_needed due to open flame requirement, not dangerous
    if entry_id == 'invisible-writing-revealed':
        return ('playable_now', 'Lemon juice invisible ink — common household science experiment')

    # ---- EXTINCT EQUIPMENT ----
    # Specific Victorian manufactured items that no longer exist

    extinct_map = {
        'specially divided bottle': ('extinct_equipment', 'Specially divided bottle — Victorian magic apparatus with internal chambers, no modern equivalent'),
        'special bottle and glass': ('extinct_equipment', 'Special bottle and glass set — Victorian magic apparatus, custom-made for the trick'),
        'pope joan board': ('extinct_equipment', 'Pope Joan board — specific Victorian circular gambling board with labeled compartments, no longer manufactured'),
        'faro layout board': ('extinct_equipment', 'Faro layout board — specific Victorian casino gambling table layout, obsolete'),
        'betting layout': ('extinct_equipment', 'Faro/casino betting layout — Victorian gambling equipment, obsolete'),
        'small magic mill toy': ('extinct_equipment', 'The Magic Mill toy — specific Victorian manufactured mechanical toy, extinct'),
    }

    for eq in equip:
        if eq in extinct_map:
            return extinct_map[eq]
        if 'spelican' in eq:
            return ('extinct_equipment', 'Spelican set — Victorian game of slender ivory/bone sticks requiring precision manufacturing; pick-up sticks are a rough modern equivalent but the authentic spelican set is extinct')
        if 'faro' in eq or 'faro' in desc:
            if eq in ('faro layout board', 'betting layout', 'draw bag') or 'faro' in entry_id:
                return ('extinct_equipment', 'Faro dealing box and layout board — specific Victorian gambling apparatus, obsolete')

    # The Magic Mill Trick (paper folding trick, not the toy)
    if entry_id == 'the-magic-mill-trick':
        return ('playable_now', 'Paper strip folded and dropped — common household materials')

    # ---- SPECIALTY NEEDED ----
    specialty_map = {
        'linking rings': ('specialty_needed', 'Linking rings — magic trick apparatus; available from magic suppliers'),
        'set of 8 metal rings': ('specialty_needed', 'Set of 8 metal linking rings — magic trick apparatus; available from magic suppliers'),
        'top hat': ('specialty_needed', 'Top hat — theatrical/costume item; rentable or purchasable from costume shops'),
        'treated sand': ('specialty_needed', 'Chemically treated sand — prepared magic prop; available from magic suppliers or DIY'),
        'hidden battery circuit': ('specialty_needed', 'Concealed battery circuit — Victorian electrical apparatus; modern equivalent possible with basic electronics'),
        '2 large final loads': ('specialty_needed', 'Magic "loads" (hidden bundles) — sleight of hand apparatus; available from magic suppliers'),
        'birdcage or cup': ('specialty_needed', 'Collapsible birdcage — magic trick prop; available from magic suppliers'),
        'punch and judy puppets': ('specialty_needed', 'Punch and Judy puppet set — specialist theatrical puppets; purchasable from puppet suppliers'),
        'cup and ball toy': ('specialty_needed', 'Cup and ball toy — available from magic/toy suppliers'),
        'cup-and-ball toy': ('specialty_needed', 'Cup-and-ball (bilboquet) — available from toy and magic suppliers'),
        'special double-faced coin': ('specialty_needed', 'Double-faced coin — magic trick prop; available from magic suppliers'),
        'metal funnel': ('specialty_needed', 'Metal funnel — hardware/kitchen store item'),
        'rice paper': ('specialty_needed', 'Rice paper — available from art/craft suppliers'),
        'small whistle': ('specialty_needed', 'Small whistle — available from toy/craft stores'),
        'pocket watch': ('specialty_needed', 'Pocket watch — antique/specialist item; less common today'),
        'fine wire': ('specialty_needed', 'Fine wire — hardware/craft store item'),
    }

    for eq in equip:
        if eq in specialty_map:
            return specialty_map[eq]

    # Prop sword
    for eq in equip:
        if 'prop sword' in eq:
            return ('specialty_needed', 'Prop sword / letter knife — theatrical prop or novelty item')

    # ---- CRAFTABLE ----
    craftable_map = {
        'fox and geese board': ('craftable', 'Fox and geese board — draw on paper or cardboard'),
        'morris board': ('craftable', 'Nine Men\'s Morris board — draw on paper or cardboard'),
        '16x16 halma board': ('craftable', 'Halma board — draw on large paper or cardboard'),
        'lotto cards': ('craftable', 'Lotto/bingo cards — make from paper'),
        'leather strip with slits': ('craftable', 'Leather strip with slits — simple craft from any strip of card/leather'),
        'drawn track': ('craftable', 'Game track — draw on paper'),
        '3×3 grid': ('craftable', 'Grid — draw on paper'),
        'stacked discs': ('craftable', 'Stacked discs — make from paper/cardboard'),
        'stacked tokens': ('craftable', 'Stacked tokens — make from paper/cardboard'),
    }

    for eq in equip:
        if eq in craftable_map:
            return craftable_map[eq]
        if 'paper grid' in eq and eq not in HOUSEHOLD_ITEMS:
            return ('craftable', 'Grid — draw on paper')
        if 'halma board' in eq:
            return ('craftable', 'Halma board — draw on large paper')
        if '3×3' in eq or 'grid' in eq:
            return ('craftable', f'{eq} — draw on paper')

    # ---- EASY TO SOURCE ----
    easy_keywords = [
        ('standard deck', 'Standard 52-card deck — widely available'),
        ('deck of cards', 'Standard card deck — widely available'),
        ('playing card', 'Standard playing cards — widely available'),
        ('arranged deck', 'Standard deck arranged in a specific order — widely available'),
        ('duplicate card', 'Standard deck with duplicate card — widely available'),
        ('two identical playing cards', 'Standard playing cards — widely available'),
        ('marked coin', 'Any coin marked with a scratch — household'),
        ('chess board', 'Chess set — widely available'),
        ('chess pieces', 'Chess set — widely available'),
        ('chessboard', 'Chess set — widely available'),
        ('draughts board', 'Draughts/checkers set — widely available'),
        ('backgammon board', 'Backgammon set — widely available'),
        ('cribbage board', 'Cribbage board — available at game stores'),
        ('domino', 'Domino set — widely available'),
        ('dice', 'Dice — widely available'),
        ('chips', 'Poker chips or coins — widely available'),
        ('poker chips', 'Poker chips — widely available'),
        ('betting chips', 'Chips/counters — widely available'),
        ('score track', 'Score track — can be made on paper or purchased'),
        ('balance scales', 'Balance scales — available from educational/kitchen suppliers'),
        ('compass', 'Drawing compass — available from stationery shops'),
        ('euchre deck', 'Euchre deck — configure from standard deck or buy'),
        ('piquet deck', 'Piquet deck — configure from standard deck or buy'),
        ('spanish deck', 'Spanish deck — remove cards from standard deck'),
        ('48-card deck', 'Modified deck — remove one card from standard deck'),
        ('64-card', 'Double piquet deck — two standard decks combined'),
        ('128-card', 'Four piquet decks — buy or combine standard decks'),
        ('happy families', 'Happy Families card set — available from game stores'),
        ('authors', 'Authors card set — available from game stores'),
        ('standard domino set', 'Standard domino set — widely available'),
        ('battledore', 'Battledore and shuttlecock — available from sports/toy stores'),
        ('shuttlecock', 'Shuttlecock — available from sports/toy stores'),
        ('8x8 board', 'Chess/checkerboard — widely available'),
        ('64 two-sided discs', 'Othello/Reversi set — widely available'),
        ('24 pieces in two colors', 'Draughts/checkers pieces — widely available'),
        ('30 pieces', 'Backgammon pieces — widely available'),
    ]

    for eq in equip:
        for kw, note in easy_keywords:
            if kw in eq:
                return ('easy_to_source', note)

    # Knucklebones/jacks
    for eq in equip:
        if 'knucklebones' in eq or 'jacks' in eq:
            return ('easy_to_source', 'Jacks set — available from toy stores; traditional knucklebones from butcher')

    # 5 knucklebones
    if '5 knucklebones or jacks' in equip or '5 knucklebones or modern jacks' in equip:
        return ('easy_to_source', 'Jacks set — available from toy stores; traditional knucklebones from butcher')

    # ---- DEFAULT: check if all household ----
    non_household = [eq for eq in equip if eq not in HOUSEHOLD_ITEMS and eq != '']
    if not non_household:
        return ('playable_now', '')

    # Anything not caught: check for obvious household
    # Reversi: 8x8 board + 64 two-sided discs caught above
    # If we're here, make a judgment
    return ('playable_now', f'Minor equipment needed: {", ".join(non_household[:2])}')


def classify_illustration(entry):
    """Return (approach, note)"""
    source = entry.get('source_book', '')
    category = entry.get('category', '')
    subcategory = entry.get('subcategory', '')
    entry_id = entry.get('id', '')
    desc = (entry.get('original_description', '') + ' ' + 
            entry.get('modern_explanation', '')).lower()
    equip = [e.lower() for e in entry.get('equipment_needed', [])]

    book_short = get_book_short(source)
    has_illustrations = book_short in ILLUSTRATED_BOOKS

    # Word games are almost always text-sufficient
    if category == 'word-game':
        return ('text_sufficient', 'Verbal/written word game; no visual diagram needed')

    # Magic tricks — always benefit from illustration
    if category == 'magic-trick':
        if has_illustrations:
            return ('has_original', 'Magic trick apparatus and hand positions illustrated in source book')
        else:
            return ('needs_generated', 'Magic trick would benefit from apparatus/technique illustration')

    # Board games — always need board layout
    if category == 'board-game':
        if has_illustrations:
            return ('has_original', 'Board game layout illustrated in source book')
        else:
            return ('needs_generated', 'Board layout and setup needs illustration')

    # Card games — mostly text-sufficient (rules conveyed in text)
    if category == 'card-game':
        if has_illustrations:
            return ('has_original', 'Card game illustrated in source book')
        else:
            return ('text_sufficient', 'Card game rules are conveyed well in text alone')

    # Physical games
    if category == 'physical-game':
        if has_illustrations:
            return ('has_original', 'Physical game formation/positions illustrated in source book')
        else:
            return ('needs_generated', 'Physical game formation and positions would benefit from illustration')

    # Puzzles — depends heavily on type
    if category == 'puzzle':
        # Pure arithmetic/logic puzzles need no diagram
        pure_math_clues = [
            'shilling', 'pounds', 'money', 'ages', 'legacy', 'apples', 'cyclist',
            'farmer', 'merchant', 'widow', 'calculate', 'arithmetic', 'multiply',
            'rate', 'integer', 'prime', 'digit', 'remainder', 'divisor',
            'total', 'how many', 'what number', 'how much', 'proportion', 
            'percent', 'fraction', 'clock puzzle', 'river crossing',
            'sons get', 'daughters', 'miser', 'housekeeper'
        ]
        
        # Visual/spatial puzzles need diagram
        visual_clues = [
            'draw', 'diagram', 'figure', 'board', 'grid', 'arrange tokens',
            'cut', 'dissect', 'fold', 'map', 'piece', 'rearrange', 'permut',
            'sliding', 'tile', 'place tokens', 'move', 'connect', 'trace',
            'route', 'path', 'tour', 'queen', 'bishop', 'knight', 'chessboard',
            'counter', 'token', 'circle', 'square', 'garden', 'fence',
            'flower bed', 'web', 'spider', 'fly', 'shunting', 'mouse', 'cat',
            'cellarman', 'nun', 'pigs', 'pardoner', 'tapiser', 'weaver',
            'miller', 'sompnour', 'landlord', 'friar', 'monk', 'squire',
            'haberdasher', 'ploughman', 'half', 'penny', 'row',
            'column', 'magic square', 'position'
        ]
        
        is_visual = any(kw in desc for kw in visual_clues)
        is_math = any(kw in desc for kw in pure_math_clues) and not is_visual

        if is_math:
            return ('text_sufficient', 'Arithmetic/logic puzzle; no diagram needed')

        # Has source with illustrations
        if has_illustrations:
            return ('has_original', 'Puzzle diagram illustrated in source book')
        
        # Source without illustrations (Amusements in Math, Canterbury Puzzles)
        if is_visual:
            return ('needs_generated', 'Spatial/arrangement puzzle would benefit from a diagram')
        
        # Default for puzzles without clear type
        return ('needs_generated', 'Puzzle diagram or arrangement illustration would help')

    # Parlor games
    if category == 'parlor-game':
        # Subcategories that are purely verbal/social
        text_sufficient_subs = {
            'acting-game', 'guessing-game', 'whisper-game', 'memory-game',
            'mathematical-trick', 'mime-game', 'attention-game', 'forfeit-game',
            'solemn-face-game', 'seat-changing-game', 'calling-game',
            'quick-response-game', 'quick-reaction-game', 'social-game',
            'theatrical-game', 'role-play-game', 'secret-code-game', 'mentalism-game',
            'yes-no-game', 'knowledge-game', 'taboo-word-game', 'taboo-game',
            'wishing-game', 'kissing-game', 'logic-puzzle-game', 'hiding-game',
            'blindfold-game', 'circle-game', 'response-game', 'secret-trick',
            'drawing-game',
        }
        if subcategory in text_sufficient_subs:
            if has_illustrations:
                return ('has_original', 'Parlor game illustrated in source book')
            return ('text_sufficient', 'Social/acting parlor game; description is sufficient')

        # Special apparatus subcategories
        apparatus_subs = {'puppet-show'}
        if subcategory in apparatus_subs:
            if has_illustrations:
                return ('has_original', 'Puppet show illustrated in source book')
            return ('needs_generated', 'Puppet show performance needs visual illustration')

        # General parlor games
        if has_illustrations:
            return ('has_original', 'Parlor game illustrated in source book')
        
        # Check if apparatus/visual needed
        if any(kw in desc for kw in ['apparatus', 'trick', 'device', 'shadow', 'puppet', 'formation']):
            return ('needs_generated', 'Parlor activity with visual elements would benefit from illustration')
        
        return ('text_sufficient', 'Parlor game rules are conveyed well in text alone')

    # Fallback
    if has_illustrations:
        return ('has_original', 'Source book contains illustrations')
    return ('text_sufficient', 'Entry can be understood from text alone')


# ============================================================
# MANUAL OVERRIDES for edge cases identified in review
# ============================================================
MANUAL_PLAYABILITY_OVERRIDES = {
    # The Magic Mill Trick uses paper strip + scissors (not the magic mill toy)
    'the-magic-mill-trick': ('playable_now', 'Paper strip folding trick — common household materials only'),
    # Invisible writing: lemon juice + candle is a classic school experiment
    'invisible-writing-revealed': ('playable_now', 'Classic lemon juice invisible ink — household materials; use candle with normal fire safety'),
    # Dominoes block game: domino set is easy to source, not household
    'dominoes-block-game': ('easy_to_source', '28-tile double-six domino set — widely available'),
    # Reversi: Othello set is widely available
    'reversi-othello': ('easy_to_source', '8x8 board with two-sided discs — Othello/Reversi sets widely available; or make from cardboard'),
    # The Fifteen Puzzle: the sliding tile puzzle is still widely sold
    'the-fifteen-puzzle': ('easy_to_source', '15-tile sliding puzzle — still widely available as a toy/novelty'),
    # Faro: faro layout is extinct
    'faro': ('extinct_equipment', 'Faro layout board and dealing box — specific Victorian casino gambling apparatus, obsolete'),
    # Pope Joan board 
    'pope-joan': ('extinct_equipment', 'Pope Joan board — circular compartmentalized Victorian board game, no longer manufactured'),
    'pope-joan-full-rules': ('extinct_equipment', 'Pope Joan board — circular compartmentalized Victorian board game, no longer manufactured'),
    # Dice Chuck-a-Luck: betting layout is extinct
    'dice-chuck-a-luck': ('extinct_equipment', 'Chuck-a-Luck birdcage and betting layout — specific Victorian casino gambling apparatus'),
    # Spelicans entries
    'spelicans': ('extinct_equipment', 'Spelican set — Victorian ivory/bone stick game requiring precision manufacture; straws are a rough modern substitute but authentic spelicans are extinct'),
    'spelicans-pick-up-sticks': ('extinct_equipment', 'Spelican set — Victorian ivory/bone stick game; straws are a rough substitute but authentic spelicans are extinct'),
    # Chinese pictures: water + wax resist is actually fine, chemical solutions flag was the issue
    'chinese-pictures-water-trick': ('craftable', 'Wax-resist watercolor technique — materials from art/craft stores; original may have used more dangerous chemicals'),
    # Fire eating - use potassium alum + alcohol - genuinely dangerous
    'fire-eating': ('dangerous', 'Fire eating with burning alcohol on tongue — serious burn/fire risk, do not attempt'),
    # Carrying fire in hands - burning alcohol on skin
    'carrying-fire-in-the-hands': ('dangerous', 'Burning surgical spirit (alcohol) on hands — fire hazard; requires expert fire safety measures'),
    # The Electric Bell - hidden battery circuit - specialty
    'the-electric-bell': ('specialty_needed', 'Concealed battery circuit — Victorian electrical apparatus; modern equivalent needs basic electronics knowledge'),
}

MANUAL_ILLUSTRATION_OVERRIDES = {
    # Physical games from Cassell's and My Book of Indoor Games - no illustrations in those books
    # but they are physical movement games that benefit from diagrams
    'the-cushion-dance': ('needs_generated', 'Dance formation diagram would help'),
    'musical-chairs': ('needs_generated', 'Game formation illustration would help'),
    'going-to-jerusalem': ('needs_generated', 'Game formation illustration would help'),
    'blind-man-s-buff': ('needs_generated', 'Game formation illustration would help'),
    # Parlor games with shadow/silhouette elements
    'shadow-buff': ('needs_generated', 'Shadow/silhouette setup needs a diagram'),
}


# ============================================================
# RUN THE AUDIT
# ============================================================

audit = []

for entry in data:
    eid = entry['id']
    
    # Apply classification
    play_tier, play_note = classify_playability(entry)
    illus_approach, illus_note = classify_illustration(entry)
    
    # Apply manual overrides
    if eid in MANUAL_PLAYABILITY_OVERRIDES:
        play_tier, play_note = MANUAL_PLAYABILITY_OVERRIDES[eid]
    if eid in MANUAL_ILLUSTRATION_OVERRIDES:
        illus_approach, illus_note = MANUAL_ILLUSTRATION_OVERRIDES[eid]
    
    audit_entry = {
        "id": eid,
        "title": entry["title"],
        "category": entry["category"],
        "source_book": entry["source_book"],
        "equipment": entry.get("equipment_needed", []),
        "playability": play_tier,
        "playability_note": play_note,
        "illustration": illus_approach,
        "illustration_note": illus_note,
    }
    audit.append(audit_entry)

# ============================================================
# SAVE AUDIT JSON
# ============================================================
with open('/home/user/workspace/heritage_parlor/data/audit.json', 'w') as f:
    json.dump(audit, f, indent=2)

print(f"Saved {len(audit)} entries to audit.json")

# ============================================================
# COMPUTE SUMMARY STATS
# ============================================================
play_counts = Counter(a['playability'] for a in audit)
illus_counts = Counter(a['illustration'] for a in audit)

# By category
cat_play = defaultdict(Counter)
cat_illus = defaultdict(Counter)
for a in audit:
    cat_play[a['category']][a['playability']] += 1
    cat_illus[a['category']][a['illustration']] += 1

extinct_entries = [a for a in audit if a['playability'] == 'extinct_equipment']
dangerous_entries = [a for a in audit if a['playability'] == 'dangerous']

# ============================================================
# GENERATE SUMMARY MARKDOWN
# ============================================================
md = []
md.append("# Heritage Parlor Game Database — Audit Summary\n")
md.append(f"**Total entries audited:** {len(audit)}\n")

md.append("\n---\n")
md.append("## Task 1: Playability Audit\n")
md.append("### Counts by Playability Tier\n")
md.append("| Tier | Count |")
md.append("|------|-------|")
tier_order = ['playable_now', 'easy_to_source', 'craftable', 'specialty_needed', 'extinct_equipment', 'dangerous']
for tier in tier_order:
    cnt = play_counts.get(tier, 0)
    md.append(f"| `{tier}` | {cnt} |")

md.append("\n### Playability by Category\n")
md.append("| Category | playable_now | easy_to_source | craftable | specialty_needed | extinct_equipment | dangerous |")
md.append("|----------|-------------|----------------|-----------|-----------------|-------------------|-----------|")
for cat in sorted(cat_play.keys()):
    row = f"| {cat} |"
    for tier in tier_order:
        row += f" {cat_play[cat].get(tier, 0)} |"
    md.append(row)

md.append("\n---\n")
md.append("### All `extinct_equipment` Entries\n")
md.append("These entries require Victorian-era manufactured items that almost certainly no longer exist or cannot be reasonably replicated.\n")
for a in extinct_entries:
    md.append(f"- **{a['title']}** (`{a['id']}`)")
    md.append(f"  - Equipment: {a['equipment']}")
    md.append(f"  - Reason: {a['playability_note']}")

md.append("\n---\n")
md.append("### All `dangerous` Entries\n")
md.append("These entries involve fire, open flames, or chemical hazards.\n")
for a in dangerous_entries:
    md.append(f"- **{a['title']}** (`{a['id']}`)")
    md.append(f"  - Equipment: {a['equipment']}")
    md.append(f"  - Reason: {a['playability_note']}")

md.append("\n---\n")
md.append("## Task 2: Illustration Source Mapping\n")
md.append("### Counts by Illustration Approach\n")
md.append("| Approach | Count |")
md.append("|----------|-------|")
illus_order = ['has_original', 'text_sufficient', 'needs_generated']
for approach in illus_order:
    cnt = illus_counts.get(approach, 0)
    md.append(f"| `{approach}` | {cnt} |")

md.append("\n### Illustration by Category\n")
md.append("| Category | has_original | text_sufficient | needs_generated |")
md.append("|----------|-------------|-----------------|----------------|")
for cat in sorted(cat_illus.keys()):
    row = f"| {cat} |"
    for approach in illus_order:
        row += f" {cat_illus[cat].get(approach, 0)} |"
    md.append(row)

md.append("\n### Categories: Text-Sufficient vs. Illustration-Needed\n")
md.append("**Mostly text-sufficient categories:**")
md.append("- `word-game` — All verbal games; no diagrams needed")
md.append("- `card-game` — Card game rules convey well in text; Foster's Complete Hoyle has no illustrations")
md.append("- `parlor-game` — Most social/acting parlor games are text-sufficient\n")

md.append("**Mostly illustration-needed categories:**")
md.append("- `magic-trick` — All tricks benefit from apparatus/hand position diagrams")
md.append("- `board-game` — All need board layout diagrams")
md.append("- `puzzle` — Spatial/arrangement puzzles need diagrams; arithmetic puzzles are text-sufficient")
md.append("- `physical-game` — Formation/movement games benefit from diagrams\n")

md.append("### Source Books and Illustration Status\n")
book_counts = defaultdict(lambda: Counter())
for a in audit:
    book_counts[a['source_book']][a['illustration']] += 1

md.append("| Source Book | has_original | text_sufficient | needs_generated | Total |")
md.append("|-------------|-------------|-----------------|----------------|-------|")
for book in sorted(book_counts.keys()):
    counts = book_counts[book]
    total = sum(counts.values())
    row = f"| {book[:50]} |"
    for approach in illus_order:
        row += f" {counts.get(approach, 0)} |"
    row += f" {total} |"
    md.append(row)

md.append("\n---\n")
md.append("## Notes on Classification Decisions\n")
md.append("- **Spelicans**: Listed as `extinct_equipment`. While pick-up sticks (Mikado) are a rough modern equivalent, authentic Victorian spelicans were made from precise ivory or bone sticks with specific shapes, and the authentic set is extinct.\n")
md.append("- **Pope Joan board**: Listed as `extinct_equipment`. The Pope Joan board was a specific circular compartmentalized board used for the Victorian card game of the same name. It is no longer manufactured commercially.\n")
md.append("- **Faro**: Listed as `extinct_equipment`. Faro required a specific dealing box, layout cloth, and case keeper — all highly specialized Victorian gambling apparatus.\n")
md.append("- **The Magic Mill**: The Victorian manufactured mechanical mill toy is `extinct_equipment`. However, 'The Magic Mill Trick' (paper folding) is `playable_now` — these are two different entries.\n")
md.append("- **Fire Eating / Carrying Fire**: Listed as `dangerous`. Both involve open flames applied to the body.\n")
md.append("- **Invisible Writing**: Listed as `playable_now` — lemon juice invisible ink is a classic household science experiment widely done safely.\n")
md.append("- **Chinese Pictures Water Trick**: Listed as `craftable` — the wax-resist watercolor technique is safe using art materials; the original Victorian version may have used chemicals but the modern explanation uses craft materials.\n")
md.append("- **The Fifteen Puzzle**: Listed as `easy_to_source` — 15-tile sliding puzzles are still widely sold as toys.\n")
md.append("- **Reversi/Othello**: Listed as `easy_to_source` — Othello sets are widely available.\n")

with open('/home/user/workspace/heritage_parlor/data/audit_summary.md', 'w') as f:
    f.write('\n'.join(md))

print("Saved audit_summary.md")
print()
print("=== FINAL COUNTS ===")
print("\nPLAYABILITY:")
for tier in tier_order:
    print(f"  {tier}: {play_counts.get(tier, 0)}")
print("\nILLUSTRATION:")
for approach in illus_order:
    print(f"  {approach}: {illus_counts.get(approach, 0)}")
print("\nEXTINCT EQUIPMENT:")
for a in extinct_entries:
    print(f"  {a['title']}: {a['playability_note']}")
print("\nDANGEROUS:")
for a in dangerous_entries:
    print(f"  {a['title']}: {a['playability_note']}")
