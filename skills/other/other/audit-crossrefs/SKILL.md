---
name: audit-crossrefs
description: "Phase 7: Convert hardcoded cross-references to auto-updating NOTEREF fields"
---

# Phase 7: Cross-References

Convert hardcoded supra/infra note numbers to NOTEREF field codes that auto-update when footnotes are renumbered.

## What This Phase Does

1. Scan footnotes for `supra note N` and `infra note N` patterns
2. Add bookmarks to target footnoteReferences in document.xml
3. Replace hardcoded numbers with NOTEREF field codes
4. Preserve existing NOTEREFs and bookmarks

## Script

```bash
BB_SCRIPTS=$(${CLAUDE_PLUGIN_ROOT}/skills/bluebook-audit/scripts)

# Preview changes
python3 "$BB_SCRIPTS/create_crossrefs.py" --docx <path> --dry-run

# Apply (creates .bak backup)
python3 "$BB_SCRIPTS/create_crossrefs.py" --docx <path>
```

## Workflow

1. **Dry run first** — review the cross-reference map and bookmark plan
2. **Apply** — the script backs up the original before writing
3. **Verify in Word** — open the DOCX, press Ctrl+A then F9 to update all fields
4. **Spot-check** — confirm 5-10 supra references display the correct numbers
5. **Renumber test** (optional) — add a footnote before a referenced target and confirm the supra numbers update

## What Gets Converted

| Pattern | Example | Result |
|---------|---------|--------|
| Single supra | `supra note 42` | NOTEREF to FN42 bookmark |
| Single infra | `infra note 188` | NOTEREF to FN188 bookmark |
| Range | `infra notes 209-210` | Two NOTEREFs with separator |
| With pincite | `supra note 42, at 15` | NOTEREF + roman `, at 15` |
| Existing NOTEREF | (already converted) | Skipped |

## What Is NOT Converted (Phase 2 — Future)

- Part/Section references (`supra Section I.A.`, `infra Part III`)
- These require a heading-to-bookmark mapping strategy since heading numbering is partially auto-generated

## Gate: Exit Cross-References

- [ ] Dry run reviewed — cross-reference map is correct
- [ ] NOTEREF fields created for all supra/infra note references
- [ ] Backup DOCX exists
- [ ] Word field update (Ctrl+A, F9) confirms correct numbers

## Workflow Complete

Present final summary to user:
- Total formatting corrections applied (from Phase 4)
- Total URLs archived (from Phase 6)
- Total NOTEREF fields created (from Phase 7)
- Final DOCX file path
