---
name: self-evolve
description: >
  The single config quality skill. Two modes: (1) Default — review/wire pending self-improvement proposals. (2) Audit — analyzes skills, rules, CLAUDE.md, project refs, hooks, and agents against the actual codebase to find inaccuracies, trigger overlaps, stale references, and weak rules, then fixes them. Trigger on 'self-evolve', 'evolve', 'config health check', 'audit config', 'check claude setup', 'apply this rule', 'reorganize rules', 'ok' (when proposals are pending). NOT for improving individual skills (use skill-creator), diagnosing code bugs (use diagnose), or fixing broken code (use fix).
argument-hint: scope-or-focus-area
---

ultrathink.

## Wire Mode: Apply Self-Improvement Proposals

When scope is `(none)`, or when pending proposals exist and user says "ok":

**Fetching proposals**:
```bash
python3 .claude/hooks/self-improve/self_improve_db.py resolve list
```

### Step 0: Consolidate before showing

User attention is finite — showing 12 proposals when 4 are duplicates, 3 already exist in rules, and 2 are noise wastes their focus on what matters. Before presenting anything, read the existing config (`.claude/rules/`, CLAUDE.md, CLAUDE.local.md, active skills) to understand what's already there. Then filter: proposals already covered by existing rules, duplicates of each other, and low-value noise that wouldn't improve agent behavior. Merge proposals addressing the same pattern into one entry with the clearest rationale.

Tell the user what you filtered: "Showing X of Y proposals (Z filtered)."

After user finishes reviewing visible proposals, batch-reject the filtered ones:
```bash
python3 .claude/hooks/self-improve/self_improve_db.py resolve <id1>,<id2>,... rejected
```

For each shown proposal, ask the user to approve or reject.

### Step 1: Classify — where does it belong?

| Test | Question | If Yes |
|------|----------|--------|
| **Rule test** | "Will an agent still produce incorrect code without this, even with the skill active?" | → Rule (`.claude/rules/`) |
| **Skill test** | "Is this a repeatable process/workflow, not a constraint?" | → Skill — rare |
| **On-demand ref** | "Is this project-specific architecture/context, not a behavioral rule?" | → Reference file pointed from CLAUDE.md |
| **Personal pref** | "Is this specific to this user, not team-shared?" | → `CLAUDE.local.md` (gitignored) |
| **Default** | None clearly match? | → Rule (safest default) |

~80% of proposals become rules — the pipeline detects behavioral corrections, and corrections are rules by definition.

### Step 2: Read existing content, check for overlap

Read all files in the target location. Scan for semantic overlap — does an existing rule/section already cover this?

### Step 3: Place — merge or add

- **If overlap exists**: merge into existing entry — expand/refine/strengthen, don't create near-duplicates
- **If distinct**: add under the most relevant section header

**Writing quality** — proposals describe specific incidents, but rules must work for the general case:

1. **Generalize from the incident.** The proposal says "Claude changed the pass dot when user meant N/A dot." The rule should address the *class*: "When multiple UI elements match an ambiguous reference, confirm which one before changing any." Don't encode the specific incident — encode the pattern.
2. **Ground in reasoning, not commands.** "ALWAYS confirm ambiguous references" is brittle — the agent doesn't know when it applies. "Because acting on the wrong target wastes a correction cycle, confirm which element when multiple candidates match" gives the agent judgment for edge cases.
3. **Trim while merging.** When adding to an existing rule file, read what's already there. If existing entries are redundant with the new content or with each other, consolidate. The goal after merging is a *tighter* file, not a longer one.
4. **Watch for accumulation.** If 3+ proposals have landed in the same file or section, that's a restructuring signal — the section may need splitting, or the underlying skill needs fixing instead of piling on more rules.
5. **Think from the agent's perspective.** Before finalizing, ask: "If I were an agent reading this rule for the first time with no context about the incident, would I understand *when* and *why* to apply it?" If the answer requires knowledge of the original proposal, rewrite.
6. **Re-read with fresh eyes.** After merging, re-read the entire section (not just your addition). Does the new content flow with the existing entries, or does it feel bolted on? Revise for coherence.

### Step 4: Verify — smoke test

Use the proposal's `rationale` to construct a minimal replay prompt that would trigger the same mistake. Spawn a subagent with the new rule, give it the prompt, check if it avoids the failure. If it fails, revise once. If still fails, flag to user. Keep this fast — one prompt, one check.

### Step 5: Resolve

```bash
python3 .claude/hooks/self-improve/self_improve_db.py resolve <id>[,<id>,...] approved  # or rejected
```

### Step 6: Confirm

Tell the user: **what** was placed, **where** (file + section), **why** that location, and **whether verification passed**.

### Manual reorganization

When invoked for rule reorganization (not proposals): read all `.claude/rules/`, identify duplicates/misplaced rules, propose consolidation plan, apply on approval.

---

## Audit Mode: Proactive Config Analysis

When scope is `full`, `skills`, `rules`, `claude-md`, or `quick`. Also when `(none)` and no pending proposals found.

### Phase 1: Understand the Project

1. Read `package.json`, `pyproject.toml`, `go.mod`, or equivalent — know the stack
2. Scan top-level directory structure — know the architecture
3. Read CLAUDE.md — know what config claims about the project
4. Read `.claude/settings.json` — know what hooks are configured
5. If `.claude/hooks/self-improve/` exists, check for pending proposals: `python3 .claude/hooks/self-improve/self_improve_db.py resolve list`

### Phase 2: Analyze

Read `references/quality-dimensions.md` for mechanical check scripts, staleness signals, and conflict resolution rules. Then run per-component analysis — see `references/audit-guide.md` for the full checklist covering skills, rules, CLAUDE.md, CLAUDE.local.md, and hooks.

### Phase 3: Fix

**Severity**: CRITICAL (wrong code/skill, broken refs) → fix. MODERATE (suboptimal output) → fix if easy. LOW (style) → report only.

Fix: broken refs, inaccurate facts, trigger overlaps, weak/stale rules, redundant cross-layer content, broken hooks, orphaned project refs.
Don't fix: workflow skill descriptions (report for skill-creator), substantial completeness gaps (report as recommendation), things that work.

### Phase 4: Verify

For each fix: re-read, re-run the specific check, confirm it passes. Check no new broken refs introduced.

### Phase 5: Report

Use the report template in `references/audit-guide.md § Report Template`. Health verdicts: HEALTHY (0 CRITICAL, ≤2 MODERATE) | NEEDS ATTENTION (unfixed MODERATE or 1 CRITICAL) | CRITICAL ISSUES (2+ CRITICAL).

## Constraints

- **Stay in your lane.** Config quality + proposals only. Not for creating skills, priming projects, or fixing code bugs.
- **Fix what's broken, not what's working.** Respect knowledge layers: skills teach, rules guard, refs provide context.
- **Don't bloat.** If a fix requires 50+ new lines, report as recommendation.
- **Don't weaken when merging.** Combined version must be at least as strong as the original.
