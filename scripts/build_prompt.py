#!/usr/bin/env python3
"""Build a locked, consistent prompt for one panel.

Fixed traits for the chosen character always come first (from
character.json), then the fashion (cat-rainbow only), then the scene.
This order is what keeps the character from drifting between panels.

Usage:
    python3 scripts/build_prompt.py --character cat-rainbow --fashion v1-hoodie \
        --scene "waiting for the night bus, console glowing" --panel 1
    python3 scripts/build_prompt.py --character cat-laurel \
        --scene "close-up portrait, bright green background"
    python3 scripts/build_prompt.py --character hooded-goggles \
        --scene "close-up portrait, bright green background"
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_POSES = {
    "cat-rainbow": "sitting centred on a green bench, legs apart, looking down at the console",
    "cat-laurel": "side profile, head turned slightly toward camera",
    "hooded-goggles": "close-up portrait, facing camera",
    "cat-bus": "sitting on red bus seats, legs apart, looking down at the handheld",
}


def load_character():
    with open(ROOT / "character.json", encoding="utf-8") as f:
        return json.load(f)


def build(character, fashion, scene, pose=None, mood=None, camera="medium shot"):
    data = load_character()
    try:
        char = data["characters"][character]
    except KeyError:
        raise SystemExit(f"unknown character {character!r}; choose one of {sorted(data['characters'])}")
    fixed = char["fixed"]
    parts = [fixed]
    if fashion:
        try:
            f = data["fashions"][fashion]
        except KeyError:
            raise SystemExit(f"unknown fashion {fashion!r}; choose one of {sorted(data['fashions'])}")
        if "character" in f and f["character"] != character:
            raise SystemExit(f"fashion {fashion!r} belongs to {f['character']}, not {character}")
        outfit = f["outfit"]
        parts.append(f"Fashion (change ONLY this): {outfit}.")
    else:
        parts.append(f"Outfit: {char['outfit']}.")
    parts.append(f"Pose: {pose or DEFAULT_POSES.get(character, 'as in the reference')}.")
    parts.append(f"Camera: {camera}.")
    if mood:
        parts.append(f"Mood shown only through the crescent eyes / goggle lenses: {mood}.")
    if scene:
        parts.append(f"Scene: {scene}.")
    parts.append(f"Reference image: {char['reference']}.")
    return " ".join(parts)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--character", default="cat-rainbow",
                   help="cat-rainbow | cat-laurel | hooded-goggles | cat-bus")
    p.add_argument("--fashion", default="",
                   help="v1-hoodie | v2-varsity | v3-techwear | v4-denim-retro (cat-rainbow) | laurel-varsity | hooded-techwear | bus-hoodie")
    p.add_argument("--scene", default="", help="what is happening in this panel")
    p.add_argument("--pose", default="", help="small pose change, head/goggles/headphones stay identical")
    p.add_argument("--mood", default="", help="e.g. happy, tired, focused")
    p.add_argument("--camera", default="medium shot")
    p.add_argument("--panel", default="1")
    args = p.parse_args()
    prompt = build(args.character, args.fashion or None, args.scene,
                   args.pose or None, args.mood or None, args.camera)
    print(f"--- Panel {args.panel} | character={args.character} fashion={args.fashion or '-'} ---")
    print(prompt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
