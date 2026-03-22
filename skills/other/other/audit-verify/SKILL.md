---
name: audit-verify
description: "Phase 5: Verify all corrections were applied correctly"
---

# Phase 5: Verify

Re-scan the corrected DOCX to confirm all fixes were applied and no new issues were introduced.

## What This Phase Does

1. Re-extract all footnotes from the corrected DOCX
2. Re-run mechanical checks (small caps scanner, signal checker, etc.)
3. Compare findings against the original audit - all flagged issues should now be clean
4. Report any remaining issues

## Verification Checks

1. **Formatting scanner**: Re-run `scan_formatting.py --docx corrected.docx` - expect 0 findings (or only known false positives like "Institutional Investors" in titles)
2. **Cross-reference check**: All `[_]` placeholders should be resolved
3. **Signal formatting**: All signals should be italic
4. **Terminal periods**: All footnotes should end with periods
5. **Id. chains**: All id. references should have single-source predecessors
6. **Gemini re-audit on fixed footnotes**: Re-run `gemini_audit.py --subset [all previously flagged FNs]` to catch issues introduced by fixes or missed in the initial pass

### Re-Scan Catches Real Issues

In the "Other People's Votes" audit, the Gemini re-scan on fixed footnotes caught a Wells Fargo press release title (FN206) that wasn't in the original "judgment call" list — it was in the same footnote as other fixes but wasn't flagged initially. The verify phase is not ceremonial; it finds real issues.

<EXTREMELY-IMPORTANT>
## Iron Law: Re-Scan Is Not Optional

The verify phase MUST re-run the scanner on the corrected DOCX. Skipping verification was the root cause of missing 41 small caps fixes in the original audit.

If the re-scan finds issues, go back to Correct phase. Do NOT proceed to Archive with unresolved issues.
</EXTREMELY-IMPORTANT>

## Red Flags - STOP If You Catch Yourself:

| Action | Why Wrong | Do Instead |
|---|---|---|
| Skipping re-scan because "all fixes applied" | Silent failures are common | Run the scanner |
| Dismissing remaining findings as false positives | Some "false positives" are real | Investigate each one |
| Proceeding to Archive with >0 real issues | Uncorrected issues persist forever | Fix them first |

## Gate: Exit Verify

Before proceeding to Archive phase:
- [ ] Re-scan completed on corrected DOCX
- [ ] Zero remaining issues (or all remaining are confirmed false positives)
- [ ] If issues found: returned to Correct phase and re-verified

## Next Phase

Read `${CLAUDE_PLUGIN_ROOT}/skills/bluebook-audit/skills/audit-archive/SKILL.md` and follow its instructions.
