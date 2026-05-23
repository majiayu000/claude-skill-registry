---
name: faion-ba-core
user-invocable: false
description: "BA Core: Planning, elicitation, requirements lifecycle, strategy analysis, solution evaluation. 21 methodologies."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---

# BA Core Sub-Skill

**Parent:** faion-business-analyst
**Focus:** Core BA practices - planning, elicitation, lifecycle management, strategy, evaluation

---

## Context Discovery

### Auto-Investigation

| Signal | Check For | Why |
|--------|-----------|-----|
| `.aidocs/` | Requirements docs, stakeholder lists | BA artifacts present |
| `docs/` or `requirements/` | Existing requirement patterns | Documentation standards |
| `STAKEHOLDERS.md` | Stakeholder registry | BA governance exists |
| `requirements.md` | Requirements format (user stories, use cases) | Elicitation approach |

### Discovery Questions

```yaml
questions:
  - question: "Do you have existing requirements documentation?"
    options:
      - label: "Yes, user stories (agile)"
        description: "Agile BA approach needed"
      - label: "Yes, formal requirements docs"
        description: "Traditional BA approach needed"
      - label: "No documentation yet"
        description: "Start with elicitation"
      - label: "Mixed/inconsistent"
        description: "Requirements lifecycle management needed"

  - question: "What's the current state of requirements?"
    options:
      - label: "Planning phase"
        description: "Use ba-planning, stakeholder-analysis"
      - label: "Gathering requirements"
        description: "Use elicitation-techniques"
      - label: "Analyzing/prioritizing"
        description: "Use requirements-prioritization"
      - label: "Validating/refining"
        description: "Use requirements-validation"

  - question: "Are you working in an agile or traditional environment?"
    options:
      - label: "Agile/Scrum"
        description: "Apply agile-ba-frameworks"
      - label: "Waterfall/traditional"
        description: "Apply traditional BA lifecycle"
      - label: "Hybrid"
        description: "Mix methodologies as needed"
```

---

## Methodologies (21)

### Planning & Governance (2)
- ba-planning.md - Define BA approach and deliverables
- stakeholder-analysis.md - Identify and analyze stakeholders

### Elicitation (1)
- elicitation-techniques.md - Interviews, workshops, surveys, observation

### Requirements Lifecycle (6)
- requirements-traceability.md - Track requirement relationships
- requirements-lifecycle.md - Manage requirements over time
- requirements-prioritization.md - MoSCoW, RICE, Kano, value/effort
- requirements-documentation.md - Formal requirements documentation
- requirements-validation.md - Validate against business goals
- ba-requirements-mgmt.md - Maintenance, change impact

### Strategy Analysis (3)
- strategy-analysis.md - Current/future state, gap analysis
- strategy-basics.md - Risk, change strategy fundamentals
- strategy-methods.md - Solution options, 50 techniques

### Solution Evaluation (1)
- solution-assessment.md - Measure, assess, improve

### Governance & Support (2)
- ba-governance.md - Governance, communication, prep
- ba-strategic-partnership.md - Innovation leadership

### Modern Practices (6)
- agile-ba-frameworks.md - Scrum, scaled agile
- ai-enabled-business-analysis.md - GenAI, agentic AI
- process-mining-automation.md - RPA, automation
- data-driven-requirements.md - Analytics-informed prioritization
- modern-ba-framework.md - BA Framework 2025-2026
- ba-trends-summary.md - Current trends

---

## When to Use

| If you need... | Methodology |
|----------------|-------------|
| Define BA approach | ba-planning |
| Map stakeholders | stakeholder-analysis |
| Gather requirements | elicitation-techniques |
| Track requirement links | requirements-traceability |
| Prioritize backlog | requirements-prioritization |
| Manage requirement changes | requirements-lifecycle |
| Analyze current vs future state | strategy-analysis |
| Evaluate delivered solution | solution-assessment |
| Work in agile environment | agile-ba-frameworks |
| Leverage AI for BA work | ai-enabled-business-analysis |

---

*BA Core Sub-Skill v1.0*
