# Presentation Spec

Create detailed slide-by-slide specification for a class presentation.

---

## Frontmatter

```yaml
context: main
allowed-tools: Read, Write, Edit, AskUserQuestion
```

---

## Prerequisites

- `lesson-plan-{topic}.md` must exist and pass Gate 1
- `master-presentation-spec.md` must exist
- Topic must be specified in invocation

---

## Instructions

You are creating a detailed specification for presentation slides. This document serves as the blueprint for implementation.

### Usage

```
/presentation-spec {topic}
```

### Step 1: Review Prerequisites

Read these files:
- `lesson-plan-{topic}.md` - Objectives and activities to support
- `master-presentation-spec.md` - Design constraints and patterns
- `research/research-{topic}.md` - Visualization patterns and content

Extract:
- Learning objectives to achieve
- Lesson sequence to follow
- Visualization patterns to implement
- Design constraints to follow

### Step 2: Map Objectives to Slides

Create a mapping showing how slides will support each objective:

| Objective | Supporting Slides | How It Supports |
|-----------|------------------|-----------------|
| 1. {obj} | Slides 3-5 | Introduces concept |
| 2. {obj} | Slides 6-8, 12 | Demonstrates with example |
| ... | ... | ... |

Every objective must have supporting slides.

### Step 3: Plan Slide Sequence

Determine the overall flow:

1. **Title slide**: Class number, topic, theme
2. **Agenda/Overview**: What we'll cover
3. **Hook**: Attention-grabbing opening
4. **Content slides**: Main instruction
5. **Activity slides**: Practice moments
6. **Summary**: Key takeaways
7. **Appendix**: Reference material

### Step 4: Specify Each Slide

For each slide, document:

- **Number and title**
- **Slide type** (from master spec)
- **Purpose** (what it accomplishes)
- **Content**: Exact text, bullets, or visual
- **Speaker notes**: What instructor says
- **Timing**: How long to spend
- **Interaction**: Click-through, questions, etc.

### Step 5: Specify Visualizations

For any slide with D3 or complex visuals:

- **Visualization name**
- **Type**: Chart, diagram, animation
- **Data structure**: What data it uses
- **Interaction model**: Click, hover, scroll
- **Animation sequence**: What animates when
- **Technical notes**: Implementation hints

### Step 6: Plan Interactions

Mark points where students engage:
- Discussion questions
- Poll/survey moments
- Think-pair-share
- Practice exercises
- Reflection pauses

### Step 7: Write Presentation Spec

Create `src/pages/class-{n}-{topic}/presentation-spec-{topic}.md`:

```markdown
# Presentation Spec: {Topic Title}

Class: {N}
Duration: {minutes} minutes
Theme: {Theme name} ({color})
Total Slides: {count}

## Objective Coverage Matrix

| # | Objective | Supporting Slides |
|---|-----------|-------------------|
| 1 | {objective} | {slide numbers} |
| 2 | {objective} | {slide numbers} |
| 3 | {objective} | {slide numbers} |

## Slide Sequence Overview

| # | Title | Type | Time | Purpose |
|---|-------|------|------|---------|
| 1 | {title} | title | 1 min | Opening |
| 2 | {title} | content | 2 min | Agenda |
| ... | ... | ... | ... | ... |

## Detailed Slide Specifications

### Slide 1: {Title}

**Type**: slide-title
**Time**: 1 minute
**Purpose**: Opening, establish topic

**Content**:
```
Class {N}
{Topic Title}
{Subtitle if any}
```

**Speaker Notes**:
{What instructor should say}

**Technical Notes**:
- Theme color: {color}
- Background: {description}

---

### Slide 2: {Title}

**Type**: slide-content
**Time**: 2 minutes
**Purpose**: Set expectations

**Content**:
```
Today We'll Cover:
• {bullet 1}
• {bullet 2}
• {bullet 3}
```

**Speaker Notes**:
{notes}

---

### Slide {N}: {Visual Title}

**Type**: slide-visual
**Time**: 5 minutes
**Purpose**: {what it achieves}

**Visualization Spec**:

**Name**: {visualization-name}
**Type**: {D3 chart / CSS animation / etc.}

**Data Structure**:
```json
{
  "items": [
    { "label": "...", "value": ... }
  ]
}
```

**Visual Description**:
{Detailed description of what it looks like}

**Animation Sequence**:
1. {Initial state}
2. {On first click: what animates}
3. {On second click: what animates}
4. {Final state}

**Interaction**:
- Click: {what happens}
- Hover: {what happens}

**Technical Requirements**:
- Responsive: Must use viewBox
- Font sizes: 1.25rem minimum for labels
- Colors: Use --theme-color for primary

**Speaker Notes**:
{What to say while visualization plays}

---

### Slide {N}: Activity

**Type**: slide-content
**Time**: 10 minutes
**Purpose**: Student practice

**Content**:
```
Activity: {Name}

Instructions:
1. {step 1}
2. {step 2}
3. {step 3}

Time: {X} minutes
```

**Activity Details**:
- Format: {individual/pairs/groups}
- Materials: {what students need}
- Expected output: {what they produce}

**Speaker Notes**:
{How to facilitate}

---

{Continue for all slides}

## Interaction Points

| Slide | Type | Prompt | Expected Response |
|-------|------|--------|-------------------|
| 5 | Question | "{question}" | {expected answers} |
| 8 | Think-Pair-Share | "{prompt}" | {discussion points} |
| 12 | Practice | "{task}" | {success criteria} |

## Visualization Inventory

| Slide | Name | Type | Complexity |
|-------|------|------|------------|
| 6 | market-funnel | D3 animated | Medium |
| 10 | comparison-chart | D3 bar | Simple |

## Time Budget

| Section | Slides | Time | Cumulative |
|---------|--------|------|------------|
| Opening | 1-2 | 3 min | 3 min |
| Hook | 3 | 5 min | 8 min |
| Core 1 | 4-8 | 20 min | 28 min |
| Activity 1 | 9 | 10 min | 38 min |
| Core 2 | 10-14 | 20 min | 58 min |
| Activity 2 | 15 | 10 min | 68 min |
| Summary | 16-17 | 7 min | 75 min |

## Design Notes

- Theme color: {hex}
- Key visual motif: {description}
- Consistent elements: {what repeats}

## Appendix Slides (if any)

| # | Title | Purpose |
|---|-------|---------|
| A1 | {title} | {reference material} |

---

*Gate 2 Checklist*:
- [ ] Every objective has supporting slides
- [ ] Complex concepts have visualization specs
- [ ] Interaction points are marked
- [ ] Slide flow supports learning progression
- [ ] Times sum to class duration
- [ ] Sources cited for content
```

---

## Output Specification

This skill produces:

- **Primary Output**: `src/pages/class-{n}-{topic}/presentation-spec-{topic}.md`
- **Format**: Markdown with detailed slide specifications
- **Gate**: Must pass Gate 2 before proceeding to presentation-build

---

## Gate 2 Checklist

After creating the spec, verify:

- [ ] Every learning objective has at least one supporting slide
- [ ] Complex concepts have D3/visualization specs
- [ ] Interaction points (questions, activities) are marked
- [ ] Slide flow supports logical learning progression
- [ ] Time estimates per slide sum to class duration
- [ ] All content sources are cited
- [ ] Visualization specs include font size requirements

---

## Examples

### Example: Visualization Spec

```markdown
### Slide 6: Market Sizing Funnel

**Type**: slide-visual
**Time**: 5 minutes
**Purpose**: Visualize TAM → SAM → SOM progression

**Visualization Spec**:

**Name**: tam-sam-som-funnel
**Type**: D3 animated funnel

**Data Structure**:
```json
{
  "levels": [
    { "name": "TAM", "value": 50000000000, "label": "Total Addressable Market" },
    { "name": "SAM", "value": 5000000000, "label": "Serviceable Available Market" },
    { "name": "SOM", "value": 500000000, "label": "Serviceable Obtainable Market" }
  ]
}
```

**Visual Description**:
Three nested trapezoids, widest at top (TAM), narrowing to SOM.
Each level has label on left, dollar value on right.
Background gets progressively darker/more saturated toward SOM.

**Animation Sequence**:
1. Initial: Empty container
2. Click 1: TAM trapezoid fades in (800ms ease-out)
3. Click 2: SAM slides up from bottom, nested inside TAM
4. Click 3: SOM slides up, nested inside SAM
5. Final: All three visible with values

**Interaction**:
- Hover on level: Shows full description tooltip
- Click level: Highlights and shows calculation

**Technical Requirements**:
- viewBox="0 0 600 400"
- Labels: 1.25rem, Inter font
- Values: 1.5rem, bold
- Colors: theme-1-customer with 80%, 60%, 40% opacity
```
