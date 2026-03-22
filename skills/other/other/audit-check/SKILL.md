---
name: audit-check
description: "Phase 2: Run mechanical checks and Gemini formatted audit"
---

# Phase 2: Check (Mechanical + AI Audit)

Two-stage checking: Python mechanical checks catch definite errors; Gemini batch audit catches judgment-call issues.

## Stage 2a: Mechanical Checks (Python)

```bash
BB_SCRIPTS=$(${CLAUDE_PLUGIN_ROOT}/skills/bluebook-audit/scripts) && python3 "$BB_SCRIPTS/scan_formatting.py" --docx path/to/file.docx
```

Checks performed on ALL footnotes:
1. **Journal name small caps** - Comprehensive pattern list (law reviews, finance journals, newspapers, periodicals, forums)
2. **Book title small caps** - Detect italic book titles that should be small caps
3. **Id. chain validation** - Rule 4.1 mechanical check (single-source predecessor)
4. **Signal italic consistency** - All signals (see, cf., e.g.) must be italic
5. **Terminal period** - Every footnote must end with a period
6. **Hereinafter consistency** - Defined at first citation, used consistently after
7. **Author name supra format** - Text before `*supra*` should be roman, not italic (unless it's a case name short form). Catches `*Manne, supra*` → should be `Manne, *supra*`
8. **Italic spillover** - Trailing/leading spaces inside italic or small caps runs (e.g., `*supra *` should be `*supra* `). These don't affect Word display but cause Gemini misparses

### NBSP Handling

DOCX uses non-breaking spaces (`\xa0`) in abbreviations. ALL search functions must handle both `\x20` and `\xa0`:
- `No.\xa02106`, `Feb.\xa07`, `Oct.\xa021`
- `Wall St.\xa0J.`, `Corp.\xa0Governance`

## Stage 2b: Gemini Batch Formatted Audit

**Default: Use Gemini Batch API** (50% cheaper, handles all footnotes in one job). Fallback to sync calls if batch is unavailable.

### Step 1: Extract formatted footnotes

```bash
BB_SCRIPTS=$(${CLAUDE_PLUGIN_ROOT}/skills/bluebook-audit/scripts) && python3 "$BB_SCRIPTS/gemini_audit.py" --docx path/to/file.docx --extract-only
```

This outputs a JSON file mapping footnote numbers to formatted text with inline markup:
- `*text*` = italic
- `[SC]text[/SC]` = small caps
- Plain text = roman

### Step 2: Submit Gemini Batch Job

Build a JSONL file with one request per footnote, then submit via Batch API:

```python
# Build JSONL (one line per footnote)
for fn_num, formatted_text in footnotes.items():
    request = {
        "custom_id": f"fn-{fn_num}",
        "body": {
            "contents": [{"parts": [{"text": PROMPT.format(fn_num=fn_num, formatted_text=formatted_text)}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1}
        }
    }

# Submit batch job (see /gemini-batch skill for full pattern)
# Use examples/batch_processor.py pattern — DO NOT guess API parameters
```

**IMPORTANT:** Follow the `/gemini-batch` skill's Iron Law — read `examples/batch_processor.py` before writing batch code.

**Fallback (sync):** If batch is unavailable, use:
```bash
BB_SCRIPTS=$(${CLAUDE_PLUGIN_ROOT}/skills/bluebook-audit/scripts) && python3 "$BB_SCRIPTS/gemini_audit.py" --docx path/to/file.docx
```

### Gemini Prompt Focuses On:
- Source type classification (case, statute, article, book, newspaper, working paper, hearing, letter, regulation)
- Typeface correctness per Rule 2 (italic vs small caps vs roman)
- Abbreviation correctness per T6/T13
- Short form validity (cases must not use supra)

<EXTREMELY-IMPORTANT>
## Iron Law: Audit ALL Footnotes

The Gemini audit MUST cover every footnote, not a subset. Auditing only "major" or "flagged" footnotes guarantees missed errors.

Previous failure: Auditing 45 of 239 footnotes missed 41 journal names needing small caps.
</EXTREMELY-IMPORTANT>

## Stage 2c: Claude Cross-Footnote Review

**Never trust a single agent.** After Gemini's per-footnote audit, Claude reviews the full set for cross-footnote patterns that per-footnote analysis misses.

Claude receives:
1. ALL formatted footnotes (fits in 1M context at ~20-40K tokens)
2. Gemini's per-footnote findings
3. Mechanical check results

**Claude reviews for:**
- **Supra chain validity** — does `supra note 42` actually point to the right source?
- **Hereinafter consistency** — defined at first citation? Used consistently after?
- **Repeated source type errors** — if Gemini misclassified one SEC release, it likely missed them all
- **Id. chain context** — predecessor footnote analysis that per-footnote Gemini can't see
- **Gemini false positive filtering** — flag Gemini suggestions that are likely wrong (SEC releases, exec orders, working papers)

**Output:** Annotated version of Gemini findings with cross-footnote issues added and false positives flagged.

## Red Flags - STOP If You Catch Yourself:

| Action | Why Wrong | Do Instead |
|---|---|---|
| Sending plain text to Gemini | 10-20x false positives without formatting info | Always include inline markup |
| Auditing a subset of footnotes | Missed errors guaranteed | Audit ALL footnotes |
| Skipping NBSP variants in mechanical checks | Silent search failures | Always try both space types |
| Trusting Gemini results without Claude cross-check | Per-footnote misses cross-footnote patterns | Always run Stage 2c |
| Trusting Claude review without mechanical checks | Claude misses deterministic patterns | Mechanical checks are authoritative for their categories |
| Skipping any stage | Each stage catches different error classes | Run all three: mechanical → Gemini → Claude |

## Merging Three-Layer Findings

**Priority order: Mechanical > Claude cross-review > Gemini per-footnote**

Mechanical checks are authoritative for deterministic rules:
- Signal italic formatting → trust mechanical checker (regex on run-level XML)
- Terminal periods → trust mechanical checker
- Id. chain validation → trust mechanical checker
- Journal/book small caps patterns → trust mechanical checker

Claude cross-review is authoritative for:
- Cross-footnote consistency (supra chains, hereinafter definitions)
- Gemini false positive filtering (source type misclassifications)
- Patterns across footnotes that per-footnote analysis misses

Gemini per-footnote is authoritative for:
- Individual source type classification (when not overridden by Claude)
- Abbreviation correctness (T6/T13 tables)
- Short form validity

**Never drop a mechanical finding because Gemini or Claude didn't flag it.** The mechanical checker catches 100% of signal issues by design.

## Gate: Exit Check

Before proceeding to Report phase:
- [ ] `scratch/audit_findings.json` exists
- [ ] Mechanical check results cover ALL footnotes
- [ ] Gemini audit results cover ALL footnotes (verify count matches extract)
- [ ] Claude cross-footnote review complete
- [ ] Findings merged (mechanical > Claude > Gemini priority)

## Next Phase

Read `${CLAUDE_PLUGIN_ROOT}/skills/bluebook-audit/skills/audit-report/SKILL.md` and follow its instructions.
