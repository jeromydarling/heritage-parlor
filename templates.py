"""
Heritage Parlor — 7 Diagram Templates
Each template produces 3 outputs: thumbnail, page1 (playable), page2 (instructions)
All SVGs use the same Victorian design language as the Blind Abbot prototype.
"""
import math, json, re

# ═══════════════════════════════════════════
# DESIGN TOKENS
# ═══════════════════════════════════════════
bg = "#faf6f0"
ink = "#1a1a1a"
light = "#555"
accent = "#8b4513"
rule = "#ccc"
white = "#ffffff"
board_fill = "#f5f0e6"   # warm cream for board backgrounds
board_dark = "#d4c5a9"   # darker cream for alternating squares

def esc(text):
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace("'", '&apos;').replace('"', '&quot;')

def wrap_text(text, max_chars=50):
    words = str(text).split()
    lines, current = [], ''
    for word in words:
        if len(current) + len(word) + 1 > max_chars:
            lines.append(current.strip())
            current = word + ' '
        else:
            current += word + ' '
    if current.strip():
        lines.append(current.strip())
    return lines


# ═══════════════════════════════════════════
# SHARED PAGE SCAFFOLDING
# ═══════════════════════════════════════════

def thumbnail_shell(size=400):
    """Start a square thumbnail SVG."""
    return [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
  <rect width="{size}" height="{size}" fill="{bg}"/>''']

def page1_shell(entry, W=816, H=1056):
    """Start a page 1 SVG with title, subtitle, border."""
    heading = "&apos;Playfair Display&apos;, Georgia, serif"
    body = "&apos;Source Sans 3&apos;, Georgia, sans-serif"
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <style>@import url("https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&amp;family=Source+Sans+3:wght@300;400;600&amp;display=swap");</style>
    <pattern id="ph" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="6" stroke="{ink}" stroke-width="0.3" opacity="0.05"/>
    </pattern>
  </defs>
  <rect width="{W}" height="{H}" fill="{bg}"/>
  <rect width="{W}" height="{H}" fill="url(#ph)"/>
  <rect x="24" y="24" width="{W-48}" height="{H-48}" rx="2" fill="none" stroke="{ink}" stroke-width="0.75" opacity="0.2"/>''']

    # Title
    title = entry['title'].upper()
    if len(title) > 40:
        title = title[:37] + '...'
    parts.append(f'  <text x="{W//2}" y="82" text-anchor="middle" font-family="{heading}" font-size="34" font-weight="bold" fill="{ink}" letter-spacing="2">{esc(title)}</text>')

    cat = entry['category'].replace('-', ' ').title()
    players = entry.get('players', '?')
    diff = entry.get('difficulty', '').title()
    parts.append(f'  <text x="{W//2}" y="110" text-anchor="middle" font-family="{body}" font-size="14" fill="{light}">{cat}  ·  {players} players  ·  {diff}</text>')
    parts.append(f'  <line x1="220" y1="126" x2="{W-220}" y2="126" stroke="{rule}" stroke-width="0.75"/>')

    return parts

def page2_content(entry, W=816, H=1056):
    """Generate page 2 instructions. Returns SVG string."""
    m = 220
    content_w = W - 2 * m
    heading_font = "'Playfair Display', Georgia, serif"
    body_font = "'Source Sans 3', Georgia, sans-serif"

    title = entry['title'].upper()
    if len(title) > 40:
        title = title[:37] + '...'

    # Build HTML content sections
    sections = []

    # What You Need
    equip = entry.get('equipment_needed', [])
    if equip:
        equip_html = ''.join(f'<div style="padding-left:16px;">·  {esc(item)}</div>' for item in equip)
    else:
        equip_html = '<div style="padding-left:16px;">Nothing special — just the game board on page 1.</div>'
    sections.append(f'<div style="font-family:{heading_font};font-size:17px;font-weight:bold;color:{ink};margin-bottom:8px;">What You Need</div>{equip_html}')

    # How to Play
    explanation = esc(entry.get('modern_explanation', 'No modern explanation available.'))
    sections.append(f'<div style="font-family:{heading_font};font-size:17px;font-weight:bold;color:{ink};margin-bottom:8px;">How to Play</div><div style="text-align:justify;font-size:14px;line-height:1.55;color:{ink};">{explanation}</div>')

    # Did You Know?
    fun = entry.get('fun_fact', '')
    if fun:
        sections.append(f'<div style="font-family:{heading_font};font-size:17px;font-weight:bold;color:{accent};margin-bottom:8px;">Did You Know?</div><div style="text-align:justify;font-size:13px;line-height:1.5;font-style:italic;color:{light};">{esc(fun)}</div>')

    # Original Victorian Description
    orig = entry.get('original_description', '')
    if orig:
        sections.append(f'<div style="font-family:{heading_font};font-size:17px;font-weight:bold;color:{ink};margin-bottom:8px;">Original Victorian Description</div><div style="text-align:justify;font-size:13px;line-height:1.5;font-style:italic;color:{light};">{esc(orig)}</div>')

    body_html = '<div style="display:flex;flex-direction:column;gap:18px;">' + ''.join(f'<div>{s}</div>' for s in sections) + '</div>'

    # Footer
    source = f"{entry.get('source_book', 'Unknown')} ({entry.get('source_year', '')})"

    title_y = 80
    rule_y = title_y + 48
    content_y = rule_y + 16
    footer_y = H - 64

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <style>@import url("https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&amp;family=Source+Sans+3:wght@300;400;600&amp;display=swap");</style>
    <pattern id="ph2" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="6" stroke="{ink}" stroke-width="0.3" opacity="0.05"/>
    </pattern>
  </defs>
  <rect width="{W}" height="{H}" fill="{bg}"/>
  <rect width="{W}" height="{H}" fill="url(#ph2)"/>
  <rect x="24" y="24" width="{W-48}" height="{H-48}" rx="2" fill="none" stroke="{ink}" stroke-width="0.75" opacity="0.2"/>
  <text x="{W//2}" y="{title_y}" text-anchor="middle" font-family="&apos;Playfair Display&apos;, Georgia, serif" font-size="22" font-weight="bold" fill="{ink}" letter-spacing="2">{esc(title)}</text>
  <text x="{W//2}" y="{title_y + 22}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="12" fill="{light}">Instructions</text>
  <line x1="{m}" y1="{rule_y}" x2="{W-m}" y2="{rule_y}" stroke="{rule}" stroke-width="0.75"/>
  <foreignObject x="{m}" y="{content_y}" width="{content_w}" height="{footer_y - content_y - 10}">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family:{body_font};font-size:14px;color:{ink};line-height:1.55;overflow:hidden;height:100%;">
      {body_html}
    </div>
  </foreignObject>
  <line x1="{m}" y1="{footer_y}" x2="{W-m}" y2="{footer_y}" stroke="{rule}" stroke-width="0.5"/>
  <text x="{W//2}" y="{footer_y + 20}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="11" fill="{light}">Source: {esc(source)}  ·  Heritage Parlor</text>
</svg>'''
    return svg


# ═══════════════════════════════════════════
# TEMPLATE 1: NxN GRID
# Handles 3x3 through 8x8 square grids
# ═══════════════════════════════════════════

def draw_nxn_grid(parts, cx, cy, cell_size, n=3, mode='thumb', show_coords=False):
    """Draw an NxN grid centered at (cx, cy)."""
    grid = cell_size * n
    gx = cx - grid // 2
    gy = cy - grid // 2
    sw_outer = 2 if mode == 'print' else 1.5
    sw_inner = 1.5 if mode == 'print' else 1
    
    # Grid background
    parts.append(f'  <rect x="{gx}" y="{gy}" width="{grid}" height="{grid}" fill="{white}" stroke="{ink}" stroke-width="{sw_outer}" rx="2"/>')
    
    # Grid lines
    for i in range(1, n):
        parts.append(f'  <line x1="{gx}" y1="{gy + i*cell_size}" x2="{gx + grid}" y2="{gy + i*cell_size}" stroke="{ink}" stroke-width="{sw_inner}"/>')
        parts.append(f'  <line x1="{gx + i*cell_size}" y1="{gy}" x2="{gx + i*cell_size}" y2="{gy + grid}" stroke="{ink}" stroke-width="{sw_inner}"/>')
    
    if mode == 'print':
        # Dashed circles for coin placement
        coin_r = cell_size * 0.22
        for row in range(n):
            for col in range(n):
                px = gx + col * cell_size + cell_size // 2
                py = gy + row * cell_size + cell_size // 2
                parts.append(f'  <circle cx="{px}" cy="{py}" r="{coin_r:.0f}" fill="none" stroke="{rule}" stroke-width="1" stroke-dasharray="6,4"/>')
        
        if show_coords:
            # Column labels (A, B, C...)
            for i in range(n):
                tx = gx + i * cell_size + cell_size // 2
                parts.append(f'  <text x="{tx}" y="{gy - 8}" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="{light}">{chr(65+i)}</text>')
            # Row labels (1, 2, 3...)
            for i in range(n):
                ty = gy + i * cell_size + cell_size // 2 + 5
                parts.append(f'  <text x="{gx - 12}" y="{ty}" text-anchor="end" font-family="Georgia, serif" font-size="13" fill="{light}">{i+1}</text>')
    else:
        # Thumbnail: filled circles
        coin_r = cell_size * 0.2
        for row in range(n):
            for col in range(n):
                px = gx + col * cell_size + cell_size // 2
                py = gy + row * cell_size + cell_size // 2
                parts.append(f'  <circle cx="{px}" cy="{py}" r="{coin_r:.0f}" fill="{ink}" opacity="0.7"/>')

def nxn_thumbnail(entry, params):
    S = 400
    n = params.get('size', 3)
    cell = min(320 // n, 110)
    parts = thumbnail_shell(S)
    draw_nxn_grid(parts, S//2, S//2, cell, n, mode='thumb')
    parts.append('</svg>')
    return '\n'.join(parts)

def nxn_page1(entry, params):
    W, H = 816, 1056
    n = params.get('size', 3)
    cell = min(500 // n, 175)
    parts = page1_shell(entry)
    draw_nxn_grid(parts, W//2, 430, cell, n, mode='print', show_coords=(n >= 5))
    
    # Brief instruction
    brief = entry.get('modern_explanation', '')
    first_sentence = brief.split('.')[0] + '.' if '.' in brief else brief[:120]
    if len(first_sentence) > 100:
        first_sentence = first_sentence[:97] + '...'
    parts.append(f'  <text x="{W//2}" y="780" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="15" fill="{light}">{esc(first_sentence)}</text>')
    parts.append(f'  <text x="{W//2}" y="804" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="13" fill="{light}">See page 2 for full instructions.</text>')
    
    parts.append(f'  <text x="{W//2}" y="{H - 42}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="11" fill="{rule}">Heritage Parlor  ·  Page 1 of 2  ·  Turn over for full instructions</text>')
    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════════
# TEMPLATE 2: MORRIS / CONCENTRIC SQUARES
# ═══════════════════════════════════════════

def draw_morris(parts, cx, cy, size, variant='nine_mens', mode='thumb'):
    """Draw a Morris board (concentric squares with connection lines)."""
    s = size  # outer square half-width
    
    if variant == 'three_mens':
        rings = 1
    elif variant == 'six_mens':
        rings = 2
    else:
        rings = 3  # nine_mens, fox_and_geese
    
    ring_sizes = [s]
    for i in range(1, rings):
        ring_sizes.append(s * (rings - i) / rings)
    
    sw = 2 if mode == 'print' else 1.5
    dot_r = 6 if mode == 'print' else 5
    
    # Draw concentric squares
    for rs in ring_sizes:
        parts.append(f'  <rect x="{cx - rs:.0f}" y="{cy - rs:.0f}" width="{rs*2:.0f}" height="{rs*2:.0f}" fill="none" stroke="{ink}" stroke-width="{sw}" rx="1"/>')
    
    # Connection lines between rings (midpoints of sides)
    if rings > 1:
        for rs_outer, rs_inner in zip(ring_sizes[:-1], ring_sizes[1:]):
            # Top
            parts.append(f'  <line x1="{cx}" y1="{cy - rs_outer:.0f}" x2="{cx}" y2="{cy - rs_inner:.0f}" stroke="{ink}" stroke-width="{sw}"/>')
            # Bottom
            parts.append(f'  <line x1="{cx}" y1="{cy + rs_outer:.0f}" x2="{cx}" y2="{cy + rs_inner:.0f}" stroke="{ink}" stroke-width="{sw}"/>')
            # Left
            parts.append(f'  <line x1="{cx - rs_outer:.0f}" y1="{cy}" x2="{cx - rs_inner:.0f}" y2="{cy}" stroke="{ink}" stroke-width="{sw}"/>')
            # Right
            parts.append(f'  <line x1="{cx + rs_outer:.0f}" y1="{cy}" x2="{cx + rs_inner:.0f}" y2="{cy}" stroke="{ink}" stroke-width="{sw}"/>')
    
    # Intersection dots
    all_points = []
    for rs in ring_sizes:
        corners = [
            (cx - rs, cy - rs), (cx, cy - rs), (cx + rs, cy - rs),
            (cx - rs, cy), (cx + rs, cy),
            (cx - rs, cy + rs), (cx, cy + rs), (cx + rs, cy + rs),
        ]
        all_points.extend(corners)
    
    # Center point for three_mens
    if variant == 'three_mens':
        all_points.append((cx, cy))
        # Diagonals
        parts.append(f'  <line x1="{cx - s:.0f}" y1="{cy - s:.0f}" x2="{cx + s:.0f}" y2="{cy + s:.0f}" stroke="{ink}" stroke-width="{sw}"/>')
        parts.append(f'  <line x1="{cx + s:.0f}" y1="{cy - s:.0f}" x2="{cx - s:.0f}" y2="{cy + s:.0f}" stroke="{ink}" stroke-width="{sw}"/>')
    
    fill = ink if mode == 'thumb' else 'none'
    stroke_col = 'none' if mode == 'thumb' else ink
    for px, py in all_points:
        if mode == 'print':
            parts.append(f'  <circle cx="{px:.0f}" cy="{py:.0f}" r="{dot_r}" fill="none" stroke="{rule}" stroke-width="1" stroke-dasharray="4,3"/>')
        else:
            parts.append(f'  <circle cx="{px:.0f}" cy="{py:.0f}" r="{dot_r}" fill="{ink}" opacity="0.7"/>')

def morris_thumbnail(entry, params):
    S = 400
    parts = thumbnail_shell(S)
    variant = params.get('variant', 'nine_mens')
    draw_morris(parts, S//2, S//2, 140, variant, mode='thumb')
    parts.append('</svg>')
    return '\n'.join(parts)

def morris_page1(entry, params):
    W, H = 816, 1056
    parts = page1_shell(entry)
    variant = params.get('variant', 'nine_mens')
    draw_morris(parts, W//2, 420, 220, variant, mode='print')
    
    parts.append(f'  <text x="{W//2}" y="780" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="15" fill="{light}">Place pieces on any intersection point. See page 2 for rules.</text>')
    parts.append(f'  <text x="{W//2}" y="{H - 42}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="11" fill="{rule}">Heritage Parlor  ·  Page 1 of 2  ·  Turn over for full instructions</text>')
    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════════
# TEMPLATE 3: STAR / POLYGON
# ═══════════════════════════════════════════

def draw_star_polygon(parts, cx, cy, radius, points=5, star=True, mode='thumb'):
    """Draw a star or polygon with numbered positions at vertices and intersections."""
    dot_r = 7 if mode == 'print' else 5
    
    # Compute outer vertices
    vertices = []
    for i in range(points):
        angle = -math.pi / 2 + 2 * math.pi * i / points
        vx = cx + radius * math.cos(angle)
        vy = cy + radius * math.sin(angle)
        vertices.append((vx, vy))
    
    if star and points >= 5:
        # Draw star: connect every other vertex
        skip = 2 if points == 5 else 2
        for i in range(points):
            j = (i + skip) % points
            parts.append(f'  <line x1="{vertices[i][0]:.1f}" y1="{vertices[i][1]:.1f}" x2="{vertices[j][0]:.1f}" y2="{vertices[j][1]:.1f}" stroke="{ink}" stroke-width="{2 if mode=="print" else 1.5}"/>')
    else:
        # Draw polygon edges
        for i in range(points):
            j = (i + 1) % points
            parts.append(f'  <line x1="{vertices[i][0]:.1f}" y1="{vertices[i][1]:.1f}" x2="{vertices[j][0]:.1f}" y2="{vertices[j][1]:.1f}" stroke="{ink}" stroke-width="{2 if mode=="print" else 1.5}"/>')
        # Draw diagonals for triangles
        if points == 3:
            # Inner triangle medians or connection lines
            for i in range(3):
                mx = (vertices[(i+1)%3][0] + vertices[(i+2)%3][0]) / 2
                my = (vertices[(i+1)%3][1] + vertices[(i+2)%3][1]) / 2
                parts.append(f'  <line x1="{vertices[i][0]:.1f}" y1="{vertices[i][1]:.1f}" x2="{mx:.1f}" y2="{my:.1f}" stroke="{ink}" stroke-width="1" opacity="0.4"/>')
    
    # Vertex dots
    for i, (vx, vy) in enumerate(vertices):
        if mode == 'print':
            parts.append(f'  <circle cx="{vx:.1f}" cy="{vy:.1f}" r="{dot_r}" fill="none" stroke="{rule}" stroke-width="1" stroke-dasharray="4,3"/>')
        else:
            parts.append(f'  <circle cx="{vx:.1f}" cy="{vy:.1f}" r="{dot_r}" fill="{ink}" opacity="0.7"/>')
    
    # For stars, add intersection points
    if star and points >= 5 and mode == 'print':
        inner_r = radius * 0.38  # approximate inner pentagon radius for 5-pointed star
        for i in range(points):
            angle = -math.pi / 2 + 2 * math.pi * i / points + math.pi / points
            ix = cx + inner_r * math.cos(angle)
            iy = cy + inner_r * math.sin(angle)
            parts.append(f'  <circle cx="{ix:.1f}" cy="{iy:.1f}" r="{dot_r}" fill="none" stroke="{rule}" stroke-width="1" stroke-dasharray="4,3"/>')

def star_thumbnail(entry, params):
    S = 400
    points = params.get('points', 5)
    is_star = params.get('type', 'star') == 'star'
    parts = thumbnail_shell(S)
    draw_star_polygon(parts, S//2, S//2, 150, points, star=is_star, mode='thumb')
    parts.append('</svg>')
    return '\n'.join(parts)

def star_page1(entry, params):
    W, H = 816, 1056
    points = params.get('points', 5)
    is_star = params.get('type', 'star') == 'star'
    parts = page1_shell(entry)
    draw_star_polygon(parts, W//2, 420, 230, points, star=is_star, mode='print')
    
    parts.append(f'  <text x="{W//2}" y="780" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="15" fill="{light}">Place numbers or counters at each position. See page 2 for rules.</text>')
    parts.append(f'  <text x="{W//2}" y="{H - 42}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="11" fill="{rule}">Heritage Parlor  ·  Page 1 of 2  ·  Turn over for full instructions</text>')
    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════════
# TEMPLATE 4: CIRCLE ARRANGEMENT
# ═══════════════════════════════════════════

def draw_circle(parts, cx, cy, radius, positions=8, mode='thumb'):
    """Draw positions arranged in a circle."""
    dot_r = 8 if mode == 'print' else 6
    
    # Main circle (guide)
    parts.append(f'  <circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{ink}" stroke-width="{1.5 if mode=="print" else 1}" opacity="0.3"/>')
    
    # Position nodes
    for i in range(positions):
        angle = -math.pi / 2 + 2 * math.pi * i / positions
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        
        if mode == 'print':
            parts.append(f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="{dot_r + 4}" fill="{white}" stroke="{ink}" stroke-width="1.5"/>')
            parts.append(f'  <text x="{px:.1f}" y="{py + 4:.1f}" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{light}">{i + 1}</text>')
        else:
            parts.append(f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="{dot_r}" fill="{ink}" opacity="0.7"/>')
    
    # Center point
    if mode == 'print':
        parts.append(f'  <circle cx="{cx}" cy="{cy}" r="4" fill="{ink}" opacity="0.3"/>')

def circle_thumbnail(entry, params):
    S = 400
    positions = params.get('positions', 8)
    parts = thumbnail_shell(S)
    draw_circle(parts, S//2, S//2, 140, positions, mode='thumb')
    parts.append('</svg>')
    return '\n'.join(parts)

def circle_page1(entry, params):
    W, H = 816, 1056
    positions = params.get('positions', 8)
    parts = page1_shell(entry)
    draw_circle(parts, W//2, 430, 220, positions, mode='print')
    
    parts.append(f'  <text x="{W//2}" y="780" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="15" fill="{light}">Arrange counters at the numbered positions. See page 2 for the puzzle.</text>')
    parts.append(f'  <text x="{W//2}" y="{H - 42}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="11" fill="{rule}">Heritage Parlor  ·  Page 1 of 2  ·  Turn over for full instructions</text>')
    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════════
# TEMPLATE 5: CHESSBOARD
# ═══════════════════════════════════════════

def draw_chessboard(parts, cx, cy, cell_size, size=8, mode='thumb', pieces=None):
    """Draw a chessboard with alternating colors."""
    grid = cell_size * size
    gx = cx - grid // 2
    gy = cy - grid // 2
    
    # Board outline
    parts.append(f'  <rect x="{gx}" y="{gy}" width="{grid}" height="{grid}" fill="{board_fill}" stroke="{ink}" stroke-width="{2 if mode=="print" else 1.5}"/>')
    
    # Alternating dark squares
    for row in range(size):
        for col in range(size):
            if (row + col) % 2 == 1:
                sx = gx + col * cell_size
                sy = gy + row * cell_size
                parts.append(f'  <rect x="{sx}" y="{sy}" width="{cell_size}" height="{cell_size}" fill="{board_dark}"/>')
    
    # Grid lines
    for i in range(1, size):
        parts.append(f'  <line x1="{gx}" y1="{gy + i*cell_size}" x2="{gx + grid}" y2="{gy + i*cell_size}" stroke="{ink}" stroke-width="0.5" opacity="0.3"/>')
        parts.append(f'  <line x1="{gx + i*cell_size}" y1="{gy}" x2="{gx + i*cell_size}" y2="{gy + grid}" stroke="{ink}" stroke-width="0.5" opacity="0.3"/>')
    
    # Outer border
    parts.append(f'  <rect x="{gx}" y="{gy}" width="{grid}" height="{grid}" fill="none" stroke="{ink}" stroke-width="{2 if mode=="print" else 1.5}"/>')
    
    if mode == 'print':
        # Column labels
        for i in range(size):
            tx = gx + i * cell_size + cell_size // 2
            parts.append(f'  <text x="{tx}" y="{gy - 6}" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{light}">{chr(97+i)}</text>')
            parts.append(f'  <text x="{tx}" y="{gy + grid + 16}" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{light}">{chr(97+i)}</text>')
        # Row labels
        for i in range(size):
            ty = gy + i * cell_size + cell_size // 2 + 5
            parts.append(f'  <text x="{gx - 10}" y="{ty}" text-anchor="end" font-family="Georgia, serif" font-size="12" fill="{light}">{size - i}</text>')
            parts.append(f'  <text x="{gx + grid + 10}" y="{ty}" font-family="Georgia, serif" font-size="12" fill="{light}">{size - i}</text>')
    
    # Piece markers for thumbnail (geometric shapes instead of Unicode to avoid rendering issues)
    if mode == 'thumb' and pieces:
        positions_to_show = [(0, 0), (2, 4), (4, 1), (6, 5), (1, 6), (5, 3)]
        pr = cell_size * 0.28
        for r, c in positions_to_show[:min(4, size)]:
            if r < size and c < size:
                px = gx + c * cell_size + cell_size // 2
                py = gy + r * cell_size + cell_size // 2
                parts.append(f'  <circle cx="{px}" cy="{py}" r="{pr:.0f}" fill="{ink}" opacity="0.75"/>')
                parts.append(f'  <circle cx="{px}" cy="{py - pr*0.1:.0f}" r="{pr*0.65:.0f}" fill="{bg}" opacity="0.2"/>') 

def chess_thumbnail(entry, params):
    S = 400
    size = params.get('size', 8)
    cell = min(320 // size, 45)
    parts = thumbnail_shell(S)
    draw_chessboard(parts, S//2, S//2, cell, size, mode='thumb', pieces=params.get('pieces', []))
    parts.append('</svg>')
    return '\n'.join(parts)

def chess_page1(entry, params):
    W, H = 816, 1056
    size = params.get('size', 8)
    cell = min(540 // size, 65)
    parts = page1_shell(entry)
    draw_chessboard(parts, W//2, 420, cell, size, mode='print', pieces=params.get('pieces', []))
    
    parts.append(f'  <text x="{W//2}" y="800" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="15" fill="{light}">Use the board above with your own pieces. See page 2 for rules.</text>')
    parts.append(f'  <text x="{W//2}" y="{H - 42}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="11" fill="{rule}">Heritage Parlor  ·  Page 1 of 2  ·  Turn over for full instructions</text>')
    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════════
# TEMPLATE 6: GRAPH / CONNECTION
# ═══════════════════════════════════════════

def draw_graph(parts, cx, cy, radius, mode='thumb'):
    """Draw a generic graph/network diagram (nodes + edges).
    Since each graph puzzle is unique, this draws a representative pattern."""
    # Default: a bridge/crossing style with banks and islands
    nodes = [
        (cx - radius, cy - radius * 0.5, 'A'),
        (cx - radius, cy + radius * 0.5, 'B'),
        (cx, cy, 'C'),  # island
        (cx + radius, cy - radius * 0.5, 'D'),
        (cx + radius, cy + radius * 0.5, 'E'),
    ]
    
    edges = [(0,2), (1,2), (2,3), (2,4), (0,3), (1,4), (0,1), (3,4)]
    
    dot_r = 10 if mode == 'print' else 8
    
    # Edges
    for i, j in edges:
        parts.append(f'  <line x1="{nodes[i][0]:.0f}" y1="{nodes[i][1]:.0f}" x2="{nodes[j][0]:.0f}" y2="{nodes[j][1]:.0f}" stroke="{ink}" stroke-width="{2 if mode=="print" else 1.5}"/>')
    
    # Nodes
    for x, y, label in nodes:
        if mode == 'print':
            parts.append(f'  <circle cx="{x:.0f}" cy="{y:.0f}" r="{dot_r}" fill="{white}" stroke="{ink}" stroke-width="2"/>')
            parts.append(f'  <text x="{x:.0f}" y="{y + 4:.0f}" text-anchor="middle" font-family="Georgia, serif" font-size="12" font-weight="bold" fill="{ink}">{label}</text>')
        else:
            parts.append(f'  <circle cx="{x:.0f}" cy="{y:.0f}" r="{dot_r}" fill="{ink}" opacity="0.8"/>')

def graph_thumbnail(entry, params):
    S = 400
    parts = thumbnail_shell(S)
    draw_graph(parts, S//2, S//2, 120, mode='thumb')
    parts.append('</svg>')
    return '\n'.join(parts)

def graph_page1(entry, params):
    W, H = 816, 1056
    parts = page1_shell(entry)
    draw_graph(parts, W//2, 420, 200, mode='print')
    
    parts.append(f'  <text x="{W//2}" y="780" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="15" fill="{light}">Trace paths between nodes. See page 2 for the challenge.</text>')
    parts.append(f'  <text x="{W//2}" y="{H - 42}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="11" fill="{rule}">Heritage Parlor  ·  Page 1 of 2  ·  Turn over for full instructions</text>')
    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════════
# TEMPLATE 7: DISSECTION / CUTTING
# ═══════════════════════════════════════════

def draw_dissection(parts, cx, cy, size, mode='thumb', dtype='tangram'):
    """Draw a tangram or dissection puzzle."""
    s = size
    
    if dtype == 'tangram':
        # Classic tangram: square divided into 7 pieces
        # Outer square
        sq = s
        x0, y0 = cx - sq//2, cy - sq//2
        parts.append(f'  <rect x="{x0}" y="{y0}" width="{sq}" height="{sq}" fill="{board_fill}" stroke="{ink}" stroke-width="{2 if mode=="print" else 1.5}"/>')
        
        # Tangram cut lines
        # Diagonal
        parts.append(f'  <line x1="{x0}" y1="{y0}" x2="{x0+sq}" y2="{y0+sq}" stroke="{ink}" stroke-width="{2 if mode=="print" else 1.5}"/>')
        # Horizontal mid
        parts.append(f'  <line x1="{x0}" y1="{y0+sq//2}" x2="{x0+sq//2}" y2="{y0+sq//2}" stroke="{ink}" stroke-width="{2 if mode=="print" else 1.5}"/>')
        # Vertical half on right
        parts.append(f'  <line x1="{x0+sq//2}" y1="{y0+sq//2}" x2="{x0+sq}" y2="{y0+sq//2}" stroke="{ink}" stroke-width="{1.5 if mode=="print" else 1}"/>')
        # Inner diagonal
        parts.append(f'  <line x1="{x0+sq//4}" y1="{y0+sq//4}" x2="{x0+sq//2}" y2="{y0+sq//2}" stroke="{ink}" stroke-width="{1.5 if mode=="print" else 1}"/>')
        parts.append(f'  <line x1="{x0+sq//2}" y1="{y0}" x2="{x0+sq}" y2="{y0+sq//2}" stroke="{ink}" stroke-width="{1.5 if mode=="print" else 1}"/>')
        # Small triangle cut
        parts.append(f'  <line x1="{x0+sq//2}" y1="{y0+sq//2}" x2="{x0+sq*3//4}" y2="{y0+sq*3//4}" stroke="{ink}" stroke-width="{1.5 if mode=="print" else 1}"/>')
        parts.append(f'  <line x1="{x0+sq//2}" y1="{y0+sq}" x2="{x0+sq*3//4}" y2="{y0+sq*3//4}" stroke="{ink}" stroke-width="{1.5 if mode=="print" else 1}"/>')
        
        if mode == 'print':
            # Label pieces
            labels = [
                (x0 + sq*0.2, y0 + sq*0.65, '1'),
                (x0 + sq*0.15, y0 + sq*0.3, '2'),
                (x0 + sq*0.35, y0 + sq*0.42, '3'),
                (x0 + sq*0.75, y0 + sq*0.25, '4'),
                (x0 + sq*0.55, y0 + sq*0.55, '5'),
                (x0 + sq*0.55, y0 + sq*0.8, '6'),
                (x0 + sq*0.8, y0 + sq*0.7, '7'),
            ]
            for lx, ly, label in labels:
                parts.append(f'  <text x="{lx:.0f}" y="{ly:.0f}" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="{accent}" font-weight="bold">{label}</text>')
            # Scissors icon hint
            parts.append(f'  <text x="{cx}" y="{y0 + sq + 30}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="13" fill="{light}">✂ Cut along the lines to make 7 pieces</text>')
    else:
        # Generic dissection: a shape with cut lines
        # Draw a rectangle with diagonal and perpendicular cuts
        w, h = s, s * 0.7
        x0, y0 = cx - w//2, cy - h//2
        parts.append(f'  <rect x="{x0}" y="{y0}" width="{w}" height="{h:.0f}" fill="{board_fill}" stroke="{ink}" stroke-width="{2 if mode=="print" else 1.5}" rx="1"/>')
        # Some cut lines
        parts.append(f'  <line x1="{x0}" y1="{y0}" x2="{x0+w}" y2="{y0+h:.0f}" stroke="{ink}" stroke-width="{1.5 if mode=="print" else 1}" stroke-dasharray="8,4"/>')
        parts.append(f'  <line x1="{x0+w//3}" y1="{y0}" x2="{x0+w//3}" y2="{y0+h:.0f}" stroke="{ink}" stroke-width="{1.5 if mode=="print" else 1}" stroke-dasharray="8,4"/>')
        parts.append(f'  <line x1="{x0+w*2//3}" y1="{y0}" x2="{x0+w*2//3}" y2="{y0+h:.0f}" stroke="{ink}" stroke-width="{1.5 if mode=="print" else 1}" stroke-dasharray="8,4"/>')
        
        if mode == 'print':
            parts.append(f'  <text x="{cx}" y="{y0 + h + 30:.0f}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="13" fill="{light}">✂ Cut along the dashed lines, then reassemble</text>')

def dissection_thumbnail(entry, params):
    S = 400
    dtype = params.get('type', 'tangram')
    parts = thumbnail_shell(S)
    draw_dissection(parts, S//2, S//2, 280, mode='thumb', dtype=dtype)
    parts.append('</svg>')
    return '\n'.join(parts)

def dissection_page1(entry, params):
    W, H = 816, 1056
    dtype = params.get('type', 'tangram')
    parts = page1_shell(entry)
    draw_dissection(parts, W//2, 420, 400, mode='print', dtype=dtype)
    
    parts.append(f'  <text x="{W//2}" y="800" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="15" fill="{light}">Cut this page along the marked lines. See page 2 for the challenge.</text>')
    parts.append(f'  <text x="{W//2}" y="{H - 42}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="11" fill="{rule}">Heritage Parlor  ·  Page 1 of 2  ·  Turn over for full instructions</text>')
    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════════
# ROUTER — picks the right template for any entry
# ═══════════════════════════════════════════

TEMPLATE_FUNCS = {
    'nxn_grid':      (nxn_thumbnail, nxn_page1),
    'morris':        (morris_thumbnail, morris_page1),
    'star_polygon':  (star_thumbnail, star_page1),
    'circle':        (circle_thumbnail, circle_page1),
    'chessboard':    (chess_thumbnail, chess_page1),
    'graph':         (graph_thumbnail, graph_page1),
    'dissection':    (dissection_thumbnail, dissection_page1),
}

def generate_three_outputs(entry, template_type, params):
    """Generate thumbnail, page1, page2 SVGs for a single entry."""
    if template_type in TEMPLATE_FUNCS:
        thumb_fn, page1_fn = TEMPLATE_FUNCS[template_type]
        thumb = thumb_fn(entry, params)
        p1 = page1_fn(entry, params)
    else:
        # Fallback for non-diagram entries: simple title card
        thumb = make_title_thumbnail(entry)
        p1 = make_title_page1(entry)
    
    p2 = page2_content(entry)
    return thumb, p1, p2


# ═══════════════════════════════════════════
# FALLBACK — Title-card style for non-diagram games
# ═══════════════════════════════════════════

def make_title_thumbnail(entry):
    """Simple thumbnail with a decorative Victorian ornament."""
    S = 400
    parts = thumbnail_shell(S)
    
    # Decorative border
    parts.append(f'  <rect x="30" y="30" width="340" height="340" rx="4" fill="none" stroke="{ink}" stroke-width="1" opacity="0.2"/>')
    parts.append(f'  <rect x="40" y="40" width="320" height="320" rx="3" fill="none" stroke="{ink}" stroke-width="0.5" opacity="0.15"/>')
    
    # Category icon (simple geometric)
    cat = entry.get('category', '')
    if cat == 'card-game':
        # Spade symbol
        parts.append(f'  <text x="200" y="220" text-anchor="middle" font-family="serif" font-size="80" fill="{ink}" opacity="0.15">♠</text>')
    elif cat == 'magic-trick':
        parts.append(f'  <text x="200" y="220" text-anchor="middle" font-family="serif" font-size="80" fill="{ink}" opacity="0.15">✦</text>')
    elif cat in ('parlor-game', 'word-game'):
        parts.append(f'  <text x="200" y="220" text-anchor="middle" font-family="serif" font-size="80" fill="{ink}" opacity="0.15">❧</text>')
    elif cat == 'physical-game':
        parts.append(f'  <text x="200" y="220" text-anchor="middle" font-family="serif" font-size="80" fill="{ink}" opacity="0.15">⚡</text>')
    else:
        parts.append(f'  <text x="200" y="220" text-anchor="middle" font-family="serif" font-size="80" fill="{ink}" opacity="0.15">◆</text>')
    
    parts.append('</svg>')
    return '\n'.join(parts)

def make_title_page1(entry):
    """Title page with decorative framing for non-diagram games."""
    W, H = 816, 1056
    parts = page1_shell(entry)
    
    m = 80
    # Decorative Victorian frame
    parts.append(f'  <rect x="{m}" y="160" width="{W-m*2}" height="{H-320}" rx="4" fill="none" stroke="{ink}" stroke-width="1" opacity="0.15"/>')
    parts.append(f'  <rect x="{m+10}" y="170" width="{W-m*2-20}" height="{H-340}" rx="3" fill="none" stroke="{ink}" stroke-width="0.5" opacity="0.1"/>')
    
    # Large category ornament
    cat = entry.get('category', '')
    sym = {'card-game':'♠', 'magic-trick':'✦', 'parlor-game':'❧', 'word-game':'✎',
           'physical-game':'⚡', 'folk-game':'☘', 'scientific-recreation':'⚗'}.get(cat, '◆')
    parts.append(f'  <text x="{W//2}" y="420" text-anchor="middle" font-family="serif" font-size="120" fill="{ink}" opacity="0.08">{sym}</text>')
    
    # Quick-start summary
    brief = entry.get('modern_explanation', '')
    sentences = [s.strip() for s in brief.split('.') if s.strip()][:3]
    y = 500
    for s in sentences:
        for line in wrap_text(s + '.', max_chars=70):
            parts.append(f'  <text x="{W//2}" y="{y}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="16" fill="{ink}">{esc(line)}</text>')
            y += 24
        y += 8
    
    # Equipment needed
    equip = entry.get('equipment_needed', [])
    if equip:
        y += 20
        parts.append(f'  <text x="{W//2}" y="{y}" text-anchor="middle" font-family="&apos;Playfair Display&apos;, Georgia, serif" font-size="14" font-weight="bold" fill="{accent}">You will need:</text>')
        y += 24
        for item in equip[:6]:
            parts.append(f'  <text x="{W//2}" y="{y}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="14" fill="{light}">{esc(item)}</text>')
            y += 22
    
    parts.append(f'  <text x="{W//2}" y="{H - 42}" text-anchor="middle" font-family="&apos;Source Sans 3&apos;, Georgia, sans-serif" font-size="11" fill="{rule}">Heritage Parlor  ·  Page 1 of 2  ·  Turn over for full instructions</text>')
    parts.append('</svg>')
    return '\n'.join(parts)


# ═══════════════════════════════════════════
# TEST — Generate samples for each template
# ═══════════════════════════════════════════

if __name__ == '__main__':
    with open('/home/user/workspace/heritage_parlor/data/entries.json') as f:
        entries_list = json.load(f)
    entries_by_id = {e['id']: e for e in entries_list}
    
    with open('/home/user/workspace/heritage_parlor/data/template_map.json') as f:
        tmap = json.load(f)
    
    import os
    out_dir = '/home/user/workspace/heritage_parlor/template_samples'
    os.makedirs(out_dir, exist_ok=True)
    
    # Pick one sample from each template
    samples = {}
    for ttype in ['nxn_grid', 'morris', 'star_polygon', 'circle', 'chessboard', 'graph', 'dissection',
                   'card_layout', 'magic_sequence', 'rules_only', 'prop_checklist']:
        if tmap[ttype]:
            item = tmap[ttype][0]
            entry = entries_by_id.get(item['id'])
            if entry:
                samples[ttype] = (entry, item.get('params', {}))
    
    for ttype, (entry, params) in samples.items():
        print(f"\n--- {ttype}: {entry['title']} ---")
        if ttype in TEMPLATE_FUNCS:
            thumb, p1, p2 = generate_three_outputs(entry, ttype, params)
        else:
            thumb, p1, p2 = generate_three_outputs(entry, ttype, params)
        
        for suffix, svg in [('thumb', thumb), ('page1', p1), ('page2', p2)]:
            path = f'{out_dir}/{ttype}_{suffix}.svg'
            with open(path, 'w') as f:
                f.write(svg)
            print(f"  {suffix}: {len(svg):,} bytes → {path}")
    
    print(f"\nGenerated {len(samples) * 3} sample SVGs")
