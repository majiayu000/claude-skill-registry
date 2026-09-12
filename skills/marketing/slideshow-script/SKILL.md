---
name: slideshow-script
description: "Generate 5 different narrative scripts for visual slideshows from a single positioning angle. Each script uses a different storytelling framework (AIDA, PAS, BAB, Star-Story-Solution, Stat-Flip) producing genuinely different stories, not layout variations. Make sure to use this skill whenever the user wants slideshow scripts, TikTok content scripts, carousel copy, narrative frameworks for visual content, or says anything about writing scripts for slides or social media storytelling. Even 'write me some TikTok content' or 'I need carousel copy' should trigger this. Outputs structured YAML content specs that chain directly to /paper-marketing for visual design."
category: creative
tier: nice-to-have
reads:
  - brand/positioning.md
  - brand/audience.md
  - brand/voice-profile.md
writes:
  - marketing/content-specs/*.yaml
depends-on:
  - brand-voice
  - positioning-angles
triggers:
  - slideshow script
  - generate scripts
  - narrative scripts
  - content scripts
  - TikTok scripts
  - storytelling frameworks
  - carousel scripts
allowed-tools:
  - Bash(mktg status *)
---

# /slideshow-script — Narrative Script Generation

Generate 5 different narrative scripts from a single positioning angle. Each script uses a different storytelling framework, producing 5 publishable pieces of content instead of 5 variations of 1 script.

For scripting frameworks reference, see [references/frameworks.md](references/frameworks.md).
For content spec YAML schema, see [references/content-spec-schema.md](references/content-spec-schema.md).

## Why 5 Scripts, Not 5 Layouts

```
Old model:  1 script × 5 visual layouts = 1 usable output (pick 1, waste 4)
New model:  5 scripts × 5 visual layouts = 5 usable outputs (post all 5)
```

Each script has a DIFFERENT narrative, DIFFERENT hook, DIFFERENT proof points. When paired with /paper-marketing, each agent gets a unique script AND a unique design direction.

## Workflow

### Phase 1: Load Brand Context

Read in parallel (if they exist):
- `brand/positioning.md` — available angles, headlines, proof points
- `brand/audience.md` — pain points, desires, language patterns
- `brand/voice-profile.md` — tone, vocabulary, do's/don'ts, signature phrases

If any files are missing, the skill still works — see Progressive Enhancement below for how to handle zero-context and partial-context scenarios.

### Phase 2: Select Positioning Angle

If the user hasn't specified an angle, present the available angles from `brand/positioning.md`:

```
"Which positioning angle should I write 5 scripts for?"

[List angles from positioning.md with their headlines]

Options:
1-N. Select a specific angle
N+1. "Use the primary angle"
```

### Phase 3: Generate 5 Scripts

For the selected positioning angle, generate 5 narratively distinct scripts — one per framework:

| # | Framework | Structure | Hook Style |
|---|-----------|-----------|------------|
| 1 | **AIDA** | Attention → Interest → Desire → Action | Bold claim or question |
| 2 | **PAS** | Problem → Agitate → Solution | Pain point the audience feels |
| 3 | **BAB** | Before → After → Bridge | "Life before" vs "life after" |
| 4 | **Star-Story-Solution** | Hook character → conflict → resolution | Personal/relatable story |
| 5 | **Stat-Flip** | Surprising data → reframe → CTA | Shocking statistic |

**Each script includes:**
- **Hook** (slide 1) — the first thing seen, must grab in 1-3 seconds
- **5-7 slides** — each with `type` annotation (stat, anchor_word, emotional_pivot, cascade, cta, logo_intro)
- **CTA** (final slide) — clear action with URL/handle
- **Animation hints** — spring preset suggestion per slide (bouncy, smooth, heavy, snappy)

**Script generation rules:**
- All 5 must use the SAME positioning angle but tell DIFFERENT stories
- No two scripts should share the same hook
- Each script should use different proof points from the positioning doc
- Voice rules from voice-profile.md apply to ALL scripts
- Slide count can vary (5-9) based on what the narrative needs

### Phase 4: Match Scripts to Visual Directions

Each script gets a recommended visual direction for /paper-marketing:

| Framework | Best Visual Direction | Why |
|-----------|---------------------|-----|
| AIDA | Typographic | Text IS the design, progressive revelation |
| PAS | Contrast Play / Split | Tension between problem and solution |
| BAB | Atmospheric | Emotional transformation needs breathing room |
| Star-Story-Solution | Editorial | Story flow needs magazine-like pacing |
| Stat-Flip | Data-Led | Numbers are the visual anchors |

These are recommendations — the user can override.

### Phase 5: Present for Approval

Use **AskUserQuestion** to show all 5 scripts with their visual direction:

```
"Here are 5 narrative scripts for '{angle_name}', each using a different storytelling framework:"

1. **AIDA** (→ Typographic): "{hook}" — Attention grab → feature interest → desire trigger → CTA
2. **PAS** (→ Contrast Play): "{hook}" — Pain → twist → relief
3. **BAB** (→ Atmospheric): "{hook}" — Before/after transformation
4. **Star-Story-Solution** (→ Editorial): "{hook}" — Story arc → resolution
5. **Stat-Flip** (→ Data-Led): "{hook}" — Shocking stat → reframe

Options:
1. "All 5 look great" — write all 5 content specs
2. "Regenerate #{n}" — rewrite a specific script
3. "Change the angle" — try a different positioning angle
4. "Edit a script" — modify specific slides
5. "Only use 3 of these" — select a subset
```

### Phase 6: Write Content Spec YAMLs

For each approved script, write a structured YAML file:

**Path:** `marketing/content-specs/{project}-{framework}.yaml`

Example: `marketing/content-specs/lumi-aida.yaml`

See [references/content-spec-schema.md](references/content-spec-schema.md) for the full schema.

```yaml
spec_version: 1
project: lumi
content_type: tiktok-slideshow
scripting_framework: AIDA
platform:
  name: tiktok
  width: 1080
  height: 1920
  aspect: "9:16"
positioning_angle: "The 30-Second Active Gate"
visual_direction: typographic
slides:
  - index: 1
    type: stat
    headline: "30"
    subhead: "seconds."
    body: null
    animation_hint: spring_bouncy
    role: hook
  - index: 2
    type: anchor_word
    headline: "Breathe in"
    subhead: "That's how long five deep breaths take."
    body: null
    animation_hint: spring_heavy
    role: interest
  # ... more slides
  - index: 7
    type: cta
    headline: "lumi.com"
    subhead: "Presence before everything."
    body: null
    animation_hint: spring_smooth
    role: action
cta:
  url: "lumi.com"
  tagline: "Presence before everything."
  handle: "@lumi"
voice_constraints:
  tone: "calm, certain, mindful"
  avoid: ["hype", "guilt", "exclamation marks"]
  signature_phrases: ["Take 5 breaths. Unlock your phone.", "Presence before everything."]
```

### Phase 7: Summary

Report what was written:
```
5 content specs written to marketing/content-specs/:
  1. lumi-aida.yaml (7 slides, Typographic)
  2. lumi-pas.yaml (6 slides, Contrast Play)
  3. lumi-bab.yaml (7 slides, Atmospheric)
  4. lumi-story.yaml (8 slides, Editorial)
  5. lumi-statflip.yaml (5 slides, Data-Led)

Next: Run /paper-marketing to design each script, or /tiktok-slideshow for the full pipeline.
```

## Standalone Usage

This skill works independently from any orchestrator:
- `/slideshow-script` alone → generates scripts for manual design work
- `/slideshow-script` → `/paper-marketing` → manual export (no video)
- `/slideshow-script` → `/content-atomizer` → repurpose scripts as text posts
- `/slideshow-script` → `/email-sequences` → use narratives in email campaigns

## Progressive Enhancement

This skill works at three levels of context:

1. **Zero context** — No brand files. Ask the user for: product name, one-sentence description, target audience, and the key benefit. Generate scripts from that. They'll be generic but functional.
2. **Partial context** — Only `positioning.md` exists. Generate scripts from the positioning angles. Copy will be accurate but may lack voice personality.
3. **Full context** — All three brand files exist (`positioning.md`, `audience.md`, `voice-profile.md`). Scripts use the right angles, speak to the right pain points, and sound like the brand.

## Anti-Patterns

- **Same hook across scripts** — The whole point of 5 scripts is 5 chances to grab attention differently. If two scripts start with a question hook, you've wasted one. A viewer who scrolled past hook A might stop for hook B — but only if B looks and sounds different.
- **Recycled proof points** — Reusing the same stat in multiple scripts means a viewer who sees script 2 after script 1 hears the same argument. Each script should use different proof points from positioning.md so every post adds new information.
- **Generic voice** — "Transform your life" could be any brand on any platform. Viewers tune it out because they've seen it a thousand times. Using the exact vocabulary and signature phrases from voice-profile.md makes the content feel authored and recognizable.
- **Platform-specific copy in scripts** — Scripts are the narrative layer, not the design layer. Writing "swipe right" or "link in bio" locks the script to one platform. Keep scripts platform-agnostic so the same narrative works for TikTok, Instagram, YouTube Shorts, or any other format.
- **Too many slides** — Every slide the viewer must sit through is friction. If a slide doesn't advance the narrative toward the CTA, it's a drop-off point. 5-7 slides usually hits the sweet spot for social content.
- **Ignoring the framework** — Each framework works because of its specific psychological structure. AIDA builds desire before asking for action. PAS makes pain visceral before offering relief. Blending frameworks dilutes the psychological effect that makes each one work.

## Edge Cases

- **positioning.md missing** — Ask the user: "What's the main angle or benefit you want to highlight?" Use their answer as the positioning angle. Offer to run /positioning-angles to build proper angles.
- **Only 1-2 proof points available** — Generate fewer scripts (3 instead of 5) and tell the user which frameworks were dropped and why. Quality over quantity.
- **User wants fewer than 5 scripts** — Respect the request. Ask which frameworks they want, or recommend the best 2-3 for their content type.
- **User wants a framework not in the list** — Accept custom frameworks. Ask for the structure (what are the phases?) and generate a script following that structure.
- **Brand voice conflicts with framework** — If the brand voice is "calm, no hype" but PAS requires agitation, dial the agitation to match the voice. Agitate with quiet observations, not exclamation marks.

## Principles

- **5 narratives, not 5 variations** — every output should be publishable
- **Frameworks enforce diversity** — AIDA and PAS produce fundamentally different stories
- **Content spec is the contract** — downstream skills read YAML, not prose
- **Archetype annotations matter** — `type: stat` tells Paper agents AND Remotion what to emphasize
- **Voice rules are non-negotiable** — all 5 scripts must sound like the brand
