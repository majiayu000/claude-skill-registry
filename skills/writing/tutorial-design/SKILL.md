---
name: tutorial-design
description: >-
  Design and write hands-on tutorials with progressive disclosure, exercises,
  and troubleshooting sections. Use when creating learning content, workshops,
  or step-by-step guides.
version: 1.0.0
tags: [tutorials, pedagogy, learning, workshops, documentation]
triggers:
  - write tutorial
  - create workshop
  - step-by-step guide
  - hands-on walkthrough
  - learning content
  - lab exercise
dependencies:
  skills: [documentation-production, code-explanation]
  tools: [Read, Write]
token_estimate: ~2500
---

# Tutorial Design

Design and write hands-on tutorials that transform complex technical concepts into engaging,
progressive learning experiences with exercises, checkpoints, and troubleshooting guidance.

## When to Use This Skill

- Writing a getting-started tutorial for a library, API, or tool
- Creating workshop materials for team training or conferences
- Building multi-part learning series with progressive difficulty
- Designing coding exercises with self-assessment checkpoints
- Converting existing documentation into guided learning content
- Creating quick-start guides that get users productive fast

## Quick Reference

| Resource | Purpose | Load when |
|----------|---------|-----------|
| `references/design-patterns.md` | Progressive disclosure patterns, exercise types, checkpoint design, difficulty calibration, prerequisite mapping | Planning tutorial structure or designing exercises |

---

## Workflow Overview

```
Phase 1: Objectives   → Define learning outcomes, prerequisites, and audience
Phase 2: Decompose    → Break concepts into atomic, sequenced steps
Phase 3: Design       → Create exercises, checkpoints, and troubleshooting tips
Phase 4: Write        → Produce tutorial content with runnable examples
Phase 5: Validate     → Test the tutorial path end-to-end
```

---

## Phase 1: Define Learning Objectives

Every tutorial starts with clear outcomes.

### Opening Section Template

```markdown
## What You'll Learn

- [Specific, measurable outcome 1]
- [Specific, measurable outcome 2]
- [Specific, measurable outcome 3]

## Prerequisites

- [Required knowledge or setup]
- [Tools needed]

## Time Estimate

~[X] minutes

## What You'll Build

[Brief description or screenshot of the final result]
```

**Writing good objectives:**
- Use action verbs: "build", "configure", "debug", "deploy" — not "understand" or "learn about"
- Make them testable: the reader should be able to verify they achieved each outcome
- Scope realistically: 3-5 objectives per tutorial

---

## Phase 2: Concept Decomposition

Break the topic into atomic learning steps.

### Sequencing Rules

1. **One concept per section** — never introduce two new ideas at once
2. **Dependency order** — concepts must build on what came before
3. **Concrete before abstract** — show the working example, then explain the theory
4. **Simple before complex** — start with the minimal version, layer complexity

### Concept Map

Before writing, sketch a dependency graph:

```
[Prerequisites] → [Core concept A] → [Core concept B]
                                    ↘ [Variation 1]
                  [Core concept A] → [Core concept C] → [Advanced topic]
```

Each node becomes a section. Dependencies become the section order.

---

## Phase 3: Design Exercises and Checkpoints

### Exercise Types

| Type | Difficulty | When to use |
|------|-----------|-------------|
| **Fill-in-the-blank** | Low | Reinforce syntax after an example |
| **Debug challenge** | Medium | Teach error reading and common mistakes |
| **Extension task** | Medium | Add a feature to working code |
| **From scratch** | High | Build based on requirements only |
| **Refactoring** | High | Improve existing implementation |

### Checkpoint Pattern

After every major section, insert a checkpoint:

```markdown
### Checkpoint

At this point you should have:
- [ ] A running server on port 3000
- [ ] The `/health` endpoint returning `{ "status": "ok" }`
- [ ] Server logs showing incoming requests

**If something's wrong**, see the [Troubleshooting](#troubleshooting) section below.
```

### Troubleshooting Sections

For every section, anticipate 2-3 common errors:

```markdown
### Troubleshooting

**Error: `EADDRINUSE: address already in use`**
Another process is using port 3000. Run `lsof -i :3000` to find it,
then stop it or change your port.

**Error: `Cannot find module 'express'`**
You haven't installed dependencies yet. Run `npm install` in the project root.
```

---

## Phase 4: Write the Tutorial

### Section Structure (for each concept)

1. **Brief intro** (1-2 sentences) — what this section covers and why it matters
2. **Minimal example** — complete, runnable code showing the concept
3. **Line-by-line explanation** — walk through the important parts
4. **Try it** — tell the reader to run the code and what to expect
5. **Extend it** — optional exercise to deepen understanding
6. **Troubleshooting** — common errors for this section

### Writing Principles

- **Show, then explain** — code first, theory second
- **Frequent validation** — readers should run code every 2-3 minutes
- **Fail forward** — include intentional errors to teach debugging
- **Incremental complexity** — each step adds one thing to the previous
- **Copy-paste friendly** — examples must work when pasted directly

### Content Elements

**Code blocks must:**
- Be complete and runnable (no `...` elisions in critical paths)
- Include expected output in a separate block
- Use meaningful variable names
- Have inline comments only where non-obvious

**Explanations should:**
- Connect to real-world use cases
- Provide the "why" behind each step
- Use analogies to familiar concepts
- Anticipate the reader's "but what about...?" questions

### Closing Section

```markdown
## Summary

You've learned how to:
- [Outcome 1 restated]
- [Outcome 2 restated]

## Next Steps

- [Natural follow-on tutorial or topic]
- [Related documentation]
- [Community resources]
```

---

## Phase 5: Validate

Before publishing, test the entire tutorial path:

1. Follow every step from a clean environment
2. Run every code example and verify output matches
3. Trigger every troubleshooting scenario at least once
4. Time the tutorial — does it match the estimate?
5. Have someone unfamiliar with the topic attempt it

---

## Tutorial Formats

| Format | Duration | When to use |
|--------|----------|-------------|
| **Quick Start** | 5 min | First contact, get running fast |
| **Deep Dive** | 30-60 min | Comprehensive single-topic exploration |
| **Workshop Series** | Multi-part | Progressive learning across sessions |
| **Cookbook** | Variable | Problem-solution pairs, non-linear reading |
| **Interactive Lab** | 15-45 min | Hands-on environment with guided steps |

## Anti-Patterns

- Introducing concepts before they are needed ("you'll use this later")
- Showing code snippets that cannot run standalone
- Assuming knowledge not listed in prerequisites
- Walls of text without code breaks
- Exercises without solutions (even collapsed/hidden ones)
- Skipping the "why" and only showing the "how"
