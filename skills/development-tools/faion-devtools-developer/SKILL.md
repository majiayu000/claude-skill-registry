---
name: faion-devtools-developer
description: "DevTools orchestrator: code quality and automation."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# DevTools Developer Orchestrator

Coordinates code quality and automation sub-skills for development tooling.

## Purpose

Orchestrates two specialized sub-skills for developer tooling, architecture patterns, and automation.

---

## Context Discovery

### Auto-Investigation

| Signal | Check For | Why |
|--------|-----------|-----|
| Architecture docs | ADRs, design patterns | Code quality focus |
| Automation scripts | Browser automation, CI/CD | Tooling focus |
| Code review process | Review guidelines, checklists | Quality culture |
| Monorepo setup | Turborepo, pnpm workspaces | Tooling complexity |
| Testing infrastructure | E2E tests, performance tests | Automation maturity |

### Discovery Questions

```yaml
questions:
  - question: "Which area do you need?"
    options:
      - label: "Code quality/architecture"
        description: "Route to faion-code-quality"
      - label: "Automation/tooling"
        description: "Route to faion-automation-tooling"
      - label: "Both"
        description: "Use both sub-skills"

  - question: "What's your primary concern?"
    options:
      - label: "Architecture patterns (DDD, CQRS)"
        description: "Use faion-code-quality"
      - label: "Browser automation"
        description: "Use faion-automation-tooling"
      - label: "CI/CD pipelines"
        description: "Use faion-automation-tooling"
      - label: "Code review/refactoring"
        description: "Use faion-code-quality"
```

---

## When to Use

- Browser automation (Puppeteer, Playwright)
- Web scraping
- Code quality and review
- Architecture patterns (DDD, CQRS, Clean Architecture)
- Microservices design
- Code decomposition and refactoring
- CI/CD pipelines
- Development practices (XP, pair programming)
- Monorepo management
- Performance testing
- Feature flags
- Tech debt management

## Sub-Skills (46 methodologies total)

### faion-code-quality (23 methodologies)

Architecture patterns, code quality, refactoring, and development practices.

**Focus:** DDD, CQRS, Clean Architecture, Event Sourcing, code review, refactoring, tech debt, XP, pair/mob programming

### faion-automation-tooling (23 methodologies)

Browser automation, CI/CD pipelines, monorepo management, and developer tooling.

**Focus:** Puppeteer, Playwright, web scraping, CI/CD, monorepo, performance testing, A/B testing, feature flags, trunk-based development

## Routing Logic

| Task Type | Route To |
|-----------|----------|
| Architecture patterns, code review, refactoring | faion-code-quality |
| Browser automation, CI/CD, monorepo, testing | faion-automation-tooling |

## Tools

**Automation:** Puppeteer, Playwright, Selenium
**Code quality:** ESLint, Prettier, ruff, SonarQube
**Monorepo:** Turborepo, Nx, pnpm workspaces
**CI/CD:** GitHub Actions, GitLab CI, Jenkins
**Performance:** Lighthouse, k6, Artillery
**Feature flags:** LaunchDarkly, Unleash, PostHog

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-software-architect | Architecture design decisions |
| faion-devops-engineer | Infrastructure and deployment |
| faion-testing-developer | Testing strategies |

## Integration

Invoked by parent skill `faion-software-developer` for tooling, automation, and architecture work.

---

*faion-devtools-developer v1.0 | 46 methodologies across 2 sub-skills*
