---
name: faion-product-manager
description: "Product orchestrator: planning (MVP, roadmaps) and operations (prioritization, backlog)."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Bash(ls:*), Bash(mkdir:*), Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Product Manager Skill

**Communication: User's language. Docs: English.**

## Purpose

Orchestrates product management activities: planning, operations, discovery, launch.

**Architecture:** Orchestrator → 2 sub-skills (17 + 16 methodologies)

---

## Context Discovery

### Auto-Investigation

Check for existing product artifacts:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| `constitution.md` | `Glob("**/.aidocs/constitution.md")` | Product defined |
| `roadmap.md` | `Glob("**/.aidocs/roadmap.md")` | Roadmap exists |
| `backlog/` | `Glob("**/.aidocs/backlog/*")` | Backlog items exist |
| `todo/` | `Glob("**/.aidocs/todo/*")` | Ready-to-execute features |
| `user-personas.md` | `Glob("**/user-personas.md")` | Users defined |
| `mvp-scope.md` | `Glob("**/mvp*.md")` | MVP defined |

**Read existing artifacts:**
- constitution.md for product vision and constraints
- roadmap.md for current plans and priorities
- Any existing specs or design docs

### Discovery Questions

Use `AskUserQuestion` to understand product management needs.

#### Q1: Product Stage

```yaml
question: "What stage is your product at?"
header: "Stage"
multiSelect: false
options:
  - label: "Idea (need to define MVP)"
    description: "No code yet, scoping what to build"
  - label: "MVP defined (need to plan execution)"
    description: "Scope clear, need roadmap and backlog"
  - label: "Building (need to manage backlog)"
    description: "Development in progress, prioritizing"
  - label: "Launched (need to iterate)"
    description: "Live product, improving based on feedback"
```

**Routing:**
- "Idea" → mvp-scoping, user-story-mapping
- "MVP defined" → roadmap-design, backlog-creation
- "Building" → `Skill(faion-product-operations)` → prioritization, grooming
- "Launched" → feedback-management, product-analytics

#### Q2: Planning Need (if Idea or MVP stage)

```yaml
question: "What planning help do you need?"
header: "Planning"
multiSelect: true
options:
  - label: "Define what to build (MVP scope)"
    description: "Features, user stories, acceptance criteria"
  - label: "Create a roadmap"
    description: "Phases, milestones, feature sequence"
  - label: "Set goals and metrics (OKRs)"
    description: "Success criteria, KPIs"
  - label: "Plan a launch"
    description: "Launch checklist, GTM coordination"
```

**Routing:**
- "MVP scope" → `Skill(faion-product-planning)` → mvp-scoping
- "Roadmap" → `Skill(faion-product-planning)` → roadmap-design
- "OKRs" → `Skill(faion-product-planning)` → okr-setting
- "Launch" → `Skill(faion-product-planning)` → launch-planning + coordinate with marketing

#### Q3: Operations Need (if Building or Launched)

```yaml
question: "What operations help do you need?"
header: "Operations"
multiSelect: true
options:
  - label: "Prioritize features (what's next?)"
    description: "RICE, MoSCoW, impact vs effort"
  - label: "Manage backlog"
    description: "Groom, refine, organize"
  - label: "Track metrics and analytics"
    description: "Understand user behavior"
  - label: "Process user feedback"
    description: "Collect and act on feedback"
```

**Routing:**
- "Prioritize" → `Skill(faion-product-operations)` → prioritization-rice/moscow
- "Backlog" → `Skill(faion-product-operations)` → backlog-management
- "Metrics" → `Skill(faion-product-operations)` → product-analytics
- "Feedback" → `Skill(faion-product-operations)` → feedback-management

#### Q4: Decision Framework Preference

```yaml
question: "How do you prefer to make product decisions?"
header: "Framework"
multiSelect: false
options:
  - label: "Data-driven (metrics, analytics)"
    description: "Decisions backed by numbers"
  - label: "User-centric (feedback, interviews)"
    description: "Decisions based on user input"
  - label: "Intuition + validation"
    description: "Hypothesize then test"
  - label: "Stakeholder consensus"
    description: "Align with team/investors"
```

**Context impact:**
- "Data-driven" → Emphasize metrics, A/B testing, analytics
- "User-centric" → Emphasize user research, feedback loops
- "Intuition" → Faster decisions, MVP experiments, iterate
- "Stakeholder" → Prioritization frameworks, alignment docs

---

## Sub-Skills

| Sub-Skill | Focus | Methodologies |
|-----------|-------|---------------|
| [faion-product-manager:planning](../faion-product-manager:planning/SKILL.md) | MVP/MLP, roadmaps, discovery, launch | 17 |
| [faion-product-manager:operations](../faion-product-manager:operations/SKILL.md) | Prioritization, backlog, analytics, lifecycle | 16 |

**Total:** 33 methodologies | 2 agents

---

## Decision Tree

### Planning Activities
Use [faion-product-manager:planning](../faion-product-manager:planning/SKILL.md):
- Define MVP/MLP scope
- Create roadmaps (Now-Next-Later, outcome-based)
- User story mapping
- Product discovery and validation
- Launch planning
- OKR setting

### Operations Activities
Use [faion-product-manager:operations](../faion-product-manager:operations/SKILL.md):
- Feature prioritization (RICE, MoSCoW)
- Backlog management and grooming
- Product analytics and metrics
- Feedback management
- Technical debt tracking
- Stakeholder management

---

## Quick Reference

| Resource | Location | Content |
|----------|----------|---------|
| **Workflows** | [workflows.md](workflows.md) | Bootstrap, MLP transformation flows |
| **Agents** | [agents.md](agents.md) | MVP analyzer, MLP orchestrator |
| **Methodologies** | [methodologies-summary.md](methodologies-summary.md) | Full 33-methodology catalog |

---

## Common Workflows

**New Product:**
```
mvp-scoping → feature-prioritization-rice → user-story-mapping → roadmap-design → product-launch
```

**Quarterly Planning:**
```
okr-setting → backlog-management → feature-prioritization-rice → release-planning
```

**Discovery Sprint:**
```
product-discovery → continuous-discovery → feedback-management → backlog-management
```

---

## Agents

| Agent | Purpose | Location |
|-------|---------|----------|
| faion-mvp-scope-analyzer-agent | MVP scope via competitor analysis | [agents.md](agents.md) |
| faion-mlp-agent | MLP orchestrator (5 modes) | [agents.md](agents.md) |

---

## Cross-Skill Routing

| Need | Route To |
|------|----------|
| Market research, competitors | [faion-researcher](../faion-researcher/SKILL.md) |
| Technical architecture | [faion-software-architect](../faion-software-architect/SKILL.md) |
| Specs to implementation | [faion-sdd](../faion-sdd/SKILL.md) |
| Execution tracking | [faion-project-manager](../faion-project-manager/SKILL.md) |
| Requirements analysis | [faion-business-analyst](../faion-business-analyst/SKILL.md) |

---

*Product Manager Orchestrator v2.0*
*33 Methodologies | 2 Sub-Skills | 2 Agents*
