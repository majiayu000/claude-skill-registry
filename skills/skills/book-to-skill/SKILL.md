---
name: book-to-skill
description: Converts .txt book files into leverageable Claude Code skills. Use when transforming books, articles, or written expertise into structured skills with frameworks, workflows, and reference material.
---

# Book to Skill Converter

Transform written knowledge into actionable Claude Code skills.

## Philosophy

I transform books into actionable skills by extracting their crystallized expertise—frameworks, principles, and techniques—into a format I can leverage repeatedly.

**I extract structure, not summaries.** A skill isn't a book report. It's a toolkit of:
- Named frameworks (mental models with clear application)
- Actionable principles (rules that guide decisions)
- Techniques (step-by-step methods)
- Anti-patterns (what to avoid and why)
- Voice calibration (how the author thinks and communicates)

**I preserve the author's precision.** Frameworks often have specific names and structures for reasons. "The 5 Whys" isn't interchangeable with "ask why multiple times." I capture the exact formulation.

**I optimize for invocation.** The generated skill should be immediately useful. When someone invokes `/author-method`, they should get actionable guidance, not philosophy.

**I layer depth appropriately.** Simple books → simple skills. Complex books with 10+ frameworks → router skills with reference files.

## Supported Formats

**Primary:** `.txt` files work directly with this skill.

**Requires conversion:** epub, pdf, mobi, docx

Before analyzing books in other formats, convert them to .txt:

```bash
# EPUB → TXT
ebook-convert book.epub book.txt

# PDF → TXT
pdftotext book.pdf book.txt
```

See [workflows/convert-formats.md](workflows/convert-formats.md) for full instructions and dependencies.

## How to Start

Three paths available:

### 1. Full Conversion (Default)
**Trigger:** User provides a `.txt` book file
**Action:** Route to [workflows/convert-book.md](workflows/convert-book.md)
**Output:** Complete skill with all files

### 2. Analysis Only
**Trigger:** User says "analyze" or "just extract" or wants to review before generating
**Action:** Route to [workflows/analyze-book.md](workflows/analyze-book.md)
**Output:** Structured extraction report (no skill generated)

### 3. Generate from Prior Analysis
**Trigger:** User has existing analysis notes or previously ran analyze-only
**Action:** Route to [workflows/generate-skill.md](workflows/generate-skill.md)
**Output:** Skill files from provided analysis

## Routing Logic

```
IF user provides non-.txt file (epub, pdf, mobi, docx):
  → Point to workflows/convert-formats.md first

IF user provides .txt book file path:
  IF "analyze only" or "just analyze" in request:
    → workflows/analyze-book.md
  ELSE:
    → workflows/convert-book.md

IF user mentions "generate" or "create skill" with analysis notes:
  → workflows/generate-skill.md

IF unclear:
  Ask: "Do you want to:
  1. Convert a book to a skill (provide .txt path)
  2. Analyze a book without generating (provide .txt path)
  3. Generate a skill from existing analysis"
```

For extraction categories, see [references/extraction-patterns.md](references/extraction-patterns.md).
For output structure patterns, see [references/skill-patterns.md](references/skill-patterns.md).

## Questions to Ask

Use AskUserQuestion tool for each of these:

1. **Purpose** (before analysis):
   - Question: "What should this skill help you do?"
   - Options: Write like the author | Apply their frameworks | Think with their mental models | Build using their approach | All of the above

2. **Skill Name** (after analysis):
   - Question: "What should this skill be named?"
   - Propose `{author-lastname}-{core-concept}` format
   - Examples: `cialdini-influence`, `meadows-systems`, `kahneman-decisions`

3. **Scope** (after extraction):
   - Present extracted elements summary
   - Question: "Which elements should I include in the skill?"
   - Options: All extracted content | Specific frameworks only | Let me specify

4. **Reference Depth**:
   - Question: "How comprehensive should the reference material be?"
   - Options: Essential only (key frameworks) | Comprehensive (all frameworks + principles) | Exhaustive (everything extracted)
