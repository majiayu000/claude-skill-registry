---
name: improve-guide
description: Main entry point for guide improvement - interactive workflow selection for audit, translation, or both
---

# Guide Improvement (Interactive Workflow Selector)

## Description

Main entry point for guide improvement with **interactive workflow selection**. Presents user with choice of:
1. **Audit EN content only** - Fix EN issues, stop before translation for manual review
2. **Translate to all locales** - Propagate EN content (assumes EN is already clean)
3. **Audit + Translate (full workflow)** - Both phases with no manual review between

This flexibility allows manual review of EN content before propagating to 17 locales.

---

## Interactive Workflow Selection

When this skill is invoked, it **first asks the user which workflow to run** before any processing begins.

**Why this matters:**
- EN content changes affect all 17 locales
- Manual review between audit and translation catches issues early
- Some users want to iterate on EN before translating
- Some users want the full automated workflow

---

## When to Use

**Use this skill as the main entry point** for all guide improvement work. The interactive selection lets you choose the right workflow for your situation.

**Direct sub-skill invocation (skip selection prompt):**
- Use `improve-en-guide` directly if you always want EN-only processing
- Use `improve-translate-guide` directly if EN is already clean and you just need translation

---

## When NOT to Use

This skill orchestrates sub-skills. If you need fine-grained control over specific phases or want to skip the selection prompt entirely, invoke the sub-skills directly:

- **`improve-en-guide`** - EN audit and fixes only
- **`improve-translate-guide`** - Translation only (requires clean EN)

---

## Inputs

### Required

**Guide reference (one of):**
- Full URL (preferred), e.g. `http://localhost:3012/en/experiences/gavitella-beach-guide`
- Slug, e.g. `gavitella-beach-guide`
- guideKey, e.g. `gavitellaBeachGuide`
- List of URLs/slugs/guideKeys for batch processing

### Optional Flags

All flags are passed through to the appropriate sub-skill:

- `--skip-json-fix` - Skip baseline JSON validation/fixing (passed to improve-en-guide)
- `--skip-validation` - Skip EN audit validation in translation phase (NOT RECOMMENDED, passed to improve-translate-guide)

### Optional (but recommended)

- Readership/audience (passed to improve-en-guide)
- Tone constraints + must-include details

---

## Workflow

### Step 1: Ask User for Workflow Selection

**Use AskUserQuestion tool** with:

- **Question:** "Which workflow do you want to run for this guide?"
- **Header:** "Workflow Selection"
- **Options:**
  1. **"Audit EN content only"** - Run SEO audit and fix EN content issues. Stops before translation so you can review/adjust EN content manually.
  2. **"Translate to all locales"** - Propagate EN content to all 17 locales (assumes EN is already audit-clean and reviewed).
  3. **"Audit + Translate (full workflow)"** - Run EN audit/fixes, then immediately translate to all locales (no manual review between phases).

### Step 2: Execute Selected Workflow

**If user selects "Audit EN content only":**
1. Invoke `improve-en-guide` skill with guide reference and any flags
2. Report EN audit results
3. STOP - Provide guidance: "EN content is now audit-clean. Review the changes, make any manual adjustments, then run /improve-guide again and select 'Translate to all locales'."

**If user selects "Translate to all locales":**
1. Invoke `improve-translate-guide` skill with guide reference and any flags
2. Report translation results for all 17 locales

**If user selects "Audit + Translate (full workflow)":**
1. Invoke `improve-en-guide` skill with guide reference and any flags
2. **Gate:** Phase 1 must complete successfully before Phase 2 begins
3. If Phase 1 fails: Report failure, STOP, provide guidance
4. Invoke `improve-translate-guide` skill with guide reference and any flags
5. Report combined results from both phases

### Step 3: Report Results

Report results based on selected workflow (see Completion Report section).

---

## Typical Usage Pattern

Most common workflow for careful iteration:

1. Run `/improve-guide` and select **"Audit EN content only"**
2. Review the EN content fixes made by the audit
3. Make any manual adjustments to EN content
4. Run `/improve-guide` again and select **"Translate to all locales"**

This pattern ensures EN content is reviewed before propagating to 17 locales.

**For quick end-to-end processing** (no manual review):
- Run `/improve-guide` and select **"Audit + Translate (full workflow)"**

---

## Completion Report

### If "Audit EN content only" was selected:

**Phase 1 Summary (EN Fixes)**
- Initial score, final score
- Audit iterations performed
- Key issue categories fixed
- Reader-first improvements made

**Next Steps Guidance:**
- Review EN changes at the guide URL
- Make any manual adjustments
- Run `/improve-guide` again and select "Translate to all locales"

### If "Translate to all locales" was selected:

**Translation Summary**
- Locales updated (should be all 17)
- Any locale-specific issues encountered
- Parallel translation efficiency

### If "Audit + Translate (full workflow)" was selected:

**Phase 1 Summary (EN Fixes)**
- Initial score, final score
- Audit iterations performed
- Key issue categories fixed
- Reader-first improvements made

**Phase 2 Summary (Translation)**
- Locales updated (should be all 17)
- Any locale-specific issues encountered
- Parallel translation efficiency

**Overall**
- Total guides processed
- Any guides/locales skipped (with reasons)
- Confirmation that:
  - Every write was validated immediately
  - Any corruption was handled only by replacement with known-good content
  - All 17 non-EN locales were successfully updated via parallel subagents
  - No translation work was deferred or suggested for external handling

---

## Core Commitments (Inherited from Sub-Skills)

**Every write is validated immediately.**
After each file write, validate JSON parseability and token integrity before doing anything else.

**Readership-first ordering is required.**
Reorder EN content so the reader can decide/act quickly, with explicit early-content gates.

**Localization must not assume sync.**
Non-EN locale content may have drifted. Check and reconcile entire locale content.

**Translation Policy (Non-Negotiable):**
- Always complete all translation work in-house
- Always use parallel subagents for localization
- Never defer or skip localization

---

## Error Handling

**Phase 1 failure (EN audit):**
- Report specific EN audit issues
- STOP before translation
- User can fix manually and re-run, or use improve-en-guide directly

**Phase 2 failure (translation):**
- Report which locales failed
- Translation for successful locales is preserved
- User can re-run improve-translate-guide for failed locales

---

## Quality Gates (Combined)

**EN (from Phase 1):**
1. Final audit score >= 9.0
2. Zero critical issues
3. Zero improvements remaining
4. EN JSON valid + tokens preserved

**Translation (from Phase 2):**
5. All 17 locale JSONs valid
6. Tokens preserved correctly in all locales
7. Structure parity vs EN in all locales
8. Drift addressed comprehensively

---

## Sub-Skill References

For detailed documentation on each phase:

- **Phase 1:** See `.claude/skills/improve-en-guide/SKILL.md`
- **Phase 2:** See `.claude/skills/improve-translate-guide/SKILL.md`
