---
name: greenfield
version: 1.1.0
description: '[Planning] Start a new project from scratch with full waterfall inception — idea, research, domain modeling, tech stack, and implementation plan'
---

**MANDATORY IMPORTANT MUST** use `TaskCreate` to break ALL work into small tasks BEFORE starting.
**MANDATORY IMPORTANT MUST** use `AskUserQuestion` at EVERY stage — validate decisions before proceeding.
**MANDATORY IMPORTANT MUST** NEVER ask tech stack upfront — business analysis and domain modeling first.

## Quick Summary

**Goal:** Guide greenfield project inception from raw idea to an approved, implementable project plan using a full waterfall process.

**Workflow (16 steps):**

1. **Discovery** (`/idea`) — Interview user about problem, vision, constraints, team skills, scale. **DO NOT ask about tech stack** — keep business-focused.
2. **Market Research** (`/web-research`) — WebSearch for competitors, market landscape, existing solutions
3. **Deep Research** (`/deep-research`) — WebFetch top sources, extract key findings
4. **Business Evaluation** (`/business-evaluation`) — Viability assessment, risk matrix, value proposition
5. **Domain Analysis & ERD** (`/domain-analysis`) — Bounded contexts, aggregates, entities, ERD diagram, domain events. Validate every context boundary with user.
6. **Tech Stack Research** (`/tech-stack-research`) — Derive technical requirements from business + domain analysis. Research top 3 options per stack layer (backend, frontend, database, messaging, infra). Detailed pros/cons matrix, team-fit scoring, market analysis. Present comparison report for user to decide.
7. **Architecture Design** (`/architecture-design`) — Research and compare top 3 architecture styles (Clean, Hexagonal, Vertical Slice, etc.). Evaluate design patterns (CQRS, Repository, Mediator). Audit against SOLID, DRY, KISS, YAGNI. Validate scalability, maintainability, IoC, technical agnosticism. Present comparison with recommendation.
8. **Implementation Plan** (`/plan`) — Create phased plan using confirmed tech stack + architecture + domain model
9. **Security Audit** (`/security`) — Review plan for OWASP Top 10, auth patterns, data protection concerns
10. **Performance Audit** (`/performance`) — Review plan for performance bottlenecks, scalability, query optimization
11. **Plan Review** (`/plan-review`) — Full plan review, risk assessment, approval
12. **Refine to PBI** (`/refine`) — Transform idea + reviewed plan into actionable PBI with acceptance criteria
13. **User Stories** (`/story`) — Break PBI into implementable user stories
14. **Plan Validation** (`/plan-validate`) — Interview user with critical questions to validate plan + stories
15. **Test Strategy** (`/tdd-spec`) — Test pyramid, frameworks, spec outline
16. **Workflow End** (`/workflow-end`) — Clean up, announce completion

**Key Rules:**

- PLANNING ONLY: never implement code
- Every stage saves artifacts to plan directory
- **MANDATORY IMPORTANT MUST** every stage requires `AskUserQuestion` validation before proceeding
- Delegate architecture decisions to `solution-architect` agent
- Present 2-4 options for every major decision with confidence %
- **Business-First Protocol:** Tech stack is NEVER asked upfront. Business analysis (steps 1-5) + domain modeling (step 6) must complete first. Tech stack is derived from requirements through research and presented as a comparison report with options.
- **MANDATORY IMPORTANT MUST** architecture design and scaffold steps MUST include code quality gate tooling setup — linter, static analyzer, formatter, pre-commit hooks, CI quality gates, and build-time enforcement are NON-SKIPPABLE infrastructure.

## Entry Point

This skill is the explicit entry point for the `greenfield-init` workflow.

**When invoked:**

1. Activate the `greenfield-init` workflow via `/workflow-start greenfield-init`
2. The workflow handles step sequencing, task creation, and progress tracking
3. Each step delegates to the appropriate skill (idea, web-research, domain-analysis, tech-stack-research, etc.)
4. The `solution-architect` agent provides architecture guidance throughout

## When to Use

- Starting a brand-new project from scratch
- No existing codebase (empty project directory)
- Planning a new application before writing any code
- Want structured waterfall inception with user collaboration at every step

## When NOT to Use

- Existing codebase with code (use `/plan` or `/feature` instead)
- Bug fixes, refactoring, or feature implementation
- Quick prototyping (use `/cook-fast` instead)

## Output

All artifacts saved to plan directory:

```
plans/{id}/
  research/
    discovery-interview.md
    market-research.md
    deep-research.md
    business-evaluation.md
    domain-analysis.md
    tech-stack-comparison.md
    architecture-design.md
  phase-01-domain-model.md
  phase-02-tech-stack.md
  phase-02b-architecture.md
  phase-03-project-structure.md
  phase-04-test-strategy.md
  phase-05-backlog.md
  plan.md (master plan with YAML frontmatter)
```

After completion, recommend next step: `/cook` to scaffold the project structure.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

---

**MANDATORY IMPORTANT MUST** break work into small todo tasks — one per workflow step.
**MANDATORY IMPORTANT MUST** validate with user at EVERY step — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality and identify fixes/enhancements.
