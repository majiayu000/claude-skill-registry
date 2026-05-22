---
name: faion-sdd-planning
description: "SDD planning: specifications, design docs, implementation plans, task creation."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# SDD Planning Sub-Skill

**Documentation planning phase of Specification-Driven Development.**

**Communication: User's language. Docs/code: English.**

---

## Context Discovery

### Auto-Investigation

| Signal | Check For | Why |
|--------|-----------|-----|
| `.aidocs/` structure | SDD workflow in use (backlog, todo, in-progress, done) | SDD adoption status |
| `spec.md` files | Specification format and quality | Spec standards present |
| `design.md` files | Design doc patterns | Design approach |
| `implementation-plan.md` | Task breakdown structure | Planning methodology |
| `TASK-*.md` files | Task format, token estimates | Task creation standards |

### Discovery Questions

```yaml
questions:
  - question: "Which SDD phase are you in?"
    options:
      - label: "Writing specification"
        description: "Use writing-specifications, spec-structure"
      - label: "Creating design doc"
        description: "Use design-doc-structure, design-doc-writing-process"
      - label: "Breaking down into tasks"
        description: "Use writing-implementation-plans, task-creation-principles"
      - label: "Setting up SDD workflow"
        description: "Use workflows, templates"

  - question: "Do you have existing SDD documentation?"
    options:
      - label: "Yes, following SDD"
        description: "Continue with established patterns"
      - label: "Partial/inconsistent"
        description: "Standardize using templates"
      - label: "No, starting fresh"
        description: "Start with spec-structure, templates"

  - question: "What's your task complexity?"
    options:
      - label: "Simple features (<50k tokens)"
        description: "Standard task breakdown"
      - label: "Complex features (>100k tokens)"
        description: "Apply impl-plan-100k-rule, split features"
```

---

## Philosophy

**"Intent is the source of truth"** - specification is the main artifact, code is implementation.

**No Time Estimates:** Use complexity (Low/Medium/High) + token estimates (~Xk).

---

## Scope

This sub-skill handles:
- Writing specifications (WHAT + WHY)
- Creating design documents (HOW)
- Breaking down implementation plans (TASKS)
- Task creation and templating
- Workflow documentation

---

## Decision Tree

| If you need... | Use | File |
|----------------|-----|------|
| **Specifications** | | |
| Write spec | writing-specifications | [writing-specifications.md](writing-specifications.md) |
| Spec structure | spec-structure | [spec-structure.md](spec-structure.md) |
| Spec requirements | spec-requirements | [spec-requirements.md](spec-requirements.md) |
| Advanced guidelines | spec-advanced-guidelines | [spec-advanced-guidelines.md](spec-advanced-guidelines.md) |
| Basic examples | spec-examples-basic | [spec-examples-basic.md](spec-examples-basic.md) |
| E-commerce example | spec-example-ecommerce-cart | [spec-example-ecommerce-cart.md](spec-example-ecommerce-cart.md) |
| AI-assisted spec | ai-assisted-specification-writing | [ai-assisted-specification-writing.md](ai-assisted-specification-writing.md) |
| **Design Documents** | | |
| Design structure | design-doc-structure | [design-doc-structure.md](design-doc-structure.md) |
| Writing process | design-doc-writing-process | [design-doc-writing-process.md](design-doc-writing-process.md) |
| Advanced patterns | design-doc-advanced-patterns | [design-doc-advanced-patterns.md](design-doc-advanced-patterns.md) |
| Examples | design-doc-examples | [design-doc-examples.md](design-doc-examples.md) |
| **Implementation Plans** | | |
| Write impl-plan | writing-implementation-plans | [writing-implementation-plans.md](writing-implementation-plans.md) |
| 100k token rule | impl-plan-100k-rule | [impl-plan-100k-rule.md](impl-plan-100k-rule.md) |
| Components | impl-plan-components | [impl-plan-components.md](impl-plan-components.md) |
| Task format | impl-plan-task-format | [impl-plan-task-format.md](impl-plan-task-format.md) |
| Examples | impl-plan-examples | [impl-plan-examples.md](impl-plan-examples.md) |
| **Tasks** | | |
| Create tasks | task-creation-principles | [task-creation-principles.md](task-creation-principles.md) |
| Template guide | task-creation-template-guide | [task-creation-template-guide.md](task-creation-template-guide.md) |
| **Templates** | | |
| All templates | templates | [templates.md](templates.md) |
| Spec template | template-spec | [template-spec.md](template-spec.md) |
| Design template | template-design | [template-design.md](template-design.md) |
| Task template | template-task | [template-task.md](template-task.md) |
| **Workflows** | | |
| Workflow overview | workflows | [workflows.md](workflows.md) |
| Spec phase | workflow-spec-phase | [workflow-spec-phase.md](workflow-spec-phase.md) |
| Design phase | workflow-design-phase | [workflow-design-phase.md](workflow-design-phase.md) |
| **Other** | | |
| Backlog grooming | backlog-grooming-roadmapping | [backlog-grooming-roadmapping.md](backlog-grooming-roadmapping.md) |
| ADR | architecture-decision-records | [architecture-decision-records.md](architecture-decision-records.md) |
| API-first | api-first-development | [api-first-development.md](api-first-development.md) |

---

## Methodologies (28)

| Category | Count | Files |
|----------|-------|-------|
| Specifications | 7 | writing-specifications, spec-structure, spec-requirements, spec-advanced-guidelines, spec-examples-basic, spec-example-ecommerce-cart, ai-assisted-specification-writing |
| Design Documents | 4 | design-doc-structure, design-doc-writing-process, design-doc-advanced-patterns, design-doc-examples |
| Implementation Plans | 5 | writing-implementation-plans, impl-plan-100k-rule, impl-plan-components, impl-plan-task-format, impl-plan-examples |
| Tasks | 2 | task-creation-principles, task-creation-template-guide |
| Templates | 4 | templates, template-spec, template-design, template-task |
| Workflows | 3 | workflows, workflow-spec-phase, workflow-design-phase |
| Other | 3 | backlog-grooming-roadmapping, architecture-decision-records, api-first-development |

---

## Related Sub-Skill

**faion-sdd-execution** - Quality gates, reflexion, patterns, memory, execution workflows.

---

*faion-sdd-planning v1.0*
*Planning phase: specs → design → impl-plan → tasks*
