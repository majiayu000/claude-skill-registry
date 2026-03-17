---
name: context-driven-development
description: Use this skill when working with Conductor's context-driven
  development methodology, managing project context artifacts, or understanding
  the relationship between product.md, tech-stack.md, and workflow.md files.
metadata:
  version: 4.1.0-fractal
---

# Context-Driven Development

Guide for implementing and maintaining context as a managed artifact alongside code, enabling consistent AI interactions and team alignment through structured project documentation.

## Do not use this skill when

- The task is unrelated to context-driven development
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Use this skill when

- Setting up new projects with Conductor
- Understanding the relationship between context artifacts
- Maintaining consistency across AI-assisted development sessions
- Onboarding team members to an existing Conductor project
- Deciding when to update context documents
- Managing greenfield vs brownfield project contexts

## Core Philosophy

Context-Driven Development treats project context as a first-class artifact managed alongside code. Instead of relying on ad-hoc prompts or scattered documentation, establish a persistent, structured foundation that informs all AI interactions.

Key principles:

1. **Context precedes code**: Define what you're building and how before implementation
2. **Living documentation**: Context artifacts evolve with the project
3. **Single source of truth**: One canonical location for each type of information
4. **AI alignment**: Consistent context produces consistent AI behavior

## The Workflow

Follow the **Context → Spec & Plan → Implement** workflow:

1. **Context Phase**: Establish or verify project context artifacts exist and are current
2. **Specification Phase**: Define requirements and acceptance criteria for work units
3. **Planning Phase**: Break specifications into phased, actionable tasks
4. **Implementation Phase**: Execute tasks following established workflow patterns

## Artifact Relationships

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [product.md - Defines WHAT and WHY](./sub-skills/productmd-defines-what-and-why.md)
### 2. [product-guidelines.md - Defines HOW to Communicate](./sub-skills/product-guidelinesmd-defines-how-to-communicate.md)
### 3. [tech-stack.md - Defines WITH WHAT](./sub-skills/tech-stackmd-defines-with-what.md)
### 4. [workflow.md - Defines HOW to Work](./sub-skills/workflowmd-defines-how-to-work.md)
### 5. [tracks.md - Tracks WHAT'S HAPPENING](./sub-skills/tracksmd-tracks-whats-happening.md)
### 6. [Keep Artifacts Synchronized](./sub-skills/keep-artifacts-synchronized.md)
### 7. [Update tech-stack.md When Adding Dependencies](./sub-skills/update-tech-stackmd-when-adding-dependencies.md)
### 8. [Update product.md When Features Complete](./sub-skills/update-productmd-when-features-complete.md)
### 9. [Verify Context Before Implementation](./sub-skills/verify-context-before-implementation.md)
### 10. [Greenfield Projects (New)](./sub-skills/greenfield-projects-new.md)
### 11. [Brownfield Projects (Existing)](./sub-skills/brownfield-projects-existing.md)
### 12. [Team Alignment](./sub-skills/team-alignment.md)
### 13. [AI Consistency](./sub-skills/ai-consistency.md)
### 14. [Institutional Memory](./sub-skills/institutional-memory.md)
### 15. [Quality Assurance](./sub-skills/quality-assurance.md)
### 16. [Product Context](./sub-skills/product-context.md)
### 17. [Technical Context](./sub-skills/technical-context.md)
### 18. [Workflow Context](./sub-skills/workflow-context.md)
### 19. [Track Context](./sub-skills/track-context.md)
### 20. [Stale Context](./sub-skills/stale-context.md)
### 21. [Context Sprawl](./sub-skills/context-sprawl.md)
### 22. [Implicit Context](./sub-skills/implicit-context.md)
### 23. [Context Hoarding](./sub-skills/context-hoarding.md)
### 24. [Over-Specification](./sub-skills/over-specification.md)
### 25. [IDE Integration](./sub-skills/ide-integration.md)
### 26. [Git Hooks](./sub-skills/git-hooks.md)
### 27. [CI/CD Integration](./sub-skills/cicd-integration.md)
### 28. [Starting a New Session](./sub-skills/starting-a-new-session.md)
### 29. [Ending a Session](./sub-skills/ending-a-session.md)
### 30. [Handling Interruptions](./sub-skills/handling-interruptions.md)
