---
name: migration-guides
description: Migration guides - from other AI tools, version upgrades, config migration. Use when switching from Cursor, Copilot, or Cody, upgrading Claude Code versions, or migrating configurations and customizations.
version: 1.0.0
author: Claude Code SDK
tags: [migration, upgrade, transition, compatibility]
---

# Migration Guides

Comprehensive guides for migrating to Claude Code from other AI coding assistants, upgrading between versions, and migrating configurations.

## Quick Reference

| Migration Type | Guide | Common Scenarios |
|---------------|-------|------------------|
| From other tools | [FROM-OTHER-TOOLS.md](./FROM-OTHER-TOOLS.md) | Cursor, Copilot, Cody, Aider |
| Version upgrades | [VERSION-UPGRADES.md](./VERSION-UPGRADES.md) | Breaking changes, new features |
| Configuration | [CONFIG-MIGRATION.md](./CONFIG-MIGRATION.md) | Settings, rules, permissions |

## Migration Decision Tree

```
What are you migrating?
|
+-- From another AI tool?
|   +-- GitHub Copilot --> See "From Copilot" section
|   +-- Cursor --> See "From Cursor" section
|   +-- Sourcegraph Cody --> See "From Cody" section
|   +-- Aider --> See "From Aider" section
|
+-- Upgrading Claude Code version?
|   +-- Minor version (1.x to 1.y) --> Usually safe, check changelog
|   +-- Major version (1.x to 2.x) --> Review breaking changes
|
+-- Migrating configuration?
    +-- Personal settings --> ~/.claude/settings.json
    +-- Project settings --> .claude/settings.json
    +-- Team settings --> .claude/settings.json + git
```

## Tool Comparison Overview

| Feature | Claude Code | Copilot | Cursor | Cody |
|---------|-------------|---------|--------|------|
| **Interface** | CLI + IDE | IDE plugin | Full IDE | IDE plugin |
| **Context** | Project-wide | File-based | Project-wide | Codebase |
| **Agentic** | Yes | Chat only | Yes | Limited |
| **MCP Support** | Yes | No | No | No |
| **Hooks** | Yes | No | No | No |
| **Skills** | Yes | No | No | No |
| **Custom Commands** | Yes | Limited | Yes | Limited |
| **Multi-file Edit** | Native | Manual | Native | Manual |
| **Git Integration** | Deep | Basic | Good | Basic |

## Core Concepts Mapping

### From Copilot

| Copilot Concept | Claude Code Equivalent |
|-----------------|----------------------|
| Copilot Chat | `claude` command |
| Inline suggestions | Not applicable (agentic model) |
| `/workspace` | Automatic (project context) |
| `/explain` | "explain this code" prompt |
| `/fix` | "fix this" prompt |
| `/tests` | "write tests for this" prompt |

### From Cursor

| Cursor Concept | Claude Code Equivalent |
|----------------|----------------------|
| Composer | `claude` agentic mode |
| Cursor Tab | Not applicable |
| `.cursorrules` | `CLAUDE.md` |
| `@codebase` | Automatic (Glob + Grep) |
| `@docs` | WebFetch or MCP servers |
| Inline edit | Edit tool |

### From Cody

| Cody Concept | Claude Code Equivalent |
|--------------|----------------------|
| Cody Chat | `claude` command |
| Autocomplete | Not applicable |
| Commands | Slash commands |
| Context selection | Automatic context |
| Embeddings | Glob + Grep search |

## Migration Workflow

### Phase 1: Assessment

- [ ] Document current tool usage patterns
- [ ] List custom configurations and rules
- [ ] Identify key workflows to preserve
- [ ] Note team conventions and standards

### Phase 2: Setup

- [ ] Install Claude Code: `npm install -g @anthropic-ai/claude-code`
- [ ] Run initial setup: `claude`
- [ ] Configure authentication
- [ ] Set permission mode for your workflow

### Phase 3: Configuration

- [ ] Create `CLAUDE.md` with project context
- [ ] Migrate rules to `.claude/settings.json`
- [ ] Set up hooks for automation
- [ ] Configure MCP servers if needed

### Phase 4: Validation

- [ ] Test key workflows
- [ ] Verify file operations work
- [ ] Check git integration
- [ ] Validate custom commands

### Phase 5: Team Rollout

- [ ] Document team conventions
- [ ] Share configuration files
- [ ] Create onboarding guide
- [ ] Establish support channel

## Configuration File Mapping

| Source Tool | Source File | Claude Code Target |
|-------------|-------------|-------------------|
| Cursor | `.cursorrules` | `CLAUDE.md` |
| Cursor | `.cursor/settings.json` | `.claude/settings.json` |
| Copilot | `.github/copilot-instructions.md` | `CLAUDE.md` |
| Cody | `.sourcegraph/cody.json` | `.claude/settings.json` |
| ESLint/Prettier | Config files | Hooks (PostToolUse) |

## Key Differences to Understand

### Agentic vs Autocomplete

Claude Code operates in an **agentic** mode:
- You describe what you want
- Claude plans and executes multiple steps
- Tools are used automatically (file read/write, search, bash)
- You approve or guide as needed

This differs from autocomplete-style tools where you:
- Type code and get suggestions
- Accept/reject line by line
- Manually trigger chat for larger tasks

### Context Window vs Embeddings

Claude Code uses a **context window** approach:
- Relevant files are loaded into context
- Glob and Grep search for specific content
- CLAUDE.md provides persistent project knowledge
- Compaction summarizes when context fills

Other tools may use **embeddings**:
- Entire codebase embedded in vector store
- Semantic search for relevant snippets
- May miss recent changes until re-indexed

### Permission Model

Claude Code has explicit permissions:
- File reads may need approval
- File writes need approval (unless configured)
- Bash commands need approval
- Permission modes control automation level

| Mode | Description |
|------|-------------|
| `default` | Ask for each sensitive operation |
| `plan` | Read-only, suggest but don't execute |
| `acceptEdits` | Auto-accept file edits |
| `dontAsk` | Trust all project operations |
| `bypassPermissions` | Skip all prompts (dangerous) |

## Common Migration Challenges

| Challenge | Solution |
|-----------|----------|
| No autocomplete | Use agentic workflow: describe, let Claude implement |
| Different context model | Use CLAUDE.md for persistent context |
| Team configuration | Commit `.claude/settings.json` to repo |
| IDE integration | Use Claude Code with your existing editor |
| Custom rules | Migrate to CLAUDE.md and hooks |

## Workflow Translation Examples

### Code Review

**Copilot/Cursor:**
```
Select code -> Right-click -> "Explain" or "Review"
```

**Claude Code:**
```bash
claude "review the changes in this PR for bugs and improvements"
```

### Bug Fixing

**Copilot/Cursor:**
```
Select error -> "Fix this"
```

**Claude Code:**
```bash
claude "fix the TypeError in src/api/handler.ts"
```

### Test Generation

**Copilot/Cursor:**
```
Select function -> "Generate tests"
```

**Claude Code:**
```bash
claude "write unit tests for the UserService class"
```

### Code Explanation

**Copilot/Cursor:**
```
Select code -> "Explain this"
```

**Claude Code:**
```bash
claude "explain how the authentication flow works in src/auth/"
```

## Best Practices

### 1. Start with CLAUDE.md

Create a comprehensive `CLAUDE.md` at project root:

```markdown
# Project Name

## Tech Stack
- Framework: Next.js 14
- Database: PostgreSQL with Drizzle
- Testing: Vitest

## Conventions
- Use TypeScript strict mode
- Prefer functional components
- Follow existing patterns in codebase

## Key Files
- `src/lib/db.ts` - Database connection
- `src/middleware.ts` - Auth middleware
```

### 2. Use Hooks for Automation

Replace IDE-specific automation with hooks:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bun run format"
          }
        ]
      }
    ]
  }
}
```

### 3. Configure Permissions Appropriately

Start conservative, loosen as needed:

```bash
# Start with default (asks for everything)
claude

# Move to auto-accept edits when comfortable
claude --dangerously-skip-permissions
```

### 4. Create Custom Slash Commands

Replace tool-specific commands with slash commands:

```markdown
<!-- .claude/commands/review.md -->
---
description: Review code changes for issues
---
Review the following code for:
- Potential bugs
- Performance issues
- Security concerns
- Code style violations
```

### 5. Leverage MCP for External Data

Replace tool-specific integrations with MCP servers:

```json
{
  "mcpServers": {
    "docs": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-docs-server"]
    }
  }
}
```

## Validation Checklist

After migration, verify:

- [ ] Can create new files
- [ ] Can edit existing files
- [ ] Can run bash commands
- [ ] Can search codebase (Glob, Grep)
- [ ] Git operations work
- [ ] Custom commands are available
- [ ] Hooks execute correctly
- [ ] CLAUDE.md context is loaded
- [ ] Team members can use shared config

## Reference Files

| File | Contents |
|------|----------|
| [FROM-OTHER-TOOLS.md](./FROM-OTHER-TOOLS.md) | Detailed tool-specific migration guides |
| [VERSION-UPGRADES.md](./VERSION-UPGRADES.md) | Version upgrade patterns and breaking changes |
| [CONFIG-MIGRATION.md](./CONFIG-MIGRATION.md) | Configuration file migration details |
