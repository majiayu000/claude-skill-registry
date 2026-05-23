---
name: claude-code-project-memory
description: Configure CLAUDE.md project memory files for persistent context, coding standards, architecture decisions, and team conventions. Reference for the 4-tier memory hierarchy, cross-platform AGENTS.md compatibility, and quick-add commands.
---

# Claude Code Project Memory (Jan 2026)

Configure `CLAUDE.md` project memory so Claude Code gets stable, scoped instructions across sessions while keeping token cost low.

## Quick Reference

| Memory Type | Typical Location | Purpose |
|------------|------------------|---------|
| Managed policy | OS-dependent (see official docs) | Organization-wide standards (security, compliance) |
| Project memory | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Shared project context and conventions |
| Project rules | `./.claude/rules/*.md` | Modular, topic-focused rules (testing, security, style) |
| User memory | `~/.claude/CLAUDE.md` | Personal preferences across projects |
| Project memory (local) | `./CLAUDE.local.md` (git-ignored) | Local-only, project-specific preferences |

### How Loading Works (High Level)

- **Recursive loading**: from the current working directory up to (but not including) filesystem root (`/`).
- **On-demand loading**: nested `CLAUDE.md` files under the cwd are loaded only when Claude reads files in those subtrees.
- **Imports**: `@path/to/file` pulls in additional context (max depth: 5; `~` supported).

## Workflow (Best Practice)

1. Start with a minimal `CLAUDE.md` (50–120 lines): what the project is, how it’s shaped, and the “must not break” rules.
2. Move long or fragile guidance into `.claude/rules/` (one topic per file).
3. Use `@imports` as navigation for detailed docs instead of copying them into memory.
4. Treat memory like code: PR review, ownership, and periodic cleanup (remove dead rules).

## Rules With Optional Path Scope

Create `.claude/rules/testing.md`, `.claude/rules/security.md`, etc. If a rule only applies to a slice of the repo, scope it:

```yaml
---
paths:
  - "src/api/**/*.ts"
---
```

## Commands (Claude Code)

- `> /memory` to view and directly edit memories.
- `> /init` to bootstrap project memory (see official docs for current behavior).

## Cross-Platform Strategy (AGENTS.md + CLAUDE.md)

If you support multiple coding assistants, keep one canonical file and mirror it:

- macOS/Linux: symlink one to the other.
- Windows: prefer copying (or a small sync script) over symlinks unless Developer Mode is enabled.

Avoid tool-specific claims in the memory file; keep it portable and strictly project-focused.

## Validation (Fast Checks)

- Run the bundled linter: `bash frameworks/shared-skills/skills/claude-code-project-memory/scripts/lint_claude_memory.sh .`
- Manually scan for unresolved `@imports` and secrets before merging memory changes.

## Resources

| Resource | Purpose |
|----------|---------|
| [references/memory-patterns.md](references/memory-patterns.md) | Patterns and anti-patterns |
| [references/memory-examples.md](references/memory-examples.md) | Full examples by stack |
| [references/large-codebase-strategy.md](references/large-codebase-strategy.md) | 100K–1M LOC strategy |
| [data/sources.json](data/sources.json) | Official links |

## Related Skills

| Skill | Purpose |
|-------|---------|
| [claude-code-skills](../claude-code-skills/SKILL.md) | Skill creation patterns |
| [claude-code-agents](../claude-code-agents/SKILL.md) | Claude Code agent setup |
| [docs-codebase](../docs-codebase/SKILL.md) | Repo documentation patterns |
