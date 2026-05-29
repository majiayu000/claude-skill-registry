---
name: presentation-builder
description: Generate polished HTML slide presentations from video scripts, outlines, or topic briefs. Produces single-file HTML with scroll-snap navigation, animations, and distinctive design. Use when user asks to create a presentation, slide deck, or wants to turn a script/outline into visual slides.
---

## Load Context First

Before executing this skill, read the following files from the project folder if they exist:

1. **USER.md** — who the user is, how they think, how they work
2. **BUSINESS.md** — their business, products, positioning, brand voice, content strategy
3. **ICP.md** — their ideal customer, their language, their fears, what makes them buy
4. **Voice or brand voice skill** — look for any installed skill related to voice, tone, or brand voice and apply it automatically
5. Any additional context provided by the user in this session

Use all context silently. Do not reference or summarize files unless asked.

---

# Presentation Builder

**Purpose:** Generate complete, polished HTML slide presentations from video scripts, outlines, or topic briefs. Output is a single `.html` file with embedded CSS and JS — no dependencies except Google Fonts.

## When to Activate

Use this skill when:
- User asks to create a presentation or slide deck
- User has a script, outline, or topic they want turned into slides
- User mentions "presentation", "slides", or "deck"
- User wants visual content for a talk or meeting

## Process

### 1. Analyze the Input

Read the script/outline/topic and identify:
- The core narrative arc (what's the story?)
- Key sections and transitions
- Data points, comparisons, lists, quotes
- How many slides are needed (aim for 10-20)

### 2. Map Content to Slide Types

| Content | Slide Type |
|---------|-----------|
| Opening / hook | **Title** |
| Bold claim, thesis, or quote | **Quote/Statement** |
| Multiple items with descriptions | **Content Grid** (cards) |
| Before/after, pros/cons | **Comparison** (two columns) |
| File structures, hierarchies | **Tree/Structure** |
| Systems with connections | **Diagram** (multi-element) |
| Features, tools, plugins | **Feature Cards** |
| Numbers, metrics, results | **Stats/Results** (big numbers) |
| Sequential instructions | **Steps/Numbered List** |
| Final pitch, links, subscribe | **CTA/Closing** |

### 3. Design Decisions

Before writing HTML, decide:
- **Color palette**: 1 accent + 1-2 supporting colors matching the topic
- **Typography**: Google Fonts pair — display font (headings) + mono font (labels). Avoid Inter, Roboto, Arial. Good choices: Sora, Space Grotesk, Outfit, Plus Jakarta Sans paired with JetBrains Mono, Fira Code.
- **Mood**: Dark theme by default. Adjust for topic energy.

### 4. Build the Presentation

For each slide:
1. Pick the appropriate slide type
2. Fill in content
3. Add staggered reveal animations
4. Set slide counter
5. **Verify: fits in one viewport** — if not, split

### 5. Technical Requirements

**Mandatory:**
- `html { scroll-snap-type: y mandatory; }`
- `.slide { scroll-snap-align: start; height: 100vh; }`
- Keyboard navigation (arrow keys)
- Fixed right-side dot navigation
- Fade-up animations with IntersectionObserver
- Slide numbering (NN / TOTAL) in top-right
- Single-file HTML with embedded CSS/JS
- Google Fonts via CDN link

## Rules

1. **One viewport per slide** — no scrolling within a slide. Split if overflow.
2. **Screenshots get their own slides** — never on content-heavy slides.
3. **Single-file HTML** — all CSS and JS embedded.
4. **No generic aesthetics** — custom colors, distinctive fonts, themed accents per presentation.
5. **Content limits** — follow max items per slide type to prevent overflow.

## Output

A complete `.html` file ready to open in any browser. Present it as a code block or save directly to a file.

## Quality Checklist

- [ ] Every slide fits in 100vh (no internal scrolling)
- [ ] Navigation works (arrows + dots)
- [ ] Animations trigger on scroll
- [ ] Slide numbers are sequential and correct
- [ ] Google Fonts loaded
- [ ] Color palette is intentional (not default)
- [ ] Typography pairing is distinctive
- [ ] Content is readable at presentation distance
- [ ] 10-20 slides (not too few, not too many)
