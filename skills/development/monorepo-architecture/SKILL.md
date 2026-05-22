---
name: monorepo-architecture
description: "Design and reason about full-stack monorepo layouts compatible with Spec-Kit Plus and Claude Code. This skill should be used when designing the initial monorepo structure for a full-stack application, planning directory organization for frontend and backend separation, establishing shared configuration and tooling patterns, defining workspace boundaries for package managers, creating architectural plans that span multiple application layers, and ensuring Spec-Kit Plus artifacts integrate correctly across the monorepo."
---

# Monorepo Architecture

## Purpose
Design and reason about full-stack monorepo layouts compatible with Spec-Kit Plus and Claude Code. This skill establishes directory structures that cleanly separate frontend, backend, and shared concerns while enabling efficient development workflows in Phase II.

## When to Use
- When designing the initial monorepo structure for a full-stack application
- When planning directory organization for frontend and backend separation
- When establishing shared configuration and tooling patterns
- When defining workspace boundaries for package managers (pnpm, npm workspaces)
- When creating architectural plans that span multiple application layers
- When ensuring Spec-Kit Plus artifacts integrate correctly across the monorepo

## When NOT to Use
- When working on single-tier applications (console-only, frontend-only)
- When the project structure has already been finalized and implemented
- When making changes to individual component internals
- When specifications have not been validated
- When decomposing architecture into tasks (use task-decomposition)

## Required Clarifications
1. What is the technology stack being used (Next.js, FastAPI, etc.)?
2. What are the specific frontend and backend requirements?
3. Are there existing repository structures that need to be considered?
4. What package manager will be used (pnpm, yarn workspaces, npm workspaces)?

## Optional Clarifications
5. Are there specific deployment requirements that affect directory structure?
6. Are there existing conventions in the codebase to follow?
7. What are the performance requirements for the monorepo setup?

## Responsibilities
- Define top-level monorepo directory structure
- Establish clear boundaries between frontend, backend, and shared code
- Plan configuration file placement (package.json, pyproject.toml, etc.)
- Design spec directory organization for multi-layer features
- Ensure CLAUDE.md files can be structured per layer
- Document workspace and dependency management strategy
- Maintain compatibility with Spec-Kit Plus tooling
- Enable independent development and deployment of layers

## Inputs
- Validated specification documents
- Constitution and Phase II governance requirements
- Technology stack decisions (Next.js, FastAPI, PostgreSQL)
- Spec-Kit Plus directory conventions
- Existing repository structure (if migrating)

## Outputs
- Monorepo directory structure diagram
- Layer boundary definitions (frontend/, backend/, shared/)
- Configuration file placement plan
- Workspace configuration strategy
- Integration points between layers
- CLAUDE.md placement strategy per layer

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, conventions |
| **Conversation** | User's specific requirements |
| **Skill References** | Domain patterns from `references/` |
| **User Guidelines** | Project-specific conventions |

## Implementation Workflow
1. Assess technology stack and requirements
2. Design top-level directory structure
3. Establish layer boundaries (frontend, backend, shared)
4. Plan configuration file placement
5. Design spec directory organization
6. Document workspace management strategy
7. Validate against constraints and anti-patterns
8. Create directory structure diagram
9. Document integration points

## Output Checklist
- [ ] Monorepo directory structure designed
- [ ] Clear layer boundaries established
- [ ] Configuration file placement planned
- [ ] Workspace management strategy documented
- [ ] Spec directory organization designed
- [ ] CLAUDE.md placement strategy defined
- [ ] Integration points documented
- [ ] Constraints respected

## Constraints
- Never mix frontend and backend code in the same directory
- Never create circular dependencies between layers
- Never violate Spec-Kit Plus directory conventions
- Never design structures that prevent independent layer testing
- Always maintain clear ownership boundaries for each layer
- Always ensure specs can reference appropriate layer contexts
- Always enable Claude Code to operate on isolated layer contexts

## Interaction With Other Skills
- **claude-context-design:** Produces structure that supports layered CLAUDE.md files
- **spec-referencing:** Creates directory layout that supports @specs path conventions
- **frontend-architecture:** Defines frontend directory within monorepo context
- **python-backend-structure:** Defines backend directory within monorepo context
- **constraint-enforcement:** Ensures monorepo design respects project constraints

## Anti-Patterns
- **Flat chaos:** Placing all code at repository root without layer separation
- **Over-nesting:** Creating excessively deep directory hierarchies
- **Shared pollution:** Putting too much code in shared directories
- **Config sprawl:** Scattering configuration files without clear organization
- **Implicit dependencies:** Creating hidden dependencies between layers
- **Tooling lock-in:** Designing structures that only work with specific tools
- **Context confusion:** Ambiguous boundaries that confuse Claude Code context loading

## Security Best Practices
- Restrict sensitive configuration to appropriate layers
- Use proper secrets management per layer
- Ensure proper access controls for different parts of the monorepo
- Separate build and deployment configurations appropriately

## Documentation Resources
- [Monorepo Tools Overview](https://vercel.com/blog/monorepos)
- [PNPM Workspaces Guide](https://pnpm.io/workspaces)
- [Nx Monorepo Patterns](https://nx.dev/getting-started/intro)
- [Lerna Monorepo Management](https://lerna.js.org/)
- [Spec-Kit Plus Documentation](https://github.com/spec-kit-plus/docs)

## Phase Applicability
Phase II only. Phase I uses single-layer Python console structure.