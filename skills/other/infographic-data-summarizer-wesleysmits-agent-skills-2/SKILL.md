---
name: creating-infographic-data-summaries
description: Converts data, research, and articles into infographic-ready summaries with visual hierarchy and chart suggestions. Use when the user asks about infographics, data visualization, visual summaries, chart types, or statistics presentation.
---

# Infographic Data Summarizer

## When to use this skill

- User asks to create infographic content
- User needs data visualization summaries
- User wants statistics formatted visually
- User mentions chart or graph selection
- User needs research distilled for visuals

## Workflow

- [ ] Extract key data points
- [ ] Identify main insight
- [ ] Structure visual hierarchy
- [ ] Suggest chart types
- [ ] Write supporting copy
- [ ] Create design brief

## Instructions

### Step 1: Data Source Analysis

**Data source types:**

| Source          | Extraction Approach                   |
| --------------- | ------------------------------------- |
| Research report | Key findings, statistics, conclusions |
| Survey results  | Top responses, percentages, trends    |
| Article/blog    | Statistics cited, main claims         |
| Dataset (CSV)   | Summarize, find outliers, trends      |
| Case study      | Before/after metrics, results         |
| Industry report | Market size, growth, forecasts        |

**Data extraction template:**

```markdown
## Data Extraction: [Source Title]

**Source:** [URL or document name]
**Date published:** [Date]
**Credibility:** [High/Medium/Low]

### Raw Data Points

| Statistic | Value    | Context            |
| --------- | -------- | ------------------ |
| [Metric]  | [Number] | [What it measures] |
| [Metric]  | [Number] | [What it measures] |
| [Metric]  | [Number] | [What it measures] |

### Key Findings

1. [Finding with specific number]
2. [Finding with specific number]
3. [Finding with specific number]

### Quotable Stat

"[Most compelling statistic in sentence form]"
```

### Step 2: Data Prioritization

**Statistic selection criteria:**

| Criteria                       | Priority |
| ------------------------------ | -------- |
| Surprising or counterintuitive | High     |
| Large percentage or growth     | High     |
| Directly relevant to audience  | High     |
| Comparison/contrast            | Medium   |
| Supporting detail              | Low      |
| Common knowledge               | Skip     |

**Priority matrix:**

```markdown
## Data Priority

### Hero Stat (1)

[The single most compelling/shareable statistic]

### Primary Stats (2-3)

1. [Supporting major insight]
2. [Supporting major insight]
3. [Supporting major insight]

### Secondary Stats (3-5)

1. [Adds context]
2. [Adds context]
3. [Adds context]

### Discard

- [Not compelling enough]
- [Too complex to visualize]
```

### Step 3: Visual Hierarchy Structure

**Infographic anatomy:**

```markdown
## Infographic Structure

### Header Section

- **Title:** [Attention-grabbing headline]
- **Subtitle:** [Context or scope]
- **Source logo:** [If featuring research partner]

### Hero Section

- **Big number:** [Hero statistic]
- **Supporting text:** [1-sentence context]
- **Icon/illustration:** [Visual representation]

### Body Sections (3-5)

#### Section 1: [Theme]

- **Subhead:** [Section title]
- **Stat:** [Number or percentage]
- **Visual:** [Chart type or icon]
- **Caption:** [Brief explanation]

#### Section 2: [Theme]

[Repeat format]

#### Section 3: [Theme]

[Repeat format]

### Footer Section

- **Call-to-action:** [What to do next]
- **Source citation:** [Where data came from]
- **Branding:** [Logo, URL, social handles]
```

### Step 4: Chart Type Selection

**Chart selection guide:**

| Data Type        | Best Chart     | When to Use                   |
| ---------------- | -------------- | ----------------------------- |
| Parts of whole   | Pie/donut      | Max 5 segments, percentages   |
| Comparison       | Bar chart      | Comparing categories          |
| Ranking          | Horizontal bar | Ordered list, top 10          |
| Change over time | Line chart     | Trends, time series           |
| Relationship     | Scatter plot   | Correlation between variables |
| Distribution     | Histogram      | Frequency, ranges             |
| Flow/process     | Flowchart      | Steps, decisions              |
| Geographic       | Map            | Location-based data           |
| Proportion       | Icon array     | X out of Y representation     |
| Progress         | Progress bar   | Completion, goals             |

**Chart alternatives:**

| Instead of            | Consider             | Why                      |
| --------------------- | -------------------- | ------------------------ |
| Pie chart (6+ slices) | Horizontal bar       | Easier to compare        |
| 3D charts             | 2D flat              | More accurate perception |
| Dual-axis line        | Two separate charts  | Less confusing           |
| Dense data table      | Highlighted key rows | Scannable                |

**Visual metaphors:**

| Concept    | Visual Approach              |
| ---------- | ---------------------------- |
| Growth     | Upward arrows, stacked bars  |
| Speed      | Speedometer, racing imagery  |
| Money      | Coins, bills, dollar signs   |
| Time       | Clocks, calendars, timelines |
| People     | Icon figures, silhouettes    |
| Comparison | Side-by-side, vs. graphics   |

### Step 5: Copy Elements

**Headline formulas:**

| Formula                             | Example                                   |
| ----------------------------------- | ----------------------------------------- |
| [Number] + [Noun] + [Action/Result] | "5 Habits That Double Productivity"       |
| The State of [Topic] in [Year]      | "The State of Remote Work in 2026"        |
| [Question]?                         | "Where Does Your Time Really Go?"         |
| [X] vs [Y]: [Comparison]            | "Millennials vs Gen Z: Spending Habits"   |
| What [Number] [People] Taught Us    | "What 1,000 Marketers Taught Us About AI" |
| The [Adjective] Guide to [Topic]    | "The Visual Guide to Sleep Science"       |

**Section headlines:**

```markdown
## Section Headline Patterns

- [Number] + Key Insight: "73% prefer remote work"
- Question format: "Who's adopting AI fastest?"
- Comparison: "Then vs Now"
- Action verb: "How teams are adapting"
- Time-based: "The rise of [trend] since 2020"
```

**Caption writing:**

| Element      | Max Length  | Purpose               |
| ------------ | ----------- | --------------------- |
| Section head | 5-7 words   | Introduce the insight |
| Stat label   | 2-4 words   | Name what's measured  |
| Caption      | 10-15 words | Explain significance  |
| Source note  | N/A         | Credit data origin    |

### Step 6: Infographic Types

**Type selection:**

| Type        | Best For            | Structure                   |
| ----------- | ------------------- | --------------------------- |
| Statistical | Data-heavy research | Hero stat + supporting data |
| Timeline    | History, evolution  | Chronological events        |
| Process     | How-to, steps       | Sequential flow             |
| Comparison  | Versus, pros/cons   | Two columns                 |
| Geographic  | Regional data       | Map-based                   |
| List        | Tips, facts         | Numbered or bulleted        |
| Anatomical  | Breakdown, parts    | Labeled diagram             |
| Flowchart   | Decisions, paths    | Branching structure         |

**Format dimensions:**

| Platform     | Dimensions         | Aspect Ratio    |
| ------------ | ------------------ | --------------- |
| Pinterest    | 1000 x 1500px      | 2:3 vertical    |
| Blog/article | 800 x 2000px       | Long vertical   |
| Social share | 1200 x 1200px      | Square          |
| Presentation | 1920 x 1080px      | 16:9 landscape  |
| Print        | 8.5 x 11" (300dpi) | Letter vertical |

### Step 7: Data Visualization Best Practices

**Do's and don'ts:**

| Do                             | Don't                       |
| ------------------------------ | --------------------------- |
| Start bar charts at zero       | Truncate axes to exaggerate |
| Use consistent colors          | Rainbow every section       |
| Label directly on chart        | Rely only on legends        |
| Round numbers (73%, not 72.8%) | Use false precision         |
| Show data source               | Present unsourced claims    |
| Use white space                | Crowd every element         |

**Color usage:**

| Purpose           | Approach                        |
| ----------------- | ------------------------------- |
| Highlight         | Use accent color for key stat   |
| Categories        | Distinct but harmonious palette |
| Comparison        | Two contrasting colors          |
| Sequential        | Light to dark gradient          |
| Positive/negative | Green/red or blue/orange        |

**Accessibility:**

| Requirement      | Implementation             |
| ---------------- | -------------------------- |
| Color blind safe | Use patterns + colors      |
| Text contrast    | 4.5:1 minimum ratio        |
| Font size        | Minimum 12pt for body      |
| Alt text         | Describe data and insights |

### Step 8: Design Brief Template

**Brief for designer:**

```markdown
## Infographic Design Brief

### Overview

**Title:** [Infographic title]
**Topic:** [Subject matter]
**Goal:** [What action should viewers take]
**Audience:** [Who this is for]
**Dimensions:** [Size and orientation]
**Brand:** [Style guide or brand to follow]

### Content Hierarchy

#### Header

- Title: "[Headline]"
- Subtitle: "[Subtitle]"

#### Hero Section

- Big number: [XX%]
- Context: "[One-sentence explanation]"
- Visual: [Icon/illustration suggestion]

#### Section 1: [Title]

- Stat: [XX]
- Chart type: [Recommended chart]
- Data: [Values to visualize]
- Caption: "[Explanation]"

#### Section 2: [Title]

[Repeat format]

#### Section 3: [Title]

[Repeat format]

#### Footer

- CTA: "[Action text]"
- CTA link: [URL]
- Source: "[Data source with date]"
- Logo: [Brand logo placement]

### Visual Notes

- Color palette: [Hex codes or brand colors]
- Style: [Modern/playful/corporate/minimal]
- Icons: [Style preference]
- Avoid: [Any restrictions]

### Files Needed

- [ ] Web version (PNG)
- [ ] Social version (1:1)
- [ ] Print version (PDF)
- [ ] Editable source file
```

### Step 9: Social Media Versions

**Platform adaptations:**

```markdown
## Social Snippets

### Instagram/LinkedIn (1080x1080)

**Headline:** [Shortened title]
**Hero stat:** [Big number]
**2-3 supporting stats:** [Key points]
**CTA:** "Full infographic in bio" / "See more →"

### Twitter/X (1200x675)

**Headline:** [Shortened title]
**1-2 key stats:** [Most shareable]
**Visual:** Cropped hero section

### Pinterest (1000x1500)

**Use full infographic** or top half with
"Pin for later" messaging

### Stories (1080x1920)

**Split into slides:**

1. Hook/title
2. Hero stat
3. Section 1
4. Section 2
5. CTA
```

### Step 10: Source Citation

**Citation format:**

```markdown
## Data Sources

**Primary source:**
[Organization Name], "[Report/Study Title]," [Year].
[URL]

**Additional sources:**

- [Source 2 with link]
- [Source 3 with link]

**Data collection:**
[Brief methodology if relevant]
```

**Citation placement:**

| Location       | Format                           |
| -------------- | -------------------------------- |
| Footer         | "Source: [Organization], [Year]" |
| Per-stat       | Superscript number with footnote |
| Separate panel | "Data sources" section           |

## Output Format

```markdown
# Infographic Summary: [Title]

## Overview

**Topic:** [Subject]
**Data sources:** [Count] sources
**Target audience:** [Who]
**Format:** [Type and dimensions]

---

## Headline

**Title:** [Main headline]
**Subtitle:** [Supporting context]

---

## Hero Statistic

**Number:** [XX%]
**Label:** [What it measures]
**Context:** [Why it matters]
**Visual suggestion:** [Chart/icon type]

---

## Supporting Sections

### Section 1: [Theme]

**Stat:** [Number]
**Chart type:** [Recommendation]
**Data points:** [Values]
**Caption:** [Explanation]

### Section 2: [Theme]

[Repeat format]

### Section 3: [Theme]

[Repeat format]

---

## Call-to-Action

**Text:** [CTA copy]
**Link:** [URL]

---

## Sources

[Full citations]

---

## Design Brief

[Complete brief for designer]

---

## Social Adaptations

[Platform-specific versions]
```

## Validation

Before completing:

- [ ] Hero stat is compelling and accurate
- [ ] All statistics have sources
- [ ] Numbers are rounded appropriately
- [ ] Chart types match data types
- [ ] Visual hierarchy is clear
- [ ] Copy is concise (under word limits)
- [ ] CTA is included
- [ ] Accessibility considered
- [ ] Multiple format sizes provided

## Error Handling

- **No clear data**: Ask for specific statistics, survey results, or research to work from.
- **Data too complex**: Simplify to 3-5 key insights; suggest detailed report for rest.
- **No source provided**: Request original source; note if data is unverified.
- **Conflicting data**: Present most recent or most credible source; note discrepancy.
- **Data not visual**: Recommend list-style infographic or icon-based representation.

## Resources

- [Canva Infographic Maker](https://www.canva.com/) - Free design templates
- [Piktochart](https://piktochart.com/) - Infographic creator
- [Venngage](https://venngage.com/) - Business infographic tool
- [Data Wrapper](https://www.datawrapper.de/) - Chart creation
- [Coolors](https://coolors.co/) - Color palette generator
