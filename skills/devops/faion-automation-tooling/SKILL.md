---
name: faion-automation-tooling
description: "Automation & tooling specialist: browser automation, CI/CD, monorepo, performance testing, feature flags. 23 methodologies."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---

# Automation & Tooling Sub-Skill

Browser automation, CI/CD pipelines, monorepo management, and developer tooling.

## Purpose

Handles browser automation, web scraping, CI/CD pipelines, monorepo management, performance testing, feature flags, and development tooling.

---

## Context Discovery

### Auto-Investigation

| Signal | Check For | Why |
|--------|-----------|-----|
| CI/CD config | `.github/workflows/`, `.gitlab-ci.yml` | Pipeline automation |
| Monorepo structure | `turbo.json`, `pnpm-workspace.yaml` | Monorepo tooling |
| Testing setup | Performance test suites, k6 scripts | Testing automation |
| Feature flag config | LaunchDarkly, Unleash SDK | Feature flag usage |
| Browser automation | Puppeteer/Playwright scripts | Automation scripts |

### Discovery Questions

```yaml
questions:
  - question: "What automation do you need?"
    options:
      - label: "Browser automation/scraping"
        description: "Use puppeteer-automation or playwright-automation"
      - label: "CI/CD pipeline"
        description: "Use cd-basics, cd-pipelines"
      - label: "Monorepo management"
        description: "Use monorepo-turborepo, pnpm-package-management"
      - label: "Performance testing"
        description: "Use perf-test-basics, perf-test-tools"

  - question: "What's your monorepo scale?"
    options:
      - label: "Small (2-5 packages)"
        description: "Simple workspace setup"
      - label: "Medium (5-15 packages)"
        description: "Use Turborepo for caching"
      - label: "Large (15+ packages)"
        description: "Full Turborepo + pnpm optimization"

  - question: "Are you using feature flags?"
    options:
      - label: "Yes, in production"
        description: "Use feature-flags for best practices"
      - label: "Planning to implement"
        description: "Start with feature-flags basics"
      - label: "No"
        description: "Skip feature flag methodologies"
```

---

## When to Use

- Browser automation (Puppeteer, Playwright)
- Web scraping
- CI/CD pipelines
- Monorepo management (Turborepo, pnpm)
- Performance testing
- A/B testing
- Feature flags
- Trunk-based development
- Logging patterns
- Internationalization
- AI-assisted development

## Methodologies (23 files)

**Browser Automation (4):** puppeteer-automation, playwright-automation, browser-automation-overview, web-scraping

**DevOps (3):** cd-basics, cd-pipelines, continuous-delivery

**Dev Methodologies (3):** dev-methodologies-architecture, dev-methodologies-practices, dev-methodologies-testing

**Tooling (5):** pnpm-package-management, monorepo-turborepo, feature-flags, internationalization, logging-patterns

**Testing & Quality (4):** perf-test-basics, perf-test-tools, ab-testing-basics, ab-testing-implementation

**Trunk-Based Dev (2):** trunk-based-dev-principles, trunk-based-dev-patterns

**Modern Practices (2):** ai-assisted-dev, best-practices-2026

## Tools

**Automation:** Puppeteer, Playwright, Selenium
**Monorepo:** Turborepo, Nx, pnpm workspaces
**CI/CD:** GitHub Actions, GitLab CI, Jenkins
**Performance:** Lighthouse, k6, Artillery
**Feature flags:** LaunchDarkly, Unleash, PostHog

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-code-quality | Code quality and architecture |
| faion-devops-engineer | Infrastructure and deployment |
| faion-cicd-engineer | Advanced CI/CD |

## Integration

Invoked by parent skill `faion-devtools-developer` for automation and tooling work.

---

*faion-automation-tooling v1.0 | 23 methodologies*
