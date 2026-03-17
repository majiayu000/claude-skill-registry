---
name: digipop-coloring-book-creation
description: |
  **DEPRECATED** — Use `creating-coloring-books` instead.
  This skill uses an outdated workflow (Pixabay sourcing, local potrace).
  The replacement skill uses Google Images → screenshot → fal.ai Qwen + Recraft.
  Do not use this skill for new coloring book work.
---

# DigiPop Coloring Book Creation Pipeline

6-phase pipeline that transforms curated source illustrations into print-ready
coloring book pages. **We do NOT generate art from scratch** — we find great
existing illustrations and convert them.

## Pipeline Overview

```
Phase 1: Research     → find 20+ candidate illustrations
Phase 2: Vectorize    → raster → SVG via fal.ai
Phase 3: Line Art     → extract clean outlines
Phase 4: Cleanup      → pure black/white, print-ready
Phase 5: QA           → independent agent inspection
Phase 6: Upload       → gallery for human review
         ── PAUSE ──  → Carrie approves / rejects
```

## Phase 1: Research (Art Search Agent)

**Goal:** Find 20+ illustrations that would make excellent coloring pages.

**Model requirement:** Use a strong visual model (Gemini 3 Pro or GLM-4-6v) for
image evaluation — the agent must SEE the candidates to score them.

### Source Strategy

Search broadly across free/open illustration sources. Be creative:
- Stock illustration sites (Unsplash, Pexels, Pixabay — illustration filters)
- Open clipart repositories (OpenClipart, SVG Repo, Wikimedia Commons)
- Creative Commons illustration archives
- Public domain art collections
- DeviantArt (CC-licensed), Behance (reference only)
- Pinterest (reference/discovery only — do not scrape)
- Theme-specific fan art communities (with licensing check)

**Future:** Source list may be locked to proven reliable sites after iteration.

### Candidate Scoring

Rate each image 1-10 on these axes:

| Axis | Weight | What to look for |
|------|--------|-------------------|
| Coloring compatibility | 3x | Clear outlines, distinct regions, no tiny details that disappear at print |
| Stylistic flair | 2x | Interesting composition, dynamic poses, visual appeal |
| Subject clarity | 2x | Single clear subject or well-separated scene elements |
| Line clarity | 2x | Clean edges, vector-like quality, minimal texture/noise |
| Print readiness | 1x | Will it look good at 8.5x11? Landscape or portrait? |

```
CandidateScore = (compat * 3 + flair * 2 + clarity * 2 + lines * 2 + print * 1) / 10
```

**Threshold:** Accept candidates scoring ≥ 6.0. Target 20+ candidates so ~10
survive through QA.

### Output

Save to `{bundle_dir}/research/`:
- `candidates.json` — array of `{url, source, license, scores, total_score, notes}`
- `thumbnails/` — downloaded preview of each candidate
- `research-report.md` — summary with top picks and rationale

## Phase 2: Vectorization (Tracing Agent)

**Goal:** Convert accepted raster candidates to clean SVG.

### fal.ai Vectorization Endpoints (pick best per image)

| Endpoint | Best for | Notes |
|----------|----------|-------|
| `fal-ai/recraft/vectorize` | Illustrations with solid colors | Recraft's vectorizer, good color separation |
| `fal-ai/star-vector` | Complex illustrations | AI vectorization preserving visual detail |
| `fal-ai/image2svg` | Clean graphics, logos | Precise control over detail levels |

### Process

1. Download full-res source image
2. Run through vectorization endpoint
3. Save SVG output to `{bundle_dir}/vectorized/`
4. Save `{filename}.meta.json` with: source_url, endpoint_used, parameters, timestamp
5. Visual diff check: does the SVG faithfully represent the source?

### Selection Heuristic

- Source is already SVG/vector → skip this phase, use directly
- Source has clean solid colors → `recraft/vectorize`
- Source is complex illustration → `star-vector`
- Source is simple graphic → `image2svg`

## Phase 3: Line Art Extraction

**Goal:** Extract clean black outlines from vectorized illustrations.

### Primary Tool: fal.ai Line Art Preprocessor

Endpoint: `fal-ai/image-preprocessors/lineart`

This extracts line art from any image — feed it the vectorized SVG rendered
as PNG, or the original raster if vectorization wasn't needed.

### Alternative: Local Processing

If fal.ai lineart doesn't produce clean enough output, fall back to local
processing with Python/Pillow:

```python
# Edge detection + threshold approach
from PIL import Image, ImageFilter
img = Image.open(path).convert('L')
edges = img.filter(ImageFilter.FIND_EDGES)
bw = edges.point(lambda x: 0 if x > threshold else 255)
```

### Output Spec

- Pure black lines on white background
- Target stroke weight: visible at 8.5x11 print (minimum ~2px at 300dpi)
- No gray, no gradients, no fills
- Save as PNG (3300x2550 for landscape, 2550x3300 for portrait)
- Save to `{bundle_dir}/lineart/`

## Phase 4: Cleanup

**Goal:** Production-ready coloring pages. Should look amazing/perfect.

### Cleanup Steps

1. **Binarize:** Strict black/white threshold (no gray pixels)
2. **Stroke normalization:** Ensure consistent line weight across the page
3. **Artifact removal:** Remove stray dots, broken lines, noise
4. **Border cleanup:** Clean margins, no edge artifacts
5. **Resolution normalize:** Scale to exactly 3300x2550 (landscape) or 2550x3300 (portrait) at 300dpi
6. **Format:** Save as PNG + companion SVG if available

### QA Metrics (automated pre-check before Phase 5)

| Metric | Pass Criteria |
|--------|---------------|
| Black pixel ratio | 2% – 15% of total pixels |
| Gray pixels | Exactly 0 |
| Min connected component | No isolated dots < 5px |
| Stroke continuity | No broken lines (gaps < 3px) |
| Margin clearance | ≥ 50px clear border on all sides |

Save to `{bundle_dir}/cleaned/`

## Phase 5: QA (Independent Agent)

**Goal:** Every page independently inspected by a visual model agent.

**Critical:** The QA agent must be a SEPARATE agent/session from the one that
produced the art. Fresh eyes, no confirmation bias.

### QA Checklist (visual inspection via Gemini/GLM)

1. **Is this a good coloring page?** Would a person enjoy coloring this?
2. **Line quality:** Are lines clean, consistent, unbroken?
3. **Complexity balance:** Not too sparse (boring), not too dense (frustrating)?
4. **Subject recognizability:** Can you tell what the image depicts?
5. **Colorable regions:** Are there clear, bounded regions to color in?
6. **Print artifacts:** Any visual glitches, moiré, or rendering errors?
7. **Age appropriateness:** Suitable for target audience?

### Scoring

Each criterion scored 1-5. Page passes if:
- No criterion scores below 3
- Average score ≥ 3.5
- "Is this a good coloring page?" scores ≥ 4

### Output

- `{bundle_dir}/qa/qa-report.json` — per-page scores and notes
- `{bundle_dir}/qa/qa-summary.md` — human-readable summary
- Pages that fail are moved to `{bundle_dir}/qa/rejected/` with rejection reason

## Phase 6: Upload to Gallery

**Goal:** Upload passing pages to Piwigo for Carrie's review.

### Upload Target

- Gallery: `https://media.delo.sh`
- Album: "Dumply's Daily Dump" (ID: 1) or create sub-album per bundle
- API: Piwigo `pwg.images.addSimple` via `ws.php`

### Upload Requirements

- Use `User-Agent: Dumply/1.0` and `Referer: https://media.delo.sh/`
- Authenticate via `pwg.session.login` (creds from env: `PIWIGO_USER`, `PIWIGO_PASSWORD`)
- Upload helper: `~/workspace-dumpling/bin/piwigo-upload`
- Or direct API calls per references/piwigo-api.md

### Post-Upload

- Set album description with bundle name, page count, theme
- Notify Cack via `sessions_send` that bundle is ready for Carrie review
- **Pipeline pauses here** — contingent on human-in-the-loop approval from Carrie

## Directory Structure

Each bundle lives under `~/workspace-dumpling/assets/{bundle-name}/`:

```
{bundle-name}/
├── research/
│   ├── candidates.json
│   ├── thumbnails/
│   └── research-report.md
├── vectorized/
│   ├── {page}.svg
│   └── {page}.meta.json
├── lineart/
│   └── {page}.png
├── cleaned/
│   ├── {page}.png
│   └── {page}.meta.json
├── qa/
│   ├── qa-report.json
│   ├── qa-summary.md
│   └── rejected/
└── bundle-manifest.json
```

### bundle-manifest.json

```json
{
  "name": "K-pop Demon Hunters",
  "theme": "K-pop fantasy coloring",
  "page_count": 10,
  "target_format": "8.5x11 PDF bundle",
  "created": "2026-02-21T15:00:00-05:00",
  "status": "pending_review",
  "phases_completed": ["research", "vectorize", "lineart", "cleanup", "qa", "upload"],
  "gallery_url": "https://media.delo.sh/index.php?/category/1",
  "plane_ticket": "DIGI-1"
}
```

## Plane Integration

Every bundle MUST have a Plane ticket in the DIGI project (workspace: lasertoast).
Create the ticket before starting Phase 1. Update status as phases complete.

## Agent Delegation Guide

| Phase | Recommended Agent/Model | Why |
|-------|------------------------|-----|
| Research | Sub-agent with Gemini 3 Pro or GLM-4-6v | Needs strong vision for image scoring |
| Vectorize | Dumply (self) | API calls to fal.ai, straightforward |
| Line Art | Dumply (self) | fal.ai API + optional local Pillow |
| Cleanup | Dumply (self) | Local Python image processing |
| QA | Spawn independent sub-agent | Fresh eyes, no confirmation bias |
| Upload | Dumply (self) | Piwigo API via helper script |
