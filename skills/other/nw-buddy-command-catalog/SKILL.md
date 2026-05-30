---
name: nw-buddy-command-catalog
description: All /nw-* commands — what they do, when to use them, which agent they invoke. For the buddy agent to help users pick the right command.
user-invocable: false
disable-model-invocation: true
---

# Command Catalog

## Wave Commands (run in order per feature)

| Command | Wave | Agent | When to Use |
|---------|------|-------|-------------|
| `/nw-discover` | DISCOVER | product-discoverer (Scout) | Validate problem exists, customer interviews, opportunity mapping |
| `/nw-diverge` | DIVERGE | diverger (Flux) | Evaluate multiple solution approaches before committing |
| `/nw-discuss` | DISCUSS | product-owner (Luna) | Define user stories, journeys, acceptance criteria |
| `/nw-design` | DESIGN | system-designer, ddd-architect, solution-architect | Route to the right architect — system (scalability), domain (DDD), or application (components) |
| `/nw-devops` | DEVOPS | platform-architect | CI/CD, infrastructure, observability, deployment strategy |
| `/nw-distill` | DISTILL | acceptance-designer | Create executable acceptance tests (Given-When-Then) |
| `/nw-deliver` | DELIVER | software-crafter | Full implementation: roadmap -> execute -> finalize |

## Routing Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/nw-new` | Guided wizard for new features | Starting something new — asks what you're building, recommends starting wave |
| `/nw-continue` | Resume in-progress feature | Returning to a feature — detects progress, starts at next wave |
| `/nw-fast-forward` | Run remaining waves without pausing | When you trust the agents to proceed without review between waves |

## DELIVER Inner Loop Commands (manual mode)

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/nw-execute` | Run single roadmap step | Implementing one step at a time (learning mode) |
| `/nw-roadmap` | Create implementation plan | Planning steps before execution |
| `/nw-review` | Expert review of artifacts | Quality check on roadmap, code, or step output |
| `/nw-mutation-test` | Test suite effectiveness | After implementation — verifies tests catch real bugs |
| `/nw-finalize` | Archive completed feature | After all steps pass — creates evolution document |

## Cross-Wave Commands (any time)

| Command | Agent | When to Use |
|---------|-------|-------------|
| `/nw-research` | researcher (Nova) | Investigate technologies, patterns, decisions needing evidence |
| `/nw-document` | documentarist + researcher | Create DIVIO-compliant documentation (tutorial, how-to, reference, explanation) |
| `/nw-diagram` | solution-architect | Generate C4 architecture diagrams (Mermaid/PlantUML) |
| `/nw-refactor` | software-crafter | Systematic refactoring using RPP levels L1-L6 |
| `/nw-bugfix` | troubleshooter + crafter | Root cause analysis -> regression test -> fix via TDD |
| `/nw-root-why` | troubleshooter | Root cause analysis (5 Whys) without fix |
| `/nw-hotspot` | (self) | Git change frequency analysis — find most-changed files |
| `/nw-rigor` | (self) | Set quality-vs-token profile (lean/standard/thorough/exhaustive) |
| `/nw-forge` | agent-builder (Zeus) | Create new specialized agents |
| `/nw-mikado` | software-crafter | Complex refactoring roadmaps with visual tracking (experimental) |
| `/nw-buddy` | buddy (Guide) | Ask any question about nWave — methodology, commands, project state |

> For the full authoritative command reference, read `docs/reference/commands/index.md`.

## Common User Scenarios -> Command

| User Says | Recommend |
|-----------|-----------|
| "I want to build something new" | `/nw-new` (wizard) or `/nw-discover` (if problem unclear) |
| "I'm not sure which approach to take" | `/nw-diverge` |
| "I need user stories for this feature" | `/nw-discuss` |
| "How should I architect this?" | `/nw-design` |
| "I need to set up CI/CD" | `/nw-devops` |
| "I need acceptance tests" | `/nw-distill` |
| "I'm ready to implement" | `/nw-deliver` |
| "I want to continue my feature" | `/nw-continue` |
| "I need to research X" | `/nw-research` |
| "I need documentation" | `/nw-document` |
| "Something is broken" | `/nw-bugfix` or `/nw-root-why` |
| "My code needs cleanup" | `/nw-refactor` |
| "How good are my tests?" | `/nw-mutation-test` |
