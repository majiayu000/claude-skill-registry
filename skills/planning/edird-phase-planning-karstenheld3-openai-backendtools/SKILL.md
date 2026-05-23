---
name: edird-phase-planning
description: Apply when doing [PLAN], [PARTITION], or planning long-running tasks in sessions
---

# EDIRD Phase Planning

## When to Invoke

- `/build` or `/solve` workflows
- [PLAN] - creating structured approach
- [PARTITION] - breaking IMPL into TASKS
- Planning features, fixes, or research in sessions

## Quick Reference

**Phases:** EXPLORE → DESIGN → IMPLEMENT → REFINE → DELIVER

**Workflow types:** BUILD (code output) | SOLVE (knowledge/decision output)

**Assessment:** COMPLEXITY-LOW/MEDIUM/HIGH | PROBLEM-TYPE (RESEARCH/ANALYSIS/EVALUATION/WRITING/DECISION)

## Phase Gates

### EXPLORE → DESIGN

- [ ] Problem or goal clearly understood
- [ ] Workflow type determined (BUILD or SOLVE)
- [ ] Assessment complete (BUILD: COMPLEXITY | SOLVE: PROBLEM-TYPE)
- [ ] Scope boundaries defined
- [ ] No blocking unknowns requiring [ACTOR] input

### DESIGN → IMPLEMENT

- [ ] Approach documented (outline, spec, or plan)
- [ ] Risky parts proven via POC (if COMPLEXITY-MEDIUM or higher)
- [ ] No open questions requiring [ACTOR] decision
- [ ] For BUILD: SPEC, IMPL, TEST documents created
- [ ] For BUILD: TASKS document created via [PARTITION]
- [ ] For SOLVE: Structure/criteria validated

### IMPLEMENT → REFINE

- [ ] Core work complete (code written / document drafted)
- [ ] For BUILD: Tests pass
- [ ] For BUILD: No TODO/FIXME left unaddressed
- [ ] For SOLVE: All sections drafted
- [ ] Progress committed/saved

### REFINE → DELIVER

- [ ] Self-review complete
- [ ] Verification against spec/rules passed
- [ ] For BUILD COMPLEXITY-MEDIUM+: Critique and reconcile complete
- [ ] For SOLVE: Claims verified, arguments strengthened
- [ ] All found issues fixed

## Workflow Examples

### BUILD (COMPLEXITY-HIGH)

```
[EXPLORE] → [RESEARCH] → [ANALYZE] → [ASSESS] → [SCOPE] → Gate
[DESIGN]  → [PLAN] → [WRITE-SPEC] → [WRITE-IMPL-PLAN] → [PROVE] → [PARTITION] → Gate
[IMPLEMENT] → [IMPLEMENT] → [TEST] → [FIX] → [COMMIT] → Gate (loop until green)
[REFINE] → [REVIEW] → [VERIFY] → [CRITIQUE] → [RECONCILE] → Gate
[DELIVER] → [VALIDATE] → [MERGE] → [CLOSE] → [ARCHIVE]
```

### SOLVE (EVALUATION)

```
[EXPLORE] → [RESEARCH] → [ANALYZE] → [ASSESS] → EVALUATION → Gate
[DESIGN]  → [FRAME] → [OUTLINE] criteria → [DEFINE] framework → Gate
[IMPLEMENT] → [RESEARCH] options → [EVALUATE] → [SYNTHESIZE] → Gate
[REFINE] → [CRITIQUE] → [VERIFY] claims → [IMPROVE] → Gate
[DELIVER] → [CONCLUDE] → [RECOMMEND] → [VALIDATE] → [ARCHIVE]
```

**Note:** COMPLEXITY-LOW skips [PROVE], [CRITIQUE], [RECONCILE].

## Phase Plan Requirements

Plans created via [PLAN] must define:
- **Objectives** - What success looks like
- **Strategy** - How to achieve objectives
- **Deliverables** - Concrete outputs with checkboxes
- **Transitions** - When to move to next phase

**Planning Horizon:**
```
[EXPLORE]   ← Plan now
[DESIGN]    ← Plan now
[IMPLEMENT] ← TBD (after DESIGN gate)
[REFINE]    ← TBD (after IMPLEMENT gate)
[DELIVER]   ← Plan now (shipping tasks from NOTES)
```

## Next Action Logic

1. **Check phase gate** → Pass? → Next phase, first verb
2. **Gate fails?** → Execute verb that addresses unchecked item
3. **Verb outcome:** -OK → next verb | -FAIL → handle | -SKIP → next verb
4. **No more verbs?** → Re-evaluate gate
5. **[DELIVER] done?** → [CLOSE] and [ARCHIVE] if session-based

**Common failure handlers:**
- -FAIL on [RESEARCH], [ASSESS], [PLAN] → [CONSULT] or more [RESEARCH]
- -FAIL on [TEST], [VERIFY] → [FIX] → retry

## Retry Limits

- **COMPLEXITY-LOW**: Infinite retries (until user stops)
- **COMPLEXITY-MEDIUM/HIGH**: Max 5 attempts per phase, then [CONSULT]

## Mandatory Gate Output

Before proceeding to next phase, output:

```markdown
## Gate: [CURRENT_PHASE] → [NEXT_PHASE]

**Complexity**: [LOW/MEDIUM/HIGH] | **Artifacts**: [list created docs]

- [x] Item - Evidence: [specific evidence]
- [ ] Item - BLOCKED: [what's missing]

**Gate status**: PASS | FAIL
```
