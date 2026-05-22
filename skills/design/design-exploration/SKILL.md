---
name: design-exploration
description: |
  Generate visual design proposal catalogues for existing projects. Use when:
  - User wants to explore design directions before implementation
  - Redesigning or refreshing an existing interface
  - Starting /aesthetic or /polish without clear direction
  - User says "explore designs", "show me options", "design directions"
  Keywords: design catalogue, proposals, visual exploration, aesthetic directions, DNA
---

# Design Exploration

Investigate existing designs, generate a visual catalogue of 5-8 diverse proposals, facilitate iterative refinement, and output a selected direction for implementation.

## When to Use

- Before `/aesthetic` or `/polish` when direction is unclear
- When user wants to see multiple design options visually
- When redesigning or refreshing existing UI
- When maturity < 6 and no clear aesthetic direction exists

## Core Principle: Visual Over Verbal

**The catalogue is a working webpage, not markdown descriptions.**

Users see actual styled components, real typography, live color palettes - not just words describing what things *would* look like.

## Workflow

### 1. Investigation

**Understand what exists:**

```bash
# Screenshot current state via Chrome MCP
mcp__claude-in-chrome__tabs_context_mcp
mcp__claude-in-chrome__navigate url="[current app URL]"
mcp__claude-in-chrome__computer action="screenshot"
```

**Analyze the current design:**
- Typography: What fonts, sizes, weights?
- Colors: What palette, what semantic meaning?
- Layout: Centered? Asymmetric? Grid-based?
- Motion: Any animations? What timing?
- Components: What patterns exist?

**Infer current DNA:**
```
DNA Axes:
- Layout: [centered|asymmetric|grid-breaking|full-bleed|bento|editorial]
- Color: [dark|light|monochrome|gradient|high-contrast|brand-tinted]
- Typography: [display-heavy|text-forward|minimal|expressive|editorial]
- Motion: [orchestrated|subtle|aggressive|none|scroll-triggered]
- Density: [spacious|compact|mixed|full-bleed]
- Background: [solid|gradient|textured|patterned|layered]
```

**Identify:**
- Strengths to preserve
- Weaknesses/opportunities
- Constraints (brand colors, accessibility, tech stack)

**Research via Gemini:**
```bash
gemini "Analyze this [product type] design. Current DNA: [inferred].
- What's working well?
- What patterns feel dated or generic?
- What distinctive directions could elevate this?
- 2025 trends for this product category
- Anti-convergence opportunities (avoid AI-default aesthetics)"
```

### 2. Build Visual Catalogue

**Create catalogue directory:**
```
.design-catalogue/
├── index.html              # Main viewer
├── styles/catalogue.css    # Viewer chrome styles
├── proposals/
│   ├── 01-[name]/
│   │   ├── preview.html
│   │   └── styles.css
│   ├── 02-[name]/
│   │   └── ...
│   └── ... (5-8 total)
└── assets/
```

**Generate 5-8 proposals** using DNA variation system.

**DNA Variation Rule:** No two proposals share >2 axes.

**Required diversity:**
- At least 1 bold/dramatic direction
- At least 1 refined/subtle direction
- At least 1 unexpected/wild card

**Each proposal preview includes:**
- Hero section in that style
- Sample card component
- Button states (default, hover, active)
- Typography scale (h1-h6, body, caption)
- Color palette swatches with hex codes
- DNA code badge

**Reference templates:**
- `references/viewer-template.html` - Main catalogue viewer
- `references/proposal-template.html` - Individual proposal page
- `references/catalogue-template.md` - Metadata structure

**Anti-convergence check:** Reference `aesthetic-system/references/banned-patterns.md`
- No Inter, Space Grotesk, Roboto as primary fonts
- No purple gradients on white
- No centered-only layouts for all proposals

### 3. Present & Serve

**Start local server:**
```bash
cd .design-catalogue && python -m http.server 8888 &
echo "Catalogue available at http://localhost:8888"
```

**Open in Chrome MCP:**
```bash
mcp__claude-in-chrome__navigate url="http://localhost:8888"
mcp__claude-in-chrome__computer action="screenshot"
```

**Present to user:**
```
Design Catalogue Ready

I've built 6 visual proposals exploring different directions for [project].
View the live catalogue: http://localhost:8888

Quick overview:
1. Midnight Editorial - [soul statement]
2. Swiss Brutalist - [soul statement]
3. Warm Workshop - [soul statement]
...

Browse the catalogue in your browser, then tell me which 2-3 resonate.
```

### 4. Collaborative Refinement

**First selection:**
```
AskUserQuestion:
"Which 2-3 directions interest you most?"
Options: [Proposal names with brief descriptions]
```

**Refinement dialogue:**
- "What specifically appeals about [selection]?"
- "Anything you'd change or combine?"
- "Should I generate hybrid proposals?"

**If refinement requested:**
- Generate 2-3 new proposals based on feedback
- Add to catalogue as new entries
- Update viewer to highlight refined options

### 5. Direction Selection

**Present finalists** with expanded detail:
- Full color palette (all semantic tokens)
- Complete typography scale with specimens
- Component transformation examples (before → after)
- Implementation priority list

**Final selection:**
```
AskUserQuestion:
"Which direction should we implement?"
Options: [Finalist names]
+ "Make more changes first"
```

### 6. Output

**Return to parent command with:**
```markdown
## Selected Direction: [Name]

**DNA:** [layout, color, typography, motion, density, background]

**Typography:**
- Headings: [Font family, weights]
- Body: [Font family, weights]
- Code/Mono: [Font family]

**Color Palette:**
- Background: [hex]
- Foreground: [hex]
- Primary: [hex]
- Secondary: [hex]
- Accent: [hex]
- Muted: [hex]

**Implementation Priorities:**
1. [First change - highest impact]
2. [Second change]
3. [Third change]

**Preserve:**
- [What to keep from current design]

**Transform:**
- [What changes dramatically]

**Anti-patterns to avoid:**
- [Specific things NOT to do]
```

**Cleanup:**
```bash
# Stop local server
pkill -f "python -m http.server 8888"
# Optionally remove catalogue (or keep for reference)
# rm -rf .design-catalogue
```

## Quick Reference

| Phase | Action |
|-------|--------|
| Investigation | Screenshot, analyze, infer DNA, research via Gemini |
| Catalogue | Build 5-8 visual proposals with DNA variety |
| Present | Serve locally, open in Chrome, describe options |
| Refine | User picks favorites, generate hybrids if needed |
| Select | Final choice with full spec |
| Output | Structured direction for implementation |

## Integration

**Invoked by:**
- `/design` command (directly)
- `/aesthetic` at Phase 0 (recommended)
- `/polish` when maturity < 6 (suggested)

**Outputs to:**
- `/aesthetic` - guides all subsequent phases
- `/polish` - constrains DNA for refinement loop
- Direct implementation - provides full spec

## References

- `references/viewer-template.html` - Catalogue viewer HTML
- `references/proposal-template.html` - Individual proposal HTML
- `references/catalogue-template.md` - Metadata structure
- `aesthetic-system/references/dna-codes.md` - DNA axis definitions
- `aesthetic-system/references/banned-patterns.md` - Anti-convergence rules
