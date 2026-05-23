---
name: enterprise-verify
description: "Evidence-based verification before any completion claim. No 'should work' or 'probably fine' — paste fresh test output or don't claim done. 7-check verification sequence. Use before committing or claiming work is complete."
---

# Enterprise Verify — Evidence-Based Completion Verification

## Why Evidence Matters

Without verification evidence, completion claims are beliefs — and beliefs ship bugs. "The code looks correct" means nothing when an import path is wrong, a test is silently skipped, or a debug `console.log` made it into the diff. Every check category below has caused a production incident at least once.

The distinction is simple: **evidence** is command output you can paste. **Belief** is anything else. This skill deals only in evidence.

---

## Step 1: Run verify.sh

The verification script runs all 7 checks mechanically and produces structured JSON evidence. Run it — don't run the checks manually.

```bash
bash .claude/skills/enterprise-verify/scripts/verify.sh \
  --base dev \
  --contract <path-to-contract> \
  --output .claude/enterprise-state/<slug>-verification-evidence.json
```

**Flags:**
- `--base <branch>` — base branch for diffs (default: `dev`)
- `--contract <path>` — contract file for postcondition extraction (optional)
- `--skip-build` — skip frontend build check (backend-only changes)
- `--output <path>` — where to write evidence JSON
- `--project <path>` — project root (auto-detected from cwd)

---

## Step 2: Read the JSON Evidence

The script outputs a JSON file with this structure:

```json
{
  "checks": {
    "test_suite":         { "result": "PASS|FAIL", "passed": N, "failed": N },
    "postcondition_trace": { "result": "MANUAL", "postconditions": "...", "test_names": "..." },
    "regression":          { "result": "PASS|FAIL", "new_failures": N },
    "build":               { "result": "PASS|FAIL|SKIP" },
    "diff":                { "result": "PASS", "files": [...] },
    "imports":             { "result": "PASS|FAIL", "unresolved": [...] },
    "debug_artifacts":     { "result": "PASS|FAIL", "findings": [...] }
  },
  "overall": "PASS|FAIL"
}
```

If `overall` is FAIL: stop, fix the failing checks, re-run verify.sh from scratch.

---

## Step 3: Complete the Two Manual Checks

The script automates 5 of 7 checks fully and collects data for the other 2. You must complete:

### Postcondition Trace (Check 2)
Map each postcondition from the contract to a specific test name from the `test_names` field. Use the EXACT test description from the runner output — not a paraphrase. If a postcondition has no matching test: FAIL.

### Diff Classification (Check 5)
The script lists changed files. Classify each as:
- **REQUIRED** — in the contract/plan
- **ENABLING** — needed to support a required change
- **DRIFT** — not related to this task → `git checkout -- path/to/file`

---

## Step 4: Write the Verification Report

```
===============================================
         ENTERPRISE VERIFICATION REPORT
===============================================

Task: [what was done]
Date: [YYYY-MM-DD]
Branch: [branch name]
Evidence: [path to JSON file]

## Automated Checks (from verify.sh)
  Check 1 — Test Suite:          [PASS — N passed, 0 failed]
  Check 3 — Regression Check:    [PASS — no regressions]
  Check 4 — Build Verification:  [PASS / SKIPPED (backend only)]
  Check 6 — Import Resolution:   [PASS — all imports resolve]
  Check 7 — Debug Artifacts:     [PASS — none found]

## Manual Checks
  Check 2 — Postcondition Trace: [PASS — N/N verified]
  Check 5 — Final Diff:          [PASS — N files, 0 drift]

  ────────────────────────────
  OVERALL: [PASS / FAIL]
```

---

## When to Run

| Trigger | Action |
|---------|--------|
| About to say "it's done" | Run verify.sh first |
| About to commit | Run verify.sh first |
| About to create a PR | Run verify.sh first |
| "One more thing" was fixed | Re-run verify.sh from scratch |

---

## Failure Recovery

When a check fails:
1. Fix the issue
2. Re-run verify.sh entirely (not just the failed check)
3. If tests fail after a fix: you introduced a regression — revert and try again

---

## Language That Signals Missing Evidence

If you catch yourself reaching for these phrases, you haven't run verification yet:

- "should work" / "probably fine" → run verify.sh, read the JSON
- "looks good" / "looks correct" → run verify.sh, report evidence
- "I'm confident" / "I believe" → confidence isn't evidence

---

## Edge Cases

**No formal contract?** Derive postconditions from the task description. Run verify.sh without `--contract` — it still runs all other checks.

**Only one file changed?** Still run verify.sh. A one-line change can break tests or leave debug artifacts.

**Test suite takes too long?** Run verify.sh once with full suite. Don't substitute partial runs.

See `references/verification-checks.md` for the detailed command reference behind each check.
