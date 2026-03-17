---
name: agents-md
description: |
    Use when creating or updating AGENTS.md files to guide AI coding agents. Covers file structure, placement, content guidelines, and best practices for project-level agent instructions.
    USE FOR: project-specific agent instructions, build/test commands for agents, coding conventions, repository-level guidance
    DO NOT USE FOR: reusable cross-project skills (use agent-skills), agent runtime definition (use adl)
license: MIT
metadata:
  displayName: "AGENTS.md"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "AGENTS.md Specification GitHub Repository"
    url: "https://github.com/anthropics/agent-skills"
  - title: "Claude Code Documentation"
    url: "https://docs.anthropic.com/en/docs/claude-code"
---

# AGENTS.md

## Overview
AGENTS.md is a community convention for providing project-specific guidance to AI coding agents. Think of it as a README for agents — containing the tribal knowledge that senior engineers carry: build steps, test commands, architectural conventions, and coding standards. Adopted by 60,000+ open-source projects and supported by Claude Code, Codex, Gemini CLI, Jules, Factory, and Cursor.

## File Placement
| Location | Scope |
|----------|-------|
| `AGENTS.md` (repo root) | Applies to the entire repository |
| `src/AGENTS.md` | Applies to the `src/` directory and below |
| `src/api/AGENTS.md` | Applies to `src/api/` specifically |

Agents read the most specific AGENTS.md for the files they're working on, inheriting from parent directories.

## Recommended Structure
```markdown
# AGENTS.md

## Build & Test
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`
- Single test: `npm test -- --grep "test name"`

## Architecture
- Monorepo with packages in `packages/`
- API server in `packages/api/` (Express + TypeScript)
- Frontend in `packages/web/` (React + Vite)
- Shared types in `packages/shared/`

## Conventions
- Use TypeScript strict mode
- Prefer `async/await` over `.then()` chains
- Use named exports, not default exports
- Error messages must be user-facing strings, not developer jargon

## Testing
- Unit tests live next to source files: `foo.test.ts`
- Integration tests in `tests/integration/`
- Use `vitest` for all tests
- Mock external APIs, never hit real endpoints in tests

## Do NOT
- Do not modify `generated/` files — they are auto-generated
- Do not add dependencies without checking `package.json` first
- Do not use `any` type in TypeScript
```

## Content Guidelines
- **Aim for under 150 lines** — concise beats comprehensive
- **Use concrete rules**, not vague guidance: "Use vitest" not "Use a good test framework"
- **Include exact commands**: `npm run build`, not "run the build"
- **Organize by category**: Build, Architecture, Conventions, Testing, Do-NOTs
- **Use bullet points** for scanability
- **Include code examples** where conventions aren't obvious

## What to Include
- Build, test, and lint commands (exact CLI invocations)
- Project structure and key directories
- Naming conventions (files, variables, branches)
- Technology choices and versions
- Error handling patterns
- Things to avoid (common mistakes agents make in this codebase)

## What NOT to Include
- General programming advice agents already know
- Full API documentation (link to it instead)
- Sensitive information (secrets, internal URLs)
- Information that changes frequently (use links to living docs)

## AGENTS.md vs Agent Skills
| Aspect | AGENTS.md | Agent Skills (SKILL.md) |
|--------|-----------|------------------------|
| Scope | One specific project/repo | Reusable across any project |
| Content | Build steps, conventions, architecture | Framework guidance, tool knowledge |
| Discovery | Found in repo directories | Discovered via skill registries |
| Format | Freeform Markdown | YAML frontmatter + Markdown |

They complement each other: AGENTS.md provides project-specific context while Agent Skills provide domain knowledge.

## Best Practices
- Keep it under 150 lines — agents have limited context, so density matters.
- Put the most important commands (build, test) at the top.
- Update AGENTS.md when you change build processes or conventions.
- Use directory-scoped AGENTS.md files for large monorepos instead of one giant root file.
- Test your AGENTS.md by asking an agent to perform a task and seeing if it follows the guidance.
- Don't duplicate README content — AGENTS.md is for agent-specific instructions that would clutter a README.
