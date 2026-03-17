---
name: overfull-hbox
description: This skill provides guidance for fixing LaTeX overfull hbox warnings by making synonym substitutions. It should be used when the task involves resolving LaTeX line-breaking issues by replacing words with synonyms from an allowed list, particularly when the goal is to reduce line width without changing meaning.
---

# Overfull Hbox

## Overview

This skill guides the process of fixing LaTeX overfull hbox warnings by strategically replacing words with shorter synonyms from an allowed synonym list. Overfull hbox warnings occur when LaTeX cannot fit content within the specified line width, and fixing them requires understanding both LaTeX's typesetting behavior and systematic synonym substitution.

## When to Use This Skill

Use this skill when:
- A task involves fixing overfull hbox warnings in LaTeX documents
- Synonym substitutions are constrained to an allowed list (e.g., `synonyms.txt`)
- The goal is to reduce line width while preserving document meaning

## Workflow

### Phase 1: Complete Information Gathering

Before making any changes, gather all necessary information:

1. **Read the complete synonym file** - Never work with truncated synonym data. If the file is large, read it in sections to ensure all synonym families are captured.

2. **Compile the document once** to get the full list of overfull hbox warnings:
   ```bash
   pdflatex -interaction=nonstopmode document.tex 2>&1 | grep -E "Overfull|hbox"
   ```

3. **Parse warning details** - Extract:
   - Line numbers where overflows occur
   - Overflow amounts (in points)
   - The problematic text content

4. **Build a synonym lookup map** - Create a mental or explicit mapping of all words in the document that have shorter synonyms available.

### Phase 2: Strategic Planning

For each overfull hbox warning:

1. **Examine the exact line content** - Read the specific lines from the LaTeX source to understand what text is causing the overflow.

2. **Identify candidate words** - List all words on or near the problematic line that:
   - Exist in the synonym list
   - Have shorter synonym alternatives

3. **Verify synonyms explicitly** - Before planning any replacement, confirm:
   - The word appears in the synonym file
   - The proposed replacement is in the same synonym family
   - The replacement is actually shorter (or affects hyphenation favorably)

4. **Consider cascading effects** - Changing one line may affect subsequent line breaks. Plan changes that minimize ripple effects.

### Phase 3: Systematic Execution

1. **Make changes in batches by paragraph** - Group related changes together to minimize recompilation cycles.

2. **Prioritize high-impact changes** - Target words with the largest character count differences first.

3. **Track all changes** - Maintain a log of:
   - Original word
   - Replacement word
   - Reason for change
   - Whether it was verified against synonym list

4. **Recompile and verify** after each batch of changes.

### Phase 4: Verification

After changes:

1. **Confirm no new warnings** - Grep for "Overfull" in compilation output
2. **Check for introduced issues** - Verify no new overfull or underfull warnings appeared
3. **Validate semantic correctness** - Ensure replacements maintain intended meaning

## Critical Understanding: LaTeX Line Breaking

LaTeX line breaking is **not** simply about character count. Key factors include:

- **Hyphenation rules** - Some words hyphenate better than others at different points
- **Character width** - Letters like 'i', 'l', 't' are narrower than 'm', 'w'
- **Kerning** - Space between specific letter pairs varies
- **Word spacing** - LaTeX adjusts inter-word spacing within allowed limits
- **Penalties** - Hyphenation and line-break penalties affect where breaks occur

A word with the same character count may produce different line widths depending on:
- Its constituent letters
- Where it can be hyphenated
- How it interacts with surrounding words

## Common Pitfalls

### 1. Working with Incomplete Data

**Problem**: Reading only part of the synonym file leads to missing valid replacement options or using invalid replacements.

**Solution**: Always read the complete synonym file before making any changes. If truncated, explicitly request remaining content.

### 2. Unverified Synonym Assumptions

**Problem**: Assuming a word is a valid synonym without checking the allowed list.

**Solution**: Before every replacement, explicitly verify:
```
Original word: "elevated"
Proposed synonym: "high"
Verification: Check synonyms.txt for the family containing both words
```

### 3. Character Count Fallacy

**Problem**: Assuming shorter character count always means shorter rendered width.

**Solution**: Understand that "minimums" (8 chars) may render wider than "reductions" (10 chars) due to letter widths. Test empirically when character counts are close.

### 4. Cascade Blindness

**Problem**: Fixing one overfull hbox creates another by shifting line breaks.

**Solution**: After each change, recompile and check if new warnings appeared. Be prepared to roll back changes that create more problems than they solve.

### 5. Batch Verification Failure

**Problem**: Making multiple unverified changes at once makes it hard to identify which change caused issues.

**Solution**: Make changes in small, logical batches. If a batch introduces problems, bisect to find the problematic change.

### 6. No Rollback Strategy

**Problem**: Making changes without ability to revert when they worsen the situation.

**Solution**: Track all changes explicitly. Consider using version control or keeping original text in comments until verified.

## Verification Checklist

Before considering the task complete:

- [ ] All overfull hbox warnings are resolved (grep compilation output)
- [ ] No new overfull or underfull warnings introduced
- [ ] Every synonym replacement was verified against the allowed list
- [ ] Document compiles successfully
- [ ] Output PDF renders correctly

## Example Workflow

Given a document with overfull hbox on line 42:

```
1. Read synonyms.txt completely
2. Compile: pdflatex document.tex
3. Note: "Overfull \hbox (12.5pt too wide) in paragraph at lines 42--43"
4. Read lines 40-45 from document.tex
5. Identify words: "demonstration" (13 chars), "comprehensive" (13 chars)
6. Check synonyms.txt:
   - "demonstration" -> "example" (7 chars) - VALID
   - "comprehensive" -> "complete" (8 chars) - VALID
7. Replace "demonstration" with "example" (higher impact)
8. Recompile and verify
9. If warning persists, try additional replacements
10. Confirm no new warnings introduced
```

## Resources

For detailed reference on LaTeX typography and line-breaking algorithms, consult the `references/` directory if available.
