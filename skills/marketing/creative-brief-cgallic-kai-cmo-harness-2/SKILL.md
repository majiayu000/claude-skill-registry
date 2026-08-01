---
name: creative-brief
description: Generate creative direction for ad campaigns — visual concepts, copy variants, video scripts, image specifications, and A/B test matrices. Platform-aware with format specs.
---

# /creative-brief — The Creative Director

Generate comprehensive creative direction for ad campaigns. Produces visual concepts, multiple copy variants, video scripts, image specifications, and structured A/B test plans. Platform-aware with exact format specs.

## Arguments

Required:
- **platform**: meta | google | tiktok | linkedin | multi (generates for all)
- **site**: Site key
- **goal**: Campaign goal in quotes

Optional:
- **--format**: image | video | carousel | all (default: all)
- **--variants**: Number of creative variants (default: 3)

Example: `/creative-brief meta kaicalls "Drive free trial signups for AI receptionist"`
Example: `/creative-brief multi kaicalls "Launch awareness campaign" --variants 5`

## The Skill

### Step 1: Load Context

Read:
- `knowledge/playbooks/ad-creative-best-practices.md` — creative rules and format specs
- `knowledge/channels/meta-advertising.md` (if Meta)
- `knowledge/channels/paid-acquisition.md` (if Google/LinkedIn)
- `knowledge/channels/tiktok-algorithm.md` (if TikTok)
- `knowledge/frameworks/content-copywriting/headline-formulas.md` — headline patterns
- `knowledge/frameworks/content-copywriting/perception-engineering.md` — persuasion layers
- Persona files from `knowledge/personas/` (if site context available)
- `~/.kai-marketing/marketing-defaults.md` (if exists — learned patterns)

### Step 2: Define Creative Strategy

Based on the goal, define the campaign's creative pillars:

```
CREATIVE BRIEF — {platform} for {site}
═══════════════════════════════════════

Goal:           {goal}
Target persona: {persona}
Core message:   {one-sentence value proposition}
Emotional hook:  {the feeling we want to trigger}
Proof type:     {social proof / data / demonstration / testimonial}

MESSAGING PILLARS:
  1. {Pillar 1 — e.g., "Speed" — 0.4s answer time}
  2. {Pillar 2 — e.g., "Never miss a call" — 24/7 coverage}
  3. {Pillar 3 — e.g., "ROI" — pays for itself in 3 days}
```

### Step 3: Generate Copy Variants

For each variant, produce platform-specific copy:

**Meta Ad Copy (per variant):**
```
VARIANT {N}: "{Hook angle}"
────────────────────────────

Primary text (125 chars):
  {text}

Headline (40 chars):
  {headline}

Description (30 chars):
  {description}

CTA: {button text}

Character count check:
  Primary:    {N}/125 ✓
  Headline:   {N}/40  ✓
  Description: {N}/30 ✓
```

**Google Search Ad (per variant):**
```
VARIANT {N}: "{Angle}"
────────────────────

Headlines (30 chars each):
  H1: {headline 1}              {N}/30
  H2: {headline 2}              {N}/30
  H3: {headline 3}              {N}/30

Descriptions (90 chars each):
  D1: {description 1}           {N}/90
  D2: {description 2}           {N}/90

Display path: {domain.com/path1/path2}
```

**TikTok Ad Script (per variant):**
```
VARIANT {N}: "{Hook}"
────────────────────

[0-2s]  HOOK: {visual + text overlay}
[2-5s]  PROBLEM: {establish pain point}
[5-10s] SOLUTION: {show product solving it}
[10-12s] PROOF: {quick social proof or result}
[12-15s] CTA: {end card with action}

Text overlay: {text that appears on screen}
Sound: {music/voiceover direction}
AI disclosure: Required ✓
```

### Step 4: Visual Direction

For each variant, provide image/video direction:

```
VISUAL DIRECTION
═══════════════

IMAGE CONCEPTS:
  Concept A: UGC-style — phone screenshot of missed call notification
             vs. screenshot of AI answering
  Concept B: Split-screen — "Before" (chaotic desk, phone ringing)
             vs. "After" (calm office, AI handling calls)
  Concept C: Data visualization — "0.4 seconds" in large bold type
             with subtle product UI in background

VIDEO CONCEPTS:
  Concept A: POV testimonial — law firm partner talking to camera
             about how many calls they were missing
  Concept B: Screen recording — showing the AI answering a real call
             with captions and music
  Concept C: Problem/solution montage — missed call → angry client →
             client leaving → switch to AI → happy ending

IMAGE SPECS:
  ┌────────────┬──────────────┬────────────┐
  │ Platform   │ Dimensions   │ Format     │
  ├────────────┼──────────────┼────────────┤
  │ Meta Feed  │ 1080x1080    │ JPG/PNG    │
  │ Meta Story │ 1080x1920    │ JPG/PNG    │
  │ Google     │ 1200x628     │ JPG/PNG    │
  │ TikTok     │ 1080x1920    │ JPG/PNG    │
  │ LinkedIn   │ 1200x627     │ JPG/PNG    │
  └────────────┴──────────────┴────────────┘
```

### Step 5: A/B Test Matrix

Structure the variants into a test plan:

```
A/B TEST PLAN
═════════════

PHASE 1 — Hook Test (Week 1):
  Variable: Hook angle
  Constant: Same creative, same audience
  Variants:
    A) Pain hook: "Tired of missing calls?"
    B) Data hook: "0.4 seconds. That's how fast AI answers."
    C) Social hook: "500+ law firms switched to AI."
  Budget: $30/day per variant
  Kill criteria: CTR < 0.5% after 1000 impressions
  Success: Advance top 1-2 hooks

PHASE 2 — Creative Test (Week 2):
  Variable: Creative format
  Constant: Winning hook from Phase 1, same audience
  Variants:
    A) UGC testimonial video
    B) Product demo screen recording
    C) Static image with bold typography
  Budget: $40/day per variant
  Kill criteria: CPA > 2x target after $100 spend

PHASE 3 — Audience Test (Week 3):
  Variable: Audience segment
  Constant: Winning hook + creative from Phase 1-2
  Variants:
    A) Broad (lawyers, interest-based)
    B) Lookalike 1% (from trial signups)
    C) Lookalike 3% (from trial signups)
```

### Step 6: Save and Offer Next Steps

Save the creative brief to `~/.kai-marketing/briefs/{date}-creative-{slug}.json`

Offer:
- "Run `/ad-copy {platform} {site} \"{offer}\"` to generate final ad copy with TOS compliance"
- "Run `/ad-research {competitor} {platform}` to see what competitors are running"

## Error Handling

- **No persona context**: Generate with broad audience assumptions, suggest defining personas
- **Unknown platform**: List valid platforms with format specs

## Chain State

**Standalone:** Can run independently
**Feeds into:** `/ad-copy` (with creative direction), A/B test plan execution
**Optional reads:** `~/.kai-marketing/marketing-defaults.md`, competitor research from `/ad-research`
