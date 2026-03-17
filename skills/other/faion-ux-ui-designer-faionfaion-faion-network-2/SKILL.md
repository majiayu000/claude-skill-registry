---
name: faion-ux-ui-designer
description: "UX/UI orchestrator: user research, UI design, accessibility."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# UX/UI Designer Orchestrator

**Communication:** User's language | **Docs/code:** English

## Purpose

Orchestrates UX/UI design activities by coordinating specialized sub-skills. Routes tasks to appropriate specialists for research, design, or accessibility work.

**Philosophy:** "Design is not just what it looks like. Design is how it works." — Steve Jobs

---

## Context Discovery

### Auto-Investigation

Check for existing design artifacts and UI setup:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| Figma links | `Grep("figma.com", "**/*.md")` | Design files exist |
| Storybook | `Glob("**/.storybook/*")` | Component library exists |
| Design tokens | `Glob("**/tokens.*")` | Design system exists |
| Tailwind config | `Glob("**/tailwind.config.*")` | Tailwind used |
| a11y config | `Grep("eslint-plugin-jsx-a11y", "**/package.json")` | A11y linting enabled |
| User personas | `Glob("**/personas*.md")` | User research done |

**Read existing assets:**
- Check existing components for design patterns
- Read Storybook stories for component API
- Review tailwind.config for design tokens

### Discovery Questions

Use `AskUserQuestion` to understand UX/UI needs.

#### Q1: Design Phase

```yaml
question: "What phase of design work are you in?"
header: "Phase"
multiSelect: false
options:
  - label: "Research (understand users)"
    description: "User interviews, testing, personas"
  - label: "Design (create solutions)"
    description: "Wireframes, prototypes, visual design"
  - label: "Evaluate (test designs)"
    description: "Usability testing, heuristic evaluation"
  - label: "Accessibility audit"
    description: "WCAG compliance, a11y improvements"
```

**Routing:**
- "Research" → `Skill(faion-ux-researcher)`
- "Design" → `Skill(faion-ui-designer)`
- "Evaluate" → `Skill(faion-ux-researcher)` → usability-testing
- "Accessibility" → `Skill(faion-accessibility-specialist)`

#### Q2: Design Fidelity (if Design phase)

```yaml
question: "What fidelity of design do you need?"
header: "Fidelity"
multiSelect: false
options:
  - label: "Low-fi (wireframes, structure)"
    description: "Layout and flow, not visuals"
  - label: "High-fi (visual design)"
    description: "Colors, typography, polished UI"
  - label: "Design system / components"
    description: "Reusable component library"
  - label: "Code implementation"
    description: "Turn designs into working UI"
```

**Routing:**
- "Low-fi" → wireframing, information-architecture
- "High-fi" → visual-design, prototyping
- "Design system" → design-tokens, component-library
- "Code" → Coordinate with `Skill(faion-frontend-developer)`

#### Q3: User Access (if Research phase)

```yaml
question: "Do you have access to real users?"
header: "Users"
multiSelect: false
options:
  - label: "Yes, can recruit users easily"
    description: "Have user base or recruitment budget"
  - label: "Limited (internal team, friends)"
    description: "Can do guerrilla testing"
  - label: "No user access"
    description: "Need proxy methods"
```

**Context impact:**
- "Easy access" → Full user interviews, usability testing
- "Limited" → Guerrilla testing, shorter sessions
- "No access" → Heuristic evaluation, competitor analysis, personas from research

#### Q4: Platform (affects design patterns)

```yaml
question: "What platform are you designing for?"
header: "Platform"
multiSelect: true
options:
  - label: "Web (desktop)"
    description: "Desktop browser experience"
  - label: "Web (mobile responsive)"
    description: "Mobile-first or responsive"
  - label: "Native mobile app"
    description: "iOS or Android native"
  - label: "Voice UI"
    description: "Voice assistants, conversational"
```

**Context impact:**
- "Desktop" → Standard web patterns, larger screens
- "Mobile responsive" → Mobile-first, touch targets, responsive
- "Native mobile" → Platform guidelines (HIG, Material)
- "Voice UI" → VUI methodologies, conversation design

---

## Architecture

```
faion-ux-ui-designer (orchestrator)
├── faion-ux-researcher (30 methodologies)
│   └── Research, testing, personas, journey mapping
├── faion-ui-designer (30 methodologies)
│   └── Wireframes, prototypes, design systems, VUI, spatial
└── faion-accessibility-specialist (22 methodologies)
    └── WCAG, ADA, a11y testing, heuristics
```

**Total:** 82 methodologies

---

## Sub-Skills

| Sub-Skill | Focus | Methodologies | Location |
|-----------|-------|---------------|----------|
| **faion-ux-researcher** | User research, testing, analysis | 30 | [~/.claude/skills/faion-ux-researcher](../faion-ux-researcher/SKILL.md) |
| **faion-ui-designer** | Wireframes, prototypes, design systems, VUI, spatial | 30 | [~/.claude/skills/faion-ui-designer](../faion-ui-designer/SKILL.md) |
| **faion-accessibility-specialist** | WCAG, ADA, a11y testing, heuristics | 22 | [~/.claude/skills/faion-accessibility-specialist](../faion-accessibility-specialist/SKILL.md) |

---

## Quick Decision Guide

| If you need... | Route to | Examples |
|----------------|----------|----------|
| **Research & Understanding** | faion-ux-researcher | User interviews, surveys, usability testing, personas, journey maps, competitive analysis |
| **Design Solutions** | faion-ui-designer | Wireframes, prototypes, design systems, design tokens, VUI, spatial UI, Figma/Adobe |
| **Accessibility & Compliance** | faion-accessibility-specialist | WCAG 2.2, ADA, a11y testing, heuristic evaluation, assistive tech |
| **Multi-domain tasks** | Multiple sub-skills | Discovery (research → design), validation (design → a11y), full cycle (research → design → a11y) |

---

## Common Workflows

### Discovery Phase
```
1. faion-ux-researcher: User interviews
2. faion-ux-researcher: Competitive analysis
3. faion-ux-researcher: Personas
4. faion-ux-researcher: Journey mapping
```

### Design Phase
```
1. faion-ui-designer: Wireframing
2. faion-ui-designer: Prototyping
3. faion-ui-designer: Design systems (if needed)
```

### Validation Phase
```
1. faion-accessibility-specialist: Heuristic evaluation
2. faion-ux-researcher: Usability testing
3. faion-accessibility-specialist: WCAG audit
```

### Full Cycle
```
1. faion-ux-researcher: Discovery
2. faion-ui-designer: Design
3. faion-accessibility-specialist: A11y validation
4. faion-ux-researcher: User testing
5. Iterate
```

---

## Execution Protocol

### Task Analysis
1. Identify task domain (research, design, or a11y)
2. Determine if single or multi-domain task
3. Route to appropriate sub-skill(s)

### Single-Domain Tasks
```
Task → Identify domain → Invoke sub-skill → Return results
```

### Multi-Domain Tasks
```
Task → Break into phases → Invoke sub-skills sequentially → Synthesize results
```

### Coordination
- Pass research findings from ux-researcher to ui-designer
- Send designs from ui-designer to accessibility-specialist for validation
- Loop back to ux-researcher for user testing validation
- Maintain consistent artifacts across sub-skills

---

## Integration Points

| External Skill | Collaboration |
|----------------|---------------|
| faion-product-manager | Receives product requirements, provides research insights |
| faion-software-developer | Provides design specs, receives implementation questions |
| faion-marketing-manager | Collaborates on landing pages, conversion optimization |
| faion-researcher | Shares market research, personas, competitor insights |

---

## Output Formats

Orchestrator outputs depend on sub-skills invoked:

### From faion-ux-researcher
- Research reports
- Personas
- Journey maps
- Usability test results
- Competitive analysis matrices

### From faion-ui-designer
- Wireframes and prototypes
- Design system documentation
- Design tokens (JSON/YAML)
- VUI conversation flows
- Spatial UI mockups

### From faion-accessibility-specialist
- WCAG audit reports
- ADA compliance documentation
- Heuristic evaluation reports
- Assistive technology test results
- VPAT documents

---

## Navigation

For detailed methodologies, see sub-skill documentation:

- **[faion-ux-researcher SKILL.md](../faion-ux-researcher/SKILL.md)** - Research methodologies
- **[faion-ui-designer SKILL.md](../faion-ui-designer/SKILL.md)** - Design methodologies
- **[faion-accessibility-specialist SKILL.md](../faion-accessibility-specialist/SKILL.md)** - Accessibility methodologies

---

## Sources

- [Nielsen Norman Group](https://www.nngroup.com/) - 10 Usability Heuristics
- [IDEO Design Kit](https://www.designkit.org/) - Human-Centered Design
- [WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/) - Accessibility
- [Material Design](https://m3.material.io/) - Google Design System
- [Human Interface Guidelines](https://developer.apple.com/design/) - Apple Design

---

*UX/UI Designer Orchestrator v3.0*
*82 Methodologies | 3 Sub-Skills | Specialized Routing*
