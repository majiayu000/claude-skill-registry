---
name: router-operations
description: Master orchestration for routing QA, testing, DevOps, observability, and git workflow questions through 15 operational skills
metadata:
  version: "1.2"
---

# Router: Operations

Master orchestrator that routes quality assurance, testing, deployment, observability, and git workflow questions through the complete operations skill set.

---

## Decision Tree: Where to Start?

```
OPERATIONS QUESTION
    │
    ├─► "How to test this?" ────────────► qa-testing-strategy
    │                                      └─► Unit, integration, E2E, BDD
    │
    ├─► "Write Playwright tests" ───────► qa-testing-playwright
    │                                      └─► E2E, page objects, CI/CD
    │
    ├─► "Test iOS app" ─────────────────► qa-testing-ios
    │                                      └─► XCTest, simulator, UI testing
    │
    ├─► "Test mobile app" ──────────────► qa-testing-mobile
    │                                      └─► iOS + Android, device matrix
    │
    ├─► "API contract testing" ─────────► qa-api-testing-contracts
    │                                      └─► OpenAPI, GraphQL, gRPC
    │
    ├─► "Debug this issue" ─────────────► qa-debugging
    │                                      └─► Troubleshooting, logging, profiling
    │
    ├─► "Improve error handling" ───────► qa-resilience
    │                                      └─► Circuit breakers, retries, chaos
    │
    ├─► "Setup monitoring" ─────────────► qa-observability
    │                                      └─► OpenTelemetry, tracing, SLOs
    │
    ├─► "Refactor this code" ───────────► qa-refactoring
    │                                      └─► Code smells, tech debt, patterns
    │
    ├─► "Check docs coverage" ──────────► qa-docs-coverage
    │                                      └─► Gap analysis, coverage reports
    │
    ├─► "Test LLM agent" ───────────────► qa-agent-testing
    │                                      └─► Test suites, scoring, refusals
    │
    ├─► "Deploy to production" ─────────► ops-devops-platform
    │                                      └─► K8s, Terraform, GitOps, SRE
    │
    ├─► "Write commit message" ─────────► git-commit-message
    │                                      └─► Conventional commits
    │
    ├─► "Git workflow / branching" ─────► git-workflow
    │                                      └─► GitHub Flow, PRs, reviews
    │
    ├─► "Create documentation" ─────────► docs-codebase
    │                                      └─► README, API docs, ADRs
    │
    ├─► "Write PRD for AI agent" ───────► docs-ai-prd
    │                                      └─► CLAUDE.md, agentic planning
    │
    └─► "Full operations audit" ────────► COMPREHENSIVE ANALYSIS
                                           └─► All operational dimensions
```

---

## Domain Detection

### Domain 1: TESTING & QA

**Triggers**: "test", "testing", "QA", "quality", "coverage", "assertion", "mock", "E2E", "unit test", "integration test", "API test", "contract test"

**Primary Skills**:

| Skill | When to Use |
|-------|-------------|
| `qa-testing-strategy` | Overall test strategy, frameworks |
| `qa-testing-playwright` | E2E web testing, browser automation |
| `qa-testing-ios` | iOS simulator testing, XCTest |
| `qa-testing-mobile` | Cross platform mobile testing |
| `qa-api-testing-contracts` | API schema and contract testing |
| `qa-agent-testing` | LLM agent/persona testing |

**Skill Chain - Complete Test Setup**:
```
qa-testing-strategy (strategy) → qa-testing-playwright (E2E)
    → qa-testing-ios (iOS) → qa-testing-mobile (cross platform)
    → qa-api-testing-contracts (API) → qa-agent-testing (AI agents)
```

### Domain 2: DEBUGGING & RESILIENCE

**Triggers**: "debug", "error", "bug", "crash", "exception", "retry", "circuit breaker", "timeout", "failure"

**Primary Skills**:

| Skill | When to Use |
|-------|-------------|
| `qa-debugging` | Troubleshooting, logging, profiling |
| `qa-resilience` | Error handling, circuit breakers, chaos |
| `qa-refactoring` | Code quality, tech debt |

**Skill Chain - Production Issues**:
```
qa-debugging (identify issue) → qa-resilience (prevent recurrence)
    → qa-refactoring (improve code quality)
```

### Domain 3: OBSERVABILITY & MONITORING

**Triggers**: "monitor", "metrics", "tracing", "logging", "SLO", "SLI", "alerting", "APM", "OpenTelemetry"

**Primary Skills**:

| Skill | When to Use |
|-------|-------------|
| `qa-observability` | Full observability stack |
| `ops-devops-platform` | Infrastructure monitoring |

**Skill Chain - Observability Setup**:
```
qa-observability (instrumentation) → ops-devops-platform (infrastructure)
    → qa-debugging (incident response)
```

### Domain 4: DEPLOYMENT & INFRASTRUCTURE

**Triggers**: "deploy", "Kubernetes", "Docker", "Terraform", "CI/CD", "GitOps", "infrastructure", "SRE"

**Primary Skills**:

| Skill | When to Use |
|-------|-------------|
| `ops-devops-platform` | Full DevOps stack |
| `git-workflow` | Deployment workflows |

**Skill Chain - Production Deployment**:
```
git-workflow (branching strategy) → ops-devops-platform (CI/CD + K8s)
    → qa-observability (monitoring) → qa-resilience (failure handling)
```

### Domain 5: GIT & VERSION CONTROL

**Triggers**: "git", "commit", "branch", "PR", "pull request", "merge", "rebase", "code review"

**Primary Skills**:

| Skill | When to Use |
|-------|-------------|
| `git-commit-message` | Conventional commit messages |
| `git-workflow` | Branching, PRs, reviews |

**Skill Chain - Git Workflow**:
```
git-workflow (strategy) → git-commit-message (commits)
    → software-code-review (PR reviews)
```

### Domain 6: DOCUMENTATION

**Triggers**: "documentation", "README", "API docs", "ADR", "PRD", "changelog", "docs"

**Primary Skills**:

| Skill | When to Use |
|-------|-------------|
| `docs-codebase` | Technical documentation |
| `docs-ai-prd` | PRDs for AI agents |
| `qa-docs-coverage` | Documentation gaps |

**Skill Chain - Documentation**:
```
qa-docs-coverage (audit) → docs-codebase (write docs)
    → docs-ai-prd (if AI project)
```

---

## Skill Registry

### Testing & QA (7)

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| `qa-testing-strategy` | Test strategy | Test pyramid, frameworks, coverage |
| `qa-testing-playwright` | E2E web testing | Page objects, auth flows, CI |
| `qa-testing-ios` | iOS testing | XCTest, simulator, UI tests |
| `qa-testing-mobile` | Cross-platform mobile | iOS + Android, device matrix |
| `qa-api-testing-contracts` | API contract testing | OpenAPI, GraphQL, gRPC |
| `qa-agent-testing` | LLM agent testing | Test suites, scoring rubrics |
| `qa-docs-coverage` | Docs audit | Gap analysis, coverage reports |

### Debugging & Quality (3)

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| `qa-debugging` | Debugging | Troubleshooting, logging, profiling |
| `qa-resilience` | Resilience | Circuit breakers, retries, chaos |
| `qa-refactoring` | Code quality | Smell detection, refactoring |

### Observability (1)

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| `qa-observability` | Monitoring | OpenTelemetry, SLOs, APM |

### DevOps & Infrastructure (1)

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| `ops-devops-platform` | DevOps | K8s, Terraform, GitOps, SRE |

### Git & Version Control (2)

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| `git-commit-message` | Commits | Conventional commit messages |
| `git-workflow` | Workflows | Branching, PRs, reviews |

### Documentation (3)

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| `docs-codebase` | Tech docs | README, API docs, ADRs |
| `docs-ai-prd` | AI PRDs | Agent specs, CLAUDE.md |
| `qa-docs-coverage` | Docs gaps | Coverage audit |

---

## Routing Logic

### Keyword-Based Routing

```
KEYWORDS -> SKILL MAPPING

"test strategy", "test pyramid", "coverage" -> qa-testing-strategy
"Playwright", "E2E", "browser test", "page object" -> qa-testing-playwright
"iOS test", "XCTest", "simulator", "xcrun" -> qa-testing-ios
"mobile test", "Android test", "device matrix", "Appium" -> qa-testing-mobile
"API test", "contract test", "OpenAPI", "schema validation" -> qa-api-testing-contracts
"agent test", "LLM test", "persona test", "refusal" -> qa-agent-testing
"docs coverage", "undocumented", "gap analysis" -> qa-docs-coverage

"debug", "troubleshoot", "stack trace", "profiling" -> qa-debugging
"resilience", "circuit breaker", "retry", "chaos" -> qa-resilience
"refactor", "code smell", "tech debt", "clean code" -> qa-refactoring

"observability", "tracing", "metrics", "SLO", "SLI" -> qa-observability
"OpenTelemetry", "APM", "distributed tracing" -> qa-observability

"deploy", "Kubernetes", "K8s", "Terraform" -> ops-devops-platform
"Docker", "container", "GitOps", "ArgoCD" -> ops-devops-platform
"CI/CD", "pipeline", "GitHub Actions" -> ops-devops-platform
"SRE", "reliability", "incident" -> ops-devops-platform

"commit message", "conventional commit" -> git-commit-message
"git workflow", "branching", "PR", "code review" -> git-workflow
"merge", "rebase", "trunk-based" -> git-workflow

"README", "API docs", "ADR", "changelog" -> docs-codebase
"PRD", "CLAUDE.md", "AI agent spec" -> docs-ai-prd
```

### Context-Based Routing

| User Context | Primary Skill | Supporting Skills |
|--------------|---------------|-------------------|
| Starting testing | `qa-testing-strategy` | `qa-testing-playwright`, `qa-testing-ios` |
| Production bug | `qa-debugging` | `qa-resilience`, `qa-observability` |
| Deploying app | `ops-devops-platform` | `git-workflow`, `qa-observability` |
| Code quality | `qa-refactoring` | `qa-debugging`, `software-code-review` |
| Git setup | `git-workflow` | `git-commit-message` |
| Writing docs | `docs-codebase` | `qa-docs-coverage` |
| Testing AI agent | `qa-agent-testing` | `ai-agents`, `ai-prompt-engineering` |

---

## Skill Chain Patterns

### Pattern 1: Complete Test Strategy

```
START
  │
  ▼
qa-testing-strategy ────────► Test pyramid + frameworks
  │
  ├─────────────────────────────────────┐
  ▼                                     ▼
qa-testing-playwright ► E2E    qa-testing-ios ► Mobile
  │                                     │
  └─────────────────┬───────────────────┘
                    ▼
           qa-agent-testing ──► AI agents (if applicable)
                    │
                    ▼
              COMPLETE TEST SUITE
```

### Pattern 2: Production Readiness

```
START
  │
  ▼
qa-testing-strategy ────────► Tests pass
  │
  ▼
qa-resilience ──────────────► Error handling
  │
  ▼
qa-observability ───────────► Monitoring setup
  │
  ▼
ops-devops-platform ────────► CI/CD + deployment
  │
  ▼
git-workflow ───────────────► Release process
  │
  ▼
PRODUCTION READY
```

### Pattern 3: Incident Response

```
INCIDENT
  │
  ▼
qa-debugging ───────────────► Root cause analysis
  │
  ▼
qa-observability ───────────► Check metrics/traces
  │
  ▼
qa-resilience ──────────────► Prevent recurrence
  │
  ▼
qa-refactoring ─────────────► Fix underlying issues
  │
  ▼
docs-codebase ──────────────► Post-mortem doc
  │
  ▼
INCIDENT RESOLVED
```

### Pattern 4: LLM Agent Testing

```
START
  │
  ▼
qa-agent-testing ───────────► Test suite design
  │
  ├─► Must-ace tasks ────────► Core functionality
  ├─► Refusal edge cases ────► Safety boundaries
  ├─► Scoring rubric ────────► 6-dimension evaluation
  │
  ▼
ai-prompt-engineering ──────► Prompt improvements
  │
  ▼
VALIDATED AGENT
```

### Pattern 5: Documentation Audit

```
START
  │
  ▼
qa-docs-coverage ───────────► Gap analysis
  │
  ▼
docs-codebase ──────────────► Write missing docs
  │
  ▼
docs-ai-prd ────────────────► AI agent specs (if applicable)
  │
  ▼
git-workflow ───────────────► PR with docs
  │
  ▼
DOCS COMPLETE
```

---

## Comprehensive Analysis Mode

For full operations audit, invoke skills in parallel:

### Layer 1: Quality Assessment (Parallel)

| Skill | Output | Purpose |
|-------|--------|---------|
| `qa-testing-strategy` | Test coverage | What's tested? |
| `qa-docs-coverage` | Doc coverage | What's documented? |
| `qa-refactoring` | Code quality | Tech debt assessment |

### Layer 2: Operational Readiness

| Skill | Output | Purpose |
|-------|--------|---------|
| `qa-resilience` | Error handling | Failure modes |
| `qa-observability` | Monitoring | Visibility gaps |
| `ops-devops-platform` | Infrastructure | Deployment gaps |

### Layer 3: Process

| Skill | Output | Purpose |
|-------|--------|---------|
| `git-workflow` | Git practices | Process gaps |
| `git-commit-message` | Commit quality | Changelog readiness |

---

## Cross-Router Handoffs

### To router-engineering

When user needs implementation:
- "Build the fix" → Route to `software-backend` or `software-frontend`
- "Implement retry logic" → Route to `software-backend`
- "Add UI for monitoring" → Route to `software-frontend`

### To router-startup

When user shifts to business:
- "Is this ready to launch?" → Route to `startup-go-to-market`
- "How to price monitoring service?" → Route to `startup-business-models`

### From router-engineering

When router-engineering detects ops needs:
- "How do I test this?" → Route here
- "Deploy to production" → Route here
- "Setup CI/CD" → Route here

---

## Quality Gates

### Pre-Deployment Checklist

| Gate | Skill | Criteria |
|------|-------|----------|
| Tests pass | `qa-testing-strategy` | >80% coverage |
| E2E pass | `qa-testing-playwright` | Critical flows green |
| Error handling | `qa-resilience` | Circuit breakers configured |
| Monitoring | `qa-observability` | SLOs defined, alerts set |
| Docs | `qa-docs-coverage` | README, API docs complete |
| Security | Route to `software-security-appsec` | OWASP checklist |

### Post-Deployment Checklist

| Gate | Skill | Criteria |
|------|-------|----------|
| Metrics flowing | `qa-observability` | Dashboards populated |
| Alerts working | `qa-observability` | Test alert fired |
| Logs searchable | `qa-debugging` | Can query recent logs |
| Rollback tested | `ops-devops-platform` | Rollback procedure verified |

---

## Output Templates

### Quick Analysis Output

```markdown
## Operations Analysis: {{TOPIC}}

**Domain Detected**: {{DOMAIN}}
**Primary Skill**: {{SKILL}}
**Supporting Skills**: {{LIST}}

### Current State
- Tests: {{TEST_STATUS}}
- Monitoring: {{MONITORING_STATUS}}
- Docs: {{DOCS_STATUS}}

### Recommended Actions
1. {{ACTION_1}} - Use {{SKILL}}
2. {{ACTION_2}} - Use {{SKILL}}

### Skills to Invoke
- {{SKILL_1}}: {{WHY}}
- {{SKILL_2}}: {{WHY}}
```

### Operations Audit Output

```markdown
## Operations Audit: {{PROJECT}}

### Testing
- Strategy: {{STATUS}} - {{NOTES}}
- E2E Coverage: {{%}}
- Agent Tests: {{STATUS}}

### Resilience
- Error Handling: {{STATUS}}
- Circuit Breakers: {{STATUS}}
- Retry Policies: {{STATUS}}

### Observability
- Metrics: {{STATUS}}
- Tracing: {{STATUS}}
- Logging: {{STATUS}}
- SLOs: {{STATUS}}

### Infrastructure
- CI/CD: {{STATUS}}
- Deployment: {{STATUS}}
- Rollback: {{STATUS}}

### Documentation
- README: {{STATUS}}
- API Docs: {{STATUS}}
- ADRs: {{STATUS}}

### Priority Actions
1. {{HIGH_PRIORITY_1}}
2. {{HIGH_PRIORITY_2}}
3. {{HIGH_PRIORITY_3}}
```

---

## Resources

| Resource | Purpose |
|----------|---------|
| `resources/routing-logic.md` | Detailed routing rules |
| `resources/quality-gates.md` | Deployment checklists |
| `resources/incident-response.md` | Incident playbook |

## Templates

| Template | Purpose |
|----------|---------|
| `templates/operations-audit.md` | Full audit report |
| `templates/test-strategy.md` | Test planning |
| `templates/incident-postmortem.md` | Post-mortem doc |

## Data

| File | Purpose |
|------|---------|
| `data/skill-registry.json` | Operations skills index |
| `data/sources.json` | Reference sources |
