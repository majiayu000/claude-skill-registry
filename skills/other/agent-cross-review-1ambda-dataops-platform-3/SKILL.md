---
name: agent-cross-review
description: Structured cross-review protocol between specialized agents. Ensures scope alignment, priority calibration, and domain-aware feedback. Use when one agent reviews another's work, during handoffs, or when validating cross-cutting concerns.
---

# Agent Cross-Review

Protocol for structured collaboration between specialized agents.

## When to Use

- One agent reviewing another's output
- Handoff between feature and expert agents
- Validating cross-cutting concerns
- Resolving conflicting recommendations

## Core Principle

> **Review in domain, defer on scope.**

Each agent excels in their specialty. Cross-review catches blind spots without overstepping boundaries.

---

## Review Protocol

### Step 1: Scope Identification

Before reviewing, identify:

```markdown
## Cross-Review Context

| Item | Value |
|------|-------|
| Reviewer | {agent-name} |
| Author | {agent-name} |
| Artifact | {file or output} |
| Review Type | Technical / Structural / Integration |
```

### Step 2: Domain Check

| Reviewer Type | Review Focus | Defer On |
|---------------|--------------|----------|
| **Feature Agent** | Structure, naming, coverage | Pytest patterns, DRY |
| **Expert Agent** | Code quality, patterns | Project conventions |
| **Architecture** | Boundaries, dependencies | Implementation details |

### Step 3: Calibrated Feedback

Use priority tiers:

```markdown
### Cross-Review: {artifact}

**CRITICAL** (blocks merge)
- [Issue affecting correctness or security]

**MAJOR** (should fix)
- [Issue affecting maintainability]

**MINOR** (nice to have)
- [Improvement suggestion]

**DEFER** (out of scope for this review)
- [Valid concern but not reviewer's domain]
```

---

## Role-Specific Protocols

### feature-interface-cli Reviewing expert-python

**Focus Areas:**
- Test file naming follows project conventions
- Coverage targets CLI-critical paths
- Integration with existing command structure

**Defer To expert-python:**
- Fixture design decisions
- pytest marker selection
- Test helper organization

**Template:**
```markdown
## CLI Feature Review

### Structure
- [ ] Test files in correct location
- [ ] Naming follows test_{feature}_cmd.py
- [ ] Coverage priorities align with CLI usage

### Concerns for expert-python
- [List items needing pytest expertise]
```

### expert-python Reviewing feature-interface-cli

**Focus Areas:**
- Type hints complete and correct
- pytest patterns followed
- DRY violations identified

**Defer To feature-interface-cli:**
- CLI-specific testing approaches
- Typer/Rich patterns
- Project structure decisions

**Template:**
```markdown
## Python Quality Review

### Code Quality
- [ ] Type hints present on public functions
- [ ] No mutable default arguments
- [ ] Error handling is specific

### Test Quality
- [ ] Fixtures use appropriate scope
- [ ] No duplicate fixture definitions
- [ ] AAA pattern followed

### Concerns for feature-interface-cli
- [List items needing project context]
```

---

## Handoff Protocol

### From Feature Agent to Expert Agent

```markdown
## Handoff: {feature} implementation

### Completed
- [What's done]

### Needs Review
- [Specific areas needing expert input]

### Context
- [Domain-specific decisions made and why]

### Questions
1. [Specific question for expert]
```

### From Expert Agent to Feature Agent

```markdown
## Technical Recommendations: {area}

### Recommendations
1. [Recommendation with rationale]

### Priority Assessment
- **Now**: [Must address before merge]
- **Soon**: [Address in follow-up]
- **Later**: [Nice to have]

### Scope Consideration
- [Note if recommendation needs project context validation]
```

---

## Conflict Resolution

When agents disagree:

### Priority Framework

| Concern Type | Primary Authority |
|--------------|-------------------|
| Project conventions | Feature agent |
| Language patterns | Expert agent |
| Test structure | Shared (use pytest-fixtures skill) |
| Architecture | Architecture skill/agent |

### Resolution Steps

1. **State the conflict** clearly
2. **Identify domain** - whose expertise applies?
3. **Check project context** - what do existing patterns show?
4. **Propose compromise** - can both concerns be addressed?
5. **Escalate if needed** - ask user for decision

---

## Common Pitfalls

| Pitfall | Example | Solution |
|---------|---------|----------|
| Scope creep | Expert suggesting CLI changes | Defer with note |
| Missing context | Recommending unused pattern | Check project first |
| Priority mismatch | Low priority as critical | Use tier framework |
| Over-optimization | Refactor working code | Focus on current task |

---

## Output Format

### Quick Review

```markdown
## Cross-Review Summary

**Artifact**: {file/output}
**Verdict**: Approve / Needs Changes / Discuss

### In My Domain
- [Finding 1]
- [Finding 2]

### Deferred (not my domain)
- [Observation for other agent]
```

### Detailed Review

```markdown
## Cross-Review: {artifact}

### Context
- Author: {agent}
- Reviewer: {agent}
- Type: {technical/structural}

### Findings

**CRITICAL**
- None / [issues]

**MAJOR**
- [issues]

**MINOR**
- [issues]

### Deferred Items
| Item | Recommended Reviewer | Reason |
|------|---------------------|--------|
| X | expert-python | pytest expertise |
| Y | feature-cli | project conventions |

### Verdict
[Approve / Needs Changes]
```

## Quality Checklist

- [ ] Identified review scope before starting
- [ ] Focused on domain expertise
- [ ] Used priority tiers appropriately
- [ ] Deferred out-of-domain concerns
- [ ] Provided actionable feedback
- [ ] Considered project context
