---
name: claude-code-analyze-config
description: Analyze repo's .claude/** for overlap with bluera-base and suggest cleanup
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
---

# Analyze Claude Config

Scan the repo's `.claude/**` for functionality that overlaps with bluera-base, report findings, and optionally clean up.

## Context

!`ls -la .claude/ 2>/dev/null | head -20 || echo "No .claude/ directory found"`

## bluera-base Components

This plugin provides:

### Commands (21 total)

- `/bluera-base:claude-code-analyze-config` - analyze .claude/ for overlap with bluera-base
- `/bluera-base:claude-code-audit-plugin` - audit a Claude Code plugin against best practices
- `/bluera-base:cancel-milhouse` - cancel active milhouse loop
- `/bluera-base:claude-code-md` - CLAUDE.md maintenance
- `/bluera-base:claude-code-clean` - diagnose slow startup and guide cleanup
- `/bluera-base:code-review` - multi-agent code review
- `/bluera-base:commit` - atomic commits with documentation awareness
- `/bluera-base:config` - configuration management
- `/bluera-base:dry` - detect duplicate code using jscpd
- `/bluera-base:explain` - explain plugin functionality
- `/bluera-base:harden-repo` - git hooks, linters, formatters setup
- `/bluera-base:help` - show plugin features and usage
- `/bluera-base:init` - initialize project with conventions
- `/bluera-base:install-rules` - install rule templates
- `/bluera-base:milhouse-loop` - iterative development loop
- `/bluera-base:readme` - README.md maintenance
- `/bluera-base:release` - version bumping and release workflow
- `/bluera-base:claude-code-statusline` - configure status line display
- `/bluera-base:claude-code-test-plugin` - plugin validation test suite
- `/bluera-base:todo` - manage project TODO tasks
- `/bluera-base:worktree` - manage git worktrees

### Skills (12 total)

- `atomic-commits` - commit grouping and documentation checks
- `auto-learn` - command pattern learning
- `claude-cleaner` - diagnose slow Claude Code startup
- `claude-md-maintainer` - CLAUDE.md structure and validation
- `code-review-repo` - code review guidelines
- `dry-refactor` - language-specific DRY refactoring guidance
- `large-file-refactor` - break apart large files
- `milhouse` - iterative loop patterns
- `readme-maintainer` - README formatting
- `release` - release workflow
- `repo-hardening` - linter/hook setup per language
- `statusline` - terminal status line configuration

### Hooks

- `SessionStart` - dependency checks, env setup
- `PreToolUse` - block manual releases, --no-verify
- `PostToolUse` - anti-pattern detection, linting
- `Stop` - milhouse loop continuation
- `PreCompact` - state preservation
- `Notification` - desktop alerts

## Workflow

### Phase 1: Scan Existing Config

Search for potentially overlapping content:

```bash
# Commands
ls .claude/commands/*.md 2>/dev/null

# Skills
ls -d .claude/skills/*/ 2>/dev/null

# Rules
ls .claude/rules/*.md 2>/dev/null

# Settings hooks
cat .claude/settings.json 2>/dev/null | jq '.hooks'
cat .claude/settings.local.json 2>/dev/null | jq '.hooks'
```

### Phase 2: Identify Overlaps

Compare each found item against bluera-base components:

| Category | Overlap Keywords |
|----------|------------------|
| Commit | commit, atomic, conventional |
| Release | release, version, tag, changelog |
| Loop | loop, iterate, milhouse, ralph |
| CLAUDE.md | claude.md, memory, rules |
| Code Review | review, lint, check |
| Hooks | pre-commit, post-edit, session |

For each potential overlap, categorize:

- **Duplicate**: Same functionality, can be removed
- **Overlap**: Similar functionality, may need merge
- **Complementary**: Different but related, keep both
- **Unique**: Not provided by bluera-base, keep

### Phase 3: Report Findings

Generate a report:

```markdown
## Config Analysis Report

### Duplicates (recommend removal)
- `.claude/commands/commit.md` - duplicates /bluera-base:commit
- `.claude/rules/commit-style.md` - covered by atomic-commits skill

### Overlaps (review needed)
- `.claude/skills/my-review/` - similar to code-review-repo
  - Unique aspects: [list]
  - Consider: merge or keep both

### Complementary (keep)
- `.claude/commands/deploy.md` - deployment workflow (not in bluera-base)

### Unique (keep)
- `.claude/rules/project-specific.md` - project-specific rules
```

### Phase 4: Interview User

For each duplicate/overlap, use AskUserQuestion:

1. **Duplicates**: "Remove `.claude/commands/commit.md`? (bluera-base provides /bluera-base:commit)"
   - Remove
   - Keep (disable bluera-base equivalent)
   - Keep both

2. **Overlaps**: "`.claude/skills/my-review/` overlaps with code-review-repo. Action?"
   - Remove (use bluera-base)
   - Merge unique parts into bluera-base skill
   - Keep separate

### Phase 5: Apply Cleanup (if --cleanup)

If `--cleanup` flag and user approved:

1. Move removed files to `.claude/archived/` (not delete)
2. Update `.claude/settings.json` if hooks changed
3. Report changes made

## Constraints

- Never delete without confirmation
- Archive removed files (don't permanently delete)
- Preserve project-specific customizations
- Favor bluera-base conventions when merging

## Example Output

```text
## Analysis Complete

Scanned: 5 commands, 3 skills, 8 rules, 2 hook configs

### Recommendations
- 2 duplicates (safe to remove)
- 1 overlap (needs review)
- 2 complementary (keep)
- 5 unique (keep)

Run with --cleanup to interactively clean up.
```
