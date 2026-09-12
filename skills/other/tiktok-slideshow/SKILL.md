---
name: tiktok-slideshow
description: >
  Orchestrator skill that chains /slideshow-script → /paper-marketing →
  /video-content for end-to-end TikTok slideshow production. Each phase is
  an independent Lego block — this orchestrator is just one recipe that
  combines them. Produces 5 publishable TikTok videos from a single
  positioning angle. Triggers on "TikTok slideshow", "TikTok video",
  "make TikTok", "slideshow video", "TikTok content".
allowed-tools:
  - Bash(mktg status *)
  - Bash(ffmpeg *)
  - Bash(bun *)
  - Bash(bunx remotion *)
---

# /tiktok-slideshow — End-to-End TikTok Content Pipeline

Orchestrator that chains 3 atomic skills into a complete TikTok production pipeline:

```
/slideshow-script  →  /paper-marketing  →  /video-content
   (5 scripts)         (5 designs)          (5 videos)
```

Each skill is a Lego block that works independently. This orchestrator is one recipe.

## Architecture

```
Phase 1: SCRIPT  — /slideshow-script generates 5 narrative scripts
Phase 2: DESIGN  — /paper-marketing creates 5 visual designs (1 per script)
Phase 3: VIDEO   — /video-content assembles videos from designs
```

**Platform spec:** TikTok 1080×1920, 9:16, 30fps, H.264

## Prerequisites

Before starting, verify all 3 sub-skills are installed:
- `~/.claude/skills/slideshow-script/SKILL.md`
- `~/.claude/skills/paper-marketing/SKILL.md`
- `~/.claude/skills/video-content/SKILL.md`

If any sub-skill is missing, tell the user and recommend `mktg update` to install it. Do not proceed without all 3.

## Workflow

### Phase 1: SCRIPT

Load the `/slideshow-script` skill at `~/.claude/skills/slideshow-script/SKILL.md` and follow its workflow:

1. Read brand files (positioning, audience, voice)
2. User selects positioning angle
3. Generate up to 5 scripts using 5 storytelling frameworks (AIDA, PAS, BAB, Star-Story-Solution, Stat-Flip). User may select fewer at the gate.
4. Each script uses the brand voice from `brand/voice-profile.md` for tone, vocabulary, and signature phrases
5. Present all 5 scripts for approval
6. Write 5 content spec YAMLs to `marketing/content-specs/`

**Gate:** User must approve scripts before Phase 2.

### Phase 2: DESIGN

Load the `/paper-marketing` skill at `~/.claude/skills/paper-marketing/SKILL.md` and follow its workflow, with these orchestrator-specific instructions:

1. Paper-marketing Phase 1 (Load Brand) proceeds as normal
2. **Skip Phase 2a-2d** — the content specs already exist from Phase 1
3. Instead, read the 5 content spec YAMLs from `marketing/content-specs/`
4. Each content spec has a `visual_direction` field — use that to set each agent's design brief
5. Each agent gets its content spec's unique script (different slides, different narrative)
6. Each agent loads the `/frontend-design` skill for design quality
7. Spawn agents — number depends on how many scripts the user approved (could be 3-5)

**Script-to-design mapping from content specs:**

| Content Spec | Visual Direction | Framework |
|--------------|-----------------|-----------|
| `{project}-aida.yaml` | typographic | AIDA |
| `{project}-pas.yaml` | contrast-play | PAS |
| `{project}-bab.yaml` | atmospheric | BAB |
| `{project}-story.yaml` | editorial | Star-Story-Solution |
| `{project}-statflip.yaml` | data-led | Stat-Flip |

8. User reviews all designs, selects favorite(s)
9. Extract `get_jsx()` from selected artboard(s)
10. Write handoff YAML(s) to `marketing/handoffs/`

**Gate:** User must select variation(s) and export PNG from Paper UI.

### Phase 3: VIDEO

Load the `/video-content` skill at `~/.claude/skills/video-content/SKILL.md` and follow its workflow:

1. Detect handoff YAML from Phase 2
2. ffmpeg slice the exported PNG into individual slides
3. User selects tier (v1 Quick / v1.5 Enhanced / v2 Full)
4. Assemble video at chosen tier
5. ffmpeg post-process (thumbnail, GIF preview, platform encode)

**For multiple selections:** If user approved multiple designs, run video assembly for each. Can be parallelized — each video is independent.

**Gate:** User approves final video(s).

## Human-in-the-Loop Gates

```
[Phase 1] → User approves 5 scripts
[Phase 2] → User selects design variation(s), exports PNG(s) from Paper UI
[Phase 3] → User selects video tier, approves final output
```

Each gate is an AskUserQuestion. The user can go back to any phase.

## Output

```
marketing/content-specs/
  {project}-aida.yaml
  {project}-pas.yaml
  {project}-bab.yaml
  {project}-story.yaml
  {project}-statflip.yaml

marketing/handoffs/
  {project}-{variation}-handoff.yaml

marketing/video/
  {project}-{variation}/
    slides/
    output_{tier}.mp4
    thumbnail.png
    preview.gif
```

## Reusable Blocks

Each skill in this chain works independently:

| Block | Standalone Use |
|-------|---------------|
| `/slideshow-script` | Generate scripts for any format (Instagram carousel, YouTube, email) |
| `/paper-marketing` | Design any visual content (not just slideshows) |
| `/video-content` | Assemble video from any PNGs (not just Paper exports) |

## Other Orchestrator Recipes (Future)

Same blocks, different combinations:

```
/instagram-carousel  = /slideshow-script → /paper-marketing (4:5 ratio, no video)
/youtube-short       = /slideshow-script → /paper-marketing → /video-content (16:9)
/reels-batch         = /slideshow-script (10 scripts) → /paper-marketing → /video-content × 10
/ad-creative         = /slideshow-script (1 script) → /paper-marketing (1 slide) → /video-content
```

## Error Recovery

| Failure | Action |
|---------|--------|
| Sub-skill not installed | Stop, recommend `mktg update`, do not proceed |
| Phase 1 scripts rejected | Revise scripts with user feedback, do not advance to Phase 2 |
| Paper MCP unavailable | Fall back to manual slide creation; user provides PNGs |
| Phase 2 design export fails | User re-exports from Paper UI; agent retries video assembly |
| Phase 3 video assembly fails | Check ffmpeg/Remotion installation, retry with v1 tier first |

## Anti-Patterns

| Anti-Pattern | Instead |
|-------------|---------|
| Skipping human gates between phases | Always wait for user approval at each gate |
| Running all 3 phases without stopping | Each phase has an explicit gate — never auto-advance |
| Generating all 5 when user only wants 2 | Respect user selection at Phase 1 gate |
| Re-using the same visual direction for all designs | Each content spec maps to a unique visual direction |
| Loading sub-skills via Bash instead of reading SKILL.md | Load each skill's SKILL.md and follow its instructions |

## Principles

- **Skills never call skills** — this SKILL.md teaches the agent the sequence; the agent loads each skill
- **Filesystem is the bus** — content specs and handoffs are YAML files, not API calls
- **Human gates at every phase** — no runaway agent chains
- **Progressive quality** — start with v1 to verify, upgrade to v2 for production
- **All outputs are publishable** — different scripts, different designs, not N versions of 1
