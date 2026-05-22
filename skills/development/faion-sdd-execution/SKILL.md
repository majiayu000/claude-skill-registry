---
name: faion-sdd-execution
description: "SDD execution: quality gates, reflexion learning, pattern/mistake memory, code review."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# SDD Execution Sub-Skill

**Execution, quality, and learning phase of Specification-Driven Development.**

**Communication: User's language. Docs/code: English.**

---

## Context Discovery

### Auto-Investigation

| Signal | Check For | Why |
|--------|-----------|-----|
| `.aidocs/memory/` | Pattern/mistake memory files | Learning system in use |
| Test files | Test coverage, testing patterns | Quality gate readiness |
| CI/CD config | Automated quality gates | Pipeline integration |
| Code review comments | Review patterns, common issues | Review cycle effectiveness |
| `TASK-*.md` status | Task completion rate, blockers | Execution health |

### Discovery Questions

```yaml
questions:
  - question: "What quality level do you need?"
    options:
      - label: "High (Production)"
        description: "Apply L1-L6 quality gates"
      - label: "Medium (Development)"
        description: "Apply L1-L5 gates"
      - label: "Low (Prototype)"
        description: "Apply L1-L3 gates"

  - question: "Are you executing or reviewing?"
    options:
      - label: "Executing tasks"
        description: "Use workflow-execution-phase, quality-gates"
      - label: "Code review"
        description: "Use code-review-cycle, confidence-checks"
      - label: "Learning from mistakes"
        description: "Use reflexion-learning, mistake-tracking"

  - question: "Do you have context/token constraints?"
    options:
      - label: "Yes, large codebase"
        description: "Apply context-strategies, task-parallelization"
      - label: "No, small project"
        description: "Standard execution workflow"
```

---

## Philosophy

**Quality → Execution → Reflection → Learning** - continuous improvement through systematic gates and memory.

---

## Scope

This sub-skill handles:
- Task execution workflows
- Quality gates (L1-L6)
- Code review cycles
- Reflexion learning (PDCA)
- Pattern/mistake memory
- Context management
- Task parallelization

---

## Key Files

| Category | File |
|----------|------|
| **Workflow** | [sdd-workflow-overview.md](sdd-workflow-overview.md), [quick-reference.md](quick-reference.md), [workflow-execution-phase.md](workflow-execution-phase.md) |
| **Quality** | [quality-gates.md](quality-gates.md), [confidence-checks.md](confidence-checks.md), [code-review-cycle.md](code-review-cycle.md) |
| **Learning** | [reflexion-learning.md](reflexion-learning.md), [pattern-memory.md](pattern-memory.md), [mistake-tracking.md](mistake-tracking.md) |
| **Context** | [context-basics.md](context-basics.md), [context-strategies.md](context-strategies.md) |
| **Parallelization** | [task-parallelization.md](task-parallelization.md), [task-dependencies.md](task-dependencies.md) |
| **Patterns** | [design-docs-patterns-big-tech.md](design-docs-patterns-big-tech.md), [design-docs-patterns.md](design-docs-patterns.md) |

---

## Methodologies (20)

| Category | Count | Files |
|----------|-------|-------|
| Workflow | 4 | sdd-workflow-overview, quick-reference, section-summaries, workflow-execution-phase |
| Quality | 3 | quality-gates, confidence-checks, code-review-cycle |
| Learning | 4 | reflexion-learning, pattern-memory, mistake-tracking, mistake-prevention |
| Context | 2 | context-basics, context-strategies |
| Parallelization | 2 | task-parallelization, task-dependencies |
| Patterns | 2 | design-docs-patterns-big-tech, design-docs-patterns |
| Other | 3 | yaml-frontmatter, key-trends-summary, living-documentation-docs-as-code |

---

## Quality Gates

| Level | Phase | Checkpoint |
|-------|-------|------------|
| L1 | Spec | Requirements complete + feasible |
| L2 | Design | Architecture sound + scalable |
| L3 | Impl-Plan | Tasks atomic + 100k compliant |
| L4 | Task | Pre-execution validation |
| L5 | Completion | Tests pass + requirements met |
| L6 | Integration | System-level validation |

---

## Reflexion Cycle

```
PLAN → DO → CHECK → ACT
  |      |      |      |
 spec  execute review learn
              (gates) (memory)
```

---

## Related Sub-Skill

**faion-sdd-planning** - Specifications, design docs, implementation plans, task creation.

---

*faion-sdd-execution v1.0*
*Execution phase: quality → execute → reflect → learn*
