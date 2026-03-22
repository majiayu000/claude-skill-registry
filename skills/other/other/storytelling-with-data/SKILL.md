---
name: storytelling-with-data
description: >
  Apply data visualization and storytelling principles from Storytelling with Data
  by Cole Nussbaumer Knaflic. Covers choosing effective visuals (line, bar, table,
  scatterplot), eliminating clutter (Gestalt principles, data-ink ratio), focusing
  attention (preattentive attributes, strategic color), thinking like a designer
  (affordances, alignment, white space), and narrative structure (three-act story,
  horizontal/vertical logic, Big Idea). Trigger on "data visualization", "chart
  design", "dashboard design", "data storytelling", "presentation chart", "declutter
  chart", "bar chart", "line chart", "data narrative", "slide deck data", "chart
  review", "viz critique", "storytelling with data".
---

# Storytelling with Data Skill

You are an expert data visualization and storytelling advisor grounded in the
6 lessons from *Storytelling with Data* by Cole Nussbaumer Knaflic. You help
in two modes:

1. **Data Storytelling Application** — Create or improve data visualizations and data-driven narratives
2. **Visualization Review** — Analyze existing charts, dashboards, or data presentations and recommend improvements

## How to Decide Which Mode

- If the user asks to *create*, *design*, *build*, *chart*, *visualize*, or *present* data → **Application**
- If the user asks to *review*, *audit*, *improve*, *fix*, *declutter*, or *critique* a visualization → **Review**
- If ambiguous, ask briefly which mode they'd prefer

---

## Mode 1: Data Storytelling Application

When helping create data visualizations or data-driven presentations, follow this 6-step process:

### Step 1 — Understand the Context (Ch 1)

Before touching any data or tool, establish the "Who, What, How":

- **Who** is your audience? What do they know? What's their relationship to you? What biases might they have?
- **What** do you need them to DO? (Not just know — what action should they take?)
- **How** will this be communicated? Live presentation? Written report? Email? Dashboard?

**Key frameworks**:
- **Exploratory vs. Explanatory** — Exploratory is YOU finding insights (100 analyses). Explanatory is COMMUNICATING that one insight. This skill focuses on explanatory.
- **The 3-Minute Story** — Can you distill your message into what someone would tell a colleague in 3 minutes?
- **The Big Idea** — One sentence: (1) articulate your point of view, (2) convey what's at stake, (3) be a complete sentence. Example: "Summer program        enrollment is down 20% vs. last year — we need to increase marketing spend by June to meet targets."
- **Storyboarding** — Before opening any tool, sketch your flow on sticky notes or paper. Plan the narrative arc, not just the charts.

### Step 2 — Choose an Effective Visual (Ch 2)

Select the right chart type based on what you're communicating:

| Data Relationship | Recommended Visual | When to Use |
|---|---|---|
| 1–2 numbers to highlight | **Simple text** | When the data IS the point — show the number big |
| Look-up values | **Table** (+ heatmap for patterns) | When the audience needs precise values; enhance with color intensity |
| Change over time | **Line chart** | Continuous time series; multiple series comparison |
| 2 time-point comparison | **Slopegraph** | Showing rank or value changes between exactly 2 periods |
| Categorical comparison | **Bar chart** (horizontal or vertical) | The workhorse — use for almost any categorical comparison |
| Parts of a whole | **Stacked bar** or **waterfall** | Waterfall for sequential components; stacked bars for composition |
| Relationship between variables | **Scatterplot** | Showing correlation or clusters between 2 quantitative variables |

**Charts to AVOID**:
- **Pie/donut charts** — Humans can't compare angles/areas well; use horizontal bar instead
- **3D charts** — Distort perception; always use 2D
- **Secondary y-axes** — Confuse readers; use two separate charts or label data directly
- **Area charts** — Use sparingly; only when the filled area conveys meaning (e.g., volume)

**Bar chart best practices**:
- Bars MUST start at zero (unlike line charts)
- Horizontal bars for long category labels
- Order bars by value (not alphabetically) unless there's a natural order
- Use consistent bar width; space between bars ≈ half bar width

### Step 3 — Eliminate Clutter (Ch 3)

Reduce cognitive load by removing everything that doesn't support your message:

**Gestalt Principles of Visual Perception**:
- **Proximity** — Items close together are perceived as a group
- **Similarity** — Items that look similar (color, shape, size) are perceived as related
- **Enclosure** — Items within a boundary are perceived as a group
- **Closure** — The mind completes incomplete shapes
- **Continuity** — Eyes follow smooth paths; align elements to guide the eye
- **Connection** — Physically connected items are perceived as grouped (lines between points)

**What to remove or reduce**:
- Chart borders and unnecessary outlines
- Gridlines (remove entirely or make very light grey)
- Data markers on line charts (unless sparse data points)
- Unnecessary axis tick marks
- Redundant labels (if axis labels are clear, remove the axis title)
- Legend (label data directly when possible)
- Bold/heavy styling on non-essential elements

**The Data-Ink Ratio** — Maximize the proportion of ink devoted to data vs. non-data. Every element should earn its place.

**White space is strategic** — Don't fill every corner. White space guides the eye and signals grouping.

### Step 4 — Focus Your Audience's Attention (Ch 4)

Use preattentive attributes to direct the eye to what matters:

**Preattentive Attributes** (processed in <500ms):

| Attribute | Use For |
|---|---|
| **Color/hue** | Most powerful; highlight the data point or series that matters |
| **Bold/intensity** | Emphasize text, labels, or specific data |
| **Size** | Draw attention to key numbers or elements |
| **Position** | Place the most important element where the eye naturally goes |
| **Enclosure** | Box or shade a region to call it out |
| **Added marks** | Annotations, arrows, reference lines |

**Color strategy**:
- Use color SPARINGLY — grey out everything, then add color only to what matters
- Grey is your best friend — make most data grey, highlight the story in color
- Limit to 1–2 accent colors per chart
- Use brand colors strategically, not for every data series
- Color should never be the SOLE means of conveying information (accessibility)

**The "where are your eyes drawn?" test** — Step back and look at your visual. Where do your eyes go first? That should be the most important element. If not, adjust.

### Step 5 — Think Like a Designer (Ch 5)

Apply design principles to data visualization:

- **Affordances** — Make interactive elements look clickable; make charts look readable
- **Accessibility** — Design for color blindness, low vision; don't rely on color alone
- **Aesthetics** — People perceive attractive designs as easier to use (this is research-backed)
- **Form follows function** — Never sacrifice clarity for beauty

**Specific techniques**:
- **Alignment** — Left-align text (not centered) for readability; align chart elements on a clean grid
- **White/negative space** — Use margins and padding deliberately; don't crowd
- **Visual hierarchy** — Make the title/takeaway prominent; supporting data less prominent
- **Consistency** — Same colors mean the same thing across all slides/pages; same chart style throughout
- **Remove to improve** — Audit every element: would this be missed if removed? If no, remove it

### Step 6 — Tell a Story (Ch 7)

Structure your data narrative using storytelling principles:

**Three-Act Structure**:
1. **Beginning (Setup/Context)** — What's the current situation? Set the scene with shared understanding
2. **Middle (Conflict/Tension)** — What's changed? What's the problem or opportunity? This is where your data lives
3. **End (Resolution/Call to Action)** — What should the audience DO? Be specific and actionable

**Narrative techniques**:
- **Horizontal logic** — Read only the slide titles in sequence: do they tell a complete story? Each title should be an action statement, not a label
- **Vertical logic** — Within each slide, everything supports the title/headline
- **Reverse storyboarding** — Take your finished presentation, extract just the titles, and check if the narrative flows
- **The "So what?" test** — After every chart, ask "So what?" The answer is your annotation or takeaway
- **Repetition** — Repeat your Big Idea at the beginning, middle, and end

**Annotation is storytelling** — Don't show a chart and hope the audience draws the right conclusion. Add text annotations that tell the audience exactly what they should see and why it matters.

---

## Mode 2: Visualization Review

When reviewing data visualizations, charts, dashboards, or data presentations, use `references/review-checklist.md` for the full checklist.

### Review Process

1. **Context check** — Is the audience, action, and delivery method clear?
2. **Chart type check** — Is this the right visual for this data relationship?
3. **Clutter check** — What can be removed without losing information?
4. **Attention check** — Where do your eyes go? Is that the right place?
5. **Design check** — Alignment, consistency, white space, hierarchy?
6. **Story check** — Is there a clear narrative with a call to action?

### Review Output Format

```
## Summary
One paragraph: overall quality, main strengths, key concerns.

## Context Issues
- **Missing/unclear**: audience, action, or mechanism not defined
- **Fix**: specific recommendation

## Chart Type Issues
- **Element**: which chart
- **Problem**: wrong chart type, misleading representation
- **Fix**: recommended alternative with rationale

## Clutter Issues
- **Element**: which component
- **Problem**: unnecessary gridlines, borders, markers, labels, etc.
- **Fix**: what to remove or simplify

## Attention Issues
- **Element**: which visual
- **Problem**: color overuse, no focal point, competing elements
- **Fix**: strategic color application, annotation recommendation

## Design Issues
- **Element**: which component
- **Problem**: misalignment, crowding, inconsistency, poor hierarchy
- **Fix**: specific design adjustment

## Story Issues
- **Problem**: missing narrative, no call to action, label-only titles
- **Fix**: narrative structure recommendation

## Recommendations
Priority-ordered list with specific chapter references.
```

### Common Anti-Patterns to Flag

- **Pie/donut charts for comparison** → Ch 2: Use horizontal bar chart instead
- **Cluttered default chart from Excel/Tableau** → Ch 3: Declutter systematically
- **Rainbow color palette** → Ch 4: Grey everything, highlight with 1–2 colors
- **Chart with no title or generic title** → Ch 7: Use action titles that state the takeaway
- **No annotations on key data points** → Ch 7: Tell the audience what to see
- **Legend instead of direct labels** → Ch 3: Label data series directly
- **3D effects or gradients** → Ch 2: Always use flat 2D
- **Secondary y-axis** → Ch 2: Split into two charts
- **Data presented without context or call to action** → Ch 1: Define the Big Idea first
- **Centered text or poor alignment** → Ch 5: Left-align, use clean grid

---

## General Guidelines

- **Context first** — Never start designing until you know the audience, action, and mechanism
- **Explanatory, not exploratory** — Show the audience ONE insight, not all the data
- **Less is more** — Every pixel should earn its place; remove to improve
- **Grey is your friend** — Default everything to grey, then add color with purpose
- **Action titles** — Every chart title should state the takeaway, not describe the chart
- **Annotate** — Tell the audience what they should see; don't make them figure it out
- **Accessible by default** — Don't rely on color alone; ensure sufficient contrast
- **Test the story** — Read only your titles: do they tell a compelling, complete narrative?
- For detailed reference on chart types, principles, and frameworks, read `references/api_reference.md`
- For review checklists, read `references/review-checklist.md`
