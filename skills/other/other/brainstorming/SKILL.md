---
name: brainstorming
description: "Use when the user asks to design, plan, or explore approaches before implementing — creating features, building components, or adding functionality that would benefit from design exploration first."
---

# Brainstorming Ideas Into Designs

Help turn ideas into fully formed designs through collaborative dialogue.

When this skill activates, present a design before writing code. The design can be short (a few sentences for simple projects) — scale it to the complexity of the task. Get the user's approval before proceeding to implementation.

## Process

1. **Explore context** — check files, docs, recent commits
2. **Ask clarifying questions** — one at a time, prefer multiple choice, understand purpose/constraints/success criteria
3. **Propose 2-3 approaches** — with trade-offs and your recommendation
4. **Present design** — scale each section to its complexity, ask after each section if it looks right
5. **Write spec** — save to `docs/specs/` (create directory if needed) and commit
6. **User reviews spec** — wait for approval before proceeding
7. **Transition** — invoke writing-plans skill to create implementation plan

## Design Principles

- **One question at a time** — don't overwhelm with multiple questions
- **YAGNI ruthlessly** — remove unnecessary features
- **Design for isolation** — break into units with one clear purpose, well-defined interfaces, testable independently
- **Explore alternatives** — always propose 2-3 approaches before settling
- **Scope check** — if the request describes multiple independent subsystems, decompose into sub-projects first

## Working in Existing Codebases

- Explore the current structure before proposing changes. Follow existing patterns.
- Where existing code has problems that affect the work, include targeted improvements as part of the design.
- Don't propose unrelated refactoring. Stay focused on what serves the current goal.

## After Design Approval

Invoke the writing-plans skill to create a detailed implementation plan. Do NOT invoke any other skill — writing-plans is the next step.
