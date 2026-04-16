"""
Batch generate all 502×3 SVGs (thumbnail, page1, page2) for Heritage Parlor.
Outputs go to svgs/ directory organized by type.
"""
import json, os, sys, time

# Add parent dir to path for templates import
sys.path.insert(0, '/home/user/workspace/heritage_parlor')
from templates import generate_three_outputs

def main():
    # Load data
    with open('/home/user/workspace/heritage_parlor/data/entries.json') as f:
        entries_list = json.load(f)
    entries_by_id = {e['id']: e for e in entries_list}
    
    with open('/home/user/workspace/heritage_parlor/data/template_map.json') as f:
        tmap = json.load(f)
    
    # Create output directories
    base_dir = '/home/user/workspace/heritage_parlor/svgs'
    for subdir in ['thumbnails', 'page1', 'page2']:
        os.makedirs(f'{base_dir}/{subdir}', exist_ok=True)
    
    # Build lookup: entry_id -> (template_type, params)
    entry_template = {}
    for ttype, items in tmap.items():
        for item in items:
            entry_template[item['id']] = (ttype, item.get('params', {}))
    
    total = len(entries_list)
    generated = 0
    errors = []
    t0 = time.time()
    
    for i, entry in enumerate(entries_list):
        eid = entry['id']
        ttype, params = entry_template.get(eid, ('rules_only', {}))
        
        try:
            thumb, p1, p2 = generate_three_outputs(entry, ttype, params)
            
            with open(f'{base_dir}/thumbnails/{eid}.svg', 'w') as f:
                f.write(thumb)
            with open(f'{base_dir}/page1/{eid}.svg', 'w') as f:
                f.write(p1)
            with open(f'{base_dir}/page2/{eid}.svg', 'w') as f:
                f.write(p2)
            
            generated += 1
        except Exception as e:
            errors.append((eid, ttype, str(e)))
        
        if (i + 1) % 100 == 0:
            elapsed = time.time() - t0
            print(f"  {i+1}/{total} entries processed ({elapsed:.1f}s)")
    
    elapsed = time.time() - t0
    print(f"\nDone: {generated} entries × 3 = {generated * 3} SVGs in {elapsed:.1f}s")
    
    if errors:
        print(f"\n{len(errors)} errors:")
        for eid, ttype, err in errors:
            print(f"  {eid} ({ttype}): {err}")
    
    # Size report
    total_bytes = 0
    for subdir in ['thumbnails', 'page1', 'page2']:
        d = f'{base_dir}/{subdir}'
        count = len([f for f in os.listdir(d) if f.endswith('.svg')])
        size = sum(os.path.getsize(f'{d}/{f}') for f in os.listdir(d) if f.endswith('.svg'))
        total_bytes += size
        print(f"  {subdir}: {count} files, {size/1024:.0f} KB")
    print(f"  Total: {total_bytes/1024/1024:.1f} MB")

if __name__ == '__main__':
    main()
