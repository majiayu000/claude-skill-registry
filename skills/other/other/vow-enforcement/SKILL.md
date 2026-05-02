---
name: vow-enforcement
description: 'Three-layer constraint enforcement (soft vows / hard vows / Nen Court). Use when classifying or graduating constraints by reliability.'
version: 1.9.3
alwaysApply: false
category: workflow-methodology
tags:
- enforcement
- constraints
- hooks
- compliance
- governance
dependencies:
- imbue:proof-of-work
- imbue:scope-guard
- imbue:justify
tools: []
usage_patterns:
- constraint-classification
- vow-graduation
- compliance-auditing
- enforcement-design
complexity: intermediate
model_hint: standard
estimated_tokens: 2800
role: hook-target
---

> Rules that depend on willpower fail under pressure.
> Enforcement earns trust by making the right path the
> only path.

# Vow Enforcement

## Table of Contents

- [The Problem](#the-problem)
- [Three Enforcement Layers](#three-enforcement-layers)
- [Vow Classification Protocol](#vow-classification-protocol)
- [Night Market Vow Inventory](#night-market-vow-inventory)
- [Vow Graduation Criteria](#vow-graduation-criteria)
- [Nen Court Protocol](#nen-court-protocol)
- [Integration Points](#integration-points)
- [When to Use](#when-to-use)
- [When NOT to Use](#when-not-to-use)

## The Problem

ODCV-Bench found that agents break self-imposed
constraints 30-50% of the time when goals conflict.
Practitioner consensus confirms: past 150 soft rules,
compliance drops for ALL rules, not just the new ones.

The core insight: "settings.json is a firewall;
CLAUDE.md is an employee handbook." Handbooks work for
guidance. Firewalls work for enforcement. Mixing them
up creates a false sense of security.

## Three Enforcement Layers

| Layer | Mechanism | Compliance | Examples |
|-------|-----------|------------|---------|
| **Soft Vow** | Skill instructions, CLAUDE.md rules | ~80% | "Write tests first", "Keep commits small" |
| **Hard Vow** | Hooks (PreToolUse/PostToolUse), settings.json permissions | ~100% | Block `--no-verify`, enforce file size limits |
| **Nen Court** | External validator agents checking output | Deterministic | Lint checks, test runs, constraint audits |

**Soft Vows** rely on model compliance. Cheap to add
and easy to iterate, but unreliable under goal
conflict. Use when the constraint requires judgment,
violation is annoying but not dangerous, or you are
still learning what the right rule is.

**Hard Vows** block forbidden actions before they
execute via hooks and settings.json permissions. Use
when the constraint is binary, violation causes real
damage, or the soft vow version was violated
repeatedly.

**Nen Court** spawns external validator agents that
audit output after a phase completes. Use when the
constraint requires analysis (not pattern matching),
a hook cannot express the rule, or the check needs
codebase context.

## Vow Classification Protocol

When adding a new constraint, follow this sequence:

### Step 1: Start as Soft Vow

Add the rule to the relevant skill or CLAUDE.md.
This is the cheapest path: zero cost, minutes to
deploy, ~80% compliance.

### Step 2: Monitor Violation Rate

Track violations via execution logs, post-hoc audits
(`imbue:justify` reports), user complaints, and Nen
Court findings from related audits.

### Step 3: Graduate if Needed

If violation rate exceeds 20% over a 30-day window:

- **Binary constraint?** Graduate to Hard Vow (hook).
- **Judgment constraint?** Graduate to Nen Court.
- **Ambiguous?** Try Hard Vow first. If false
  positives exceed 10%, move to Nen Court.

## Night Market Vow Inventory

Current classification of existing constraints:

| Constraint | Current Layer | Target Layer | Notes |
|------------|--------------|--------------|-------|
| Iron Law (no impl without failing test) | Nen Court | Nen Court | `validators/iron_law.py` audits commit order (#406) |
| No `--no-verify` | Hard | Hard | Already hook-enforceable |
| Scope-guard worthiness scoring | Soft | Soft | Requires judgment, not binary |
| Proof-of-work evidence | Nen Court | Nen Court | `validators/proof_of_work.py` checks `[Ex]` refs and status (#406) |
| Bounded discovery reads | Hard | Hard | `vow_bounded_reads.py` with `fcntl.flock` for parallel safety (#418) |
| No AI attribution in commits | Hard | Hard | Hook pattern-matches git commit command |
| Markdown line wrapping at 80 chars | Nen Court | Nen Court | `validators/markdown_wrap.py` flags >80-char prose lines (#406) |
| No emojis in commits | Hard | Hard | Hook pattern-matches git commit command |

### Validator Invocation

The three Nen Court validators are standalone scripts under
`plugins/imbue/validators/`.  Each reads JSON on stdin and writes a
verdict JSON on stdout, using exit codes 0 (pass), 1 (violation), and
2 (inconclusive).  Examples:

```bash
# Markdown wrap audit on a list of files
echo '{"files": ["README.md", "docs/guide.md"]}' \
  | python plugins/imbue/validators/markdown_wrap.py

# Iron Law audit on an explicit commit log
echo '{"commits": [
  {"sha": "abc", "ts": 100, "files": ["tests/test_x.py"]},
  {"sha": "def", "ts": 200, "files": ["src/x.py"]}
]}' | python plugins/imbue/validators/iron_law.py

# Proof-of-work audit on agent output
echo '{"text": "Tested foo [E1] [E2] [E3]. Status: PASS.", "min_evidence": 3}' \
  | python plugins/imbue/validators/proof_of_work.py
```

Mission orchestrator integration: dispatch the appropriate validator
at each phase boundary (see Nen Court Protocol below) and treat exit
code 1 as a blocking gate, exit code 2 as advisory.

## Vow Graduation Criteria

A vow graduates when any of these conditions hold:

1. **Frequency**: 3+ violations detected in 30 days
2. **Severity**: Single violation caused rollback,
   data loss, or broken CI
3. **User escalation**: User explicitly requests
   enforcement ("make it impossible to X")

### Graduation Process

1. Document the violation pattern with evidence
2. Design the hook or validator agent
3. Test the enforcement mechanism in isolation
4. Deploy alongside the soft vow (shadow mode)
5. After 1 week with no false positives, retire the
   soft vow

### Demotion

Hard Vows can be demoted back to Soft if:

- The hook produces > 10% false positive rate
- The constraint was too aggressive (blocking
  legitimate work)
- The underlying concern no longer applies

## Nen Court Protocol

Nen Court runs at phase boundaries in the mission
orchestrator lifecycle:

- After `specify`: validate spec completeness
- After `plan`: validate plan feasibility
- After `execute`: validate Iron Law, additive bias,
  proof-of-work
- Before `pr-prep`: final compliance audit

### Validator Agent Contract

```yaml
validator:
  name: iron-law-court
  constraint: "Tests must drive implementation"
  inputs:
    - git log with timestamps
    - diff of test files vs implementation files
  checks:
    - test file modified before implementation file
    - no test assertions changed to match output
    - coverage did not decrease
  output:
    verdict: pass | violation | inconclusive
    evidence: [list of specific findings]
    recommendation: [action if violation]
```

### Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| **pass** | Constraint satisfied | Phase advances |
| **violation** | Constraint broken with evidence | Phase blocked until fixed or user overrides |
| **inconclusive** | Cannot determine compliance | Flag for human review, do not block |

### User Override

The user can override any Nen Court verdict:

- "Proceed anyway" or "override" clears the block
- The override is logged for future audit
- Frequent overrides on the same constraint suggest
  the constraint needs revision, not more enforcement

## Integration Points

- **`imbue:scope-guard`** -- Soft vow layer. Worthiness
  scoring is a judgment call that belongs in skills.
- **`imbue:proof-of-work`** -- Mixed enforcement.
  Evidence rules are soft; evidence content can be
  verified by a Nen Court validator.
- **`imbue:justify`** -- Post-hoc Nen Court audit.
  Already functions as a validator agent for additive
  bias, Iron Law, and test mutations.
- **Mission Orchestrator** -- Phase-routing with Nen
  Court checkpoints between phases as gates:

```
specify -> [Nen Court: spec review] -> plan
plan    -> [Nen Court: plan review] -> execute
execute -> [Nen Court: justify]     -> pr-prep
```

Phase advances only when Nen Court returns `pass` or
the user provides an explicit override.

## When to Use

- Designing new constraints for the codebase
- Auditing existing constraints for enforcement gaps
- Deciding whether a rule needs a hook or a skill
- Reviewing Nen Court findings at phase boundaries
- Proposing constraint graduations after audits

## When NOT to Use

- One-off rules that apply to a single task
- Constraints that are already hard-enforced and
  working
- Exploratory work where constraints would slow
  learning

## Related Skills

- `imbue:karpathy-principles` - the discursive layer
  this skill governs (vow-enforcement decides which
  principles graduate from skills to hooks)
- `imbue:scope-guard`, `imbue:proof-of-work`,
  `leyline:additive-bias-defense` - example soft vows
  that vow-enforcement classifies and may promote
- See `docs/quality-gates.md#skill-level-quality-gate-composition`
  for the federation this skill governs
