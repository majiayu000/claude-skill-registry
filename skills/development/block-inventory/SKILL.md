---
name: block-inventory
description: Survey available blocks from local AEM Edge Delivery Services project and Block Collection to understand the block palette available for authoring. Returns block inventory with purposes to inform content modeling decisions.
---

# Block Inventory

Survey and catalog available blocks to understand what authoring options exist.

## When to Use This Skill

Use this skill when:
- Starting a page import to understand available blocks
- Planning content structure and need to know block options
- An author would see a block library and choose from available options

**Do NOT use this skill when:**
- You already know which specific block you need
- Building new blocks from scratch
- Only checking if one specific block exists (use block-collection-and-party directly)

## Why This Skill Exists

Real authors see a block library in their authoring tools. They think: "I want a hero section... oh, there's a Hero block!"

This skill provides that same context - understanding what blocks are available BEFORE making authoring decisions.

## Related Skills

- **page-import** - Top-level orchestrator
- **identify-page-structure** - Invokes this skill to survey blocks (Step 2.5)
- **block-collection-and-party** - This skill uses it to search Block Collection
- **content-modeling** - Can reference block inventory but maintains independent judgment

## Block Inventory Workflow

### Step 1: Scan Local Project Blocks

Check what blocks already exist in the project:

```bash
# List all local blocks
ls -d blocks/*/
```

**For each block found:**
- Record block name
- Note: Purpose/description comes from block code or documentation

**Output:** List of local block names

---

### Step 2: Search Block Collection for Common Blocks

Search for commonly-used blocks that might not be in the project yet.

**Common blocks to search (run in parallel):**

```bash
# Search all common blocks in parallel
node .claude/skills/block-collection-and-party/scripts/search-block-collection-github.js hero &
node .claude/skills/block-collection-and-party/scripts/search-block-collection-github.js cards &
node .claude/skills/block-collection-and-party/scripts/search-block-collection-github.js columns &
node .claude/skills/block-collection-and-party/scripts/search-block-collection-github.js accordion &
node .claude/skills/block-collection-and-party/scripts/search-block-collection-github.js tabs &
node .claude/skills/block-collection-and-party/scripts/search-block-collection-github.js carousel &
node .claude/skills/block-collection-and-party/scripts/search-block-collection-github.js quote &
node .claude/skills/block-collection-and-party/scripts/search-block-collection-github.js fragment &
wait
```

**Why these specific blocks:**
- hero - Large prominent content at page top
- cards - Grid of items with images/text
- columns - Side-by-side content layouts
- accordion - Expandable Q&A sections
- tabs - Switchable content panels
- carousel - Rotating image/content displays
- quote - Highlighted testimonials or quotes
- fragment - Reusable content sections

**Output:** Block Collection blocks with live example URLs

---

### Step 3: Get Block Purposes

For each block found (local or Block Collection):

**If from Block Collection:**
- Purpose is clear from live example URL
- Visit live example to understand usage: `https://main--aem-block-collection--adobe.aem.live/block-collection/{block-name}`

**If local block:**
- Check for README or comments in block code
- Infer from block name and structure
- May need to describe based on code examination

**Output:** Block name + purpose/description

---

### Step 4: Consolidate Block Inventory

Create comprehensive block palette:

**Format:**
```
Available Blocks:

LOCAL BLOCKS:
- {block-name}: {purpose}
- {block-name}: {purpose}

BLOCK COLLECTION (can be added):
- hero: Large heading, text, and buttons at top of page
- cards: Grid of items with images, headings, and descriptions
- columns: Side-by-side content in 2-3 columns
- accordion: Expandable questions and answers
- tabs: Content organized in switchable tabs
- carousel: Rotating images or content panels
- quote: Highlighted testimonial or pullquote
- fragment: Reusable content section
```

**Important notes in output:**
- Local blocks are already available for use
- Block Collection blocks can be added if needed
- Link to Block Collection for authors to see examples

**Output:** Complete block inventory

---

## Usage Example

**Scenario:** Starting WKND Trendsetters homepage import

**Step 1 - Local blocks:**
```bash
ls -d blocks/*/
# Output: (none found - new project)
```

**Step 2 - Block Collection search:**
```bash
# Run parallel searches
node .claude/skills/block-collection-and-party/scripts/search-block-collection-github.js hero &
node .claude/skills/block-collection-and-party/scripts/search-block-collection-github.js cards &
# ... (all common blocks)
wait
```

**Results:**
- hero ✅ Found
- cards ✅ Found
- columns ✅ Found
- accordion ✅ Found
- tabs ✅ Found
- carousel ✅ Found
- quote ✅ Found
- fragment ✅ Found

**Step 3 - Get purposes:**
Visit live examples or read descriptions from search results

**Step 4 - Consolidated output:**
```
Block Inventory for Migration:

LOCAL BLOCKS:
(None - new project)

BLOCK COLLECTION AVAILABLE:
- hero: Large heading, paragraph, and call-to-action buttons for page introductions
  Example: https://main--aem-block-collection--adobe.aem.live/block-collection/hero

- cards: Grid layout of content items with images, headings, and descriptions
  Example: https://main--aem-block-collection--adobe.aem.live/block-collection/cards

- columns: Side-by-side content in 2-3 columns for comparisons or layouts
  Example: https://main--aem-block-collection--adobe.aem.live/block-collection/columns

- accordion: Expandable sections for FAQs or collapsed content
  Example: https://main--aem-block-collection--adobe.aem.live/block-collection/accordion

- tabs: Tabbed interface for organizing related content
  Example: https://main--aem-block-collection--adobe.aem.live/block-collection/tabs

- carousel: Rotating slideshow of images or content
  Example: https://main--aem-block-collection--adobe.aem.live/block-collection/carousel

- quote: Highlighted testimonial or pullquote with attribution
  Example: https://main--aem-block-collection--adobe.aem.live/block-collection/quote

- fragment: Reusable content section that can be embedded across pages
  Example: https://main--aem-block-collection--adobe.aem.live/block-collection/fragment
```

---

## Key Principles

**Completeness over perfection:**
- Better to show too many blocks than miss one
- Authors can ignore blocks they don't need
- Discovering a perfect-fit block later is frustrating

**Practical purposes:**
- Describe blocks in author language, not developer terms
- "Grid of items" not "repeating collection pattern"
- "Expandable Q&A" not "interactive disclosure widget"

**Block Collection focus:**
- Prioritize Block Collection blocks (vetted, accessible, performant)
- These are the canonical implementations
- Can be added to any project

**Speed matters:**
- Run searches in parallel
- Don't visit every live example (time-consuming)
- Get enough info to understand purpose

---

## Common Blocks Reference

Here's a quick reference for the most common blocks:

| Block | Purpose | When Authors Use It |
|-------|---------|-------------------|
| hero | Page introduction | "I want a big heading at the top" |
| cards | Content grid | "I want items in a grid with pictures" |
| columns | Side-by-side | "I want two things next to each other" |
| accordion | Collapsible Q&A | "I have FAQs that should expand/collapse" |
| tabs | Tabbed content | "I want content in switchable tabs" |
| carousel | Image slider | "I want images that rotate/slide" |
| quote | Testimonial | "I want to highlight a customer quote" |
| fragment | Reusable content | "I want to reuse this section on multiple pages" |

---

## Limitations

This skill does NOT:
- Determine which block to use (that's content-modeling's job)
- Validate if blocks work correctly
- Create new blocks
- Search Block Party (focuses on Block Collection + local)
- Provide detailed implementation guidance

For those needs, use the appropriate skills:
- content-modeling: Determine which block fits
- block-collection-and-party: Deep search and code examination
- building-blocks: Create new blocks
- content-driven-development: Implementation guidance
