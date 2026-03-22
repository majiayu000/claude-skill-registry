---
name: audit-extract
description: "Phase 1: Extract footnotes from DOCX with formatting annotations"
---

# Phase 1: Extract Footnotes

Parse the DOCX file and build structured data for all subsequent phases.

## What This Phase Does

1. Parse `word/footnotes.xml` via lxml
2. Extract each footnote's runs with formatting flags (italic, small caps, bold)
3. Parse `word/_rels/footnotes.xml.rels` for hyperlink URLs
4. Build citation registry (hereinafter definitions, author-to-first-cite mapping)
5. Resolve cross-references (`supra note [_]` placeholders)
6. Extract all URLs for archiving inventory

## Script

```bash
BB_SCRIPTS=$(${CLAUDE_PLUGIN_ROOT}/skills/bluebook-audit/scripts) && python3 "$BB_SCRIPTS/extract_footnotes.py" --docx <path>
```

Output: `scratch/footnotes_data.json`

## Gate: Exit Extract

Before proceeding to Check phase:
- [ ] `scratch/footnotes_data.json` exists
- [ ] Contains entries for ALL footnotes in the document (verify count)
- [ ] Each entry has `formatted_text` field with inline markup
- [ ] Citation registry has hereinafter definitions
- [ ] URL inventory extracted

**If footnote count doesn't match document:** STOP. Investigate missing footnotes before proceeding.

## Next Phase

Read `${CLAUDE_PLUGIN_ROOT}/skills/bluebook-audit/skills/audit-check/SKILL.md` and follow its instructions.
