---
name: authoring-analysis
description: Analyze content sequences and determine authoring approach (default content vs blocks). Validates block selection and section styling for import/migration to AEM Edge Delivery Services.
---

# Authoring Analysis

Determine authoring approach for EACH content sequence: default content or specific block.

## When to Use This Skill

Use this skill when:
- You have page structure with content sequences (from identify-page-structure)
- You have block inventory (local + Block Collection)
- Ready to make authoring decisions following David's Model

**Invoked by:** page-import skill (Step 3)

## Prerequisites

From identify-page-structure skill, you need:
- ✅ Section boundaries with styling notes
- ✅ Content sequences per section (neutral descriptions)
- ✅ Block inventory (local + Block Collection with purposes)
- ✅ screenshot.png for visual reference

## Related Skills

- **page-import** - Orchestrator that invokes this skill
- **identify-page-structure** - Provides section structure and block inventory
- **content-modeling** - This skill invokes it when block selection is unclear
- **block-collection-and-party** - This skill invokes it to validate blocks
- **generate-import-html** - Uses this skill's output to create HTML

## **IMPORTANT: Step 3e Execution Trigger**

After completing Step 3 (analyzing all sequences), you MUST execute Step 3e if:
- ✅ At least one section contains exactly ONE sequence that became a block
- ✅ That section has distinct background styling from identify-page-structure

If NO sections meet these criteria → Skip Step 3e
If ANY sections meet these criteria → Execute Step 3e for EACH qualifying section

## Authoring Analysis Workflow

**Context:** You now have:
- Section boundaries with styles
- Content sequences per section
- Available block palette

**FOR EACH content sequence, follow this mandatory process:**

---

### Step 3a: MANDATORY - Default Content Check (FIRST!)

**Question:** "Can an author create this with normal typing in Word/Google Docs?"

**Default content means:**
- ✅ Headings, paragraphs, lists
- ✅ Inline images within text
- ✅ Simple quotes
- ✅ Just... typing content

**NOT default content means:**
- ❌ Repeating structured patterns (card grids, feature lists)
- ❌ Interactive components (accordions, tabs, carousels)
- ❌ Complex layouts (side-by-side columns, split content)
- ❌ Requires specific structure for decoration

**Decision:**
- If YES (can type normally) → **Mark as DEFAULT CONTENT, DONE** ✅
- If NO (needs structure) → **Proceed to Step 3b**

**Examples:**
```
"Large centered heading, paragraph, two buttons"
→ Can author just type heading, paragraph, links? YES
→ Decision: DEFAULT CONTENT ✅

"Two centered buttons"
→ Can author just type two links? YES
→ Decision: DEFAULT CONTENT ✅

"Four items in grid, each with image, heading, description"
→ Can author just type this? NO - requires grid structure
→ Decision: Proceed to Step 3b ➡️

"Expandable questions and answers"
→ Can author just type this? NO - requires interaction/decoration
→ Decision: Proceed to Step 3b ➡️
```

---

### Step 3b: Block Selection (ONLY IF NOT DEFAULT)

**With block inventory context, ask:** "Which available block would an author choose for this?"

**DECISION TREE: When to Invoke content-modeling**

**OBVIOUS MATCH (Don't invoke content-modeling):**

Pattern matches block purpose 1:1:
- "Grid of items with images/text" + see "cards" block → USE IT ✅
- "Expandable questions" + see "accordion" block → USE IT ✅
- "Tabbed content panels" + see "tabs" block → USE IT ✅
- "Side-by-side content" + see "columns" block → USE IT ✅
- "Rotating images" + see "carousel" block → USE IT ✅

**Criteria for OBVIOUS:**
- Content description matches block purpose exactly
- No ambiguity about structure
- Block exists in inventory

**UNCLEAR MATCH (Invoke content-modeling):**

Ambiguous which block to use:
- "Three items with images" - Could be cards? Could be columns? → INVOKE
- "List of features with icons" - Cards? Custom list block? → INVOKE
- "Customer quotes with photos" - Quote block? Cards? Testimonial block? → INVOKE

Missing from inventory:
- Content needs structure BUT no matching block exists → INVOKE
- content-modeling can recommend canonical model or suggest creating custom block

Complex authoring consideration:
- "Hero-like content but in middle of page" → INVOKE
- "Card-like items but only 2 of them" → INVOKE
- Need validation on author mental model → INVOKE

**Criteria for UNCLEAR:**
- Multiple blocks could work
- No obvious block match
- Need authoring perspective validation
- Creating custom block might be needed

---

### Step 3c: Validate Block Exists (IF NEEDED)

**Only if block not in Block Collection common set:**

Invoke **block-collection-and-party** skill to:
- Confirm block exists
- Get live example URL
- Review content model

---

### Step 3d: Get Block HTML Structure (BEFORE generating HTML)

**CRITICAL:** Before generating any HTML in next skill, fetch the pre-decoration HTML structure for ALL blocks you'll use.

```bash
# Get structure examples for each block
node .claude/skills/block-collection-and-party/scripts/get-block-structure.js cards
node .claude/skills/block-collection-and-party/scripts/get-block-structure.js tabs
node .claude/skills/block-collection-and-party/scripts/get-block-structure.js accordion
node .claude/skills/block-collection-and-party/scripts/get-block-structure.js columns
```

**Why this prevents mistakes:**
- Shows exact row/column structure (e.g., cards: each card = 1 row with 2 columns)
- Reveals all variants (e.g., "Cards" vs "Cards (no images)")
- Displays clean HTML without decoration
- Prevents the #1 HTML generation error: wrong structure

**Use the output to:**
1. Understand how many columns each row should have
2. See where images vs content go
3. Match your content to the correct variant
4. Generate HTML that matches the expected structure exactly

---

### Step 3 Output Format

**Complete analysis for all sequences:**

```
Section 1 (light):
  - Sequence 1: "Large centered heading, paragraph, two call-to-action buttons"
    → Decision: DEFAULT CONTENT
    → Reason: Author can type heading, paragraph, links normally
    → Note: Prominent styling is a CSS concern

  - Sequence 2: "Two images side-by-side"
    → Decision: Columns block (2 columns)
    → Reason: Side-by-side layout requires structure
    → Obvious match with "columns" block in inventory

Section 2 (light):
  - Sequence 1: "Centered heading"
    → Decision: DEFAULT CONTENT
    → Reason: Just a heading - author types it

  - Sequence 2: "Grid of 8 items, each with icon and short text"
    → Decision: Cards block
    → Reason: Repeating structured pattern, needs block
    → Obvious match with "cards" block in inventory

  - Sequence 3: "Two centered buttons"
    → Decision: DEFAULT CONTENT
    → Reason: Just two links - author types them

Section 3 (grey):
  - Sequence 1: "Eyebrow text, heading, paragraph, button stacked vertically"
    → Decision: DEFAULT CONTENT
    → Reason: Author types text and link normally

  - Sequence 2: "Four items in grid, each with image, category tag, heading, description"
    → Decision: Cards block
    → Reason: Repeating structured pattern
    → Obvious match with "cards" block in inventory

Section 4 (dark):
  - Sequence 1: "Tab navigation with three switchable content panels"
    → Decision: Tabs block
    → Reason: Interactive component, needs decoration
    → Obvious match with "tabs" block in inventory
```

---

### Step 3e: Validate Section Styling (Single-Block Sections Only)

**⚠️ EXECUTION TRIGGER:** This step is executed AFTER Step 3 is complete. Execute this step if and only if:
- ✅ You have completed Step 3 (identified which sequences become blocks)
- ✅ At least one section contains exactly ONE sequence that became a block
- ✅ That section has distinct background styling from identify-page-structure

**If NO sections meet these criteria → Skip Step 3e entirely and proceed to next skill**

**If ANY sections meet these criteria → You MUST execute all sub-steps below for EACH qualifying section**

---

**Why this validation matters:**

When a section contains a single block, the background styling might be:
- **Block-specific design** (e.g., hero with dark background image) → Don't add section-metadata
- **Section container styling** (e.g., dark section with tabs block) → Add section-metadata

Without validation, we risk adding unnecessary section-metadata that conflicts with block styling or makes authoring more complex.

**Sections with multiple sequences:** Always keep section-metadata (styling applies to all content, not validated in Step 3e)

---

**For EACH section with exactly one block, execute ALL these sub-steps:**

**Sub-step 1: Identify the candidate sections**

Review your Step 3 output. Find sections where:
- Section contains exactly 1 content sequence
- That sequence became a block (not default content)
- Section has distinct background styling from identify-page-structure

**Example:**
```
Section 1 (dark blue):
  - Sequence 1: Large centered heading, paragraph, two buttons
    → Decision: Hero block

Section 3 (grey):
  - Sequence 1: Tab navigation with three switchable panels
    → Decision: Tabs block
```

---

**Sub-step 2: For each candidate section, examine the screenshot**

Open screenshot.png and examine the section visually.

**Ask these questions:**

**Q1: Is the background an image (photo, gradient, illustration)?**
- If YES → Likely block-specific design
- If NO (solid color) → Continue to Q2

**Q2: Does the content fill the colored area edge-to-edge, or is there visible section padding?**
- Edge-to-edge (full-bleed) → Likely block-specific design
- Visible padding around content → Likely section container styling

**Q3: Does the block type typically have its own background styling?**
- Hero, banner, full-width CTAs → Often have own backgrounds
- Tabs, accordion, cards, columns → Often use section backgrounds

---

**Sub-step 3: Make the decision**

Based on your analysis, decide for each single-block section:

**SKIP section-metadata if:**
- Background is an image/gradient (block-specific)
- Content is full-bleed/edge-to-edge (no section padding visible)
- Block type typically has intrinsic background (hero, banner)

**KEEP section-metadata if:**
- Background is solid color with visible section padding
- Block type typically inherits section styling (tabs, cards, accordion)
- Styling clearly provides container context (not block design)

---

**Sub-step 4: Document your decisions**

For each validated section, note:
- Section number
- Block type
- Background analysis (image vs solid, full-bleed vs padded)
- Decision (keep or skip section-metadata)
- Reason

**Example output:**
```
VALIDATED SECTIONS:

Section 1 (dark blue):
  - Block: Hero
  - Background: Full-width dark blue gradient image
  - Layout: Edge-to-edge, no visible section padding
  - Decision: SKIP section-metadata
  - Reason: Background is hero's design, not section styling

Section 3 (grey):
  - Block: Tabs
  - Background: Solid grey (#f5f5f5)
  - Layout: Content centered with visible padding (~80px on sides)
  - Decision: KEEP section-metadata style="grey"
  - Reason: Section provides container styling for tabs block
```

---

**When in doubt:**

If you're uncertain whether background is block-specific or section-wide:
- **Default to KEEPING section-metadata** (safer, easier for authors to remove than add)
- **Add a note** in your documentation explaining the ambiguity
- Consider asking the user for guidance

---

**Step 3e Completion Checklist:**

Before proceeding to next skill, verify you have completed:
- ✅ Identified all single-block sections with background styling
- ✅ Examined original screenshot for EACH candidate section
- ✅ Answered Q1, Q2, Q3 for EACH candidate section
- ✅ Made skip/keep decision for EACH candidate section
- ✅ Documented reasoning for EACH decision
- ✅ Updated section styling notes with validated decisions

---

## Final Output

This skill provides complete authoring analysis:

**1. Authoring decisions for all sequences:**
- Each sequence marked as DEFAULT CONTENT or specific block name
- Reasoning documented

**2. Block structures fetched:**
- HTML structure examples for all blocks to be used

**3. Section styling validation (if applicable):**
- Updated section list with validated styling decisions
- Some sections may be marked "no section-metadata"

**Next step:** Pass these outputs to generate-import-html skill
