---
version: 4.1.0-fractal
name: c4-architecture-c4-architecture
description: "Generate comprehensive C4 architecture documentation for an existing repository/codebase using a bottom-up analysis approach."
---

# C4 Architecture Documentation Workflow

Generate comprehensive C4 architecture documentation for an existing repository/codebase using a bottom-up analysis approach.

[Extended thinking: This workflow implements a complete C4 architecture documentation process following the C4 model (Context, Container, Component, Code). It uses a bottom-up approach, starting from the deepest code directories and working upward, ensuring every code element is documented before synthesizing into higher-level abstractions. The workflow coordinates four specialized C4 agents (Code, Component, Container, Context) to create a complete architectural documentation set that serves both technical and non-technical stakeholders.]

## Use this skill when

- Working on c4 architecture documentation workflow tasks or workflows
- Needing guidance, best practices, or checklists for c4 architecture documentation workflow

## Do not use this skill when

- The task is unrelated to c4 architecture documentation workflow
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Overview

This workflow creates comprehensive C4 architecture documentation following the [official C4 model](https://c4model.com/diagrams) by:

1. **Code Level**: Analyzing every subdirectory bottom-up to create code-level documentation
2. **Component Level**: Synthesizing code documentation into logical components within containers
3. **Container Level**: Mapping components to deployment containers with API documentation (shows high-level technology choices)
4. **Context Level**: Creating high-level system context with personas and user journeys (focuses on people and software systems, not technologies)

**Note**: According to the [C4 model](https://c4model.com/diagrams), you don't need to use all 4 levels of diagram - the system context and container diagrams are sufficient for most software development teams. This workflow generates all levels for completeness, but teams can choose which levels to use.

All documentation is written to a new `C4-Documentation/` directory in the repository root.

## Phase 1: Code-Level Documentation (Bottom-Up Analysis)

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [1.1 Discover All Subdirectories](./sub-skills/11-discover-all-subdirectories.md)
### 2. [1.2 Process Each Directory (Bottom-Up)](./sub-skills/12-process-each-directory-bottom-up.md)
### 3. [2.1 Analyze All Code-Level Documentation](./sub-skills/21-analyze-all-code-level-documentation.md)
### 4. [2.2 Create Component Documentation](./sub-skills/22-create-component-documentation.md)
### 5. [2.3 Create Master Component Index](./sub-skills/23-create-master-component-index.md)
### 6. [3.1 Analyze Components and Deployment Definitions](./sub-skills/31-analyze-components-and-deployment-definitions.md)
### 7. [3.2 Map Components to Containers](./sub-skills/32-map-components-to-containers.md)
### 8. [4.1 Analyze System Documentation](./sub-skills/41-analyze-system-documentation.md)
### 9. [4.2 Create Context Documentation](./sub-skills/42-create-context-documentation.md)
