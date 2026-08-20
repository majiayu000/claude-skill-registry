---
name: prd-v04-visual-prototype-gate
description: >
  Generate visual prototype prompts from SCR- entries for Google Stitch (or equivalent UI generation tool).
  Triggers on: 'make a prototype', 'visualize screens', 'generate Stitch prompt', 'I need a visual demo',
  'prototype the workflow', 'show me what this looks like', 'get this to a demo', 'visual gate'.
  Consumes SCR- (Screen Flow Definition), PER- (Personas), UJ- (User Journeys), DES- (Design Components).
  Outputs Stitch prompt blocks per SCR- entry + Feedback Capture Template. No new SoT IDs created —
  this skill makes existing SCR- entries visual and routes feedback back to them.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Visual Prototype Gate

Position in workflow: v0.4 Screen Flow Definition → **v0.4 Visual Prototype Gate** → v0.5 Red Team Review

Screens on paper are hypotheses. Screens rendered visually are testable. This skill converts SCR- entries into structured prompts for Google Stitch (or any UI generation tool), then captures feedback routed back to specific SoT IDs.

**Rule: No product advances past v0.4 without a visual prototype reviewed by at least one stakeholder.**

## Consumes

- **SCR-\* entries** (from Screen Flow Definition) — Each SCR- becomes one Stitch prompt. 1:1 mapping, no exceptions.
- **PER-\* entries** (from Persona Definition) — User context shapes copy, complexity, and emotional framing per screen.
- **UJ-\* entries** (from User Journey Mapping) — Journey position determines each screen's emotional beat (uncertainty → clarity → confidence).
- **DES-\* entries** (from Screen Flow Definition) — Shared components referenced in prompts for visual consistency.
- **BR-\* business rules** — Constraints affecting visual layout (pricing tiers, role-based visibility, data rules).

## Produces

- **Stitch Prompt Block per SCR-** — One structured prompt per screen, ready to paste into Stitch. Grouped by UJ- journey for context.
- **Prototype Context Brief** — Product context + design style preamble (pasted once into Stitch before screen prompts).
- **Feedback Capture Template** — Table mapping each prototype screen to its SCR- ID for structured review. See `assets/feedback-capture-template.md`.
- **No new SoT IDs** — This skill visualizes existing IDs. Feedback routes back to SCR-, DES-, or CFD- entries.

## Step-by-Step Process

### Step 1: Confirm Inputs Exist

Check that Screen Flow Definition is complete:
- [ ] At least 3 SCR- entries exist with Purpose, Key Elements, and Related IDs populated
- [ ] At least 1 UJ- journey references those screens
- [ ] Design style preference confirmed with user (or default: "Clean B2B SaaS, minimal, professional")

If SCR- entries are incomplete, stop and run `prd-v04-screen-flow-definition` first.

### Step 2: Write the Prototype Context Brief

One block, written once per product. This is pasted into Stitch as the opening context before individual screen prompts.

```
PRODUCT CONTEXT
[2-3 sentences from PRD v0.1 Spark: what the product is, who uses it, what pain it solves]

PRIMARY USER
[From PER-001: role, context, technical comfort level]

DESIGN STYLE
[Confirmed aesthetic — e.g., "Clean B2B SaaS, dark sidebar, minimal. Color for status only."]
```

### Step 3: Generate Per-Screen Prompts

For each SCR- entry, produce one Stitch prompt block. Follow this template:

```
SCREEN: [SCR-XXX] — [Screen Name]
Journey position: [UJ-XXX], Step [N] of [Total]
User goal: [From SCR- Purpose field]
Situation: [What just happened — derived from prior UJ- step]
Key UI elements: [From SCR- Key Elements, using specific UI/UX keywords]
  - [Element 1: be specific — "green 'Run' button, top right, disabled until selection made"]
  - [Element 2: reference DES-XXX if shared component]
  - [Element 3+]
Constraints: [BR-XXX rules affecting this screen — e.g., "free tier sees max 3 items"]
Emotional beat: [Derived from journey position — early=uncertainty, mid=engagement, end=confidence]
Layout: [UI surface type — full page, sidebar panel, modal, card grid, etc.]
```

**Stitch-specific guidance** (from research):
- Use UI/UX keywords: "navigation bar," "card layout," "call-to-action," not vague terms like "a button"
- One screen per Stitch generation for best results — do not combine multiple SCR- entries into one prompt
- Include adjectives for aesthetic: "minimal," "clean," "dark," "warm" — Stitch uses these for palette and typography
- Reference specific positions: "top-right," "below the header," "spanning full width"

### Step 4: Identify the Money Shot

Select the single screen that communicates core product value fastest. This is typically the screen at the UJ- "Moment of Value" step. Mark it in the output. This frame gets screenshotted for any stakeholder deck, landing page, or pitch.

### Step 5: Output Feedback Capture Template

Alongside prompts, output the feedback capture template (see `assets/feedback-capture-template.md`). This is the structured review artifact — reviewers annotate per-screen, feedback routes to specific IDs.

## Stitch Workflow Notes

Google Stitch iterates best with incremental refinement:
1. Paste the Prototype Context Brief first
2. Generate one screen at a time using per-screen prompts
3. Refine each screen with targeted follow-ups ("Move the CTA to the right," "Change card layout to 2-column grid")
4. Export to Figma if design iteration continues beyond prototype stage

For non-Stitch tools, see `references/tool-adaptation-notes.md`.

## Quality Gates (v0.4 → v0.5 Readiness)

Before proceeding to v0.5 Red Team Review:
- [ ] All SCR- entries have a corresponding visual prototype screen
- [ ] At least one stakeholder has reviewed the prototype
- [ ] Feedback Capture Template is completed with disposition for each item
- [ ] Money Shot identified and captured

## Downstream Connections

| Consumer | What It Uses |
|----------|--------------|
| **v0.5 Red Team Review** | Visual prototype informs risk assessment — "does this feel buildable?" |
| **v0.6 Architecture** | Validated screens inform API data requirements |
| **v0.7 Build Execution** | Prototype becomes the visual spec for implementation |
| **Stakeholder Communication** | Money Shot used in decks, pitches, landing pages |

## Detailed References

- **Feedback capture template**: See `assets/feedback-capture-template.md`
- **Tool adaptation notes**: See `references/tool-adaptation-notes.md`
- **Screen count guidelines**: See `references/screen-count-guidelines.md`
