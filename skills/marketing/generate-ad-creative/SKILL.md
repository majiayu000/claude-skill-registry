---
name: generate-ad-creative
description: End-to-end ad creative generation for Clarido — from performance analysis to rendered video variants. Use when creating new ad creatives, video ads, or marketing content.
disable-model-invocation: true
allowed-tools: Bash(pipenv *), Bash(cd videos *), Bash(npx remotion *), Bash(npm *), Bash(mkdir *), Bash(ls *)
---

# Generate New Ad Creative

End-to-end workflow for generating new Clarido ad creatives. Invoked by the user with `/generate-ad-creative`.

This skill covers the full pipeline: analyzing existing ad performance, generating two creative concepts (explore vs exploit), producing multiple asset variants, composing in Remotion, rendering final outputs, and documenting everything for auditability.

## Workflow Overview

### Phase 1: Performance Analysis & Concept Generation
### Phase 2: User Selection
### Phase 3: Asset Generation (multiple variants)
### Phase 4: Remotion Composition & Rendering
### Phase 5: Output Packaging & Documentation

---

## Phase 1: Performance Analysis & Concept Generation

### Step 1.1 — Pull Current Ad Performance

Use the Meta Marketing API to pull performance data for all active and recent campaigns.

```python
# Key metrics to pull per ad:
# - CTR (click-through rate)
# - CPL (cost per lead) or CPA (cost per action)
# - ROAS (if applicable)
# - Video metrics: ThruPlay rate, video_p25/p50/p75/p100 (retention curve)
# - Spend, impressions, reach, frequency
# - Creative type (video, image, carousel)
# - Ad copy / headline
# - Audience targeting summary
# - Date range active
```

Use the Meta Marketing API credentials from `.env`:
- `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID` (`act_217614761779242`)
- API version: v21.0
- Currency: CAD

Pull data at the **ad level** (not campaign or ad set) to evaluate individual creatives.

### Step 1.2 — Analyze & Identify Patterns

Analyze the data to identify:
- **Top performers**: Which creatives have the best CTR, lowest CPL, highest retention?
- **Creative patterns**: What emotional hooks, visual styles, lengths, and formats work?
- **Audience patterns**: Which targeting is working best?
- **Drop-off patterns**: Where do viewers stop watching? (use video percentile metrics)
- **Gaps**: What emotional angles or formats haven't been tested yet?

### Step 1.3 — Generate Two Creative Concepts

Present **two concepts** to the user:

#### Concept A: Exploration (new territory)
- A creative that tests a **new emotional angle, visual style, or format** not yet represented in the account
- Should be informed by what's working but deliberately different
- Higher risk, higher potential upside
- Include:
  - Creative brief (hook, narrative arc, CTA)
  - Visual style description
  - Recommended duration (justify with retention data)
  - Audience targeting recommendation
  - Test plan: what metric will determine success, what's the minimum spend to validate, what's the kill criteria

#### Concept B: Exploitation (iterate on what works)
- A creative that is a **close variant** of the best-performing existing ad
- Change ONE variable: different hook, different visual treatment, different CTA, different pacing
- Lower risk, reliable baseline
- Include:
  - What existing ad it's based on and what's being changed
  - Creative brief
  - Audience targeting (same as original or slight variation to test)
  - Test plan: A/B framework against the original, success criteria

**Present both concepts clearly with a recommendation**, then ask the user which to proceed with. Allow the user to modify the concept before proceeding.

---

## Phase 2: User Selection

Ask the user to choose Concept A or B (or provide modifications). Once confirmed, proceed to asset generation.

---

## Phase 3: Asset Generation (Multiple Variants)

### Step 3.1 — Generate Video Clips (up to 3 variants)

Use Fal AI to generate video clips. Generate **up to 3 variants** with different prompts or parameters to give the user options.

- Use Kling V3 Pro for best quality: `fal-ai/kling-video/v3/pro/text-to-video`
- Use the queue API (submit → poll → download) since video generation takes 2-5 minutes
- Generate all variants in parallel to minimize wait time
- Default: 5 seconds, 1:1 aspect ratio, no audio
- Save to `videos/public/` with descriptive names: `{concept-name}-clip-v1.mp4`, `-v2.mp4`, `-v3.mp4`

**Cost awareness**: Each 5s Kling V3 Pro clip costs ~$1.12 (no audio). 3 clips = ~$3.36.

### Step 3.2 — Generate Background Music (3-5 variants)

Use ElevenLabs Music API (`POST /v1/music`) to generate background music variants.

- Generate **3-5 variants** with different prompts exploring different moods/instruments
- Each should match the ad's emotional arc (e.g., tense → calm, energetic → resolved)
- Set `force_instrumental: true` and `music_length_ms` to match ad duration
- Save as `{concept-name}-music-v1.mp3`, `-v2.mp3`, etc.

If ElevenLabs music fails (402), fall back to Fal AI Beatoven (`beatoven/music-generation`).

### Step 3.3 — Generate Sound Effects

Use ElevenLabs Sound Generation (`POST /v1/sound-generation`) for any needed SFX:
- Transition sounds, pop-ins, whooshes, etc.
- Keep duration short (0.3-1.0 seconds)
- Save to `videos/public/`

---

## Phase 4: Remotion Composition & Rendering

### Step 4.1 — Name the Composition

**Naming is critical.** Every ad lives in `videos/src/` alongside all others and appears in the Remotion Studio sidebar. Names must be descriptive enough to identify the creative at a glance months later.

**Naming convention**: `{Scenario}{Style}` in PascalCase.

- **Scenario**: The specific situation or emotional hook (not a generic category)
- **Style**: The visual treatment or format

**Good names:**
- `OverwhelmedInBedRealistic` — person in bed, realistic AI video
- `FounderAtDinnerClay` — founder checking phone at dinner, clay animation style
- `MorningJournalWatercolor` — morning journaling scene, watercolor illustration
- `ThreeAmThoughtSpiral` — 3am anxiety thought cascade
- `TodoListAvalanche` — to-do list growing out of control
- `ParkBenchReflection` — calm reflection moment on a park bench

**Bad names (too vague):**
- `OverwhelmAd` — which overwhelm ad? What style?
- `NewAd` — meaningless
- `VideoV2` — no context
- `LeadsCampaign` — describes the objective, not the creative

The name flows through everything:
- Directory: `videos/src/OverwhelmedInBedRealistic/`
- Composition IDs: `OverwhelmedInBedRealistic-Square`, `OverwhelmedInBedRealistic-Vertical`
- Folder in Remotion Studio sidebar: `OverwhelmedInBedRealistic`
- Output directory: `videos/out/2026-02-16_10-30-00-000_OverwhelmedInBedRealistic/`
- Asset file prefixes: `overwhelmed-in-bed-realistic-clip-v1.mp4`

### Step 4.2 — Build the Composition

Create the directory under `videos/src/{AdName}/`.

Follow Remotion best practices (see `videos/.claude/skills/remotion/` rules):
- All animations via `useCurrentFrame()` + `interpolate()` / `spring()` — NO CSS animations
- Use `<Sequence>` with `premountFor` for timing
- Use `<Audio>` and `<Video>` from `@remotion/media`
- Use `staticFile()` for assets in `videos/public/`
- Brand style: black/white with yellow (`#FFD60A`) accent
- Font: system font stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`)

Structure:
```
videos/src/{AdName}/
├── config.ts          # Timing, constants, text content
├── index.tsx          # Main composition (layers video, overlays, audio)
├── [Components].tsx   # Scene-specific components
```

Register in `videos/src/Root.tsx`:
- Square format: `{AdName}-Square` (1080x1080)
- Vertical format: `{AdName}-Vertical` (1080x1920)
- Group in a `<Folder>` using the same `{AdName}`

### Step 4.2 — Render All Combinations

For the user-selected video clip and music track, render both formats:

```bash
cd videos
npx remotion render {AdName}-Square out/{output-dir}/square.mp4
npx remotion render {AdName}-Vertical out/{output-dir}/vertical.mp4
```

If the user wants to compare multiple video/music combos, render the preferred combinations.

---

## Phase 5: Output Packaging & Documentation

### Output Directory Structure

Every generation run produces a timestamped directory:

```
videos/out/{YYYY-MM-DD_HH-MM-SS-mmm}_{ad-name}/
├── square.mp4                    # 1080x1080 render
├── vertical.mp4                  # 1080x1920 render
├── assets/
│   ├── clip-v1.mp4               # Video variant 1
│   ├── clip-v2.mp4               # Video variant 2
│   ├── clip-v3.mp4               # Video variant 3
│   ├── music-v1.mp3              # Music variant 1
│   ├── music-v2.mp3              # Music variant 2
│   ├── music-v3.mp3              # Music variant 3
│   └── sfx/                      # Sound effects used
│       └── pop.mp3
├── BRIEF.md                      # Creative brief & documentation
└── performance-snapshot.json     # Ad performance data at time of generation
```

### BRIEF.md Contents

The brief must document:

```markdown
# {Ad Name} — Creative Brief

**Generated**: {timestamp}
**Concept type**: Exploration / Exploitation
**Based on**: {if exploitation, which existing ad and what was changed}

## Performance Context
- Top performing ad at time of generation: {name}, {CTR}%, {CPL}
- Account-wide averages: {CTR}%, {CPL}
- Key insight that informed this creative: {insight}

## Creative Concept
- **Hook** (0-3s): {description}
- **Narrative** (3-Xs): {description}
- **Resolution/CTA** (X-end): {description}
- **Duration**: {X}s (rationale: {why this length})
- **Format**: Video with text overlays, no voiceover / with voiceover

## Visual Style
{Description of the visual approach}

## Audio
- **Background music**: {description of selected track}
- **SFX**: {what sounds are used and when}

## Ad Copy (for Meta)
- **Primary text**: {suggested ad copy}
- **Headline**: {headline}
- **CTA button**: {Learn More / Sign Up / Download / etc.}

## Audience Targeting
- **Interests**: {list}
- **Demographics**: {age, gender, location}
- **Lookalike**: {if applicable}
- **Exclusions**: {existing customers, etc.}

## Test Plan
- **Objective**: {Leads / App Installs / Link Clicks}
- **Budget**: ${X}/day for {Y} days
- **Success metric**: {CTR > X% / CPL < $Y}
- **Kill criteria**: {If CPL > $Z after ${A} spend, pause}
- **What we're testing**: {the specific hypothesis}

## Asset Variants Generated
- Video clips: {count} variants
- Music tracks: {count} variants
- Selected combination: clip-v{X} + music-v{Y}

## Rendering
- Square (1080x1080): square.mp4
- Vertical (1080x1920): vertical.mp4
- Codec: H.264
- FPS: 30
```

### performance-snapshot.json

Save the raw ad performance data pulled in Phase 1 as JSON for future reference.

---

## Important Guidelines

- **Always run end-to-end**: Don't stop at code — generate assets, render videos, produce the output directory
- **Parallel generation**: Submit all video clip requests and music requests in parallel to minimize total wait time
- **Cost transparency**: Before generating, tell the user the estimated cost (video clips + music)
- **Brand consistency**: Yellow accent (#FFD60A), black/white palette, system fonts
- **Duration**: Default to 13-15 seconds based on retention data. Justify any different length
- **Muted-first design**: Ads should work with sound off (text overlays carry the message). Audio enhances but isn't required
- **User approval gates**: Get user approval at concept selection AND before final render (show asset options first)
