#!/usr/bin/env python3
"""
Heritage Parlor Game Database Audit
Task 1: Playability / Equipment Tier
Task 2: Illustration Source Mapping
"""

import json

with open('/home/user/workspace/heritage_parlor/data/entries.json') as f:
    data = json.load(f)

# ============================================================
# CLASSIFICATION LOGIC
# ============================================================

# Books that have illustrations
ILLUSTRATED_BOOKS = {
    "Modern Magic",
    "The Magician's Own Book",
    "Hoffmann's Puzzles Old and New",
    "Cassell's Book of In-door Amusements, Card Games, and Fireside Fun",
    "Every Boy's Book",
    "The Sociable",
}

# ============================================================
# PLAYABILITY CLASSIFICATION
# Based on equipment_needed + original_description + modern_explanation
# ============================================================

# Equipment that is clearly common household / no-equipment
HOUSEHOLD_ITEMS = {
    '', 'paper', 'pencils', 'pencil', 'coins', 'coin', 'chairs', 'chair',
    'table', 'handkerchief', 'knotted handkerchief', 'soft ball or knotted handkerchief',
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
    'pianist or musician', 'rice paper', 'tissue paper', 'paper disc with holes',
    'paper cylinder', 'cardboard', '2 cardboard tubes', 'playing card',
    '3 playing cards', 'beaded necklace', 'dried wishbone from poultry',
    'small bread roll', 'small plate or disc', 'damp hands', 'glue',
    'lemon juice', 'paper pellets', 'pocket watch',  # pocket watch is borderline
    'magic wand or pencil',  # a pencil works
    'blown egg', 'elder branch', 'cherry on string', 'lamp',
    'score pad', 'white sheet',  # for shadow/silhouette games
}

# Easy to buy at a general store or online
EASY_TO_SOURCE = {
    'standard deck of cards', 'standard deck', 'deck of cards',
    'standard deck (ace to 9)', 'standard deck minus one card',
    'standard deck or snap deck', 'standard deck with one queen removed',
    'arranged deck of cards', 'duplicate card', 'two identical playing cards',
    '18 labeled cards', 'marked coin', 'special double-faced coin',
    'dice', '3 dice', '4 dice', '2 dice cups',
    'dominoes', '28-tile double-six domino set', 'standard domino set',
    'chess pieces', 'chess board', 'chessboard', 'chess clock (optional)',
    'chess notation', 'small chessboard or paper grid', 'chessboard or paper grid',
    '8x8 board', 'draughts board',
    'backgammon board', 'cribbage board', 'cribbage board with pegs',
    'score track 1-100 (or paper)',  # can be made
    'chips', 'chips or counters', 'poker chips', 'betting chips',
    '10 coins', '10 tokens', '13 tokens', '20 tokens', '24 tokens',
    '8 tokens', '9 tokens', '8 numbered tokens', '9 numbered counters',
    '4 counters', 'counters', '13 geese pieces', '1 fox piece',
    '24 pieces in two colors', '30 pieces (15 per player)',
    '9 pieces each', 'pieces', 'pieces in up to 4 colors',
    '64 two-sided discs in black and white',  # othello discs
    '9 arrows or tokens', '20+ small objects',
    'shuttlecock', 'battledore paddles',
    'compass', 'wooden dowel',
    'balance scales',  # still available
    'metal plate or coin',  # any metal disc works
}

# Things that can be crafted / drawn
CRAFTABLE = {
    'drawn track', 'paper grid', '3×3 grid',  # can draw
    'fox and geese board',  # can draw on paper
    'morris board',  # can draw on paper
    'lotto cards',  # can make
    '15-tile sliding puzzle',  # can make with paper/cardboard
    '16x16 halma board',  # can draw
    'stacked discs', 'stacked tokens',
    'leather strip with slits',  # craftable
    'cloth tube', 'paper strip',
    'small whistle',  # craftable with elder branch (mentioned in entries)
}

# Specialty items - available but need specific shopping
SPECIALTY = {
    'linking rings',  # magic shop
    'top hat',  # costume shop
    'cup and ball toy', 'cup-and-ball toy',  # magic/toy shop
    'set of 8 metal rings',  # magic shop
    'small magic mill toy',  # specialty toy
    'prop sword or letter knife',  # prop shop
    'lemon juice',  # household actually...
    'surgical spirit',  # pharmacy
    'treated sand',  # specialty
    'metal funnel',  # hardware store
    'fine wire',  # hardware store
    'beaded necklace',  # craft store
    'punch and judy puppets',  # specialty toy
    '5 knucklebones or jacks', '5 knucklebones or modern jacks',  # toy shop
    'spelican set or straws', 'set of spelicans',  # specialty
    'special bottle and glass',  # magic supply
    'specially divided bottle',  # magic supply
    'hidden battery circuit',  # electronics hobby
    '2 large final loads',  # magic supply
    'birdcage or cup',  # magic supply
    'small hidden object',  # any small object
    'rice paper',  # craft/art store
    'tissue paper',  # available
    'pocket watch',  # specialty (not common anymore)
    'shilling',  # old coin - specialty/collectible
}

# Specific card game decks that are specialty
SPECIALTY_CARD_DECKS = {
    '24-card euchre deck (9 through ace, 4 suits)',  # euchre decks available
    '32-card piquet deck', '32-card piquet deck (7 through ace in 4 suits)',
    '64-card double piquet deck',  # uncommon
    '128-card quad piquet deck (4 x 32 cards)',  # very uncommon
    '40-card spanish deck (remove 8s, 9s, 10s from standard deck)',  # can be made from standard deck
    '48-card deck (remove 8 of diamonds)',  # can be made from standard deck
    'authors illustrated card set',  # can be found
    'happy families illustrated card set',  # can be found
}

# Extinct / Victorian manufactured items no longer available
EXTINCT = {
    '15-tile sliding puzzle',  # Actually these ARE still made, keep as craftable
    'pope joan board',  # very specific Victorian game board
    'faro layout board',  # specific gambling board, historical
    'betting layout',  # faro betting table
    'draw bag',  # part of faro setup
}

# Chemical / dangerous items
DANGEROUS_ITEMS = {
    'chemical solutions', 'surgical spirit',
}

# ============================================================
# SOURCE BOOK ILLUSTRATION MAPPING
# ============================================================

def get_book_short(source_book):
    if 'Modern Magic' in source_book:
        return 'Modern Magic'
    elif 'Magician' in source_book:
        return "The Magician's Own Book"
    elif 'Hoffmann' in source_book or 'Puzzles Old and New' in source_book:
        return "Hoffmann's Puzzles Old and New"
    elif "Cassell" in source_book:
        return "Cassell's Book of In-door Amusements"
    elif 'Every Boy' in source_book:
        return "Every Boy's Book"
    elif 'Sociable' in source_book:
        return "The Sociable"
    elif 'Canterbury' in source_book:
        return "The Canterbury Puzzles"
    elif 'Amusements in Mathematics' in source_book:
        return "Amusements in Mathematics"
    elif 'Foster' in source_book:
        return "Foster's Complete Hoyle"
    elif 'My Book of Indoor Games' in source_book:
        return "My Book of Indoor Games"
    return source_book

def classify_playability(entry):
    """Return (tier, note)"""
    equip = [e.lower().strip() for e in entry.get('equipment_needed', [])]
    desc = (entry.get('original_description', '') + ' ' + 
            entry.get('modern_explanation', '') + ' ' +
            entry.get('title', '')).lower()
    category = entry.get('category', '')
    subcategory = entry.get('subcategory', '')
    
    # Check for dangerous first
    dangerous_keywords = [
        'phosphor', 'acid', 'sulphuric', 'sulfuric', 'mercury', 'arsenic',
        'potassium', 'sodium metal', 'chlorine', 'nitric', 'cyanide',
        'prussic', 'oxalic', 'fire-eating', 'fire eating', 'chew and swallow glowing fire',
        'swallow fire', 'burning cotton', 'inflammable', 'burning alcohol',
        'naptha', 'naphtha'
    ]
    equip_dangerous = ['chemical solutions']
    
    # Check for dangerous chemicals in description
    for kw in dangerous_keywords:
        if kw in desc:
            return ('dangerous', f'Involves {kw} - chemical hazard')
    for eq in equip:
        if eq in equip_dangerous:
            return ('dangerous', 'Requires chemical solutions - hazardous')
    
    # Check for specifically extinct Victorian manufactured items
    # These are specific manufactured puzzles/devices
    extinct_checks = {
        'pick-me-up': 'The Pick-Me-Up Puzzle - specific Victorian brass cylinder puzzle',
        'planet puzzle': 'The Planet Puzzle - specific Victorian tray with planetary orbits',
        'magic mill': 'Magic Mill toy - specific Victorian manufactured toy',
        'small magic mill': 'Magic Mill toy - specific Victorian manufactured toy',
        'pope joan board': 'Pope Joan board - specific Victorian gambling board',
        'faro layout': 'Faro layout board - specific Victorian gambling equipment',
        'faro dealing': 'Faro dealing box - specific Victorian gambling equipment',
        'spelican': 'Spelican set - specific Victorian game of delicate ivory/wooden sticks',
    }
    
    for kw, note in extinct_checks.items():
        if kw in desc:
            return ('extinct_equipment', note)
    
    for eq in equip:
        if 'pope joan' in eq:
            return ('extinct_equipment', 'Pope Joan board - specific Victorian board no longer manufactured')
        if 'faro' in eq:
            return ('extinct_equipment', 'Faro layout/dealing box - specific Victorian gambling equipment')
        if 'spelican' in eq:
            return ('extinct_equipment', 'Spelican set - specific Victorian manufactured game of delicate sticks')
        if 'small magic mill' in eq:
            return ('extinct_equipment', 'Magic Mill toy - specific Victorian manufactured mechanical toy')
        if 'hidden battery circuit' in eq:
            return ('specialty_needed', 'Requires a concealed electrical battery circuit - Victorian electrical apparatus')
        if 'treated sand' in eq:
            return ('specialty_needed', 'Requires chemically treated sand')
        if 'specially divided bottle' in eq:
            return ('extinct_equipment', 'Specially divided bottle - specific Victorian magic apparatus')
        if 'special bottle and glass' in eq:
            return ('extinct_equipment', 'Special bottle and glass - specific Victorian magic apparatus')
        if '2 large final loads' in eq:
            return ('specialty_needed', 'Magic "loads" - sleight of hand apparatus, available from magic suppliers')
        if 'birdcage' in eq and 'magic' in desc:
            return ('specialty_needed', 'Collapsible birdcage - magic trick apparatus, available from magic suppliers')
        if 'punch and judy puppets' in eq:
            return ('specialty_needed', 'Punch and Judy puppet set - specialty theatrical puppets')
        if 'linking rings' in eq:
            return ('specialty_needed', 'Linking rings - magic trick apparatus, available from magic suppliers')
        if 'set of 8 metal rings' in eq:
            return ('specialty_needed', 'Set of 8 metal rings - magic trick apparatus, available from magic suppliers')
        if 'cup-and-ball' in eq or 'cup and ball' in eq:
            return ('specialty_needed', 'Cup and ball toy - available from magic/toy suppliers')
        if 'batting layout' in eq or 'betting layout' in eq:
            return ('extinct_equipment', 'Faro/casino betting layout table - Victorian gambling equipment')
        if 'draw bag' in eq and 'faro' in desc:
            return ('extinct_equipment', 'Faro draw bag - specific Victorian gambling apparatus')
    
    # Check for craftable items (items that need a drawn board)
    if 'fox and geese board' in equip:
        return ('craftable', 'Fox and geese board - can be drawn on paper')
    if 'morris board' in equip:
        return ('craftable', 'Morris board - can be drawn on paper')
    if '16x16 halma board' in equip:
        return ('craftable', 'Halma board - can be drawn on paper or purchased')
    if 'lotto cards' in equip:
        return ('craftable', 'Lotto cards - can be made from paper')
    if 'leather strip with slits' in equip:
        return ('craftable', 'Leather strip with slits - simple craft')
    if 'stacked discs' in equip or 'stacked tokens' in equip:
        return ('craftable', 'Can be made from paper/cardboard discs')
    if 'drawn track' in equip:
        return ('craftable', 'Game track - can be drawn on paper')
    
    # Check for specialty items that need shopping
    specialty_equip = {
        'top hat': 'Top hat - costume/theatrical supply',
        'pocket watch': 'Pocket watch - antique/specialist',
        'rice paper': 'Rice paper - art/craft supply',
        'fine wire': 'Fine wire - hardware store',
        'metal funnel': 'Metal funnel - hardware store',
        'small whistle': 'Small whistle - craft or music store',
    }
    for eq in equip:
        for sp_key, sp_note in specialty_equip.items():
            if sp_key in eq:
                return ('specialty_needed', sp_note)
    
    # Check for easy to source
    easy_equip_keywords = [
        'deck of cards', 'standard deck', 'playing card', 'arranged deck',
        'duplicate card', 'two identical', 'marked coin',
        'chess', 'draughts', 'checkers', 'backgammon', 'cribbage', 'dominoes',
        'dice', 'chips', 'poker', 'betting chip',
        'shuttlecock', 'battledore',
        'snap deck', 'euchre deck', 'piquet deck', 'spanish deck',
        '48-card', 'lotto', 'happy families', 'authors',
        'balance scales', 'compass',
    ]
    for eq in equip:
        for kw in easy_equip_keywords:
            if kw in eq:
                return ('easy_to_source', f'Requires {eq}')
    
    # Check for "special double-faced coin" - needs magic supplier
    for eq in equip:
        if 'double-faced coin' in eq or 'double faced coin' in eq:
            return ('specialty_needed', 'Special double-faced coin - magic supplier item')
    
    # Check for card game specific decks
    for eq in equip:
        if 'piquet deck' in eq:
            return ('easy_to_source', f'Piquet deck - available from card game suppliers or configurable from standard deck')
        if '40-card spanish' in eq or 'spanish deck' in eq:
            return ('craftable', 'Spanish deck - remove specific cards from standard deck')
        if '48-card' in eq:
            return ('craftable', 'Modified deck - remove one card from standard deck')
        if 'euchre deck' in eq:
            return ('easy_to_source', 'Euchre deck - available or configurable from standard deck')
    
    # Special board games that need specific boards
    for eq in equip:
        if 'halma board' in eq:
            return ('craftable', 'Halma board - can be drawn on paper or purchased online')
        if 'fox and geese' in eq:
            return ('craftable', 'Fox and geese board - can be drawn on paper')
        if 'morris' in eq:
            return ('craftable', 'Morris board - can be drawn on paper')
        if '3×3 grid' in eq or 'paper grid' in eq or 'drawn track' in eq:
            return ('craftable', f'{eq} - can be drawn on paper')
        if 'chessboard or paper grid' in eq or 'small chessboard or paper grid' in eq:
            return ('craftable', 'Can be drawn on paper')
    
    # If we get here, check if all equipment is household
    if not equip or all(eq in HOUSEHOLD_ITEMS or eq == '' for eq in equip):
        return ('playable_now', '')
    
    # Check for mixed equipment
    non_household = [eq for eq in equip if eq not in HOUSEHOLD_ITEMS and eq != '']
    if not non_household:
        return ('playable_now', '')
    
    # If remaining equipment is not classified, make a judgment call
    remaining = ', '.join(non_household)
    
    # Surgical spirit - it's a chemical/alcohol but available
    if 'surgical spirit' in non_household:
        return ('dangerous', 'Uses surgical spirit (rubbing alcohol) for fire effects - fire hazard')
    
    return ('playable_now', f'Needs: {remaining}')


def classify_illustration(entry):
    """Return (approach, note)"""
    source = entry.get('source_book', '')
    category = entry.get('category', '')
    subcategory = entry.get('subcategory', '')
    title = entry.get('title', '')
    desc = (entry.get('original_description', '') + ' ' + 
            entry.get('modern_explanation', '')).lower()
    
    book_short = get_book_short(source)
    has_illustrations = book_short in ILLUSTRATED_BOOKS
    
    # Determine if this type of entry would likely have had an illustration
    # Categories that typically have illustrations:
    # - magic-trick (apparatus, hand positions)
    # - puzzle (diagrams)
    # - board-game (board layout)
    # - physical-game (setup/formation)
    
    # Categories typically text-sufficient:
    # - word-game (verbal, no visual)
    # - most parlor-game subcategories (acting, guessing, forfeits)
    
    text_sufficient_categories = {'word-game'}
    text_sufficient_subcategories = {
        'acting-game', 'memory-game', 'guessing-game', 'forfeits',
        'verbal-game', 'singing-game', 'number-game', 'riddle',
        'story-game', 'question-answer', 'circle-game', 'truth-game',
        'pencil-game',  # these have diagrams usually
    }
    
    # Word games are always text sufficient
    if category == 'word-game':
        return ('text_sufficient', 'Word/verbal game needs no illustration')
    
    # Math puzzles from Amusements in Mathematics or Canterbury Puzzles
    if book_short in {'Amusements in Mathematics', 'The Canterbury Puzzles'}:
        # Some have diagrams, some are pure math
        if any(kw in desc for kw in ['draw', 'diagram', 'board', 'grid', 'figure', 'arrange', 'cut', 'dissect', 'map', 'puzzle piece']):
            if has_illustrations:
                return ('has_original', 'Puzzle likely has diagram in source book')
            else:
                return ('needs_generated', 'Puzzle diagram would help but source has no illustrations')
        else:
            return ('text_sufficient', 'Mathematical puzzle, no diagram needed')
    
    # Magic tricks always have apparatus illustrations in illustrated books
    if category == 'magic-trick':
        if has_illustrations:
            return ('has_original', 'Magic trick apparatus/technique illustrated in source book')
        else:
            return ('needs_generated', 'Magic trick would benefit from apparatus illustration')
    
    # Board games always need board illustrations
    if category == 'board-game':
        if has_illustrations:
            return ('has_original', 'Board game layout illustrated in source book')
        else:
            return ('needs_generated', 'Board game layout illustration needed')
    
    # Puzzles - depends on type
    if category == 'puzzle':
        if has_illustrations:
            return ('has_original', 'Puzzle diagram illustrated in source book')
        else:
            # Pure math puzzles may not need illustration
            if any(kw in desc for kw in ['shillings', 'pounds', 'money', 'ages', 'numbers', 'calculate', 'arithmetic', 'legacy', 'apples', 'cyclists']):
                return ('text_sufficient', 'Mathematical/arithmetic puzzle, text sufficient')
            return ('needs_generated', 'Puzzle would benefit from a diagram')
    
    # Card games
    if category == 'card-game':
        if has_illustrations:
            return ('has_original', 'Card game illustrated in source book')
        else:
            # Simple card games don't need illustrations
            return ('text_sufficient', 'Card game rules are text sufficient')
    
    # Physical games
    if category == 'physical-game':
        if has_illustrations:
            return ('has_original', 'Physical game formation/setup illustrated in source book')
        else:
            return ('needs_generated', 'Physical game would benefit from formation diagram')
    
    # Parlor games - mostly text sufficient, but some need illustration
    if category == 'parlor-game':
        if subcategory in text_sufficient_subcategories:
            return ('text_sufficient', 'Parlor game is verbal/acting, no illustration needed')
        # Special parlor games with apparatus
        if any(kw in desc for kw in ['apparatus', 'trick', 'mechanism', 'device', 'puppet', 'shadow']):
            if has_illustrations:
                return ('has_original', 'Parlor trick/apparatus illustrated in source book')
            else:
                return ('needs_generated', 'Parlor trick apparatus would benefit from illustration')
        if has_illustrations:
            return ('has_original', 'Parlor game illustrated in source book')
        return ('text_sufficient', 'Parlor game can be explained with text alone')
    
    # Default
    if has_illustrations:
        return ('has_original', 'Source book contains illustrations')
    return ('text_sufficient', 'Entry can be understood from text alone')


# ============================================================
# RUN THE AUDIT
# ============================================================

audit = []

for entry in data:
    play_tier, play_note = classify_playability(entry)
    illus_approach, illus_note = classify_illustration(entry)
    
    audit_entry = {
        "id": entry["id"],
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

# Save audit.json
with open('/home/user/workspace/heritage_parlor/data/audit.json', 'w') as f:
    json.dump(audit, f, indent=2)

print(f"Saved {len(audit)} entries to audit.json")

# ============================================================
# SUMMARY STATS
# ============================================================
from collections import Counter, defaultdict

play_counts = Counter(a['playability'] for a in audit)
illus_counts = Counter(a['illustration'] for a in audit)

print("\n=== PLAYABILITY ===")
for tier, count in sorted(play_counts.items(), key=lambda x: -x[1]):
    print(f"  {tier}: {count}")

print("\n=== ILLUSTRATION ===")
for approach, count in sorted(illus_counts.items(), key=lambda x: -x[1]):
    print(f"  {approach}: {count}")

print("\n=== EXTINCT EQUIPMENT ===")
for a in audit:
    if a['playability'] == 'extinct_equipment':
        print(f"  {a['title']}: {a['playability_note']}")

print("\n=== DANGEROUS ===")
for a in audit:
    if a['playability'] == 'dangerous':
        print(f"  {a['title']}: {a['playability_note']}")
