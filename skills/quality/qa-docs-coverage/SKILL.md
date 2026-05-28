---
name: qa-docs-coverage
description: "Docs as QA: audit doc coverage and freshness, validate runbooks, and maintain documentation quality gates for APIs, services, events, and operational workflows."
---

# QA Docs Coverage (Dec 2025) — Discovery, Freshness, and Runbook Quality

**Modern Best Practices**: Phase-based audits, priority-driven documentation, automated coverage tracking

This skill provides operational workflows for auditing existing codebases, identifying documentation gaps, and systematically generating missing documentation. It complements [docs-codebase](../docs-codebase/SKILL.md) by providing the **discovery and analysis** layer.

**Key Principle**: Templates exist in docs-codebase. This skill tells you **what** to document and **how to find** undocumented components.

Core references: Diataxis documentation framework (https://diataxis.fr/) and OpenAPI (https://spec.openapis.org/oas/latest.html).

---

## When to Use This Skill

Invoke this skill when:

- Auditing documentation coverage for an existing codebase
- Generating documentation for legacy or underdocumented projects
- Creating documentation coverage reports
- Systematically documenting APIs, services, events, or database schemas
- Onboarding to a new codebase and need to understand what's documented vs not
- Preparing for compliance audits requiring documentation
- Setting up documentation maintenance processes

---

## Core QA (Default)

### What “Docs as QA” Means

- Treat docs as production quality artifacts: they reduce MTTR, enable safe changes, and define expected behavior.
- REQUIRED doc types for reliability and debugging ergonomics:
  - “How to run locally/CI” and “how to test”.
  - Operational runbooks (alerts, common failures, rollback).
  - Service contracts (OpenAPI/AsyncAPI) and schema examples.
  - Known issues and limitations (with workarounds).

### Coverage Model (Risk-Based)

- Prioritize docs by impact:
  - P1: externally consumed contracts and failure behavior (OpenAPI/AsyncAPI, auth, error codes, SLOs).
  - P2: internal integration and operational workflows (events, jobs, DB schema, runbooks).
  - P3: developer reference (configs, utilities).

### Freshness Checks (Prevent Stale Docs)

- Define owners, review cadence, and a “last verified” field for critical docs.
- CI economics [Inference]:
  - Block PRs only for missing/invalid P1 docs.
  - Warn for P2/P3 gaps; track via backlog.
- Run link checks and linting as fast pre-merge steps.

### Runbook Testability

- A runbook is “testable” if a new engineer can follow it and reach a measurable end state.
- Include: prerequisites, exact commands, expected outputs, rollback criteria, and escalation paths.

### Do / Avoid

Do:
- Keep docs close to code (same repo) and version them with changes.
- Use contracts and examples as the source of truth for integrations.

Avoid:
- Large “doc-only” projects with no owners and no CI gates.
- Writing runbooks that cannot be executed in a sandbox/staging environment.

## Quick Reference

| Audit Task | Tool/Pattern | Output | Priority |
|------------|--------------|--------|----------|
| **Discover APIs** | `**/*Controller.cs`, `**/routes/**/*.ts` | Component inventory | Use [discovery-patterns.md](resources/discovery-patterns.md) |
| **Calculate Coverage** | Compare inventory vs docs | Coverage report | Use [coverage-report-template.md](templates/coverage-report-template.md) |
| **Prioritize Gaps** | External-facing → P1, Internal → P2, Config → P3 | Documentation backlog | Use [priority-framework.md](resources/priority-framework.md) |
| **Generate Docs** | docs-codebase templates | Documentation files | Use [audit-workflows.md](resources/audit-workflows.md) Phase 3 |
| **Automate Checks** | CI/CD gates, PR templates | Continuous coverage | Use [cicd-integration.md](resources/cicd-integration.md) |

---

## Decision Tree: Documentation Audit Workflow

```text
User needs: [Audit Type]
    ├─ Starting fresh audit?
    │   ├─ Public-facing APIs? → Priority 1: External-Facing (OpenAPI, webhooks, error codes)
    │   ├─ Internal services/events? → Priority 2: Internal Integration (endpoints, schemas, jobs)
    │   └─ Configuration/utilities? → Priority 3: Developer Reference (options, helpers, constants)
    │
    ├─ Found undocumented component?
    │   ├─ API/Controller? → Scan endpoints → Use api-docs-template → Priority 1
    │   ├─ Service/Handler? → List responsibilities → Document contracts → Priority 2
    │   ├─ Database/Entity? → Generate ER diagram → Document entities → Priority 2
    │   ├─ Event/Message? → Map producer/consumer → Schema + examples → Priority 2
    │   └─ Config/Utility? → Extract options → Defaults + descriptions → Priority 3
    │
    ├─ Large codebase with many gaps?
    │   └─ Use phase-based approach:
    │       1. Discovery Scan → Coverage Analysis
    │       2. Prioritize by impact (P1 → P2 → P3)
    │       3. Generate docs incrementally (critical first)
    │       4. Set up maintenance (PR templates, quarterly audits)
    │
    └─ Maintaining existing docs?
        └─ Check for:
            ├─ Outdated docs (code changed, docs didn't) → Update or archive
            ├─ Orphaned docs (references non-existent code) → Remove
            └─ Missing coverage → Add to backlog → Prioritize
```

---

## Navigation: Discovery & Analysis

### Component Discovery

**Resource**: [resources/discovery-patterns.md](resources/discovery-patterns.md)

Language-specific patterns for discovering documentable components:

- .NET/C# codebase (Controllers, Services, DbContexts, Kafka handlers)
- Node.js/TypeScript codebase (Routes, Services, Models, Middleware)
- Python codebase (Views, Models, Tasks, Config)
- Go, Java/Spring, React/Frontend patterns
- Discovery commands (ripgrep, grep, find)
- Cross-reference discovery (Kafka topics, external APIs, webhooks)

### Priority Framework

**Resource**: [resources/priority-framework.md](resources/priority-framework.md)

Framework for prioritizing documentation efforts:

- Priority 1: External-Facing (public APIs, webhooks, auth) - Must document
- Priority 2: Internal Integration (services, events, database) - Should document
- Priority 3: Developer Reference (config, utilities) - Nice to have
- Prioritization decision tree
- Documentation debt scoring (formula + interpretation)
- Compliance considerations (ISO 27001, GDPR, HIPAA)

### Audit Workflows

**Resource**: [resources/audit-workflows.md](resources/audit-workflows.md)

Systematic workflows for conducting audits:

- Phase 1: Discovery Scan (identify all components)
- Phase 2: Coverage Analysis (compare against existing docs)
- Phase 3: Generate Documentation (use templates)
- Phase 4: Maintain Coverage (PR templates, CI/CD checks)
- Audit types (full, incremental, targeted)
- Audit checklist (pre-audit, during, post-audit)
- Tools and automation

### CI/CD Integration

**Resource**: [resources/cicd-integration.md](resources/cicd-integration.md)

Automated documentation checks and enforcement:

- PR template documentation checklists
- CI/CD coverage gates (GitHub Actions, GitLab CI, Jenkins)
- Pre-commit hooks (Git, Husky)
- Documentation linters (markdownlint, Vale, link checkers)
- Automated coverage reports
- Best practices and anti-patterns

---

## Navigation: Templates

### Coverage Report Template

**Template**: [templates/coverage-report-template.md](templates/coverage-report-template.md)

Structured coverage report with:

- Executive summary (coverage %, key findings, recommendations)
- Coverage by category (API, Service, Data, Events, Infrastructure)
- Gap analysis (P1, P2, P3 with impact/effort)
- Outdated documentation tracking
- Documentation debt score
- Action plan (sprints + ongoing)

### Documentation Backlog Template

**Template**: [templates/documentation-backlog-template.md](templates/documentation-backlog-template.md)

Backlog tracking with:

- Status summary (In Progress, To Do P1/P2/P3, Blocked, Completed)
- Task organization by priority
- Templates reference (quick links)
- Effort estimates (Low < 2h, Medium 2-8h, High > 8h)
- Review cadence (weekly, bi-weekly, monthly, quarterly)

---

## Output Artifacts

After running an audit, produce these artifacts:

1. **Coverage Report** - `.codex/docs/audit/coverage-report.md`
   - Overall coverage percentage
   - Detailed findings by category
   - Gap analysis with priorities
   - Recommendations and next audit date

2. **Documentation Backlog** - `.codex/docs/audit/documentation-backlog.md`
   - In Progress items with owners
   - To Do items by priority (P1, P2, P3)
   - Blocked items with resolution path
   - Completed items with dates

3. **Generated Documentation** - `.codex/docs/` (organized by category)
   - API reference (public/private)
   - Event catalog (Kafka/messaging)
   - Database schema (ER diagrams)
   - Background jobs (runbooks)

---

## Integration with Foundation Skills

This skill works closely with:

**[docs-codebase](../docs-codebase/SKILL.md)** - Provides templates for:

- [api-docs-template.md](../docs-codebase/templates/api-reference/api-docs-template.md) - REST API documentation
- [adr-template.md](../docs-codebase/templates/architecture/adr-template.md) - Architecture decisions
- [readme-template.md](../docs-codebase/templates/project-management/readme-template.md) - Project overviews
- [changelog-template.md](../docs-codebase/templates/project-management/changelog-template.md) - Release history

**Workflow**:

1. Use **qa-docs-coverage** to discover gaps
2. Use **docs-codebase** templates to fill gaps
3. Use **qa-docs-coverage** CI/CD integration to maintain coverage

---

## Anti-Patterns to Avoid

- **Documenting everything at once** - Prioritize by impact, document incrementally
- **Merging doc drafts without review** - Drafts must be validated by owners and runnable in practice
- **Ignoring outdated docs** - Outdated docs are worse than no docs
- **Documentation without ownership** - Assign owners for each doc area
- **Skipping the audit** - Don't assume you know what's documented
- **Blocking all PRs** - Only block for P1 gaps, warn for P2/P3

---

## Optional: AI / Automation

Do:
- Use AI to draft docs from code and tickets, then require human review and link/command verification.
- Use AI to propose “freshness diffs” and missing doc sections; validate by running the runbook steps.

Avoid:
- Publishing unverified drafts that include incorrect commands, unsafe advice, or hallucinated endpoints.

---

## Success Criteria

**Immediate (After Audit)**:

- Coverage report clearly shows gaps with priorities
- Documentation backlog is actionable and assigned
- Critical gaps (P1) identified with owners

**Short-term (1-2 Sprints)**:

- All P1 gaps documented
- Documentation coverage > 80% for external-facing components
- Documentation backlog actively managed

**Long-term (Ongoing)**:

- Quarterly audits show improving coverage (upward trend)
- PR documentation checklist compliance > 90%
- "How do I" questions in Slack decrease
- Onboarding time for new engineers decreases

---

## Related Skills

- **[docs-codebase](../docs-codebase/SKILL.md)** - Templates for writing documentation (README, ADR, API docs, changelog)
- **[docs-ai-prd](../docs-ai-prd/SKILL.md)** - PRD and tech spec templates for new features
- **[software-code-review](../software-code-review/SKILL.md)** - Code review including documentation standards

---

## Usage Notes

**For Claude**: When auditing a codebase:

1. **Start with discovery** - Use [resources/discovery-patterns.md](resources/discovery-patterns.md) to find components
2. **Calculate coverage** - Compare discovered components vs existing docs
3. **Prioritize gaps** - Use [resources/priority-framework.md](resources/priority-framework.md) to assign P1/P2/P3
4. **Follow workflows** - Use [resources/audit-workflows.md](resources/audit-workflows.md) for systematic approach
5. **Use templates** - Reference docs-codebase for documentation structure
6. **Set up automation** - Use [resources/cicd-integration.md](resources/cicd-integration.md) for ongoing maintenance

**Remember**: The goal is not 100% coverage, but **useful coverage** for the target audience. Document what developers, operators, and integrators actually need.
