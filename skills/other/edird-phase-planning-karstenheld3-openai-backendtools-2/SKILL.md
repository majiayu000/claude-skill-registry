---
name: edird-phase-planning
description: Apply when doing planning for long-running tasks in sessions on top level
---

# EDIRD Phase Planning

## When to Invoke

- `/build` or `/solve` workflows
- [PLAN] - creating high-level plans to achieve goals
- Planning for long agentic runs for features, fixes, or research

**NOT for document writing** - Use dedicated workflows instead:
- `/write-spec` for SPEC documents
- `/write-impl-plan` for IMPL documents
- `/write-test-plan` for TEST documents
- `/write-tasks-plan` for TASKS documents

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

## How to Plan Well

### Goal Decomposition

1. **Start with outcome** - What does "done" look like?
2. **Identify dependencies** - What must complete before what?
3. **Find parallel opportunities** - What can run concurrently?
4. **Size steps for testability** - Each step should be verifiable

### Scope Calibration

- **Too big**: Step takes >30min AWT or touches >3 files → decompose further
- **Too small**: Step takes <2min AWT → combine with adjacent step
- **Right size**: Verifiable outcome, clear done criteria, single responsibility

### Dependency Mapping

Ask for each step:
- What inputs do I need? (determines predecessors)
- What outputs do I produce? (determines successors)
- Can this run while something else runs? (candidate for Concurrent block)

### Common Planning Mistakes

- **Vague objectives**: "Make it work" → Define specific success criteria
- **Missing dependencies**: Steps that assume prior work → Explicit `← Px-Sy`
- **Over-sequencing**: All steps linear when some could parallelize
- **Under-estimating**: No AWT in Strategy → Add time budget
- **Skipping verification**: No test step after implement → Add [TEST] or [VERIFY]

## Next Action Logic

1. **Check phase gate** → Pass? → Next phase, first verb
2. **Gate fails?** → Execute verb that addresses unchecked item
3. **Verb outcome:** -OK → next verb | -FAIL → handle | -SKIP → next verb
4. **No more verbs?** → Re-evaluate gate
5. **[DELIVER] done?** → [CLOSE] and [ARCHIVE] if session-based

**Common failure handlers:**
- -FAIL on [RESEARCH], [ASSESS], [PLAN] → [CONSULT] or more [RESEARCH]
- -FAIL on [TEST], [VERIFY] → [FIX] → retry

## Effort Allocation

### Time Units

- **AWT** (Agentic Work Time) - Agent processing time, excludes user wait
- **HHW** (Human-Hour Work) - Human equivalent effort for task sizing

### Phase Budgets by Complexity

| Phase | LOW | MEDIUM | HIGH |
|-------|-----|--------|------|
| EXPLORE | 5min | 15min | 30min |
| DESIGN | 5min | 30min | 60min |
| IMPLEMENT | varies | varies | varies |
| REFINE | 5min | 15min | 30min |
| DELIVER | 2min | 5min | 10min |

Values are AWT guidelines, not hard limits.

### Diminishing Returns

- Phase takes 2x budget without gate progress → [CONSULT]
- Same step retried 3x without improvement → [CONSULT]
- Research yields no new information after 3 sources → move on

### Retry Limits

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
