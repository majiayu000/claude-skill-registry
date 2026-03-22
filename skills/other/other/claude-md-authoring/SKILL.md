---
name: claude-md-authoring
description: Guidelines for creating and maintaining CLAUDE.md files. Use when creating, updating, or reviewing CLAUDE.md documentation. Includes target file determination, templates, auto-load behavior, monorepo patterns, and best practices.
durability: encoded-preference
---

# Purpose

This skill provides a complete framework for authoring CLAUDE.md files, including:
1. Determining which CLAUDE.md file to update (root vs subdirectory)
2. Templates and structural patterns
3. Best practices for content and formatting
4. Monorepo and multi-component project strategies

# Determining Target CLAUDE.md File

Before creating or updating content, determine which CLAUDE.md file should be the target.

## Working Directory Detection

Analyze the session to identify the primary working area using these signals:
- **File modification analysis**: Which directory has the most changes?
- **Command execution context**: Where were build/test commands run?
- **User focus indicators**: Explicit statements, file paths, problem domains
- **Scope analysis**: Multi-package → root; single component → subdirectory; architectural → root

See `references/targeting-examples.md` for detailed examples of target file selection.

## Content Classification Criteria

Use this decision matrix to classify session insights:

| Content Type | Examples | Target CLAUDE.md |
|--------------|----------|------------------|
| **Component-specific commands** | `npm run migrate`, `make build-api`, `pytest tests/api/` | Subdirectory |
| **Component-specific conventions** | "API routes must use async/await", "Frontend components use composition API" | Subdirectory |
| **Component-specific gotchas** | "PostgreSQL connections timeout after 30s", "React strict mode breaks this package" | Subdirectory |
| **Component architecture** | "API uses layered architecture", "Frontend state management with Pinia" | Subdirectory |
| **Component-specific testing** | "API tests require Docker", "Frontend uses Playwright" | Subdirectory |
| **Platform-specific (if per-package)** | "Windows: use WSL for API builds" | Subdirectory |
| **Shared conventions** | Commit message format, code review process, PR guidelines | Root |
| **Monorepo-wide commands** | `npm run build:all`, `make test-all`, workspace management | Root |
| **Project architecture** | Overall system design, service communication, shared infrastructure | Root |
| **Cross-cutting concerns** | Authentication strategy, logging approach, error handling patterns | Root |
| **Development environment** | IDE setup, linter configuration, formatter settings | Root |

## Decision Flow

Follow this systematic approach:

```
1. Identify primary working directory
   └─> Use file modification counts and command context

2. Classify content type
   └─> Use Content Classification Criteria table

3. Apply decision rules:

   IF content applies ONLY to identified directory:
       └─> Target: subdirectory CLAUDE.md

   ELSE IF content applies to multiple directories:
       └─> Target: root CLAUDE.md

   ELSE IF content is architectural/cross-cutting:
       └─> Target: root CLAUDE.md

   ELSE IF uncertain:
       └─> Ask user for clarification
```

## Edge Cases

**Multi-Directory Work Sessions:**
- Related components (e.g., `api/controllers/` and `api/models/`) → use parent directory CLAUDE.md
- Unrelated components → update root CLAUDE.md with cross-cutting insights
- Refactoring across areas → document in root CLAUDE.md

**Uncertain Classification:**
1. Ask the user: "Should this guidance apply only to [directory] or project-wide?"
2. Default to narrower scope (easier to move content up than down)
3. Consider where information would be most useful in future sessions

**Existing Subdirectory CLAUDE.md:**
1. Read it first to understand existing structure
2. Add new content to appropriate section
3. Avoid duplicating information from root CLAUDE.md
4. Maintain consistency with existing style

## Subdirectory CLAUDE.md Management

### When to Create

Create a new subdirectory CLAUDE.md when:

1. **Isolation Test**: Content is meaningful ONLY in that directory context
2. **Scope Test**: Information would clutter root CLAUDE.md
3. **Frequency Test**: Future sessions will work in this directory
4. **Ownership Test**: Directory has distinct conventions/workflows

### Subdirectory CLAUDE.md Template

Use this minimal template for new subdirectory CLAUDE.md files:

```markdown
# [Component Name]

[One-line description of this component's purpose]

## Commands

### Development
```bash
# Component-specific development commands
```

### Testing
```bash
# Component-specific test commands
```

## Architecture

### Component Structure
[Brief overview of how this component is organized]

### Key Technologies
- [Technology]: [Version and purpose]

## Important Notes

### Conventions
- [Component-specific conventions]

### Gotchas
- [Component-specific gotchas]
```

### Content Scope Rules

**Subdirectory CLAUDE.md should contain:**
- Commands run from this directory
- Conventions specific to this component
- Architecture of this component only
- Dependencies unique to this component
- Gotchas specific to this component

**Subdirectory CLAUDE.md should NOT contain:**
- General project conventions (belongs in root)
- Commands run from project root
- Cross-component architecture
- Shared dependencies
- Monorepo-wide workflows

## Targeting Examples

See `references/targeting-examples.md` for detailed examples of target file selection.

# Auto-Loaded Files & Advanced Patterns

For detailed documentation on auto-loaded files, CLAUDE.md vs .claude/ directory, monorepo patterns, and @import syntax, see `references/advanced-patterns.md`.

**Key rules:**
- `CLAUDE.md`, `CLAUDE.local.md`, `.claude/CLAUDE.md`, and `.claude/rules/*.md` are auto-loaded at startup
- Files named `CLAUDE-API.md` or `CLAUDE-FRONTEND.md` are NOT auto-loaded -- use subdirectory CLAUDE.md or @import
- `.claude/` directories in subdirectories are IGNORED -- only project root or `~/.claude/` are recognized
- Use subdirectory `CLAUDE.md` for simple instructions; use `.claude/skills/` with `paths:` for complex scoped logic
- Use `@import` to modularize single-project documentation (e.g., `@./docs/api-guidelines.md`)

# CLAUDE.md Template Structure

See `references/template.md` for the full CLAUDE.md starter template.

## Section Priority

Order sections by frequency of use:

1. **Commands**: Most frequently needed information
2. **Architecture**: Understanding the codebase
3. **Workflow**: How to work with the project
4. **Notes/Gotchas**: Avoiding common problems
5. **Other sections**: As relevant to the project

# Example Update Scenarios

See `references/update-scenarios.md` for detailed update examples.

# Large Projects Tips

For extensive documentation:
- Use clear section headers for navigation
- Include a table of contents for long files (use @import to modularize)
- Cross-reference related sections
- Consider subdirectory CLAUDE.md files for isolated components
- Use skills with `paths:` field for complex, scoped logic

# Content Placement by Frequency

When deciding what belongs directly in CLAUDE.md versus an external file:

| Content Type | Placement | Example |
|--------------|-----------|---------|
| High-frequency (used most sessions) | Inline in CLAUDE.md | Commands, architecture, workflow |
| Low-frequency (used occasionally) | @import or inline | Testing gotchas, environment notes |
| Rarely-needed (one-time setup) | External file with summary reference | MCP setup guides, onboarding steps |

**Principle**: CLAUDE.md should prioritize content that is useful in the majority of sessions. Rarely-needed content (one-time setup, infrequent procedures) should be extracted to external files and replaced with a one-liner summary that tells Claude WHEN to offer the guide and WHERE to find it.

# Anti-Patterns

**Do NOT:**
- Create files like `CLAUDE-API.md` or `CLAUDE-FRONTEND.md` (not auto-loaded)
- Place `.claude/` directories in subdirectories (ignored by Claude Code)
- Default to root CLAUDE.md without analyzing session context
- Add subdirectory-specific content to root CLAUDE.md
- Duplicate root CLAUDE.md content in subdirectories
- Create subdirectory CLAUDE.md for trivial or single-use information
- Mix component-specific and project-wide content in same file
- Keep one-time setup procedures inline when they could be extracted with a summary reference
- Include general programming knowledge (Claude already knows this)
- Write tutorials on basic syntax
- Copy documentation that exists elsewhere (use @import instead)
- Make sections too verbose (use references/ in skills for details)
- Use inconsistent heading levels
- Include sensitive information (API keys, passwords)

**DO:**
- Systematically analyze session context before choosing target file
- Use content classification criteria to determine target
- Ask user when uncertain about target file
- Use subdirectory CLAUDE.md files for component-specific guidance
- Keep subdirectory CLAUDE.md focused and minimal
- Use @import for modularizing single-project documentation
- Focus on project-specific conventions and decisions
- Keep commands and examples up-to-date
- Include "why" behind non-obvious decisions
- Cross-reference related sections
- Use code blocks with syntax highlighting
- Extract rarely-needed content (one-time setup, infrequent procedures) to external files with summary references
- Verify no duplicate information exists across CLAUDE.md files
