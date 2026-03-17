---
name: vibe
description: 'Comprehensive code validation. Runs complexity analysis then multi-model council. Answer: Is this code ready to ship? Triggers: "vibe", "validate code", "check code", "review code", "code quality", "is this ready".'
metadata:
  tier: judgment
  dependencies:
    - council    # multi-model judgment
    - complexity # complexity analysis
    - standards  # loaded for language-specific context
---

# Vibe Skill

> **Purpose:** Is this code ready to ship?

Two steps:
1. **Complexity analysis** — Find hotspots (radon, gocyclo)
2. **Council validation** — Multi-model judgment

---

## Quick Start

```bash
/vibe                                    # validates recent changes
/vibe recent                             # same as above
/vibe src/auth/                          # validates specific path
/vibe --quick recent                     # fast inline check, no agent spawning
/vibe --deep recent                      # 3 judges instead of 2
/vibe --mixed recent                     # cross-vendor (Claude + Codex)
/vibe --preset=security-audit src/auth/  # security-focused review
/vibe --explorers=2 recent               # judges with explorer sub-agents
/vibe --debate recent                    # two-round adversarial review
```

---

## Execution Steps

### Step 1: Determine Target

**If target provided:** Use it directly.

**If no target or "recent":** Auto-detect from git:
```bash
# Check recent commits
git diff --name-only HEAD~3 2>/dev/null | head -20
```

If nothing found, ask user.

**Pre-flight: If no files found:**
Return immediately with: "PASS (no changes to review) — no modified files detected."
Do NOT spawn agents for empty file lists.

### Step 1.5: Fast Path (--quick mode)

**If `--quick` flag is set**, skip Steps 2a–2e (constraint tests, metadata checks, OL validation, codex review, knowledge search, product context) and jump directly to Step 4 with inline council. Complexity analysis (Step 2) still runs — it's cheap and informative.

**Why:** Steps 2a–2e add 30–90 seconds of pre-processing that feed multi-judge council packets. In --quick mode (single inline agent), these inputs aren't worth the cost — the inline reviewer reads files directly.

### Step 2: Run Complexity Analysis

**Detect language and run appropriate tool:**

**For Python:**
```bash
# Check if radon is available
mkdir -p .agents/council
echo "$(date -Iseconds) preflight: checking radon" >> .agents/council/preflight.log
if ! which radon >> .agents/council/preflight.log 2>&1; then
  echo "⚠️ COMPLEXITY SKIPPED: radon not installed (pip install radon)"
  # Record in report that complexity was skipped
else
  # Run cyclomatic complexity
  radon cc <path> -a -s 2>/dev/null | head -30
  # Run maintainability index
  radon mi <path> -s 2>/dev/null | head -30
fi
```

**For Go:**
```bash
# Check if gocyclo is available
echo "$(date -Iseconds) preflight: checking gocyclo" >> .agents/council/preflight.log
if ! which gocyclo >> .agents/council/preflight.log 2>&1; then
  echo "⚠️ COMPLEXITY SKIPPED: gocyclo not installed (go install github.com/fzipp/gocyclo/cmd/gocyclo@latest)"
  # Record in report that complexity was skipped
else
  # Run complexity analysis
  gocyclo -over 10 <path> 2>/dev/null | head -30
fi
```

**For other languages:** Skip complexity with explicit note: "⚠️ COMPLEXITY SKIPPED: No analyzer for <language>"

**Interpret results:**

| Score | Rating | Action |
|-------|--------|--------|
| A (1-5) | Simple | Good |
| B (6-10) | Moderate | OK |
| C (11-20) | Complex | Flag for council |
| D (21-30) | Very complex | Recommend refactor |
| F (31+) | Untestable | Must refactor |

**Include complexity findings in council context.**

### Step 2a: Run Constraint Tests

**Skip if `--quick` (see Step 1.5).**

**If the project has constraint tests, run them before council:**

```bash
# Check if constraint tests exist (Olympus pattern)
if [ -d "internal/constraints" ] && ls internal/constraints/*_test.go &>/dev/null; then
  echo "Running constraint tests..."
  go test ./internal/constraints/ -run TestConstraint -v 2>&1
  # If FAIL → include failures in council context as CRITICAL findings
  # If PASS → note "N constraint tests passed" in report
fi
```

**Why:** Constraint tests catch mechanical violations (ghost references, TOCTOU races, dead code at entry points) that council judges miss. Proven by Argus ghost ref in ol-571 — council gave PASS while constraint test caught it.

Include constraint test results in the council packet context. Failed constraint tests are CRITICAL findings that override council PASS verdict.

### Step 2b: Metadata Verification Checklist (MANDATORY)

**Skip if `--quick` (see Step 1.5).**

Run mechanical checks BEFORE council — catches errors LLMs estimate instead of measure:
1. **File existence** — every path in `git diff --name-only HEAD~3` must exist on disk
2. **Line counts** — if a file claims "N lines", verify with `wc -l`
3. **Cross-references** — internal markdown links resolve to existing files
4. **Diagram sanity** — files with >3 ASCII boxes should have matching labels

Include failures in council packet as `context.metadata_failures` (MECHANICAL findings). If all pass, note in report.

### Step 2c: Deterministic Validation (Olympus)

**Skip if `--quick` (see Step 1.5).**

**Guard:** Only run when `.ol/config.yaml` exists AND `which ol` succeeds. Skip silently otherwise.

**Implementation:**

```bash
# Run ol-validate.sh
skills/vibe/scripts/ol-validate.sh
ol_exit_code=$?

case $ol_exit_code in
  0)
    # Passed: include the validation report in vibe output
    echo "✅ Deterministic validation passed"
    # Append the report section to council context and vibe report
    ;;
  1)
    # Failed: abort vibe with FAIL verdict
    echo "❌ Deterministic validation FAILED"
    echo "VIBE FAILED — Olympus Stage1 validation did not pass"
    exit 1
    ;;
  2)
    # Skipped: note and continue
    echo "⚠️ OL validation skipped"
    # Continue to council
    ;;
esac
```

**Behavior:**
- **Exit 0 (passed):** Include the validation report section in vibe output and council context. Proceed normally.
- **Exit 1 (failed):** Auto-FAIL the vibe. Do NOT proceed to council.
- **Exit 2 (skipped):** Note "OL validation skipped" in report. Proceed to council.

### Step 2.5: Codex Review (if available)

**Skip if `--quick` (see Step 1.5).**

Run a fast, diff-focused code review via Codex CLI before council:

```bash
echo "$(date -Iseconds) preflight: checking codex" >> .agents/council/preflight.log
if which codex >> .agents/council/preflight.log 2>&1; then
  codex review --uncommitted > .agents/council/codex-review-pre.md 2>&1 && \
    echo "Codex review complete — output at .agents/council/codex-review-pre.md" || \
    echo "Codex review skipped (failed)"
else
  echo "Codex review skipped (CLI not found)"
fi
```

**If output exists**, summarize and include in council packet (cap at 2000 chars to prevent context bloat):
```json
"codex_review": {
  "source": "codex review --uncommitted",
  "content": "<first 2000 chars of .agents/council/codex-review-pre.md>"
}
```

**IMPORTANT:** The raw codex review can be 50k+ chars. Including the full text in every judge's packet multiplies token cost by N judges. Truncate to the first 2000 chars (covers the summary and top findings). Judges can read the full file from disk if they need more detail.

This gives council judges a Codex-generated review as pre-existing context — cheap, fast, diff-focused. It does NOT replace council judgment; it augments it.

**Skip conditions:**
- Codex CLI not on PATH → skip silently
- `codex review` fails → skip silently, proceed with council only
- No uncommitted changes → skip (nothing to review)

### Step 2d: Search Knowledge Flywheel

**Skip if `--quick` (see Step 1.5).**

```bash
if command -v ao &>/dev/null; then
    ao search "code review findings <target>" 2>/dev/null | head -10
fi
```
If ao returns prior code review patterns for this area, include them in the council packet context. Skip silently if ao is unavailable or returns no results.

### Step 2e: Check for Product Context

**Skip if `--quick` (see Step 1.5).**

```bash
if [ -f PRODUCT.md ]; then
  # PRODUCT.md exists — include developer-experience perspectives
fi
```

When `PRODUCT.md` exists in the project root AND the user did NOT pass an explicit `--preset` override:
1. Read `PRODUCT.md` content and include in the council packet via `context.files`
2. Add a single consolidated `developer-experience` perspective to the council invocation:
   - **With spec:** `/council --preset=code-review --perspectives="developer-experience" validate <target>` (3 judges: 2 code-review + 1 DX)
   - **Without spec:** `/council --perspectives="developer-experience" validate <target>` (3 judges: 2 independent + 1 DX)
   The DX judge covers api-clarity, error-experience, and discoverability in a single review.
3. With `--deep`: adds 1 more judge per mode (4 judges total).

When `PRODUCT.md` exists BUT the user passed an explicit `--preset`: skip DX auto-include (user's explicit preset takes precedence).

When `PRODUCT.md` does not exist: proceed to Step 3 unchanged.

> **Tip:** Create `PRODUCT.md` from `docs/PRODUCT-TEMPLATE.md` to enable developer-experience-aware code review.

### Step 3: Load the Spec (New)

**Skip if `--quick` (see Step 1.5).**

Before invoking council, try to find the relevant spec/bead:

1. **If target looks like a bead ID** (e.g., `na-0042`): `bd show <id>` to get the spec
2. **Search for plan doc:** `ls .agents/plans/ | grep <target-keyword>`
3. **Check git log:** `git log --oneline | head -10` to find the relevant bead reference

If a spec is found, include it in the council packet's `context.spec` field:
```json
{
  "spec": {
    "source": "bead na-0042",
    "content": "<the spec/bead description text>"
  }
}
```

### Step 4: Run Council Validation

**With spec found — use code-review preset:**
```
/council --preset=code-review validate <target>
```
- `error-paths`: Trace every error handling path. What's uncaught? What fails silently?
- `api-surface`: Review every public interface. Is the contract clear? Breaking changes?
- `spec-compliance`: Compare implementation against the spec. What's missing? What diverges?

The spec content is injected into the council packet context so the `spec-compliance` judge can compare implementation against it.

**Without spec — 2 independent judges (no perspectives):**
```
/council validate <target>
```
2 independent judges (no perspective labels). Use `--deep` for 3 judges on high-stakes reviews. Override with `--quick` (inline single-agent check) or `--mixed` (cross-vendor with Codex).

**Council receives:**
- Files to review
- Complexity hotspots (from Step 2)
- Git diff context
- Spec content (when found, in `context.spec`)

All council flags pass through: `--quick` (inline), `--mixed` (cross-vendor), `--preset=<name>` (override perspectives), `--explorers=N`, `--debate` (adversarial 2-round). See Quick Start examples and `/council` docs.

### Step 5: Council Checks

Each judge reviews for:

| Aspect | What to Look For |
|--------|------------------|
| **Correctness** | Does code do what it claims? |
| **Security** | Injection, auth issues, secrets |
| **Edge Cases** | Null handling, boundaries, errors |
| **Quality** | Dead code, duplication, clarity |
| **Complexity** | High cyclomatic scores, deep nesting |
| **Architecture** | Coupling, abstractions, patterns |

### Step 6: Interpret Verdict

| Council Verdict | Vibe Result | Action |
|-----------------|-------------|--------|
| PASS | Ready to ship | Merge/deploy |
| WARN | Review concerns | Address or accept risk |
| FAIL | Not ready | Fix issues |

### Step 7: Write Vibe Report

**Write to:** `.agents/council/YYYYMMDDTHHMMSSZ-vibe-<target>.md` (use `date -u +%Y%m%dT%H%M%SZ`)

```markdown
# Vibe Report: <Target>

**Date:** YYYY-MM-DD
**Files Reviewed:** <count>

## Complexity Analysis

**Status:** ✅ Completed | ⚠️ Skipped (<reason>)

| File | Score | Rating | Notes |
|------|-------|--------|-------|
| src/auth.py | 15 | C | Consider breaking up |
| src/utils.py | 4 | A | Good |

**Hotspots:** <list files with C or worse>
**Skipped reason:** <if skipped, explain why - e.g., "radon not installed">

## Council Verdict: PASS / WARN / FAIL

| Judge | Verdict | Key Finding |
|-------|---------|-------------|
| Error-Paths | ... | ... (with spec — code-review preset) |
| API-Surface | ... | ... (with spec — code-review preset) |
| Spec-Compliance | ... | ... (with spec — code-review preset) |
| Judge 1 | ... | ... (no spec — 2 independent judges) |
| Judge 2 | ... | ... (no spec — 2 independent judges) |
| Judge 3 | ... | ... (no spec — 2 independent judges) |

## Shared Findings
- ...

## Concerns Raised
- ...

## Recommendation
<council recommendation>

## Decision

[ ] SHIP - Complexity acceptable, council passed
[ ] FIX - Address concerns before shipping
[ ] REFACTOR - High complexity, needs rework
```

### Step 8: Report to User

Tell the user:
1. Complexity hotspots (if any)
2. Council verdict (PASS/WARN/FAIL)
3. Key concerns
4. Location of vibe report

### Step 9: Record Ratchet Progress

After council verdict:
1. If verdict is PASS or WARN:
   - Run: `ao ratchet record vibe --output "<report-path>" 2>/dev/null || true`
   - Suggest: "Run /post-mortem to capture learnings and complete the cycle."
2. If verdict is FAIL:
   - Do NOT record ratchet progress.
   - Extract top 5 findings from the council report for structured retry context:
     ```
     Read the council report. For each finding (max 5), format as:
     FINDING: <description> | FIX: <fix or recommendation> | REF: <ref or location>

     Fallback for v1 findings (no fix/why/ref fields):
       fix = finding.fix || finding.recommendation || "No fix specified"
       ref = finding.ref || finding.location || "No reference"
     ```
   - Tell user to fix issues and re-run /vibe, including the formatted findings as actionable guidance.

### Step 9.5: Feed Findings to Flywheel

**If verdict is WARN or FAIL**, write top findings as a lightweight learning for future sessions:

```bash
if [[ "$VERDICT" == "WARN" || "$VERDICT" == "FAIL" ]]; then
  mkdir -p .agents/learnings
  LEARNING_FILE=".agents/learnings/$(date -u +%Y-%m-%d)-vibe-$(echo "$TARGET" | tr '/' '-' | head -c 40).md"
  cat > "$LEARNING_FILE" <<EOF
---
type: anti-pattern
source: vibe
date: $(date -Iseconds)
confidence: high
---

# Vibe findings: $TARGET

$(for finding in "${TOP_FINDINGS[@]:0:3}"; do
  echo "- **${finding.severity}:** ${finding.description} (${finding.location})"
done)

**Recommendation:** ${COUNCIL_RECOMMENDATION}
EOF

  # Index for flywheel if ao available
  if command -v ao &>/dev/null; then
    ao forge markdown "$LEARNING_FILE" 2>/dev/null || true
  fi
fi
```

**Why:** Vibe catches anti-patterns repeatedly across epics but they evaporate unless `/post-mortem` runs. This captures findings at the point of discovery — lightweight (one file write, no `/retro` invocation) and immediately available to future sessions via inject.

**Skip if:** PASS verdict (nothing to learn from clean code).

### Step 10: Test Bead Cleanup

After validation completes (regardless of verdict), clean up any stale test beads to prevent bead pollution:

```bash
# Test bead hygiene: close any beads created by test/validation runs
if command -v bd &>/dev/null; then
  test_beads=$(bd list --status=open 2>/dev/null | grep -iE "test bead|test quest|smoke test" | awk '{print $1}')
  if [ -n "$test_beads" ]; then
    echo "$test_beads" | xargs bd close 2>/dev/null || true
    log "Cleaned up $(echo "$test_beads" | wc -l | tr -d ' ') test beads"
  fi
fi
```

---

## Integration with Workflow

```
/implement issue-123
    │
    ▼
(coding, quick lint/test as you go)
    │
    ▼
/vibe                      ← You are here
    │
    ├── Complexity analysis (find hotspots)
    └── Council validation (multi-model judgment)
    │
    ├── PASS → ship it
    ├── WARN → review, then ship or fix
    └── FAIL → fix, re-run /vibe
```

---

## Examples

**User says:** "Run a quick validation on the latest changes."

**Do:**
```bash
/vibe recent
```

### Validate Recent Changes

```bash
/vibe recent
```

Runs complexity on recent changes, then council reviews.

### Validate Specific Directory

```bash
/vibe src/auth/
```

Complexity + council on auth directory.

### Deep Review

```bash
/vibe --deep recent
```

Complexity + 3 judges for thorough review.

### Cross-Vendor Consensus

```bash
/vibe --mixed recent
```

Complexity + Claude + Codex judges.

See `references/examples.md` for additional examples: security audit with spec compliance, developer-experience code review with PRODUCT.md, and fast inline checks.

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "COMPLEXITY SKIPPED: radon not installed" | Python complexity analyzer missing | Install with `pip install radon` or skip complexity (council still runs). |
| "COMPLEXITY SKIPPED: gocyclo not installed" | Go complexity analyzer missing | Install with `go install github.com/fzipp/gocyclo/cmd/gocyclo@latest` or skip. |
| Vibe returns PASS but constraint tests fail | Council LLMs miss mechanical violations | Check `.agents/council/<timestamp>-vibe-*.md` for constraint test results. Failed constraints override council PASS. Fix violations and re-run. |
| Codex review skipped | Codex CLI not on PATH or no uncommitted changes | Install Codex CLI (`brew install codex`) or commit changes first. Vibe proceeds without codex review. |
| "No modified files detected" | Clean working tree, no recent commits | Make changes or specify target path explicitly: `/vibe src/auth/`. |
| Spec-compliance judge not spawned | No spec found in beads/plans | Reference bead ID in commit message or create plan doc in `.agents/plans/`. Without spec, vibe uses 2 independent judges (3 with `--deep`). |

---

## See Also

- `skills/council/SKILL.md` — Multi-model validation council
- `skills/complexity/SKILL.md` — Standalone complexity analysis
- `.agents/specs/conflict-resolution-algorithm.md` — Conflict resolution between agent findings
