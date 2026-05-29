---
name: page-decomposition
description: Analyze content sequences within a section and provide neutral descriptions for AEM Edge Delivery Services. Invoked per section during page import to identify breaking points between default content and blocks.
---

# Page Decomposition

Analyze content sequences within a section and provide neutral descriptions without assigning block names.

## When to Use This Skill

This skill is called by **identify-page-structure** for EACH section to:
- Identify content sequences within that section
- Provide neutral descriptions (NO block names yet)
- Identify breaking points between sequences
- Enable authoring-focused decisions later

**IMPORTANT:** This skill analyzes ONE section at a time, not the whole page.

## Input Required

From the calling skill (identify-page-structure), you need:
- Section visual description and boundaries
- Screenshot showing the section
- Cleaned HTML content for the section

## Related Skills

- **page-import** - Top-level orchestrator
- **identify-page-structure** - Invokes this skill for each section (Step 2b)
- **block-inventory** - Provides available blocks AFTER decomposition
- **content-modeling** - Makes authoring decisions AFTER decomposition
- **content-driven-development** - References section structure in html-structure.md

## Key Concepts

**Content Hierarchy:**
```
DOCUMENT
├── SECTION (top-level, analyzed by identify-page-structure Step 2a)
│   ├── Content Sequence 1 ← THIS SKILL IDENTIFIES THESE
│   ├── Content Sequence 2 ← THIS SKILL IDENTIFIES THESE
│   └── ...
└── SECTION
    └── Content Sequence 1
```

**What is a "content sequence"?**
A vertical flow of related content that will eventually become:
- Default content (headings, paragraphs, lists, inline images), OR
- A block (structured, repeating, or interactive component)

**Breaking points between sequences:**
- Visual/semantic shift in content type
- Change from prose → structured pattern
- Change from one pattern → different pattern

**Philosophy:**
- Describe WHAT you see, not WHAT it should be
- "Two images side-by-side" not "Columns block"
- "Grid of 8 items with icons" not "Cards block"
- Stay neutral - authoring decisions come later

## Decomposition Workflow

**Context:** identify-page-structure has already identified section boundaries (Step 2a). This skill is invoked FOR ONE SECTION to analyze its internal content sequences.

---

### Step 1: Examine the Section

Look at the screenshot and HTML for THIS section only.

**What to observe:**
- Vertical flow of content from top to bottom
- Where content changes type or pattern
- Visual groupings or breaks

**Ignore:**
- Other sections (out of scope)
- Section styling (already identified by page-import)
- Block names (stay neutral)

**Output:** Mental model of content flow within this section

---

### Step 2: Identify Breaking Points

Find where content shifts from one type/pattern to another.

**Breaking point indicators:**
- Prose text → Structured grid
- Heading/paragraph → Side-by-side images
- One repeating pattern → Different repeating pattern
- Structured content → Prose text

**Example within a section:**
```
Content flows top to bottom:
- Large heading
- Paragraph
- Two buttons
[BREAK] ← Visual/semantic shift
- Two images displayed side-by-side
```

**Output:** List of breaking points

---

### Step 3: Define Content Sequences

Between each breaking point is a content sequence.

**For each sequence, describe:**
- What elements it contains (heading, paragraph, images, etc.)
- How they're arranged (stacked, side-by-side, in a grid)
- Quantity (one heading, two images, grid of 8 items)

**Use neutral language:**
- ✅ "Two images displayed side-by-side"
- ❌ "Columns block with two images"
- ✅ "Grid of 8 items, each with icon and short text"
- ❌ "Cards block"
- ✅ "Large centered heading, paragraph, two buttons stacked vertically"
- ❌ "Hero block"

**Output:** Neutral descriptions for each sequence

---

### Step 4: Return Structured Output

Provide content sequences for this section in structured format.

**Output format:**
```javascript
{
  sectionNumber: 1,  // From identify-page-structure
  sequences: [
    {
      sequenceNumber: 1,
      description: "Large centered heading, paragraph, two buttons stacked vertically"
    },
    {
      sequenceNumber: 2,
      description: "Two images displayed side-by-side"
    }
  ]
}
```

**This enables:**
- Clear understanding of section's internal structure
- Neutral foundation for authoring decisions
- Separation of description from implementation

---

## Section Metadata Format

**Table format:**
```markdown
+------------------------------+
| Section Metadata             |
+------------------+-----------+
| style            | light     |
+------------------+-----------+
```

**Placement:** At the start of each section, before content

**Usage:** Applied by generate-import-html skill when generating final HTML

---

## Examples

### Example 1: Hero Section

**Input:** "Section 1 (light background): Large prominent content at top of page"

**Visual observation:**
- Large centered heading
- Paragraph text below it
- Two call-to-action buttons
[BREAK - visual shift]
- Two large images displayed next to each other

**Output:**
```javascript
{
  sectionNumber: 1,
  sequences: [
    {
      sequenceNumber: 1,
      description: "Large centered heading, paragraph, two call-to-action buttons stacked vertically"
    },
    {
      sequenceNumber: 2,
      description: "Two large images displayed side-by-side"
    }
  ]
}
```

---

### Example 2: Features Section

**Input:** "Section 2 (light background): Grid of feature items"

**Visual observation:**
- Centered heading
[BREAK - shift to structured pattern]
- Grid of 8 items
- Each item has: small icon, short text description
[BREAK - shift back to simple elements]
- Two centered buttons

**Output:**
```javascript
{
  sectionNumber: 2,
  sequences: [
    {
      sequenceNumber: 1,
      description: "Single centered heading"
    },
    {
      sequenceNumber: 2,
      description: "Grid of 8 items, each with small icon and short text description"
    },
    {
      sequenceNumber: 3,
      description: "Two centered buttons"
    }
  ]
}
```

---

### Example 3: Article Cards Section

**Input:** "Section 3 (grey background): Blog articles"

**Visual observation:**
- Eyebrow text "Latest Articles"
- Large heading
- Paragraph description
- Browse button
[BREAK - shift to repeating pattern]
- 4 items in grid
- Each item: image, category tag, heading, short description, read link

**Output:**
```javascript
{
  sectionNumber: 3,
  sequences: [
    {
      sequenceNumber: 1,
      description: "Eyebrow text, large heading, paragraph description, browse button - all stacked vertically"
    },
    {
      sequenceNumber: 2,
      description: "Grid of 4 items, each with image, category tag, heading, description, and read link"
    }
  ]
}
```

---

### Example 4: Simple Content Section

**Input:** "Section 4 (light background): Body content"

**Visual observation:**
- Multiple paragraphs of text
- Some inline images within the text
- Headings interspersed (H2, H3)
- No clear breaking points - content flows naturally

**Output:**
```javascript
{
  sectionNumber: 4,
  sequences: [
    {
      sequenceNumber: 1,
      description: "Flowing prose content: multiple paragraphs with inline images and headings (H2, H3)"
    }
  ]
}
```

**Note:** This entire section is one sequence because content flows naturally without structural breaks.

---

## Common Mistakes to Avoid

**Using block names in descriptions:**
❌ "Hero block with heading and buttons"
✓ "Large centered heading, paragraph, two buttons stacked vertically"

**Not identifying breaking points:**
❌ Describing entire section as one sequence when there are clear shifts
✓ Identifying where content type changes and breaking into sequences

**Being too granular:**
❌ Each element as separate sequence: "Heading", "Paragraph", "Button"
✓ Related elements together: "Heading, paragraph, two buttons stacked vertically"

**Mixing analysis levels:**
❌ Analyzing multiple sections at once
✓ Focus on ONE section at a time (per invocation)

**Making authoring decisions:**
❌ "This should be a cards block because..."
✓ "Grid of 4 items with images and text" (neutral description)
