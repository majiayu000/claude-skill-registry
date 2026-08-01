---
name: ad-render
description: Render video ads using Remotion. Scaffolds a project from brand tokens + creative brief, generates scene compositions for 4 archetypes, renders to MP4 in multiple formats.
---

# /ad-render — The Video Producer

Turn a creative brief into rendered video ads. Uses Remotion to generate MP4 files in all major ad formats (vertical, square, landscape).

Chains naturally from `/creative-brief` → `/ad-copy` → `/ad-render`.

## Prerequisites

- **Node.js** (v18+) — required for Remotion
- **Brand config** — run `kai-config set brand.name "YourBrand"` and set colors

## Arguments

Required:
- **archetype**: problem-agitation | social-proof | product-demo | lifestyle

Optional:
- **--format**: vertical | square | landscape | all (default: all)
- **--copy**: JSON string or file path with ad copy fields (hook, problem, solution, cta)

Example: `/ad-render problem-agitation`
Example: `/ad-render social-proof --format vertical`

## The Skill

### Step 1: Load Brand Tokens

Read brand configuration:
```bash
kai-config get brand.name
kai-config get brand.colors.primary
```

If brand is not configured, prompt user: "Set your brand first: `kai-config set brand.name 'YourBrand'` and `kai-config set brand.colors.primary '#yourcolor'`"

### Step 2: Check for Ad Copy

Look for the most recent creative brief or ad copy in `~/.kai-marketing/briefs/`.
If ad copy fields are provided via `--copy`, use those.
If neither exists, prompt user to run `/ad-copy` or `/creative-brief` first.

Extract from the copy:
- **hook**: The attention-grabbing first line
- **problem**: The pain point being addressed
- **benefit**: What the product solves
- **stat**: A proof point (number, percentage, result)
- **cta**: The call to action text

### Step 3: Scaffold Remotion Project

Run:
```bash
kai-render scaffold --archetype {archetype} --format {format}
```

This creates a Remotion project at `~/.kai-marketing/renders/{date}/` with:
- `src/config/brand.ts` — Brand colors, fonts, assets from config
- `src/config/scenes.json` — Scene-by-scene composition config
- `src/templates/` — Remotion composition templates
- `package.json` — Dependencies and render scripts

Display the scene breakdown:
```
VIDEO AD — {archetype} ({format})
═══════════════════════════════════

Brand: {name} | Colors: {primary} / {secondary}

Scene 1: HOOK (3.0s)
  Text: "{hook text}"
  Animation: scale
  Background: brand color

Scene 2: PROBLEM (4.0s)
  Text: "{problem text}"
  Animation: slide-up
  Background: gradient

Scene 3: AGITATE (3.0s)
  Text: "Sound familiar?"
  Animation: fade-in
  Background: gradient

Scene 4: CTA (3.0s)
  Text: "{cta}"
  Animation: spring
  Background: brand color

Total: 13.0s | Format: 1080x1920 (9:16)
```

### Step 4: Install & Render

If Node.js is available:
```bash
cd ~/.kai-marketing/renders/{date}
npm install
npx remotion render src/Root.tsx {CompositionName} out/{format}.mp4
```

If Node.js is NOT available:
"Node.js required for video rendering. Install: https://nodejs.org. The Remotion project has been scaffolded — you can render it on any machine with Node."

### Step 5: Show Output

```
VIDEO AD RENDERED
═════════════════

Archetype: {archetype}
Duration:  {total_seconds}s
Files:
  vertical:  ~/.kai-marketing/renders/{date}/out/vertical.mp4  (1080x1920)
  square:    ~/.kai-marketing/renders/{date}/out/square.mp4    (1080x1080)
  landscape: ~/.kai-marketing/renders/{date}/out/landscape.mp4 (1920x1080)

Platform destinations:
  Meta Reels/Stories: vertical.mp4
  Meta Feed:          square.mp4
  Google/YouTube:     landscape.mp4
  TikTok:             vertical.mp4
  LinkedIn:           landscape.mp4 or square.mp4
```

### Step 6: Offer Variants

"Want to render another archetype? Available: problem-agitation, social-proof, product-demo, lifestyle"

## Archetypes

| Archetype | Best For | Duration | Scenes |
|-----------|----------|----------|--------|
| **problem-agitation** | Cold audiences, awareness | 10-15s | Hook → Problem → Agitate → CTA |
| **social-proof** | Warm audiences, consideration | 8-12s | Stat → Explain → CTA |
| **product-demo** | Retargeting, feature awareness | 15-20s | Intro → Demo → Benefit → CTA |
| **lifestyle** | Brand building, emotional | 8-12s | Aspiration → Bridge → CTA |

## Error Handling

- **Node.js not installed**: Scaffold only, provide instructions to render elsewhere
- **Brand not configured**: Direct to `kai-config set brand.*`
- **No ad copy**: Direct to `/ad-copy` or `/creative-brief`
- **Remotion render fails**: Show error, suggest checking Node version and dependencies

## Chain State

**Reads from:** `~/.kai-marketing/briefs/`, `~/.kai-marketing/config.yaml` (brand)
**Writes to:** `~/.kai-marketing/renders/{date}/`
**Chains from:** `/creative-brief` → `/ad-copy` → `/ad-render`
