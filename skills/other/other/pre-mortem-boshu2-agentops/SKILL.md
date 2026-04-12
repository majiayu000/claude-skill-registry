---
name: pre-mortem
description: 'Validate a plan or spec before implementation using multi-model council. Answer: Is this good enough to implement? Triggers: "pre-mortem", "validate plan", "validate spec", "is this ready".'
skill_api_version: 1
metadata:
  tier: judgment
  dependencies:
    - council  # multi-model judgment
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: full
output_contract: skills/council/schemas/verdict.json
---

# Pre-Mortem Skill

> **Purpose:** Is this plan/spec good enough to implement?

> **Mandatory for 3+ issue epics.** Pre-mortem is enforced by hook when `/crank` is invoked on epics with 3+ child issues. 6/6 consecutive positive ROI. Bypass: `--skip-pre-mortem` flag or `AGENTOPS_SKIP_PRE_MORTEM_GATE=1`.

Run `/council validate` on a plan or spec to get multi-model judgment before committing to implementation.

---

## Quick Start

```bash
/pre-mortem                                         # validates most recent plan (inline, no spawning)
/pre-mortem path/to/PLAN.md                         # validates specific plan (inline)
/pre-mortem --deep path/to/SPEC.md                  # 4 judges (thorough review, spawns agents)
/pre-mortem --mixed path/to/PLAN.md                 # cross-vendor (Claude + Codex)
/pre-mortem --preset=architecture path/to/PLAN.md   # architecture-focused review
/pre-mortem --explorers=3 path/to/SPEC.md           # deep investigation of plan
/pre-mortem --debate path/to/PLAN.md                # two-round adversarial review
```

---

## Execution Steps

### Step 0: Bead-Input Pre-Flight (Mandatory)

When the input to `/pre-mortem` is a bead ID (matches pattern `[a-z]{2,6}-[0-9a-z.]+`) AND complexity is "full" OR the bead is older than 7 days OR the bead description was filed by a prior session, automatically run `ao beads verify <bead-id>` as the very first action. If verify reports any STALE citations, present them to the user and ask for scope re-validation before proceeding. This implements the shared stale-scope validation rule.

### Step 1: Find the Plan/Spec

**If path provided:** Use it directly.

**If no path:** Find most recent plan:
```bash
ls -lt .agents/plans/ 2>/dev/null | head -3
ls -lt .agents/specs/ 2>/dev/null | head -3
```

Use the most recent file. If nothing found, ask user.

### Step 1.4: Retrieve Prior Learnings & Compiled Prevention (Mandatory)

Run `ao lookup` for the plan's domain, then load compiled checks from `.agents/pre-mortem-checks/*.md` (fall back to `.agents/findings/registry.jsonl`). Include matched entries in the council packet as `known_risks` and record `ao metrics cite` influence. Full contract (fail-open rules, section-evidence handling, ranking heuristics, citation lifecycle) in [references/compiled-prevention.md](references/compiled-prevention.md). This file also contains Step 1a (flywheel search, skipped under `--quick`) and Step 1b (PRODUCT.md auto-include).

### Step 1a: Flywheel Search (Skip if --quick)

Run the flywheel search from [references/compiled-prevention.md](references/compiled-prevention.md) unless `--quick` is active.

### Step 1b: PRODUCT.md Context (Skip if --quick)

When `PRODUCT.md` exists and full council mode is active, add one product judge: 3 judges total (2 plan-review + 1 product).

### Step 1.5: Fast Path (--quick mode)

**By default, pre-mortem runs inline (`--quick`)** — single-agent structured review, no spawning. This catches real implementation issues at ~10% of full council cost (proven in ag-nsx: 3 actionable bugs found inline that would have caused runtime failures).

In `--quick` mode, skip Steps 1a and 1b as standalone pre-processing phases. If `PRODUCT.md` exists, Step 1b's product context is still loaded inline during the quick review. `--deep`, `--mixed`, `--debate`, and `--explorers` add the dedicated product perspective and wider council fan-out.

To escalate to full multi-judge council, use `--deep` (4 judges) or `--mixed` (cross-vendor).

### Step 1.6: Scope Mode Selection

Determine review posture — EXPANSION, HOLD SCOPE, or REDUCTION — and commit `scope_mode: <expansion|hold|reduction>` in the council packet. Auto-detection rules and mode-specific judge prompts are in [references/scope-mode.md](references/scope-mode.md).

### Step 1.7: Load Council FAIL Patterns (Mandatory)

Read [references/council-fail-patterns.md](references/council-fail-patterns.md) for the top 8 council FAIL patterns to check against. These patterns are derived from 124 analyzed FAIL verdicts across 946 council sessions. They apply to both `--quick` and `--deep` modes.

### Step 2: Run Council Validation

**Default (inline, no spawning):**
```
/council --quick validate <plan-path>
```
Single-agent structured review. Catches real implementation issues at ~10% of full council cost. Sufficient for most plans (proven across 6+ epics).

Default (2 judges with plan-review perspectives) applies when you intentionally run non-quick council mode.

**With --deep (4 judges with plan-review perspectives):**
```
/council --deep --preset=plan-review validate <plan-path>
```
Spawns 4 judges:
- `missing-requirements`: What's not in the spec that should be? What questions haven't been asked?
- `feasibility`: What's technically hard or impossible here? What will take 3x longer than estimated?
- `scope`: What's unnecessary? What's missing? Where will scope creep?
- `spec-completeness`: Are boundaries defined? Do conformance checks cover all acceptance criteria? Is the plan mechanically verifiable?

Use `--deep` for high-stakes plans (migrations, security, multi-service, 7+ issues).

**With --mixed (cross-vendor):**
```
/council --mixed --preset=plan-review validate <plan-path>
```
3 Claude + 3 Codex agents for cross-vendor plan validation with plan-review perspectives.

**With explicit preset override:**
```
/pre-mortem --preset=architecture path/to/PLAN.md
```
Explicit `--preset` overrides the automatic plan-review preset. Uses architecture-focused personas instead.

**With explorers:**
```
/council --deep --preset=plan-review --explorers=3 validate <plan-path>
```
Each judge spawns 3 explorers to investigate aspects of the plan's feasibility against the codebase. Useful for complex migration or refactoring plans.

**With debate mode:**
```
/pre-mortem --debate
```
Enables adversarial two-round review for plan validation. Use for high-stakes plans where multiple valid approaches exist. See `/council` docs for full --debate details.

### Steps 2.4–2.8: Mandatory Council Checks

Five mandatory checks run during council validation — temporal interrogation, error-&-rescue map, council FAIL pattern check, test pyramid coverage, and input validation for enum-like fields. Each has auto-trigger conditions and judge-prompt snippets. Full step text and check tables in [references/mandatory-checks.md](references/mandatory-checks.md).

### Step 3: Interpret Council Verdict

| Council Verdict | Pre-Mortem Result | Action |
|-----------------|-------------------|--------|
| PASS | Ready to implement | Proceed |
| WARN | Review concerns | Address warnings or accept risk |
| FAIL | Not ready | Fix issues before implementing |

### Step 4: Write Pre-Mortem Output

Write to `.agents/council/YYYY-MM-DD-pre-mortem-<topic>.md` using the full template (frontmatter, verdict table, pseudocode-fix format, decision gate) in [references/write-pre-mortem-output.md](references/write-pre-mortem-output.md). That reference also contains Step 4.5 (persist reusable findings to `.agents/findings/registry.jsonl`) and Step 4.6 (copy pseudocode fixes verbatim into plan issues so workers do not reimplement them from scratch).

When Step 4.5 writes reusable findings, include `dedup_key` and refresh compiled findings with `finding-compiler.sh` when that hook exists.

The generated report must preserve this exact heading because `ao rpi phased` extracts verdicts with a regex anchored to it:

## Council Verdict: PASS / WARN / FAIL

### Step 5: Record Ratchet Progress

```bash
ao ratchet record pre-mortem 2>/dev/null || true
```

### Step 6: Report to User

Tell the user:
1. Council verdict (PASS/WARN/FAIL)
2. Key concerns (if any)
3. Recommendation
4. Location of pre-mortem report

---

## Integration with Workflow

```
/plan epic-123
    │
    ▼
/pre-mortem                    ← You are here
    │
    ├── PASS → /implement
    ├── WARN → Review, then /implement or fix
    └── FAIL → Fix plan, re-run /pre-mortem
```

---

## Examples & Troubleshooting

See [references/examples.md](references/examples.md) for worked examples (default inline, `--mixed` cross-vendor, auto-find recent, `--deep` high-stakes) and the troubleshooting table (timeouts, FAIL on valid plans, missing product perspectives, gate-blocking, spec-completeness warnings, mandatory-for-epics enforcement).

## Troubleshooting

See [references/examples.md](references/examples.md) for the troubleshooting table.

---

## See Also

- `skills/council/SKILL.md` — Multi-model validation council
- `skills/plan/SKILL.md` — Create implementation plans
- `skills/vibe/SKILL.md` — Validate code after implementation

## Reference Documents

- [references/compiled-prevention.md](references/compiled-prevention.md)
- [references/scope-mode.md](references/scope-mode.md)
- [references/mandatory-checks.md](references/mandatory-checks.md)
- [references/write-pre-mortem-output.md](references/write-pre-mortem-output.md)
- [references/examples.md](references/examples.md)
- [references/council-fail-patterns.md](references/council-fail-patterns.md)
- [references/enhancement-patterns.md](references/enhancement-patterns.md)
- [references/error-rescue-map-template.md](references/error-rescue-map-template.md)
- [references/failure-taxonomy.md](references/failure-taxonomy.md)
- [references/simulation-prompts.md](references/simulation-prompts.md)
- [references/prediction-tracking.md](references/prediction-tracking.md)
- [references/spec-verification-checklist.md](references/spec-verification-checklist.md)
- [references/temporal-interrogation.md](references/temporal-interrogation.md)
- Shared stale-scope validation rule — re-validate inherited scope estimates against HEAD before acting on deferred beads or handoff docs.
