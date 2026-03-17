# Master Spec

Establish the design system documentation for all course presentations.

---

## Frontmatter

```yaml
context: main
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
```

---

## Prerequisites

- `course-plan.md` must exist
- Institution config should be defined
- Understanding of delivery context (classroom size, Zoom streaming)

---

## Instructions

You are creating the master presentation specification - the design system that governs all presentations in the course. This document ensures visual consistency and readability across all materials.

### Step 1: Review Context

Read these files to understand requirements:
- `course-plan.md` - Visualization guidelines, principles
- `src/config/institution.ts` - Brand colors
- `src/config/course.ts` - Theme definitions
- `.claude/rpiv-config.json` - Validation rules

### Step 2: Define Color Palette

Document the complete color system:

1. **Institution Colors**: Primary and accent from brand
2. **Theme Colors**: One per framework theme (if applicable)
3. **Semantic Colors**: Success, warning, error, info
4. **Neutral Colors**: Background, text, borders
5. **CSS Variables**: How to reference colors

### Step 3: Define Typography

Establish font system:

1. **Font Families**: Headings, body, code
2. **Font Loading**: Google Fonts or self-hosted
3. **Type Scale**: All sizes from 1rem to 3rem
4. **Minimum Sizes**: CRITICAL - classroom readability requirements
5. **Line Heights**: For different contexts

**CRITICAL Requirements**:
- Titles: minimum 2.5rem (40px)
- Body: minimum 1.5rem (24px)
- Labels: minimum 1.25rem (20px)
- Absolute minimum: 1rem (16px)

### Step 4: Define Layout System

Document slide types and their layouts:

| Slide Type | Class | Purpose |
|------------|-------|---------|
| slide-title | Opening slide | Course/section title |
| slide-statement | Key message | Single powerful statement |
| slide-content | Bullet points | Lists, key points |
| slide-visual | Visualizations | D3 charts, diagrams |
| slide-quote | Attributed quote | Expert quotes |
| slide-two-part | Two sections | Definition + explanation |
| slide-comparison | Two columns | Compare/contrast |

### Step 5: Define Component Guidelines

For each UI component:
- Progress bar
- TOC overlay
- Appendix navigation
- Keyboard hints
- Slide transitions
- D3 visualization containers

### Step 6: Define D3 Visualization Standards

Critical for consistency:

1. **Responsive Pattern**:
   - Use viewBox, not fixed dimensions
   - Calculate positions as proportions
   - Scale with container

2. **Font Sizes**:
   - Axis labels: 1.25rem minimum
   - Data labels: 1.25rem minimum
   - Legends: 1.25rem minimum

3. **Animation Standards**:
   - Default duration: 800ms
   - Easing: d3.easeCubicOut
   - Stagger delay: 200ms

4. **Color Usage**:
   - Use theme colors
   - Maintain contrast ratios

### Step 7: Define Keyboard Navigation

Document standard shortcuts:
- Arrow keys: Navigate slides
- T: Toggle TOC
- A: Toggle Appendix
- S: Toggle Syllabus
- F: Toggle fullscreen
- 0-9: Jump to slide

### Step 8: Write Master Spec

Create `master-presentation-spec.md` with comprehensive documentation.

---

## Output Specification

This skill produces:

- **Primary Output**: `master-presentation-spec.md`
- **Format**: Markdown with CSS examples and code snippets
- **Dependencies**: Required before any presentation-build

---

## Quality Criteria

A good master spec:
- Has complete color palette with CSS variables
- Documents all minimum font sizes explicitly
- Includes code examples for every pattern
- Shows responsive D3 template
- Documents all keyboard shortcuts
- Provides checklist for code review

---

## Examples

### Example: Color Palette Section

```markdown
## Color Palette

### Institution Colors

| Name | Hex | CSS Variable | Usage |
|------|-----|--------------|-------|
| Primary Blue | #356093 | `--ncssm-blue` | Headers, links |
| Accent Gold | #d4a028 | `--ncssm-gold` | Highlights |

### Theme Colors (DE Framework)

| Theme | Color | CSS Variable |
|-------|-------|--------------|
| 1. Customer | #356093 | `--theme-1-customer` |
| 2. Value | #7c3aed | `--theme-2-value` |
| 3. Acquire | #059669 | `--theme-3-acquire` |
| 4. Money | #d4a028 | `--theme-4-money` |
| 5. Build | #dc2626 | `--theme-5-build` |
| 6. Scale | #0891b2 | `--theme-6-scale` |

### CSS Variables

\`\`\`css
:root {
  /* Institution */
  --ncssm-blue: #356093;
  --ncssm-gold: #d4a028;

  /* Current theme (set per presentation) */
  --theme-color: var(--theme-1-customer);

  /* Semantic */
  --color-success: #059669;
  --color-warning: #d97706;
  --color-error: #dc2626;
}
\`\`\`
```

### Example: Typography Section

```markdown
## Typography

### Font Families

\`\`\`css
:root {
  --font-heading: 'Inter', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-code: 'JetBrains Mono', monospace;
}
\`\`\`

### Type Scale (CRITICAL)

| Level | Size | Usage | Minimum |
|-------|------|-------|---------|
| Display | 3rem | Hero titles | 2.5rem |
| H1 | 2.5rem | Slide titles | 2.5rem |
| H2 | 2rem | Section headers | 1.5rem |
| Body | 1.5rem | Main content | 1.5rem |
| Label | 1.25rem | Charts, captions | 1.25rem |
| Small | 1rem | Metadata only | 1rem |

### Code Review Rules

\`\`\`javascript
// REJECT - Too small
.attr('font-size', '12px')
.style('font-size', '0.8rem')

// ACCEPT
.attr('font-size', '1.25rem')
.style('font-size', '1.5rem')
\`\`\`
```
