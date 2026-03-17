---
name: faion-researcher
description: "Research: idea generation, market research, competitors, personas, pricing, validation."
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Task, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Research Domain Skill

**Communication: User's language. Docs: English.**

## Purpose

Orchestrate all research and discovery activities for product/startup development. Coordinates 2 specialized sub-skills for comprehensive research coverage.

---

## Context Discovery

### Auto-Investigation

Check for existing research and product context:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| `.aidocs/product_docs/` | `Glob("**/.aidocs/product_docs/*")` | Product docs exist |
| `market-research.md` | `Glob("**/market-research.md")` | Market research done |
| `competitive-analysis.md` | `Glob("**/competitive-analysis.md")` | Competitors analyzed |
| `user-personas.md` | `Glob("**/user-personas.md")` | Personas defined |
| `constitution.md` | `Glob("**/.aidocs/constitution.md")` | Product defined |
| Landing page | `Glob("**/pages/index.*")` | Positioning visible |

**Read existing assets:**
- Check landing page for current positioning/messaging
- Read constitution.md for product context
- Check any existing research docs

### Discovery Questions

Use `AskUserQuestion` to understand research needs.

#### Q1: Research Stage

```yaml
question: "What stage of research are you in?"
header: "Stage"
multiSelect: false
options:
  - label: "Exploring ideas (no specific direction)"
    description: "Generate and evaluate new ideas"
  - label: "Have an idea, need validation"
    description: "Test if idea is worth pursuing"
  - label: "Committed, need market intelligence"
    description: "Understand market, competitors, pricing"
  - label: "Building, need user insights"
    description: "Understand users for better product"
```

**Routing:**
- "Exploring ideas" → `Skill(faion-market-researcher)` → idea-generation
- "Need validation" → `Skill(faion-user-researcher)` → problem-validation
- "Market intelligence" → `Skill(faion-market-researcher)` → competitors, TAM, pricing
- "User insights" → `Skill(faion-user-researcher)` → personas, JTBD, pain points

#### Q2: Research Focus (if market intelligence)

```yaml
question: "What do you need to understand?"
header: "Focus"
multiSelect: true
options:
  - label: "Market size (TAM/SAM/SOM)"
    description: "How big is the opportunity?"
  - label: "Competitors & alternatives"
    description: "Who else solves this problem?"
  - label: "Pricing benchmarks"
    description: "What do customers pay for similar?"
  - label: "Industry trends"
    description: "Where is the market heading?"
```

**Routing:**
- "Market size" → tam-sam-som-analysis
- "Competitors" → competitor-analysis
- "Pricing" → pricing-research
- "Trends" → trend-analysis

#### Q3: User Research Type (if user insights)

```yaml
question: "What user insights do you need?"
header: "Insights"
multiSelect: true
options:
  - label: "Who are my users? (personas)"
    description: "User profiles and segments"
  - label: "What problems do they have?"
    description: "Pain points and frustrations"
  - label: "What are they trying to achieve?"
    description: "Jobs-to-be-done, goals"
  - label: "Would they pay for a solution?"
    description: "Willingness to pay, value perception"
```

**Routing:**
- "Personas" → persona-building
- "Problems" → pain-point-research
- "Achieve" → jobs-to-be-done
- "Pay" → value-proposition + pricing-research

#### Q4: Evidence Standards

```yaml
question: "What would convince you the research is solid?"
header: "Evidence"
multiSelect: false
options:
  - label: "Quick directional insights"
    description: "Enough to make a decision, move fast"
  - label: "Backed by data sources"
    description: "Links to research, reports, data"
  - label: "Primary research (interviews/surveys)"
    description: "Talk to real users/customers"
```

**Context impact:**
- "Quick" → Web search, secondary research, fast output
- "Backed by data" → Include sources, citations, methodology
- "Primary research" → Interview guides, survey design, synthesis

---

## Architecture

```
faion-researcher (orchestrator)
├── faion-market-researcher (22 methodologies)
│   ├── Market sizing (TAM/SAM/SOM)
│   ├── Competitor analysis
│   ├── Pricing research
│   ├── Trend analysis
│   ├── Niche evaluation
│   ├── Business model planning
│   └── Idea generation
└── faion-user-researcher (21 methodologies)
    ├── Persona building
    ├── User interviews
    ├── Pain point research
    ├── Jobs-to-be-done
    ├── Problem validation
    ├── Value proposition design
    └── Survey design
```

**Total:** 43 methodologies across 2 sub-skills

---

## Quick Decision Tree

| If you need... | Route to Sub-Skill |
|---------------|-------------------|
| **Market Intelligence** | |
| Market size (TAM/SAM/SOM) | faion-market-researcher |
| Competitors & gaps | faion-market-researcher |
| Pricing benchmarks | faion-market-researcher |
| Market trends | faion-market-researcher |
| Niche evaluation | faion-market-researcher |
| Business models | faion-market-researcher |
| Generate ideas | faion-market-researcher |
| **User Understanding** | |
| User profiles | faion-user-researcher |
| Pain points | faion-user-researcher |
| User motivations (JTBD) | faion-user-researcher |
| Value proposition | faion-user-researcher |
| Interview questions | faion-user-researcher |
| Problem validation | faion-user-researcher |
| Survey design | faion-user-researcher |
| **Full Research** | |
| Complete product research | Both (sequential) |

---

## Sub-Skills (2)

### faion-market-researcher

**Focus:** Market & business intelligence

| Capability | Methodologies |
|------------|---------------|
| Market Analysis | TAM/SAM/SOM, market sizing, trends |
| Competitive Intel | Competitor analysis, competitive intelligence |
| Business Planning | Models, niche eval, risk, distribution |
| Pricing | Research, benchmarking |
| Ideas | Generation, frameworks |

**Files:** 22 | **Location:** [faion-market-researcher/](../faion-market-researcher/)

### faion-user-researcher

**Focus:** User research & validation

| Capability | Methodologies |
|------------|---------------|
| Personas | Building, segmentation, AI-assisted |
| Interviews | Methods, analysis, at-scale |
| Pain Points | Research, validation |
| JTBD | Framework, motivations |
| Validation | Methods, problem-solution fit |
| Value Prop | Design, canvas |

**Files:** 21 | **Location:** [faion-user-researcher/](../faion-user-researcher/)

---

## Agents (2)

| Agent | Model | Purpose | Modes |
|-------|-------|---------|-------|
| faion-research-agent | opus | Research orchestrator | ideas, market, competitors, pains, personas, validate, niche, pricing, names |
| faion-domain-checker-agent | sonnet | Domain availability verification | - |

**Details:** [agent-invocation.md](agent-invocation.md)

---

## Research Modes (9)

| Mode | Output | Sub-Skill Used |
|------|--------|----------------|
| ideas | idea-candidates.md | market-researcher |
| market | market-research.md | market-researcher |
| competitors | competitive-analysis.md | market-researcher |
| pricing | pricing-research.md | market-researcher |
| niche | niche-evaluation.md | market-researcher |
| personas | user-personas.md | user-researcher |
| pains | pain-points.md | user-researcher |
| validate | problem-validation.md | user-researcher |
| names | name-candidates.md | market-researcher |

---

## Core Workflows

### 1. Idea Discovery
```
Context → Generate Ideas → Select → Pain Research → Niche Eval → Results
Sub-skills: market-researcher (ideas, niche) + user-researcher (pains)
```

### 2. Product Research
```
Parse Project → Read Docs → Select Modules → Sequential Execution → Summary
Sub-skills: market-researcher (market, competitors, pricing) + user-researcher (personas, validate)
```

### 3. Project Naming
```
Gather Concept → Generate Names → Select → Check Domains → Results
Sub-skill: market-researcher (naming)
```

**Details:** [workflows.md](workflows.md)

---

## Quick Reference

| Topic | File | Description |
|-------|------|-------------|
| **Navigation** | [CLAUDE.md](CLAUDE.md) | Entry point, when to use |
| **Agents** | [agent-invocation.md](agent-invocation.md) | Agent syntax, modes |
| **Workflows** | [workflows.md](workflows.md) | Research workflows |
| **Frameworks** | [frameworks.md](frameworks.md) | 7 Ps, JTBD, TAM/SAM/SOM |
| **Methodologies** | [methodologies-index.md](methodologies-index.md) | Full index |

---

## Output Files

All outputs go to `.aidocs/product_docs/`:

| Module | Output File | Sub-Skill |
|--------|-------------|-----------|
| Idea Discovery | idea-validation.md | market-researcher |
| Market Research | market-research.md | market-researcher |
| Competitors | competitive-analysis.md | market-researcher |
| Pricing | pricing-research.md | market-researcher |
| Niche | niche-evaluation.md | market-researcher |
| Personas | user-personas.md | user-researcher |
| Pain Points | pain-points.md | user-researcher |
| Validation | problem-validation.md | user-researcher |
| Summary | executive-summary.md | Both |

---

## Integration

### Entry Point
Invoked via `/faion-net` when intent is research-related:
```
if intent in ["idea", "research", "market", "competitors", "naming", "personas", "pricing"]:
    invoke("faion-researcher")
```

### Sub-Skill Invocation
```
# Market intelligence
invoke("faion-market-researcher", mode="market")

# User research
invoke("faion-user-researcher", mode="personas")

# Full research (sequential)
invoke("faion-market-researcher", mode="market")
invoke("faion-market-researcher", mode="competitors")
invoke("faion-user-researcher", mode="personas")
invoke("faion-user-researcher", mode="validate")
```

### Next Steps
After research complete, offer:
- "Create GTM Manifest?" → `faion-marketing-manager`
- "Create spec.md?" → `faion-sdd`
- "Start development?" → `faion-software-developer`

---

## Rules

1. **Sequential execution** - Run agents ONE BY ONE (not parallel)
2. **Sub-skill routing** - Market topics → market-researcher, User topics → user-researcher
3. **Source citations** - All research must include URLs
4. **Data quality** - If not found → "Data not available"

---

*faion-researcher v2.0*
*Orchestrator with 2 sub-skills*
*Total: 43 methodologies | Agents: 2 | Modes: 9*
