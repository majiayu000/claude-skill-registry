---
name: hidden-folder-audit
description: Audit and consolidate hidden folders in a repository. Identifies duplicates, dead directories, and consolidation opportunities for .agent-os/, .ai/, .claude/, and other hidden folders.
version: 1.2.0
updated: 2026-01-20
category: meta
triggers:
- hidden folder audit
- consolidate hidden folders
- .agent-os cleanup
- .ai cleanup
- dot folder review
---

# Hidden Folder Audit Skill

Systematic audit and consolidation of hidden (dot) folders in a repository. Identifies duplicate configurations, dead symlinks, orphaned directories, and consolidation opportunities to establish a clean, maintainable folder structure.

## Version Metadata

```yaml
version: 1.2.0
python_min_version: '3.10'
dependencies: []
compatibility:
  tested_python:
  - '3.10'
  - '3.11'
  - '3.12'
  - '3.13'
  os:
  - Windows
  - Linux
  - macOS
```

## When to Use

- Repository has accumulated multiple hidden folders over time
- Multiple AI/agent configuration directories exist (`.agent-os/`, `.ai/`, `.claude/`)
- Symlinks point to non-existent targets
- Unclear which configuration is authoritative
- Preparing for repository restructure or cleanup
- After inheriting or forking a repository
- Before establishing new folder standards

## Audit Process

### Step 1: Inventory All Hidden Folders

List all hidden directories at the repository root.

```bash
# List all hidden directories (excluding .git)
find . -maxdepth 1 -type d -name ".*" ! -name ".git" | sort

# With sizes
du -sh .*/ 2>/dev/null | grep -v "^0" | sort -hr

# Include symlinks
find . -maxdepth 1 \( -type d -o -type l \) -name ".*" ! -name ".git" | sort
```

### Step 2: Check Git Tracking Status

Determine which hidden folders are tracked, ignored, or untracked.

```bash
# Check if folder is tracked
git ls-files --error-unmatch .folder/ 2>/dev/null && echo "TRACKED" || echo "NOT TRACKED"

# Check if folder is ignored
git check-ignore -v .folder/ 2>/dev/null && echo "IGNORED" || echo "NOT IGNORED"

# List all tracked hidden files
git ls-files | grep "^\." | cut -d'/' -f1 | sort -u

# List all gitignored hidden folders
git status --porcelain --ignored | grep "^!!" | grep "^\./\." | cut -d'/' -f2 | sort -u
```

### Step 3: Analyze Content Overlap

Check for duplicate or overlapping content between hidden folders.

```bash
# Compare agent configurations
diff -rq .agent-os/agents/ .claude/agents/ 2>/dev/null

# Find duplicate files by name
find .agent-os .ai .claude -name "*.md" -type f 2>/dev/null | xargs -I {} basename {} | sort | uniq -d

# Find duplicate files by content (MD5)
find .agent-os .ai .claude -type f 2>/dev/null | xargs md5sum 2>/dev/null | sort | uniq -w32 -d

# Compare directory structures
diff <(find .agent-os -type f | sed 's|.agent-os/||' | sort) \
     <(find .claude -type f | sed 's|.claude/||' | sort) 2>/dev/null
```

### Step 4: Identify Authoritative Source

Determine which folder should be the single source of truth.

**Criteria for Authoritative Source:**
1. **Git tracking** - Tracked folders are more likely authoritative
2. **Recency** - Check last modification dates
3. **Completeness** - More complete configuration wins
4. **Active use** - Referenced in CI/CD, scripts, documentation
5. **Tool requirements** - Some tools require specific folder names

```bash
# Check modification times
stat -c '%Y %n' .*/ 2>/dev/null | sort -rn | head -10

# Check for references in scripts and CI
grep -r "\.agent-os" --include="*.sh" --include="*.yml" --include="*.yaml" .
grep -r "\.claude" --include="*.sh" --include="*.yml" --include="*.yaml" .

# Check symlink targets
find . -maxdepth 2 -type l -exec ls -la {} \;
```

### Step 5: Plan Consolidation

Create a migration plan based on analysis.

**Migration Checklist:**
- [ ] Identify target folder structure
- [ ] List files to migrate
- [ ] Identify files to delete
- [ ] Update references in code/scripts
- [ ] Update .gitignore
- [ ] Test after migration

## Common Hidden Folders Reference

Based on actual cleanup sessions, this table provides verified recommendations.

| Folder | Purpose | Action | Notes |
|--------|---------|--------|-------|
| `.claude/` | Claude Code configuration, agents, skills, docs | **KEEP** | Authoritative for AI tools |
| `.claude-flow/` | Runtime data, state, coordination | **KEEP** | Add to .gitignore |
| `.githooks/` | Git hooks | **KEEP** | Standard location |
| `.github/` | GitHub workflows, templates | **KEEP** | Required by GitHub |
| `.git/` | Git repository data | **NEVER TOUCH** | - |
| `.gitignore` | Git ignore patterns | **KEEP** | Update as needed |
| `.vscode/` | VS Code settings | **KEEP** | Team settings if tracked |
| `.idea/` | JetBrains IDE settings | **KEEP** | Or add to .gitignore |
| `.env` | Environment variables | **KEEP** | Must be in .gitignore |
| `.agent-os/` | Legacy agent OS configuration | **CONSOLIDATE** | Merge into `.claude/` |
| `.ai/` | Legacy AI configuration | **CONSOLIDATE** | Merge into `.claude/` |
| `.drcode/` | External tool (Dr. Code) config | **DELETE** | Legacy AI config, confirmed deletable |
| `.slash-commands/` | Command registry | **CONSOLIDATE** | Move to `.claude/docs/commands/` |
| `.git-commands/` | Git helper scripts | **CONSOLIDATE** | Move to `scripts/git/` |
| `.benchmarks/` | Benchmark data | **DELETE** | Usually empty, delete if so |
| `benchmarks/` | Benchmark data and reports | **SPLIT** | Move fixtures to tests/fixtures/, gitignore reports/results |
| `.agent-runtime/` | Dead symlinks, orphaned state | **DELETE** | After verifying dead links |
| `.common/` | Orphaned utilities | **DELETE** | Relocate useful scripts first |
| `.specify/` | Stale specification templates | **DELETE** | Migrate to `specs/templates/` |
| `.pytest_cache/` | Pytest cache | **DELETE** | Regenerated automatically |
| `.ruff_cache/` | Ruff linter cache | **DELETE** | Regenerated automatically |
| `.mypy_cache/` | MyPy type checker cache | **DELETE** | Regenerated automatically |
| `.coordination/` | Multi-agent coordination | **MIGRATE** | Move to `.claude-flow/` |
| `.session/` | Session state files | **MIGRATE** | Move to `.claude-flow/` |

## Related Directory Patterns

Some non-hidden directories follow similar cleanup/consolidation patterns.

### specs/archive/

Standard location for completed specification plans.

```bash
# Archive completed plans (check YAML frontmatter for status: completed)
mkdir -p specs/archive
git mv specs/modules/<completed-plan>.md specs/archive/
```

### benchmarks/

Benchmark directories typically contain mixed content requiring separation.

| Subdirectory | Content | Action |
|--------------|---------|--------|
| `legacy_projects/` | Reference test data (*.dat, *.csv) | Move to `tests/fixtures/` |
| `reports/` | Timestamped HTML reports | Add to .gitignore |
| `results/` | Timestamped CSV/JSON | Add to .gitignore |
| Root `*.py` files | Benchmark scripts | Keep tracked |

```bash
# Separate fixtures from generated outputs
mkdir -p tests/fixtures/orcaflex
git mv benchmarks/legacy_projects/* tests/fixtures/orcaflex/
git rm -r --cached benchmarks/reports benchmarks/results
echo "benchmarks/reports/" >> .gitignore
echo "benchmarks/results/" >> .gitignore
```

## Consolidation Commands

### Migrate .agent-os to .claude

```bash
# Backup first
cp -r .agent-os .agent-os.backup

# Migrate agents
mkdir -p .claude/agents
cp -r .agent-os/agents/* .claude/agents/ 2>/dev/null

# Migrate standards (if applicable)
mkdir -p .claude/standards
cp -r .agent-os/standards/* .claude/standards/ 2>/dev/null

# Update git tracking
git rm -r --cached .agent-os/ 2>/dev/null
git add .claude/

# Remove old folder after verification
rm -rf .agent-os
rm -rf .agent-os.backup  # After confirming migration
```

### Migrate .ai to .claude

```bash
# Backup first
cp -r .ai .ai.backup

# Migrate prompts to skills
mkdir -p .claude/skills/prompts
cp -r .ai/prompts/* .claude/skills/prompts/ 2>/dev/null

# Migrate config
cp .ai/config.* .claude/ 2>/dev/null

# Cleanup
git rm -r --cached .ai/ 2>/dev/null
rm -rf .ai
```

### Clean Dead Symlinks

```bash
# Find broken symlinks
find . -maxdepth 2 -type l ! -exec test -e {} \; -print

# Remove broken symlinks
find . -maxdepth 2 -type l ! -exec test -e {} \; -delete

# Remove specific dead symlink folder
rm -rf .agent-runtime
```

### Consolidate Runtime Directories

```bash
# Create standard runtime directory
mkdir -p .claude-flow/state
mkdir -p .claude-flow/cache
mkdir -p .claude-flow/logs

# Migrate coordination data
mv .coordination/* .claude-flow/state/ 2>/dev/null
mv .session/* .claude-flow/state/ 2>/dev/null

# Remove old directories
rm -rf .coordination .session
```

### Update .gitignore

Add these patterns after consolidation:

```gitignore
# Runtime and state (not tracked)
.claude-flow/
.coordination/
.session/

# Legacy folders (prevent re-creation)
.agent-os/
.ai/
.agent-runtime/

# Cache directories
.pytest_cache/
.ruff_cache/
.mypy_cache/
__pycache__/
```

## Audit Checklist

### Pre-Audit
- [ ] Working directory is clean (`git status`)
- [ ] Create backup branch: `git checkout -b backup/pre-hidden-audit`
- [ ] Document current state: `ls -la .*/ > hidden-folders-before.txt`

### Discovery Phase
- [ ] List all hidden folders at root level
- [ ] Record size of each hidden folder
- [ ] Identify symlinks and their targets
- [ ] Check git tracking status for each

### Analysis Phase
- [ ] Identify duplicate configurations
- [ ] Find broken symlinks
- [ ] Determine authoritative source for each config type
- [ ] Check for active usage in scripts/CI

### Planning Phase
- [ ] Create target folder structure diagram
- [ ] List files to migrate with source/destination
- [ ] List files/folders to delete
- [ ] Identify scripts/references to update

### Execution Phase
- [ ] Backup folders before migration
- [ ] Migrate content to authoritative locations
- [ ] Update git tracking (`git rm --cached`, `git add`)
- [ ] Remove legacy folders
- [ ] Update .gitignore

### Verification Phase
- [ ] Run tests to ensure nothing broke
- [ ] Verify symlinks work (if any remain)
- [ ] Confirm scripts still function
- [ ] Check CI/CD pipelines
- [ ] Commit with descriptive message

### Documentation Phase
- [ ] Update README if folder structure changed
- [ ] Document new standard in CLAUDE.md or equivalent
- [ ] Remove references to legacy folders in docs

## Verification Commands

Use these commands to verify the final state after audit and cleanup.

### Verify Hidden Folder State

```bash
# List remaining hidden folders (should be minimal)
echo "=== Remaining Hidden Folders ==="
find . -maxdepth 1 -type d -name ".*" ! -name ".git" | sort

# Expected remaining folders:
# .claude/       - AI configuration (authoritative)
# .claude-flow/  - Runtime data (gitignored)
# .github/       - GitHub workflows
# .githooks/     - Git hooks
# .vscode/       - VS Code settings (if tracked)

# Verify no legacy folders remain
echo "=== Checking for Legacy Folders ==="
for dir in .agent-os .ai .drcode .slash-commands .git-commands .benchmarks .agent-runtime .common .specify; do
  if [ -d "$dir" ]; then
    echo "WARNING: $dir still exists!"
  fi
done
echo "Check complete."
```

### Verify Consolidation Targets

```bash
# Verify .claude/ structure
echo "=== .claude/ Structure ==="
ls -la .claude/

# Verify scripts/git/ exists if .git-commands was consolidated
echo "=== scripts/git/ ==="
ls -la scripts/git/ 2>/dev/null || echo "scripts/git/ does not exist"

# Verify .claude/docs/commands/ if .slash-commands was consolidated
echo "=== .claude/docs/commands/ ==="
ls -la .claude/docs/commands/ 2>/dev/null || echo ".claude/docs/commands/ does not exist"

# Verify specs/archive exists for completed plans
echo "=== specs/archive/ ==="
ls -la specs/archive/ 2>/dev/null || echo "specs/archive/ does not exist"

# Verify benchmark structure
echo "=== benchmarks/ Structure ==="
ls -la benchmarks/ 2>/dev/null || echo "benchmarks/ does not exist"

# Check for legacy_projects in benchmarks (should be moved)
if [ -d "benchmarks/legacy_projects" ]; then
  echo "[WARN] benchmarks/legacy_projects/ should be moved to tests/fixtures/"
fi
```

### Verify Git Status

```bash
# Check for untracked hidden folders
echo "=== Untracked Hidden Folders ==="
git status --porcelain | grep "^??" | grep "^\./\." || echo "None found"

# Verify .gitignore includes runtime folders
echo "=== .gitignore Hidden Folder Entries ==="
grep -E "^\.(claude-flow|coordination|session)" .gitignore || echo "No runtime folders in .gitignore"

# Count tracked files in .claude/
echo "=== .claude/ Tracked Files ==="
git ls-files .claude/ | wc -l
```

### Final State Checklist

```bash
# Run all verification checks
echo "=== Final State Verification ==="

# 1. Only expected hidden folders exist
hidden_count=$(find . -maxdepth 1 -type d -name ".*" ! -name ".git" ! -name ".claude" ! -name ".claude-flow" ! -name ".github" ! -name ".githooks" ! -name ".vscode" | wc -l)
if [ "$hidden_count" -eq 0 ]; then
  echo "[OK] No unexpected hidden folders"
else
  echo "[WARN] $hidden_count unexpected hidden folders found"
fi

# 2. Legacy folders are gone
legacy_count=0
for dir in .agent-os .ai .drcode .slash-commands .git-commands .benchmarks; do
  [ -d "$dir" ] && legacy_count=$((legacy_count + 1))
done
if [ "$legacy_count" -eq 0 ]; then
  echo "[OK] All legacy folders removed"
else
  echo "[WARN] $legacy_count legacy folders remain"
fi

# 3. .claude/ has expected subdirectories
for subdir in agents docs skills; do
  if [ -d ".claude/$subdir" ]; then
    echo "[OK] .claude/$subdir exists"
  else
    echo "[WARN] .claude/$subdir missing"
  fi
done

# 4. Git working directory is clean
if git diff --quiet 2>/dev/null; then
  echo "[OK] Git working directory is clean"
else
  echo "[INFO] Git has uncommitted changes"
fi
```

## Best Practices

1. **Always backup before deleting** - Create a backup branch or copy
2. **Use git rm for tracked folders** - Preserves history
3. **Check symlink targets before deleting** - May need to update references
4. **Update .gitignore first** - Prevents accidental re-tracking
5. **Test after consolidation** - Ensure nothing broke
6. **Commit in logical chunks** - Separate migration from cleanup
7. **Document the changes** - Future maintainers will thank you

## Related Skills

- [repo-cleanup](../repo-cleanup/SKILL.md) - General repository cleanup
- [module-based-refactor](../module-based-refactor/SKILL.md) - For source code restructuring
- [session-start-routine](../session-start-routine/SKILL.md) - Session initialization

## References

- Git ls-files documentation: https://git-scm.com/docs/git-ls-files
- Git check-ignore documentation: https://git-scm.com/docs/git-check-ignore
- Symbolic links in Git: https://git-scm.com/book/en/v2/Git-Internals-Git-References

---

## Version History

- **1.2.0** (2026-01-20): Added Related Directory Patterns section
  - Added benchmarks/ entry to reference table (SPLIT action)
  - Added Related Directory Patterns section for non-hidden directories
  - Added specs/archive/ as standard location for completed plans
  - Added benchmarks/ separation pattern (fixtures vs generated outputs)
  - Updated verification commands for new patterns
- **1.1.0** (2026-01-20): Updated reference table and added verification commands
  - Updated Common Hidden Folders Reference table with verified recommendations
  - Added .drcode/ as DELETE (confirmed legacy AI config)
  - Added .slash-commands/ as CONSOLIDATE to .claude/docs/commands/
  - Added .git-commands/ as CONSOLIDATE to scripts/git/
  - Added .benchmarks/ as DELETE (usually empty)
  - Added .githooks/ as KEEP (standard location)
  - Added Verification Commands section with:
    - Verify Hidden Folder State commands
    - Verify Consolidation Targets commands
    - Verify Git Status commands
    - Final State Checklist script
  - Added Notes column to reference table for additional context
- **1.0.0** (2025-01-20): Initial release based on digitalmodel repository hidden folder audit session
