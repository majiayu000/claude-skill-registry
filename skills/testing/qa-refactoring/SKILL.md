---
name: qa-refactoring
description: "Safe refactoring for quality engineering: characterization tests, seam creation, incremental steps, contracts, and CI quality gates to preserve behavior while changing structure."
---

# QA Refactoring Safety (Dec 2025) — Quick Reference

This skill provides execution-ready patterns for improving code quality and refactoring safely (preserve behavior, reduce risk, keep CI green).

Core references: Michael Feathers on characterization testing (https://michaelfeathers.silvrback.com/characterization-testing) and Martin Fowler’s Strangler Fig application pattern (https://martinfowler.com/bliki/StranglerFigApplication.html).

---

## Core QA (Default)

### Safe Refactor Loop (Behavior First)

- Baseline: tests green on main; reproduce the behavior you must preserve.
- Characterize: add characterization tests around current behavior before changing structure (Feathers: https://michaelfeathers.silvrback.com/characterization-testing).
- Create seams: introduce injection points/adapters to isolate dependencies.
- Refactor in small steps: one behavior-preserving change at a time, with CI staying green.
- Verify: run the smallest relevant suite locally, then full CI; monitor for regressions after merge.

### Test Strategy for Refactors

- Prefer contract and integration tests around boundaries to preserve behavior.
- Use snapshots/golden masters only when:
  - Output is stable and meaningful, and
  - You have a plan to review diffs and prevent “approve everything”.

### CI Economics and Debugging Ergonomics

- Keep refactor PRs small and reviewable; avoid refactor + feature in one PR.
- REQUIRED: failure artifacts for tests that guard refactors (logs/trace IDs, deterministic seeds).

### Do / Avoid

Do:
- Add missing tests before refactoring high-risk areas.
- Add guardrails (linters, type checks, contract checks) so refactors don’t silently break interfaces.

Avoid:
- Combining large structural refactors with behavior changes.
- Using flaky E2E as the primary safety net for refactors.

## Quick Reference

| Task | Tool/Pattern | Command/Approach | When to Use |
|------|--------------|------------------|-------------|
| Long method (>50 lines) | Extract Method | Split into smaller functions | Single method does too much |
| Large class (>300 lines) | Split Class | Create focused single-responsibility classes | God object doing too much |
| Duplicated code | Extract Function/Class | DRY principle | Same logic in multiple places |
| Complex conditionals | Replace Conditional with Polymorphism | Use inheritance/strategy pattern | Switch statements on type |
| Long parameter list | Introduce Parameter Object | Create DTO/config object | Functions with >3 parameters |
| Legacy code modernization | Characterization Tests + Strangler Fig | Write tests first, migrate incrementally | No tests, old codebase |
| Automated quality gates | ESLint, SonarQube, Prettier | `npm run lint`, CI/CD pipeline | Prevent quality regression |
| Technical debt tracking | SonarQube, CodeClimate | Debt ratio < 10% target | Prioritize refactoring work |

---

## Decision Tree: Refactoring Strategy

```text
Code issue: [Refactoring Scenario]
    ├─ Code Smells Detected?
    │   ├─ Duplicated code? → Extract method/function
    │   ├─ Long method (>50 lines)? → Extract smaller methods
    │   ├─ Large class (>300 lines)? → Split into focused classes
    │   ├─ Long parameter list? → Parameter object
    │   └─ Feature envy? → Move method closer to data
    │
    ├─ Legacy Code (No Tests)?
    │   ├─ High risk? → Write characterization tests first
    │   ├─ Large rewrite needed? → Strangler Fig (incremental migration)
    │   ├─ Unknown behavior? → Characterization tests + small refactors
    │   └─ Production system? → Canary deployments + monitoring
    │
    ├─ Quality Standards?
    │   ├─ New project? → Setup linter + formatter + quality gates
    │   ├─ Existing project? → Add pre-commit hooks + CI checks
    │   ├─ Complexity issues? → Set cyclomatic complexity limits (<10)
    │   └─ Technical debt? → Track in register, 20% sprint capacity
```

---

## When to Use This Skill

Use this skill when a user requests:

- Refactoring code to improve readability/maintainability
- Identifying and fixing code smells
- Managing technical debt
- Establishing code quality standards
- Setting up automated quality gates (linters, formatters)
- Modernizing legacy codebases
- Reducing code complexity
- Improving test coverage
- Code review automation
- Establishing refactoring strategies

---

## Operational Deep Dives

**Shared Foundation**

- [../software-clean-code-standard/resources/clean-code-standard.md](../software-clean-code-standard/resources/clean-code-standard.md) - Canonical clean code rules (`CC-*`) for citation
- Legacy playbook: [../software-clean-code-standard/resources/code-quality-operational-playbook.md](../software-clean-code-standard/resources/code-quality-operational-playbook.md) - `RULE-01`–`RULE-13`, decision trees, and operational procedures
- [../software-clean-code-standard/resources/refactoring-operational-checklist.md](../software-clean-code-standard/resources/refactoring-operational-checklist.md) - Refactoring smell-to-action mapping, safe refactoring guardrails
- [../software-clean-code-standard/resources/working-effectively-with-legacy-code-operational-checklist.md](../software-clean-code-standard/resources/working-effectively-with-legacy-code-operational-checklist.md) - Seams, characterization tests, incremental migration patterns

**Skill-Specific**

See [resources/operational-patterns.md](resources/operational-patterns.md) for detailed refactoring catalogs, automated quality gates, technical debt playbooks, and legacy modernization steps.

---

## Templates

See [templates/](templates/) for copy-paste ready examples organized by domain:

## Refactoring Process

Checklists and workflows for systematic code improvement:

- [Refactoring Checklist](templates/process/refactoring-checklist.md) - Refactor safety checklist (characterization tests + incremental steps)
- [Code Review Quality Checklist](templates/process/code-review-quality.md) - Quality-focused code review guide with SOLID principles

## Technical Debt Tracking

Tools for managing and prioritizing technical debt:

- [Technical Debt Register](templates/tracking/tech-debt-register.md) - Track and prioritize technical debt with impact/effort matrix

## Quality Gates Configuration

Automated quality enforcement by tech stack:

### JavaScript/TypeScript
- [ESLint Configuration](templates/quality-gates/javascript/eslint-config.js) - Comprehensive linting setup with complexity rules, code smell prevention

### Platform-Agnostic
- [SonarQube Setup](templates/quality-gates/platform-agnostic/sonarqube-setup.md) - Static analysis and quality gates for 20+ languages (Docker, Cloud, Server)

---

## Resources

See [resources/](resources/) for deep-dive guides:
- **Operational Patterns**: [resources/operational-patterns.md](resources/operational-patterns.md) - Core refactoring catalogs, quality gates, and legacy modernization
- **Refactoring Catalog**: [resources/refactoring-catalog.md](resources/refactoring-catalog.md)
- **Code Smells Guide**: [resources/code-smells-guide.md](resources/code-smells-guide.md)
- **Technical Debt Management**: [resources/tech-debt-management.md](resources/tech-debt-management.md)
- **Legacy Code Modernization**: [resources/legacy-code-strategies.md](resources/legacy-code-strategies.md)

---

## Optional: AI / Automation

Do:
- Use AI to propose mechanical refactors (rename/extract/move) only when you can prove behavior preservation via tests and contracts.
- Use AI to summarize diffs and risk hotspots; verify by running targeted characterization tests.

Avoid:
- Accepting refactors that change behavior without an explicit requirement and regression tests.
- Letting AI “fix tests” by weakening assertions to make CI green.

---

## Navigation

**Resources**
- [resources/operational-patterns.md](resources/operational-patterns.md)
- [resources/refactoring-catalog.md](resources/refactoring-catalog.md)
- [resources/code-smells-guide.md](resources/code-smells-guide.md)
- [resources/tech-debt-management.md](resources/tech-debt-management.md)
- [resources/legacy-code-strategies.md](resources/legacy-code-strategies.md)

**Templates**
- [templates/README.md](templates/README.md)
- [templates/process/refactoring-checklist.md](templates/process/refactoring-checklist.md)
- [templates/process/code-review-quality.md](templates/process/code-review-quality.md)
- [templates/process/README.md](templates/process/README.md)
- [templates/tracking/tech-debt-register.md](templates/tracking/tech-debt-register.md)
- [templates/tracking/README.md](templates/tracking/README.md)
- [templates/quality-gates/README.md](templates/quality-gates/README.md)
- [templates/quality-gates/javascript/eslint-config.js](templates/quality-gates/javascript/eslint-config.js)
- [templates/quality-gates/platform-agnostic/sonarqube-setup.md](templates/quality-gates/platform-agnostic/sonarqube-setup.md)

**Data**
- [data/sources.json](data/sources.json) — Curated external references

---
