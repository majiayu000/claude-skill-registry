---
name: code-review
description: Use when reviewing code changes before committing, after implementing features, or when asked to review. Triggers on staged changes, PR reviews, or explicit review requests.
---

# Code Review

Rigorous code review focused on quality, maintainability, and architectural soundness.

## When to Use

- After implementing a feature or fix
- Before committing changes
- When explicitly asked to review code
- Before creating a PR

## Method

Start by inspecting the changes. Use the deterministic script to collect the review context:

```bash
scripts/collect_review_context.sh
```

If on the `main` branch, review the staged git diff. If on a different branch, review committed and uncommitted changes compared to main.

Dispatch two subagents to carefully review the code changes. Tell them they're competing with another agent - whoever finds more legitimate issues wins honour and glory. Make sure they examine both architecture AND implementation, and check every criterion below.

## Review Criteria

### 1. Code Quality

| Check | Look For |
|-------|----------|
| **DRY** | Duplicated logic, copy-pasted code, repeated patterns that should be abstracted |
| **Code Bloat** | Unnecessary code, over-engineering, premature abstractions, dead code |
| **Bugs** | Logic errors, edge cases, off-by-one errors, null/undefined handling |

### 2. Code Slop & Technical Debt

| Symptom | Description |
|---------|-------------|
| **Magic values** | Hardcoded strings/numbers without constants |
| **Inconsistent naming** | Mixed conventions, unclear names |
| **Missing error handling** | Unhandled exceptions, silent failures |
| **TODO/FIXME comments** | Deferred work that should be tracked |
| **Commented-out code** | Delete it or explain why it exists |
| **Dependency bloat** | New deps when stdlib/existing deps suffice |

### 3. Architecture (in context of broader system)

| Principle | Review Questions |
|-----------|-----------------|
| **Modularity** | Are changes properly bounded? Do they respect module boundaries? |
| **Cohesion** | Does each unit have a single, clear responsibility? |
| **Separation of Concerns** | Is business logic mixed with presentation/data access? |
| **Information Hiding** | Are implementation details properly encapsulated? |
| **Coupling** | Does this create tight coupling? Are dependencies appropriate? |

### 4. Devil's Advocate

Challenge the implementation:
- Is this the simplest solution? Could it be simpler?
- What happens under load/scale?
- What are the failure modes?
- What assumptions might be wrong?
- Is there a more fundamentally correct approach, even if harder?

### 5. Test Effectiveness

| Check | Criteria |
|-------|----------|
| **Coverage** | Are the important paths tested? |
| **Meaningful assertions** | Do tests verify behavior, not implementation? |
| **Edge cases** | Are boundaries and error conditions tested? |
| **Readability** | Can you understand what's tested from test names? |
| **Fragility** | Will tests break on valid refactors? |

## Output Format

Report findings organized by severity:

```markdown
## Code Review Findings

### Critical (must fix)
- [Issue]: [Location] - [Why it matters]

### Important (should fix)
- [Issue]: [Location] - [Recommendation]

### Minor (consider fixing)
- [Issue]: [Location] - [Suggestion]

### Positive Observations
- [What was done well]
```

## Common Mistakes

| Mistake | Correction |
|---------|------------|
| Surface-level review | Dig into logic, trace data flow |
| Ignoring context | Review changes in relation to the system |
| Only finding negatives | Note what's done well |
| Vague feedback | Be specific: file, line, concrete suggestion |
| Bikeshedding | Focus on impact, not style preferences |

## Red Flags - STOP and Investigate

- New dependencies added without clear justification
- Changes that bypass existing patterns without explanation
- Test coverage decreased
- Complex logic without tests
- Security-sensitive code modified
