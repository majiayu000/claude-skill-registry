---
name: code-review-checklist
description: Structured code review criteria for pre-implementation plan review (Critic) and post-implementation security/quality review. Covers security, performance, maintainability, and correctness with severity ratings.
license: MIT
metadata:
  author: groupzer0
  version: "1.0"
---

# Code Review Checklist

Systematic review criteria for evaluating code and plans. Use this skill when:
- Critic reviews plans before implementation
- Security agent conducts code audits
- Architect reviews architectural compliance
- UAT validates implementation quality

## Review Context

**This skill supports two review phases:**

| Phase | Agent | Focus | Documents |
|-------|-------|-------|-----------|
| **Pre-Implementation** | Critic | Plan quality, clarity, completeness | `planning/*.md` |
| **Post-Implementation** | Security, Architect | Code quality, security, architecture | Source code |

---

## Pre-Implementation Review (Critic)

### Value Statement Assessment (MUST START HERE)

| Check | Question | Finding Severity |
|-------|----------|------------------|
| Presence | Does plan have clear value statement in user story format? | CRITICAL if missing |
| Clarity | Is "So that" outcome measurable or verifiable? | HIGH if vague |
| Alignment | Does value support Master Product Objective? | CRITICAL if drift |
| Directness | Is value delivered directly, not deferred? | HIGH if deferred |

### Plan Completeness

| Check | Question | Finding Severity |
|-------|----------|------------------|
| Scope | Are boundaries clearly defined? | MEDIUM |
| Deliverables | Are all deliverables listed with acceptance criteria? | HIGH |
| Dependencies | Are dependencies identified and sequenced? | MEDIUM |
| Risks | Are risks documented with mitigations? | LOW |
| Version | Is semver bump specified with rationale? | MEDIUM |

### Constraint Compliance

| Check | Question | Finding Severity |
|-------|----------|------------------|
| No Code | Does plan avoid prescriptive code? | LOW |
| No How | Does plan focus on WHAT/WHY, not HOW? | LOW |
| Architecture | Does plan respect architectural constraints? | HIGH |

---

## Post-Implementation Review (Security/Architect)

### Security Checklist

| Category | Check | Severity |
|----------|-------|----------|
| **Input Validation** | All user input validated server-side? | CRITICAL |
| **Authentication** | Auth checks on all protected routes? | CRITICAL |
| **Authorization** | RBAC/ownership verified before access? | CRITICAL |
| **Secrets** | No hardcoded credentials or keys? | CRITICAL |
| **SQL/Injection** | Parameterized queries used? | CRITICAL |
| **XSS** | Output encoding applied? | HIGH |
| **CSRF** | Tokens on state-changing requests? | HIGH |
| **Logging** | Security events logged without sensitive data? | MEDIUM |
| **Dependencies** | No known CVEs in dependencies? | Varies |

### Performance Checklist

| Category | Check | Severity |
|----------|-------|----------|
| **N+1 Queries** | Batch fetches instead of loops? | HIGH |
| **Pagination** | Large datasets paginated? | HIGH |
| **Caching** | Appropriate caching strategy? | MEDIUM |
| **Async** | Long operations non-blocking? | MEDIUM |
| **Resource Limits** | Bounded allocations? | HIGH |

### Maintainability Checklist

| Category | Check | Severity |
|----------|-------|----------|
| **Naming** | Clear, descriptive names? | LOW |
| **Complexity** | Cyclomatic complexity < 10? | MEDIUM |
| **Coupling** | Low coupling between modules? | MEDIUM |
| **Documentation** | Public APIs documented? | LOW |
| **Error Handling** | Errors handled, not swallowed? | HIGH |
| **Tests** | Adequate coverage for changes? | HIGH |

### Architectural Compliance

| Category | Check | Severity |
|----------|-------|----------|
| **Boundaries** | Module boundaries respected? | HIGH |
| **Patterns** | Established patterns followed? | MEDIUM |
| **Dependencies** | Dependency direction correct? | HIGH |
| **Single Responsibility** | Classes/modules focused? | MEDIUM |

---

## Severity Definitions

| Severity | Response | Examples |
|----------|----------|----------|
| **CRITICAL** | Block until fixed | Auth bypass, SQL injection, no value statement |
| **HIGH** | Fix before merge | Missing validation, N+1 queries, unclear scope |
| **MEDIUM** | Fix in current cycle | Code smells, missing docs, minor coupling |
| **LOW** | Track for later | Style issues, optimization opportunities |

---

## Finding Format

Document findings consistently:

```markdown
### [ID]: [Brief Title]
- **Severity**: CRITICAL / HIGH / MEDIUM / LOW
- **Status**: OPEN / ADDRESSED / RESOLVED / DEFERRED
- **Location**: [file:line or plan section]
- **Description**: [What is the issue?]
- **Impact**: [Why does this matter?]
- **Recommendation**: [How to fix?]
```

---

## Agent-Specific Guidance

### For Critic Agent
- Focus on plan quality, not implementation details
- Value statement assessment is mandatory first step
- Reference Planner constraints when reviewing
- Create critique in `agent-output/critiques/`

### For Security Agent
- Focus on OWASP Top 10 and injection patterns
- Reference `security-patterns` skill for detection
- Create audit in `agent-output/security/`
- Use CVSS-aligned severity

### For Architect Agent
- Focus on system-level design compliance
- Reference `architecture-patterns` skill
- Update `system-architecture.md` when issues found
- Include ADR updates if decisions affected
