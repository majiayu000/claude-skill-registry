---
name: scaffold-rules
description: Scaffold development rules for AI coding agents. Auto-invoked when user asks about setting up rules, coding conventions, or configuring their AI agent environment.
license: ISC
compatibility: Requires bun
allowed-tools: Glob, Read, Write, Edit, AskUserQuestion
---

# Scaffold Rules

Scaffold and merge development rules adapted to different AI coding agent environments.

## Purpose

Use this skill when the user wants to:
- Set up development rules or coding conventions
- Configure their AI coding agent (Claude Code, Cursor, Copilot, etc.)
- Add or update project guidelines
- Standardize conventions across a team

## Supported Agents

| Agent | Config Location | Format |
|-------|-----------------|--------|
| Claude Code | `.claude/rules/*.md` | Separate markdown files |
| Cursor | `.cursorrules` or `.cursor/rules/*.md` | Single or multi-file |
| GitHub Copilot | `.github/copilot-instructions.md` | Single file |
| Windsurf | `.windsurfrules` | Single file |
| Cline/Roo | `.clinerules` | Single file |
| Aider | `.aider.conf.yml` | YAML config |

## Rule Categories

### Bun APIs
Prefer Bun's native APIs over Node.js equivalents:
- `Bun.file()` over `fs` APIs
- `Bun.$` for shell commands
- `Bun.write()` for file writes
- `import.meta.dir` for current directory

### Git Workflow
Commit conventions and version control:
- Conventional commit prefixes: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`, `test:`
- Multi-line commit message formatting
- Agent-specific sandbox workarounds

### GitHub CLI
Prefer `gh` CLI for GitHub operations:
- PR review and creation patterns
- Issue management
- JSON output field references
- Authentication benefits over WebFetch

### TypeScript Conventions
Code style standards:
- Prefer `type` over `interface`
- No `any` types (use `unknown` with type guards)
- Arrow functions preferred
- Object parameter pattern for 2+ parameters
- PascalCase for types, `PascalCaseSchema` suffix for Zod schemas

### Testing Patterns
Bun test runner conventions:
- Use `test()` instead of `it()`
- `*.spec.ts` file naming
- No conditionals around assertions
- Assert existence before checking values

## Merge Behavior

**Always scans existing rules first.** When existing rules are found:

1. **Analyze overlap** - Identify sections covering same topics
2. **Propose merge** - Show what would be added/changed
3. **User approval** - Ask before modifying:
   - Keep existing (skip new content)
   - Merge (add missing sections)
   - Replace entirely

This ensures the command never overwrites user customizations without consent.

## Agent Adaptations

Content is adapted based on agent capabilities:

- **Sandbox awareness**: Include/exclude sandbox workarounds based on agent
- **Tool references**: Adjust tool names (e.g., "Bash tool" → "terminal")
- **Format**: Single file vs multi-file based on agent convention
- **Length**: Condense for agents with size limits

## Usage

Run the `/scaffold-rules` command to interactively scaffold rules, or invoke when user asks about:
- "Set up coding conventions"
- "Configure my AI agent"
- "Add development rules"
- "What rules should I have?"
