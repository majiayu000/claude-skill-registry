---
name: task-design
description: Design well-structured tasks for AI agents. Use when creating issues, work items, or task specifications that agents will execute autonomously.
---

# Task Design

## Core Principle

**A well-designed task is an executable contract.**

The agent should be able to read the task, understand what to do, know when to stop, and verify success—all without asking clarifying questions.

---

## When to Use

Use this skill when:
- Creating issues/tasks e.g. `bd` (beads)
- Writing GitHub Issues for autonomous agents
- Specifying work for subagents
- Breaking down features into actionable tasks

---

## The Complete Task Template

```markdown
# [PREFIX] Task Title

## Summary
One-sentence executive summary of what needs to be done.

---

## Context
Why is this task needed? What problem does it solve?
What happens if we don't do this?

---

## Reference (Optional)
Link to TRD, design doc, or specification that governs this task.
Example: `docs/plans/TRD-feature.md — Section FR-2`

---

## Scope

### In Scope
- File: `path/to/file.ext`
- Component: `ComponentName`

### Out of Scope
- NOT changing X
- NOT touching Y

---

## Requirements

| Req | Description | Level |
|-----|-------------|-------|
| R-1 | Specific, testable requirement | MUST |
| R-2 | Another requirement | MUST |
| R-3 | Nice to have | SHOULD |

---

## Technical Constraints
What the agent MUST NOT do or change.

- Use existing `X` pattern
- Don't add new dependencies
- Follow conventions in `path/to/example`
- Output format must be JSON

---

## Acceptance Criteria (CoS)
Checklist for completion. Agent checks these off.

- [ ] Criterion 1 implemented
- [ ] Criterion 2 verified
- [ ] Tests pass
- [ ] Documentation updated

---

## Testing Requirements
How to validate the work.

- Manual: Load and invoke
- Automated: `npm test` passes
- Verify: Check output structure

---

## Files Likely to Change
Help the agent understand scope.

- `src/feature.ts` — Main implementation
- `tests/feature.test.ts` — Tests
- `README.md` — Documentation update

---

## Definition of Done
Task is complete when:

- [ ] All acceptance criteria checked
- [ ] All tests pass
- [ ] Code committed and pushed
- [ ] Issue closed in backlog
```

---

## Section-by-Section Guide

### Summary
**One sentence. No more.**

❌ Bad: "We need to add authentication because users want to log in and we should use JWT"
✅ Good: "Add JWT-based authentication endpoint"

### Context
**Answer: Why does this matter?**

This helps the agent make trade-off decisions. If they understand the *why*, they make better *how* choices.

### Reference
**Link to source of truth.**

If there's a TRD, design doc, or spec, reference the specific section. The agent will read it before acting.

Example:
```
**TRD:** `docs/plans/TRD-auth.md` — Section FR-2: User Authentication
```

### Scope
**Be explicit about boundaries.**

Agents tend to over-deliver or under-deliver. Explicit scope prevents both.

In Scope = What to touch
Out of Scope = What NOT to touch (even if related)

### Requirements
**Verifiable statements with MUST/SHOULD/MAY.**

| Level | Meaning |
|-------|---------|
| MUST | Required. Failure = incomplete task |
| SHOULD | Expected unless justified |
| MAY | Optional, at agent's discretion |

### Technical Constraints
**Guardrails, not instructions.**

These are the "don'ts"—what the agent must avoid.

Examples:
- "Don't add npm dependencies"
- "Use the existing `ApiClient` class"
- "Follow REST conventions in codebase"

### Acceptance Criteria
**Checkboxes the agent completes.**

Write as if you're the agent checking off boxes. Each criterion should be:
- Binary (done or not done)
- Verifiable (can be checked)
- Specific (no ambiguity)

### Testing Requirements
**How the agent validates their work.**

For code: what tests to run
For skills: how to manually verify
For docs: how to check correctness

### Files Likely to Change
**Reduce scope anxiety.**

Agents sometimes hesitate because they don't know where to look. This section gives them permission and direction.

### Definition of Done
**The exit condition.**

When all these are true, the agent stops working and reports completion.

---

## Quick Template (Minimal)

For simpler tasks, use this abbreviated format:

```markdown
## Summary
One-sentence description.

## Scope
- File: `path/to/file.ext`

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Validation
How to verify completion.
```

---

## Using with bd (Beads)

When creating issues with `bd create`, use the `--body` flag:

```bash
bd create "[FEATURE] Add user auth" --body "## Summary
Add JWT authentication endpoint.

## Context
Users need to log in to access protected routes.

## Scope
- File: \`src/routes/auth.ts\`
- File: \`src/middleware/jwt.ts\`

## Acceptance Criteria
- [ ] POST /auth/login endpoint works
- [ ] Returns JWT on valid credentials
- [ ] Returns 401 on invalid credentials
- [ ] Unit tests pass

## Validation
1. Run: \`npm test\`
2. Manual: POST to /auth/login with test credentials"
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| "Implement the thing" | "Create POST /api/users endpoint" |
| Vague context | Explain why this matters |
| No constraints | List what NOT to do |
| "Make it work" | Specific acceptance criteria |
| No testing section | Define how to validate |

---

## Examples

### Example 1: Feature Task

```markdown
## Summary
Add rate limiting middleware to API endpoints.

## Context
The API is vulnerable to abuse. Adding rate limiting protects against DDoS and brute-force attacks.

## Reference
**TRD:** `docs/security-plan.md` — Section 3.2: Rate Limiting

## Scope
- File: `src/middleware/rateLimiter.ts` (new)
- File: `src/app.ts` (add middleware)

## Requirements
| Req | Description | Level |
|-----|-------------|-------|
| R-1 | Limit to 100 requests per minute per IP | MUST |
| R-2 | Return 429 Too Many Requests when exceeded | MUST |
| R-3 | Exclude health check endpoint | SHOULD |

## Technical Constraints
- Use existing Redis connection from `src/lib/redis.ts`
- Don't add new npm dependencies (use built-in or existing)

## Acceptance Criteria
- [ ] Rate limiter middleware created
- [ ] Applied to all routes except /health
- [ ] 429 response when limit exceeded
- [ ] Unit tests cover limit scenarios
- [ ] Integration test for rate limit reset

## Validation
1. `npm test` passes
2. Manual: Hit endpoint 101 times, verify 429 on 101st

## Definition of Done
- [ ] All acceptance criteria checked
- [ ] PR created and merged
```

### Example 2: Skill Creation Task

```markdown
## Summary
Create repo-scanner skill for assimilation pipeline.

## Context
First phase of assimilation. Scans repo structure without reading all code.

## Reference
**TRD:** `docs/plans/TRD-assimilation.md` — Section FR-1

## Scope
- File: `.github/skills/assimilation/repo-scanner/SKILL.md`
- Mirror: `.claude/skills/assimilation/repo-scanner/SKILL.md`

## Requirements
| Req | Description | Level |
|-----|-------------|-------|
| FR-1.1 | Skip ignore patterns (node_modules, .git, etc.) | MUST |
| FR-1.3 | Detect language from config files | MUST |
| FR-1.4 | Detect framework from config files | MUST |
| FR-1.5 | Produce scan-report.json or fail with error | MUST |

## Technical Constraints
- Follow agentskills.io spec (name + description in frontmatter)
- No code execution, markdown instructions only
- Output to .github/temp/scan-report.json

## Acceptance Criteria
- [ ] SKILL.md follows agentskills.io spec
- [ ] Ignore patterns documented
- [ ] Framework detection table complete
- [ ] Output schema defined
- [ ] Exists in both .github/ and .claude/

## Validation
1. Load skill in Claude Code
2. Ask: "scan this repo"
3. Verify scan-report.json produced
4. Verify ignored dirs not in output

## Definition of Done
- [ ] All acceptance criteria checked
- [ ] Issue closed in bd
```

---

## Related Skills

- [bd](../bd/SKILL.md) — Issue tracking with beads
- [agent-runbook](../agent-runbook/SKILL.md) — Multi-step workflow documentation
- [subagent](../subagent/SKILL.md) — Task delegation protocol
