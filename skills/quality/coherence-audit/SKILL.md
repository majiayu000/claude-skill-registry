# Coherence Audit Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-25

Guide systematic coherence audits when discrepancies reveal potential systemic issues.

## When to Activate

Use this skill when:
- Discrepancy found between documentation and reality
- "If you see one bug, there are many more"
- Post-epic validation failure
- Documentation drift detected
- Coherence failure identified
- README doesn't match actual state
- Invoked by epic-validation skill

## Why This Methodology Works

This audit is counter-intuitive. When you see a bug, instinct says "fix it now." The methodology says "wait."

The constraint is the feature, not the obstacle. By forcing understanding before action, you:
- Find related issues (not just the obvious one)
- Discover root causes (not just symptoms)
- Fix the process (not just the bug)
- Create institutional memory (not just a commit)

The 45 minutes spent understanding produces compound returns. The 30-second fix produces a single commit.

**When you feel the urge to edit immediately, that's the signal to trust the methodology.** You'll fix it in Phase 4. First, understand.

## Core Principles

### 1. Understanding Must Precede Action

Complete phases 1-3 before touching any files.

Premature fixing misses related issues, root causes, and process improvements. If phases 1-3 are done properly, Phase 4 becomes mechanical. The hard work is understanding; the fix is usually trivial.

### 2. Ground Truth as Foundation

Start with what actually exists, not what documentation claims.

`ls | wc -l` is not an opinion. Documentation describes intent; the filesystem describes reality. Never trust claims about state - inspect directly.

### 3. Cross-Reference for Systematic Discovery

Compare every claim against ground truth using exhaustive check matrix.

The pattern of what's correct vs incorrect reveals the failure mechanism. If onboarding.md is correct but README.md is wrong, that tells you someone updated one but forgot the other - a different failure than nobody updating anything.

### 4. Object vs Meta Distinction

Separate "fix the thing" (Phase 4) from "fix the process" (Phase 5).

Most people stop at Phase 4. Phase 5 is where you get compound returns - every future project benefits from the process improvement. Fixing a README is a point fix; adding a coherence check to the quality checklist closes a class of bugs.

### 5. Root Cause Reveals Mechanism

Trace backward from symptom through causal chain to systemic failure.

The README error is the leaf of a tree. "Tools created but not integrated" is the root. Without root cause analysis, you're playing whack-a-mole with symptoms.

### 6. Verification as Closure

Re-run discovery method to prove zero discrepancies remain.

The same systematic method that found bugs must confirm they're fixed. This is proof of correctness, not just "checking your work."

---

## Workflow

```
TRIGGER → INVENTORY → CROSS-REFERENCE → ROOT-CAUSE → OBJECT-FIX → PROCESS-FIX → POST-MORTEM → VERIFY
                ↑                                                                              ↓
                └──────────────────── if discrepancies remain ─────────────────────────────────┘
```

### Phase 1: Ground Truth Inventory

**Objective:** Establish what actually exists in the repository right now.

1. Count actual items (files, skills, tests, etc.) - no assumptions
2. List all relevant contents by direct inspection
3. Capture current state of documentation claims
4. Create objective baseline that cannot be argued with

**Outputs:** Inventory document with counts and lists; ground truth baseline for comparison

### Phase 2: Cross-Reference Check

**Objective:** Compare every claim against ground truth systematically.

1. Build exhaustive check matrix (every claim vs ground truth)
2. Check each source of claims (README, docs, code comments, configs)
3. Record discrepancies with specific file:line references
4. Note pattern of correct vs incorrect (reveals failure mechanism)

**Outputs:** Discrepancy report with file:line references; pattern analysis

### Phase 3: Root Cause Analysis

**Objective:** For each discrepancy, trace backward to understand mechanism.

Answer the five questions:

1. **Which task should have done this?**
2. **Did acceptance criteria include it?**
3. **Did validation check it?**
4. **What should have caught this?**
5. **Why didn't it?**

Then:
- Identify causal chain from symptom to systemic failure
- Look for false closures (acceptance criteria not actually met)

**Outputs:** Root cause analysis; causal chain documentation; process gaps identified

### Phase 4: Object-Level Fixes

**Objective:** Fix all discrepancies found (the easy part).

1. Fix each discrepancy identified in Phase 2
2. Commit with clear messages referencing the audit
3. This should be mechanical if phases 1-3 done well

**Outputs:** Commits fixing all discrepancies

### Phase 5: Process-Level Fixes

**Objective:** Fix the system that produced the bug (the important part).

> Remember: You're fixing the system that produces bugs, not just the bug itself. Phase 4 fixes symptoms; Phase 5 closes bug classes.

1. For each process gap from Phase 3, implement a fix
2. Update checklists, validation steps, workflows
3. Add automated checks where manual checks failed

**Outputs:** Process improvements committed; future projects protected

### Phase 6: Post-Mortem Documentation

**Objective:** Create permanent record for institutional memory.

1. Write post-mortem with timeline, root causes, fixes, lessons
2. Include "Lessons Learned" section with actionable principles
3. File at `docs/postmortems/YYYY-MM-DD-<slug>.md`
4. This is knowledge extraction, not just documentation

**Outputs:** Post-mortem document committed

### Phase 7: Verification

**Objective:** Re-run Phase 2 to prove zero discrepancies remain.

1. Execute all cross-reference checks from Phase 2
2. Confirm each previously-found discrepancy is resolved
3. If new discrepancies found, return to Phase 4
4. Only complete when all checks pass

**Outputs:** Verification report showing zero discrepancies

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| One Bug Means Many | Single discrepancy found | Run full audit, not point fix | Related issues hide near visible ones |
| Resist Immediate Fix | Urge to edit rises | Note it, continue through Phase 3 | Waiting is discipline, not laziness |
| The Contrast Reveals | Some docs correct, some wrong | Note which and analyze why | Pattern shows failure mechanism |
| Fix Is Phase 4 | You understand full scope | Now edit files | Understanding makes fixes mechanical |
| Recursion for Meta-Fixes | Process gap identified | Fix the system that produces bugs | Phase 5 closes bug classes |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Description | Consequence | Instead |
|--------------|-------------|-------------|---------|
| Jump to Fix | Edit file as soon as bug seen | Miss related issues, root cause, process fixes | Complete phases 1-3 first |
| Stop at Object Level | Fix README, declare done | Same bug class recurs | Always do Phase 5 |
| Skip Post-Mortem | "I fixed it, why document?" | No institutional memory | Write lessons learned |
| Trust Claims | Read docs to learn what exists | Docs may be stale | Inspect filesystem directly |
| Partial Verification | Check only what you fixed | Other discrepancies remain | Re-run ALL Phase 2 checks |
| Blame Without Analysis | "Someone forgot to update" | Doesn't explain why validation missed it | Trace full causal chain |

---

## Quality Checklist

- [ ] Ground truth inventory complete (files counted, contents listed)
- [ ] Cross-reference matrix exhaustive (all claim sources checked)
- [ ] All discrepancies identified with file:line references
- [ ] Root cause chain traced for each discrepancy (five questions answered)
- [ ] Process gaps identified (what should have caught this?)
- [ ] Object-level fixes committed
- [ ] At least one process-level fix implemented
- [ ] Post-mortem document created and committed
- [ ] Phase 2 re-run shows zero discrepancies
- [ ] All changes pushed to remote

---

## Examples

### Example 1: README Skill Count Drift (Actual Case)

**Trigger:** README says "15 skills" but 23 exist

**Phase 1 - Inventory:**
```bash
ls skills/ | wc -l           # → 23 (ground truth)
grep "skills bundled" README.md    # → "15 skills"
grep "skills bundled" docs/onboarding.md  # → "23 skills"
```

**Phase 2 - Cross-Reference:**
| Source | Claim | Actual | Status |
|--------|-------|--------|--------|
| README.md:41 | 15 skills | 23 | DISCREPANCY |
| README.md:130 | 15 skills | 23 | DISCREPANCY |
| onboarding.md | 23 skills | 23 | PASS |
| skills.rs | 23 bundled | 23 | PASS |

**Phase 3 - Root Cause:**
1. Which task? beadsmith-e12.11 should have updated README
2. Acceptance criteria? "documentation updated" (ambiguous - said "README or docs")
3. Validation check? epic-validation skill would check this
4. What should have caught? epic-validation Phase 2: "Check README mentions features"
5. Why didn't it? Skill created but never invoked - not integrated into beads-loop

**Root cause:** False bead closure (e12.13 created tool but didn't integrate it)

**Phase 4 - Object Fixes:**
- Edit README.md: 15 → 23
- Add 8 missing skills to table

**Phase 5 - Process Fixes:**
- Update beads-loop step 1: invoke epic-validation at 100%
- Add Documentation Coherence section to quality checklist

**Phase 6 - Post-Mortem:**
- Created: `docs/postmortems/2026-01-25-bdd-epic-coherence.md`

**Phase 7 - Verify:**
- Re-run all checks → zero discrepancies

### Example 2: API Contract Mismatch

**Trigger:** Client code calls endpoint that returns 404

**Phase 1:** List actual server endpoints (ground truth)

**Phase 2:** Compare client calls, API docs, server routes
- Find: `/api/users/list` in client, `/api/users` in server

**Phase 3:** Trace to PR that renamed endpoint without updating clients
- Root cause: No contract validation in CI

**Phase 4:** Fix client to call correct endpoint

**Phase 5:** Add CI check that validates client/server contract match

**Phase 6:** Post-mortem with "endpoint rename" checklist

**Phase 7:** Verify all client calls resolve

---

## References

- Post-mortem: `docs/postmortems/2026-01-25-bdd-epic-coherence.md` (first application)
- Related: `epic-validation` skill (invokes this skill)
- Related: `decision-audit` skill (recording quality trade-offs)

---

## Metadata

| Property | Value |
|----------|-------|
| Domain | quality-assurance |
| Energy | high |
| Time Estimate | 30-90 minutes |
| Invoked By | epic-validation, user command |
