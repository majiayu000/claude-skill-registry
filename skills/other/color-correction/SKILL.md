---
name: color-correction
description: Diagnose and fix video/image color OBJECTIVELY with the analyze_color tool (scopes/stats — black/white points, contrast, saturation, clipping, cast) instead of eyeballing a contact sheet. Covers the "washed out" signature, why reference color-match (mkl/ColorMatch/ColorMatchAdobe) CAN'T add contrast a flat source lacks, the levels/contrast-stretch fix (core AdjustContrast / CurveEditor), the measure→fix→re-measure loop, the side-by-side sandbox pattern, and where to place the fix in a render graph (after decode, before save). Use when a render looks washed out / flat / dull / over-saturated / color-cast, or when deciding between a color-match and a contrast/levels fix.
globs:
  - "**/*.json"
  - "**/packs/**"
---

# Color Correction (measure, don't eyeball)

## The core principle

**You cannot reliably judge color from a storyboard / contact sheet.** "Is it washed
out?" flip-flops by eye, especially on AI-gen video. Make color **measurable** with the
`analyze_color` MCP tool, read the numbers like a colorist reads scopes, then pick the
fix the data points to — and re-measure to confirm. The whole skill is this loop:

```
extract a frame ─► analyze_color ─► read black/white points + contrast + saturation
       ▲                                          │
       │                                          ▼
   re-measure  ◄──── apply fix (levels / contrast / match) ◄── diagnose from the numbers
```

> Origin: on a WAN-Animate render we argued for many turns over whether the clip was
> "washed out." The instant we measured it, the answer was unambiguous and the *correct*
> fix (a contrast stretch, NOT the color-match nodes we'd been adding) fell straight out.

---

## The `analyze_color` tool

Read-only. Source = `asset_id`, a ComfyUI output ref (`filename`/`subfolder`/`type`), or
an image `path` (absolute, or under the output dir). It returns per-image stats + heuristic
flags + a one-line verdict, and (optional) an overlaid R/G/B/luma **histogram PNG**.

```
analyze_color({ filename: "render_00007_.png" })                 # absolute numbers
analyze_color({ path: "frame.png", reference_path: "src.jpg" })  # + shot-match deltas
analyze_color({ filename: "x.png", histogram: true })            # + histogram image
```

**Videos:** `analyze_color` is image-only (no ffmpeg dep). Extract a frame first with the
ComfyUI venv's cv2:

```bash
"<comfy-venv>/python" -c "import cv2; c=cv2.VideoCapture(r'IN.mp4'); n=int(c.get(7)); \
  c.set(1, n//2); _,f=c.read(); cv2.imwrite(r'frame.png', f)"
```

(grab the middle frame, or frame 0; for window-drift checks grab a frame from each window.)

### What the numbers mean (8-bit)

| Field | Reads like a scope | Healthy-ish |
|---|---|---|
| `luma.blackPoint` (1st pct) | where shadows bottom out | ~0–16 (lifted if >16) |
| `luma.whitePoint` (99th pct) | where highlights top out | ~240–255 (dim if <235) |
| `luma.contrast` (std) | overall punch | ~45+ (flat if <45) |
| `luma.dynamicRange` | white−black | wide is good |
| `saturation.meanSaturation` (HSV S) | vectorscope spread | ~0.25+ (dull if <0.22) |
| `channels.{r,g,b}Mean` + `castHint` | RGB parade / white balance | spread <~12 = neutral |
| `luma.clippedHighPct/LowPct` | blown / crushed pixels | keep low (<~2%) |

Flags: `washedOut, lowContrast, liftedBlacks, dimHighlights, lowSaturation, colorCast`.

---

## The "washed out" signature

Washed out = **compressed tonal range**, and it has an exact fingerprint:

- `whitePoint` well below 255 (e.g. **191**) — highlights never reach white
- `blackPoint` lifted off 0 (e.g. **45**) — milky shadows
- `contrast` low (std < 45)
- often *normal* saturation — **washout is usually NOT a saturation problem.**

If you see that, the fix is a **levels / contrast stretch**, not a color match. (Real case:
a WAN-Animate frame measured blackPoint 45 / whitePoint 191 / contrast 43 — clearly a range
problem; saturation 0.25 was fine.)

---

## The load-bearing insight: a reference-match can't add contrast the source lacks

The instinct is to "match the render to the input photo" with a color-match node
(`ColorMatchV2` mkl/hm, `ImageColorMatchAdobe+`, easy `imageColorMatch`). **Measure the
reference first.** If the reference is itself flat (e.g. a casual phone selfie:
blackPoint 40, contrast 44), matching to it **cannot** produce punch — you'll match your way
to the *same* flat numbers. In the real case, mkl and Adobe matches both left the frame
flagged `washedOut` (whitePoint only crept 191→~218).

So:

- **Use a reference-match** (`ColorMatchV2`, `ImageColorMatchAdobe+`) when you want to *match
  a known-good graded frame / shot-match across clips*, and the reference is actually good.
- **Use a levels / contrast stretch** when the defect is compressed range (the washout case)
  — it targets full range *regardless* of the reference. This is usually the real fix.

---

## The fix: contrast / levels stretch (core nodes, no install)

`AdjustContrast` (core `comfy_extras.nodes_dataset`, category *image/adjustments*) — one
`factor` (1.0 = none, >1 = more). Pivots around mid-gray, so it pushes the white point up
and the black point down together. Tune it **by measurement**, not feel. Real measured sweep
on the washout frame:

| factor | blackPoint | whitePoint | contrast | sat | clippedHigh | verdict |
|---|---|---|---|---|---|---|
| 1.3 | 29 | 239 | 56 | 0.33 | **0%** | ✅ not washed (slightly soft) |
| ~1.4 | ~20 | ~247 | ~60 | ~0.38 | ~1–2% | ✅ **sweet spot** |
| 1.6 | 7 | 254 | 67 | 0.44 | **7.2%** ⚠️ | punchy but blows highlights |

Pick the factor that lands **whitePoint ~248–255 with `clippedHighPct` < ~2%**. Going too far
(1.6 here) blows highlights *and* over-warms (per-channel contrast drops blue more than red →
`castHint` worsens). Sweet spot was ~1.4.

Other levers when contrast alone isn't enough:
- `CurveEditor` (core, *utilities*) → feeds a CURVE for precise black/white-point + gamma
  control (a true levels curve) when you need more than a single contrast pivot.
- `AdjustContrast` + a small saturation/brightness adjust (same *image/adjustments* family)
  to fine-tune after the stretch.
- A **mild** reference-match *after* the stretch only if you genuinely need to shot-match.

---

## The sandbox pattern (test corrections side by side, then measure)

Don't tune blind on the full pipeline. Build a tiny separate workflow (`panel_new_workflow`)
and let one run produce several candidates you then measure:

```
LoadImage (the washed frame, staged into input/)
LoadImage (the reference, if shot-matching)
        │
        ├─► AdjustContrast factor 1.3 ─► SaveImage "contrast13"
        ├─► AdjustContrast factor 1.6 ─► SaveImage "contrast16"
        ├─► ColorMatchV2 (mkl, ref)   ─► SaveImage "balance_mkl"
        └─► ImageColorMatchAdobe+(LAB)─► SaveImage "balance_adobe"
```

Run once, then `analyze_color` **every** output (+ the reference + the untouched frame) and
compare blackPoint / whitePoint / contrast / saturation / clippedHigh. Whichever lands the
numbers in range wins; interpolate the factor (1.3 vs 1.6 → 1.4) and confirm with one more
pass. Stage the frame into the ComfyUI **input** dir first (cp the extracted PNG there) so
`LoadImage` can see it — input/output dirs may be custom, so don't guess paths.

---

## Porting the fix into a render graph

Place the chosen correction **after decode, before the save** — for a WAN/video graph that's
right after `WanVideoDecode` (or the per-chunk color-match) and feeding the
`VHS_VideoCombine`/save node. One `AdjustContrast` node is usually the whole fix; keep it as a
single inline node (or a small bypassable group) so it's easy to toggle and re-tune. Re-render
a clip, extract a frame, `analyze_color` it, and nudge the factor to hit whitePoint ~250.

---

## Video-specific gotchas

- **Per-window drift (WAN long video):** WAN-Animate/long clips render in temporal windows and
  can desaturate/dim across them. Measure a frame from the *first* window and a *late* window —
  if they differ, that's drift, not a global grade issue (use the embeds' between-window
  `colormatch`, not a final stretch).
- **Relight LoRA ≠ levels:** a WanAnimate relight LoRA changes *lighting*, not black/white
  points — it won't fix a compressed-range washout. Measure before and after to prove it.
- **Don't over-stretch:** watch `clippedHighPct` — blown highlights are unrecoverable. Prefer
  the lower factor that still clears `dimHighlights`.
- **Cast is often inherited:** if the reference has the same warm/cool cast (festival/sunset
  light), a matching cast on the render is *correct* — don't "fix" it.

---

## Quick reference — the decision tree

```
analyze_color the frame
  ├─ washedOut / lowContrast / dimHighlights ........ contrast/levels stretch (AdjustContrast ~1.4 → measure)
  ├─ lowSaturation only ............................. saturation boost (small)
  ├─ colorCast (and reference is neutral) ........... white-balance / neutralization, or reference-match
  ├─ want to MATCH a known-good graded frame ........ ColorMatchV2 / ImageColorMatchAdobe+ (ref must be good)
  └─ blackPoint/whitePoint already 0/255, sat ok .... color is healthy — stop touching it
```

Always **re-measure after the fix.** If `analyze_color` still flags it, the fix was wrong —
adjust and measure again. Numbers over vibes.
