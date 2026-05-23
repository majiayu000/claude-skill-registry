---
name: faion-product-operations
description: "Product operations: prioritization (RICE, MoSCoW), backlog, analytics, feedback."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Product Operations Sub-Skill

**Communication: User's language. Docs: English.**

## Purpose

Day-to-day product operations: prioritization, backlog, analytics, feedback, lifecycle management.

**Parent:** [faion-product-manager](../faion-product-manager/SKILL.md)

---

## Context Discovery

### Auto-Investigation

Detect existing product operations artifacts:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| Backlog | `Glob("**/.aidocs/backlog/*")` or `Glob("**/backlog/*")` | Feature backlog exists |
| Prioritization | `Grep("RICE\\|MoSCoW\\|priority")` | Prioritization framework in use |
| Analytics | `Grep("analytics\\|metrics\\|KPI")` or `Glob("**/analytics/*")` | Product metrics tracked |
| Feedback | `Glob("**/feedback/*")` or `Grep("user feedback")` | Feedback process exists |
| Tech debt | `Glob("**/tech-debt/*")` or `Grep("technical debt")` | Tech debt managed |
| Experiments | `Grep("A/B test\\|experiment")` | Experimentation culture |
| Lifecycle docs | `Grep("lifecycle\\|maturity\\|growth")` | Lifecycle awareness |
| Stakeholder map | `Grep("stakeholder")` | Stakeholder management |

**Read existing operations artifacts:**
- Backlog structure and feature prioritization
- Analytics dashboards or KPI definitions
- Feedback collection process
- Tech debt register

### Discovery Questions

#### Q1: Operations Focus

```yaml
question: "What product operations area do you need help with?"
header: "Focus"
multiSelect: false
options:
  - label: "Prioritization (choose what to build)"
    description: "RICE, MoSCoW, or other prioritization framework"
  - label: "Backlog management (grooming)"
    description: "Organize features, epics, technical debt"
  - label: "Analytics and metrics (track performance)"
    description: "Define KPIs, setup dashboards, data analysis"
  - label: "Feedback management (user input)"
    description: "Collect, organize, and act on feedback"
```

#### Q2: Data Maturity

```yaml
question: "How data-driven is your product process?"
header: "Data"
multiSelect: false
options:
  - label: "No metrics yet"
    description: "Need to define KPIs and setup analytics"
  - label: "Basic analytics (usage, retention)"
    description: "Have metrics but need better insights"
  - label: "A/B testing and experiments"
    description: "Running experiments, optimizing based on data"
  - label: "Advanced (cohorts, funnels, ML)"
    description: "Sophisticated analytics, predictive models"
```

#### Q3: Product Type

```yaml
question: "What type of product are you managing?"
header: "Product"
multiSelect: false
options:
  - label: "SaaS B2B"
    description: "Enterprise or SMB software product"
  - label: "SaaS B2C"
    description: "Consumer software, focus on growth"
  - label: "AI-native or AI agent product"
    description: "LLM-powered, agentic AI considerations"
  - label: "Traditional software (non-SaaS)"
    description: "On-premise, desktop, or mobile app"
```

---

## Decision Tree

| If you need... | Use | File |
|----------------|-----|------|
| **Prioritize (data-driven)** | feature-prioritization-rice | [feature-prioritization-rice.md](feature-prioritization-rice.md) |
| **Prioritize (quick)** | feature-prioritization-moscow | [feature-prioritization-moscow.md](feature-prioritization-moscow.md) |
| **Manage backlog** | backlog-management | [backlog-management.md](backlog-management.md) |
| **Track metrics** | product-analytics | [product-analytics.md](product-analytics.md) |
| **Manage feedback** | feedback-management | [feedback-management.md](feedback-management.md) |
| **Lifecycle stage** | product-lifecycle | [product-lifecycle.md](product-lifecycle.md) |
| **Ops processes** | product-operations | [product-operations.md](product-operations.md) |
| **Stakeholder alignment** | stakeholder-management | [stakeholder-management.md](stakeholder-management.md) |
| **Technical debt** | technical-debt-management | [technical-debt-management.md](technical-debt-management.md) |
| **Growth strategy** | product-led-growth | [product-led-growth.md](product-led-growth.md) |
| **A/B testing** | experimentation-at-scale | [experimentation-at-scale.md](experimentation-at-scale.md) |
| **Learning velocity** | learning-speed-competitive-moat | [learning-speed-competitive-moat.md](learning-speed-competitive-moat.md) |
| **AI products** | ai-native-product-development | [ai-native-product-development.md](ai-native-product-development.md) |
| **AI agents** | agentic-ai-product-development | [agentic-ai-product-development.md](agentic-ai-product-development.md) |
| **Explainability** | product-explainability | [product-explainability.md](product-explainability.md) |
| **Team evolution** | blurred-roles-team-evolution | [blurred-roles-team-evolution.md](blurred-roles-team-evolution.md) |

---

## Core Methodologies (16)

### Prioritization
- **feature-prioritization-rice** - RICE scoring (Reach × Impact × Confidence / Effort)
- **feature-prioritization-moscow** - Must/Should/Could/Won't

### Operations
- **backlog-management** - DEEP principles, Definition of Ready
- **product-analytics** - Metrics and data analysis
- **feedback-management** - User feedback collection and processing
- **product-operations** - Operational processes and workflows
- **stakeholder-management** - Goal → Actor → Impact → Deliverable
- **technical-debt-management** - Debt tracking and paydown

### Lifecycle & Growth
- **product-lifecycle** - Intro/Growth/Maturity/Decline stages
- **product-led-growth** - PLG strategies and tactics
- **experimentation-at-scale** - A/B testing and experiments
- **learning-speed-competitive-moat** - Learning as competitive advantage

### AI & Modern Product
- **ai-native-product-development** - AI-first product design
- **agentic-ai-product-development** - AI agent products
- **product-explainability** - Making products understandable
- **blurred-roles-team-evolution** - Modern team structures

---

## Common Sequences

- **Backlog grooming:** backlog-management → feature-prioritization-rice → technical-debt-management
- **Metrics review:** product-analytics → feedback-management → experimentation-at-scale
- **Stakeholder sync:** stakeholder-management → product-lifecycle → product-operations

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [faion-product-manager](../faion-product-manager/SKILL.md) | Parent orchestrator |
| [faion-product-manager:planning](../faion-product-manager:planning/SKILL.md) | Sibling (MVP/roadmaps) |
| [faion-project-manager](../faion-project-manager/SKILL.md) | Execution coordination |
| [faion-business-analyst](../faion-business-analyst/SKILL.md) | Requirements analysis |

---

*Product Operations Sub-Skill v1.0*
*16 Methodologies*
