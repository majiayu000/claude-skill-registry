---
name: tufte-slide-design
description: This skill applies Edward Tufte's data visualization principles from "The Visual Display of Quantitative Information" to create high-impact slides. Use when designing presentations, creating charts/graphs, reviewing slides for clarity, or transforming data into visual displays. Triggers on phrases like "make a slide", "create presentation", "design chart", "visualize data", "review my slides", or "make this more impactful".
---

# Tufte Slide Design

Apply Edward Tufte's principles from "The Visual Display of Quantitative Information" to create presentations that communicate complex ideas with clarity, precision, and efficiency.

## Core Philosophy

Tufte's central insight: **"Clutter and confusion are failures of design, not attributes of information."**

Information overload is rarely the problem—poor information design is. The goal is graphical excellence: the well-designed presentation of interesting data combining substance, statistics, and design.

## The Five Laws of Data-Ink

When designing any slide with data:

1. **Above all else, show the data** - Data is the primary focus
2. **Maximize the data-ink ratio** - Every pixel should convey information
3. **Erase non-data-ink** - Remove decorations that don't inform
4. **Erase redundant data-ink** - Eliminate duplicate information carriers
5. **Revise and edit** - Continuously refine toward simplicity

### Data-Ink Ratio Formula

```
Data-Ink Ratio = Ink presenting data / Total ink used
```

Target: As close to 1.0 as possible. Each element should earn its place.

## Slide Design Workflow

### Step 1: Identify the Data Story

Before creating any slide, answer:
- What is the ONE key insight this slide must communicate?
- What data supports this insight?
- What would be lost if this slide were removed?

### Step 2: Apply the Chartjunk Elimination Checklist

Remove or minimize:

| Chartjunk Element | Action |
|-------------------|--------|
| 3D effects | Flatten to 2D |
| Gradient fills | Use solid colors |
| Heavy gridlines | Lighten or remove |
| Decorative borders | Remove entirely |
| Background images | Remove unless data |
| Drop shadows | Remove |
| Unnecessary legends | Label directly on chart |
| Excessive tick marks | Reduce to minimum |
| Moiré patterns | Use solid fills |

### Step 3: Check Graphical Integrity

Tufte's Six Principles of Graphical Integrity:

1. **Proportional representation** - Visual size must match numerical quantity
2. **Clear labeling** - Label data directly on the graphic
3. **Show data variation, not design variation** - Design should not distort
4. **Use proper monetary units** - Deflate/standardize when showing money over time
5. **Match dimensions** - Don't use 2D/3D to represent 1D data
6. **Preserve context** - Never quote data out of context

### Step 4: Calculate the Lie Factor

```
Lie Factor = Size of effect in graphic / Size of effect in data
```

- Lie Factor = 1.0: Truthful
- Lie Factor > 1.0: Overstates the effect
- Lie Factor < 1.0: Understates the effect

**Example violation**: A 53% numerical change shown as 783% visual change = Lie Factor of 14.8

### Step 5: Apply Advanced Techniques

#### Small Multiples
Use for comparing related data:
- Same graphic structure repeated with different data slices
- Enables visual comparison within eye span
- "Move to the heart of visual reasoning—to see, distinguish, choose"

#### Sparklines
Word-sized graphics for inline data display:
- High resolution in small space
- Embed in tables or text
- "Datawords: data-intense, design-simple, word-sized graphics"

#### Direct Labeling
Instead of legends, label data directly:
- Reduces eye movement
- Eliminates legend decoding
- Places information where attention focuses

## Slide Types and Tufte Approaches

### Data-Heavy Slides

1. Strip unnecessary gridlines
2. Use range-frame axes (only show data range)
3. Consider small multiples for comparisons
4. Direct label instead of legends
5. Horizontal orientation where possible

### Text-Heavy Slides (Anti-Pattern)

Tufte's critique of bullet points ("The Cognitive Style of PowerPoint"):
- Bullet lists fragment thought
- Hierarchical bullets obscure relationships
- Low information density

**Alternative approaches:**
- Use sentence-case prose for complex ideas
- Provide detailed handouts instead
- Show data tables with full context
- Use visual diagrams showing relationships

### Title Slides

Apply same principles:
- Remove decorative elements
- Use typography for hierarchy, not ornament
- Every word should contribute meaning

## Quick Reference: Before/After Patterns

### Bar Charts
**Before**: 3D bars, gradient fills, heavy gridlines, legend below
**After**: 2D bars, solid colors, no gridlines, direct labels

### Line Charts
**Before**: Multiple colors, thick lines, point markers, legend
**After**: Direct labels on lines, minimal markers, reduced palette

### Pie Charts
**Tufte's view**: Generally avoid. If required:
- Never use 3D
- Limit to 3-4 slices maximum
- Consider bar chart instead

### Tables
**Before**: Heavy borders, alternating row colors, centered text
**After**: Minimal rules, left-aligned text, whitespace for separation

## Resources

For detailed principles and examples, reference:
- `references/tufte-principles.md` - Complete principle documentation with examples
- `references/slide-checklist.md` - Quick checklist for slide review

## Anti-Patterns to Avoid

1. **PowerPoint defaults** - Override all default templates and effects
2. **Chart templates** - Design from data, not from template
3. **Decoration for engagement** - Data is engaging when well-presented
4. **Hiding complexity** - Show the complexity, design it well
5. **Animation for emphasis** - Use visual hierarchy instead
