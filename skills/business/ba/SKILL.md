---
name: ba
description: Business analysis methodologies, requirements engineering, RACI matrices, user stories for Pulse Radar.
---

# Business Analysis Skill

## Project Context

**Pulse Radar** — AI-система збору знань з комунікаційних каналів.
- **Core Flow:** Telegram → Ingest → AI-extraction → Atom → Topic → Dashboard
- **Problem:** 100+ msg/day, 80% noise → structured knowledge
- **Status:** MVP Verified (13/33 features)

## Key Resources

```
docs/ba-course/          # BA methodology course (15 lessons)
├── 01-введение.md
├── 02-стейкхолдеры.md   # Stakeholder Analysis, RACI
├── 03-требования.md     # Requirements elicitation
├── 05-артефакты-ба-часть-1.md  # Vision & Scope, Glossary
├── 08-артефакты-ба-часть-2.md  # User Stories, Use Cases
└── 11-риски-и-изменения-требований.md  # Risk Management

docs/ba/                 # Product artifacts (build here)
├── 01-vision-scope.md
├── 02-glossary.md
└── 04-requirements/

.artifacts/ba-work/      # Work tracking
├── PROGRESS.md          # Artifact status
├── DECISIONS.md         # Product decisions
└── QUESTIONS.md         # Open questions
```

## Frameworks

### RACI Matrix
```
R - Responsible (does the work)
A - Accountable (final authority, ONE per activity)
C - Consulted (input before)
I - Informed (notified after)
```

### MoSCoW Prioritization
- **Must:** Critical for release
- **Should:** Important but not critical
- **Could:** Nice to have
- **Won't:** Explicitly out of scope

### INVEST User Stories
- **I**ndependent
- **N**egotiable
- **V**aluable
- **E**stimable
- **S**mall
- **T**estable

## Templates

### User Story
```markdown
## US-XXX: [Title]

**As a** [role]
**I want** [feature]
**So that** [benefit]

### Acceptance Criteria:
1. Given [context], When [action], Then [result]
```

### Use Case
```markdown
## UC-XXX: [Title]

**Actors:** [who]
**Preconditions:** [what must be true]
**Trigger:** [what starts it]

### Main Success Scenario:
1. [Step]

### Extensions:
- 2a. [Alternative]

**Postconditions:** [result]
```

### Risk Register
```markdown
| ID | Risk | Probability | Impact | Score | Mitigation |
|----|------|-------------|--------|-------|------------|
| R01 | [risk] | L/M/H | L/M/H | 1-9 | [action] |
```

## Domain Terms (Pulse Radar)

| Term | Definition |
|------|------------|
| Atom | Knowledge unit (TASK, IDEA, DECISION, PROBLEM, QUESTION, INSIGHT) |
| Signal | Message with importance_score > 0.65 |
| Noise | Message with importance_score < 0.25 |
| Topic | Container for organizing Atoms |
| Analysis Run | AI extraction execution (7 states) |

## Verification

Before completing analysis:
- [ ] All requirements testable
- [ ] Exactly one A per RACI row
- [ ] At least 3 risks identified
- [ ] Edge cases have recommendations
- [ ] Questions logged in QUESTIONS.md

## References
- @references/raci-examples.md — RACI matrix examples
- @references/edge-case-patterns.md — Common edge cases
- @references/stakeholder-templates.md — Stakeholder analysis templates