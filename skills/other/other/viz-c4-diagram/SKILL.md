---
version: 1.0.0
name: viz-c4-diagram
description: >
  Generate C4 architecture diagrams using Mermaid syntax. Use when the user says
  "draw a C4 diagram", "architecture diagram", "system context diagram", "container diagram",
  "component diagram", or "visualize the architecture".
disable-model-invocation: false
user-invocable: true
argument-hint: "[system name] [level: context|container|component|code|all]"
---

# Generate C4 Diagrams

## Path Resolution

1. Read `workflow.json` in the project root
2. If it exists and `docsRepo` is `"."`: this IS the docs repo — use local paths
3. If it exists and `docsRepo` is a repo name: resolve via `pwsh .claude/skills/tool-worktree/scripts/resolve-repo.ps1 <docsRepo>` to get the docs root path. Templates at `<resolved>/templates/`, output to `<resolved>/architecture/`
4. If no `workflow.json`: templates at `templates/`, output to `docs/architecture/`

## Instructions

1. **Resolve paths** (see Path Resolution above)
2. **Read the template** at `<templates>/c4-diagrams.md` for Mermaid C4 syntax reference
2. **Determine the scope**:
   - What system or subsystem to diagram?
   - What level(s)? (Context, Container, Component, Code)
   - If not specified, start with Context + Container
3. **Analyze the codebase** if diagramming an existing system:
   - Read project structure and key files
   - Identify external dependencies and integrations
   - Map internal components and their relationships
4. **Generate diagrams** using Mermaid C4 syntax:
   - **Level 1 — Context**: `C4Context` — system and its environment
   - **Level 2 — Container**: `C4Container` — high-level tech building blocks
   - **Level 3 — Component**: `C4Component` — internals of a container
   - **Level 4 — Code**: `classDiagram` — class/interface relationships
5. **Save** to the appropriate location:
   - Standalone: `<output>/[system]-c4.md`
   - As part of a design doc: embed in the design doc directly

## C4 Level Guide

### Level 1: System Context
- **Audience**: Everyone (tech and non-tech)
- **Shows**: The system as a box, users, and external systems
- **Elements**: `Person`, `System`, `System_Ext`, `Rel`

### Level 2: Container
- **Audience**: Technical people
- **Shows**: Applications, databases, message queues, file systems
- **Elements**: `Container`, `ContainerDb`, `ContainerQueue`, `System_Ext`, `System_Boundary`

### Level 3: Component
- **Audience**: Developers
- **Shows**: Components inside a container (services, repositories, controllers)
- **Elements**: `Component`, `Container_Boundary`, `ContainerDb`

### Level 4: Code
- **Audience**: Developers working on the component
- **Shows**: Classes, interfaces, relationships
- **Use**: Standard Mermaid `classDiagram` (not C4 syntax)

## Quality Checklist

- [ ] Each diagram has a descriptive title
- [ ] Relationships have labels describing what flows between elements
- [ ] External systems are clearly distinguished (`_Ext` suffix)
- [ ] Technology choices are annotated (e.g., "ASP.NET Core", "PostgreSQL")
- [ ] Diagrams zoom in logically (Context → Container → Component)
- [ ] No diagram has more than ~15 elements (split if larger)

## Tips

- Start broad (Context) and zoom in — don't jump to Component level
- Every relationship arrow should have a verb ("Calls", "Reads from", "Publishes to")
- Include the technology in element descriptions ("Angular", "REST/JSON", "gRPC")
- For deployment diagrams, use `C4Deployment` with `Deployment_Node`
