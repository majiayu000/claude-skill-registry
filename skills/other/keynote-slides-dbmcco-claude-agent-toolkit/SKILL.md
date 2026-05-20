---
name: keynote-slides
description: Build Keynote-style single-file HTML slide decks with brand-ready templates, minimal navigation, and Gemini nano banana media generation. Includes Narrative Engine integration for framework-driven deck creation with 17 proven storytelling structures and 5-agent review panel. Use when creating or editing slide decks, transforming content into presentations, or generating slide visuals.
---
<!-- ABOUTME: Skill guide for building Keynote-style HTML decks with brand tokens and Gemini media hooks. -->
<!-- ABOUTME: Points to the single-file template, templates, and media generation workflow. -->
# Keynote Slides

## Assets

- `assets/keynote-slides.html` holds the single-file slide deck template.
- `references/brand-guidelines.md` captures brand tokens, typography, and image style guidance.
- `references/gemini-media.md` documents the Gemini nano banana and Veo media settings.

## Workflow

1. Run the deck bootstrap to create a deck folder:
```bash
scripts/new-deck.sh example-pitch --entity northwind --title "Example Pitch" --type pitch
```
2. Update `decks/brands.js` when brand tokens change.
3. Edit `decks/<deck-id>/index.html` and duplicate slides inside `<main id="deck">`, keeping each `data-title` unique.
4. Use layout classes (`layout-title`, `layout-split`, `layout-grid`, `layout-metrics`, `layout-quote`) to keep spacing consistent.
5. Apply `reveal` plus `--reveal-index` to stagger key elements.

## Entities

- Use the generator panel to select the active entity profile.
- Add `data-entity="entity-id"` on a slide to override the global profile for that slide.
- Add `?entity=entity-id` to the URL for a quick switch.
- Use `mediaPromptPrefix` in `brandProfiles` to keep Gemini media outputs on brand.

## Deck storage

- `decks/<deck-id>/index.html` is the editable deck file.
- `decks/<deck-id>/deck-config.js` stores deck metadata (entity, title, resources).
- `decks/<deck-id>/deck.json` stores the same metadata in JSON form.
- `decks/<deck-id>/slides.md` is for draft copy and notes.
- `decks/<deck-id>/resources/assets/` holds logos, images, and media inputs.
- `decks/<deck-id>/resources/materials/` holds briefs, pricing docs, P&L inputs, and outlines.

### PMF Panel Integration

Export PMF Panel findings as deck input materials:

```bash
# From pmf-panel directory
.claude/export-deck-brief.sh <scenario-id>

# Copy to deck materials
cp scenarios/<scenario-id>/deck-brief.md \
   ../keynote-slides-skill/decks/<deck-id>/resources/materials/pmf-brief.md
```

The brief includes diagnosis, scenarios, 30/60/90 plan, and specialist perspectives ready for narrative engine ingestion.

## Collaboration

- Co-author the narrative: propose headlines, POV, and slide ordering based on `deckType` and entity preferences.
- Keep the brief in `resources/materials/brief.md` and capture evolving preferences in `deck.json` or `decks/brands.js`.
- Use concise headline options (3-5 variants) and confirm direction before building slides.

## Review loop

- Use the Chrome Devtools MCP tools to capture a snapshot/screenshot and review layout.
- Check hierarchy, alignment, spacing rhythm, and contrast; then adjust copy and spacing.
- Use the generator panel for brand-aware media, then re-check balance and whitespace.

## Templates

- Copy markup from the `<template>` blocks at the bottom of the file.
- Replace placeholders with branded copy, numbers, and visuals.

## Media generation

1. Add `data-gen` and `data-prompt` to `<img>` or `<video>` elements.
2. Open the generator panel with `g` or the `Gen` button.
3. Save the API key and model settings to localStorage (never commit keys).
4. For image-to-image or image-to-video, load a base image in the panel.
5. Run "Generate slide" or "Generate all" and review outputs.

### Model-Mediated Image Acquisition

Use the `/acquire-images` skill (see `skills/acquire-images.md`) to populate slides with visuals.

Claude decides whether to **generate** (Gemini) or **search** (stock photos) for each slide:

| Content Type | Decision | Why |
|--------------|----------|-----|
| Diagrams, flowcharts | GENERATE | Custom layouts, brand colors |
| Data visualizations | GENERATE | Precise data representation |
| Real-world photos | SEARCH | Authentic people, places |
| Team/people shots | SEARCH | Realistic human photos |
| Abstract concepts | GENERATE | Metaphorical, brand-styled |
| Branded hero images | HYBRID | Search base + AI overlay |

**Search sources:** Unsplash, Pexels, Google Custom Search.

**Attribution:** Downloaded images tracked in `resources/materials/image-credits.json`.

See `skills/acquire-images.md` for the full workflow.

## Preview

```bash
scripts/serve-decks.sh
```
Then open `http://<tailscale-ip>:8921/decks/<deck-id>/index.html`.

## Speaker notes

- Add per-slide notes with a hidden block:
  ```html
  <aside class="slide-notes">Speaker notes here.</aside>
  ```
- Toggle the notes panel with the "Notes" button or press `n`.
- Append `?notes=1` to open notes by default.
- Use "Export notes" to download a markdown file.

## Animation + SVG

- Use `data-anim` for lightweight entrance animations (fade, slide-up, slide-left, slide-right, scale-in).
- Set `--anim-delay` to stagger; avoid mixing with `reveal` on the same element.
- Disable animation with `?motion=off` or rely on `prefers-reduced-motion`.
- Inline SVG diagrams use `.diagram` and `data-media="svg"`:
  ```html
  <svg class="diagram" data-media="svg" viewBox="0 0 800 450" role="img" aria-label="Diagram"></svg>
  ```
- Keep media lanes explicit:
  - `data-gen` = Gemini only (optional `data-media="gemini"`).
  - Inline SVG = no `data-gen`.
  - Static images/videos = no `data-gen`.

### Micro Animations

Micro animations are **small decorative accent elements** that add subtle motion to slides without distracting from content.

**What micro animations ARE:**
- Small accent lines that expand/draw next to headlines
- Subtle decorative strokes or shapes that pulse gently
- Tiny visual flourishes positioned near text (not on text)
- CSS-driven, lightweight, and unobtrusive

**What micro animations are NOT:**
- Large SVG graphics or overlays covering slide areas
- Animations applied directly to text (no flashing, glowing, or bouncing text)
- Complex particle systems or heavy motion graphics
- Anything that competes with or obscures content

**Implementation:**
```html
<!-- Accent line after a headline -->
<h1 class="title">Your headline here</h1>
<span class="accent-line"></span>
```

**Available classes:**
- `.accent-line` — 80px amber line that expands from left, then pulses
- `.accent-line.long` — 120px version for major headlines

**Behavior:**
- Line draws in from left (0.8s ease-out) when slide becomes active
- Then gently pulses (opacity + slight scale) on a 4s cycle
- Respects `prefers-reduced-motion` and `?motion=off`

**When to use:**
- Title slides (layout-title) to add visual interest
- Key message slides where you want emphasis
- Sparingly — 3-4 slides per deck maximum

## Copy editor

- Open `decks/<deck-id>/editor.html` in a second window to edit copy without touching HTML.
- Use the editor "Open deck" button to connect and update the live preview.
- For existing decks, copy the template first:
  ```bash
  cp skills/keynote-slides/assets/keynote-editor.html decks/<deck-id>/editor.html
  ```
- Edits are stored in localStorage; export JSON from the editor for handoff.

## PDF export

- Use the browser print dialog and "Save as PDF".
- Enable background graphics for gradients and color fills.
- The template includes print styles to paginate each slide.
- CLI option:
  ```bash
  node scripts/export-pdf.js decks/<deck-id> --out /tmp/<deck-id>.pdf
  ```

## Navigation

- Arrow keys, PageUp/PageDown, Space.
- Home/End for first or last slide.
- Use `#slide-title` hash navigation for direct jumps.

## Review Mode / Feedback System

Enable reviewers to leave comments on deck elements for collaborative feedback.

### Entering Review Mode

- Click the "Review" button in the bottom toolbar (next to Gen)
- Press `r` key to toggle review mode
- Add `?review=1` to the URL to start in review mode

### Adding Comments

1. In review mode, hover over elements to see them highlighted
2. **Click** any commentable element (titles, text, cards, metrics, media frames)
3. **Or select text** within an element to comment on specific wording/typos
4. First-time commenters enter name and email (stored in session)
5. Type feedback in the popover and click "Add Comment"
6. A numbered badge (①②③) appears on commented elements for easy reference

### Viewing Comments

- Press `c` or click the sidebar toggle to open the comment sidebar
- Comments are grouped by slide
- Click "Go to slide" to navigate to the commented element
- Mark comments as resolved or delete them

### Exporting Feedback

From the comment sidebar:
- **Export JSON** - Downloads `comments-<deck-id>.json` for backup or import
- **Export MD** - Downloads markdown summary for sharing or Claude iteration

### Feedback Viewer Page

Use `assets/feedback-viewer.html` to review all feedback outside the deck:

1. Open `feedback-viewer.html` in a browser
2. Load a `comments.json` file or enter a URL
3. Filter by open/resolved status
4. Mark comments as resolved
5. Export updated JSON or markdown

Add `?url=<path-to-json>` to auto-load comments.

### Comment Data Structure

Comments are stored in localStorage keyed by deck ID. Export structure:

```json
{
  "deckId": "example-pitch",
  "nextNumber": 4,
  "comments": [
    {
      "id": "c_1706123456789_abc123",
      "number": 1,
      "slideIndex": 2,
      "slideTitle": "Our Solution",
      "elementSelector": "[data-comment-target='headline']",
      "elementText": "First 50 chars of element...",
      "selectedText": "specific phrase",
      "comment": "This needs more specificity",
      "author": {
        "name": "Sarah Chen",
        "email": "sarah@example.com"
      },
      "createdAt": "2024-01-24T10:30:00Z",
      "resolved": false
    }
  ]
}
```

- `number`: Sequential comment number (①②③) for easy reference in feedback
- `selectedText`: If reviewer selected specific text, captures that selection (null otherwise)

### Element Targeting

For precise comment targeting, add `data-comment-target` attributes:

```html
<h2 data-comment-target="solution-headline">Our Solution</h2>
<p data-comment-target="value-prop-1">We reduce costs by 40%...</p>
```

Elements without explicit targets use a generated CSS selector path.

---

## Narrative Engine Integration

For content-driven deck creation, use the Narrative Engine workflow that matches your material to proven storytelling frameworks.

### Reference Files

- `references/narrative-engine/narrative-arcs.md` — Beat-by-beat structures for 10 narrative arcs
- `references/narrative-engine/framework-selection.md` — Selection matrix by audience/purpose/content
- `references/narrative-engine/framework_selection_guide.md` — Deep pairing guidance for arcs + frameworks
- `references/narrative-engine/communication-frameworks.md` — 7 efficiency-optimized frameworks
- `references/narrative-engine/checklists.md` — Quality gates for narrative + copy review
- `references/narrative-engine/agent-reference-*.md` — Agent-specific frameworks for review

### Workflow: Narrative Build

1. **Ingest resources:** Run `node scripts/ingest-resources.js decks/<deck-id>` to read all materials
   - Or use `node scripts/narrative-build.js decks/<deck-id>` to prepare model-mediated prompts
2. **Focal discovery + discovery:** Align on the one point, then answer 5 questions (audience, purpose, content type, tone, reveal)
3. **Density + framework match:** Choose density mode, then get 2-3 recommendations with content mapped to structure
4. **Deck generation:** Build slides with source attribution tags
5. **Review panel:** 5 agents + Director synthesize feedback

### Discovery Questions

| Question | Options |
|----------|---------|
| **Audience** | Executive, Technical, Investors, Skeptics, General, Mixed |
| **Purpose** | Persuade, Inform, Inspire, Align, Report, Defend, Entertain |
| **Content type** | Research, Strategy, Origin story, Post-mortem, Pattern insight, etc. |
| **Tone** | Authoritative, Provocative, Warm, Urgent, Balanced, Visionary |
| **Reveal potential** | Yes (has surprise), No (straightforward), Help me find one |

### Framework Selection Quick Reference

| If your content has... | Consider... |
|------------------------|-------------|
| A genuine surprise | The Prestige or Mystery Box |
| Multiple stakeholder views | Rashomon |
| A transformation story | Hero's Journey |
| Future vision | Time Machine |
| Root cause analysis | Columbo |
| Strategy/roadmap | The Heist |
| Paradigm shift | Trojan Horse |

### 5-Agent Review Panel

| Agent | Lens | Key Question |
|-------|------|--------------|
| **Audience Advocate** | Target audience persona | "Does this land for [audience]?" |
| **Comms Specialist** | Messaging, emotion, PR risk | "Is this tight and bulletproof?" |
| **Visual Designer** | Metaphor coherence, S.T.A.R. moments | "What visual makes this unforgettable?" |
| **Critic** | Pacing, weak links, efficacy | "What's the weakest link?" |
| **Content Expert** | Accuracy, logic, sources | "Can every claim be defended?" |

### Stress Test Panel (Optional)

After the 5-agent review, optionally stress-test with stakeholder personas auto-selected by content type:

| Persona | Questions | Best For |
|---------|-----------|----------|
| **Engineer** | "How does this actually work?" | Technical proposals, product launches |
| **Skeptic** | "Why should I believe this?" | Bold claims, paradigm shifts |
| **Risk Officer** | "What could go wrong?" | Strategy, transformation, investment |
| **CFO** | "What are the numbers?" | Pitches, business cases, ROI claims |
| **Lawyer** | "What's the exposure?" | Policy, compliance, external-facing |
| **Conservative** | "Why change what's working?" | Change management |
| **COO** | "Would this actually work?" | Execution plans, go-to-market |

The Director triages findings into **Must Fix**, **Should Fix**, and **Could Fix** categories.

### Source Attribution Tags

| Tag | Meaning |
|-----|---------|
| `[DIRECT]` | Verbatim from source material |
| `[PARAPHRASE]` | Restated ideas |
| `[ELABORATED]` | Expanded concept |
| `[SYNTHESIZED]` | Combined multiple sources |
| `[GENERATED]` | New content for flow |

### Headline Rules

- **Image & Action:** Concrete nouns + strong transitive verbs; avoid "is/are"
- **Tension & Turn:** Because/Therefore, Not/But, Before/After
- **Cadence:** 8-14 words; two-beat rhythm
- **Specific Anchors:** Time/place/actor/number in every third headline
- **Power verbs:** tilts, unseats, ignites, drains, compounds, unlocks, anchors, accelerates
- **Metaphor family:** One per deck (journey OR ecology OR weather, etc.)

See `/docs/integrated-architecture.md` for full technical details.
