---
name: pre-push-validation
description: Ensures CLAUDE.md, README.md, and CHANGELOG.md are updated before git push operations
version: 1.0.0
author: Tom Cranstoun
trigger_type: intent
keywords:
  - git push
  - commit push
  - pushing changes
  - before push
  - validate docs
  - check documentation
intent_patterns:
  - "push.*changes"
  - "git push"
  - "ready.*push"
  - "update.*push"
enforcement: suggest
---

# Pre-Push Validation Skill

Ensures critical documentation files are updated before pushing changes to the repository.

## What This Skill Does

**Automatic validation before `git push`** - The pre-push hook checks that documentation is current:

1. **CHANGELOG.md** - Must document your changes
2. **README.md** - Must reflect any project structure changes
3. **CLAUDE.md** - Must reflect any AI instruction changes

## How It Works

### Pre-Push Hook

The hook `.claude/hooks/pre-push-validation.sh` runs automatically before `git push` operations:

**Validation Logic:**
- ✅ **Checks commit dates** - Documentation must be updated since oldest unpushed commit
- ✅ **Detects uncommitted changes** - Warns if docs have uncommitted changes
- ✅ **Validates file existence** - Ensures all critical files exist
- ❌ **Blocks push** - If documentation is outdated relative to code changes

**Example Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 PRE-PUSH VALIDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Commits to push: 3
🌿 Branch: main → origin/main

📝 Checking documentation files...

✓ CLAUDE.md: Updated 2025-12-10
✓ README.md: Updated 2025-12-10
❌ CHANGELOG.md: Not updated since 2025-12-09

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ VALIDATION FAILED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please update the following files before pushing:
  • CHANGELOG.md

💡 Tips:
  1. Update CHANGELOG.md with your changes
  2. Update README.md if project structure changed
  3. Update CLAUDE.md if AI instructions changed
  4. Commit your documentation updates
  5. Push again
```

## When to Update Each File

### CHANGELOG.md (Required for ALL commits)

**Always update when:**
- Adding new features
- Fixing bugs
- Refactoring code
- Changing dependencies
- Modifying configuration
- Updating documentation

**Format:**
```markdown
## [YYYY-MM-DD<letter>] - Brief Title

### Added/Changed/Fixed/Removed
- Detailed description of changes
- Impact and rationale
- Technical details

### Files Modified
1. `path/to/file.js` - Description
2. `path/to/file.css` - Description

**Total: X files modified**
```

### README.md (Update when project changes)

**Update when:**
- Adding new blocks or components
- Changing project structure
- Adding new npm scripts
- Modifying development workflow
- Adding new dependencies
- Changing infrastructure

### CLAUDE.md (Update when AI instructions change)

**Update when:**
- Adding new coding patterns
- Changing project conventions
- Adding new skills or commands
- Modifying development requirements
- Updating architecture decisions
- Changing configuration patterns

## Using the Skill

### Before Every Push

1. **Review your commits:**
   ```bash
   git log origin/main..HEAD --oneline
   ```

2. **Update documentation:**
   - CHANGELOG.md - Document all changes
   - README.md - Update if structure changed
   - CLAUDE.md - Update if AI instructions changed

3. **Commit all changes (including user edits):**
   ```bash
   git add .
   git commit -m "docs: Update documentation for [feature/fix]"
   ```

4. **Push with confidence:**
   ```bash
   git push
   ```
   The hook will validate and either allow or block the push.

### Bypassing Validation (NOT RECOMMENDED)

If you absolutely must push without updating documentation:

```bash
git push --no-verify
```

**⚠️ Warning:** Only use this for:
- Emergency hotfixes
- Work-in-progress branches
- Documentation-only changes

**Never use `--no-verify` for main/production branches.**

## Hook Installation

The hook is automatically available in Claude Code projects. To verify:

```bash
ls -la .claude/hooks/pre-push-validation.sh
```

Should show executable permissions: `-rwxr-xr-x`

If not executable:
```bash
chmod +x .claude/hooks/pre-push-validation.sh
```

## Workflow Integration

### Recommended Git Workflow

1. **Make code changes** - Implement features/fixes
2. **Commit code** - `git commit -m "feat: Add new feature"`
3. **Update documentation** - CHANGELOG.md, README.md, CLAUDE.md as needed
4. **Commit documentation** - `git commit -m "docs: Document new feature"`
5. **Push** - `git push` (hook validates automatically)

### Multi-Commit Sessions

If you have multiple commits:

```bash
# Commits in current session
git log origin/main..HEAD --oneline

# The hook checks documentation is newer than ALL unpushed commits
```

**Best Practice:** Update documentation as you go, not at the end.

## Troubleshooting

### "VALIDATION FAILED" Error

**Problem:** Documentation files are outdated compared to code commits.

**Solution:**
1. Check which files need updating (listed in error message)
2. Update those files with your changes
3. Commit all changes (including user edits): `git add . && git commit -m "docs: Update documentation"`
4. Try pushing again: `git push`

### "Has uncommitted changes" Warning

**Problem:** Documentation file has uncommitted changes.

**Solution:**
1. Review changes: `git diff [file]`
2. Stage all changes: `git add .`
3. Commit changes: `git commit -m "docs: Update [file]"`
4. Push: `git push`

### Hook Not Running

**Problem:** Push succeeds without validation.

**Possible causes:**
1. Hook file not executable - Run: `chmod +x .claude/hooks/pre-push-validation.sh`
2. Not in git repository - Verify: `git rev-parse --is-inside-work-tree`
3. New branch without upstream - Expected behavior, validation skipped

## Benefits

1. **Consistent Documentation** - Forces documentation updates before push
2. **Better Change History** - CHANGELOG.md always current
3. **Team Alignment** - Everyone knows what changed and why
4. **AI Assistant Context** - CLAUDE.md stays current with project changes
5. **Prevents "I forgot to document"** - Automated validation reminder

## Configuration

The hook is configured via critical files array in the script:

```bash
CRITICAL_FILES=(
    "CLAUDE.md"
    "README.md"
    "CHANGELOG.md"
)
```

To add more files, edit `.claude/hooks/pre-push-validation.sh` and add to the array.

## See Also

- **Hook configuration:** `.claude/hooks/CONFIG.md`
- **Git hooks documentation:** `.claude/hooks/README.md`
- **CHANGELOG format:** `CHANGELOG.md` (see existing entries)
- **README structure:** `README.md` (top-level sections)
- **CLAUDE.md patterns:** `CLAUDE.md` (configuration patterns section)
