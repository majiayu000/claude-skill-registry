---
name: paper-marketing
description: >
  On-brand visual marketing content using Paper MCP and parallel agent teams.
  Reads the project's brand/ directory to build a design system, then spawns
  designer agents in parallel — each creating a unique artboard with a
  different on-brand layout interpretation. Intelligently adapts agent count
  and approach based on user goals via AskUserQuestion interrogation.
  Produces Instagram carousels, TikTok slideshows, social posts, story slides,
  and visual assets. When used with content spec YAMLs from /slideshow-script,
  each agent gets a unique script AND unique design direction.
  Make sure to use this skill whenever the user wants visual marketing
  content designed in Paper — carousels, slideshows, social posts, story
  slides, or any visual asset. Even if they just say "design something" or
  "make slides" or "create visual content", this is the skill. Also triggers
  on "paper marketing", "instagram design", "TikTok design", "slideshow
  design", "create carousel", or "social graphics".
category: creative
tier: nice-to-have
reads:
  - brand/voice-profile.md
  - brand/creative-kit.md
  - brand/positioning.md
  - brand/assets.md
  - marketing/content-specs/*.yaml
writes:
  - brand/creative-kit.md
  - marketing/content-specs/*.yaml
  - marketing/handoffs/*-handoff.yaml
  - brand/assets.md
depends-on:
  - brand-voice
triggers:
  - paper marketing
  - design carousel
  - create slides
  - visual content
  - instagram design
  - social graphics
  - slide design
  - TikTok design
  - slideshow design
allowed-tools:
  - Bash(mktg status *)
---

# /paper-marketing — On-Brand Visual Content in Paper MCP

Spawn parallel designer agents in Paper, each creating a unique on-brand interpretation of marketing content. Same brand system, different creative executions. Agent count and approach intelligently adapt to the user's actual goal.

## Quick Reference

| Phase | What Happens | Key Tool |
|-------|-------------|----------|
| 1. Load Brand | Read brand/ files, discover Paper file, confirm with user | `mcp__paper__get_basic_info()` |
| 2. Goal Discovery | Interrogate user: content type, variation count, priority | `AskUserQuestion` |
| 3. Create Tasks | Build rich task descriptions with full brand system + content | `TeamCreate` + `TaskCreate` |
| 4. Spawn Agents | Launch N designer agents in parallel | `Agent` (background, Sonnet) |
| 5. Review | Screenshot artboards, compare, user selects winner | `mcp__paper__get_screenshot()` |
| 6. Export | Extract JSX, write handoff YAML, instruct user to export PNG | `mcp__paper__get_jsx()` |
| 7. Log | Update brand/assets.md, append workflow log | File writes |

For Paper MCP HTML rules, see [references/paper-mcp-rules.md](references/paper-mcp-rules.md).
For brand system extraction template, see [references/brand-system-template.md](references/brand-system-template.md).
For platform-specific conventions, see [references/platform-conventions.md](references/platform-conventions.md).
For agent quality rubric, see [references/agent-quality-rubric.md](references/agent-quality-rubric.md).

## Workflow

### Phase 1: Load Brand System + Discover Paper File

**Step 1a: Load brand context.** Run `mktg status --json` to confirm brand files exist. Then read in parallel:
- `brand/voice-profile.md` — tone, vocabulary, do's/don'ts, signature phrases
- `brand/creative-kit.md` — colors (hex + roles), fonts (families + weights + sizes), spacing rhythm
- `brand/positioning.md` — angles, headlines, proof points
- `brand/assets.md` — what already exists (avoid duplication)

**Step 1b: Extract the design system.** From brand files, build:
- **Palette**: every color token with hex and role (bg, accent, text, muted, divider)
- **Typography**: font families, weights, sizes for each role (display, section, body, label, stat)
- **Layout tokens**: slide dimensions, padding, content area, footer structure
- **Voice rules**: signature phrases, copy rules, words to use/avoid
- **Positioning angles**: available angles and their headline directions

If `creative-kit.md` is missing, use AskUserQuestion to gather basics (bg color light/dark, accent color, font preference), then write the result to `brand/creative-kit.md` so it persists.

**Step 1c: Discover the Paper workspace.** Call `mcp__paper__get_basic_info()` and record:
- **File name** — this is the workspace all agents will use
- **Existing artboards** — names and IDs, so agents know what's already there
- **Loaded fonts** — so agents can use them without guessing

**Step 1d: Confirm with AskUserQuestion:**
```
"I see Paper file '{fileName}' is open with artboards: {list}. I'll create new artboards here for the marketing designs. Right file?"

Options:
1. "Yes, use this file" — proceed
2. "Different file" — user specifies which file to open
```

Do NOT proceed until the user confirms.

### Phase 2: Intelligent Goal Discovery

This is the most important phase. Use **AskUserQuestion** to understand what the user actually needs before deciding how many agents to spawn.

#### 2a. Check for Content Specs

First, check if content spec YAMLs already exist (written by `/slideshow-script` or `/tiktok-slideshow`):

```bash
ls marketing/content-specs/*.yaml 2>/dev/null
```

**If content specs exist:** Read them. Each spec has `content_type`, `visual_direction`, `slides[]`, and `scripting_framework`. Skip to Phase 2d — the scripts are already written.

**If no content specs:** Proceed to interrogation (2b).

#### 2b. Interrogate the User

Use AskUserQuestion to understand the goal. Don't assume 5 agents or any specific format:

```
"What visual content do you need? Help me understand so I can design the right approach."

Options:
1. "TikTok slideshow (1080×1920, 5-9 slides)" — vertical storytelling
2. "Instagram carousel (1080×1350, 5-9 slides)" — educational/positioning
3. "Instagram single post (1080×1080 or 1080×1350)" — one powerful image
4. "Instagram story / Reel cover (1080×1920)" — single claim
5. "Social graphics batch" — multiple formats for one message
6. "Ad creative" — single high-impact visual for ads
7. "Custom" — user describes what they need
```

Then follow up based on answer:

```
"How many variations do you want to explore?"

Options:
1. "Just 1 great one" — single agent, iterate until perfect
2. "2-3 options" — focused exploration
3. "5 full variations" — maximum creative exploration
4. "Match my content specs" — 1 per content spec YAML
```

Then:

```
"What's the priority?"

Options:
1. "Speed — get something designed fast" → fewer agents, simpler approach
2. "Quality — make it exceptional" → load /frontend-design, thorough review
3. "Exploration — see many different directions" → max agents, varied styles
```

**Use these answers to determine:**
- How many agents to spawn (1-5)
- Whether to load `/frontend-design` for design quality
- Which variation directions to use
- How much review/iteration to do

#### 2c. Select Variations (Intelligent)

Based on interrogation, select the RIGHT number of variations with the RIGHT directions:

**Variation types for marketing content:**

| Direction | What Changes | Good For |
|-----------|-------------|----------|
| **Typographic** | Text-dominant, massive display type, minimal decoration | Quote posts, positioning statements |
| **Data-Led** | Giant stat numbers as visual anchors, text secondary | Proof points, market data, before/after |
| **Editorial** | Magazine-layout feel, asymmetric text placement, generous white space | Long-form carousel slides, thought leadership |
| **Product-Forward** | Mockup/screenshot center stage, text supports the visual | Feature demos, app screenshots |
| **Atmospheric** | Arabic script as decoration, calligraphic accents, spacious and reverent | Spiritual content, Quranic references |
| **Bold Minimal** | One idea per slide, maximum white space, zero ornamentation | Hook slides, CTAs, single-message posts |
| **Structured** | Clear grid feel, numbered steps, consistent slot layout | How-it-works, listicles, tutorials |
| **Contrast Play** | Dramatic scale differences, weight extremes | Attention-grabbing hooks, comparison content |
| **Stacked** | Vertical rhythm, everything centered, one element per visual beat | Stories, reels covers |
| **Split** | Two-column or two-zone layout, tension between halves | Before/after, problem/solution |

Rules for selection:
- Each must be **tangibly different** (different layout structure, emphasis, visual rhythm)
- Match directions to the content type and user's priority
- If user chose "Just 1 great one" — pick the best direction for their content and go
- If content specs exist, use their `visual_direction` field

Present the plan via AskUserQuestion:
```
"Here's my design plan: {N} variation(s), {content_type}:"

1. **{Direction}** — {one-line description of this approach}
[... more if multiple]

Options:
1. "Looks great, go" — proceed
2. "Change direction(s)" — user adjusts
3. "Add more variations" — increase agent count
4. "Fewer variations" — reduce agent count
```

#### 2d. Define Content Spec

**If content specs exist from /slideshow-script:** Read them. Each agent gets its own spec's content.

**If no content specs:** Write out the exact content each agent will design with:
- Every text string (headings, body copy, labels, CTAs)
- Which positioning angle is being used
- Every slide/section and its purpose
- Information hierarchy (what's most important)
- Signature phrases from `brand/voice-profile.md`

Show to user via AskUserQuestion:
```
"Here's the content for the designs. Anything to add or change?"

[slide-by-slide or section-by-section copy]

Options:
1. "Looks complete, go" — proceed
2. "Missing something" — user adds content
3. "Change the copy" — user edits specific text
```

**Write approved content to `marketing/content-specs/{name}.yaml`** so it persists for downstream skills (/video-content). If content specs already exist from `/slideshow-script`, do NOT overwrite them — they are the source of truth. Only write new specs when running standalone (no prior scripting phase).

Do NOT proceed to Phase 3 until user approves variations AND content.

### Phase 3: Create Team and Tasks

```
TeamCreate: name="paper-mktg", description="{N} on-brand marketing designers in Paper"
```

Create N tasks (all parallel, no dependencies) + 1 review task (blocked by all N).

**Each task description MUST include all of this** (the agent picking it up has zero prior context):

1. **Paper Workspace**: File name (from get_basic_info), existing artboards to avoid, loaded fonts available
2. **Context**: What is being designed, which project, what the product does (1-2 sentences)
3. **Brand System**: Full palette (every hex with role), typography (every font/weight/size with role), layout tokens. Copied verbatim.
4. **Voice Rules**: Key do's/don'ts from voice-profile.md. Signature phrases. Words to avoid.
5. **Design Brief**: This variation's specific layout approach, emphasis, vibe. What makes it different.
6. **Content Spec**: Every piece of text, every slide/section — from content spec YAML or Phase 2d
7. **Paper MCP Workflow**: The exact tool sequence (see Phase 4)
8. **Paper HTML Rules**: From [references/paper-mcp-rules.md](references/paper-mcp-rules.md)
9. **Quality Rubric**: From [references/agent-quality-rubric.md](references/agent-quality-rubric.md)
10. **Platform Conventions**: From [references/platform-conventions.md](references/platform-conventions.md) for the target platform
11. **Tradeoffs**: What could go wrong with this layout variation and how to counter it
12. **Artboard spec**: Name ("Marketing: {variation_name}"), width, height

### Phase 4: Spawn Designer Agents

Spawn all in a **single message** (parallel). Each agent gets:

```
subagent_type: "general-purpose"
model: "sonnet"
team_name: "paper-mktg"
run_in_background: true
```

**Agent prompt structure:**

```
You are a senior marketing designer creating on-brand visual content.
Your layout approach: {variation_style}. {one-sentence vibe}

## Design Quality
Read the /frontend-design skill at ~/.claude/skills/frontend-design/SKILL.md for design principles.
Apply Swiss editorial typography: maximize contrast between display (700, 200px+) and label (300, 14px).
Spacing: tighter to group, generous to breathe. Color: one accent moment per slide.
Layout: favor asymmetry. Scale: dramatic differences (hero 3x larger than secondary).

## Your Task
Design {content_type} for {project_name} in Paper design tool. Create ONE artboard ({width}x{height}).

Read your full task description by calling TaskGet with taskId "{id}",
then mark it in_progress with TaskUpdate. When done, mark it completed.

## Paper Workspace
You are working in Paper file "{fileName}".
Existing artboards: {list}.
Loaded fonts: {list from get_basic_info}.
Do NOT modify existing artboards.

## Paper MCP Workflow
1. mcp__paper__get_basic_info() — confirm file state
2. mcp__paper__get_font_family_info({brand fonts}) — VERIFY every font before use
3. mcp__paper__create_artboard() — name: "Marketing: {variation_name}", width/height
4. mcp__paper__write_html() — build slide 1 in detail (2-3 calls for first slide)
5. mcp__paper__duplicate_nodes() — clone slide 1 structure for remaining slides
6. mcp__paper__set_text_content() — swap text per cloned slide
7. mcp__paper__update_styles() — adjust colors, sizes, emphasis per slide
8. mcp__paper__get_screenshot() — every 2-3 modifications, critique against quality rubric
9. mcp__paper__finish_working_on_nodes() — ALWAYS call when done

## Brand System
{full palette, typography, layout tokens from task description}

## Voice Rules
{key do's/don'ts, signature phrases, words to avoid}

## Design Brief
{this variation's layout approach, emphasis, vibe, tradeoffs}

## Content
{verbatim content spec — unique script per agent if from /slideshow-script}

## Quality Rubric
After each screenshot, check: (1) text readability at 50% zoom, (2) brand fidelity,
(3) archetype match, (4) platform safe zones, (5) visual rhythm, (6) hierarchy.
Fix any failures BEFORE moving to next slide.

## Paper HTML Rules
- Inline styles ONLY (style="...")
- display: flex for ALL containers (no grid, no margins, no tables)
- Google Fonts via font-family name (verify with get_font_family_info first)
- NO emojis — use SVG icons or text
- Arabic text: direction: rtl; font-family: "Noto Naskh Arabic"
- Build incrementally. Screenshot every 2-3 writes.
- Set layer-name attribute for semantic names.
```

### Phase 5: Monitor and Review

1. Shut down agents as they complete (`SendMessage type: "shutdown_request"`)
2. When all done, screenshot each artboard via `mcp__paper__get_screenshot()`
3. Present all with critique for each:
   - **Best element**: The standout design/layout decision
   - **Brand fidelity**: Does it feel on-brand? Colors, fonts, voice correct?
   - **Risk**: What could go wrong if this is the chosen direction
4. If multiple variations, show comparison matrix:

```
| Criterion | {Var 1} | {Var 2} | ... |
|-----------|---------|---------|-----|
| Hook strength | 8/10 | 9/10 | ... |
| Text readability | 9/10 | 8/10 | ... |
| Brand fidelity | 9/10 | 9/10 | ... |
| Visual variety | 7/10 | 9/10 | ... |
| Animation potential | 7/10 | 9/10 | ... |
```

5. Ask user via AskUserQuestion:
```
"Here are the variations. What would you like to do?"

Options:
1. "Use #{n}" — pick one as the final
2. "Mix elements" — combine best parts of multiple
3. "Refine #{n}" — iterate on a favorite
4. "Create more slides in #{n}'s style" — extend the chosen direction
5. "Start over with different content" — new round
```
6. Clean up: `TeamDelete`

### Phase 6: Export and Handoff

After user selects a variation:

1. **Extract JSX** from selected artboard via `mcp__paper__get_jsx()`:
   ```
   mcp__paper__get_jsx(nodeId: "{selected_artboard_id}")
   ```
   Save extracted HTML/CSS for Remotion reference.

2. **Write handoff YAML** to `marketing/handoffs/{name}-handoff.yaml`:
   ```yaml
   handoff_version: 1
   project: {project_name}
   content_type: {content_type}
   selected_variation: {variation_name}
   artboard:
     name: "Marketing: {variation_name}"
     width: {width}
     height: {height}
     slide_count: {N}
   content_spec: "marketing/content-specs/{name}.yaml"
   brand_snapshot:
     bg_primary: "{hex}"
     bg_deep: "{hex}"
     accent: "{hex}"
     accent_muted: "{rgba}"
     text_primary: "{hex}"
     text_muted: "{rgba}"
     divider: "{rgba}"
     font_display: "{font_family}"
     font_display_weights: [300, 400, 700]
     font_body: "{font_family}"
     font_body_weights: [300, 400]
   export_search_pattern: "{variation_name}@2x.png"
   extracted_jsx:
     slide_1: "{jsx}"
     slide_2: "{jsx}"
   ```

3. **Instruct user to export** from Paper UI:
   ```
   "Select the '{variation_name}' artboard in Paper and export as PNG @ 2x.
   Save to ~/Desktop/ or your preferred location.
   Then tell me the file path so /video-content can process it."
   ```

### Phase 7: Log and Register (if workflow logging active)

If a workflow log exists at `marketing/logs/`, append steps for:
- Which brand files were read
- Which content type was created
- Which variation was chosen
- What the final artboard looks like
- Tool calls made

Update `brand/assets.md` with the new asset.

## Anti-Patterns

- **Spawning before confirming** — Each agent costs tokens and time. Creating 5 agents for a user who wanted 1 is wasteful and frustrating. Always get explicit approval on both the variation plan AND the content before spawning.
- **Hardcoding brand values** — If you put hex codes or font names directly in the skill, it breaks the moment it's used on a different project. Always read from brand/ files at runtime so the skill works universally.
- **Using CSS grid in Paper** — Paper MCP's HTML renderer only supports `display: flex`. Using `grid`, margins, or HTML tables produces broken layouts with no error message — elements just disappear or stack incorrectly.
- **Modifying existing artboards** — The user's existing artboards may contain in-progress work. Agents must create new artboards only. Touching existing work risks destroying hours of effort.
- **Identical variations** — The entire value of spawning multiple agents is seeing genuinely different creative directions. If two designs look similar, the user got one option at the cost of two. Each variation must use a structurally different layout approach from the direction table.
- **Skipping font verification** — Paper renders missing fonts as a default fallback, which silently breaks the brand look. Always call `get_font_family_info()` first to confirm the font is loaded.
- **Giant write_html calls** — Paper's HTML renderer handles ~15 lines per call reliably. Larger blocks risk partial rendering or silent truncation. Build incrementally: hero first, then body, then footer.

## Edge Cases

- **Paper MCP not connected** — If `get_basic_info()` fails, tell the user to open Paper and connect the MCP server. Do not proceed without it.
- **Font not available** — If `get_font_family_info()` returns no match, fall back to a similar Google Font that IS available. Note the substitution in the task description.
- **Agent task fails** — If an agent can't complete (Paper errors, timeout), note which variation failed and offer to re-run just that one.
- **No brand files exist** — Skill still works. Use AskUserQuestion to gather basics (colors, fonts, vibe) and write creative-kit.md before proceeding.
- **Content specs from /slideshow-script are stale** — If content spec YAMLs exist but are older than the current positioning.md, flag this to the user and ask whether to use existing specs or regenerate.

## Principles

- **Intelligent interrogation**: Use AskUserQuestion to understand the goal BEFORE deciding agent count and approach. Don't assume 5 agents every time.
- **Rich task descriptions**: An agent picking up a task cold must have everything. No assumptions.
- **Duplicate-first building**: Build slide 1 in detail, duplicate for remaining slides, then customize. 40% faster, more consistent.
- **Frontend design quality**: Load /frontend-design skill for Swiss editorial typography and layout principles.
- **Screenshot reviews with rubric**: Agents screenshot every 2-3 writes and check against the 6-point quality rubric.
- **Font verification**: Always get_font_family_info before using any font.
- **Distinct variations**: If two designs look similar, the skill failed. Same brand, different layouts.
- **Brand fidelity**: Every variation MUST use the project's brand palette, fonts, and voice.
- **Content spec persistence**: Write approved content to YAML so downstream skills can read it.
- **JSX extraction**: Always get_jsx from selected artboard for Remotion handoff.
- **Universal**: Works for any project with `brand/` files. Reads brand system at runtime, never hardcodes.
