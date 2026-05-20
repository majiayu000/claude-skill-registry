---
name: bluebook-audit
description: "This skill should be used when the user asks to 'audit footnotes', 'check Bluebook formatting', 'audit citations', 'run footnote audit', 'check my footnotes', 'bluebook audit', or needs systematic Bluebook compliance checking of a law review manuscript."
user-invocable: false
---

# Bluebook Footnote Audit Workflow

Systematic Bluebook 21st edition compliance audit for law review manuscripts in DOCX format.

**Announce:** "Using bluebook-audit to run a systematic Bluebook compliance check."

## Overview

Seven-phase linear workflow: Extract -> Check -> Report -> Correct -> Verify -> Archive -> Cross-Refs

```
/bluebook-audit  -> extract -> check -> report -> [USER REVIEWS] -> correct -> verify -> archive -> crossrefs
/bluebook-audit-fix -> diagnose -> route to {re-check, re-correct, re-verify}
```

## Phase Summary

| Phase | Responsibility | Gate |
|-------|---------------|------|
| Extract | Parse DOCX -> structured JSON with formatting | `footnotes_data.json` exists, all FNs extracted |
| Check | Mechanical checks → Gemini Batch per-footnote → Claude cross-footnote review | `audit_findings.json` exists, ALL FNs covered, three-layer merge complete |
| Report | Present findings to user for review | `AUDIT_REPORT.md` exists, user acknowledges |
| Correct | Apply fixes to DOCX via lxml | Corrected DOCX exists, fix counts match |
| Verify | Re-scan to confirm fixes applied | Zero remaining issues in re-scan |
| Archive | perma.cc URL archiving | All URLs archived, links written to DOCX |
| Cross-Refs | Convert supra/infra notes to NOTEREF fields | All cross-refs are auto-updating fields |

## How to Start

1. User provides a DOCX file path
2. Workflow creates `scratch/` directory for intermediate artifacts
3. Proceeds through phases sequentially

## Next Step

Read the entry command:

```
Read("commands/bluebook-audit.md")  # relative to this skill's base directory
```

<EXTREMELY-IMPORTANT>
## Iron Law: ALL Footnotes Must Be Checked

**Every footnote in the document must be audited. No subsets. No sampling.**

Auditing only "major-severity" footnotes or a random sample guarantees missed errors. The formatted Gemini audit must cover ALL footnotes, not just previously flagged ones.

Skipping footnotes is NOT HELPFUL — missed errors go to publication and embarrass the user.
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## Iron Law: Formatted Text for Gemini Audit

**NEVER send plain text to Gemini for typeface auditing. Always include formatting markup.**

Plain text produces 10-20x false positives because Gemini cannot see what is already italic/small caps/roman. Inline markup (`*italic*`, `[SC]small caps[/SC]`) reduces false positives from ~400 to ~20 for a 239-footnote document.
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## Iron Law: Verify After Corrections

**After applying corrections, ALWAYS re-run the scanner to verify fixes were applied.**

NBSP characters, run boundaries, and cross-run text cause silent failures. A fix that "applied" in code may not have actually changed the DOCX. Re-scanning is mandatory.
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## Iron Law: Mechanical Findings Override Gemini

**Never drop a mechanical finding because Gemini didn't flag it.**

Deterministic checks (signal italic, terminal periods, Id. chains) are 100% reliable. Gemini misses ~30% of signal formatting issues because it focuses on citation-level analysis and lacks a dedicated signal-checking output field. During merge/dedup, mechanical findings are authoritative for their rule categories. Gemini adds value only for judgment calls (source type classification, abbreviation tables).

Previous failure: Gemini reported FN103 as having only typeface issues on article titles, completely missing that "See also" was not italicized — which the mechanical checker caught.
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## Iron Law: Source Type Classification Requires Human Review

**Gemini consistently misclassifies non-standard source types. Never auto-fix Gemini's typeface suggestions for SEC releases, executive orders, working papers, or regulatory materials.**

The hardest part of a Bluebook audit is determining the correct typeface for non-standard sources. Gemini defaults to "everything should be italic or small caps" but many source types are correctly roman:
- SEC releases/rules/concept releases → roman (regulatory material, Rule 14.6)
- Executive order titles → roman (Rule 14.7)
- Working paper series designations → roman (parenthetical)
- Company names in no-action letters → roman

The audit report MUST separate "verified fixes" (clear violations) from "judgment calls" (source type dependent) and include a "correct as-is" section documenting why Gemini's suggestions were rejected. See `references/audit-patterns.md` for the full source type reference table.

Previous failure: Gemini flagged 10+ items as needing italic/small caps that were actually correct as roman (SEC releases, exec orders, working paper designations). Without the source type reference table, these would have been incorrectly "fixed."
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## Rationalization Table

| Excuse | Reality | Do Instead |
|---|---|---|
| "Gemini already checked this phase" | Gemini hallucinates citation formats; its output requires human verification | Run the mechanical checker independently and merge results |
| "Sampling footnotes is good enough" | One wrong supra reference invalidates the reader's trust in ALL footnotes | Audit every footnote — no subsets, no sampling |
| "Re-scanning is redundant overhead" | Fixes in one phase create new errors in dependent phases | Re-run the scanner after every correction pass |
| "The document is short, I can eyeball it" | Eyeballing misses systematic errors that pattern-matching catches | Run all phases regardless of document length |
| "This footnote format is close enough" | Bluebook compliance is binary — close is wrong | Fix it to spec or flag it for human review |
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## Red Flags + STOP

- **"Skipping a phase because the document 'looks clean'"** → STOP. Every phase catches different error types.
- **"Trusting Gemini's output without spot-checking"** → STOP. Gemini fabricates citation details.
- **"Applying fixes without re-running the affected phase"** → STOP. Fixes cascade.
- **"Marking a footnote as correct without checking the reporter/volume"** → STOP. Surface-level review misses citation errors.
- **"Rushing the final verification because earlier phases were clean"** → STOP. Earlier phases being clean doesn't guarantee the fixes didn't introduce new errors.
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## Delete & Restart

**If you sent plain text to Gemini instead of formatted text with footnote markers, DELETE the results and START OVER with properly formatted input.** Gemini cannot audit what it cannot parse.
</EXTREMELY-IMPORTANT>

## Why Skipping Hurts the Thing You Care About Most

| Shortcut | Consequence |
|---|---|
| Skipping a phase because footnotes "looked fine" | You skipped the signal-word phase because footnotes "looked fine." Wrong supra references persist — your efficiency corrupted the document. |
| Not verifying fixes after applying them | You applied formatting fixes without re-checking. The fixes introduced new errors — your speed was destructive. |
