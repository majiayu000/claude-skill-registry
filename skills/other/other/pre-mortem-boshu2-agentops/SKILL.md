---
name: pre-mortem
description: 'Validate a plan or spec before implementation using multi-model council. Answer: Is this good enough to implement? Triggers: "pre-mortem", "validate plan", "validate spec", "is this ready".'
metadata:
  tier: judgment
  dependencies:
    - council  # multi-model judgment
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

### Step 1: Find the Plan/Spec

**If path provided:** Use it directly.

**If no path:** Find most recent plan:
```bash
ls -lt .agents/plans/ 2>/dev/null | head -3
ls -lt .agents/specs/ 2>/dev/null | head -3
```

Use the most recent file. If nothing found, ask user.

### Step 1.5: Default Inline Mode

**By default, pre-mortem runs inline (`--quick`)** — single-agent structured review, no spawning. This catches real implementation issues at ~10% of full council cost (proven in ag-nsx: 3 actionable bugs found inline that would have caused runtime failures).

**Skip Steps 1a and 1b** (knowledge search, product context) unless `--deep`, `--mixed`, `--debate`, or `--explorers` is set. These pre-processing steps are for multi-judge council packets only.

To escalate to full multi-judge council, use `--deep` (4 judges) or `--mixed` (cross-vendor).

### Step 1a: Search Knowledge Flywheel

**Skip unless `--deep`, `--mixed`, or `--debate`.**

```bash
if command -v ao &>/dev/null; then
    ao search "plan validation lessons <goal>" 2>/dev/null | head -10
fi
```
If ao returns prior plan review findings, include them as context for the council packet. Skip silently if ao is unavailable or returns no results.

### Step 1b: Check for Product Context

**Skip unless `--deep`, `--mixed`, or `--debate`.**

```bash
if [ -f PRODUCT.md ]; then
  # PRODUCT.md exists — include product perspectives alongside plan-review
fi
```

When `PRODUCT.md` exists in the project root AND the user did NOT pass an explicit `--preset` override:
1. Read `PRODUCT.md` content and include in the council packet via `context.files`
2. Add a single consolidated `product` perspective to the council invocation:
   ```
   /council --preset=plan-review --perspectives="product" validate <plan-path>
   ```
   This yields 3 judges total (2 plan-review + 1 product). The product judge covers user-value, adoption-barriers, and competitive-position in a single review.
3. With `--deep`: 5 judges (4 plan-review + 1 product).

When `PRODUCT.md` exists BUT the user passed an explicit `--preset`: skip product auto-include (user's explicit preset takes precedence).

When `PRODUCT.md` does not exist: proceed to Step 2 unchanged.

> **Tip:** Create `PRODUCT.md` from `docs/PRODUCT-TEMPLATE.md` to enable product-aware plan validation.

### Step 2: Run Council Validation

**Default (inline, no spawning):**
```
/council --quick validate <plan-path>
```
Single-agent structured review. Catches real implementation issues at ~10% of full council cost. Sufficient for most plans (proven across 6+ epics).

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

### Step 3: Interpret Council Verdict

| Council Verdict | Pre-Mortem Result | Action |
|-----------------|-------------------|--------|
| PASS | Ready to implement | Proceed |
| WARN | Review concerns | Address warnings or accept risk |
| FAIL | Not ready | Fix issues before implementing |

### Step 4: Write Pre-Mortem Report

**Write to:** `.agents/council/YYYY-MM-DD-pre-mortem-<topic>.md`

```markdown
# Pre-Mortem: <Topic>

**Date:** YYYY-MM-DD
**Plan/Spec:** <path>

## Council Verdict: PASS / WARN / FAIL

| Judge | Verdict | Key Finding |
|-------|---------|-------------|
| Missing-Requirements | ... | ... |
| Feasibility | ... | ... |
| Scope | ... | ... |

## Shared Findings
- ...

## Concerns Raised
- ...

## Recommendation
<council recommendation>

## Decision Gate

[ ] PROCEED - Council passed, ready to implement
[ ] ADDRESS - Fix concerns before implementing
[ ] RETHINK - Fundamental issues, needs redesign
```

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

## Examples

### Validate a Plan (Default — Inline)

**User says:** `/pre-mortem .agents/plans/2026-02-05-auth-system.md`

**What happens:**
1. Agent reads the auth system plan
2. Runs `/council --quick validate <plan-path>` (inline, no spawning)
3. Single-agent structured review finds missing error handling for token expiry
4. Council verdict: WARN
5. Output written to `.agents/council/2026-02-13-pre-mortem-auth-system.md`

**Result:** Fast pre-mortem report with actionable concerns. Use `--deep` for high-stakes plans needing multi-judge consensus.

### Cross-Vendor Plan Validation

**User says:** `/pre-mortem --mixed .agents/plans/2026-02-05-auth-system.md`

**What happens:**
1. Agent runs mixed-vendor council (3 Claude + 3 Codex)
2. Cross-vendor perspectives catch platform-specific issues
3. Verdict: PASS with 2 warnings

**Result:** Higher confidence from cross-vendor validation before committing resources.

### Auto-Find Recent Plan

**User says:** `/pre-mortem`

**What happens:**
1. Agent scans `.agents/plans/` for most recent plan
2. Finds `2026-02-13-add-caching-layer.md`
3. Runs inline council validation (no spawning, ~10% of full council cost)
4. Records ratchet progress

**Result:** Frictionless validation of most recent planning work.

### Deep Review for High-Stakes Plan

**User says:** `/pre-mortem --deep .agents/plans/2026-02-05-migration-plan.md`

**What happens:**
1. Agent reads the migration plan
2. Searches knowledge flywheel for prior migration learnings
3. Checks PRODUCT.md for product context
4. Runs `/council --deep --preset=plan-review validate <plan-path>` (4 judges)
5. Council verdict with multi-perspective consensus

**Result:** Thorough multi-judge review for plans where the stakes justify spawning agents.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Council times out | Plan too large or complex for judges to review in allocated time | Split plan into smaller epics or increase timeout via council config |
| FAIL verdict on valid plan | Judges misunderstand domain-specific constraints | Add context via `--perspectives-file` with domain explanations |
| Product perspectives missing | PRODUCT.md exists but not included in council packet | Verify PRODUCT.md is in project root and no explicit `--preset` override was passed |
| Pre-mortem gate blocks /crank | Epic has 3+ issues and no pre-mortem ran | Run `/pre-mortem` before `/crank`, or use `--skip-pre-mortem` flag (not recommended) |
| Spec-completeness judge warns | Plan lacks Boundaries or Conformance Checks sections | Add SDD sections or accept WARN (backward compatibility — not a failure) |
| Mandatory for epics enforcement | Hook blocks /crank on 3+ issue epic without pre-mortem | Run `/pre-mortem` first, or set `AGENTOPS_SKIP_PRE_MORTEM_GATE=1` to bypass |

---

## See Also

- `skills/council/SKILL.md` — Multi-model validation council
- `skills/plan/SKILL.md` — Create implementation plans
- `skills/vibe/SKILL.md` — Validate code after implementation
