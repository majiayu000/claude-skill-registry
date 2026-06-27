---
name: dev-architecture-playbook
description: Route full software-development architecture work from product intent through design, implementation, testing, release, and operations. Use when the user asks for a complete development architecture, wants to know which Spellbook skills to combine, needs an execution path across PRD/spec/API/data/security/performance/release/SRE, or asks to turn an idea or repo into a production-ready engineering plan.
---

# Dev Architecture Playbook

## Purpose

Use this as the lifecycle router before starting broad product or architecture work. It chooses the minimum useful skill chain, defines gates, and prevents starting implementation before the required contracts exist.

## Route

Classify the request first:

| Request | Primary Skills | Output |
|---|---|---|
| Idea, product direction, or market/user problem | `product-discovery`, `prd-master` | Product brief, user stories, success metrics |
| Architecture or module boundaries | `architecture-foundation`, `technical-spec`, `elegant-architecture` | Architecture spec, boundaries, rejected alternatives |
| API, auth, data, or schema contract | `api-design`, `auth-security`, `database-patterns`, `data-contract-migrations` | Versioned contracts and migration plan |
| UI/product surface | `frontend-design`, `ui-ux-pro-max`, `ui-design-system`, `playwright-automation` | UX flow, component plan, visual checks |
| Implementation workflow | `fixflow`, `plan-flow`, `threads`, `systematic-debugging` | Step-test-update plan and ownership |
| Quality and regression risk | `comprehensive-testing`, `codebase-audit`, `vibeguard`, `project-health-auditor` | Test matrix and risk list |
| Release and operations | `release-engineering`, `config-secrets-environments`, `performance-capacity`, `incident-slo-runbook`, `observability-sre`, `devops-excellence` | Rollout, config, capacity, SLO, runbook |

## Required Gates

Do not treat the architecture as complete until these gates are explicit:

1. Goal and non-goals.
2. Domain model and ownership boundaries.
3. External API, data, and config contracts.
4. Security and permission model.
5. Test strategy with command-level verification.
6. Release, rollback, and migration gates.
7. Observability, SLO, and incident response.

If a gate is irrelevant, state why. Do not silently skip data, security, or rollback gates for production systems.

## Execution Pattern

Use this sequence for greenfield or major refactors:

1. Product: write the product brief or PRD.
2. Architecture: define modules, runtime boundaries, and tradeoffs.
3. Contracts: define API, data, config, and security contracts.
4. Plan: split work into independently verifiable steps.
5. Implement: use one workflow skill per step, not every skill at once.
6. Verify: run build, typecheck, tests, and focused behavioral checks.
7. Release: define rollout, migration, rollback, monitoring, and support owner.

For existing repos, start with `repo-agent-context-audit` or `codebase-audit` before proposing new structure.

## Output Shape

Return a compact plan:

```text
goal:
context:
selected_skill_chain:
architecture_gates:
implementation_steps:
verification_commands:
release_and_ops_gates:
open_risks:
```

Prefer the smallest chain that covers the risk. Too many skills at once usually means the scope needs to be split.
