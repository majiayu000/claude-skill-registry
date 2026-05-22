---
name: faion-review
description: "Code review or SDD document review. Runs appropriate reviewers based on context."
user-invocable: false
allowed-tools: Read, Glob, Grep, Bash, Task, AskUserQuestion
---

# SDD Review Skill

**Communication with user: User's language.**

## Purpose

Perform code review or SDD document review using specialized agents.

## Modes

### Code Review Mode
Review git diff for a project directory.

### SDD Review Mode
Review SDD documents (spec, design, impl-plan, tasks) for a feature.

## Mode Detection

```
Input contains "sdd:" prefix → SDD Review
Input is directory path → Code Review
Ask user if unclear
```

---

## Code Review Mode

### Workflow

```
1. Get git diff for directory
   ↓
2. Call general-purpose agent with review prompt
   ↓
3. Report findings
```

### Review Criteria

**Critical (must fix):**
- Correctness issues
- Missing/broken tests
- Security vulnerabilities
- Breaking changes

**Style (should fix):**
- Convention violations
- Pattern deviations
- Naming issues

**Quality (consider):**
- Complexity
- Error handling
- Edge cases

**Performance (check):**
- N+1 queries
- Missing indexes
- Resource leaks

### Output Format

```markdown
## Code Review: {directory}

### Summary
{overall assessment}

### Critical Issues
1. {issue}: {file:line} - {description}

### Style Issues
1. {issue}: {file:line}

### Suggestions
- {suggestion}

### Pre-Merge Checklist
- [ ] All critical issues fixed
- [ ] Tests passing
- [ ] No security issues
```

---

## SDD Review Mode

### Workflow

```
1. Parse project/feature from input
   ↓
2. Run reviewers in sequence:
   - faion-spec-reviewer-agent
   - faion-design-reviewer-agent
   - faion-impl-plan-reviewer-agent
   - faion-tasks-reviewer-agent (if tasks exist)
   ↓
3. Aggregate results
   ↓
4. Report overall verdict
```

### Agent Calls

```python
# Spec review
Task(
    subagent_type="faion-spec-reviewer-agent",
    prompt=f"Review spec for {project}/{feature}"
)

# Design review
Task(
    subagent_type="faion-design-reviewer-agent",
    prompt=f"Review design for {project}/{feature}"
)

# Implementation plan review
Task(
    subagent_type="faion-impl-plan-reviewer-agent",
    prompt=f"Review impl-plan for {project}/{feature}"
)

# Tasks review (if exist)
Task(
    subagent_type="faion-tasks-reviewer-agent",
    prompt=f"Review tasks for {project}/{feature}"
)
```

### Output Format

```markdown
## SDD Review: {project}/{feature}

### Document Status
| Document | Status | Issues |
|----------|--------|--------|
| spec.md | ✅/⚠️/❌ | {count} |
| design.md | ✅/⚠️/❌ | {count} |
| implementation-plan.md | ✅/⚠️/❌ | {count} |
| tasks/ | ✅/⚠️/❌ | {count} |

### Overall Verdict: {APPROVED / NEEDS_WORK / REJECTED}

### Issues Found
{detailed issues per document}

### Recommendations
{what to fix before proceeding}
```

---

## Agents Used

| Agent | Mode | Purpose |
|-------|------|---------|
| general-purpose | Code | Git diff analysis |
| faion-spec-reviewer-agent | SDD | Spec completeness, testability |
| faion-design-reviewer-agent | SDD | Architecture, FR coverage |
| faion-impl-plan-reviewer-agent | SDD | 100k token rule, dependencies |
| faion-tasks-reviewer-agent | SDD | Multi-pass task quality |
