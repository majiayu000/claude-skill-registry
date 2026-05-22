---
name: bug-diagnosis
version: 2.0.1
description: Quick triage skill for initial bug assessment and user-reported issues. Use for bug reports, error reports, quick diagnosis, initial triage, "what's causing", "why is this failing". For systematic multi-file debugging with verification protocols, use `debugging` skill instead.
infer: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, WebFetch, WebSearch, TodoWrite
---

> **Skill Variant:** Use this skill for **quick bug triage and interactive debugging** with user feedback. For systematic autonomous debugging workflows with 4-phase protocol and verification gates, use `debugging` skill instead. For feature investigation without fixes, use `feature-investigation`.

## Disambiguation

- For **systematic multi-file debugging** with verification protocols -> use `debugging`
- For **feature investigation** without fixes -> use `feature-investigation`
- This skill focuses on **quick triage** of user-reported bugs

# Bug Diagnosis & Debugging

You are to operate as an expert full-stack .NET Angular debugging engineer to diagnose, debug, and fix the bug described in `[bug-description-or-bug-info-file-path]`.

**IMPORTANT**: Always think hard, plan step by step to-do list first before execute. Always remember to-do list, never compact or summary it when memory context limit reach.

**Prerequisites:** **MUST READ** `.claude/skills/shared/anti-hallucination-protocol.md` before executing.

---

## PHASE 1: EXTERNAL MEMORY-DRIVEN BUG ANALYSIS

Build a structured knowledge model in a Markdown analysis file at `.ai/workspace/analysis/[semantic-name].analysis.md`.

### PHASE 1A: INITIALIZATION AND DISCOVERY

1. **Initialize** the analysis file with: Metadata, Progress, Errors, File List, Knowledge Graph sections
2. **Discovery searches**: Semantic and grep search all error keywords. Prioritize: Domain Entities, Commands, Queries, Event Handlers, Controllers, Background Jobs, Consumers, Frontend Components

### PHASE 1B: SYSTEMATIC FILE ANALYSIS

1. Count total files, split into batches of 10 in priority order
2. For each file, document: filePath, type, content, symbols, dependencies, businessContext, errorPatterns, stackTraceRelevance, validationLogic

### PHASE 1C: OVERALL ANALYSIS

Write comprehensive summary showing: end-to-end workflows, error propagation paths, integration points and failure points.

---

## PHASE 2: ROOT CAUSE ANALYSIS & FIX STRATEGY

### Root Cause Dimensions

1. **Technical**: Code defects, architectural issues
2. **Business Logic**: Rule violations, validation failures
3. **Data**: Data corruption, integrity violations
4. **Integration**: API contract violations, communication failures

### Generate Fix Strategy

Document alternatives with: suggestedFix, riskAssessment, regressionMitigation, testingStrategy, rollbackPlan.

---

## PHASE 3: APPROVAL GATE

**CRITICAL**: Present root cause analysis and fix strategy for explicit user approval before implementation.

---

## PHASE 4: DEBUGGING EXECUTION

Once approved: execute fix plan, make minimal targeted changes, follow platform patterns.

---

## Platform Error Patterns Reference

### Backend Validation
```csharp
return base.Validate()
    .And(_ => condition, "Error message")
    .AndAsync(async req => await ValidateAsync(req));

await repository.GetByIdAsync(id).EnsureFound($"Not found: {id}");
await entity.ValidateAsync(repository, ct).EnsureValidAsync();
```

### Frontend Error Handling
```typescript
this.apiService.getData().pipe(
    this.observerLoadingErrorState('loadData'),
    this.tapResponse(
        data => this.updateState({ data }),
        error => this.handleError(error)
    ),
    this.untilDestroyed()
).subscribe();
```

---

## Quick Verification Checklist

Before removing/changing ANY code:
- [ ] Searched static imports?
- [ ] Searched string literals?
- [ ] Checked dynamic invocations?
- [ ] Read actual implementations?
- [ ] Traced dependencies?
- [ ] Declared confidence level?

**If confidence < 90% -> REQUEST USER CONFIRMATION**

---

## Common Bug Categories

| Category | Examples |
|----------|---------|
| Data Issues | Missing null checks, race conditions, stale cache |
| Validation | Missing rules, bypassed validation, async not awaited |
| Cross-Service | Message bus failures, sync ordering, API contract mismatches |
| Frontend | Lifecycle issues, state bugs, missing error handling |
| Authorization | Missing role checks, wrong company context |

## Related

- `debugging`
- `code-review`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**
- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
