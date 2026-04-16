#!/usr/bin/env python3
"""
Heritage Parlor — Kit Cover Generator (Recraft API)

Generates illustrated cover images for each pre-built game kit.
Run once, commit the output PNGs.

Usage:
  RECRAFT_API_KEY=your-key python3 generate_covers.py

Output:
  svgs/covers/rainy-day.png
  svgs/covers/restaurant.png
  svgs/covers/road-trip.png
  svgs/covers/holiday-party.png
  svgs/covers/brain-teaser.png
"""
import os, sys, time, requests

API_KEY = os.environ.get("RECRAFT_API_KEY", "")
if not API_KEY:
    print("Error: Set RECRAFT_API_KEY environment variable.")
    print("Usage: RECRAFT_API_KEY=your-key python3 generate_covers.py")
    sys.exit(1)

API_URL = "https://external.api.recraft.ai/v1/images/generations"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svgs", "covers")
os.makedirs(OUTPUT_DIR, exist_ok=True)

KITS = [
    {
        "id": "rainy-day",
        "prompt": (
            "Victorian parlor interior illustration, warm sepia and brown ink-and-watercolor style on aged cream paper. "
            "A family gathered around a round table by a tall rain-streaked window, oil lamp glowing, playing a card game. "
            "Patterned wallpaper, heavy curtains, potted fern. Cozy and intimate atmosphere. "
            "Style of 1880s book illustration. Ornate decorative border with corner flourishes. No text or letters."
        ),
    },
    {
        "id": "restaurant",
        "prompt": (
            "Victorian restaurant illustration, warm sepia and brown ink-and-watercolor style on aged cream paper. "
            "Two elegantly dressed figures seated at a small round table with white tablecloth, candle, and teacups, "
            "playing a word game while waiting for dinner. Tiled floor, arched window, potted palm. "
            "Style of 1890s magazine illustration. Ornate decorative border with corner flourishes. No text or letters."
        ),
    },
    {
        "id": "road-trip",
        "prompt": (
            "Victorian travel illustration, warm sepia and brown ink-and-watercolor style on aged cream paper. "
            "Family inside an ornate railway carriage compartment, passing countryside through the window. "
            "Mother and children playing guessing games, father consulting a folded map. Luggage on overhead rack. "
            "Style of 1870s travel book illustration. Ornate decorative border with corner flourishes. No text or letters."
        ),
    },
    {
        "id": "holiday-party",
        "prompt": (
            "Victorian Christmas parlor illustration, warm sepia and brown ink-and-watercolor style on aged cream paper. "
            "Grand parlor with roaring fireplace, evergreen garlands and wreath, candles on mantelpiece. "
            "Large group of adults and children in festive dress playing parlor games, laughing. Christmas tree in corner. "
            "Style of 1880s holiday book illustration. Ornate decorative border with corner flourishes. No text or letters."
        ),
    },
    {
        "id": "brain-teaser",
        "prompt": (
            "Victorian scientific illustration, warm sepia and brown ink-and-watercolor style on aged cream paper. "
            "A study desk with geometric puzzles: tangram pieces, a compass and protractor, nested wooden boxes, "
            "an astrolabe, scattered puzzle cards, and a magnifying glass. Bookshelf in background. "
            "Style of 1890s scientific journal frontispiece. Ornate decorative border with corner flourishes. No text or letters."
        ),
    },
]

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def generate_cover(kit):
    kit_id = kit["id"]
    output_path = os.path.join(OUTPUT_DIR, f"{kit_id}.png")

    if os.path.exists(output_path):
        print(f"  Skipping {kit_id} (already exists)")
        return True

    print(f"  Generating {kit_id}...")

    payload = {
        "prompt": kit["prompt"],
        "style": "realistic_image",
        "model": "recraftv3",
        "size": "1024x1024",
        "response_format": "url",
    }

    try:
        resp = requests.post(API_URL, json=payload, headers=HEADERS, timeout=120)
        resp.raise_for_status()
        data = resp.json()

        image_url = data.get("data", [{}])[0].get("url")
        if not image_url:
            print(f"  Error: No image URL in response for {kit_id}")
            print(f"  Response: {data}")
            return False

        img_resp = requests.get(image_url, timeout=60)
        img_resp.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(img_resp.content)

        size_kb = len(img_resp.content) / 1024
        print(f"  Saved {kit_id}.png ({size_kb:.0f} KB)")
        return True

    except requests.exceptions.RequestException as e:
        print(f"  Error generating {kit_id}: {e}")
        return False


def main():
    print("Heritage Parlor — Kit Cover Generator")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Generating {len(KITS)} covers...\n")

    success = 0
    for i, kit in enumerate(KITS):
        if generate_cover(kit):
            success += 1
        if i < len(KITS) - 1:
            time.sleep(2)  # Rate limit courtesy

    print(f"\nDone: {success}/{len(KITS)} covers generated.")
    if success < len(KITS):
        print("Re-run to retry failed covers (existing files are skipped).")


if __name__ == "__main__":
    main()
