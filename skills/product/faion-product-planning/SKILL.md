---
name: faion-product-planning
description: "Product planning: MVP/MLP scoping, roadmaps, user story mapping, OKRs."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Product Planning Sub-Skill

**Communication: User's language. Docs: English.**

## Purpose

Product planning from ideation to launch: MVP/MLP scoping, roadmaps, discovery, launch planning.

**Parent:** [faion-product-manager](../faion-product-manager/SKILL.md)

---

## Context Discovery

### Auto-Investigation

Detect existing product planning artifacts:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| Roadmap | `Glob("**/roadmap*.md")` or `Glob("**/.aidocs/roadmap.md")` | Roadmap exists |
| MVP/MLP docs | `Grep("MVP\\|MLP\\|MMP")` | Minimum product scope defined |
| User stories | `Glob("**/stories/*")` or `Grep("As a .* I want")` | User story mapping |
| OKRs | `Grep("OKR\\|Objective\\|Key Result")` | Goals framework in use |
| Product specs | `Glob("**/spec*.md")` or `Glob("**/.aidocs/*/spec.md")` | Product specifications |
| Launch plans | `Glob("**/launch*.md")` or `Grep("go-to-market")` | Launch planning |
| Discovery notes | `Glob("**/discovery/*")` or `Grep("Five Whys")` | Discovery process documented |
| Feature backlog | `Glob("**/.aidocs/backlog/feature-*")` | Feature queue |

**Read existing planning artifacts:**
- roadmap.md for product timeline
- Feature specs for scope
- OKRs or goals
- User story maps or epics

### Discovery Questions

#### Q1: Planning Stage

```yaml
question: "What planning stage are you at?"
header: "Stage"
multiSelect: false
options:
  - label: "Ideation (new product concept)"
    description: "Need discovery, MVP scoping, positioning"
  - label: "MVP definition (scope a first version)"
    description: "Define minimum features, validation experiments"
  - label: "Roadmap planning (prioritize features)"
    description: "Now-Next-Later roadmap, release planning"
  - label: "Launch preparation (GTM plan)"
    description: "Launch timeline, positioning, messaging"
```

#### Q2: Product Maturity

```yaml
question: "What's your product maturity?"
header: "Maturity"
multiSelect: false
options:
  - label: "Pre-MVP (idea stage)"
    description: "Need micro-MVPs, landing pages, validation"
  - label: "MVP in progress"
    description: "Building first version, iterating on scope"
  - label: "Post-MVP, scaling (MLP)"
    description: "MVP validated, adding lovability and features"
  - label: "Mature product (portfolio strategy)"
    description: "Multiple products, long-term roadmap"
```

#### Q3: Planning Framework

```yaml
question: "What planning framework do you prefer?"
header: "Framework"
multiSelect: false
options:
  - label: "Outcome-based roadmaps"
    description: "Focus on outcomes, not features or dates"
  - label: "Now-Next-Later (uncertain timeline)"
    description: "Flexible roadmap without specific dates"
  - label: "OKRs (objectives and key results)"
    description: "Goal-based planning with measurable KRs"
  - label: "User story mapping"
    description: "User journeys, activities, releases"
```

---

## Decision Tree

| If you need... | Use | File |
|----------------|-----|------|
| **Define MVP scope** | mvp-scoping | [mvp-scoping.md](mvp-scoping.md) |
| **Choose product framework** | minimum-product-frameworks | [minimum-product-frameworks.md](minimum-product-frameworks.md) |
| **Transform MVP to MLP** | mlp-planning | [mlp-planning.md](mlp-planning.md) |
| **Quick validation** | micro-mvps | [micro-mvps.md](micro-mvps.md) |
| **Roadmap (uncertain timeline)** | roadmap-design | [roadmap-design.md](roadmap-design.md) |
| **Roadmap (outcome-based)** | outcome-based-roadmaps | [outcome-based-roadmaps.md](outcome-based-roadmaps.md) |
| **User stories** | user-story-mapping | [user-story-mapping.md](user-story-mapping.md) |
| **Sprint planning** | release-planning | [release-planning.md](release-planning.md) |
| **Set goals** | okr-setting | [okr-setting.md](okr-setting.md) |
| **Launch planning** | product-launch | [product-launch.md](product-launch.md) |
| **Discovery process** | continuous-discovery | [continuous-discovery.md](continuous-discovery.md) |
| **Positioning** | competitive-positioning | [competitive-positioning.md](competitive-positioning.md) |
| **Portfolio management** | portfolio-strategy | [portfolio-strategy.md](portfolio-strategy.md) |
| **Write specs** | spec-writing | [spec-writing.md](spec-writing.md) |

---

## Core Methodologies (17)

### MVP & MLP
- **mvp-scoping** - Define core problem, minimum features, 4-week constraint
- **mlp-planning** - Transform MVP to Most Lovable Product
- **minimum-product-frameworks** - 9 frameworks (MVP/MLP/MMP/MAC/RAT/MDP/MVA/MFP/SLC)
- **micro-mvps** - Landing page, concierge, Wizard of Oz validation

### Planning & Roadmaps
- **roadmap-design** - Now-Next-Later roadmaps
- **outcome-based-roadmaps** - Outcome-focused planning
- **outcome-based-roadmaps-advanced** - Advanced outcome roadmapping
- **user-story-mapping** - Activities → Tasks → Releases
- **okr-setting** - Objectives + Key Results
- **release-planning** - Sprint goal, velocity, capacity
- **portfolio-strategy** - Multi-product portfolio management

### Discovery & Launch
- **product-discovery** - Five Whys to root cause
- **continuous-discovery** - Ongoing discovery habits
- **continuous-discovery-habits** - Weekly touchpoints framework
- **product-launch** - Launch timeline and execution
- **competitive-positioning** - Market positioning analysis
- **spec-writing** - Product specification authoring

---

## Common Sequences

- **New product:** mvp-scoping → user-story-mapping → roadmap-design → product-launch
- **Discovery sprint:** product-discovery → continuous-discovery → spec-writing
- **Planning cycle:** okr-setting → roadmap-design → release-planning

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [faion-product-manager](../faion-product-manager/SKILL.md) | Parent orchestrator |
| [faion-product-manager:operations](../faion-product-manager:operations/SKILL.md) | Sibling (prioritization, backlog) |
| [faion-researcher](../faion-researcher/SKILL.md) | Market data for planning |
| [faion-sdd](../faion-sdd/SKILL.md) | Specs to implementation |

---

*Product Planning Sub-Skill v1.0*
*17 Methodologies*
