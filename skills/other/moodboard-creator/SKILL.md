---
description: Create visual moodboards from collected inspiration with iterative refinement. Use after trend research or website analysis to synthesize design direction before implementation.
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
  - mcp__claude-in-chrome__computer
---

# Moodboard Creator

Create and refine visual moodboards that synthesize design inspiration into a cohesive direction.

## Purpose

Before jumping to code, create a moodboard that:
- Consolidates inspiration into clear direction
- Extracts colors, typography, and patterns
- Allows iterative refinement with user feedback
- Establishes design language before implementation

## Workflow

### Step 1: Gather Sources

Collect inspiration from:
- Trend research screenshots
- Analyzed websites
- User-provided URLs or images
- Dribbble/Behance shots

For each source, note:
- URL or source
- Key visual elements to extract
- Why it's relevant

### Step 2: Extract Elements

From collected sources, extract:

**Colors**
- Primary colors (1-2)
- Secondary/accent colors (1-2)
- Background colors
- Text colors
- Note hex codes

**Typography**
- Headline font style (name if identifiable)
- Body font style
- Weight and size observations
- Spacing/tracking notes

**UI Patterns**
- Navigation styles
- Card treatments
- Button designs
- Section layouts
- Decorative elements

**Mood/Atmosphere**
- Keywords describing the feel
- Emotional response
- Brand personality traits

### Step 3: Create Moodboard Document

Generate a structured moodboard:

```markdown
## Moodboard v1 - [Project Name]

### Inspiration Sources
| Source | Key Takeaway |
|--------|--------------|
| [URL/Name 1] | [What we're taking from it] |
| [URL/Name 2] | [What we're taking from it] |
| [URL/Name 3] | [What we're taking from it] |

### Color Direction
```
Primary:    #[hex] - [color name]
Secondary:  #[hex] - [color name]
Accent:     #[hex] - [color name]
Background: #[hex] - [color name]
Text:       #[hex] - [color name]
```

### Typography Direction
- **Headlines**: [Font/style] - [weight, size notes]
- **Body**: [Font/style] - [readability notes]
- **Accents**: [Any special type treatments]

### UI Patterns to Incorporate
1. **[Pattern Name]**: [Description of how to use it]
2. **[Pattern Name]**: [Description of how to use it]
3. **[Pattern Name]**: [Description of how to use it]

### Layout Approach
- Grid system: [e.g., 12-column, bento, asymmetric]
- Spacing philosophy: [tight, airy, mixed]
- Section structure: [full-width, contained, alternating]

### Mood Keywords
[Keyword 1] | [Keyword 2] | [Keyword 3] | [Keyword 4]

### Visual References
[Descriptions of key screenshots/references]

### What to Avoid
- [Anti-pattern from inspiration that doesn't fit]
- [Style that would clash]
```

### Step 4: User Review

Present moodboard to user and ask:
- Does this direction feel right?
- Any colors to adjust?
- Typography preferences?
- Patterns to add or remove?
- Keywords that don't fit?

### Step 5: Iterate

Based on feedback:
1. Update moodboard version number
2. Adjust elements per feedback
3. Add new inspirations if needed
4. Remove rejected elements
5. Present updated version

Continue until user approves.

### Step 6: Finalize

When approved, create final moodboard summary:

```markdown
## FINAL Moodboard - [Project Name]

### Approved Direction
[Summary of the design direction]

### Color Palette (Final)
| Role | Hex | Usage |
|------|-----|-------|
| Primary | #xxx | Buttons, links, accents |
| Secondary | #xxx | Hover states, icons |
| Background | #xxx | Page background |
| Surface | #xxx | Cards, modals |
| Text Primary | #xxx | Headings, body |
| Text Secondary | #xxx | Captions, muted |

### Typography (Final)
- Headlines: [Font Name] - [weight]
- Body: [Font Name] - [weight]
- Monospace: [Font Name] (if needed)

### Key Patterns
1. [Pattern with implementation notes]
2. [Pattern with implementation notes]

### Ready for Implementation
[Checkbox] Colors defined
[Checkbox] Fonts selected
[Checkbox] Layout approach set
[Checkbox] User approved
```

## Iteration Best Practices

- Keep each version documented
- Make focused changes (don't overhaul everything)
- Explain changes clearly
- Show before/after for major shifts
- Maximum 3-4 iterations (then synthesize feedback)

## Fallback Mode

If no visual sources available:
1. Ask user to describe desired mood/feel
2. Reference aesthetic categories from design-wizard
3. Suggest color palettes from color-curator fallbacks
4. Use typography pairings from typography-selector fallbacks
5. Create text-based moodboard from descriptions

## Output

Final moodboard should directly inform:
- Tailwind config colors
- Google Fonts selection
- Component styling decisions
- Layout structure
