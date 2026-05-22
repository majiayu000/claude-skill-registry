---
name: 5w1h-decision
description: "5W1H Decision Framework Tool. Use for: (1) Systematic decision-making before creating todos, (2) Preventing duplicate implementation, (3) Detecting avoidance behavior, (4) Ensuring agile refactor compliance with executor/dispatcher separation"
---

# 5W1H Decision Framework - Systematic Decision Making

## Core Principles

### Decision Philosophy: Think Before Act

| Principle | Description | Validation |
|-----------|-------------|------------|
| Systematic Thinking | Every decision requires 5W1H analysis | All 6 questions answered |
| No Duplication | Check existing implementation first | Who analysis complete |
| No Avoidance | Reject escape language | Why validation passed |
| Agile Compliance | Executor/Dispatcher separation | How task type matched |
| TDD Integration | Test-first strategy required | How includes TDD steps |

### Key Files

| File | Purpose |
|------|---------|
| `.claude/output-styles/5w1h-format.md` | **System-level format enforcement** |
| `.claude/methodologies/5w1h-self-awareness-methodology.md` | Complete methodology |
| `.claude/methodologies/agile-refactor-methodology.md` | Agent collaboration rules |
| `.claude/methodologies/claude-self-check-methodology.md` | Avoidance language detection |
| `CLAUDE.md` | Project development guidelines |

---

## 5W1H Framework Quick Reference

### Who (Responsibility Attribution)

**Format (Agile Refactor Compliant)**:
```markdown
Who: {Executor Agent} (executor) | {Dispatcher} (dispatcher)
```

**Valid Patterns**:

| Scenario | Who Format |
|----------|------------|
| Agent implements code | `parsley-flutter-developer (executor) \| rosemary-project-manager (dispatcher)` |
| Main thread dispatches | `rosemary-project-manager (self-execute - dispatch/review)` |
| Documentation agent | `thyme-documentation-integrator (executor) \| rosemary-project-manager (dispatcher)` |

**Checks**:
- [ ] Searched existing Domain for duplicate functionality
- [ ] Verified Service layer implementation
- [ ] Confirmed test coverage
- [ ] Executor matches task type

---

### What (Function Definition)

**Single Responsibility Verification**:

```markdown
What: [Function Name]
- Description: [One sentence description]
- Input: [Explicit input types]
- Output: [Explicit output types]
- Exception: [Error handling]
```

**Checks**:
- [ ] Single responsibility (one sentence description)
- [ ] Clear input/output definition
- [ ] No overlap with existing functions
- [ ] Can write Given-When-Then test

---

### When (Trigger Timing)

**Event-Driven Format**:

```markdown
When: [Event Name]
- Trigger: [User action / System event]
- Event: [EventName]
- Side Effects: [List all side effects]
- Integration: [Event system integration point]
```

**Checks**:
- [ ] Clear trigger event identified
- [ ] Side effects fully documented
- [ ] Integration with Event-Driven Architecture

---

### Where (Execution Location)

**Architecture Layer Format**:

```markdown
Where: [Layer] / [Component]
- Architecture: [Domain/Application/Infrastructure/Presentation]
- Component: [Specific class or module]
- UseCase: [UseCase call chain]
- Call Path: UI -> UseCase -> Domain -> Service
```

**Checks**:
- [ ] Correct Clean Architecture layer
- [ ] DDD aggregate boundary respected
- [ ] UseCase path traceable

---

### Why (Motivation Validation)

**Requirement Traceability Format**:

```markdown
Why: [Requirement Reference]
- Requirement ID: [UC-XXX]
- Business Value: [User benefit]
- User Scenario: [Specific use case]
- Document: [docs/app-requirements-spec.md#UC-XXX]
```

**Avoidance Language Detection** (BLOCKED):

| Category | Blocked Phrases |
|----------|-----------------|
| Quality Compromise | "too complex", "workaround", "temporary fix", "quick fix" |
| Simplification | "simpler approach", "easier way", "simplify" |
| Problem Ignoring | "ignore for now", "skip for now", "deal with later" |
| Test Compromise | "simplify test", "lower test standard", "basic test only" |
| Code Escape | "comment out", "disable", "temporarily disable" |

**Checks**:
- [ ] Has requirement document reference
- [ ] Clear business value stated
- [ ] No avoidance language detected

---

### How (Implementation Strategy)

**Task Type Format (Required)**:

```markdown
How: [Task Type: {TYPE}] {Strategy Description}
```

**Task Types and Valid Executors**:

| Task Type | Valid Executor | Description |
|-----------|----------------|-------------|
| `Implementation` | Agent (parsley, sage, etc.) | Code implementation |
| `Dispatch` | Main Thread (rosemary) | Task assignment |
| `Review` | Main Thread (rosemary) | Acceptance check |
| `Documentation` | thyme / rosemary | Document updates |
| `Analysis` | lavender / rosemary | Problem analysis |
| `Planning` | rosemary / lavender | Strategy planning |

**Violation Detection**:

| Who Executor | How Task Type | Result |
|--------------|---------------|--------|
| rosemary-project-manager | Implementation | BLOCKED |
| parsley-flutter-developer | Dispatch | BLOCKED |
| Any agent | Implementation | ALLOWED |
| rosemary-project-manager | Dispatch/Review | ALLOWED |

**Checks**:
- [ ] TDD test-first strategy
- [ ] Task Type matches executor
- [ ] No architectural debt introduced
- [ ] No temporary solutions

---

## Complete 5W1H Template

```markdown
5W1H-{YYYYMMDD}-{HHMMSS}-{random}

Who: {agent} (executor) | rosemary-project-manager (dispatcher)
- Domain: {Responsible class/module}
- Existing: {Search result for duplicates}

What: {Function Name}
- Description: {One sentence}
- Input: {Types}
- Output: {Types}

When: {Event Trigger}
- Trigger: {User action / System event}
- Side Effects: {List}

Where: {Layer / Component}
- Architecture: {Clean Architecture layer}
- UseCase: {Call chain}

Why: {Requirement}
- Requirement ID: {UC-XXX}
- Business Value: {User benefit}

How: [Task Type: {TYPE}] {Strategy}
1. Write failing test
2. Implement to pass test
3. Refactor
4. Integration verification
```

---

## Common Violations and Fixes

### Violation 1: Missing Executor/Dispatcher

```markdown
// VIOLATION
Who: parsley-flutter-developer
- Implement ISBN validation

// FIX
Who: parsley-flutter-developer (executor) | rosemary-project-manager (dispatcher)
- Domain: BookValidator in Book Aggregate
- Existing: Searched, no duplicate found
```

### Violation 2: Missing Task Type

```markdown
// VIOLATION
How: TDD implementation strategy
1. Write test
2. Implement

// FIX
How: [Task Type: Implementation] TDD implementation strategy
1. Write failing test for ISBN validation
2. Implement BookValidator.validateISBN()
3. Refactor for readability
4. Integrate with AddBookUseCase
```

### Violation 3: Main Thread Doing Implementation

```markdown
// VIOLATION
Who: rosemary-project-manager (self-execute)
How: [Task Type: Implementation] Build Domain event classes

// FIX
Who: parsley-flutter-developer (executor) | rosemary-project-manager (dispatcher)
How: [Task Type: Implementation] Build Domain event classes
```

### Violation 4: Avoidance Language

```markdown
// VIOLATION
Why: Need to simplify the complex validation
- Using a simpler approach for now

// FIX
Why: UC-001 Book Addition Requirement
- Requirement ID: UC-001
- Business Value: Ensure user input data format correctness
- User Scenario: User manually inputs ISBN and needs immediate validation
```

---

## Token Generation

### Session Token Format

```text
5W1H-{YYYYMMDD}-{HHMMSS}-{random}
Example: 5W1H-20250925-191735-a7b3c2
```

### Generate Token Script

```bash
# Generate new session token
uv run .claude/skills/5w1h-decision/scripts/generate_token.py

# Validate 5W1H content
uv run .claude/skills/5w1h-decision/scripts/validate_5w1h.py "content"
```

### Hook Integration

The 5W1H checker is integrated into PreToolUse Hook:
- Checks before TodoWrite operations
- Validates all 6 W/H sections present
- Detects avoidance language
- Validates agile refactor compliance

### Output Style Integration (System-Level Enforcement)

**Since v0.25.1**, 5W1H format is enforced at the system level via Output Style:

**File Location**: `.claude/output-styles/5w1h-format.md`

**Enforcement Mechanism**:
- Output Style is injected into Claude's system prompt
- Every response MUST follow the 5W1H format structure
- No manual activation required - always active

**Relationship with Other Mechanisms**:

| Mechanism | Level | Purpose | Enforcement |
|-----------|-------|---------|-------------|
| **Output Style** | System | Response format structure | Automatic (system prompt) |
| **PreToolUse Hook** | Tool | Todo creation validation | Before TodoWrite |
| **UserPromptSubmit Hook** | Session | Token generation + reminder | Each user input |
| **SKILL** | Reference | Documentation + scripts | On-demand |

**Key Advantage**:
- Output Style provides **consistent format enforcement** without relying on Hook execution
- Even if Hooks fail, Claude still follows the format due to system-level injection

---

## Checklist Before Todo Creation

### Completeness Check

- [ ] **Who**: Executor/Dispatcher clearly identified, no duplicate implementation
- [ ] **What**: Single responsibility, clear I/O definition
- [ ] **When**: Trigger timing explicit, side effects identified
- [ ] **Where**: Correct architecture layer, UseCase path clear
- [ ] **Why**: Requirement reference, no avoidance language
- [ ] **How**: Task Type present, TDD strategy, matches executor

### Agile Refactor Compliance Check

- [ ] Who has (executor) | (dispatcher) format
- [ ] How has [Task Type: XXX] prefix
- [ ] Implementation tasks assigned to agents (not main thread)
- [ ] Dispatch/Review tasks assigned to main thread

### Quality Gate

**ALL items must be checked before creating todo.**

Missing any item = BLOCKED

---

## Related Documentation

### Methodologies
- [5W1H Self-Awareness Methodology](../../../.claude/methodologies/5w1h-self-awareness-methodology.md)
- [Agile Refactor Methodology](../../../.claude/methodologies/agile-refactor-methodology.md)
- [Claude Self-Check Methodology](../../../.claude/methodologies/claude-self-check-methodology.md)

### Project Files
- [CLAUDE.md](../../../CLAUDE.md) - Project guidelines
- [Agent Collaboration](../../../.claude/agent-collaboration.md) - Agent rules

### Scripts (in this SKILL)
- [Token Generator](./scripts/generate_token.py)
- [5W1H Validator](./scripts/validate_5w1h.py)

---

## Quick Reference Card

### Required Format

```text
5W1H-{TOKEN}

Who: {agent} (executor) | rosemary-project-manager (dispatcher)
What: {Single responsibility function}
When: {Event trigger with side effects}
Where: {Architecture layer / Component}
Why: {Requirement ID + Business value}
How: [Task Type: {TYPE}] {TDD strategy steps}
```

### Task Type Quick Reference

| Type | Executor | Example |
|------|----------|---------|
| Implementation | parsley, sage, pepper | Write code |
| Dispatch | rosemary | Assign task |
| Review | rosemary | Accept deliverable |
| Documentation | thyme | Update docs |
| Analysis | lavender | Design analysis |
| Planning | rosemary | Strategy planning |

### Avoidance Detection Keywords

| Block | Reason |
|-------|--------|
| "too complex" | Escaping difficulty |
| "simpler approach" | Compromising quality |
| "for now" | Temporary solution |
| "skip" | Avoiding problem |
| "later" | Deferring issue |
