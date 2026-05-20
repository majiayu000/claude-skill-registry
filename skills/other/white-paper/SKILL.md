---
name: white-paper
description: Build single-file HTML white papers with brand-ready templates, print-optimized 8.5x11 layout, Gemini media generation, and SVG diagram creation. Includes narrative engine with 10 story arcs and communication frameworks for research papers, strategic reports, and thought leadership content.
---
<!-- ABOUTME: Skill guide for building print-ready HTML white papers with brand tokens, narrative engine, and media hooks. -->
<!-- ABOUTME: Points to the single-file template, visualization tools, and model-mediated discovery workflow. -->
# White Paper Skill

## Assets

- `assets/white-paper.html` — Single-file white paper template (1600+ lines)
- `references/brand-guidelines.md` — Brand tokens, typography, and image style guidance
- `references/gemini-media.md` — Gemini API settings and prompt engineering tips
- `references/narrative-engine/` — Full narrative framework library (10 arcs + communication frameworks)

## Core Workflow

### 1. Bootstrap a Paper

```bash
scripts/new-paper.sh market-analysis --entity synthyra --title "Q1 Market Analysis"
```

This creates:
```
papers/market-analysis/
├── index.html           # Main paper (edit sections here)
├── paper-config.js      # Paper metadata (JS)
├── paper.json           # Paper metadata (JSON)
├── draft.md             # Working notes and outline
└── resources/
    ├── assets/          # Logos, images, media inputs
    └── materials/       # Briefs, research, data sources
        └── brief.md     # Paper brief template
```

### 2. Gather Materials

Place source documents in `resources/materials/`:
- Research reports, data files, notes
- Run ingestion to summarize for model synthesis:

```bash
node scripts/ingest-resources.js papers/market-analysis
```

### 3. Narrative Discovery ("Walk Me Through")

Run the narrative build script to start model-mediated discovery:

```bash
node scripts/narrative-build.js papers/market-analysis
```

This generates prompts for:
1. **Audience** — Who will read this?
2. **Purpose** — What should they DO after reading?
3. **Content Type** — Research, analysis, strategy, case study?
4. **Tone** — Authoritative, provocative, balanced, urgent?
5. **Reveal Question** — Does material have a genuine surprise?
6. **Density Mode** — Executive (4-8 pages), Standard (8-15), Comprehensive (15-25)

Output: `narrative-context.json` with framework selection and rationale.

### 4. Edit the Paper

Open `papers/<paper-id>/index.html` and:
- Update cover page (title, subtitle, author, date, logo)
- Fill in sections using templates at bottom of file
- Add charts, tables, figures as needed

### 5. Generate Visuals

Press `g` to open the generator panel:
- Add Gemini API key (stored locally, never committed)
- Select entity profile
- Click "Generate Figure" or "Generate All"

### 6. Export to PDF

- Open in browser and Print → Save as PDF
- Paper size: Letter (8.5 × 11)
- Enable background graphics
- Verify page breaks in print preview

---

## Narrative Engine

### 10 Story Arcs (Engagement-Optimized)

| Arc | Best For | Reveal Position |
|-----|----------|-----------------|
| **The Prestige** | Counterintuitive findings, debunking | ~60% |
| **Mystery Box** | Investigative reports, research | ~60% |
| **The Heist** | Strategy, transformation roadmaps | ~75% |
| **Time Machine** | Scenario planning, strategic planning | ~55% |
| **Trojan Horse** | Paradigm shifts, winning skeptics | ~50% |
| **Hero's Journey** | Origin stories, transformation cases | ~65% |
| **Freytag's Five-Act** | Complex emotional narratives | ~60% |
| **Columbo** | Post-mortems, root cause analysis | ~70% |
| **Game of the Scene** | Pattern recognition, insight transfer | ~65% |
| **Rashomon** | Multi-stakeholder, synthesis | ~70% |

### Communication Frameworks (Efficiency-Optimized)

| Framework | Best For |
|-----------|----------|
| **Minto Pyramid** | Executive communication, board presentations |
| **SCQA** | Opening hooks, problem framing |
| **AIDA** | Sales presentations, fundraising |
| **PAS** | Change management, selling to skeptics |
| **Raskin's Greatest Sales Deck** | B2B sales, category creation |
| **Duarte Resonate** | Keynotes, vision presentations |
| **SUCCESs** | Ensuring memorability |
| **Cialdini's Seven Principles** | Layering persuasion |

### Framework Selection by Content Type

| Content Type | Best Arc | Best Framework |
|--------------|----------|----------------|
| Research findings | Mystery Box | Pyramid + SUCCESs |
| Strategic plan | Heist | Raskin |
| Post-mortem | Columbo | Story Spine |
| Market analysis | Time Machine | SCQA |
| Case study | Hero's Journey | Story Spine |
| Policy recommendation | Rashomon | SCQA + Pyramid |

See `references/narrative-engine/framework-selection.md` for the full matrix.

---

## Visual Decision Logic

### When to Use SVG (built into template)

| Visual Type | Use SVG |
|-------------|---------|
| Bar charts | ✓ |
| Line charts | ✓ |
| Pie charts | ✓ |
| Process workflows | ✓ |
| Comparison tables | ✓ |
| Org charts | ✓ |
| Timelines | ✓ |
| Data-driven diagrams | ✓ |

**Benefits**: Crisp at any scale, brand colors built-in, no API calls, fast.

### When to Use Gemini AI

| Visual Type | Use Gemini |
|-------------|------------|
| Conceptual illustrations | ✓ |
| Abstract visualizations | ✓ |
| Photo-realistic images | ✓ |
| Complex metaphorical imagery | ✓ |
| Hero images | ✓ |

**Benefits**: Rich imagery, conceptual depth, emotional impact.

### SVG Templates in HTML

The template includes ready-to-use SVG patterns:

- `#template-bar-chart` — Vertical bar chart with axis, labels, grid
- `#template-line-chart` — Line chart with area fill, data points
- `#template-workflow` — Process boxes with arrows

Copy these templates and customize the data.

### Chart Color Tokens

```css
--chart-1: #ed8936;  /* Orange - primary */
--chart-2: #38A169;  /* Green - secondary */
--chart-3: #3182CE;  /* Blue */
--chart-4: #805AD5;  /* Purple */
--chart-5: #D53F8C;  /* Pink */
--chart-6: #00B5D8;  /* Cyan */
```

---

## Print Formatting

### Page Layout (8.5 × 11 Letter)

- Margins: 0.75in top/bottom, 1in left/right
- Content width: 6.5 inches
- Font size: 11pt body
- Line height: 1.6

### Page Break Control

```html
<!-- Force page break before a section -->
<section class="page" data-page="5">

<!-- Prevent break inside an element -->
<figure class="no-break">
```

### Screen Preview

On screen, the template shows:
- Gray background with centered white paper
- Page number indicators
- TOC navigation (left sidebar)
- Generator panel (bottom right)

All UI elements are hidden when printing.

---

## Entity Profiles

Define entities in `papers/brands.js`:

```javascript
window.WHITEPAPER_BRANDS = {
  synthyra: {
    label: "Synthyra",
    tokens: {
      "brand-ink": "#171923",
      "brand-accent": "#ed8936",
      // ...
    },
    fonts: {
      display: '"Inter", sans-serif',
      body: '"Inter", sans-serif'
    },
    mediaPromptPrefix: "modern biotech aesthetic, clean clinical style"
  }
};
```

Select entity via:
- Generator panel dropdown
- URL param: `?entity=synthyra`
- Per-section: `data-entity="synthyra"`

---

## Quality Checklists

### Master Quality Gates

- [ ] **Focal clarity**: Can you state the ONE point in one sentence?
- [ ] **Section necessity**: Does every section earn its place?
- [ ] **Headline power**: Vivid verb, concrete nouns, one idea
- [ ] **Evidence quality**: Every claim has supporting data?
- [ ] **Arc integrity**: Reveal at correct position?
- [ ] **Visual balance**: Charts and text complement each other?

### Headline Sweeps

1. **Clarity**: Understandable in <3 seconds?
2. **So What**: Answers "why should I care?"
3. **Specificity**: Numbers instead of vague words?
4. **Emotion**: Makes reader feel something?
5. **Proof**: Can be defended if challenged?

### Source Attribution Tags

| Tag | Meaning |
|-----|---------|
| `[PRIMARY]` | Original research or data |
| `[SECONDARY]` | Analysis of existing sources |
| `[CITED]` | Direct quote with attribution |
| `[SYNTHESIZED]` | Combined multiple sources |
| `[GENERATED]` | AI-assisted content |

See `references/narrative-engine/checklists.md` for complete quality gates.

---

## Paper Storage Structure

```
papers/<paper-id>/
├── index.html                    # Main paper
├── paper-config.js               # JS config
├── paper.json                    # JSON config
├── draft.md                      # Working notes
├── narrative-context.json        # Discovery decisions
├── generation-queue.json         # Visuals to generate
└── resources/
    ├── assets/                   # Logos, images
    └── materials/
        ├── brief.md              # Paper brief
        ├── ingestion.json        # Processed materials
        └── [source documents]
```

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `new-paper.sh` | Bootstrap new paper folder |
| `serve-papers.sh` | Local preview server (port 8922) |
| `ingest-resources.js` | Read and summarize materials |
| `narrative-build.js` | Generate discovery prompts |

---

## Preview & Export

### Local Preview

```bash
./scripts/serve-papers.sh
# Open: http://localhost:8922/papers/<paper-id>/index.html
```

### PDF Export

1. Open paper in browser
2. Press Cmd+P (Mac) or Ctrl+P (Windows)
3. Destination: Save as PDF
4. Paper size: Letter
5. Margins: Default (handled by CSS)
6. ☑ Background graphics (for colors)

---

## Collaboration

### Co-Author Role

When building a paper, Claude should:
- **Propose thesis** and key findings
- **Suggest structure** based on framework selection
- **Offer headline options** (3-5) for key sections
- **Confirm direction** before building content
- **Reference materials** from `resources/materials/`

### Capture Preferences

- Entity-level: `papers/brands.js`
- Paper-level: `paper.json`
- Evolving notes: `draft.md`

### Visual Review

- Use Chrome DevTools MCP to capture screenshots
- Check hierarchy, spacing, contrast, page flow
- Verify print preview before final export
