#!/usr/bin/env python3
"""Turn a storyline YAML into one locked prompt per panel.

Input YAML shape (see storyline/example-storyline.yaml):
    title: ...
    character: cat-rainbow
    fashion: v1-hoodie
    panels:
      - scene: ...
        character: ...   # optional, overrides the storyline default
        pose: ...        # optional
        mood: ...        # optional
        camera: ...      # optional
        dialogue: ...    # caption, never baked into the image

Output:
    prompts/<slug>-panels.json  — machine-readable prompts
    prompts/<slug>-panels.md    — human-readable, one panel per section

Usage:
    python3 scripts/storyline.py storyline/example-storyline.yaml
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from build_prompt import build  # noqa: E402


def parse_yaml(path):
    # Tiny dependency-free parser for this file's flat shape only.
    title = ""
    character = "cat-rainbow"
    fashion = ""
    panels = []
    current = None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        key, _, value = line.strip().partition(":")
        value = value.strip().strip('"').strip("'")
        if indent == 0 and key == "title":
            title = value
        elif indent == 0 and key == "character":
            character = value
        elif indent == 0 and key == "fashion":
            fashion = value
        elif indent == 2 and key == "- scene":
            current = {"scene": value}
            panels.append(current)
        elif indent == 4 and current is not None:
            current[key] = value
    return title, character, fashion, panels


def slugify(text):
    slug = "".join(c.lower() if c.isalnum() else "-" for c in text)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "storyline"


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 scripts/storyline.py storyline/<file>.yaml")
    src = Path(sys.argv[1])
    title, character, fashion, panels = parse_yaml(src)
    if not panels:
        raise SystemExit(f"no panels found in {src}")
    out_dir = ROOT / "prompts"
    out_dir.mkdir(exist_ok=True)
    slug = slugify(title or src.stem)
    result = []
    for i, panel in enumerate(panels, 1):
        panel_character = panel.get("character") or character
        prompt = build(panel_character, fashion or None, panel.get("scene", ""),
                       panel.get("pose") or None,
                       panel.get("mood") or None, panel.get("camera") or "medium shot")
        result.append({"panel": i, "character": panel_character, "fashion": fashion, "scene": panel.get("scene", ""),
                       "pose": panel.get("pose", ""), "mood": panel.get("mood", ""),
                       "camera": panel.get("camera", "medium shot"),
                       "dialogue": panel.get("dialogue", ""), "prompt": prompt})
    (out_dir / f"{slug}-panels.json").write_text(json.dumps(
        {"title": title, "character": character, "fashion": fashion, "panels": result}, indent=2, ensure_ascii=False), encoding="utf-8")
    md = [f"# {title}\n", f"Character: `{character}`  |  Fashion: `{fashion}`\n"]
    for r in result:
        md.append(f"## Panel {r['panel']} — {r['character']}\n\n**Scene:** {r['scene']}\n\n**Dialogue:** {r['dialogue'] or '—'}\n\n**Prompt:**\n\n{r['prompt']}\n")
    (out_dir / f"{slug}-panels.md").write_text("\n".join(md), encoding="utf-8")
    print(f"{len(result)} panels — character {character} fashion {fashion or '-'}")
    print(f"  prompts/{slug}-panels.json")
    print(f"  prompts/{slug}-panels.md")


if __name__ == "__main__":
    main()
