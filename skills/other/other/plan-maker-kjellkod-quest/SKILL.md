---
name: plan-maker
description: Create implementation plans with testable acceptance criteria, validation strategies, integration touchpoints, and risk analysis before coding begins.
---

# Plan Maker

Create implementation plans that pass the plan-reviewer checklist and unblock coding.

## When to Use

Use for: Features, refactors, infrastructure, architectural changes, multi-file work
Skip for: Trivial fixes (1-2 lines), typos, pure research

---

## Core Principles

**Code Quality First**
- Readability > cleverness. KISS/DRY/YAGNI/SRP - but clarity always wins.
- Test real logic (business rules, algorithms, edge cases), skip trivial code (getters, imports, types)
- Mock at boundaries (APIs, DBs, I/O), not internal logic. Avoid mocking hell.

**Testing Philosophy**
- Automated: Clear run instructions, explicit mocking strategy, real assertions
- Manual: Labeled "MANUAL TEST", step-by-step, explain why not automated
- Reasonable automation: UI/judgment → manual, deterministic/critical → automated

---

## Plan Sizing

**Small (1 doc)**: 1-3 files, single component, clear requirements
**Large (multi-doc)**: 4+ files, multiple components, multiple phases
→ High-level plan + phase implementation plans

---

## Required Elements

Every plan MUST include:

### 1. Overview
- Problem statement, user impact, scope boundaries (what's OUT)

### 2. Acceptance Criteria
- Observable outcomes (not implementation details)
- Specific, measurable, testable, bounded

Good: "Pre-push generates coverage.json in <2 seconds"
Bad: "Coverage works well"

### 3. Validation Plan

**Automated Tests:**
```markdown
**Automated Test**: [Description]
- **File**: tests/unit/test_example.py
- **Test**: test_function_name()
- **Run**: python3 -m pytest tests/unit/test_example.py::test_function_name
- **Covers**: Happy path, edge case, error case
- **Mocking**: None (or: Mock API client)
- **Expected**: Returns dict with file paths
```

**Manual Tests:**
```markdown
**MANUAL TEST**: [Description]
- **Why manual**: End-to-end workflow validation
- **Preconditions**: Feature branch, test data setup
- **Steps**: 1. Action, 2. Action, 3. Action
- **Expected**: Specific observable outcome
- **Observability**: Logs to check, files created, UI state
```

### 4. Integration Touchpoints
List all systems (APIs, DBs, files, services, UI)
For each: What could break + How we validate

### 5. Implementation Approach
- Critical files (paths, line numbers, change type)
- Architecture (components, data flow, dependencies)
- Key functions (name, purpose, inputs/outputs, logic)

### 6. Risks & Mitigations
Top 3-5 risks with Impact/Likelihood/Mitigation

### 7. Open Questions
Ambiguities, decisions needed, assumptions (never silently assume)

---

## Optional Sections (When Relevant)

- **Configuration**: Sources, precedence, defaults, validation
- **Backward Compatibility**: Old clients/data, breaking changes, safe defaults
- **External Dependencies**: Timeouts, retries, fallbacks, error messages
- **UI States**: Loading, error, empty, success
- **Security**: No logging secrets, redaction, encryption

---

## Templates

### Small Plan
```markdown
# [Feature Name]

## Overview
**Problem**: [What we're solving]
**Impact**: [Who benefits, how]
**Scope**: [In/out]

## Acceptance Criteria
1. [Observable outcome]
2. [Observable outcome]

## Implementation
**Files**:
- `/path/file.py` - Modify - [Description]

**Key Functions**:
- `function_name()` - Purpose, inputs, outputs, logic

**Data Flow**: Step 1 → Step 2 → Step 3

## Validation
**Automated Test**: [Description]
- File, test name, run command, covers, mocking, expected

**MANUAL TEST**: [Description]
- Why manual, preconditions, steps, expected, observability

## Integration Touchpoints
**System**: [Name] - Could break: [X] - Validation: [Y]

## Risks
1. **Risk**: [Description] - Impact: H/M/L - Likelihood: H/M/L - Mitigation: [How]

## Open Questions
- [ ] [Question]
```

### Large Plan (High-Level)
```markdown
# [Feature] - High-Level

## Overview
Problem, impact, scope

## Acceptance Criteria
1-5 end-to-end observable outcomes

## Phases
**Phase 1**: [Name] - Goal, deliverable, plan doc link
**Phase 2**: [Name] - Goal, deliverable, plan doc link

## End-to-End Validation
Manual steps to validate complete feature

## Integration Touchpoints
All systems affected across phases

## Risks
Top 3-5 cross-phase risks

## Dependencies
Phase X blocks Phase Y because [reason]
```

### Phase Plan
Use Small Plan template, add:
- **Blocks**: What depends on this
- **Blocked By**: What this depends on

---

## Anti-Patterns (Avoid)

**Vague criteria**: "Works well", "handles gracefully", "fast"
→ Specific: "Returns 400 with error message when field missing"

**Unbounded scope**: "All formats", "all edge cases"
→ Bounded: "CSV and JSON (PDF deferred)"

**Implementation as criteria**: "Uses Factory pattern"
→ Observable: "User can't select product twice"

**Mocking hell**: Testing trivial code with mocks for mocks
→ Test real logic with minimal mocking

**Missing touchpoints**: "Add endpoint" (no mention of DB, auth, logs)
→ Complete: Database, auth, logging, monitoring specs

---

## Self-Review Checklist

Before human review:
- [ ] All required sections present
- [ ] Every acceptance criterion has validation
- [ ] Every touchpoint has "could break" + "validation"
- [ ] Top 3-5 risks documented
- [ ] Acceptance criteria are specific, measurable, testable
- [ ] No vague language ("works", "handles gracefully")
- [ ] Automated tests have file + name + run command
- [ ] Manual tests have step-by-step instructions
- [ ] File paths are absolute
- [ ] Open questions explicitly called out
- [ ] Scope is bounded (out-of-scope listed)

---

## Workflow

1. **Gather context**: Read code, understand problem, identify touchpoints
2. **Draft plan**: Use template, fill required sections, be specific
3. **Self-review**: Run checklist, fix gaps
4. **Human review**: Present with 3-5 key bullets, iterate on feedback
5. **Sign-off**: Address feedback, mark ready for implementation

---

## Planning Principles

1. Testability first (every criterion testable)
2. Code readability over dogma (KISS wins)
3. Test real logic (not trivial code)
4. Avoid mocking hell (boundaries only)
5. Explicit over implicit (document assumptions)
6. Bounded scope (constraints, not "all")
7. Integration awareness (know what breaks)
8. Actionable (concrete enough to start)
9. Shippable not perfect (stop conditions)
10. No hallucination (flag ambiguity)
