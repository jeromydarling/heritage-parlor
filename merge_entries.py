import json
import sys
sys.path.insert(0, '/home/user/workspace/heritage_parlor')

# Import all entry lists
exec(open('/home/user/workspace/heritage_parlor/gomme1_entries.py').read())
exec(open('/home/user/workspace/heritage_parlor/gomme2_carroll_entries.py').read())
exec(open('/home/user/workspace/heritage_parlor/sociable_entries.py').read())
exec(open('/home/user/workspace/heritage_parlor/hoffmann_entries.py').read())
exec(open('/home/user/workspace/heritage_parlor/magician_entries.py').read())

# Load existing titles for deduplication
with open('/home/user/workspace/heritage_parlor/data/entries.json') as f:
    existing = json.load(f)

existing_titles = set(e['title'].lower().strip() for e in existing)
existing_ids = set(e.get('id', '') for e in existing)

# Combine all new entries
all_new = (
    gomme1_entries + 
    gomme2_entries + 
    carroll_entry + 
    sociable_entries + 
    hoffmann_entries + 
    magician_entries
)

print(f"Total new entries before deduplication: {len(all_new)}")

# Normalize field names to match schema exactly
# The schema uses: equipment (not equipment_needed), original_description, modern_description
def normalize_entry(e, entry_num):
    """Ensure all required fields present and properly named"""
    normalized = {
        "id": e.get("id", ""),
        "slug": e.get("slug", e.get("id", "")),
        "title": e.get("title", ""),
        "source_book": e.get("source_book", ""),
        "source_author": e.get("source_author", ""),
        "source_year": e.get("source_year", 0),
        "source_url": e.get("source_url", ""),
        "category": e.get("category", ""),
        "subcategory": e.get("subcategory", ""),
        "tags": e.get("tags", []),
        "difficulty": e.get("difficulty", "beginner"),
        "players": e.get("players", ""),
        "equipment": e.get("equipment", []),
        "family_friendly": e.get("family_friendly", True),
        "original_description": e.get("original_description", ""),
        "modern_description": e.get("modern_description", ""),
        "fun_fact": e.get("fun_fact", ""),
        "image_prompt": e.get("image_prompt", ""),
        "entry_number": entry_num
    }
    return normalized

# Deduplicate and normalize
final_entries = []
seen_ids = set()
seen_titles = set(existing_titles)  # Start with existing titles
skipped = []

for entry in all_new:
    title_lower = entry['title'].lower().strip()
    entry_id = entry.get('id', '')
    
    # Check for duplicates against existing DB
    if title_lower in seen_titles:
        skipped.append(f"DUPE AGAINST EXISTING: {entry['title']}")
        continue
    
    # Check for duplicates within new entries
    if entry_id in seen_ids:
        skipped.append(f"DUPE WITHIN NEW: {entry['title']}")
        continue
    
    seen_ids.add(entry_id)
    seen_titles.add(title_lower)
    final_entries.append(entry)

# Number entries starting from 363
numbered_entries = []
for i, entry in enumerate(final_entries, start=363):
    numbered_entries.append(normalize_entry(entry, i))

print(f"\nSkipped ({len(skipped)}):")
for s in skipped:
    print(f"  {s}")

print(f"\nFinal new entries: {len(numbered_entries)}")

# Count by source book
from collections import Counter
source_counts = Counter(e['source_book'] for e in numbered_entries)
print("\nBy source book:")
for book, count in sorted(source_counts.items()):
    print(f"  {count:3d} - {book}")

category_counts = Counter(e['category'] for e in numbered_entries)
print("\nBy category:")
for cat, count in sorted(category_counts.items()):
    print(f"  {count:3d} - {cat}")

# Save to file
output_path = '/home/user/workspace/heritage_parlor/data/new_entries.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(numbered_entries, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(numbered_entries)} entries to {output_path}")

# Save source counts for stats
with open('/tmp/stats_data.json', 'w') as f:
    json.dump({
        'total': len(numbered_entries),
        'source_counts': dict(source_counts),
        'category_counts': dict(category_counts),
        'skipped': skipped
    }, f, indent=2)
