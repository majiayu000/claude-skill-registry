---
name: slides-design
description: Create strategic HTML presentations with Chart.js, design tokens, and contextual decision system. Use for investor pitches, sales decks, product demos, QBRs, and conference talks. Features 15 deck strategies, 25 layouts, BM25 search, and Duarte Sparkline emotion arcs.
---

# Slides Design

Create persuasive HTML slide decks using design tokens, Chart.js, and a contextual decision system.

## Skill Activation (Required)

**Before creating slides, activate in order:**
1. `design-system` - Design tokens, color palettes, typography, spacing
2. `frontend-design` - Design thinking, aesthetics, visual asset generation
3. `ui-ux-pro-max` (if `frontend-design` is not available) - Premium UI patterns, component library

## When to Use

- Investor pitch decks (YC-style, Series A)
- Sales presentations and product demos
- Conference talks and webinars
- Internal QBRs and team all-hands
- Case study presentations

## Critical Requirements

**ALL slides MUST:**
1. Embed design tokens inline (for `file://` compatibility)
   ```bash
   node .claude/skills/design-system/scripts/embed-tokens.cjs --minimal
   ```
2. Use CSS variables exclusively: `var(--color-primary)`, `var(--slide-bg)`
3. Use Chart.js for data visualizations (not CSS-only bars)
4. Include navigation (keyboard arrows, click, progress bar)
5. Center-align content properly
6. Focus on conversion/persuasion (you're SELLING)

## Quick Start

### 1. Get Design Tokens
```bash
node .claude/skills/design-system/scripts/embed-tokens.cjs --minimal
```

### 2. Search Strategy + Emotion Arc
```bash
python .claude/skills/design-system/scripts/search-slides.py "[goal]" -d strategy
```

### 3. Contextual Search Per Slide
```bash
python .claude/skills/design-system/scripts/search-slides.py "[slide goal]" \
  --context --position [N] --total [TOTAL] --prev-emotion [PREV]
```

### 4. Generate HTML
Follow `references/html-template.md` for navigation and Chart.js patterns.

## Decision System

| CSV File | Purpose |
|----------|---------|
| `slide-strategies.csv` | 15 deck types + emotion arcs |
| `slide-layouts.csv` | 25 layouts + animations |
| `slide-layout-logic.csv` | Goal → Layout mapping |
| `slide-typography.csv` | Content → Typography scale |
| `slide-color-logic.csv` | Emotion → Color treatment |
| `slide-copy.csv` | 25 copywriting formulas |
| `slide-charts.csv` | 25 Chart.js configurations |

**Data location:** `.claude/skills/design-system/data/`

## References

| Topic | File |
|-------|------|
| HTML Template | `references/html-template.md` |
| Slide Strategies | `references/slide-strategies.md` |
| Layout Patterns | `references/layout-patterns.md` |
| Copywriting | `references/copywriting-formulas.md` |

## Premium Workflow (Duarte Sparkline)

Alternate emotions for engagement: "What Is" (frustration) ↔ "What Could Be" (hope)

Pattern breaks calculated at 1/3 and 2/3 positions for full-bleed emotional slides.

## Output

Save to: `assets/designs/slides/{slug}-{date}.html`

## Examples

```bash
/slides:create "10-slide seed funding pitch for ClaudeKit"
/slides:create "B2B sales deck with ROI focus"
/slides:create "5-slide product demo with features"
```

**Skill Dependencies:** frontend-design, ui-ux-pro-max, design-system, brand-guidelines
**Primary Agents:** ui-ux-designer, content-creator
