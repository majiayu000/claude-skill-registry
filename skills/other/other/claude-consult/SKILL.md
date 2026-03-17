---
name: claude-consult
description: Consult Claude specialist agents during implementation for codebase understanding, pattern checking, security review, debugging help, and more. Use this skill whenever you're unsure about conventions, stuck on a failure, or need expert input before writing code. Does not replace the formal review gates in agent-loops — this is for mid-implementation consultation.
keywords:
  - consultation
  - claude agent
  - specialist
  - expert help
triggers:
  - unsure about codebase conventions
  - stuck on a test failure
  - need security or architecture guidance
  - before writing code in an unfamiliar area
---

# Claude Consult

Get expert help from Claude specialist agents during implementation. Each agent
has domain-specific skills pre-loaded and tools scoped to its role.

**This is NOT a replacement for the review gates.** The `agent-loops` skill
defines formal code review (`specialist-review`) and test audit
(`test-review-request`) gates that run after implementation. This skill is for
asking questions **during** implementation — before you've written code, while
you're writing it, or when you're stuck.

## When to Use

- "How does this module work?" — before implementing
- "Does my approach match existing conventions?" — while implementing
- "Is this pattern secure?" — before committing to a design
- "Why is this test failing?" — when stuck
- "What do the testing standards say about X?" — before writing tests
- "Is this component accessible?" — during UI work

## How to Invoke

```bash
claude -p --agent <agent-name> "<your question>"
```

All agents run headless (`-p` / print mode). They read the codebase, apply their
loaded skills, and return an answer to stdout. Capture or pipe as needed:

```bash
# Direct invocation
claude -p --agent debugger "Why is test_auth_flow failing in src/auth/tests.py?"

# Capture to variable
ANSWER=$(claude -p --agent security-auditor "Is the input validation in src/api/handler.py safe?")

# Save to file
claude -p --agent architect-reviewer "Does adding a cache layer between api and db match the existing architecture?" > /tmp/arch-advice.md
```

## Agent Roster

### Codebase Understanding

| Agent | Use when you need to... | Skills loaded |
|---|---|---|
| `search-specialist` | Find where something is defined or called | codanna-codebase-intelligence |
| `architect-reviewer` | Evaluate module boundaries and dependencies | system-design, api-design-patterns |
| `docs-architect` | Understand existing documentation structure | documentation-production, code-explanation |

### Code Quality & Patterns

| Agent | Use when you need to... | Skills loaded |
|---|---|---|
| `code-reviewer` | Check if code follows project conventions | code-quality-workflow, testing-anti-patterns, secure-coding-practices |
| `refiner` | Get suggestions for improving code quality | code-quality-workflow |
| `rest-expert` | Design or check REST API patterns | api-design-patterns |

### Security

| Agent | Use when you need to... | Skills loaded |
|---|---|---|
| `security-auditor` | Full security review of a code path | owasp-top-10, secure-coding-practices, vibe-security, security-testing-patterns |
| `owasp-top10-expert` | Check against OWASP Top 10 specifically | owasp-top-10, secure-coding-practices, vibe-security |
| `penetration-tester` | Identify exploitable vulnerabilities | security-testing-patterns, owasp-top-10, threat-modeling-techniques |
| `jwt-expert` | Review JWT/auth token handling | secure-coding-practices |
| `compliance-auditor` | Check regulatory compliance | secure-coding-practices, owasp-top-10 |

### Testing

| Agent | Use when you need to... | Skills loaded |
|---|---|---|
| `test-automator` | Plan test strategy or check coverage approach | test-review, python-testing-patterns, testing-anti-patterns |
| `vitest-expert` | Vitest-specific test patterns | testing-anti-patterns |

### Debugging

| Agent | Use when you need to... | Skills loaded |
|---|---|---|
| `debugger` | Investigate a test failure or error | systematic-debugging, root-cause-tracing |

### Performance

| Agent | Use when you need to... | Skills loaded |
|---|---|---|
| `performance-engineer` | Find bottlenecks in code paths | workflow-performance, python-performance-optimization, react-performance-optimization |
| `frontend-optimizer` | Optimize frontend bundle/rendering | react-performance-optimization, design-system-architecture |
| `performance-monitor` | Set up or check monitoring/observability | workflow-performance |

### Frontend & UI

| Agent | Use when you need to... | Skills loaded |
|---|---|---|
| `ui-ux-designer` | Review UI for usability and accessibility | ux-review, accessibility-audit, design-system-architecture |
| `component-architect` | Design component APIs and composition | design-system-architecture, typescript-advanced-patterns |
| `interaction-designer` | Review interaction patterns and states | ux-review, accessibility-audit |
| `state-architect` | Choose or review state management approach | react-performance-optimization, typescript-advanced-patterns |
| `react-specialist` | React-specific patterns and optimization | react-performance-optimization, typescript-advanced-patterns, testing-anti-patterns |
| `tailwind-expert` | Tailwind styling and responsive design | design-system-architecture, accessibility-audit |

### Language Specialists

| Agent | Use when you need to... | Skills loaded |
|---|---|---|
| `python-pro` | Python idioms, async, decorators | async-python-patterns, python-testing-patterns, python-performance-optimization |
| `rust-pro` | Ownership, lifetimes, traits | test-driven-development |
| `typescript-pro` | Advanced types and type safety | typescript-advanced-patterns, testing-anti-patterns |
| `javascript-pro` | JS/Node.js async and cross-runtime | testing-anti-patterns, typescript-advanced-patterns |
| `sql-pro` | Query optimization and schema design | database-design-patterns |

### Infrastructure

| Agent | Use when you need to... | Skills loaded |
|---|---|---|
| `cloud-architect` | AWS/Azure/GCP architecture decisions | terraform-best-practices, kubernetes-deployment-patterns, gitops-workflows |
| `kubernetes-architect` | K8s deployment and service mesh | kubernetes-deployment-patterns, kubernetes-security-policies, helm-chart-patterns, gitops-workflows |
| `terraform-specialist` | IaC modules and state management | terraform-best-practices |

### Data

| Agent | Use when you need to... | Skills loaded |
|---|---|---|
| `database-admin` | DB operations, backup, replication | database-design-patterns |
| `database-optimizer` | Slow queries, indexing, N+1 problems | database-design-patterns |
| `postgres-expert` | Postgres-specific schemas and migrations | database-design-patterns |

### Documentation

| Agent | Use when you need to... | Skills loaded |
|---|---|---|
| `mermaid-expert` | Generate architecture/flow diagrams | documentation-production |
| `tutorial-engineer` | Write tutorials and how-to guides | documentation-production, code-explanation |
| `technical-writer` | Write clear technical documentation | documentation-production, code-explanation |
| `reference-builder` | Generate API/config reference docs | documentation-production |

### Coordination & Meta

| Agent | Use when you need to... | Skills loaded |
|---|---|---|
| `orchestrator` | Break down complex tasks | task-orchestration, dispatching-parallel-agents |
| `prompt-engineer` | Craft or improve prompts for AI features | writing-skills |
| `learning-guide` | Understand a concept or pattern | code-explanation |

## Operating Rules

### 1. Consult, don't delegate implementation

These agents advise — they don't write your code. Read the answer, apply it
yourself. The agent may suggest approaches, but **you** implement them.

### 2. Scope your questions

Bad: `"Review everything in src/"`
Good: `"Is the input validation in src/api/handler.py:45-60 safe against injection?"`

Narrow questions get better answers and use fewer tokens.

### 3. Don't replace review gates

Consulting `security-auditor` during implementation doesn't skip the formal
`specialist-review` gate afterward. The review gates exist for independent
verification — consulting during implementation is for getting guidance early.

### 4. Use the cheapest agent that works

For factual lookups (where is X, what does the standard say), prefer
`search-specialist` or the language-specific agents. Reserve
`security-auditor`, `debugger`, and `performance-engineer` for questions
that need deeper analysis.

### 5. One question per invocation

Each `claude -p --agent` call is a cold start. Don't try to batch multiple
unrelated questions in one call — they'll get shallow treatment. Ask one
focused question per invocation.

## Relationship to agent-loops

```
agent-loops                          claude-consult
─────────────                        ──────────────
Formal review gates                  Mid-implementation help
Runs AFTER implementation            Runs DURING implementation
Produces reports with P0-P3          Answers questions directly
Required before merge                Optional, use as needed
specialist-review + test-review      Any agent from the roster
```

Both skills are designed to work together. Consult agents while implementing
to prevent issues, then run the formal review gates to verify nothing was missed.
