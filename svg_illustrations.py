"""
Illustrated SVG thumbnails for non-diagram games.
Each illustration depicts the actual game being played with unique scene composition.
Uses subcategory, tags, and modern_explanation to differentiate every game.
"""
import math, json, os, hashlib, re

# Design tokens matching the site
bg = "#faf6f0"
ink = "#2a2118"
light = "#6b5d4f"
accent = "#8b4513"
muted = "#a89a8a"
cream = "#f5f0e6"
warm = "#e8ddd0"

def esc(t):
    return str(t).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def seed_from_id(game_id):
    return int(hashlib.md5(game_id.encode()).hexdigest()[:8], 16)

def seeded_float(seed, i=0):
    """Deterministic float 0-1 from seed + index."""
    return ((seed * 1103515245 + 12345 + i * 7919) % (2**31)) / (2**31)

# ═══════════════════════════════════════
# PERSON FIGURES
# ═══════════════════════════════════════

def standing_person(x, y, scale=1.0, facing='right', arms='down', hat=False):
    s = scale
    flip = -1 if facing == 'left' else 1
    parts = []
    head_y = y - 28*s
    parts.append(f'<circle cx="{x}" cy="{head_y}" r="{6*s}" fill="{ink}" opacity="0.6"/>')
    if hat:
        parts.append(f'<rect x="{x - 7*s}" y="{head_y - 10*s}" width="{14*s}" height="{6*s}" rx="{1*s}" fill="{ink}" opacity="0.45"/>')
        parts.append(f'<rect x="{x - 10*s}" y="{head_y - 4*s}" width="{20*s}" height="{2*s}" rx="{1*s}" fill="{ink}" opacity="0.4"/>')
    # Body
    parts.append(f'<line x1="{x}" y1="{y - 22*s}" x2="{x}" y2="{y}" stroke="{ink}" stroke-width="{2*s}" opacity="0.6" stroke-linecap="round"/>')
    # Legs
    parts.append(f'<line x1="{x}" y1="{y}" x2="{x - 6*s}" y2="{y + 16*s}" stroke="{ink}" stroke-width="{2*s}" opacity="0.6" stroke-linecap="round"/>')
    parts.append(f'<line x1="{x}" y1="{y}" x2="{x + 6*s}" y2="{y + 16*s}" stroke="{ink}" stroke-width="{2*s}" opacity="0.6" stroke-linecap="round"/>')
    # Arms
    if arms == 'up':
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x - 10*s}" y2="{y - 28*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x + 10*s}" y2="{y - 28*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
    elif arms == 'out':
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x - 14*s}" y2="{y - 10*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x + 14*s}" y2="{y - 10*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
    elif arms == 'presenting':
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x - 8*s}" y2="{y - 6*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x + 12*s*flip}" y2="{y - 22*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
    elif arms == 'holding':
        # Arms forward together (holding something)
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x + 8*s*flip}" y2="{y - 10*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x + 4*s*flip}" y2="{y - 8*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
    elif arms == 'running':
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x - 12*s*flip}" y2="{y - 12*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x + 12*s*flip}" y2="{y - 20*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
    elif arms == 'clapping':
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x + 4*s}" y2="{y - 22*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x - 4*s}" y2="{y - 22*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
    else:  # down
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x - 8*s}" y2="{y - 4*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
        parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x + 8*s}" y2="{y - 4*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
    return '\n'.join(parts)

def sitting_person(x, y, scale=1.0, arms='table'):
    s = scale
    parts = []
    parts.append(f'<circle cx="{x}" cy="{y - 20*s}" r="{5*s}" fill="{ink}" opacity="0.55"/>')
    parts.append(f'<line x1="{x}" y1="{y - 15*s}" x2="{x}" y2="{y}" stroke="{ink}" stroke-width="{2*s}" opacity="0.55" stroke-linecap="round"/>')
    if arms == 'table':
        parts.append(f'<line x1="{x}" y1="{y - 10*s}" x2="{x + 10*s}" y2="{y - 6*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.55" stroke-linecap="round"/>')
        parts.append(f'<line x1="{x}" y1="{y - 10*s}" x2="{x - 10*s}" y2="{y - 6*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.55" stroke-linecap="round"/>')
    elif arms == 'writing':
        parts.append(f'<line x1="{x}" y1="{y - 10*s}" x2="{x + 12*s}" y2="{y - 2*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.55" stroke-linecap="round"/>')
        parts.append(f'<line x1="{x}" y1="{y - 10*s}" x2="{x - 6*s}" y2="{y - 4*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.55" stroke-linecap="round"/>')
    # Legs bent
    parts.append(f'<line x1="{x}" y1="{y}" x2="{x + 6*s}" y2="{y + 10*s}" stroke="{ink}" stroke-width="{2*s}" opacity="0.55" stroke-linecap="round"/>')
    parts.append(f'<line x1="{x + 6*s}" y1="{y + 10*s}" x2="{x + 6*s}" y2="{y + 18*s}" stroke="{ink}" stroke-width="{2*s}" opacity="0.55" stroke-linecap="round"/>')
    return '\n'.join(parts)

def kneeling_person(x, y, scale=1.0, facing='right'):
    """Person kneeling (for marble games, etc)."""
    s = scale
    flip = -1 if facing == 'left' else 1
    parts = []
    parts.append(f'<circle cx="{x}" cy="{y - 16*s}" r="{5*s}" fill="{ink}" opacity="0.55"/>')
    parts.append(f'<line x1="{x}" y1="{y - 11*s}" x2="{x}" y2="{y + 2*s}" stroke="{ink}" stroke-width="{2*s}" opacity="0.55" stroke-linecap="round"/>')
    # Arm reaching forward
    parts.append(f'<line x1="{x}" y1="{y - 6*s}" x2="{x + 14*s*flip}" y2="{y}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.55" stroke-linecap="round"/>')
    parts.append(f'<line x1="{x}" y1="{y - 6*s}" x2="{x - 4*s*flip}" y2="{y - 2*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.55" stroke-linecap="round"/>')
    # Kneeling legs
    parts.append(f'<line x1="{x}" y1="{y + 2*s}" x2="{x - 6*s}" y2="{y + 10*s}" stroke="{ink}" stroke-width="{2*s}" opacity="0.55" stroke-linecap="round"/>')
    parts.append(f'<line x1="{x - 6*s}" y1="{y + 10*s}" x2="{x}" y2="{y + 14*s}" stroke="{ink}" stroke-width="{2*s}" opacity="0.55" stroke-linecap="round"/>')
    return '\n'.join(parts)


# ═══════════════════════════════════════
# PROPS
# ═══════════════════════════════════════

def draw_cards_fan(x, y, n=5, scale=1.0):
    s = scale
    parts = []
    for i in range(n):
        angle = -20 + (40 / (n - 1)) * i if n > 1 else 0
        parts.append(f'<rect x="{x - 10*s}" y="{y - 16*s}" width="{20*s}" height="{28*s}" rx="{2*s}" '
                     f'fill="{cream}" stroke="{ink}" stroke-width="{0.8*s}" opacity="0.7" '
                     f'transform="rotate({angle},{x},{y + 6*s})"/>')
    parts.append(f'<text x="{x}" y="{y + 2*s}" text-anchor="middle" font-size="{10*s}" fill="{accent}" opacity="0.6">♠</text>')
    return '\n'.join(parts)

def draw_top_hat(x, y, scale=1.0):
    s = scale
    return f'''<ellipse cx="{x}" cy="{y}" rx="{14*s}" ry="{4*s}" fill="{ink}" opacity="0.6"/>
<rect x="{x - 9*s}" y="{y - 22*s}" width="{18*s}" height="{22*s}" rx="{2*s}" fill="{ink}" opacity="0.5"/>
<ellipse cx="{x}" cy="{y - 22*s}" rx="{9*s}" ry="{3*s}" fill="{ink}" opacity="0.35"/>'''

def draw_wand(x, y, angle=30, scale=1.0):
    s = scale
    length = 30 * s
    rad = math.radians(angle)
    x2 = x + length * math.cos(rad)
    y2 = y - length * math.sin(rad)
    return f'''<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{ink}" stroke-width="{2.5*s}" stroke-linecap="round" opacity="0.6"/>
<line x1="{x2 - 4*s*math.cos(rad)}" y1="{y2 + 4*s*math.sin(rad)}" x2="{x2}" y2="{y2}" stroke="{cream}" stroke-width="{2.5*s}" stroke-linecap="round" opacity="0.8"/>'''

def draw_sparkles(x, y, n=4, radius=15, scale=1.0):
    s = scale
    parts = []
    for i in range(n):
        angle = (360 / n) * i + 15
        rad = math.radians(angle)
        sx = x + radius * s * math.cos(rad)
        sy = y + radius * s * math.sin(rad)
        size = 3 * s
        parts.append(f'<path d="M{sx},{sy - size} L{sx + size*0.3},{sy - size*0.3} L{sx + size},{sy} L{sx + size*0.3},{sy + size*0.3} L{sx},{sy + size} L{sx - size*0.3},{sy + size*0.3} L{sx - size},{sy} L{sx - size*0.3},{sy - size*0.3}Z" fill="{accent}" opacity="0.3"/>')
    return '\n'.join(parts)

def draw_blindfold_person(x, y, scale=1.0):
    s = scale
    parts = []
    parts.append(f'<circle cx="{x}" cy="{y - 28*s}" r="{6*s}" fill="{ink}" opacity="0.6"/>')
    parts.append(f'<rect x="{x - 8*s}" y="{y - 31*s}" width="{16*s}" height="{4*s}" rx="{1*s}" fill="{accent}" opacity="0.5"/>')
    parts.append(f'<line x1="{x}" y1="{y - 22*s}" x2="{x}" y2="{y}" stroke="{ink}" stroke-width="{2*s}" opacity="0.6" stroke-linecap="round"/>')
    parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x - 18*s}" y2="{y - 18*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
    parts.append(f'<line x1="{x}" y1="{y - 16*s}" x2="{x + 18*s}" y2="{y - 14*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.6" stroke-linecap="round"/>')
    parts.append(f'<line x1="{x}" y1="{y}" x2="{x - 5*s}" y2="{y + 16*s}" stroke="{ink}" stroke-width="{2*s}" opacity="0.6" stroke-linecap="round"/>')
    parts.append(f'<line x1="{x}" y1="{y}" x2="{x + 7*s}" y2="{y + 16*s}" stroke="{ink}" stroke-width="{2*s}" opacity="0.6" stroke-linecap="round"/>')
    return '\n'.join(parts)

def draw_circle_of_people(cx, cy, n=6, radius=80, scale=1.0, arms='down', held_hands=False):
    parts = []
    for i in range(n):
        angle = (360 / n) * i - 90
        rad = math.radians(angle)
        px = cx + radius * math.cos(rad)
        py = cy + radius * math.sin(rad)
        parts.append(standing_person(px, py, scale=scale * 0.8, arms=arms))
    if held_hands:
        for i in range(n):
            a1 = math.radians((360 / n) * i - 90)
            a2 = math.radians((360 / n) * ((i + 1) % n) - 90)
            x1 = cx + radius * math.cos(a1)
            y1 = cy + radius * math.sin(a1)
            x2 = cx + radius * math.cos(a2)
            y2 = cy + radius * math.sin(a2)
            mx = cx + (radius * 0.82) * math.cos((a1 + a2) / 2)
            my = cy + (radius * 0.82) * math.sin((a1 + a2) / 2)
            parts.append(f'<path d="M{x1},{y1} Q{mx},{my} {x2},{y2}" fill="none" stroke="{ink}" stroke-width="0.7" opacity="0.15"/>')
    return '\n'.join(parts)

def draw_table(x, y, w, h):
    return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{warm}" stroke="{ink}" stroke-width="1" opacity="0.3"/>
<line x1="{x + 8}" y1="{y + h}" x2="{x + 8}" y2="{y + h + 20}" stroke="{ink}" stroke-width="2" opacity="0.2"/>
<line x1="{x + w - 8}" y1="{y + h}" x2="{x + w - 8}" y2="{y + h + 20}" stroke="{ink}" stroke-width="2" opacity="0.2"/>'''

def draw_speech_bubble(x, y, text="?", scale=1.0):
    s = scale
    return f'''<ellipse cx="{x}" cy="{y}" rx="{16*s}" ry="{10*s}" fill="{cream}" stroke="{ink}" stroke-width="{0.8*s}" opacity="0.5"/>
<text x="{x}" y="{y + 4*s}" text-anchor="middle" font-family="Georgia, serif" font-size="{11*s}" fill="{ink}" opacity="0.6">{esc(text)}</text>'''

def draw_quill(x, y, scale=1.0):
    s = scale
    return f'''<line x1="{x}" y1="{y}" x2="{x + 20*s}" y2="{y - 30*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.5" stroke-linecap="round"/>
<path d="M{x + 20*s},{y - 30*s} Q{x + 28*s},{y - 38*s} {x + 16*s},{y - 42*s} Q{x + 18*s},{y - 34*s} {x + 20*s},{y - 30*s}" fill="{ink}" opacity="0.4"/>'''

def draw_paper_sheet(x, y, w=30, h=38, scale=1.0):
    s = scale
    parts = [f'<rect x="{x}" y="{y}" width="{w*s}" height="{h*s}" rx="1" fill="{cream}" stroke="{ink}" stroke-width="{0.6*s}" opacity="0.5"/>']
    for i in range(4):
        ly = y + (8 + i * 7) * s
        parts.append(f'<line x1="{x + 4*s}" y1="{ly}" x2="{x + (w - 4)*s}" y2="{ly}" stroke="{muted}" stroke-width="{0.4*s}" opacity="0.4"/>')
    return '\n'.join(parts)

def draw_ball(x, y, r=5, color=None):
    c = color or accent
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="0.5"/>'

def draw_marbles(x, y, n=5, seed=0):
    parts = []
    colors = [accent, ink, muted, light, "#6b7b4f"]
    for i in range(n):
        mx = x + (i * 12) + (seed + i) % 5 - 2
        my = y + (seed + i * 3) % 6 - 3
        c = colors[(seed + i) % len(colors)]
        parts.append(f'<circle cx="{mx}" cy="{my}" r="4" fill="{c}" opacity="0.5"/>')
        parts.append(f'<circle cx="{mx - 1}" cy="{my - 1}" r="1.5" fill="{cream}" opacity="0.3"/>')
    return '\n'.join(parts)

def draw_musical_notes(x, y, n=3, scale=1.0):
    s = scale
    parts = []
    for i in range(n):
        nx = x + i * 18 * s
        ny = y - (i % 2) * 8 * s
        parts.append(f'<circle cx="{nx}" cy="{ny}" rx="{4*s}" ry="{3*s}" fill="{ink}" opacity="0.35" transform="rotate(-20,{nx},{ny})"/>')
        parts.append(f'<line x1="{nx + 3.5*s}" y1="{ny}" x2="{nx + 3.5*s}" y2="{ny - 16*s}" stroke="{ink}" stroke-width="{1*s}" opacity="0.35"/>')
    return '\n'.join(parts)

def draw_chair(x, y, scale=1.0):
    s = scale
    return f'''<rect x="{x - 8*s}" y="{y}" width="{16*s}" height="{20*s}" rx="{2*s}" fill="{warm}" stroke="{ink}" stroke-width="{0.8*s}" opacity="0.4"/>
<rect x="{x - 8*s}" y="{y - 10*s}" width="{16*s}" height="{14*s}" rx="{2*s}" fill="{warm}" stroke="{ink}" stroke-width="{0.8*s}" opacity="0.4"/>'''

def draw_handkerchief(x, y, scale=1.0):
    s = scale
    return f'''<path d="M{x},{y} L{x + 14*s},{y - 6*s} L{x + 20*s},{y + 8*s} L{x + 6*s},{y + 14*s}Z" fill="{cream}" stroke="{ink}" stroke-width="{0.6*s}" opacity="0.5"/>
<path d="M{x + 14*s},{y - 6*s} Q{x + 18*s},{y - 2*s} {x + 20*s},{y + 8*s}" fill="none" stroke="{ink}" stroke-width="{0.4*s}" opacity="0.3"/>'''

def draw_rope(x1, y1, x2, y2, sag=20):
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2 + sag
    return f'<path d="M{x1},{y1} Q{mx},{my} {x2},{y2}" fill="none" stroke="{ink}" stroke-width="2" opacity="0.4" stroke-linecap="round"/>'

def draw_bottle(x, y, scale=1.0):
    s = scale
    return f'''<rect x="{x - 5*s}" y="{y - 20*s}" width="{10*s}" height="{20*s}" rx="{2*s}" fill="{ink}" opacity="0.25"/>
<rect x="{x - 3*s}" y="{y - 28*s}" width="{6*s}" height="{10*s}" rx="{1*s}" fill="{ink}" opacity="0.3"/>'''

def draw_candle(x, y, scale=1.0):
    s = scale
    parts = []
    parts.append(f'<rect x="{x - 3*s}" y="{y - 20*s}" width="{6*s}" height="{20*s}" rx="{1*s}" fill="{cream}" stroke="{ink}" stroke-width="{0.5*s}" opacity="0.5"/>')
    # Flame
    parts.append(f'<ellipse cx="{x}" cy="{y - 24*s}" rx="{3*s}" ry="{5*s}" fill="{accent}" opacity="0.4"/>')
    parts.append(f'<ellipse cx="{x}" cy="{y - 25*s}" rx="{1.5*s}" ry="{3*s}" fill="#e8c060" opacity="0.5"/>')
    return '\n'.join(parts)

def draw_book(x, y, scale=1.0, open=False):
    s = scale
    if open:
        return f'''<path d="M{x},{y} L{x - 18*s},{y + 2*s} L{x - 18*s},{y - 20*s} L{x},{y - 18*s}" fill="{cream}" stroke="{ink}" stroke-width="{0.6*s}" opacity="0.5"/>
<path d="M{x},{y} L{x + 18*s},{y + 2*s} L{x + 18*s},{y - 20*s} L{x},{y - 18*s}" fill="{cream}" stroke="{ink}" stroke-width="{0.6*s}" opacity="0.5"/>
<line x1="{x}" y1="{y}" x2="{x}" y2="{y - 18*s}" stroke="{ink}" stroke-width="{0.8*s}" opacity="0.4"/>'''
    else:
        return f'''<rect x="{x - 10*s}" y="{y - 14*s}" width="{20*s}" height="{28*s}" rx="{2*s}" fill="{accent}" opacity="0.25" stroke="{ink}" stroke-width="{0.6*s}"/>
<line x1="{x - 8*s}" y1="{y - 12*s}" x2="{x + 8*s}" y2="{y - 12*s}" stroke="{ink}" stroke-width="{0.4*s}" opacity="0.2"/>'''

def draw_spinning_top(x, y, scale=1.0):
    s = scale
    return f'''<path d="M{x - 8*s},{y - 6*s} Q{x},{y + 14*s} {x + 8*s},{y - 6*s}" fill="{ink}" opacity="0.35"/>
<line x1="{x}" y1="{y - 6*s}" x2="{x}" y2="{y - 16*s}" stroke="{ink}" stroke-width="{1.5*s}" opacity="0.4" stroke-linecap="round"/>
<ellipse cx="{x}" cy="{y - 6*s}" rx="{8*s}" ry="{2*s}" fill="{ink}" opacity="0.2"/>'''

def draw_cup(x, y, inverted=True, scale=1.0):
    s = scale
    if inverted:
        return f'<path d="M{x - 12*s},{y} L{x - 8*s},{y - 25*s} L{x + 8*s},{y - 25*s} L{x + 12*s},{y}" fill="{ink}" opacity="0.3" stroke="{ink}" stroke-width="0.5"/>'
    return f'<path d="M{x - 12*s},{y - 25*s} L{x - 8*s},{y} L{x + 8*s},{y} L{x + 12*s},{y - 25*s}" fill="none" stroke="{ink}" stroke-width="1" opacity="0.4"/>'


# ═══════════════════════════════════════
# DECORATIVE ELEMENTS
# ═══════════════════════════════════════

def svg_start(S=400):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
<rect width="{S}" height="{S}" fill="{bg}"/>
<rect x="20" y="20" width="{S-40}" height="{S-40}" rx="4" fill="none" stroke="{ink}" stroke-width="0.5" opacity="0.12"/>'''

def ground_line(y=310, x1=60, x2=340):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{ink}" stroke-width="0.5" opacity="0.15"/>'

# ═══════════════════════════════════════
# SCENE COMPOSERS — PARLOR GAMES (84)
# ═══════════════════════════════════════

def parlor_game_scene(entry, S=400):
    seed = seed_from_id(entry['id'])
    parts = [svg_start(S)]
    subcat = entry.get('subcategory', '')
    tags = entry.get('tags', [])
    explanation = entry.get('modern_explanation', '').lower()

    if 'acting' in subcat or 'charade' in subcat or 'theatrical' in subcat:
        # Performer on stage with small audience
        parts.append(standing_person(200, 210, scale=2.2, arms='presenting', facing='right'))
        # Audience in arc
        for i, xp in enumerate([90, 130, 270, 310]):
            yoff = 10 if i % 2 else 0
            parts.append(standing_person(xp, 275 + yoff, scale=1.1, arms='clapping'))
        # Stage footlights
        for i in range(5):
            parts.append(f'<circle cx="{140 + i * 30}" cy="300" r="2.5" fill="{accent}" opacity="0.2"/>')

    elif 'mime' in subcat or 'performance' in subcat:
        # Solo performer with dramatic pose
        parts.append(standing_person(200, 220, scale=2.5, arms='up'))
        parts.append(standing_person(100, 280, scale=1.0))
        parts.append(standing_person(300, 280, scale=1.0))
        parts.append(f'<line x1="140" y1="305" x2="260" y2="305" stroke="{accent}" stroke-width="1" opacity="0.2"/>')

    elif 'guessing' in subcat or 'deduction' in subcat or 'category-guessing' in subcat:
        # Two groups facing each other
        for i in range(3):
            parts.append(standing_person(80 + i * 35, 255, scale=1.3))
        for i in range(3):
            parts.append(standing_person(250 + i * 35, 255, scale=1.3))
        parts.append(draw_speech_bubble(200, 185, "?", scale=1.8))

    elif 'writing' in subcat or 'literary' in subcat or 'newspaper' in subcat:
        parts.append(draw_table(100, 230, 200, 8))
        for i in range(3):
            parts.append(sitting_person(140 + i * 50, 230, scale=1.2, arms='writing'))
        parts.append(draw_paper_sheet(155, 200, scale=1.0))
        parts.append(draw_paper_sheet(205, 198, scale=1.0))
        parts.append(draw_quill(175, 215, scale=1.0))

    elif 'blindfold' in subcat or 'guiding' in subcat:
        parts.append(draw_blindfold_person(200, 230, scale=2.0))
        parts.append(standing_person(110, 265, scale=1.1, arms='out'))
        parts.append(standing_person(290, 255, scale=1.2, arms='up'))

    elif 'music' in subcat or 'singing' in tags:
        parts.append(draw_circle_of_people(200, 220, n=6, radius=75, scale=1.0))
        parts.append(draw_musical_notes(170, 150, n=4, scale=1.2))

    elif 'whisper' in subcat or 'secret' in subcat or 'secret-code' in subcat:
        # Whispering chain
        for i in range(5):
            x = 80 + i * 60
            parts.append(standing_person(x, 250, scale=1.3, facing='right' if i % 2 == 0 else 'left'))
        # Dotted line between them
        for i in range(4):
            x1 = 100 + i * 60
            parts.append(f'<line x1="{x1}" y1="230" x2="{x1 + 40}" y2="230" stroke="{ink}" stroke-width="0.8" stroke-dasharray="3,3" opacity="0.2"/>')

    elif 'attention' in subcat or 'quick-response' in subcat or 'quick-reaction' in subcat:
        # Group in circle, one pointing
        parts.append(draw_circle_of_people(200, 225, n=5 + seed % 3, radius=72, scale=0.95))
        parts.append(standing_person(200, 225, scale=1.4, arms='presenting'))
        # Exclamation
        parts.append(f'<text x="230" y="170" font-family="Georgia, serif" font-size="24" fill="{accent}" opacity="0.35">!</text>')

    elif 'solemn' in subcat or 'solemn-face' in subcat:
        # Two people face-to-face, trying not to laugh
        parts.append(standing_person(160, 240, scale=2.0, facing='right'))
        parts.append(standing_person(240, 240, scale=2.0, facing='left'))
        parts.append(f'<text x="200" y="170" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="{ink}" opacity="0.2">😐</text>')

    elif 'seat-changing' in subcat or 'circle' in subcat:
        # Chairs in a circle, people standing
        n = 6
        for i in range(n):
            angle = (360 / n) * i - 90
            rad = math.radians(angle)
            cx = 200 + 70 * math.cos(rad)
            cy = 230 + 70 * math.sin(rad)
            parts.append(draw_chair(cx, cy, scale=0.8))
        # People between chairs
        for i in range(n - 1):
            angle = (360 / n) * (i + 0.5) - 90
            rad = math.radians(angle)
            px = 200 + 90 * math.cos(rad)
            py = 230 + 90 * math.sin(rad)
            parts.append(standing_person(px, py, scale=0.7, arms='running'))

    elif 'kissing' in subcat or 'compliment' in subcat or 'wishing' in subcat:
        # Two people standing close, circle of audience
        parts.append(standing_person(185, 230, scale=1.8, facing='right'))
        parts.append(standing_person(215, 230, scale=1.8, facing='left'))
        for i in range(4):
            angle = -60 + i * 40
            rad = math.radians(angle)
            parts.append(standing_person(200 + 100 * math.cos(rad), 270 + 40 * math.sin(rad), scale=0.9))

    elif 'forfeit' in subcat:
        # Person doing a silly task, others watching
        parts.append(standing_person(200, 220, scale=2.0, arms='up'))
        parts.append(standing_person(100, 270, scale=1.1, arms='clapping'))
        parts.append(standing_person(300, 270, scale=1.1, arms='clapping'))
        parts.append(draw_speech_bubble(200, 160, "⚡", scale=1.2))

    elif 'drawing' in subcat:
        # Person at easel
        parts.append(standing_person(180, 250, scale=1.8, arms='presenting'))
        # Easel
        parts.append(f'<rect x="220" y="170" width="50" height="65" rx="2" fill="{cream}" stroke="{ink}" stroke-width="0.8" opacity="0.4"/>')
        parts.append(f'<line x1="245" y1="235" x2="230" y2="280" stroke="{ink}" stroke-width="1.5" opacity="0.25"/>')
        parts.append(f'<line x1="245" y1="235" x2="260" y2="280" stroke="{ink}" stroke-width="1.5" opacity="0.25"/>')

    elif 'puppet' in subcat:
        # Puppet stage
        parts.append(f'<rect x="120" y="140" width="160" height="120" rx="3" fill="{warm}" stroke="{ink}" stroke-width="1" opacity="0.3"/>')
        parts.append(f'<rect x="120" y="130" width="160" height="14" rx="2" fill="{ink}" opacity="0.2"/>')
        # Puppet figures
        parts.append(standing_person(170, 200, scale=0.8, arms='up'))
        parts.append(standing_person(230, 200, scale=0.8, arms='presenting'))
        # Audience
        parts.append(standing_person(150, 300, scale=1.0))
        parts.append(standing_person(200, 310, scale=1.0))
        parts.append(standing_person(250, 300, scale=1.0))

    elif 'role-play' in subcat or 'mentalism' in subcat:
        # Fortune teller / mystic vibe
        parts.append(sitting_person(200, 235, scale=1.6))
        # Crystal ball
        parts.append(f'<circle cx="200" cy="210" r="15" fill="none" stroke="{ink}" stroke-width="1" opacity="0.3"/>')
        parts.append(f'<circle cx="200" cy="210" r="10" fill="{cream}" opacity="0.2"/>')
        parts.append(draw_sparkles(200, 210, n=5, radius=22))
        parts.append(draw_table(150, 240, 100, 6))

    elif 'blame' in subcat or 'taboo' in subcat or 'yes-no' in subcat:
        # Person in hot seat, others questioning
        parts.append(draw_chair(200, 235, scale=1.2))
        parts.append(sitting_person(200, 225, scale=1.5))
        for i, xp in enumerate([100, 130, 270, 300]):
            parts.append(standing_person(xp, 270, scale=1.0, arms='presenting'))
        parts.append(draw_speech_bubble(150, 185, "?", scale=1.0))
        parts.append(draw_speech_bubble(250, 190, "!", scale=1.0))

    elif 'memory' in subcat:
        # Person thinking, objects around
        parts.append(standing_person(200, 250, scale=2.0, arms='down'))
        # Thought bubble trail
        for i in range(3):
            r = 3 + i * 2
            parts.append(f'<circle cx="{200 + i * 12}" cy="{175 - i * 15}" r="{r}" fill="{cream}" stroke="{ink}" stroke-width="0.5" opacity="{0.3 + i * 0.1}"/>')
        parts.append(f'<ellipse cx="240" cy="130" rx="28" ry="18" fill="{cream}" stroke="{ink}" stroke-width="0.6" opacity="0.4"/>')
        parts.append(f'<text x="240" y="135" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{ink}" opacity="0.3">...</text>')

    else:
        # Generic parlor: circle with one performing
        n_people = 5 + seed % 3
        parts.append(draw_circle_of_people(200, 225, n=n_people, radius=72, scale=0.95))
        parts.append(standing_person(200, 225, scale=1.6, arms='presenting'))
        # Vary with seed: add a prop
        prop_idx = seed % 4
        if prop_idx == 0:
            parts.append(draw_speech_bubble(240, 170, "?"))
        elif prop_idx == 1:
            parts.append(draw_book(160, 180, open=True))
        elif prop_idx == 2:
            parts.append(draw_candle(300, 290))
        else:
            parts.append(draw_handkerchief(250, 180))

    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════
# CARD GAMES (49)
# ═══════════════════════════════════════

def card_game_scene(entry, S=400):
    seed = seed_from_id(entry['id'])
    parts = [svg_start(S)]

    # Oval table
    parts.append(f'<ellipse cx="200" cy="230" rx="120" ry="70" fill="{warm}" stroke="{ink}" stroke-width="1" opacity="0.25"/>')

    # Cards on table (vary count by seed)
    n_table = 2 + seed % 5
    for i in range(n_table):
        cx = 160 + i * 18 + (seed + i) % 8
        cy = 218 + (seed + i) % 4 * 3
        angle = -15 + i * 7 + seed % 5
        parts.append(f'<rect x="{cx - 8}" y="{cy - 12}" width="16" height="22" rx="1.5" fill="{cream}" stroke="{ink}" stroke-width="0.6" opacity="0.6" transform="rotate({angle},{cx},{cy})"/>')

    # Players (vary count 2-4)
    n_players = 2 + seed % 3
    positions = [(200, 120), (90, 230), (310, 230), (200, 340)]
    for i in range(n_players):
        px, py = positions[i]
        n_cards = 3 + (seed + i) % 4
        parts.append(draw_cards_fan(px, py - 15, n=n_cards, scale=0.65))
        parts.append(f'<circle cx="{px}" cy="{py - 48}" r="5" fill="{ink}" opacity="0.5"/>')

    # Suit decoration varying by seed
    suits = ['♠', '♥', '♦', '♣']
    suit = suits[seed % 4]
    parts.append(f'<text x="200" y="240" text-anchor="middle" font-size="14" fill="{accent}" opacity="0.15">{suit}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════
# MAGIC TRICKS (78)
# ═══════════════════════════════════════

def magic_trick_scene(entry, S=400):
    seed = seed_from_id(entry['id'])
    parts = [svg_start(S)]
    subcat = entry.get('subcategory', '')
    tags = entry.get('tags', [])
    explanation = entry.get('modern_explanation', '').lower()

    if 'coin-trick' in subcat:
        parts.append(standing_person(180, 245, scale=2.0, arms='presenting'))
        # Coins
        n_coins = 1 + seed % 3
        for i in range(n_coins):
            cx = 235 + i * 16
            cy = 195 - i * 4
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="{accent}" opacity="0.4"/>')
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="{cream}" opacity="0.3"/>')
        parts.append(draw_sparkles(245, 190, n=4, radius=22))

    elif 'card-trick' in subcat or 'card-sleight' in subcat:
        parts.append(standing_person(170, 245, scale=2.0, arms='presenting'))
        # Card spread or flourish
        for i in range(7):
            cx = 220 + i * 10
            cy = 195 + (i - 3) ** 2 * 0.8
            angle = -20 + i * 6
            parts.append(f'<rect x="{cx - 6}" y="{cy - 10}" width="12" height="18" rx="1" fill="{cream}" stroke="{ink}" stroke-width="0.5" opacity="{0.4 + i * 0.05}" transform="rotate({angle},{cx},{cy})"/>')
        parts.append(draw_sparkles(260, 185, n=3, radius=18))

    elif 'string-trick' in subcat or 'rope' in ' '.join(tags):
        parts.append(standing_person(200, 250, scale=2.0, arms='out'))
        parts.append(draw_rope(155, 210, 245, 210, sag=-10))
        # Knot in middle
        parts.append(f'<circle cx="200" cy="205" r="5" fill="{ink}" opacity="0.25"/>')
        parts.append(draw_sparkles(200, 200, n=3, radius=20))

    elif 'ring-trick' in subcat:
        parts.append(standing_person(200, 260, scale=1.8, arms='up'))
        # Linking rings
        r = 18 + seed % 5
        parts.append(f'<circle cx="180" cy="175" r="{r}" fill="none" stroke="{ink}" stroke-width="2" opacity="0.4"/>')
        parts.append(f'<circle cx="210" cy="175" r="{r}" fill="none" stroke="{ink}" stroke-width="2" opacity="0.4"/>')
        if seed % 2:
            parts.append(f'<circle cx="220" cy="170" r="{r - 4}" fill="none" stroke="{ink}" stroke-width="1.5" opacity="0.3"/>')
        parts.append(draw_sparkles(195, 175, n=4, radius=30))

    elif 'cups-and-balls' in subcat or 'cup' in explanation:
        parts.append(standing_person(200, 260, scale=1.8, arms='out'))
        for i, cx in enumerate([150, 200, 250]):
            parts.append(draw_cup(cx, 225, inverted=True, scale=0.9))
        parts.append(draw_ball(200, 228, r=4))

    elif 'fire-trick' in subcat:
        parts.append(standing_person(190, 250, scale=2.0, arms='presenting'))
        # Flames
        for i in range(3):
            fx = 240 + i * 15
            fy = 200
            parts.append(f'<ellipse cx="{fx}" cy="{fy}" rx="5" ry="12" fill="{accent}" opacity="{0.3 + i * 0.05}"/>')
            parts.append(f'<ellipse cx="{fx}" cy="{fy - 3}" rx="3" ry="7" fill="#e8c060" opacity="0.35"/>')

    elif 'escape-trick' in subcat or 'handcuff' in explanation:
        parts.append(standing_person(200, 240, scale=2.0, arms='out'))
        # Chain/handcuffs on wrists
        parts.append(f'<circle cx="160" cy="210" r="6" fill="none" stroke="{ink}" stroke-width="2" opacity="0.4"/>')
        parts.append(f'<circle cx="240" cy="215" r="6" fill="none" stroke="{ink}" stroke-width="2" opacity="0.4"/>')
        parts.append(f'<line x1="166" y1="210" x2="234" y2="215" stroke="{ink}" stroke-width="1" stroke-dasharray="4,3" opacity="0.25"/>')

    elif 'handkerchief-trick' in subcat or 'handkerchief' in tags:
        parts.append(standing_person(180, 245, scale=2.0, arms='presenting'))
        parts.append(draw_handkerchief(240, 190, scale=2.0))
        parts.append(draw_sparkles(250, 195, n=4, radius=20))

    elif 'liquid-trick' in subcat or 'chemical' in subcat:
        parts.append(standing_person(280, 255, scale=1.5, arms='presenting'))
        # Flask
        parts.append(f'<path d="M170,255 L170,210 L160,195 L160,175 L195,175 L195,195 L185,210 L185,255" fill="none" stroke="{ink}" stroke-width="1.2" opacity="0.4"/>')
        parts.append(f'<ellipse cx="177" cy="240" rx="7" ry="12" fill="{accent}" opacity="0.2"/>')
        parts.append(draw_bottle(130, 250))
        parts.append(draw_sparkles(175, 195, n=3, radius=18))

    elif 'hat-trick' in subcat or 'production' in subcat:
        parts.append(standing_person(170, 250, scale=2.0, arms='presenting'))
        parts.append(draw_top_hat(260, 235, scale=1.4))
        parts.append(draw_wand(230, 215, angle=35, scale=1.2))
        parts.append(draw_sparkles(260, 215, n=5, radius=22))

    elif 'mentalism' in subcat or 'mind-reading' in subcat:
        parts.append(standing_person(200, 245, scale=2.0, arms='presenting'))
        # Thought waves
        for i in range(3):
            r = 20 + i * 12
            parts.append(f'<path d="M{200 - r*0.7},{175} A{r},{r} 0 0,1 {200 + r*0.7},{175}" fill="none" stroke="{accent}" stroke-width="1" opacity="{0.3 - i * 0.08}"/>')
        parts.append(draw_speech_bubble(200, 150, "✦", scale=1.0))

    elif 'balance-trick' in subcat or 'levitation' in subcat:
        parts.append(standing_person(180, 250, scale=2.0, arms='presenting'))
        # Floating object
        parts.append(f'<rect x="235" y="175" width="30" height="6" rx="1" fill="{ink}" opacity="0.3"/>')
        # Levitation lines
        for i in range(3):
            parts.append(f'<line x1="{240 + i * 8}" y1="185" x2="{240 + i * 8}" y2="195" stroke="{ink}" stroke-width="0.5" stroke-dasharray="2,2" opacity="0.2"/>')
        parts.append(draw_sparkles(250, 178, n=4, radius=16))

    elif 'watch-trick' in subcat or 'domino' in subcat:
        parts.append(standing_person(180, 245, scale=2.0, arms='presenting'))
        # Watch/object
        parts.append(f'<circle cx="245" cy="200" r="14" fill="none" stroke="{ink}" stroke-width="1.5" opacity="0.4"/>')
        parts.append(f'<circle cx="245" cy="200" r="10" fill="{cream}" opacity="0.3"/>')
        parts.append(f'<line x1="245" y1="193" x2="245" y2="200" stroke="{ink}" stroke-width="0.8" opacity="0.3"/>')
        parts.append(f'<line x1="245" y1="200" x2="251" y2="204" stroke="{ink}" stroke-width="0.8" opacity="0.3"/>')
        parts.append(draw_sparkles(245, 200, n=3, radius=22))

    elif 'paper-magic' in subcat:
        parts.append(standing_person(180, 250, scale=2.0, arms='presenting'))
        # Paper pieces flying
        for i in range(4):
            px = 230 + (seed + i * 17) % 40
            py = 170 + (seed + i * 23) % 50
            angle = (seed + i * 45) % 360
            parts.append(f'<rect x="{px}" y="{py}" width="12" height="8" rx="1" fill="{cream}" stroke="{ink}" stroke-width="0.4" opacity="0.4" transform="rotate({angle},{px + 6},{py + 4})"/>')

    elif 'science-trick' in subcat or 'electrical' in subcat:
        parts.append(standing_person(280, 255, scale=1.5, arms='presenting'))
        parts.append(draw_table(100, 252, 140, 7))
        # Apparatus
        parts.append(f'<path d="M150,252 L150,210 L140,195 L140,180 L170,180 L170,195 L160,210 L160,252" fill="none" stroke="{ink}" stroke-width="1.2" opacity="0.4"/>')
        # Spark
        parts.append(f'<line x1="155" y1="185" x2="160" y2="178" stroke="{accent}" stroke-width="1.5" opacity="0.4"/>')
        parts.append(f'<line x1="160" y1="178" x2="155" y2="171" stroke="{accent}" stroke-width="1.5" opacity="0.4"/>')

    else:
        # Generic magic scene - hat + wand
        parts.append(standing_person(180, 250, scale=2.0, arms='presenting'))
        parts.append(draw_top_hat(260, 235, scale=1.3))
        parts.append(draw_wand(230, 215, angle=35, scale=1.2))
        parts.append(draw_sparkles(260, 215, n=5, radius=22))

    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════
# WORD GAMES (42)
# ═══════════════════════════════════════

def word_game_scene(entry, S=400):
    seed = seed_from_id(entry['id'])
    parts = [svg_start(S)]
    subcat = entry.get('subcategory', '')
    tags = entry.get('tags', [])

    if 'spelling' in subcat or 'alphabet' in subcat or 'letter' in subcat:
        # Scattered letters
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(14):
            lx = 70 + ((seed + i * 37) % 260)
            ly = 90 + ((seed + i * 53) % 220)
            letter = letters[(seed + i) % 26]
            size = 16 + (i % 4) * 7
            opacity = 0.12 + (i % 5) * 0.06
            parts.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-family="Georgia, serif" font-size="{size}" fill="{ink}" opacity="{opacity}">{letter}</text>')
        parts.append(draw_quill(180, 280, scale=2.0))

    elif 'rhyming' in subcat or 'poetry' in subcat:
        # Open book with quill
        parts.append(draw_book(200, 220, open=True, scale=2.5))
        parts.append(draw_quill(250, 200, scale=1.5))
        # Audience
        parts.append(sitting_person(120, 260, scale=1.1))
        parts.append(sitting_person(280, 260, scale=1.1))

    elif 'word-guessing' in subcat or 'category-word' in subcat or 'category' in subcat:
        # People talking with word bubbles
        parts.append(standing_person(140, 255, scale=1.6, facing='right'))
        parts.append(standing_person(260, 255, scale=1.6, facing='left'))
        parts.append(draw_speech_bubble(140, 185, "A?", scale=1.2))
        parts.append(draw_speech_bubble(260, 190, "B!", scale=1.2))
        # Word dashes
        for i in range(4):
            parts.append(f'<line x1="{165 + i * 18}" y1="310" x2="{175 + i * 18}" y2="310" stroke="{ink}" stroke-width="2" opacity="0.25"/>')

    elif 'acronym' in subcat or 'number' in subcat:
        # Person at blackboard
        parts.append(standing_person(130, 260, scale=1.6, arms='presenting'))
        # Blackboard
        parts.append(f'<rect x="190" y="150" width="140" height="100" rx="3" fill="{ink}" opacity="0.08"/>')
        parts.append(f'<rect x="195" y="155" width="130" height="90" rx="2" fill="{ink}" opacity="0.06"/>')
        # Letters/numbers on board
        items = "ABCXYZ123" if 'acronym' in subcat else "1234567"
        for i, ch in enumerate(items[:6]):
            parts.append(f'<text x="{210 + (i % 3) * 38}" y="{185 + (i // 3) * 30}" font-family="Georgia, serif" font-size="14" fill="{cream}" opacity="0.5">{ch}</text>')

    elif 'taboo' in subcat or 'response' in subcat or 'nonsense' in subcat:
        # Group with crossed-out word
        parts.append(draw_circle_of_people(200, 230, n=5, radius=68, scale=0.9))
        # Forbidden sign
        parts.append(f'<circle cx="200" cy="230" r="20" fill="none" stroke="{accent}" stroke-width="2" opacity="0.3"/>')
        parts.append(f'<line x1="186" y1="216" x2="214" y2="244" stroke="{accent}" stroke-width="2" opacity="0.3"/>')

    elif 'team-word' in subcat or 'comparison' in subcat:
        # Two teams
        for i in range(3):
            parts.append(standing_person(90 + i * 30, 260, scale=1.2))
        for i in range(3):
            parts.append(standing_person(260 + i * 30, 260, scale=1.2))
        # VS divider
        parts.append(f'<line x1="200" y1="180" x2="200" y2="300" stroke="{ink}" stroke-width="0.5" stroke-dasharray="4,4" opacity="0.15"/>')
        parts.append(draw_speech_bubble(140, 195, "...", scale=1.0))
        parts.append(draw_speech_bubble(260, 195, "...", scale=1.0))

    elif 'riddle' in subcat or 'trivia' in subcat or 'knowledge' in subcat:
        # Quiz master + contestants
        parts.append(standing_person(200, 220, scale=2.0, arms='presenting', hat=True))
        parts.append(draw_book(200, 270, scale=1.2))
        for i in range(4):
            parts.append(standing_person(80 + i * 80, 290, scale=0.9))
        parts.append(draw_speech_bubble(200, 160, "?!", scale=1.3))

    else:
        # Generic word game: people at table with paper and quills
        parts.append(draw_table(100, 235, 200, 8))
        n_players = 2 + seed % 2
        for i in range(n_players):
            x = 140 + i * 60
            parts.append(sitting_person(x, 235, scale=1.2, arms='writing'))
            parts.append(draw_paper_sheet(x + 5, 207, scale=0.9))
        parts.append(draw_quill(180 + (seed % 40), 220, scale=1.0))
        # Seed-based variation
        if seed % 3 == 0:
            parts.append(draw_speech_bubble(200, 168, "ABC", scale=1.1))
        elif seed % 3 == 1:
            parts.append(draw_book(120, 260, scale=0.9))

    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════
# PHYSICAL GAMES (31) + FOLK GAMES (44)
# ═══════════════════════════════════════

def physical_game_scene(entry, S=400):
    seed = seed_from_id(entry['id'])
    parts = [svg_start(S)]
    subcat = entry.get('subcategory', '')
    tags = entry.get('tags', [])
    explanation = entry.get('modern_explanation', '').lower()

    if 'blindfold' in subcat or 'blind' in tags:
        parts.append(draw_blindfold_person(200, 225, scale=2.2))
        parts.append(standing_person(110, 260, scale=1.2, arms='running'))
        parts.append(standing_person(295, 250, scale=1.3, arms='out'))
        parts.append(standing_person(320, 300, scale=0.9))

    elif 'elimination' in subcat or 'musical' in tags:
        # Musical chairs
        n_chairs = 4
        for i in range(n_chairs):
            parts.append(draw_chair(110 + i * 60, 240, scale=0.9))
        for i in range(n_chairs + 1):
            parts.append(standing_person(90 + i * 55, 200, scale=1.1, arms='running'))
        parts.append(draw_musical_notes(170, 150, n=3))

    elif 'chasing' in subcat or 'tag' in subcat or 'chase' in tags or 'catch' in tags:
        # Chase scene
        parts.append(standing_person(140, 230, scale=1.9, arms='out', facing='right'))
        parts.append(standing_person(270, 235, scale=1.7, arms='running', facing='right'))
        parts.append(standing_person(320, 260, scale=1.2, arms='running'))
        parts.append(ground_line(305))

    elif 'circle' in subcat or 'ring' in tags or 'circle' in explanation[:50]:
        n = 7 + seed % 3
        parts.append(draw_circle_of_people(200, 220, n=n, radius=82, scale=0.9, held_hands=True))

    elif 'freeze' in subcat or 'statue' in tags:
        # Frozen poses
        parts.append(standing_person(120, 240, scale=1.5, arms='up'))
        parts.append(standing_person(200, 250, scale=1.7, arms='out'))
        parts.append(standing_person(280, 235, scale=1.6, arms='presenting'))
        parts.append(ground_line(305))

    elif 'tossing' in subcat or 'throwing' in subcat or 'ball-game' in subcat:
        parts.append(standing_person(130, 250, scale=1.7, arms='presenting'))
        parts.append(standing_person(280, 250, scale=1.7, arms='up'))
        # Ball in arc
        parts.append(f'<path d="M165,210 Q205,150 245,210" fill="none" stroke="{ink}" stroke-width="0.5" stroke-dasharray="3,3" opacity="0.2"/>')
        parts.append(draw_ball(205, 160, r=6))

    elif 'marble' in subcat:
        # Kneeling players with marbles
        parts.append(kneeling_person(150, 250, scale=1.5, facing='right'))
        parts.append(kneeling_person(260, 250, scale=1.5, facing='left'))
        # Marble ring
        parts.append(f'<circle cx="200" cy="275" r="40" fill="none" stroke="{ink}" stroke-width="0.8" opacity="0.2"/>')
        parts.append(draw_marbles(180, 275, n=7, seed=seed))

    elif 'wrestling' in subcat or 'strength' in tags:
        # Two people close together wrestling
        parts.append(standing_person(185, 240, scale=1.8, arms='out', facing='right'))
        parts.append(standing_person(215, 240, scale=1.8, arms='out', facing='left'))
        parts.append(ground_line(305))

    elif 'jumping' in subcat or 'skip' in tags:
        # Person jumping, rope on ground
        parts.append(standing_person(200, 220, scale=2.0, arms='up'))
        parts.append(draw_rope(120, 270, 280, 270, sag=15))
        parts.append(standing_person(110, 260, scale=1.0, arms='holding'))
        parts.append(standing_person(290, 260, scale=1.0, arms='holding'))

    elif 'dexterity' in subcat or 'coordination' in subcat:
        parts.append(standing_person(200, 240, scale=2.0, arms='presenting'))
        parts.append(draw_ball(235, 195, r=5))
        parts.append(draw_ball(245, 210, r=4))
        parts.append(draw_sparkles(240, 200, n=3, radius=16))

    elif 'top' in subcat:
        parts.append(kneeling_person(180, 250, scale=1.5))
        parts.append(draw_spinning_top(250, 260))
        parts.append(standing_person(300, 260, scale=1.2))
        parts.append(ground_line(305))

    elif 'bat-and-ball' in subcat:
        parts.append(standing_person(160, 240, scale=1.8, arms='presenting'))
        # Bat
        parts.append(f'<line x1="180" y1="215" x2="210" y2="195" stroke="{ink}" stroke-width="3" opacity="0.4" stroke-linecap="round"/>')
        parts.append(draw_ball(230, 200, r=5))
        parts.append(standing_person(300, 260, scale=1.3))

    elif 'string' in subcat or 'cats-cradle' in tags:
        parts.append(standing_person(165, 245, scale=1.8, arms='out', facing='right'))
        parts.append(standing_person(235, 245, scale=1.8, arms='out', facing='left'))
        # String between hands
        parts.append(f'<path d="M140,215 L180,210 L220,215 L260,210" fill="none" stroke="{ink}" stroke-width="1" opacity="0.35"/>')
        parts.append(f'<path d="M145,220 L190,225 L210,218 L255,222" fill="none" stroke="{ink}" stroke-width="1" opacity="0.3"/>')

    elif 'toy' in subcat or 'skill-toy' in subcat or 'paper-craft' in subcat:
        parts.append(standing_person(180, 245, scale=1.8, arms='holding'))
        # Generic toy shape
        parts.append(f'<rect x="210" y="200" width="25" height="30" rx="3" fill="{warm}" stroke="{ink}" stroke-width="0.8" opacity="0.4"/>')
        parts.append(standing_person(290, 270, scale=1.1))

    else:
        # Generic physical
        parts.append(standing_person(130, 240, scale=1.6, arms='up'))
        parts.append(standing_person(200, 230, scale=1.8, arms='out'))
        parts.append(standing_person(280, 250, scale=1.4, arms='running'))
        parts.append(ground_line(305))

    parts.append('</svg>')
    return '\n'.join(parts)


def folk_game_scene(entry, S=400):
    seed = seed_from_id(entry['id'])
    parts = [svg_start(S)]
    subcat = entry.get('subcategory', '')
    tags = entry.get('tags', [])
    explanation = entry.get('modern_explanation', '').lower()

    if 'singing' in subcat or 'singing' in tags:
        # Ring of people with musical notes
        n = 6 + seed % 3
        parts.append(draw_circle_of_people(200, 225, n=n, radius=78, scale=0.95, held_hands=True))
        parts.append(draw_musical_notes(155, 140, n=4, scale=1.3))

    elif 'chasing' in subcat or 'circle-chase' in subcat:
        # Circle with one person running around outside
        n = 6 + seed % 2
        parts.append(draw_circle_of_people(200, 230, n=n, radius=70, scale=0.9))
        # Runner outside circle
        parts.append(standing_person(320, 230, scale=1.4, arms='running'))
        # Dropped handkerchief
        parts.append(draw_handkerchief(280, 290))

    elif 'dancing' in subcat:
        # Pairs dancing
        for i in range(3):
            x = 110 + i * 95
            parts.append(standing_person(x - 10, 240, scale=1.4, facing='right'))
            parts.append(standing_person(x + 10, 240, scale=1.4, facing='left'))
        parts.append(draw_musical_notes(160, 160, n=3))
        parts.append(ground_line(305))

    elif 'dramatic' in subcat or 'performance' in subcat or 'imitation' in subcat:
        # One person acting, circle watching
        parts.append(standing_person(200, 220, scale=2.0, arms='presenting'))
        for i in range(5):
            angle = -60 + i * 30
            rad = math.radians(angle)
            parts.append(standing_person(200 + 95 * math.cos(rad), 275 + 30 * math.sin(rad), scale=0.9))

    elif 'guessing' in subcat:
        # IT person in center, others around
        parts.append(standing_person(200, 225, scale=1.8, arms='presenting'))
        parts.append(draw_circle_of_people(200, 225, n=6, radius=80, scale=0.85))
        parts.append(draw_speech_bubble(200, 160, "?"))

    elif 'forfeit' in subcat or 'action' in subcat:
        # Person doing something silly
        parts.append(standing_person(200, 220, scale=2.2, arms='up'))
        parts.append(standing_person(110, 270, scale=1.0, arms='clapping'))
        parts.append(standing_person(290, 270, scale=1.0, arms='clapping'))
        parts.append(standing_person(320, 290, scale=0.9))
        parts.append(standing_person(80, 290, scale=0.9))

    elif 'corner' in subcat:
        # Four corners with people
        corners = [(100, 160), (300, 160), (100, 300), (300, 300)]
        for cx, cy in corners:
            parts.append(standing_person(cx, cy, scale=1.2))
            parts.append(f'<rect x="{cx - 12}" y="{cy + 14}" width="24" height="4" rx="1" fill="{ink}" opacity="0.1"/>')
        parts.append(standing_person(200, 230, scale=1.5, arms='out'))

    elif 'reaction' in subcat or 'attention' in tags:
        # Quick response — people in a line
        for i in range(5):
            arms = 'up' if (seed + i) % 3 == 0 else 'out' if (seed + i) % 3 == 1 else 'down'
            parts.append(standing_person(90 + i * 60, 250, scale=1.3, arms=arms))
        parts.append(f'<text x="200" y="170" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="{accent}" opacity="0.25">!</text>')

    else:
        # Default folk: ring game with held hands
        n = 6 + seed % 4
        parts.append(draw_circle_of_people(200, 225, n=n, radius=80, scale=1.0, held_hands=True))
        # Vary: add center person for some
        if seed % 2:
            parts.append(standing_person(200, 225, scale=1.3, arms='presenting'))

    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════
# SCIENTIFIC RECREATIONS (12)
# ═══════════════════════════════════════

def science_scene(entry, S=400):
    seed = seed_from_id(entry['id'])
    parts = [svg_start(S)]
    explanation = entry.get('modern_explanation', '').lower()

    parts.append(draw_table(80, 255, 240, 8))
    parts.append(standing_person(310, 255, scale=1.5, arms='presenting'))

    if 'water' in explanation or 'liquid' in explanation:
        # Beaker with liquid
        parts.append(f'<path d="M160,255 L160,215 L150,200 L150,180 L185,180 L185,200 L175,215 L175,255" fill="none" stroke="{ink}" stroke-width="1.2" opacity="0.4"/>')
        parts.append(f'<ellipse cx="167" cy="240" rx="7" ry="12" fill="#4a7a9b" opacity="0.2"/>')
        parts.append(draw_bottle(120, 248))
    elif 'fire' in explanation or 'candle' in explanation or 'heat' in explanation:
        parts.append(draw_candle(150, 250, scale=1.5))
        parts.append(draw_candle(200, 248, scale=1.3))
    elif 'magnet' in explanation or 'electric' in explanation:
        # Horseshoe magnet
        parts.append(f'<path d="M150,220 L150,195 A20,20 0 0,1 190,195 L190,220" fill="none" stroke="{accent}" stroke-width="3" opacity="0.4" stroke-linecap="round"/>')
        # Iron filings
        for i in range(8):
            fx = 155 + (seed + i * 11) % 30
            fy = 230 + (seed + i * 7) % 15
            parts.append(f'<line x1="{fx}" y1="{fy}" x2="{fx + 3}" y2="{fy - 3}" stroke="{ink}" stroke-width="0.6" opacity="0.25"/>')
    elif 'spin' in explanation or 'rotat' in explanation or 'wheel' in explanation:
        # Spinning wheel/disc
        cx, cy = 170, 215
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="30" fill="none" stroke="{ink}" stroke-width="1.5" opacity="0.35"/>')
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{ink}" opacity="0.4"/>')
        for i in range(6):
            a = math.radians(i * 60 + seed % 30)
            parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + 28 * math.cos(a)}" y2="{cy + 28 * math.sin(a)}" stroke="{ink}" stroke-width="0.8" opacity="0.2"/>')
    else:
        # Generic apparatus: gear + flask
        cx, cy, r = 150, 220, 20
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ink}" stroke-width="1.2" opacity="0.35"/>')
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.4}" fill="none" stroke="{ink}" stroke-width="1" opacity="0.3"/>')
        for i in range(8):
            a = math.radians(i * 45)
            parts.append(f'<rect x="{cx + r * 0.8 * math.cos(a) - 3}" y="{cy + r * 0.8 * math.sin(a) - 3}" width="6" height="6" rx="1" fill="{ink}" opacity="0.2" transform="rotate({i * 45},{cx + r * 0.8 * math.cos(a)},{cy + r * 0.8 * math.sin(a)})"/>')
        # Flask
        parts.append(f'<path d="M220,255 L220,220 L215,210 L215,195 L240,195 L240,210 L235,220 L235,255" fill="none" stroke="{ink}" stroke-width="1" opacity="0.35"/>')

    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════
# PUZZLE GAMES — fallback for non-diagram puzzles (22)
# ═══════════════════════════════════════

def puzzle_scene(entry, S=400):
    seed = seed_from_id(entry['id'])
    parts = [svg_start(S)]
    explanation = entry.get('modern_explanation', '').lower()
    tags = entry.get('tags', [])
    subcat = entry.get('subcategory', '')

    if 'arithmetic' in subcat or 'number' in subcat or 'age' in subcat or 'price' in subcat:
        # Math puzzle: numbers floating
        nums = "0123456789+-×÷="
        for i in range(12):
            nx = 70 + ((seed + i * 41) % 260)
            ny = 80 + ((seed + i * 59) % 240)
            ch = nums[(seed + i) % len(nums)]
            size = 18 + (i % 3) * 10
            opacity = 0.1 + (i % 4) * 0.06
            parts.append(f'<text x="{nx}" y="{ny}" text-anchor="middle" font-family="Georgia, serif" font-size="{size}" fill="{ink}" opacity="{opacity}">{ch}</text>')
        # Person thinking
        parts.append(standing_person(200, 310, scale=1.2, arms='down'))

    elif 'logic' in subcat or 'deduction' in subcat or 'sequence' in subcat:
        # Logic chain
        parts.append(standing_person(200, 280, scale=1.5, arms='presenting'))
        # Chain of connected nodes
        for i in range(5):
            cx = 90 + i * 60
            parts.append(f'<circle cx="{cx}" cy="170" r="16" fill="{cream}" stroke="{ink}" stroke-width="0.8" opacity="0.4"/>')
            parts.append(f'<text x="{cx}" y="175" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{ink}" opacity="0.3">{chr(65 + i)}</text>')
            if i < 4:
                parts.append(f'<line x1="{cx + 16}" y1="170" x2="{cx + 44}" y2="170" stroke="{ink}" stroke-width="0.8" opacity="0.2"/>')

    elif 'water-pouring' in subcat:
        # Three vessels
        for i, (w, h) in enumerate([(30, 60), (24, 45), (18, 35)]):
            vx = 130 + i * 60
            parts.append(f'<rect x="{vx}" y="{260 - h}" width="{w}" height="{h}" rx="2" fill="none" stroke="{ink}" stroke-width="1" opacity="0.35"/>')
            fill_h = h * (0.3 + seeded_float(seed, i) * 0.5)
            parts.append(f'<rect x="{vx + 1}" y="{260 - fill_h}" width="{w - 2}" height="{fill_h}" rx="1" fill="#4a7a9b" opacity="0.15"/>')
        parts.append(standing_person(310, 255, scale=1.3, arms='presenting'))

    elif 'probability' in subcat or 'combinatorics' in subcat:
        # Dice / probability
        for i in range(3):
            dx = 150 + i * 50
            dy = 200 + (seed + i) % 10
            parts.append(f'<rect x="{dx}" y="{dy}" width="25" height="25" rx="3" fill="{cream}" stroke="{ink}" stroke-width="0.8" opacity="0.4"/>')
            # Dots
            n_dots = 1 + (seed + i) % 6
            dots_pos = [(0.5, 0.5), (0.25, 0.25), (0.75, 0.75), (0.25, 0.75), (0.75, 0.25), (0.5, 0.25)]
            for j in range(min(n_dots, 6)):
                px, py = dots_pos[j]
                parts.append(f'<circle cx="{dx + px * 25}" cy="{dy + py * 25}" r="2" fill="{ink}" opacity="0.35"/>')
        parts.append(standing_person(200, 280, scale=1.3))

    elif 'mechanical' in subcat or 'dexterity' in subcat:
        # Hands manipulating object
        parts.append(standing_person(200, 250, scale=2.0, arms='holding'))
        # Puzzle box
        parts.append(f'<rect x="215" y="210" width="35" height="35" rx="2" fill="{warm}" stroke="{ink}" stroke-width="0.8" opacity="0.4"/>')
        parts.append(f'<line x1="232" y1="210" x2="232" y2="245" stroke="{ink}" stroke-width="0.4" opacity="0.2"/>')
        parts.append(f'<line x1="215" y1="228" x2="250" y2="228" stroke="{ink}" stroke-width="0.4" opacity="0.2"/>')

    elif 'riddle' in subcat:
        parts.append(standing_person(200, 250, scale=2.0, arms='presenting'))
        parts.append(draw_speech_bubble(200, 170, "?!", scale=2.0))
        parts.append(standing_person(110, 280, scale=1.0))
        parts.append(standing_person(290, 280, scale=1.0))

    else:
        # Generic puzzle: person studying something on table
        parts.append(draw_table(120, 240, 160, 7))
        parts.append(sitting_person(200, 240, scale=1.5, arms='table'))
        # Puzzle pieces
        for i in range(4):
            px = 145 + i * 35
            py = 218 + (seed + i) % 8
            angle = (seed + i * 23) % 30 - 15
            parts.append(f'<rect x="{px}" y="{py}" width="18" height="14" rx="2" fill="{warm}" stroke="{ink}" stroke-width="0.5" opacity="0.35" transform="rotate({angle},{px + 9},{py + 7})"/>')
        # Thought bubble
        parts.append(f'<circle cx="225" cy="180" r="3" fill="{cream}" stroke="{ink}" stroke-width="0.4" opacity="0.3"/>')
        parts.append(f'<circle cx="232" cy="170" r="4" fill="{cream}" stroke="{ink}" stroke-width="0.4" opacity="0.3"/>')
        parts.append(f'<ellipse cx="245" cy="155" rx="18" ry="12" fill="{cream}" stroke="{ink}" stroke-width="0.5" opacity="0.3"/>')
        parts.append(f'<text x="245" y="159" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="{ink}" opacity="0.3">?</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════

def generate_illustrated_thumbnail(entry):
    cat = entry.get('category', '')
    if cat == 'card-game':
        return card_game_scene(entry)
    elif cat == 'magic-trick':
        return magic_trick_scene(entry)
    elif cat == 'word-game':
        return word_game_scene(entry)
    elif cat == 'physical-game':
        return physical_game_scene(entry)
    elif cat == 'folk-game':
        return folk_game_scene(entry)
    elif cat == 'scientific-recreation':
        return science_scene(entry)
    elif cat == 'puzzle':
        return puzzle_scene(entry)
    else:  # parlor-game, board-game, and anything else
        return parlor_game_scene(entry)


# ═══════════════════════════════════════
# TEST — Generate samples
# ═══════════════════════════════════════

if __name__ == '__main__':
    with open('/home/user/workspace/heritage_parlor/data/entries.json') as f:
        entries = json.load(f)
    entries_by_id = {e['id']: e for e in entries}

    # Pick diverse samples from each category — using subcategories for variety
    samples = {
        'parlor-game': ['acting-proverbs', 'aesop-s-mission', 'blind-postman', 'alphabet-games', 'the-cushion-dance-parlor', 'consequences'],
        'card-game': ['whist', 'cribbage', 'snap', 'old-maid'],
        'magic-trick': ['coin-through-the-handkerchief', 'the-magic-rings', 'the-cut-string-restored', 'fire-eating', 'finding-a-chosen-card-by-mathematics', 'the-three-cups'],
        'word-game': ['adjectives', 'the-adventurers', 'bouts-rimes', 'crambo'],
        'physical-game': ['blind-man-s-buff', 'musical-chairs', 'marbles', 'battledore-and-shuttlecock'],
        'folk-game': ['oranges-and-lemons', 'drop-the-handkerchief', 'london-bridge-is-falling-down', 'nuts-in-may'],
        'scientific-recreation': ['new-perpetual-motion', 'thaumatrope-sociable'],
        'puzzle': ['the-divided-garden', 'the-magic-square-order-3'],
    }

    out_dir = '/home/user/workspace/heritage_parlor/illustration_samples'
    os.makedirs(out_dir, exist_ok=True)
    # Clear old files
    for f in os.listdir(out_dir):
        if f.endswith('.svg'):
            os.remove(os.path.join(out_dir, f))

    generated = 0
    for cat, ids in samples.items():
        for gid in ids:
            entry = entries_by_id.get(gid)
            if not entry:
                # Fuzzy match
                matches = [e for e in entries if gid.replace('-', '') in e['id'].replace('-', '')]
                if matches:
                    entry = matches[0]
                    gid = entry['id']
            if not entry:
                # Just pick from category by index
                cat_entries = [e for e in entries if e['category'] == cat]
                idx = len([i for i in ids if i == gid])
                if cat_entries and idx < len(cat_entries):
                    entry = cat_entries[min(idx, len(cat_entries) - 1)]
                    gid = entry['id']
            if not entry:
                print(f"  SKIP: {gid}")
                continue
            svg = generate_illustrated_thumbnail(entry)
            path = f'{out_dir}/{cat}__{gid}.svg'
            with open(path, 'w') as f:
                f.write(svg)
            print(f"  {cat}: {entry['title']} ({entry.get('subcategory', 'none')})")
            generated += 1

    print(f"\nGenerated {generated} samples")
