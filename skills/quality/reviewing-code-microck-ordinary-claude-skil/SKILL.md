---
name: Reviewing Code
description: Systematically evaluate code changes for security, correctness, performance, and spec alignment. Use when reviewing PRs, assessing code quality, or verifying implementation against requirements.
---

# Reviewing Code

Evaluate code changes across security, correctness, spec alignment, performance, and maintainability. Apply sequential or parallel review based on scope.

## Quick Start

**Sequential (small PRs, <5 files):**
1. Gather context from feature specs and acceptance criteria
2. Review sequentially through focus areas
3. Report findings by priority
4. Recommend approval/revision/rework

**Parallel (large PRs, >5 files):**
1. Identify independent review aspects (security, API, UI, data)
2. Spawn specialist agents for each dimension
3. Consolidate findings
4. Report aggregate assessment

## Context Gathering

**Read documentation:**
- `docs/feature-spec/F-##-*.md` — Technical design and requirements
- `docs/user-stories/US-###-*.md` — Acceptance criteria
- `docs/api-contracts.yaml` — Expected API signatures
- `docs/data-plan.md` — Event tracking requirements (if applicable)
- `docs/design-spec.md` — UI/UX requirements (if applicable)
- `docs/system-design.md` — Architecture patterns (if available)
- `docs/plans/<slug>/plan.md` — Original implementation plan (if available)

**Determine scope:**
- Files changed and features affected (F-## IDs)
- Stories implemented (US-### IDs)
- API, database, or schema changes

## Quality Dimensions

**Security (/25)**
- Input validation and sanitization
- Authentication/authorization checks
- Sensitive data handling
- Injection vulnerabilities (SQL, XSS, etc.)

**Correctness (/25)**
- Logic matches acceptance criteria
- Edge cases handled properly
- Error handling complete
- Null/undefined checks present

**Spec Alignment (/20)**
- APIs match `docs/api-contracts.yaml`
- Data events match `docs/data-plan.md`
- UI matches `docs/design-spec.md`
- Implementation follows feature spec

**Performance (/15)**
- Algorithm efficiency
- Database query optimization
- Resource usage (memory, network)

**Maintainability (/15)**
- Code clarity and readability
- Consistent with codebase patterns
- Appropriate abstraction levels
- Comments where needed

**Total: /100**

## Finding Priority

### 🔴 CRITICAL (Must fix before merge)
- Security vulnerabilities
- Broken functionality
- Spec violations (API contract breaks)
- Data corruption risks

**Format:**
```
Location: file.ts:123
Problem: [Description]
Impact: [Risk/consequence]
Fix: [Specific change needed]
Spec reference: [docs/api-contracts.yaml line X]
```

### 🟡 IMPORTANT (Should fix)
- Logic bugs in edge cases
- Missing error handling
- Performance issues
- Missing analytics events
- Accessibility violations

### 🟢 NICE-TO-HAVE (Optional)
- Code style improvements
- Better abstractions
- Enhanced documentation

### ✅ GOOD PRACTICES
Highlight what was done well for learning

## Review Strategies

### Single-Agent Review
Best for <5 files, single concern:
1. Review sequentially through focus areas
2. Concentrate on 1-2 most impacted areas
3. Generate unified report

### Parallel Multi-Agent Review
Best for >5 files, multiple concerns:
1. Spawn specialized agents:
   - **Security:** `senior-engineer` for vulnerability assessment
   - **Architecture:** `Explore` for pattern compliance
   - **API Contracts:** `programmer` for endpoint validation
   - **Frontend:** `programmer` for UI/UX and accessibility
   - **Documentation:** `documentor` for comment quality and docs

2. Each agent reviews specific quality dimension
3. Consolidate findings into single report

## Report Structure

```
# Code Review: [Feature/PR]

## Summary
**Quality Score:** [X/100]
**Issues:** Critical: [N], Important: [N], Nice-to-have: [N]
**Assessment:** [APPROVE / NEEDS REVISION / MAJOR REWORK]

## Spec Compliance
- [ ] APIs match `docs/api-contracts.yaml`
- [ ] Events match `docs/data-plan.md`
- [ ] UI matches `docs/design-spec.md`
- [ ] Logic satisfies story AC

## Findings

### Critical Issues
[Issues with fix recommendations]

### Important Issues
[Issues that should be addressed]

### Nice-to-Have Suggestions
[Optional improvements]

### Good Practices
[What worked well]

## Recommendations
[Next steps: approval, revision needed, etc.]
```

## Fix Implementation

**Offer options:**
1. Fix critical + important issues
2. Fix only critical (minimum for safety)
3. Provide detailed explanation for learning
4. Review only (no changes)

**Parallel fixes for large revisions:**
- Spawn agents for independent fix areas
- Coordinate on shared dependencies
- Document each fix with location, change, and verification method

**Document format:**
```
✅ FIXED: [Issue name]
File: [path:line]
Change: [what changed]
Verification: [how to test]
```

## Documentation Updates

**Check if specs need updates:**
- Feature spec "Decisions" or "Deviations" if implementation differs
- Design spec if UI changed
- API contracts if endpoints modified (requires approval)
- Data plan if events changed

**Always flag for user approval before modifying specs.**

## Key Points

- Read all context documents before starting
- Focus on most impacted areas first
- Be thorough with security-sensitive code, API changes, and critical user flows
- Use scoring framework for comprehensive reviews
- Parallel review scales to large PRs
- Flag spec deviations for user decision
