---
name: "Learning Psychology Skill"
description: "Help humans learn through partnership, not instruction."
applyTo: "**/*learn*,**/*teach*,**/*tutor*,**/*explain*"
---

# Learning Psychology Skill

> Help humans learn through partnership, not instruction.

---

## Study Project Scaffolding

### Recommended Folder Structure

```text
study-project/
├── .github/
│   ├── copilot-instructions.md    # Learning context for Alex
│   └── prompts/
│       └── concept-review.prompt.md
├── courses/
│   ├── [course-name]/
│   │   ├── COURSE-OVERVIEW.md     # Syllabus, objectives
│   │   ├── notes/
│   │   │   ├── week-01.md
│   │   │   └── week-02.md
│   │   ├── assignments/
│   │   │   └── assignment-1.md
│   │   └── resources/
│   │       └── readings.md
├── concepts/
│   ├── CONCEPT-MAP.md             # How concepts connect
│   └── [concept-name].md          # Deep dives on key concepts
├── flashcards/
│   └── [topic]-cards.md           # Spaced repetition material
├── practice/
│   ├── problems/                  # Practice problems
│   └── solutions/                 # Worked solutions
├── projects/
│   └── [project-name]/            # Hands-on projects
└── README.md                      # Learning goals overview
```

### LEARNING-PLAN.md Template

```markdown
# Learning Plan: [Subject/Course]

## Goals
- **Primary**: [What you want to achieve]
- **Timeline**: [Duration]
- **Current Level**: [Beginner/Intermediate/Advanced]

## Learning Objectives
1. [ ] [Specific, measurable objective]
2. [ ] [Another objective]
3. [ ] [Another objective]

## Resources
| Resource | Type | Priority |
|----------|------|----------|
| [Book/Course] | [Primary/Supplementary] | [High/Medium/Low] |

## Schedule
| Week | Topic | Activities | Deliverable |
|------|-------|------------|-------------|
| 1 | [Topic] | [Reading, exercises] | [Notes, quiz] |

## Progress Tracking
- [ ] Week 1 complete
- [ ] Week 2 complete

## Review Schedule (Spaced Repetition)
| Concept | First Review | Second Review | Third Review |
|---------|--------------|---------------|--------------|
| [Concept] | Day 1 | Day 7 | Day 30 |
```

### CONCEPT-MAP.md Template

```markdown
# Concept Map: [Subject]

## Core Concepts

```text
                    [Central Concept]
                          │
            ┌─────────────┼─────────────┐
            │             │             │
      [Concept A]   [Concept B]   [Concept C]
            │             │
      [Sub-concept]  [Sub-concept]
```

## Concept Relationships

| Concept | Depends On | Enables |
|---------|------------|---------|
| [A] | [Prerequisites] | [What it unlocks] |

## Learning Sequence
1. Start with: [Foundation concepts]
2. Then learn: [Building blocks]
3. Finally: [Advanced topics]
```

### copilot-instructions.md Template (Study Projects)

```markdown
# [Subject] Study Project — Learning Context

## Overview
[What you're studying and why]

## Current Phase
- [ ] Foundation
- [ ] Core concepts
- [ ] Practice
- [ ] Mastery

## Alex Guidance
- **Learning style**: [Visual/Auditory/Kinesthetic/Reading-Writing]
- **Preferred explanation**: Start with examples, then theory
- Use analogies to connect new concepts to things I know
- Quiz me on concepts after explanations
- Suggest practice problems when I seem ready

## What I Know
[Background knowledge Alex can build on]

## What Confuses Me
[Concepts I struggle with — Alex should detect and address]

## Don't
- Don't give me the answer directly — help me discover it
- Don't overwhelm with theory before practical examples
- Don't assume I know prerequisite concepts
```

---

## Core Insight

Humans don't want to be taught—they want to learn through authentic conversation.

```text
Traditional:  Request → Tutorial → Lessons → Knowledge Transfer
Natural:      Greeting → Context → Dialog → Application → Partnership
```

## Natural Learning Flow

1. **Casual greeting** — Establish connection
2. **Context discovery** — Understand their situation
3. **Research + dialog** — Investigate while they provide requirements
4. **Practical application** — Solve real problems during learning
5. **Ongoing partnership** — Relationship-based knowledge building

## Critical Success Factors

| Factor | Implementation |
| ------ | -------------- |
| **Authenticity** | Real conversation, not scripted |
| **Adaptation** | Adjust to their constraints |
| **Problem-solving** | Learn while solving real issues |
| **Partnership** | Collaborative, not instructional |

## Anti-Patterns

- ❌ "Let me teach you about X"
- ❌ Starting with theory before understanding context
- ❌ Ignoring practical constraints
- ❌ One-way knowledge transfer

## Good Patterns

- ✅ "What are you trying to accomplish?"
- ✅ Discovering their specific situation first
- ✅ Adapting to their resources/limitations
- ✅ Solving their actual problem while explaining

## Zone of Proximal Development

Meet the learner where they are:

- **Too easy** → Boredom, disengagement
- **Too hard** → Frustration, giving up
- **Just right** → Flow, effective learning

Ask calibration questions to find the right level.

## Theoretical Foundations

Key sources:

- Vygotsky — Zone of Proximal Development, social learning
- Lave & Wenger — Situated learning, communities of practice
- Bandura — Social learning theory
- Brusilovsky — Adaptive learning systems

## Synapses

See [synapses.json](synapses.json) for connections.
