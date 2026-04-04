---
name: slide-deck-generator
description: Generate a polished HTML slide deck from a topic, outline, or data. Outputs a self-contained .html file with keyboard/touch navigation, responsive typography, and the ALPA (Alpaca Labs) design system — Helvetica, editorial layout, clean white backgrounds.
---

# Presentation Generator

You generate self-contained HTML slide presentations using the ALPA (Alpaca Labs) design system — editorial layout with Helvetica, left-aligned typography, generous whitespace, and a clean monochrome palette. The user provides a topic, outline, data, or document — you produce a complete `.html` file they can open in any browser.

## On Start

When invoked, list the available page types for the user before proceeding:

| # | Type | Layout | Background |
|---|------|--------|------------|
| 1 | Title (Image + Title) | Full bleed image, text overlay bottom-left | Image |
| 2 | Title (Text Only) | Left-aligned h1 + subtitle + credit | White |
| 3 | Heading + Body | Eyebrow + h2 + paragraph | White |
| 4 | Heading + List | Eyebrow + h2 + bullet list | White / Grey |
| 5 | Heading + Stats | Eyebrow + h2 + vertical stat lines | White |
| 6 | Stat Row | Large centered numbers in columns | White / Grey |
| 7 | Stat Comparison | Before/after with arrows | White / Grey |
| 8 | Heading + Stat Row | Eyebrow + h2 + stat columns (centered) | White / Grey |
| 9 | Statement (white) | Bold centered text | White |
| 10 | Statement (dark) | Bold centered text | Dark |
| 11 | Data Table | Eyebrow + h2 + table | Grey |
| 12 | Insight List | Eyebrow + h2 + numbered items | White |
| 13 | Bar Chart | Eyebrow + h2 + horizontal bars | White |
| 14 | Timeline | Eyebrow + h2 + phased dots (centered) | White |
| 15 | Two Column | Eyebrow + h2 + side-by-side text | White / Grey |
| 16 | Comparison | Eyebrow + h2 + before/after boxes (centered) | White |
| 17 | Image — Full Bleed | Single image, edge to edge | Image |
| 18 | Image — Full Bleed + Title | Full image with gradient + overlaid text | Image |
| 19 | Image — Split 2 | Two images side by side | White border |
| 20 | Image — Split 3 | Three images in a row | White border |
| 21 | Image — Split 4 | 2×2 grid | White border |
| 22 | Image — Split 6 | 3×2 grid | White border |

Any slide can include a **Callout** (footnote annotation) appended below the main content.

A sample deck demonstrating every type is at `~/.claude/skills/alpa-presentation/sample.html`.

## Workflow

1. **Understand the input.** The user may provide:
   - A topic or title (you research/generate content)
   - An outline or bullet points (you expand into slides)
   - A document or report (you distill into a deck)
   - Data or analysis results (you visualize as stats/tables/charts)

2. **Plan the deck.** Before writing HTML, decide:
   - How many slides (aim for 10-20, never fewer than 6)
   - Which slide type and components each slide uses
   - The narrative arc: setup -> insight -> evidence -> recommendation -> close

3. **Write the HTML file.** Use the template below as the foundation. Customize only the slide content inside `<body>`.

4. **Save the file.** Write to the path the user specifies, or default to `~/Documents/presentation.html`. Tell the user the path so they can open it.

## Design System

### Layout Philosophy
- **Left-aligned by default.** Content is flush-left with generous left padding. Only statement slides center text.
- **Massive whitespace.** Content should breathe. Never fill the slide — leave at least 40% empty.
- **Eyebrow top-left.** Small bold monospace text in the top-left corner identifies the section.
- **Brand mark bottom-right.** A small "ALPA" wordmark sits fixed in the bottom-right corner.
- **No decorative boxes or cards.** Stats, lists, and content stand on their own — no background panels or rounded containers.

### Slide Types (background classes on `.slide` div)
| Class | Background | Text | Use for |
|-------|-----------|------|---------|
| *(none)* | White (#ffffff) | Dark | Title, content, lists, tables — the default |
| `grey` | Light grey (#f5f5f3) | Dark | Tables, stat comparisons, alternating rhythm |
| `dark` | Dark (#1a1a1a) | White | Statement slides — bold centered declarations |

### Components

**Eyebrow** — small bold label directly above the heading:
```html
<div class="eyebrow">Eyebrow Text</div>
<h2>The heading below</h2>
```
Always placed inside `.content`, immediately before the `<h2>`.

**Heading + Body** — the most common slide: heading with paragraph below:
```html
<div class="content">
    <div class="eyebrow">Eyebrow Text</div>
    <h2>The heading states the insight</h2>
    <p>Supporting paragraph with context and detail. Keep it to 2-3 lines max.</p>
</div>
```

**Heading + List** — bullet list below a heading:
```html
<div class="content">
    <h2>What we need to answer</h2>
    <ul class="body-list">
        <li>First question or point</li>
        <li>Second question or point</li>
        <li>Third question or point</li>
    </ul>
</div>
```

**Heading + Stats** — vertical stat list (not cards):
```html
<div class="content">
    <h2>Who do we build for?</h2>
    <p>Context paragraph explaining what the numbers mean.</p>
    <div class="stat-list">
        <div class="stat-line">8,211 employees</div>
        <div class="stat-line">3,313 contingent workers</div>
        <div class="stat-line bold">11,524 total workforce</div>
    </div>
</div>
```

**Stat Row** — large numbers in columns with labels (centered layout):
```html
<div class="stat-row">
    <div class="stat-col">
        <div class="stat-title">Bay Area</div>
        <div class="stat-value">50%</div>
        <div class="stat-label">Share of workforce</div>
    </div>
    <div class="stat-col">
        <div class="stat-title">Americas</div>
        <div class="stat-value">13%</div>
        <div class="stat-label">Share of workforce</div>
    </div>
</div>
```

**Stat Comparison** — before/after with arrows and change indicators:
```html
<div class="stat-row">
    <div class="stat-col">
        <div class="stat-title">Bay Area</div>
        <div class="stat-value muted">50%</div>
        <div class="stat-label">Share of workforce</div>
        <div class="stat-arrow">&#8595;</div>
        <div class="stat-value">32%</div>
        <div class="stat-change negative">-26% &#9660;</div>
    </div>
    <div class="stat-col">
        <div class="stat-title">Americas</div>
        <div class="stat-value muted">13%</div>
        <div class="stat-label">Share of workforce</div>
        <div class="stat-arrow">&#8595;</div>
        <div class="stat-value">26%</div>
        <div class="stat-change positive">+115% &#9650;</div>
    </div>
</div>
```

**Heading + Stat Row** — eyebrow + heading with columnar stats below. Same vertical rhythm as timeline slides. Use `.slide.centered`:
```html
<div class="slide centered">
    <div class="content">
        <div class="eyebrow">Section</div>
        <h2>Perfil del comprador</h2>
        <div class="stat-row">
            <div class="stat-col">
                <div class="stat-title">Label</div>
                <div class="stat-value">50%</div>
                <div class="stat-label">Description text</div>
            </div>
            <div class="stat-col">
                <div class="stat-title">Label</div>
                <div class="stat-value">30%</div>
                <div class="stat-label">Description text</div>
            </div>
        </div>
    </div>
    <div class="brand-mark">ALPA</div>
</div>
```
The `.slide.centered .content h2` rule tightens the heading's bottom margin so the heading sits close to the stat-row, matching the timeline layout.

**Statement** — bold centered text on white or dark:
```html
<!-- White statement -->
<div class="slide">
    <div class="statement">We talk about flexibility but design for predictability.</div>
</div>

<!-- Dark statement -->
<div class="slide dark">
    <div class="statement">People don't connect to policies. They connect to places, to their work, and to each other.</div>
</div>
```

**Data Table** — clean table with dotted borders:
```html
<div class="content">
    <h2>Bay Area: Workforce & Footprint Shifts ('20 - '25)</h2>
    <table class="data-table">
        <thead><tr><th>Cities</th><th>Workforce Today</th><th>Change</th><th>Ratio</th></tr></thead>
        <tbody>
            <tr><td>San Francisco</td><td>2,330</td><td class="negative">-26% &#9660;</td><td>1 : 108</td></tr>
            <tr class="total-row"><td></td><td><strong>2,330</strong></td><td class="negative">-26% &#9660;</td><td><strong>1 : 108</strong></td></tr>
        </tbody>
    </table>
</div>
```

**Insight List** — numbered items with bold lead:
```html
<div class="content">
    <h2>Key findings</h2>
    <ul class="insight-list">
        <li><span class="num">01</span><span><span class="emphasis">Bold lead</span> — supporting detail after the dash</span></li>
    </ul>
</div>
```

**Bar Chart** — horizontal bars with labels and values:
```html
<div class="content">
    <h2>Distribution</h2>
    <div class="bar-chart">
        <div class="bar-row">
            <span class="bar-label">Label</span>
            <div class="bar-track"><div class="bar-fill accent" style="width:73%"></div></div>
            <span class="bar-value">73%</span>
        </div>
    </div>
</div>
```

**Timeline** — phased progression:
```html
<div class="timeline">
    <div class="timeline-item active">
        <div class="timeline-dot"></div>
        <div class="timeline-label">Phase 1</div>
        <div class="timeline-title">Title</div>
        <div class="timeline-desc">Description</div>
    </div>
</div>
```

**Two Column** — side by side content areas:
```html
<div class="two-col">
    <div><!-- left content --></div>
    <div><!-- right content --></div>
</div>
```

**Comparison** — side by side with arrow:
```html
<div class="comparison">
    <div class="comparison-side">
        <div class="comparison-label">Before</div>
        <div class="comparison-content">Description</div>
    </div>
    <div class="comparison-arrow">&#8594;</div>
    <div class="comparison-side highlight">
        <div class="comparison-label">After</div>
        <div class="comparison-content">Description</div>
    </div>
</div>
```

**Callout** — inline annotation:
```html
<div class="callout">Key takeaway or footnote.</div>
```

**Image — Full Bleed** — single image filling the entire slide:
```html
<div class="slide image-slide">
    <img src="image-url.jpg" alt="Description" />
</div>
```

**Image — Full Bleed + Title** — full-bleed image with overlaid title (like a cover or statement). Use `.image-title-slide`:
```html
<div class="slide image-title-slide">
    <img src="image-url.jpg" alt="Description" />
    <div class="image-title-overlay">
        <h1>Title Goes Here</h1>
        <p class="subtitle">Optional subtitle</p>
    </div>
    <div class="brand-mark">ALPA</div>
</div>
```

**Image — Split 2** — two images side by side with white border:
```html
<div class="slide image-grid cols-2">
    <img src="image1.jpg" alt="" />
    <img src="image2.jpg" alt="" />
</div>
```

**Image — Split 3** — three images in a row:
```html
<div class="slide image-grid cols-3">
    <img src="image1.jpg" alt="" />
    <img src="image2.jpg" alt="" />
    <img src="image3.jpg" alt="" />
</div>
```

**Image — Split 4** — two rows of two:
```html
<div class="slide image-grid cols-2 rows-2">
    <img src="image1.jpg" alt="" />
    <img src="image2.jpg" alt="" />
    <img src="image3.jpg" alt="" />
    <img src="image4.jpg" alt="" />
</div>
```

**Image — Split 6** — two rows of three:
```html
<div class="slide image-grid cols-3 rows-2">
    <img src="image1.jpg" alt="" />
    <img src="image2.jpg" alt="" />
    <img src="image3.jpg" alt="" />
    <img src="image4.jpg" alt="" />
    <img src="image5.jpg" alt="" />
    <img src="image6.jpg" alt="" />
</div>
```

### Composition Rules
- Every content slide (not statements) should have a `eyebrow` top-left
- **Title slide**: full-bleed image with `.image-title-slide` — h1 + subtitle over gradient overlay. Falls back to white text-only title if no image is available.
- **Content slides**: white (default), left-aligned — `eyebrow` + `.content` with heading + body/list/stats
- **Statement slides**: centered text, no eyebrow — white bg for regular statements, `dark` for dramatic ones
- **Stat slides**: white or grey, centered stat-row or stat-comparison layout
- **Table slides**: white or grey, left-aligned heading + data-table
- **Dark slides**: use sparingly — at most 1-2 per deck for maximum emphasis
- **Closing slide**: white, left-aligned or centered — bold statement or summary
- Use `<span class="emphasis">` for bold inline text
- Never put more than one major component per slide (one table OR one stat-row OR one list)
- Alternate slide backgrounds for visual rhythm — never use the same type 3x in a row
- **Centered content**: Use `.slide.centered` (class on the slide div) for slides with a heading + grid, timeline, stat-row, or comparison below. These read better centered. Left-align is for heading + body text, lists, tables, and insight lists.
- Leave generous whitespace — content should occupy at most 60% of the slide

### Writing Style
- Headlines: short, declarative, opinionated. State the insight, not the topic.
  - Good: "We have 18 huddle rooms. At peak, 29 groups need one."
  - Bad: "Huddle Room Analysis"
- Subtitles and descriptions: lightweight, factual, no jargon
- Stats: pick the most dramatic number, give it context with the label
- Tables: 4-6 rows max. Use colored indicators for changes (red for negative, green for positive).
- Lists: lead with the bold action/finding, follow with the detail after an em dash

## HTML Template

Use this exact CSS and JS. Only modify the slide `<div>` elements inside `<body>`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<style>


:root {
    --black: #1a1a1a;
    --grey-700: #484848;
    --grey-500: #6b6b6b;
    --grey-300: #b0b0b0;
    --grey-200: #d4d4d4;
    --grey-100: #e8e8e6;
    --grey-50: #f5f5f3;
    --white: #ffffff;
    --accent: #E8B517;
    --negative: #D92B2B;
    --positive: #2563EB;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    background: var(--black);
    overflow: hidden;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* --- Slide base --- */
.slide {
    width: 100vw; height: 100vh;
    display: none; flex-direction: column;
    justify-content: flex-start; align-items: flex-start;
    padding: clamp(48px, 6vw, 96px) clamp(60px, 8vw, 140px);
    background: var(--white); color: var(--black);
    position: relative;
}
.slide.active { display: flex; }
.slide.dark { background: var(--black); color: var(--white); justify-content: center; align-items: center; }
.slide.centered { justify-content: center; align-items: center; }
.slide.grey { background: var(--grey-50); }

/* --- Eyebrow (top-left) --- */
.eyebrow {
    font-size: clamp(9px, 0.8vw, 11px);
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--grey-500);
    margin-bottom: clamp(16px, 2vw, 28px);
    margin-left: 4px;
}
.slide.dark .eyebrow { color: var(--grey-300); }

/* --- Brand mark (bottom-right) --- */
.brand-mark {
    position: absolute;
    bottom: clamp(28px, 3vw, 48px);
    right: clamp(36px, 4vw, 64px);
    font-size: clamp(11px, 1vw, 14px);
    font-weight: 700;
    letter-spacing: 0.15em;
    color: var(--grey-300);
    text-transform: uppercase;
}
.slide.dark .brand-mark { color: var(--grey-500); }

/* --- Page number (bottom-right, auto-generated by JS) --- */
.page-number {
    position: absolute;
    top: clamp(32px, 4vw, 56px);
    right: clamp(36px, 4vw, 64px);
    font-size: clamp(11px, 1vw, 14px);
    font-weight: 400;
    color: var(--grey-300);
}
.slide.dark .page-number { color: var(--grey-500); }

/* --- Typography --- */
h1 {
    font-size: clamp(40px, 6vw, 88px);
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1.0;
    max-width: 900px;
    margin-bottom: clamp(24px, 3vw, 48px);
}
h2 {
    font-size: clamp(24px, 3.2vw, 52px);
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.1;
    max-width: 900px;
    margin-bottom: clamp(24px, 3vw, 48px);
}
.subtitle {
    font-size: clamp(14px, 1.6vw, 24px);
    font-weight: 400;
    line-height: 1.4;
    max-width: 700px;
    color: var(--grey-500);
    margin-bottom: clamp(12px, 1.5vw, 24px);
}
p {
    font-size: clamp(13px, 1.3vw, 18px);
    font-weight: 400;
    letter-spacing: -0.01em;
    line-height: 1.7;
    max-width: 800px;
    color: var(--grey-700);
}
.slide.dark p { color: var(--grey-300); }

/* --- Content wrapper (left-aligned) --- */
.content {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    flex: 1;
    width: 100%;
    max-width: 1100px;
}
.slide.centered .content { align-items: center; text-align: center; }
.slide.centered .content h2 { margin-bottom: clamp(16px, 2vw, 32px); }
.content .stat-row { margin: 0; }

/* --- Statement (centered, for statement slides) --- */
.statement {
    font-size: clamp(28px, 4vw, 60px);
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.15;
    text-align: center;
    max-width: 900px;
    margin: auto;
}

/* --- Body list (bullet points) --- */
.body-list {
    list-style: disc;
    padding-left: 24px;
    max-width: 800px;
}
.body-list li {
    font-size: clamp(14px, 1.4vw, 20px);
    font-weight: 400;
    line-height: 1.6;
    color: var(--grey-700);
    padding: 6px 0;
}
.body-list li::marker { color: var(--black); }

/* --- Stat list (vertical, no cards) --- */
.stat-list {
    margin-top: 16px;
}
.stat-line {
    font-size: clamp(14px, 1.4vw, 20px);
    font-weight: 400;
    line-height: 1.8;
    color: var(--grey-700);
}
.stat-line.bold {
    font-weight: 700;
    color: var(--black);
}

/* --- Stat row (large numbers in columns) --- */
.stat-row {
    display: flex;
    gap: clamp(32px, 5vw, 80px);
    justify-content: center;
    align-items: flex-start;
    width: 100%;
    margin: auto;
    flex-wrap: wrap;
    text-align: center;
}
.stat-col { flex: 1; min-width: 160px; max-width: 280px; }
.stat-title {
    font-size: clamp(13px, 1.3vw, 18px);
    font-weight: 400;
    color: var(--grey-700);
    margin-bottom: 12px;
}
.stat-value {
    font-size: clamp(40px, 5.5vw, 80px);
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1.0;
    margin-bottom: 8px;
}
.stat-value.muted { color: var(--grey-300); }
.stat-label {
    font-size: clamp(11px, 1vw, 14px);
    font-weight: 400;
    color: var(--grey-500);
    margin-bottom: 8px;
}
.stat-arrow {
    font-size: clamp(16px, 1.6vw, 22px);
    color: var(--grey-300);
    margin: 12px 0;
}
.stat-change {
    font-size: clamp(11px, 1vw, 14px);
    font-weight: 700;
    margin-top: 4px;
}
.stat-change.negative { color: var(--negative); }
.stat-change.positive { color: var(--positive); }

/* --- Data table --- */
.data-table {
    width: 100%;
    max-width: 1000px;
    border-collapse: collapse;
    margin-top: 16px;
    text-align: left;
}
.data-table th {
    font-size: clamp(9px, 0.8vw, 12px);
    font-weight: 700;
    color: var(--grey-500);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 14px 16px;
    border-top: 1px dotted var(--grey-200);
    border-bottom: 1px dotted var(--grey-200);
    background: var(--grey-50);
    text-align: center;
}
.data-table th:first-child { text-align: left; }
.data-table td {
    font-size: clamp(12px, 1.2vw, 16px);
    font-weight: 400;
    color: var(--grey-700);
    padding: 14px 16px;
    border-bottom: 1px dotted var(--grey-200);
    text-align: center;
}
.data-table td:first-child { text-align: left; color: var(--black); font-weight: 400; }
.data-table .negative { color: var(--negative); font-weight: 400; }
.data-table .positive { color: var(--positive); font-weight: 400; }
.data-table .total-row td { font-weight: 700; color: var(--black); }

/* --- Insight list --- */
.insight-list { list-style: none; text-align: left; width: 100%; max-width: 800px; }
.insight-list li {
    display: flex; align-items: flex-start; gap: 20px;
    padding: 18px 0;
    border-bottom: 1px solid var(--grey-100);
    font-size: clamp(13px, 1.3vw, 18px);
    font-weight: 400; line-height: 1.6;
    color: var(--grey-700);
}
.insight-list .num { font-weight: 700; color: var(--black); min-width: 32px; }
.emphasis { font-weight: 700; color: var(--black); }
.slide.dark .emphasis { color: var(--white); }

/* --- Bar chart --- */
.bar-chart { display: flex; flex-direction: column; gap: 10px; width: 100%; max-width: 500px; }
.bar-row { display: flex; align-items: center; gap: 12px; }
.bar-label { font-size: clamp(11px, 1vw, 14px); font-weight: 400; color: var(--grey-500); min-width: 100px; text-align: right; }
.bar-track { flex: 1; height: 28px; background: var(--grey-100); overflow: hidden; }
.bar-fill { height: 100%; background: var(--grey-300); transition: width 0.6s ease; }
.bar-fill.accent { background: var(--black); }
.bar-value { font-size: clamp(11px, 1vw, 14px); font-weight: 700; color: var(--grey-500); min-width: 44px; }

/* --- Comparison --- */
.comparison { display: flex; align-items: stretch; gap: 2px; width: 100%; max-width: 850px; }
.comparison-side { flex: 1; background: var(--grey-50); padding: clamp(28px, 3vw, 44px); text-align: center; }
.comparison-side.highlight { background: var(--black); color: var(--white); }
.comparison-side.highlight p { color: var(--grey-300); }
.comparison-label { font-size: clamp(9px, 0.8vw, 11px); font-weight: 700; color: var(--grey-500); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 20px; }
.comparison-content { font-size: clamp(13px, 1.3vw, 18px); font-weight: 400; line-height: 1.6; }
.comparison-arrow { display: flex; align-items: center; font-size: clamp(13px, 1.3vw, 18px); color: var(--grey-300); padding: 0 8px; background: var(--white); }

/* --- Timeline --- */
.timeline { display: flex; align-items: flex-start; gap: 0; width: 100%; max-width: 900px; position: relative; margin-top: 20px; }
.timeline::before { content: ''; position: absolute; top: 6px; left: 12px; right: 12px; height: 2px; background: var(--grey-200); z-index: 0; }
.timeline-item { flex: 1; text-align: center; position: relative; z-index: 1; padding: 0 12px; }
.timeline-dot { width: 14px; height: 14px; background: var(--grey-200); margin: 0 auto 20px; }
.timeline-item.active .timeline-dot { background: var(--black); }
.timeline-label { font-size: clamp(9px, 0.8vw, 11px); font-weight: 700; color: var(--grey-500); text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 8px; }
.timeline-title { font-size: clamp(13px, 1.3vw, 18px); font-weight: 700; letter-spacing: -0.01em; line-height: 1.3; margin-bottom: 10px; }
.timeline-desc { font-size: clamp(11px, 1vw, 14px); font-weight: 400; line-height: 1.6; color: var(--grey-500); }

/* --- Two column --- */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(24px, 3vw, 48px); width: 100%; max-width: 900px; text-align: left; }

/* --- Callout --- */
.callout { display: inline-block; width: fit-content; background: var(--grey-50); padding: 18px 28px; margin-top: 24px; font-size: clamp(11px, 1vw, 14px); font-weight: 400; color: var(--grey-700); }

/* --- Image: full bleed --- */
.slide.image-slide { padding: 0; }
.slide.image-slide > img { width: 100%; height: 100%; object-fit: cover; display: block; }

/* --- Image: full bleed + title overlay --- */
.slide.image-title-slide { padding: 0; position: relative; }
.slide.image-title-slide > img { width: 100%; height: 100%; object-fit: cover; display: block; }
.image-title-overlay { position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: flex-end; align-items: flex-start; padding: clamp(48px, 6vw, 96px) clamp(60px, 8vw, 140px); background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.2) 40%, transparent 70%); }
.image-title-overlay h1 { color: var(--white); }
.image-title-overlay .subtitle { color: var(--grey-300); }
.slide.image-title-slide .brand-mark { color: rgba(255,255,255,0.5); }

/* --- Image: grids --- */
.slide.image-grid { padding: 0; display: none; }
.slide.image-grid.active { display: grid; }
.slide.image-grid img { width: 100%; height: 100%; object-fit: cover; display: block; }
.slide.image-grid.cols-2 { grid-template-columns: 1fr 1fr; gap: 4px; background: var(--white); }
.slide.image-grid.cols-3 { grid-template-columns: 1fr 1fr 1fr; gap: 4px; background: var(--white); }
.slide.image-grid.rows-2 { grid-template-rows: 1fr 1fr; }

/* --- Navigation --- */
.nav { position: fixed; bottom: 28px; left: 50%; transform: translateX(-50%); display: flex; gap: 4px; z-index: 100; }
.nav-btn { width: 40px; height: 40px; border: none; background: var(--black); color: var(--white); font-size: clamp(13px, 1.3vw, 18px); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: opacity 0.15s ease; opacity: 0.3; }
.nav-btn:hover { opacity: 1; }
.progress { position: fixed; top: 0; left: 0; height: 3px; background: var(--accent); transition: width 0.3s ease; z-index: 100; }
</style>
</head>
<body>

<!-- SLIDES GO HERE -->

<!--
SLIDE STRUCTURE EXAMPLES:

Title slide (image cover — default):
<div class="slide image-title-slide active">
    <img src="cover-image.jpg" alt="Cover" />
    <div class="image-title-overlay">
        <h1>Title Goes<br/>Here</h1>
        <p class="subtitle">Subtitle — Month Year</p>
    </div>
    <div class="brand-mark">ALPA</div>
</div>

Title slide (text only — fallback):
<div class="slide active">
    <div class="content">
        <h1>Title Goes<br/>Here</h1>
        <p class="subtitle">Subtitle — Month Year</p>
        <p>Prepared by Name</p>
    </div>
    <div class="brand-mark">ALPA</div>
</div>

Content slide:
<div class="slide">
    <div class="content">
        <div class="eyebrow">Eyebrow Text</div>
        <h2>Heading states the insight</h2>
        <p>Supporting text goes here.</p>
    </div>
    <div class="brand-mark">ALPA</div>
</div>

Statement slide (white):
<div class="slide centered">
    <div class="statement">Bold centered statement text.</div>
    <div class="brand-mark">ALPA</div>
</div>

Statement slide (dark):
<div class="slide dark">
    <div class="statement">Bold centered statement text on dark.</div>
    <div class="brand-mark">ALPA</div>
</div>

Centered content slide (stats, timelines, grids):
<div class="slide centered">
    <div class="content">
        <div class="eyebrow">Section</div>
        <h2>Heading</h2>
        <!-- stat-row, timeline, grid, or comparison here -->
    </div>
    <div class="brand-mark">ALPA</div>
</div>

Table slide:
<div class="slide grey">
    <div class="content">
        <div class="eyebrow">Eyebrow Text</div>
        <h2>Table heading</h2>
        <table class="data-table">...</table>
    </div>
    <div class="brand-mark">ALPA</div>
</div>
-->

<nav class="nav">
    <button class="nav-btn" onclick="prevSlide()">&#8592;</button>
    <button class="nav-btn" onclick="nextSlide()">&#8594;</button>
</nav>
<div class="progress" id="progress"></div>

<script>
const slides = document.querySelectorAll('.slide');
let current = 0;
function showSlide(n) {
    slides[current].classList.remove('active');
    current = (n + slides.length) % slides.length;
    slides[current].classList.add('active');
    document.getElementById('progress').style.width = ((current + 1) / slides.length * 100) + '%';
}
function nextSlide() { showSlide(current + 1); }
function prevSlide() { showSlide(current - 1); }
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); nextSlide(); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); prevSlide(); }
});
let touchStartX = 0;
document.addEventListener('touchstart', (e) => { touchStartX = e.changedTouches[0].screenX; });
document.addEventListener('touchend', (e) => {
    const diff = e.changedTouches[0].screenX - touchStartX;
    if (Math.abs(diff) > 50) { diff < 0 ? nextSlide() : prevSlide(); }
});
document.getElementById('progress').style.width = (1 / slides.length * 100) + '%';
// Auto-inject page numbers (skip first and last slide)
slides.forEach((slide, i) => {
    if (i > 0 && i < slides.length - 1) {
        const num = document.createElement('div');
        num.className = 'page-number';
        num.textContent = String(i).padStart(2, '0');
        slide.appendChild(num);
    }
});
</script>
</body>
</html>
```

## Accent Color

The default accent is `--accent: #E8B517` (warm yellow — used only on the progress bar). The design is primarily monochrome — black, white, and greys. Change indicators use `--negative: #D92B2B` (red) and `--positive: #2563EB` (blue) for data.

If the presentation is for a different brand or context, change `--accent`. Common alternatives:
- Blue: `#2563EB`
- Teal: `#0D7377`
- Purple: `#6B21A8`
- Orange: `#C2410C`

Ask the user if they want a specific accent color. If the topic suggests a brand, try to match.

## Slide Structure Rules

1. **First slide**: Always `active` — use `.image-title-slide` with a relevant cover image, h1 + subtitle over gradient. If no image is available, fall back to white text-only title (h1 + `.subtitle` + credit).
2. **Second slide**: Context or framing question — what we need to answer, what this is about.
3. **Middle slides**: Alternate between white and grey backgrounds. Use statement slides (white or dark) to break rhythm and emphasize key points. Build the argument.
4. **Stat slides**: Use `<div class="slide centered">` to center the stat-row on the page. No eyebrow needed.
5. **Statement slides**: Center the `.statement` div. No eyebrow. Use dark bg sparingly (1-2 per deck).
6. **Penultimate slide**: The ask / recommendations / next steps
7. **Last slide**: White — closing statement or summary, left-aligned or centered.

## Output

Write the complete HTML file using the Write tool. The first slide must have class `active`. Every slide must be a direct child `<div class="slide ...">` inside body, before the `<nav>`. Add `<div class="brand-mark">ALPA</div>` to every slide.
