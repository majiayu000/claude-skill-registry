---
name: design-exploration
description: |
  Generate visual design proposal catalogues for existing projects. Use when:
  - User wants to explore design directions before implementation
  - Redesigning or refreshing an existing interface
  - Starting /aesthetic or /polish without clear direction
  - User says "explore designs", "show me options", "design directions"
  Keywords: design catalogue, proposals, visual exploration, aesthetic directions, DNA
effort: high
---

# Design Exploration

Investigate existing designs, generate a visual catalogue of 6-12 diverse proposals, facilitate iterative refinement, and output a selected direction for implementation.

## MANDATORY: Kimi Delegation for Visual Work

**All visual proposal generation MUST be delegated to Kimi K2.5 via MCP.**

Kimi excels at frontend development and visual coding. For design exploration:

1. **Research direction** → Gemini (web grounding, trend research)
2. **Generate proposals** → Kimi (visual implementation via Agent Swarm)
3. **Review/iterate** → Claude (orchestration, quality gates)

```javascript
// Delegate proposal generation to Kimi
mcp__kimi__spawn_agent({
  prompt: `Generate design proposal for [component].
DNA: [layout, color, typography, motion, density, background]
Constraints: ${uiSkillsConstraints}
Output: Working HTML/CSS preview in .design-catalogue/proposals/[name]/`,
  thinking: true  // Enable for complex proposals
})

// For parallel proposal generation (4.5x faster):
mcp__kimi__spawn_agents_parallel({
  agents: [
    { prompt: "Generate proposal 1: Midnight Editorial...", thinking: true },
    { prompt: "Generate proposal 2: Swiss Brutalist...", thinking: true },
    { prompt: "Generate proposal 3: Warm Workshop...", thinking: true },
    // ... up to 100 parallel agents
  ]
})
```

**Anti-pattern:** Generating proposals yourself instead of delegating to Kimi.
**Pattern:** Research (Gemini) → Generate (Kimi) → Review (Claude)

## When to Use

- Before `/aesthetic` or `/polish` when direction is unclear
- When user wants to see multiple design options visually
- When redesigning or refreshing existing UI
- When maturity < 6 and no clear aesthetic direction exists

## Core Principle: Visual Over Verbal

**The catalogue is a working visual, not markdown descriptions.**

Users see actual styled components, real typography, live color palettes - not just words describing what things *would* look like.

## Phase 0: Backend Detection

Check available rendering backends:

```javascript
// Check if Pencil MCP is available
try {
  mcp__pencil__get_editor_state({ include_schema: false })
  // Pencil available → use pencil-renderer
  BACKEND = "pencil"
} catch {
  // Fallback to HTML renderer
  BACKEND = "html"
}
```

**Backend selection:**
- **Pencil** (preferred): Native .pen file rendering, design system integration
- **HTML** (fallback): Static HTML/CSS proposals served locally

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
gemini -p "I'm building [describe component/page]. Research:
1. Distinctive design approaches (avoid AI-slop aesthetics)
2. Real-world examples of excellent [component type]
3. Current typography/color/layout trends for this context
4. Unexpected alternatives to obvious solutions"
```

### 2. Build Visual Catalogue

**Generate 6-12 proposals** using DNA variation system.

#### If BACKEND = "pencil":

Use `pencil-renderer` primitive:

```javascript
// For each proposal
// 1. Get style guide matching DNA mood
mcp__pencil__get_style_guide_tags()
mcp__pencil__get_style_guide({ tags: [mapped_tags] })

// 2. Render via pencil-renderer workflow
// See: pencil-renderer/SKILL.md
```

All proposals render to a single .pen document as separate frames.

#### If BACKEND = "html":

Create catalogue directory:
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
│   └── ... (6-12 total)
└── assets/
```

**DNA Variation Rule:** No two proposals share >2 axes.

**Required diversity:**
- At least 2 bold/dramatic directions
- At least 2 refined/subtle directions
- At least 1 unexpected/wild card
- At least 1 that preserves current strengths

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

#### If BACKEND = "pencil":

```javascript
// Screenshot each proposal frame
for (const frame of proposalFrames) {
  mcp__pencil__get_screenshot({ nodeId: frame.id })
}
```

Present in chat with screenshots.

#### If BACKEND = "html":

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

I've built [N] visual proposals exploring different directions for [project].

Quick overview:
1. Midnight Editorial - [soul statement]
2. Swiss Brutalist - [soul statement]
3. Warm Workshop - [soul statement]
...

[If Pencil] View the .pen file directly in your editor
[If HTML] Browse the catalogue: http://localhost:8888

Tell me which 2-3 resonate.
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

### 5.5. Expert Panel Review (MANDATORY)

**Before presenting any design to user, run expert panel review.**

See: `ui-skills/references/expert-panel-review.md`

1. Simulate 10 world-class advertorial experts (Ogilvy, Rams, Scher, Wiebe, Laja, Walter, Cialdini, Ive, Wroblewski, Millman)
2. Each expert scores 0-100 and provides specific improvement feedback
3. Calculate average score
4. **If average < 90:** Implement highest-impact feedback, iterate, re-review
5. **If average ≥ 90:** Proceed to handoff

```markdown
Expert Panel Review: [Design Name]

| Expert | Score | Critical Improvement |
|--------|-------|---------------------|
| Ogilvy | 88 | Headline needs stronger benefit |
| Rams | 92 | Clean execution |
| ...
**Average: 89.2** ❌ → Iterating...
```

**Do not return design until 90+ average achieved.**

### 6. Output & Handoff

**Return selected direction:**
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

**Handoff routing:**

| Backend | Handoff Target |
|---------|---------------|
| Pencil | `pencil-to-code` — exports .pen → React/Tailwind |
| HTML | `design-theme` — implements tokens in codebase |

```
AskUserQuestion:
"Ready to generate implementation code?"
Options:
- "Yes, generate React components" → invoke handoff
- "No, I'll implement manually" → return spec only
```

**Cleanup (HTML backend only):**
```bash
# Stop local server
pkill -f "python -m http.server 8888"
# Optionally remove catalogue
# rm -rf .design-catalogue
```

## Quick Reference

| Phase | Action |
|-------|--------|
| Backend Detection | Check Pencil MCP availability |
| Investigation | Screenshot, analyze, infer DNA, research via Gemini |
| Catalogue | Build 6-12 visual proposals with DNA variety |
| Present | Serve/screenshot, describe options |
| Refine | User picks favorites, generate hybrids if needed |
| Select | Final choice with full spec |
| Handoff | Route to pencil-to-code or design-theme |

## Integration

**Invoked by:**
- `/design` command (directly)
- `/aesthetic` at Phase 0 (recommended)
- `/polish` when maturity < 6 (suggested)

**Outputs to:**
- `pencil-to-code` — when Pencil backend, user wants code
- `design-theme` — when HTML backend, user wants implementation
- `/aesthetic` — guides all subsequent phases
- `/polish` — constrains DNA for refinement loop

## Related Skills

- `pencil-renderer` — Pencil MCP rendering primitive
- `pencil-to-code` — .pen → React/Tailwind export
- `aesthetic-system` — DNA codes, anti-convergence rules
- `design-tokens` — Token system patterns
- `design-theme` — Theme implementation

## References

- `references/viewer-template.html` - Catalogue viewer HTML
- `references/proposal-template.html` - Individual proposal HTML
- `references/catalogue-template.md` - Metadata structure
- `aesthetic-system/references/dna-codes.md` - DNA axis definitions
- `aesthetic-system/references/banned-patterns.md` - Anti-convergence rules
