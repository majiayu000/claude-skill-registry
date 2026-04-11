---
name: vibe
description: 'Comprehensive code validation. Runs complexity analysis then multi-model council. Answer: Is this code ready to ship? Triggers: "vibe", "validate code", "check code", "review code", "code quality", "is this ready".'
skill_api_version: 1
metadata:
  tier: judgment
  dependencies:
    - council    # multi-model judgment
    - complexity # complexity analysis
    - bug-hunt   # proactive code audit
    - standards  # loaded for language-specific context
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: full
output_contract: skills/council/schemas/verdict.json
---

# Vibe Skill

> **Purpose:** Is this code ready to ship?

Three steps:
1. **Complexity analysis** — Find hotspots (radon, gocyclo)
2. **Bug hunt audit** — Systematic sweep for concrete bugs
3. **Council validation** — Multi-model judgment

---

## Quick Start

```bash
/vibe                                    # validates recent changes
/vibe recent                             # same as above
/vibe src/auth/                          # validates specific path
/vibe --quick recent                     # fast inline check, no agent spawning
/vibe --structured recent                # 6-phase verification report (build→types→lint→tests→security→diff)
/vibe --deep recent                      # 3 judges instead of 2
/vibe --sweep recent                     # deep audit: per-file explorers + council
/vibe --mixed recent                     # cross-vendor (Claude + Codex)
/vibe --preset=security-audit src/auth/  # security-focused review
/vibe --explorers=2 recent               # judges with explorer sub-agents
/vibe --debate recent                    # two-round adversarial review
/vibe --tier=quality recent              # use quality tier for council calls
```

---

## Execution Steps

### Step 0: Load Prior Review Context

Before reviewing, pull relevant learnings from prior code reviews and known patterns:

```bash
if command -v ao &>/dev/null; then
    ao lookup --query "<target-scope> code review patterns" --limit 3 2>/dev/null || true
fi
```

**Apply retrieved knowledge (mandatory when results returned):**

If learnings or patterns are returned, do NOT just load them as passive context. For each returned item:
1. Check: does this learning apply to the code under review? (answer yes/no)
2. If yes: include it as a `known_risk` in your review — state the pattern, what to look for, and whether the code exhibits it
3. Cite the learning by filename in your review output when it influences a finding

After applying, record the citation:
```bash
ao metrics cite "<learning-path>" --type applied 2>/dev/null || true
```

Skip silently if ao is unavailable or returns no results.

**Project reviewer config:** If `.agents/reviewer-config.md` exists, its full config (`reviewers`, `plan_reviewers`, `skip_reviewers`) is passed to council for judge selection. See `skills/council/SKILL.md` Step 1b.

### Crank Checkpoint Detection

Before scanning for changed files via git diff, check if a crank checkpoint exists:

```bash
if [ -f .agents/vibe-context/latest-crank-wave.json ]; then
    echo "Crank checkpoint found — using files_changed from checkpoint"
    FILES_CHANGED=$(jq -r '.files_changed[]' .agents/vibe-context/latest-crank-wave.json 2>/dev/null)
    WAVE_COUNT=$(jq -r '.wave' .agents/vibe-context/latest-crank-wave.json 2>/dev/null)
    echo "Wave $WAVE_COUNT checkpoint: $(echo "$FILES_CHANGED" | wc -l | tr -d ' ') files changed"
fi
```

When a crank checkpoint is available, use its `files_changed` list instead of re-detecting via `git diff`. This ensures vibe validates exactly the files that crank modified.

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

### Step 1.5a: Structured Verification Path (--structured mode)

**If `--structured` flag is set**, run a 6-phase mechanical verification pipeline instead of the council flow. This produces a machine-readable verification report suitable for PR gates and CI integration.

Phases: Build → Types → Lint → Tests → Security → Diff Review.

Read `references/verification-report.md` for the full report template and per-phase commands. Each phase is fail-fast — if Build fails, skip remaining phases and report NOT READY.

After all phases complete, write the structured report to `.agents/council/YYYY-MM-DD-verification-<target>.md` and output the summary table to the user.

**When to use:** Pre-PR gate, CI integration, when you need a mechanical pass/fail rather than judgment-based review.

### Step 1.5: Fast Path (--quick mode)

**If `--quick` flag is set**, skip Steps 2a through 2e as heavy pre-processing, plus 2.5 and 2f, and jump to Step 4 with inline council after Steps 2.3, 2.4, 2g, and Step 3. Domain checklists, compiled-prevention loading, test-pyramid inventory, and inline product context are cheap and high-value, so they still run in quick mode. Complexity analysis (Step 2) still runs — it's cheap and informative.

**Why:** Steps 2.5 and 2a–2f add 30–90 seconds of pre-processing that mainly feed multi-judge council packets. In --quick mode (single inline agent), those inputs are not worth the cost, but test-pyramid and product-context checks still shape the inline review meaningfully.

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

### Step 2.3: Load Domain-Specific Checklists

Detect code patterns in the target files and load matching domain-specific checklists from `standards/references/`:

| Trigger | Checklist | Detection |
|---------|-----------|-----------|
| SQL/ORM code | `sql-safety-checklist.md` | Files contain SQL queries, ORM imports (`database/sql`, `sqlalchemy`, `prisma`, `activerecord`, `gorm`, `knex`), or migration files in changeset |
| LLM/AI code | `llm-trust-boundary-checklist.md` | Files import `anthropic`, `openai`, `google.generativeai`, or match `*llm*`, `*prompt*`, `*completion*` patterns |
| Concurrent code | `race-condition-checklist.md` | Files use goroutines, `threading`, `asyncio`, `multiprocessing`, `sync.Mutex`, `concurrent.futures`, or shared file I/O patterns |
| Codex skills | `codex-skill.md` | Files under `skills-codex/`, or files matching `*codex*SKILL.md`, `convert.sh`, `skills-codex-overrides/`, or converter scripts |

For each matched checklist, load it via the Read tool and include relevant items in the council packet as `context.domain_checklists`. Multiple checklists can be loaded simultaneously.

Skip silently if no patterns match. This step runs in both `--quick` and full modes (domain checklists are cheap to load and high-value).

**Steps 2.4-2f, 2h, 3-3.6 (Deep Checks & Pre-Council Prep):** Read `references/deep-checks.md` for compiled prevention, prior findings, pre-council deep analysis checks, product context, spec loading, suppressions, pre-mortem correlation, and model cost tiers. Loaded automatically unless `--quick` mode is set. In `--quick` mode, skip directly to Step 2g.

**Compiled prevention inputs:** Load `.agents/pre-mortem-checks/` and `.agents/planning-rules/` when available. These compiled artifacts contain known_risks from prior findings that inform the review — carry matched finding IDs into council context so judges can assess whether the flywheel prevented rediscovery.

### Step 2a: Prior Findings Check

**Skip if `--quick`.** Load prior findings from `.agents/findings/registry.jsonl`.

### Step 2b: Constraint Tests

**Skip if `--quick`.** Run compiled constraint tests from `.agents/constraints/`.

### Step 2c: Metadata Checks

**Skip if `--quick`.** Verify file metadata consistency.

### Step 2.5: OL Validation

**Skip if `--quick`.** Run organizational-lint checks.

### Step 2d: Knowledge Search

**Skip if `--quick`.** Search for relevant prior learnings via `ao lookup`.

### Step 2e: Bug Hunt

**Skip if `--quick`.** Run proactive bug-hunt audit on target files.

### Step 2f: Codex Review

**Skip if `--quick`.** When `--mixed` is passed and Codex CLI is available, send the first 2000 chars of the diff to Codex for a parallel review. Cap input at 2000 chars to stay within Codex context budgets.

### Step 3: Product Context

**Skip if `--quick` as a separate judge-fanout step.** When `PRODUCT.md` exists and the user did not pass an explicit `--preset` override, quick mode still loads DX expectations inline in the single-agent review. In non-quick modes, add a DX (developer experience) judge: 2 independent + 1 DX judge (3 judges total). The DX judge evaluates whether the code aligns with the product's stated personas and value propositions.

### Step 2g: Test Pyramid Inventory (MANDATORY)

Assess test coverage against the test pyramid standard (the test pyramid standard (loaded via `/standards`)).

Read `skills/vibe/references/test-pyramid-weighting.md` for test pyramid weighting — L3+ tests found all production bugs, weight them 5x.

**Test Pyramid Weighting:** Weight test coverage by level: L0–L1 at 1x, L2 at 3x, L3+ at 5x. Unit-only coverage is a WARN signal, not a PASS. See `references/test-pyramid-weighting.md`.

**Run even in `--quick` mode** — this is cheap (file existence checks) and high-signal.

1. **Identify changed modules** from git diff or target scope
2. **For each changed module, check coverage pyramid (L0–L3):**
   - L0: Does a contract/spec enforcement test cover this module?
   - L1: Does a unit test file exist for this module?
   - L2: If module crosses boundaries, does an integration test exist?
3. **For boundary-touching code, check bug-finding pyramid (BF1–BF5):**
   - BF4 (Chaos): Do external call sites have failure injection tests?
   - BF1 (Property): Do data transformations have property tests?
   - BF2 (Golden): Do output generators have golden file tests?
4. **Compute weighted pyramid score** for changed code paths:

   **Formula:**
   ```
   weighted_score = (L0_count x 1 + L1_count x 1 + L2_count x 3 + L3_count x 5 + L4_count x 5) / max_possible
   ```
   Where `max_possible = total_test_count x 5` (the score if every test were L3+).

   Count tests at each level for changed code paths:
   - L0: Build/compile checks (weight 1)
   - L1: Unit tests (weight 1)
   - L2: Integration tests (weight 3)
   - L3: E2E/system tests (weight 5)
   - L4: Smoke/fresh-context tests (weight 5)

   **Interpretation:**
   - `weighted_score >= 0.6` — strong pyramid, L2+ tests present
   - `0.3 <= weighted_score < 0.6` — acceptable, but recommend more integration tests
   - `weighted_score < 0.3` AND all tests are L0-L1 only — **WARN: unit-only test coverage** (feeds into vibe verdict as a WARN signal, not a separate gate)

   **Satisfaction exposure:** The `weighted_score` is also exposed as `satisfaction_score` (with source `"test-pyramid-weighted"`) in the test_pyramid output block AND promoted to the top-level verdict JSON as `satisfaction_score` (verdict schema field, `skills/council/schemas/verdict.json`: number 0.0-1.0, "Probabilistic satisfaction score (0.0 = unsatisfied, 1.0 = fully satisfied). Optional — absent means not computed."). Downstream consumers (e.g., `/validation` STEP 1.8 holdout evaluation) can use `satisfaction_score` as a normalized quality signal.

   **Include in council packet and vibe report output:**
   ```
   ## Test Pyramid Score
   | Level | Count | Weight | Contribution |
   |-------|-------|--------|--------------|
   | L0    | 2     | 1x     | 2            |
   | L1    | 8     | 1x     | 8            |
   | L2    | 0     | 3x     | 0            |
   | L3    | 0     | 5x     | 0            |
   | L4    | 0     | 5x     | 0            |
   | **Total** | **10** | | **10 / 50 = 0.20** |
   WARN: weighted_score 0.20 < 0.3 and all tests are L0-L1 only
   ```

5. **Build coverage table** and include in council packet as `context.test_pyramid`:

```json
"test_pyramid": {
  "coverage": {
    "L0": {"status": "pass", "files": ["test_spec_enforcement.py"]},
    "L1": {"status": "pass", "files": ["test_module.py"]},
    "L2": {"status": "gap", "reason": "crosses subsystem boundary, no integration test"}
  },
  "bug_finding": {
    "BF4_chaos": {"status": "gap", "reason": "external API calls without failure injection"},
    "BF1_property": {"status": "na", "reason": "no data transformations in scope"}
  },
  "weighted_score": 0.20,
  "satisfaction_score": 0.20,
  "satisfaction_source": "test-pyramid-weighted",
  "score_breakdown": {"L0": 2, "L1": 8, "L2": 0, "L3": 0, "L4": 0},
  "max_possible": 50,
  "warn_unit_only": true,
  "verdict": "WARN: weighted_score 0.20 < 0.3, all tests L0-L1 only"
}
```

**Verdict rules:**
- `weighted_score < 0.3` AND all tests L0-L1 only — **WARN: unit-only coverage** (include in council findings)
- Missing L1 on feature code — **WARN** (include in council findings)
- Missing L0 on spec-changing code — **WARN**
- Missing BF4 on boundary code — **WARN** (advisory, not blocking)
- All levels covered with `weighted_score >= 0.6` — no mention needed

When coverage gaps are found, run `/test <module>` to generate test candidates for uncovered code.

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
- Sweep manifest (when `--deep` or `--sweep`, in `context.sweep_manifest` — judges shift to adjudication mode, see `references/deep-audit-protocol.md`)

All council flags pass through: `--quick` (inline), `--mixed` (cross-vendor), `--preset=<name>` (override perspectives), `--explorers=N`, `--debate` (adversarial 2-round), `--tier=<name>` (model cost tier: quality/balanced/budget). See Quick Start examples and `/council` docs.

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

## Council Verdict:

| Council Verdict | Vibe Result | Action |
|-----------------|-------------|--------|
| PASS | Ready to ship | Merge/deploy |
| WARN | Review concerns | Address or accept risk |
| FAIL | Not ready | Fix issues |

### Step 7: Write Vibe Report

**Write to:** `.agents/council/YYYY-MM-DD-vibe-<target>.md` (use `date +%Y-%m-%d`)

Read `references/report-format.md` for the full vibe report markdown template. The report includes: complexity analysis, council verdict table, shared/critical/informational findings, all findings (when `--deep`/`--sweep`), recommendation, and decision checkboxes.

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
   - Extract ALL findings from the council report for structured retry context (group by category if >20):
     ```
     Read the council report. For each finding, format as:
     FINDING: <description> | FIX: <fix or recommendation> | REF: <ref or location>

     Fallback for v1 findings (no fix/why/ref fields):
       fix = finding.fix || finding.recommendation || "No fix specified"
       ref = finding.ref || finding.location || "No reference"
     ```
   - Tell user to fix issues and re-run /vibe, including the formatted findings as actionable guidance.

### Step 9.5: Feed Findings to Flywheel

**If verdict is WARN or FAIL**, persist reusable findings to `.agents/findings/registry.jsonl` and optionally mirror the broader narrative to a learning file.

Registry write rules:

- persist only reusable issues that should change future review or implementation behavior
- require `dedup_key`, provenance, `pattern`, `detection_question`, `checklist_item`, `applicable_when`, and `confidence`
- `applicable_when` must use the controlled vocabulary from the finding-registry contract
- append or merge by `dedup_key`
- use the contract's temp-file-plus-rename atomic write rule

If a broader prose summary still helps, also write the existing anti-pattern learning file to `.agents/learnings/YYYY-MM-DD-vibe-<target>.md`. Skip both if verdict is PASS.

After the registry update, if `hooks/finding-compiler.sh` exists, run:

```bash
bash hooks/finding-compiler.sh --quiet 2>/dev/null || true
```

This keeps the same-session post-mortem path synchronized with the latest reusable findings. `session-end-maintenance.sh` remains the idempotent backstop.

### Step 10: Test Bead Cleanup

After validation completes, clean up stale test beads (`bd list --status=open | grep -iE "test bead|test quest"`) via `bd close` to prevent bead pollution. Skip if `bd` unavailable.

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
    ├── Bug hunt audit (find concrete bugs)
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
| Codex review skipped | `--mixed` not passed, Codex CLI not on PATH, or no uncommitted changes | Codex review is opt-in — pass `--mixed` to enable. Also requires Codex CLI on PATH and uncommitted changes. |
| "No modified files detected" | Clean working tree, no recent commits | Make changes or specify target path explicitly: `/vibe src/auth/`. |
| Spec-compliance judge not spawned | No spec found in beads/plans | Reference bead ID in commit message or create plan doc in `.agents/plans/`. Without spec, vibe uses 2 independent judges (3 with `--deep`). |

---

## Write-Time Quality Hook

The `hooks/write-time-quality.sh` PostToolUse hook runs automatically after every Write/Edit tool call, catching common anti-patterns at edit time rather than review time. It checks:

- **Go:** unchecked errors, `fmt.Print` in library code
- **Python:** bare `except:`, `eval`/`exec`, missing type hints on public functions
- **Shell:** missing `set -euo pipefail`, unquoted variables

The hook is non-blocking (always exits 0) and outputs warnings via JSON. See [references/write-time-quality.md](references/write-time-quality.md) for the full design.

## See Also

- `skills/council/SKILL.md` — Multi-model validation council
- `skills/complexity/SKILL.md` — Standalone complexity analysis
- `skills/bug-hunt/SKILL.md` — Proactive code audit and bug investigation
- `.agents/specs/conflict-resolution-algorithm.md` — Conflict resolution between agent findings
- [test](../test/SKILL.md) — Test generation and coverage analysis
- [perf](../perf/SKILL.md) — Performance profiling and benchmarking

## Reference Documents

- [references/deep-checks.md](references/deep-checks.md)
- [references/verification-report.md](references/verification-report.md)
- [references/write-time-quality.md](references/write-time-quality.md)
- [references/deep-audit-protocol.md](references/deep-audit-protocol.md)
- [references/examples.md](references/examples.md)
- [references/go-patterns.md](references/go-patterns.md)
- [references/go-standards.md](references/go-standards.md)
- [references/json-standards.md](references/json-standards.md)
- [references/markdown-standards.md](references/markdown-standards.md)
- [references/patterns.md](references/patterns.md)
- [references/python-standards.md](references/python-standards.md)
- [references/report-format.md](references/report-format.md)
- [references/rust-standards.md](references/rust-standards.md)
- [references/shell-standards.md](references/shell-standards.md)
- [references/typescript-standards.md](references/typescript-standards.md)
- [references/vibe-coding.md](references/vibe-coding.md)
- [references/vibe-suppressions.md](references/vibe-suppressions.md)
- [references/test-pyramid-weighting.md](references/test-pyramid-weighting.md)
- [references/yaml-standards.md](references/yaml-standards.md)
