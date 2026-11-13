# Neon Cat universe — consistent characters for storylines

Black cat + hooded figure, night city, retro handheld gaming.
Same characters, same styles in every panel — only the fashion / scene changes.

## Status

Draft v0.4.0 — 13 Nov 2026. All four characters are MAIN characters, and all of them + the NULLS gear are also game objects in the console game. Per-character fashion variants added: laurel-varsity, hooded-techwear, bus-hoodie.

| ID | Who | Reference |
|---|---|---|
| `cat-rainbow` | Black cat, rainbow goggles, white headphones, red console, green bench, neon night | `assets/reference/original.png` |
| `cat-laurel` | Black cat, laurel wreath, white crescent eye, dark green paw hoodie, bright green bg | `assets/reference/ref-cat-laurel.png` |
| `hooded-goggles` | Faceless hooded figure, round mint goggles with sparkles, bright green bg | `assets/reference/ref-hooded-goggles.png` |
| `cat-bus` | Black cat, white tee + blue jeans, red bus seats at night, city lights | `assets/reference/ref-cat-bus.png` |
| `nulls-gear` | World / props: transparent retro hardware — NULLS, NULLBOY, NULLCAM, NULLSTATION | `assets/reference/ref-nulls-gear.png` |

Fashion variants for `cat-rainbow` (generated 13 Nov):

- V1 Hoodie — `assets/variants/v1-hoodie.webp`
- V2 Varsity — `assets/variants/v2-varsity.webp`
- V3 Techwear — `assets/variants/v3-techwear.webp`
- V4 Denim retro — `assets/variants/v4-denim-retro.webp`

Push target: `musegodz` only, never `zannyzette`.

## Files

| File | What it is |
|---|---|
| `CHARACTER_BIBLE.md` | Fixed traits per character. Source of truth. |
| `character.json` | Same bible, machine-readable. |
| `characters/*.md` | One file per character. |
| `world/*.md` | World / props. |
| `fashions/*.md` | One file per fashion variant (cat-rainbow only). |
| `scripts/build_prompt.py` | Builds a locked, consistent prompt for one panel. |
| `scripts/storyline.py` | Turns a storyline YAML into one prompt per panel. |
| `storyline/example-storyline.yaml` | 3-panel example. |

## Quick start

```bash
# one panel
python3 scripts/build_prompt.py --character cat-rainbow --fashion v1-hoodie --scene "waiting for the night bus, console glowing"
python3 scripts/build_prompt.py --character cat-laurel --scene "close-up portrait, bright green background"

# a whole storyline (outputs prompts/storyline-panels.json + .md)
python3 scripts/storyline.py storyline/example-storyline.yaml
```

Use the generated prompt + that character's reference image in `assets/reference/` as the image input every time. That pair is what keeps the character consistent.

## Rule

Never generate from a freehand prompt. Always go through `build_prompt.py` — it puts the fixed traits first, so the character cannot drift.
