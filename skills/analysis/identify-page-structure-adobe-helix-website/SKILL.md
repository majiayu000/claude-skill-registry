---
name: identify-page-structure
description: Identify section boundaries and content sequences within a scraped webpage for AEM Edge Delivery Services import. Performs two-level analysis (sections, then sequences per section) and surveys available blocks.
---

# Identify Page Structure

Analyze webpage structure using two-level hierarchy: sections, then content sequences within each section.

## When to Use This Skill

Use this skill when:
- You have scraped webpage output (screenshot, HTML, metadata)
- Need to identify section boundaries and content sequences
- Ready to understand page structure before making authoring decisions

**Invoked by:** page-import skill (Step 2)

## Prerequisites

From scrape-webpage skill, you need:
- ✅ screenshot.png showing full page
- ✅ cleaned.html with page content
- ✅ metadata.json with paths

## Related Skills

- **page-import** - Orchestrator that invokes this skill
- **scrape-webpage** - Provides input (screenshot, HTML)
- **page-decomposition** - This skill invokes it for EACH section
- **block-inventory** - This skill invokes it to survey available blocks
- **authoring-analysis** - Uses this skill's output to make authoring decisions

## Key Concepts

**CRITICAL:** Content follows a strict two-level hierarchy:

```
DOCUMENT
├── SECTION (top-level container with optional metadata)
│   ├── Content Sequence 1 (default content OR block)
│   ├── Content Sequence 2 (default content OR block)
│   └── ...
├── SECTION
│   └── Content Sequence 1
└── ...
```

**This skill analyzes BOTH levels:**
- Level 1: Section boundaries (Step 2a)
- Level 2: Content sequences within EACH section (Step 2b per section)

## Structure Identification Workflow

### Step 2a: Identify Section Boundaries (Level 1)

Examine the **screenshot** to find visual/thematic breaks that indicate new sections.

**Visual cues for section boundaries:**
- Background color changes (white → grey → dark → white)
- Spacing/padding changes (tight → wide → normal)
- Clear horizontal breaks or dividers
- Thematic content shifts

**What to exclude:**
- Header/navigation (auto-populated)
- Footer (auto-populated)
- Cookie banners, popups

**For each section, note:**
- Section number (sequential: 1, 2, 3...)
- Visual style (light, dark, grey, accent)
- Brief overview of what's in it

**Example output:**
```
Section 1: light background, hero content
Section 2: light background, grid of features
Section 3: grey background, article cards
Section 4: dark background, tabs
```

---

### Step 2b: Analyze Content Sequences Within Each Section (Level 2)

For EACH section identified in Step 2a, analyze its internal content sequences.

**What is a "content sequence"?**
A vertical flow of related content that will become EITHER:
- Default content (headings, paragraphs, lists, inline images)
- A block (structured, repeating, or interactive component)

**Breaking points between sequences:**
- Change from default content → block
- Change from block → different block
- Change from block → default content

**INVOKE page-decomposition skill FOR EACH SECTION** to get neutral descriptions.

**For each section, get:**
- Sequence 1: [Neutral description - NO block names yet]
- Sequence 2: [Neutral description]
- ...

**Example output:**
```
Section 1 (light):
  - Sequence 1: Large centered heading, paragraph, two buttons
  - Sequence 2: Two images displayed side-by-side

Section 2 (light):
  - Sequence 1: Centered heading
  - Sequence 2: Grid of 8 items, each with icon and short text
  - Sequence 3: Two centered buttons

Section 3 (grey):
  - Sequence 1: Eyebrow text, heading, paragraph, button
  - Sequence 2: Four items in grid, each with image, category tag, heading, description

Section 4 (dark):
  - Sequence 1: Tab navigation with three switchable content panels
```

---

### Step 2.5: Survey Available Blocks

**STOP: Before making any authoring decisions, understand what blocks are available.**

**INVOKE block-inventory skill** to catalog available blocks.

**Why this matters:**
Real authors see a block library and choose from available options. You need the same context to make authentic authoring decisions following David's Model.

**What this provides:**
- Local blocks already in project
- Common Block Collection blocks that can be added
- Purpose/description for each block
- Live example URLs

**Example output:**
```
Available Blocks:

LOCAL BLOCKS:
- custom-banner: Special promotional banner
- testimonial-slider: Customer testimonials carousel

BLOCK COLLECTION AVAILABLE:
- hero: Large heading, text, buttons for page intro
- cards: Grid of items with images/text
- columns: Side-by-side content layout
- accordion: Expandable Q&A sections
- tabs: Switchable content panels
- carousel: Rotating image/content displays
- quote: Highlighted testimonials
- fragment: Reusable content sections
```

---

## Output Format

This skill provides complete page structure:

**1. Section boundaries with styling:**
```
Section 1: light background
Section 2: light background
Section 3: grey background (#f5f5f5)
Section 4: dark background (#1a1a1a)
```

**2. Content sequences per section (neutral descriptions):**
```
Section 1 (light):
  - Sequence 1: Large centered heading, paragraph, two call-to-action buttons
  - Sequence 2: Two images displayed side-by-side

Section 2 (light):
  - Sequence 1: Single centered heading
  - Sequence 2: Grid of 8 items, each with icon and short text
  - Sequence 3: Two centered buttons

[Continue for all sections...]
```

**3. Block palette:**
```
LOCAL BLOCKS: [list]
BLOCK COLLECTION AVAILABLE: [list with purposes]
```

**Next step:** Pass these outputs to authoring-analysis skill

---

## Key Principles

**Two-level analysis is mandatory:**
- You MUST identify sections first (2a)
- Then analyze each section's content sequences (2b)
- Don't skip levels or combine them

**Stay neutral at this stage:**
- Describe WHAT you see, not WHAT it should be
- "Grid of items with images" not "Cards block"
- Authoring decisions come in next skill

**Block inventory before decisions:**
- Survey blocks BEFORE making any authoring choices
- Authors see a library and choose - you need same context
