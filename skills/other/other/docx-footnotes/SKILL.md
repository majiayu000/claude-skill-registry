---
name: docx-footnotes
description: "Repair DOCX footnote damage from Google Docs or Word Online round-trips, and convert hardcoded supra/infra note references to auto-updating NOTEREF field codes. Use this skill whenever a user's .docx footnotes are broken after editing in a cloud editor — common symptoms include missing footnote separator lines, stripped paragraph styles (pStyle), author bio custom marks (*, †, ‡) replaced with numbers, footnote numbering starting at the wrong number, or TOC separator paragraphs that inflate to fill a whole page. Also use this skill when the user wants to convert 'supra note N' cross-references to NOTEREF fields, fix footnote numbering offsets caused by customMarkFollows bio footnotes, or perform any OOXML-level footnote surgery on a Word document. Even if the user doesn't mention OOXML or XML directly — if they describe footnote formatting problems in a .docx that was edited in Google Docs or Word Online, this is the right skill."
user-invocable: false
---

# DOCX Footnote Repair & Cross-References

Fix footnote formatting damage caused by Google Docs and Word Online, and convert hardcoded supra note references to NOTEREF field codes.

## Quick Start

Scripts are in this skill's `scripts/` directory. Use `$SKILL_DIR` below as a placeholder for the absolute path to this skill (the directory containing this SKILL.md).

```bash
# Fix all cloud editor damage + convert cross-references
pixi exec --spec python=3.13 --spec lxml -- python3 \
  "$SKILL_DIR/scripts/fix_gdocs_footnotes.py" path/to/file.docx --crossrefs

# Dry run (show what would change)
pixi exec --spec python=3.13 --spec lxml -- python3 \
  "$SKILL_DIR/scripts/fix_gdocs_footnotes.py" path/to/file.docx --dry-run

# Cross-references only
pixi exec --spec python=3.13 --spec lxml -- python3 \
  "$SKILL_DIR/scripts/create_crossrefs.py" --docx path/to/file.docx
```

## Scripts

### fix_gdocs_footnotes.py

Detects and repairs OOXML damage from Google Docs / Word Online round-trips. Idempotent.

**What it fixes:**
- Missing separator/continuation footnotes (id=-1, 0)
- Custom mark restoration for author bio footnotes (*, dagger, double-dagger)
- Footnote ID renumbering (shifted by missing system footnotes)
- Missing paragraph styles (adds configurable pStyle to all footnotes)
- TOC separator paragraph inflation (shrinks to near-zero height)

**Flags:**
- `--output` / `-o`: Output path (default: overwrite input)
- `--dry-run`: Show what would change without modifying
- `--bio-footnotes N`: Number of author bio footnotes (default: 3)
- `--crossrefs`: Chain to create_crossrefs.py after fixing
- `--fix-numbering`: Fix numbering offset from customMarkFollows bio footnotes (adds numRestart, updates NOTEREFs and supra references)

### create_crossrefs.py

Converts hardcoded "supra note N" references to NOTEREF field codes that auto-update.

**What it does:**
- Finds all `supra note <number>` patterns in document body and footnotes
- Creates bookmark targets on referenced footnotes
- Replaces hardcoded numbers with `NOTEREF _RefFN<id> \h` field codes
- Preserves italic formatting on "supra"

## Reference

See [`footnotes-reference.md`](footnotes-reference.md) for detailed technical reference covering:
1. Run-level editing gotchas (NBSP, cross-run matching, xml:space)
2. Cloud editor damage patterns (what gets destroyed and why)
3. Direct ZIP surgery patterns (bypassing Document libraries)

### Footnote Numbering Offset Fix

When author bio footnotes use `customMarkFollows` (*, †, ‡), they consume auto-numbers 1–3, causing body footnotes to start at 4. Fix by adding `numRestart=eachSect` to `settings.xml` and updating NOTEREF cached values.

**Requires:** A section break between title page and body. Must use **Word** (not LibreOffice) for PDF — LibreOffice renders numRestart as zeros.

See [`footnotes-reference.md`](footnotes-reference.md) § 4 for details, code patterns, and the critical rule: numRestart goes in `settings.xml` ONLY (not in sectPr — causes all-zeros).
