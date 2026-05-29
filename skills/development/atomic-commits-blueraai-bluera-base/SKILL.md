---
name: atomic-commits
description: Create atomic commits grouped by logical features with README.md and CLAUDE.md awareness.
version: 1.0.0
---

# Atomic Commits with Documentation Awareness

Guidelines for creating well-organized commits with README.md and CLAUDE.md awareness.

## Documentation Check

Before committing, evaluate if changes need documentation updates.

### README.md (User-facing documentation)

| Change Type | README Section to Update |
|-------------|-------------------------|
| New commands or features | Commands/Usage documentation |
| CLI interface changes | Usage examples |
| Configuration changes | Configuration/Environment sections |
| Breaking API changes | Upgrade/migration notes |
| New features | Feature documentation |
| Installation changes | Installation section |

**Trigger files (project-specific - customize in your .claude/skills/):**

- `src/cli.ts` or `src/index.ts` - Entry points
- `.claude-plugin/plugin.json` - Plugin metadata
- `commands/*.md` - Command definitions

### CLAUDE.md (Claude Code memory - hierarchical)

CLAUDE.md stores context that helps future sessions "do the right thing". Update when:

- You struggled with something and the insight would prevent future mistakes
- Important patterns or conventions that aren't obvious from code alone
- Workflows or commands that are non-trivial to discover

CLAUDE.md is hierarchical - use the directory level matching the changed files. Use `@path/to/file` includes to stay DRY.

| Change Scope | Which CLAUDE.md |
|--------------|-----------------|
| Project-wide (scripts, CI/CD, build) | Root CLAUDE.md |
| Directory-specific patterns | Subdirectory CLAUDE.md (create if needed) |

## Grouping Rules

Identify logical features by grouping related files:

- Same feature = same commit
- Infrastructure/config = separate commit
- Tests = with their implementation OR separate if test-only

## Commit Message Format

```text
<type>(<scope>): <description>
```

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `style`, `build`, `ci`, `perf`

**Note:** Commit messages are validated by commitlint (conventional commits format).
