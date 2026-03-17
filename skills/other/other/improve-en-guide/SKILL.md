---
name: improve-en-guide
description: Run SEO audit and iteratively fix all issues for English guide content only. No translation.
---

# English Guide SEO Audit + Fix (EN Only, Reader-First)

## Scope

**This skill ONLY handles English content.**

- Runs baseline JSON validation and fixing
- Runs SEO audit for the given guide
- Iteratively fixes all audit issues in the EN locale only
- Validates that all EN audit issues are resolved
- **Stops before any translation work**

Use `improve-translate-guide` for translation after EN is clean.

## Core Commitments (Non-Negotiable)

**Every write is validated immediately.**
After each file write, validate JSON parseability and token integrity before doing anything else.

If validation fails, the only allowed fix is replacement with known-good content.

- Restore the file from a known-good snapshot taken immediately before the edit.
- Then re-apply the intended change safely (prefer structured JSON editing).
- No other fix is valid. No "surgery" on corrupted text, no partial patching.

**Readership-first ordering is required.**
Reorder content so the reader can decide/act quickly, with explicit early-content gates (defined below).

---

## Operating Mode

**READ + SNAPSHOT + BASELINE VALIDATE + RUN (SCRIPT) + EDIT (EN JSON, VALIDATE EACH WRITE) + RE-RUN (UNTIL CLEAN) + REPORT**

---

## Allowed

- Ask user to specify a single guide or a batch definition
- Read/parse guide references (URL/slug/guideKey list)
- Read guide manifest data to map slug(s) to guideKey(s)
- Run `apps/brikette/scripts/baseline-validate-and-fix-json.ts` (optional, recommended)
- Run `apps/brikette/scripts/audit-guide-seo.ts` (EN locale only)
- Read/modify EN guide JSON:
  - `apps/brikette/src/locales/en/guides/content/{guideKey}.json`
- Update audit results in:
  - `apps/brikette/src/data/guides/guide-manifest-overrides.json`
- Web research for fact verification + finding usable images (as needed)
- Write original prose (no copying copyrighted text)

---

## Not Allowed

- Third-party SEO tools/APIs (Semrush, Ahrefs, Screaming Frog, etc.)
- Changes outside the target guides except where strictly required by the audit
- **Any translation or localization work** (use improve-translate-guide instead)
- Deferring validation/fixing "until later"
- Any remediation for corrupted JSON other than replacement with known-good content

---

## Inputs

### Required

**Guide reference (one of):**
- Full URL (preferred), e.g. `http://localhost:3012/en/experiences/gavitella-beach-guide`
- Slug, e.g. `gavitella-beach-guide`
- guideKey, e.g. `gavitellaBeachGuide`
- List of URLs/slugs/guideKeys for batch processing

### Optional Flags

- `--skip-json-fix` - Skip baseline JSON validation/fixing step

### Optional (but recommended)

- Readership/audience (ask after the first audit results are known)
- Tone constraints + must-include details (accessibility, costs, transport, safety, crowds, seasonality)

---

## Pre-step: Ask About Readership (Required)

After the first audit results are known, ask:

- Intended readership?
- Tone constraints?
- Must-include details (accessibility, costs, transport, safety, crowds, seasonality)?

If the user doesn't respond, assume: general travelers + practical "how to go / what to expect."

---

## Script of Record

Audit logic is exactly:

- `apps/brikette/scripts/audit-guide-seo.ts`

Baseline validation:

- `apps/brikette/scripts/baseline-validate-and-fix-json.ts`

---

## JSON Editing Safety Protocol (Mandatory for Large Content Updates)

When expanding guide content significantly (adding 500+ words or 3+ new sections):

**REQUIRED: Use scripted JSON editing, not direct Edit tool**
1. Create a temporary Python or Node.js script in `apps/brikette/scripts/temp-*.py` or `scripts/temp-*.js`
2. Load JSON with `JSON.parse()` or `json.load()`
3. Modify only string values programmatically
4. Write with `JSON.stringify(obj, null, 2) + '\n'` or `json.dump()`
5. Validate immediately after write
6. Delete temp script after completion

**Why:** The Edit tool with complex multi-line strings containing quotes, apostrophes, and special characters frequently causes JSON parse errors. Structured editing via scripts eliminates this failure mode.

**Exception:** Small edits (single field, <100 chars) can use Edit tool directly.

---

## Validation & Replacement Protocol (applies to every write)

### A. Snapshot before every edit (mandatory)

Before modifying any JSON file:

1. Read the full file contents into memory as the known-good snapshot.
2. Ensure you can restore it immediately if needed.

### B. Validate immediately after every write (mandatory)

For any file you write (EN guide JSON, manifest overrides JSON), run:

**JSON parse check (hard gate)**
- Must parse as valid JSON (UTF-8).
- If it fails, restore snapshot immediately.

**Token preservation check (hard gate)**
Preserve exactly:
- `%LINK:target|anchor%` - only anchor may change; target must remain identical
- `%IMAGE:path%` unchanged
- `%COMPONENT:name%` unchanged
- URLs, paths, IDs, technical tokens

If broken/missing/unexpected changes, restore snapshot immediately.

### C. Only permitted remedy for failed validation

1. Replace corrupted content with the known-good snapshot.
2. Re-apply the intended change using structured JSON editing.
3. If repeated failure (or no known-good snapshot) and you cannot produce a clean write promptly, stop and ask user what to do.

---

## Readership-first Ordering Gates (Mandatory)

The guide must communicate essentials early. Apply this in EN content.

### Default early-content window

Target first ~250-350 words. Choose the smallest number that fully communicates essentials for that guide type.

### Guide-type specific gates

**Directions / "how to get there" guides**

Within first ~300 words:
- Starting point(s) and destination
- Best default route + alternatives (walk/transit/taxi/car)
- Typical time range(s)
- Approx cost expectations (if relevant)
- One or two "gotchas" (stairs, last service, reservations, weather exposure)

**Beach guides**

Within first ~250-300 words:
- Who it's best for / not for (kids, mobility, budget, crowds)
- Access difficulty (stairs, distance, transport)
- Facilities snapshot (toilets, showers, shade, rentals)
- Costs (free vs lido fees; parking; rentals if known)
- Best time to go + one safety note if relevant

**Attractions / POIs**

Within first ~250-300 words:
- Why go + time needed
- Access and booking/queues
- Cost expectations (if relevant)
- One or two key gotchas

**Food/drink venues**

Within first ~250-300 words:
- What it is + price band
- Booking necessity
- Dietary constraints baseline
- Best use case (sunset, quick bite, special occasion)

---

## Workflow

### 1) Resolve guide reference to guideKey

For each input item:
- If URL/slug: map to guideKey via manifest
- Validate EN file exists for each guideKey

**Stop-the-line rule:**
If any guide cannot be resolved, report which item failed and ask user how to proceed.

### 2) Baseline validation (unless --skip-json-fix)

Run:
```bash
cd apps/brikette && pnpm tsx scripts/baseline-validate-and-fix-json.ts
```

Validate:
- EN guide JSON parses cleanly
- guide-manifest-overrides.json parses cleanly

If any file is corrupted:
- Replace corrupted content with known-good content immediately.
- If you cannot restore promptly, stop and ask user what they want to do.

### 3) Run initial audit

```bash
pnpm --filter brikette tsx scripts/audit-guide-seo.ts {guideKey}
```

Read audit output from overrides JSON.

### 4) Apply EN fixes iteratively

- Use structured JSON editing (load, modify, stringify)
- After each EN write:
  - snapshot exists
  - validate parse + token integrity
- Enforce readership-first ordering gates
- Re-run audit after each iteration until clean:
  - score >= 9.0
  - zero critical issues
  - zero improvements

**Stop-the-line:**
- If any write fails validation, restore snapshot immediately and redo safely.
- If you cannot produce a timely clean write, stop and ask the user what to do.

### 5) Completion report

Report:

**Per guide:**
- Initial score, final score
- Audit iterations performed
- Key issue categories fixed
- Reader-first improvements made (what the first ~300 words now cover)
- Confirmation that:
  - every write was validated immediately
  - any corruption was handled only by replacement with known-good content

---

## Quality Gates (must pass before "complete")

1. Final audit score >= 9.0
2. Zero critical issues
3. Zero improvements remaining
4. EN JSON valid + tokens preserved
5. Overrides JSON valid

---

## Success Criteria

All EN audit issues resolved. No translation performed.

---

## What Happens Next

After this skill completes successfully, the user should run `improve-translate-guide` to propagate the fixed EN content to all locales.

Or use `improve-guide` (the orchestrator) to run both sequentially in one command.

---

## Error Handling (Replacement-Only)

**JSON corruption detected**
- Restore file from known-good snapshot immediately.
- Re-apply intended change safely via structured JSON editing.
- If no snapshot exists or you cannot restore promptly, stop and ask user what they want to do.

**Audit script fails**
- Validate guide-manifest-overrides.json and the target EN guide JSON parse cleanly; restore if corrupted.
- Verify script path exists and dependencies installed.
- Re-run.
