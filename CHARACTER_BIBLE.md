# Character Bible — Neon Cat universe

Source of truth for every image / panel. If a prompt contradicts this file, this file wins.

## Roster (13 Nov, 5 references)

| ID | Who | Reference |
|---|---|---|
| `cat-rainbow` | Black cat, rainbow goggles, white headphones, red console, green bench, neon night | `assets/reference/original.png` |
| `cat-laurel` | Black cat, side profile, laurel wreath, white crescent eye, dark green hoodie with paw logo, bright green bg | `assets/reference/ref-cat-laurel.png` |
| `hooded-goggles` | Faceless black hooded figure, round mint-green goggles with sparkles, bright green bg | `assets/reference/ref-hooded-goggles.png` |
| `cat-bus` | Black cat, white tee + blue jeans, sitting on red bus seats at night, holding handheld, city lights | `assets/reference/ref-cat-bus.png` |

World / props:

| ID | What | Reference |
|---|---|---|
| `nulls-gear` | Flat-lay transparent retro hardware — NULLS, NULLBOY, NULLCAM, NULLSTATION MEMORY CARD — dark red bg | `assets/reference/ref-nulls-gear.png` |

**Locked, Mirel 13 Nov 16:50:** all four are MAIN characters — no side characters. And all of them, plus the NULLS gear, are also game objects in the console game (characters as in-game objects, gear as in-game items). No single main; the roster is the cast.

**Open, awaiting Mirel:** repo name — proposed `neon-cat-universe` (alt: `nulls-game`).

## Fixed per character — never change

Each character has its own fixed block in `character.json` (`characters.<id>.fixed`). The rules that hold across all of them:

- **Eyes:** never drawn as normal eyes. White crescent-moon shapes only — inside the goggles for `cat-rainbow`, directly on the face for `cat-laurel` / `cat-bus`.
- **Style:** flat colour + hard shadow, clean illustration. No photorealism, no text in the image (except device labels in `nulls-gear`), no watermark.
- **Format:** 1280×720, 16:9 landscape, unless a panel explicitly needs a different crop.

## Variable — only these may change per panel

1. `character` — one of the four above.
2. `fashion` — only for `cat-rainbow` (v1 hoodie / v2 varsity / v3 techwear / v4 denim retro). The other characters keep their outfit from their reference unless Mirel approves a variant.
3. `scene` — where he is, what is happening around him.
4. `pose_detail` — small pose change only. Head / goggles / headphones stay identical for that character.
5. `expression` — mood shown only through the crescent eyes (or goggle lenses for `hooded-goggles`).
6. `dialogue` — caption / speech, never baked into the image.
7. `camera` — wide / medium / close-up, same character scale.

## How to use

Every generation must go through `scripts/build_prompt.py`. It injects that character's fixed traits first, then fashion (if any), then the scene. Never write a freehand prompt that omits the fixed block — that is how the character drifts.

```bash
python3 scripts/build_prompt.py --character cat-rainbow --fashion v1-hoodie --scene "waiting for the night bus, console glowing" --panel 1
python3 scripts/build_prompt.py --character cat-laurel --scene "close-up portrait, bright green background"
python3 scripts/build_prompt.py --character hooded-goggles --scene "close-up portrait, bright green background"
python3 scripts/storyline.py storyline/example-storyline.yaml
```

## Fashions (cat-rainbow only)

- **v1-hoodie** — oversized black hoodie, rainbow drawstrings, small rainbow chest logo, baggy dark jeans, chunky white sneakers.
- **v2-varsity** — black/white varsity jacket, rainbow stripes on sleeves, white tee, black cargo pants, white high-tops.
- **v3-techwear** — black tactical vest, rainbow zipper, dark long sleeve, utility pants with straps, black boots with rainbow soles.
- **v4-denim-retro** — oversized dark denim jacket, rainbow patch on back, striped tee, beige cargo pants, retro sneakers.
