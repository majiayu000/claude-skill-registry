---
name: improve-translate-guide
description: Propagate updated EN guide content to all locales using parallel translation. Requires EN audit to be clean first.
---

# Guide Translation/Propagation (Parallel, Drift-Aware, Locale-Safe)

## Scope

**This skill handles translation/propagation only.**

- First validates that EN content passes all SEO audits (FAIL if issues remain)
- Propagates updated EN content to all 17 non-EN locales using parallel translation
- Uses parallel subagents for concurrent translation (required in Claude; Codex runs sequentially)
- Validates translations after propagation

**Prerequisite:** Run `improve-en-guide` first to ensure EN content is audit-clean.

## Core Commitments (Non-Negotiable)

**EN must be clean before translating.**
The skill validates EN audit status before any translation work. If EN has unresolved issues, the skill FAILS immediately with guidance to run `improve-en-guide` first.

**Every write is validated immediately.**
After each locale file write, validate JSON parseability, token integrity, and structure parity before doing anything else.

If validation fails, the only allowed fix is replacement with known-good content.

**Localization must not assume sync.**
Non-EN locale content may have drifted. You must check and reconcile the entire locale content, not only the strings changed in EN.

**Translation Policy (Non-Negotiable):**
- **Always complete all translation work in-house.** Never ask about engaging professional translators or offloading translation work to external services.
- **Claude:** Always use parallel subagents for localization. Spawn multiple Task tool subagents to translate locales concurrently, maximizing speed.
- **Codex:** Run locales sequentially (Task tool may be unavailable). This is the approved exception.
- **Never defer or skip localization.** All 17 non-EN locales must be updated for every guide processed.

---

## Operating Mode

**VALIDATE EN + PARALLEL TRANSLATE (DRIFT-AWARE) + VALIDATE EACH LOCALE WRITE + REPORT**

---

## Allowed

- Run `apps/brikette/scripts/audit-guide-seo.ts` to validate EN is clean
- Read EN guide JSON to use as source for translation
- Read/modify non-EN locale guide JSON files:
  - `apps/brikette/src/locales/{locale}/guides/content/{guideKey}.json`
- **Spawn parallel Task tool subagents for concurrent locale translation** (required for all localization work)
- Translate content naturally while preserving tokens exactly

---

## Not Allowed

- **Modifying EN content** (use improve-en-guide for that)
- Third-party SEO tools/APIs
- Changing link targets in localization (only translate visible anchor text)
- Translating or altering any "preserve exactly" tokens
- Deferring validation/fixing "until later"
- Any remediation for corrupted JSON other than replacement with known-good content
- **Asking about professional translators or external translation services** (forbidden)
- **Suggesting to defer/skip localization or offload translation work** (forbidden)
- **Claude:** Sequential locale processing when parallel is possible (forbidden - always use Task tool for parallel translation)

---

## Inputs

### Required

**Guide reference (one of):**
- Full URL, e.g. `http://localhost:3012/en/experiences/gavitella-beach-guide`
- Slug, e.g. `gavitella-beach-guide`
- guideKey, e.g. `gavitellaBeachGuide`
- List of URLs/slugs/guideKeys for batch processing

### Optional Flags

- `--skip-validation` - Bypass EN audit check (NOT RECOMMENDED - may propagate broken content)

---

## Target Locales

All 17 non-EN locales must be updated:

`ar, da, de, es, fr, hi, hu, it, ja, ko, no, pl, pt, ru, sv, vi, zh`

---

## Workflow (Structure-First, Translate-Second)

**Critical pattern:** Never let agents perform structural repair and translation simultaneously. Structure is fixed by script (Phase 1), then agents translate text only (Phase 2). This prevents agents from creating condensed summaries instead of faithful translations.

**Evidence:** Batch 1-2 (agent-only) = 0% success; Batch 3 (structure-first) = 100% success.

### Phase 0: Preparation

**A. Validate EN is audit-clean (mandatory unless --skip-validation)**

Run:
```bash
pnpm --filter brikette tsx scripts/audit-guide-seo.ts {guideKey}
```

Check: score >= 9.0, zero critical issues, zero improvements.

**If EN audit fails:**
- STOP with message: "EN content has unresolved audit issues. Run improve-en-guide first."
- Do NOT proceed.

**B. List expected locale file paths**

For each guideKey, confirm paths exist or will be created:
```
apps/brikette/src/locales/{locale}/guides/content/{guideKey}.json
```
for all 17 locales: ar, da, de, es, fr, hi, hu, it, ja, ko, no, pl, pt, ru, sv, vi, zh

**C. Confirm Python runtime available** (required for structural repair)

### Phase 1: Structural Repair (Script, Not Agents)

Restore EN structure in all locale files before any translation work. This guarantees correct section counts, IDs, and array shapes.

**Run a Python structural repair script** for each target guideKey. The script:
1. Deep-copies EN structure
2. Preserves existing locale translations by section ID match
3. Writes fixed locale file

**Structural repair template:**
```python
import json
from pathlib import Path

LOCALES = ['ar','da','de','es','fr','hi','hu','it','ja','ko','no','pl','pt','ru','sv','vi','zh']

def fix_guide(guide_key):
    en_path = Path(f"src/locales/en/guides/content/{guide_key}.json")
    en_data = json.loads(en_path.read_text())

    for locale in LOCALES:
        locale_path = Path(f"src/locales/{locale}/guides/content/{guide_key}.json")
        if not locale_path.exists():
            # New locale file: use EN wholesale (will be translated in Phase 2)
            locale_path.write_text(json.dumps(en_data, ensure_ascii=False, indent=2) + "\n")
            continue

        locale_data = json.loads(locale_path.read_text())
        fixed = json.loads(json.dumps(en_data))  # deep copy EN structure

        # Preserve locale translations (merge policy)
        for field in ["seo", "linkLabel", "intro", "lastUpdated"]:
            if field in locale_data:
                fixed[field] = locale_data[field]

        # Match sections by ID, preserve locale text
        if "sections" in locale_data:
            by_id = {s.get("id"): s for s in locale_data["sections"]}
            for i, section in enumerate(fixed.get("sections", [])):
                if section["id"] in by_id:
                    src = by_id[section["id"]]
                    for key in ["title", "body", "list", "images"]:
                        if key in src:
                            fixed["sections"][i][key] = src[key]

        # Preserve other translated fields
        for field in ["toc","images","essentialsTitle","essentials","typicalCostsTitle",
                       "typicalCosts","tipsTitle","tips","warningsTitle","warnings",
                       "faqsTitle","faqs","fallback"]:
            if field in locale_data:
                fixed[field] = locale_data[field]

        locale_path.write_text(json.dumps(fixed, ensure_ascii=False, indent=2) + "\n")
```

**Merge policy:**
- **Preserve locale text for:** seo.title, seo.description, linkLabel, intro[], each section's title, body[], images[].alt, images[].caption, FAQ answers, tips[]
- **Force EN structure for:** section ordering, section IDs, required keys, array shapes (number of sections, number of FAQs)
- **ID matching:** Match sections by `id` field. If locale section has ID not in EN, discard it. If EN section has no locale match, keep EN text (translated in Phase 2).
- **Fallback:** If locale has no `sections` array, use EN content wholesale — fully translated in Phase 2.
- **Safety:** Never silently delete locale-only top-level keys. Log a warning if locale has keys not in EN.

### Gate 1: Structural Validation (Mandatory — Do NOT Skip)

After structural repair, validate all 17 locales pass structural checks:

```bash
cd apps/brikette && bash scripts/validate-guide-structure.sh {guideKey}
```

**Gate 1 checks:**
- File parses as valid JSON
- `sections.length` exactly matches EN
- All section IDs match EN (same IDs, same order)
- Required top-level keys present (seo, linkLabel, intro, sections)
- `faqs.length`, `tips.length` match EN (if present in EN)

**If Gate 1 fails:**
- **Do NOT proceed to Phase 2.**
- Fix failing locales (re-run structural repair with corrections).
- Re-run Gate 1 until all 17 locales pass.

### Phase 2: Translation (Agents — Translation Only)

Spawn parallel agents for translation-only work. **Agents MUST NOT make structural edits — only translate text within the existing structure.**

**Recommended parallelization (proven for 17 locales):**
- Agent 1: ar, da, de, es (4 locales)
- Agent 2: fr, hi, hu, it (4 locales)
- Agent 3: ja, ko, no, pl, pt (5 locales)
- Agent 4: ru, sv, vi, zh (4 locales)

**Launch pattern:** Single message with 4 Task tool calls.

**Timing:** ~40 minutes with 4 parallel agents.

**Per-locale translation workflow (each subagent executes):**

**A. Read existing locale file** (structure already correct from Phase 1)

**B. Translate text fields only:**
- Translate: seo.title, seo.description, linkLabel, intro[], section titles, section body[], FAQ questions/answers, tips[], image alt/caption
- Preserve tokens exactly: `%LINK:target|anchor%` → translate anchor only, `%IMAGE:path%` unchanged
- Keep link targets unchanged
- Do NOT add, remove, or reorder sections, FAQs, tips, or body elements

**C. Write locale file and validate immediately:**
- JSON parse check
- Token target preservation (targets before `|` must match EN)
- Structure parity vs EN (section count, IDs, body array lengths)

**D. If validation fails:**
- Restore from git or pre-edit snapshot immediately
- Redo translation safely
- If still failing, stop and ask user

### Gate 2: Translation Validation (Mandatory — Do NOT Skip)

After all translation agents complete, run both validations:

**A. Structural + translation validation:**
```bash
cd apps/brikette && bash scripts/validate-guide-structure.sh --phase2 {guideKey}
```

**Gate 2 checks (in addition to Gate 1 structural checks):**
- Per-section `body` array length equals EN body array length (anti-condensation)
- All token targets preserved (LINK, HOWTO, URL, IMAGE targets match EN)
- No empty strings in translated fields where EN is non-empty

**B. Full i18n parity audit (strict mode):**
```bash
cd apps/brikette && CONTENT_READINESS_MODE=fail pnpm test i18n-parity-quality-audit
```

**If Gate 2 fails:**
- DO NOT report completion
- Identify failing locales and failure type:
  - **Structural regression** (wrong section count/IDs) → re-run Phase 1 structural repair, then re-translate
  - **Bad translation** (empty strings, missing tokens, condensed body) → re-translate specific locale
- Re-run Gate 2 until all locales pass

### Phase 3: Completion Report (Mandatory)

After all gates pass, compile the completion report with persistence evidence.

**Required evidence (all 4 items mandatory):**

**1. Validation output:**
- Gate 1 result (all locales pass structural checks)
- Gate 2 result (all locales pass translation + parity audit)
- Section counts per locale

**2. Persistence verification:**
```bash
git diff --stat
```
Must show changed files for all target locales (non-zero diff per locale).

**3. Existence checks:**
Confirm all expected locale files exist:
```bash
for locale in ar da de es fr hi hu it ja ko no pl pt ru sv vi zh; do
  file="src/locales/$locale/guides/content/{guideKey}.json"
  [ -f "$file" ] && echo "OK $locale" || echo "MISSING $locale"
done
```

**4. Failure list:**
- List any locales that failed during the process and remediation steps taken
- Or "None — all locales passed on first attempt"

**Translation summary:**
- Locales updated (count + list)
- Parallel translation efficiency (number of subagents spawned) — Claude only
- Any locale-specific issues encountered

**Per guide confirmation:**
- EN was validated before translation (Phase 0)
- Structural repair applied and validated (Phase 1 + Gate 1)
- Translation-only agents used (Phase 2)
- All validation gates passed (Gate 1 + Gate 2)
- Persistence verified (`git diff --stat` + existence checks)
- No translation work was deferred or suggested for external handling

---

## Localization Rules (enforced by validation)

**Preserve Exactly (Never Translate):**
- `%LINK:target|anchor%` - translate anchor only; preserve target exactly
- `%IMAGE:path%` unchanged
- `%COMPONENT:name%` unchanged
- URLs, paths, IDs, technical tokens

**Translate Naturally:**
- Titles, body, FAQs
- Section headings
- Meta titles/descriptions
- Image alt text (if present)

**Match Structure:**
- Same section order + counts
- Same number of intro paragraphs
- Same FAQ count and ordering
- Same gallery structure

**Locale-appropriate phrasing:**
- Maintain existing formality level unless clearly inconsistent or incorrect

---

## Quality Gates (must pass before "complete")

**Gate 1 (structural — after Phase 1):**
1. All locale files parse as valid JSON
2. Section count exactly matches EN
3. Section IDs match EN (same IDs, same order)
4. Required top-level keys present (seo, linkLabel, intro, sections)
5. FAQs/tips lengths match EN (if present)

**Gate 2 (translation — after Phase 2):**
6. Per-section body array lengths match EN (anti-condensation)
7. Token targets preserved (LINK, HOWTO, URL, IMAGE targets match EN)
8. No empty strings in translated fields where EN is non-empty
9. Passes `CONTENT_READINESS_MODE=fail` i18n-parity-quality-audit

**Completion (Phase 3):**
10. All 17 locales pass both Gate 1 and Gate 2
11. `git diff --stat` shows changed files for all target locales
12. All expected locale file paths exist
13. Completion report includes all 4 required evidence items
14. No translation work was deferred or suggested for external handling

---

## Error Handling (Replacement-Only)

**JSON corruption detected**
- Restore file from known-good snapshot immediately.
- Re-apply intended change safely via structured JSON editing.
- If no snapshot exists or you cannot restore promptly, stop and ask user what they want to do.

**EN audit validation fails**
- Report specific issues
- STOP immediately
- Direct user to run `improve-en-guide` first

---

## Practical Implementation Note

Edits should be applied by:
1. loading JSON,
2. modifying only string fields,
3. serializing with `JSON.stringify(obj, null, 2)` + newline.

Avoid manual text patching in non-EN locales. This reduces risk of invalid quotes, delimiter issues, and encoding damage.
