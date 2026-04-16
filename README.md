# Heritage Parlor

**502 Victorian-era parlor games, magic tricks, puzzles, and amusements from thirteen public domain books (1857–1917).**

Every game includes modern plain-English instructions, a unique SVG illustration, and a two-page printable game sheet — so families can play without a phone.

## Live Demo

**Current deployment**: [Heritage Parlor](https://www.perplexity.ai/computer/a/heritage-parlor-8CixAQq1RIK1sbSeKL4eGQ)

## What's Here

- **502 games** across 9 categories: parlor games, card games, magic tricks, puzzles, word games, physical games, board games, folk games, and scientific recreations
- **1,506 SVGs**: unique thumbnail + two-page printable sheet per game
- **36 DIY build guides** with Heritage Skills crosslinks
- **36 artisan commission specs** (Fabrica) with materials, dimensions, and pricing
- **Community features**: game suggestions, submit a game, themed game night menus
- **Dark mode**, responsive design, search, filtering by category and playability

## Data

All game data lives in `data/entries.json`. Each entry includes:
- Original Victorian-era description from the source book
- Modern how-to-play explanation
- Historical fun fact
- Player count, difficulty, play duration
- Playability rating (playable now → extinct equipment)
- Category and subcategory
- Source book attribution with Gutenberg link

## Source Books

Thirteen books, all public domain:
- Cassell's Book of In-door Amusements (1881)
- The Book of Indoor and Outdoor Games (1904)
- What Shall We Do Now? (1907)
- Games for Everybody (1905)
- The American Boy's Handy Book (1882)
- Amusements in Mathematics (1917)
- The Magician's Own Book (1857)
- And six more...

## Project Spec

See [SPEC.md](SPEC.md) for the full product specification, including Phase 2 plans (auth, database, commerce, admin dashboard).

## Setup

No build step. Open `index.html` in a browser, or serve with any static file server:

```bash
python -m http.server 8000
```

## SVG Regeneration

To regenerate all SVGs:

```bash
python batch_generate_svgs.py
```

Requires: `templates.py` (diagram templates) and `svg_illustrations.py` (scene illustrations).

## License

All game content is public domain. Code is MIT.
