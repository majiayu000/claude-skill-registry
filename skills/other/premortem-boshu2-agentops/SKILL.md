---
name: premortem
spine: true
description: 'Stress-test plans before work. Use when: a plan is drafted but not yet executed and you want to surface failure modes, risks, and what would prove it wrong before committing.'
practices:
- adr
- mythical-man-month
- design-by-contract
hexagonal_role: domain
consumes:
- standards
produces:
- result.json
- verdict.json
context_rel:
- kind: shared-kernel
  with: standards
skill_api_version: 1
metadata:
  graph_root: true
  tier: judgment
  dependencies:
  - council
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: full
output_contract: skills/council/schemas/verdict.json
---
# Premortem Skill

> **Purpose:** Is this plan/spec good enough to implement?
> **Mandatory doctrine for 3+ issue epics.** Run premortem before `/crank` on epics with 3+ child issues — operating doctrine, not a hook (AgentOps 3.0 is hookless). 6/6 consecutive positive ROI. Bypass: `--skip-premortem` flag or `AGENTOPS_SKIP_PREMORTEM_GATE=1`.

## Constraints

- **Judge the plan, never the implementation.** This keeps the plan-pawl separate from the acceptance-test and finished-diff pawls, because one verdict cannot prove all three artifacts.
- **Use an independent judge.** The author must not grade their own plan, because shared assumptions make self-review autocorrelated; one-way doors additionally require a different model family.
- **Pre-register kill conditions for irreversible work.** A strategy, experiment, or one-way-door plan must say what evidence changes the decision before deliberation, because an unfalsifiable review is ceremony.
- **Consult the pawl before raising the andon.** WARN, FAIL, or REFUTED is repair evidence: revise the plan and rerun automatically. Raise the andon and route one helper only for a true breaker such as missing authority, unavailable required trust domain after retry, or an impossible invariant.

## Loop position

Pre-flight check between moves **3 (slice plan)** and **4 (TDD per slice)** of the [operating loop](../../docs/architecture/operating-loop.md). Consumes the [slice validation plan](../../docs/templates/slice-validation.md); produces a PASS/WARN/FAIL verdict on the plan AND on the wave-validity rows (distinct write scopes, no shared migration/contract/CLI surface, owner per slice, discard path per slice). A wave can only be claimed parallel if premortem confirms every conflict-free row. FAIL on wave-validity → run slices sequential or send the plan back to `/plan` for re-slicing. Between waves, Premortem accepts only a changed plan from an explicit orchestrator request; Validate and Learn cannot invoke it directly.

Run `/council validate` on a plan or spec to get multi-model judgment before committing to implementation.

## Quick Start

```bash
/premortem                                         # validates most recent plan (inline, no spawning)
/premortem path/to/PLAN.md                         # validates specific plan (inline)
/premortem --deep path/to/SPEC.md                  # 4 judges (thorough review, spawns agents)
/premortem --mixed path/to/PLAN.md                 # cross-vendor (Claude + Codex)
/premortem --preset=architecture path/to/PLAN.md   # architecture-focused review
/premortem --explorers=3 path/to/SPEC.md           # deep investigation of plan
/premortem --debate path/to/PLAN.md                # two-round adversarial review
```

## Execution Steps

### Step 0: Bead-Input Pre-Flight (Mandatory)

When the input to `/premortem` is a bead ID (matches pattern `[a-z]{2,6}-[0-9a-z.]+`) AND complexity is "full" OR the bead is older than 7 days OR the bead description was filed by a prior session, automatically run `ao beads verify <bead-id>` as the very first action. If verify reports any STALE citations, present them to the user and ask for scope re-validation before proceeding. This implements the shared stale-scope validation rule.

### Step 1: Find the Plan/Spec

**If path provided:** Use it directly.

**If no path:** Find most recent plan:
```bash
ls -lt .agents/plans/ 2>/dev/null | head -3
ls -lt .agents/specs/ 2>/dev/null | head -3
```

Use the most recent file. If nothing found, ask user.

### Step 1.4: Retrieve Prior Learnings & Compiled Prevention (Mandatory)

Run `ao lookup` for the plan's domain, then load compiled checks from `.agents/premortem-checks/*.md` (fall back to `.agents/findings/registry.jsonl`). Include matched entries in the council packet as `known_risks` and record `ao metrics cite` influence. Full contract (fail-open rules, section-evidence handling, ranking heuristics, citation lifecycle) in [references/compiled-prevention.md](references/compiled-prevention.md). This file also contains Step 1a (flywheel search, skipped under `--quick`) and Step 1b (PRODUCT.md auto-include).

Fail-open reader behavior is mandatory: missing or empty compiled prevention inputs skip silently; malformed line -> warn and ignore that line; unreadable file -> warn once and continue without findings.

### Step 1a: Flywheel Search (Skip if --quick)

Run the flywheel search from [references/compiled-prevention.md](references/compiled-prevention.md) unless `--quick` is active.

### Step 1b: PRODUCT.md Context (Skip if --quick)

When `PRODUCT.md` exists and full council mode is active, add one product judge: 3 judges total (2 plan-review + 1 product).

### Step 1.5: Fast Path (--quick mode)

**By default, premortem runs inline (`--quick`)** — single-agent structured review, no spawning. This catches real implementation issues at ~10% of full council cost (proven in ag-nsx: 3 actionable bugs found inline that would have caused runtime failures).

In `--quick` mode, skip Steps 1a and 1b as standalone pre-processing phases. If `PRODUCT.md` exists, Step 1b's product context is still loaded inline during the quick review. `--deep`, `--mixed`, `--debate`, and `--explorers` add the dedicated product perspective and wider council fan-out.

To escalate to full multi-judge council, use `--deep` (4 judges) or `--mixed` (cross-vendor).

### Step 1.5.1: Reversibility self-check — size the gate to the stakes (Mandatory)

Before selecting gate depth, **state the plan's blast radius and reversibility in one sentence.** If the plan is
reversible (content recoverable, deletion non-destructive, no shared schema/CLI/contract/migration surface), **say so and
default to the lightest gate** — inline `--quick` plus a single blind sub-agent for the no-self-grading floor (Step 2.9).
Escalate to `--deep` / `--mixed` / full council **only on a named irreversible surface** — a one-way door per the
[blast-radius rule](../../docs/contracts/pawls.md#the-blast-radius-rule-the-list-is-examples-not-the-boundary)
(schema migration, public API, architecture fork, security posture, deletion, mutate-shared-trunk). This is the de-escalation
dual of Step 2.10's escalation rule: 2.10 says *add* rigor for one-way doors; this says *notice and drop* rigor when the op
is reversible. Running a cross-family duel on a reversible doc/refactor is the waterfall the ratchet exists to avoid.

### Step 1.6: Scope Mode Selection

Determine review posture — EXPANSION, HOLD SCOPE, or REDUCTION — and commit `scope_mode: <expansion|hold|reduction>` in the council packet. Auto-detection rules and mode-specific judge prompts are in [references/scope-mode.md](references/scope-mode.md).

### Step 1.7: Load Council FAIL Patterns (Mandatory)

Read [references/council-fail-patterns.md](references/council-fail-patterns.md) for the top 8 council FAIL patterns to check against. These patterns are derived from 124 analyzed FAIL verdicts across 946 council sessions. They apply to both `--quick` and `--deep` modes.

### Step 2: Run Council Validation

Run `/council --quick validate <plan-path>` for reversible work. Use `/council --deep --preset=plan-review validate <plan-path>` for high-stakes work, `/council --mixed --preset=plan-review validate <plan-path>` when cross-family judgment is required, `--explorers=3` for codebase investigation, and `/premortem --debate` for adversarial comparison. An explicit `/premortem --preset=architecture` overrides automatic plan-review routing. Mode composition and judge roles are in [references/mandatory-checks.md](references/mandatory-checks.md#steps-2911-independent-adjudication-and-plan-pawl).

**Checkpoint:** before deliberation, confirm the packet records `scope_mode`, blast radius/reversibility, `author_id`, a distinct `judge_id`, and any required pre-registered `decision_rule`. Do not emit PASS while an invariant is missing.

### Steps 2.4–2.8: Mandatory Council Checks

Five mandatory checks run during council validation — temporal interrogation, error-&-rescue map, council FAIL pattern check, test pyramid coverage, and input validation for enum-like fields. Each has auto-trigger conditions and judge-prompt snippets. Full step text and check tables in [references/mandatory-checks.md](references/mandatory-checks.md).

When a plan introduces a regex, grep, glob, or similar scope predicate, also apply [references/scope-predicate-positive-negative-cases.md](references/scope-predicate-positive-negative-cases.md): require positive and negative examples before approval.

**Narrow-waist slice checks (S1/S3/S4 — FAIL the plan if any fails).** The plan feeds the [narrow-waist micro-cycle](../../docs/architecture/operating-loop.md#the-narrow-waist-micro-cycle-canonical--every-loop-skill-cites-this); confirm each slice can run it:
- **One behavior per slice (S1):** reject any slice that bundles ≥2 Given/When/Then behaviors — send back to `/plan` for re-slicing.
- **ATDD-red gate (S3):** each slice must name a runnable acceptance test authored to fail RED before implementation; a slice with no failing acceptance test is FAIL (no test = no contract).
- **Refactor-separated (S4):** flag any slice that mixes a refactor with a feature, or whose refactor step changes a test — refactor-under-green is its own slice.

**Re-baseline against what exists (mandatory when the plan proposes NEW
construction).** A plan that says "build X" / "X is missing" / "the unbuilt
arm" must prove X does not already exist — `grep`/read the codebase for the
capability, the command, the function, the table — *before* the effort estimate
is accepted. The dominant scoping failure is estimating new construction for
machinery that is already built (and only needs integration), which inflates
effort 2× and risks a duplicate/competing implementation. Judge prompt: "For
each 'build/add/missing' claim, was the absence verified by a search, or
assumed? Name the search." Treat an unverified "it's missing" as a WARN at
minimum; FAIL if the plan's effort/sequencing depends on it.

### Steps 2.9–2.11: Independent adjudication and plan-pawl

Apply the no-self-grading rule, cross-family rule for one-way doors, pre-registered decision rule, and discovery plan-pawl equivalence exactly as specified in [references/mandatory-checks.md](references/mandatory-checks.md#steps-2911-independent-adjudication-and-plan-pawl). A completed discovery plan-pawl duel is the premortem verdict for fanout-class discovery; do not run a duplicate council.

### Step 3: Interpret Council Verdict

| Council Verdict | Premortem Result | Action |
|-----------------|-------------------|--------|
| PASS | Ready to implement | Proceed |
| WARN | Review concerns | Address warnings or accept risk |
| FAIL | Not ready | Fix issues before implementing |

### Step 4: Write Premortem Output

Write to `.agents/council/YYYY-MM-DD-premortem-<topic>.md` using the full template (frontmatter, verdict table, pseudocode-fix format, decision gate) in [references/write-premortem-output.md](references/write-premortem-output.md). That reference also contains Step 4.5 (persist reusable findings to `.agents/findings/registry.jsonl`) and Step 4.6 (copy pseudocode fixes verbatim into plan issues so workers do not reimplement them from scratch).

When Step 4.5 writes reusable findings, include `dedup_key`; do not invoke a repository hook or activate a constraint. `ao membrane digest` refreshes the canonical recurring-catch advisory sink. Mechanical candidates use explicit `ao membrane derive-checks --detector-evidence <json>` replay and remain warn-only shadows until separately measured.

The generated report must preserve this exact heading because downstream validators and ledger readers extract verdicts with a regex anchored to it:

## Council Verdict: PASS / WARN / FAIL

## Output Specification

- **Artifact path:** `.agents/council/`.
- **Filename convention:** `YYYY-MM-DD-premortem-<topic>.md`.
- **Serialization/schema format:** Markdown report using [references/write-premortem-output.md](references/write-premortem-output.md), with council verdict data conforming to `skills/council/schemas/verdict.json`.
- **Validator command:** `bash skills/premortem/scripts/validate.sh && grep -Eq '^## Council Verdict: (PASS|WARN|FAIL)$' .agents/council/YYYY-MM-DD-premortem-<topic>.md`.
- **Downstream handoff:** PASS proceeds to `/implement`; WARN or FAIL returns the plan to its author for repair and automatic re-review. Only a breaker raises the andon or routes one helper.

### Step 5: Record Ratchet Progress

```bash
ao ratchet record premortem 2>/dev/null || true
```

### Step 6: Report to User

Tell the user:
1. Council verdict (PASS/WARN/FAIL)
2. Key concerns (if any)
3. Recommendation
4. Location of premortem report

## Integration with Workflow

```
/plan epic-123
    │
    ▼
/premortem                    ← You are here
    │
    ├── PASS → /implement
    ├── WARN → Review, then /implement or fix
    └── FAIL → Fix plan, re-run /premortem
```

## Quality Checklist

- Every verdict cites concrete plan text and names the failure mode or proof that resolved it.
- Every wave-validity row has non-overlapping write scope, one owner, and a discard path before parallel execution.
- Every irreversible decision has an independent cross-family judge and a decision rule recorded before deliberation.
- WARN, FAIL, and REFUTED routes repair and rerun; only a breaker routes the andon/helper path.

## Examples

See [references/examples.md](references/examples.md) for worked examples (default inline, `--mixed` cross-vendor, auto-find recent, `--deep` high-stakes) and the troubleshooting table (timeouts, FAIL on valid plans, missing product perspectives, gate-blocking, spec-completeness warnings, mandatory-for-epics enforcement).

## Troubleshooting

Use the structured troubleshooting table in [references/examples.md](references/examples.md); repair ordinary verdicts in place and reserve escalation for a breaker.

## See Also

- `skills/council/SKILL.md` — Multi-model validation council
- [`pawl-review`](../pawl-review/SKILL.md) — fresh reviewer execution for the finished diff; this skill attacks the plan before work
- `skills/plan/SKILL.md` — Create implementation plans
- `skills/validate/SKILL.md` — Validate code after implementation

## Reference Documents

- [references/premortem.feature](references/premortem.feature) — Executable spec: plan PASS/WARN/FAIL verdict before work, wave-validity gates parallelism, --quick inline default (soc-qk4b)
- [references/compiled-prevention.md](references/compiled-prevention.md)
- [references/scope-mode.md](references/scope-mode.md)
- [references/mandatory-checks.md](references/mandatory-checks.md)
- [references/scope-predicate-positive-negative-cases.md](references/scope-predicate-positive-negative-cases.md)
- [references/write-premortem-output.md](references/write-premortem-output.md)
- [references/examples.md](references/examples.md)
- [references/council-fail-patterns.md](references/council-fail-patterns.md)
- [references/enhancement-patterns.md](references/enhancement-patterns.md)
- [references/error-rescue-map-template.md](references/error-rescue-map-template.md)
- [references/failure-taxonomy.md](references/failure-taxonomy.md)
- [references/simulation-prompts.md](references/simulation-prompts.md)
- [references/prediction-tracking.md](references/prediction-tracking.md)
- [references/spec-verification-checklist.md](references/spec-verification-checklist.md)
- [references/temporal-interrogation.md](references/temporal-interrogation.md)
