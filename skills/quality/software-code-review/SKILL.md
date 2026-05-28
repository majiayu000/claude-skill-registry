---
name: software-code-review
description: Patterns, checklists, and templates for systematic code review with a focus on correctness, security, readability, performance, and maintainability.
---

# Code Reviewing Skill — Quick Reference

This skill provides operational checklists and prompts for structured code review across languages and stacks. Use it when the primary task is reviewing existing code rather than designing new systems.

---

## Quick Reference

| Review Type | Focus Areas | Key Checklist | When to Use |
|-------------|-------------|---------------|-------------|
| Security Review | Auth, input validation, secrets, OWASP Top 10 | [software-security-appsec](../software-security-appsec/SKILL.md) | Security-critical code, API endpoints |
| Performance Review | N+1 queries, algorithms, caching, hot paths | DB queries, loops, memory allocation | High-traffic features, bottlenecks |
| Correctness Review | Logic, edge cases, error handling, tests | Boundary conditions, null checks, retries | Business logic, data transformations |
| Maintainability Review | Naming, complexity, duplication, readability | Function length, naming clarity, DRY | Complex modules, shared code |
| Test Review | Coverage, edge cases, flakiness, assertions | Test quality, missing scenarios | New features, refactors |
| Frontend Review | Accessibility, responsive design, performance | [frontend-review.md](templates/web-frontend/frontend-review.md) | UI/UX changes |
| Backend Review | API design, error handling, database patterns | [api-review.md](templates/backend-api/api-review.md) | API endpoints, services |
| Blockchain Review | Reentrancy, access control, gas optimization | [crypto-review.md](templates/blockchain/crypto-review.md) | Smart contracts, DeFi protocols |

---

## Specialized: .NET/EF Core Crypto Integration

Skip unless reviewing C#/.NET crypto/fintech services using Entity Framework Core.

For C#/.NET crypto/fintech services using Entity Framework Core, see:

- [resources/dotnet-efcore-crypto-rules.md](resources/dotnet-efcore-crypto-rules.md) — Complete review rules (correctness, security, async, EF Core, tests, MRs)

**Key rules summary:**

- Review only new/modified code in the MR
- Use `decimal` for financial values, UTC for dates
- Follow `CC-SEC-03` (no secrets in code) and `CC-OBS-02` (no sensitive data in logs)
- Async for I/O, pass `CancellationToken`, avoid `.Result`/`.Wait()` (see `CC-ERR-04`, `CC-FLOW-03`)
- EF Core: `AsNoTracking` for reads, avoid N+1, no dynamic SQL
- `Result<T>` pattern for explicit success/fail

---

## When to Use This Skill

Invoke this skill when the user asks to:

- Review a pull request or diff for issues
- Audit code for security vulnerabilities or injection risks
- Improve readability, structure, and maintainability
- Suggest targeted refactors without changing behavior
- Validate tests and edge-case coverage

## Decision Tree: Selecting Review Mode

```text
Code review task: [What to Focus On?]
    ├─ Security-critical changes?
    │   ├─ Auth/access control → Security Review (OWASP, auth patterns)
    │   ├─ User input handling → Input validation, XSS, SQL injection
    │   └─ Smart contracts → Blockchain Review (reentrancy, access control)
    │
    ├─ Performance concerns?
    │   ├─ Database queries → Check for N+1, missing indexes
    │   ├─ Loops/algorithms → Complexity analysis, caching
    │   └─ API response times → Profiling, lazy loading
    │
    ├─ Correctness issues?
    │   ├─ Business logic → Edge cases, error handling, tests
    │   ├─ Data transformations → Boundary conditions, null checks
    │   └─ Integration points → Retry logic, timeouts, fallbacks
    │
    ├─ Maintainability problems?
    │   ├─ Complex code → Naming, function length, duplication
    │   ├─ Hard to understand → Comments, abstractions, clarity
    │   └─ Technical debt → Refactoring suggestions
    │
    ├─ Test coverage gaps?
    │   ├─ New features → Happy path + error cases
    │   ├─ Refactors → Regression tests
    │   └─ Bug fixes → Reproduction tests
    │
    └─ Stack-specific review?
        ├─ Frontend → [frontend-review.md](templates/web-frontend/frontend-review.md)
        ├─ Backend → [api-review.md](templates/backend-api/api-review.md)
        ├─ Mobile → [mobile-review.md](templates/mobile/mobile-review.md)
        ├─ Infrastructure → [infrastructure-review.md](templates/infrastructure/infrastructure-review.md)
        └─ Blockchain → [crypto-review.md](templates/blockchain/crypto-review.md)
```

**Multi-Mode Reviews:**

For complex PRs, apply multiple review modes sequentially:

1. **Security first** (P0/P1 issues)
2. **Correctness** (logic, edge cases)
3. **Performance** (if applicable)
4. **Maintainability** (P2/P3 suggestions)

---

## Async Review Workflows (Dec 2025)

### Timezone-Friendly Reviews

| Practice | Implementation |
|----------|----------------|
| Review windows | Define 4-hour overlap windows |
| Review rotation | Assign reviewers across timezones |
| Async communication | Use PR comments, not DMs |
| Review SLAs | 24-hour initial response, 48-hour completion |

### Non-Blocking Reviews

```text
PR Submitted -> Auto-checks (CI) -> Async Review -> Merge
       |              |               |
  Author continues   If green,    Reviewer comments
  on other work      queue for    when available
                     review
```

**Anti-patterns:**

- Synchronous review meetings for routine PRs
- Blocking on reviewer availability for non-critical changes
- Single reviewer bottleneck

### Review Prioritization Matrix

| Priority | Criteria | SLA |
|----------|----------|-----|
| P0 | Security fix, production incident | 4 hours |
| P1 | Bug fix, blocking dependency | 24 hours |
| P2 | Feature work, tech debt | 48 hours |
| P3 | Documentation, refactoring | 72 hours |

---

### Optional: AI/Automation Extensions

> **Note**: AI-assisted review tools. Human review remains authoritative.

#### AI Review Assistants

| Tool | Use Case | Limitation |
|------|----------|------------|
| GitHub Copilot PR | Summary, suggestions | May miss context |
| CodeRabbit | Automated comments | Requires human validation |
| Graphite | PR stacking, review flow | Process, not content |

**AI assistant rules:**

- AI suggestions are advisory only
- Human reviewer approves/rejects
- AI cannot bypass security review
- AI findings require manual verification

#### AI Review Checklist

- [ ] AI suggestions validated against codebase patterns
- [ ] AI-flagged issues manually confirmed
- [ ] False positives documented for tool improvement
- [ ] Human reviewer explicitly approved

---

## Simplicity and Complexity Control

- Prefer existing, battle-tested libraries over bespoke implementations when behavior is identical.
- Flag avoidable complexity early: remove dead/commented-out code, collapse duplication, and extract single-responsibility helpers.
- Call out premature optimization; favor clarity and measured, evidence-based tuning.
- Encourage incremental refactors alongside reviews to keep modules small, predictable, and aligned to standards.

---

## Operational Playbooks

**Shared Foundation**

- [../software-clean-code-standard/resources/clean-code-standard.md](../software-clean-code-standard/resources/clean-code-standard.md) - Canonical clean code rules (`CC-*`) for citation in reviews
- Legacy playbook: [../software-clean-code-standard/resources/code-quality-operational-playbook.md](../software-clean-code-standard/resources/code-quality-operational-playbook.md) - `RULE-01`–`RULE-13`, refactoring decision trees, and design patterns

**Code Review Specific**

- [resources/operational-playbook.md](resources/operational-playbook.md) — Review scope rules, severity ratings (P0-P3), checklists, modes, and PR workflow patterns

## Navigation

**Resources**
- [resources/operational-playbook.md](resources/operational-playbook.md)
- [resources/review-checklist-comprehensive.md](resources/review-checklist-comprehensive.md)
- [resources/implementing-effective-code-reviews-checklist.md](resources/implementing-effective-code-reviews-checklist.md)
- [resources/looks-good-to-me-checklist.md](resources/looks-good-to-me-checklist.md)
- [resources/automation-tools.md](resources/automation-tools.md)
- [resources/dotnet-efcore-crypto-rules.md](resources/dotnet-efcore-crypto-rules.md)
- [resources/psychological-safety-guide.md](resources/psychological-safety-guide.md)

**Templates**
- [templates/core/pull-request-description-template.md](templates/core/pull-request-description-template.md)
- [templates/core/review-checklist-judgment.md](templates/core/review-checklist-judgment.md)
- [templates/core/review-comment-guidelines.md](templates/core/review-comment-guidelines.md)
- [templates/backend-api/api-review.md](templates/backend-api/api-review.md)
- [templates/web-frontend/frontend-review.md](templates/web-frontend/frontend-review.md)
- [templates/mobile/mobile-review.md](templates/mobile/mobile-review.md)
- [templates/infrastructure/infrastructure-review.md](templates/infrastructure/infrastructure-review.md)
- [templates/blockchain/crypto-review.md](templates/blockchain/crypto-review.md)
- [templates/data-ml/data-pipeline-review.md](templates/data-ml/data-pipeline-review.md)
- [templates/data-ml/experiment-tracking-review.md](templates/data-ml/experiment-tracking-review.md)
- [templates/data-ml/ml-model-review.md](templates/data-ml/ml-model-review.md)
- [templates/data-ml/ml-deployment-review.md](templates/data-ml/ml-deployment-review.md)

**Data**
- [data/sources.json](data/sources.json) — Curated external references
- Shared checklists: [../software-clean-code-standard/templates/checklists/secure-code-review-checklist.md](../software-clean-code-standard/templates/checklists/secure-code-review-checklist.md), [../software-clean-code-standard/templates/checklists/backend-api-review-checklist.md](../software-clean-code-standard/templates/checklists/backend-api-review-checklist.md)
