---
name: repo-cleanup
description: Systematic cleanup of repository clutter including build artifacts, duplicates, temp files, and consolidation of scattered directories. Use for repository maintenance, artifact removal, directory consolidation, and gitignore updates.
version: 2.2.0
updated: 2026-01-20
category: meta
triggers:
- repository cleanup
- artifact removal
- temp file cleanup
- duplicate files
- build artifacts
- cache cleanup
- directory consolidation
- gitignore update
- log file cleanup
- untracked files
---

# Repository Cleanup Skill

Quick cleanup of repository clutter including build artifacts, duplicates, temp files, and consolidation of scattered directories into standard locations.

## Version Metadata

```yaml
version: 2.2.0
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

- Repository has accumulated build artifacts and temp files
- Multiple agent/coordination directories scattered in root
- Log files and coverage reports cluttering the workspace
- Need to consolidate prototype code and test outputs
- Preparing for a clean commit or release
- After major refactoring work

## Cleanup Categories

### 1. Build Artifacts

Files generated during build/install processes that should not be tracked.

| Pattern | Description | Location |
|---------|-------------|----------|
| `*.egg-info/` | Python package metadata | `src/*/` |
| `__pycache__/` | Python bytecode cache | Throughout |
| `.pytest_cache/` | Pytest cache | Root and test dirs |
| `build/` | Build output directory | Root |
| `dist/` | Distribution packages | Root |
| `*.pyc` | Compiled Python files | Throughout |
| `*.pyo` | Optimized Python files | Throughout |

**Cleanup commands:**
```bash
# Find all build artifacts
find . -type d -name "__pycache__" -o -name "*.egg-info" -o -name ".pytest_cache"

# Remove Python cache (safe - regenerated automatically)
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
```

### 2. Log Files

Generated log files that accumulate during development and testing.

| Pattern | Description |
|---------|-------------|
| `*.log` | General log files |
| `*LogFile.txt` | OrcaFlex log files |
| `*.log.*` | Rotated log files |
| `debug.log` | Debug output |

**Cleanup commands:**
```bash
# Find log files
find . -name "*.log" -o -name "*LogFile.txt"

# Remove log files (verify first)
find . -name "*.log" -type f -delete
find . -name "*LogFile.txt" -type f -delete
```

### 3. Temp Files

Temporary files created during processing or editing.

| Pattern | Description |
|---------|-------------|
| `*.tmp` | Temporary files |
| `.temp/` | Temp directories |
| `cache/` | Cache directories |
| `*.bak` | Backup files |
| `*.swp` | Vim swap files |
| `*~` | Editor backup files |

**Cleanup commands:**
```bash
# Find temp files
find . -name "*.tmp" -o -name "*.bak" -o -name "*.swp" -o -name "*~"

# Remove temp files
find . \( -name "*.tmp" -o -name "*.bak" -o -name "*.swp" -o -name "*~" \) -type f -delete
```

### 4. Coverage Reports

Test coverage artifacts that can be regenerated.

| Pattern | Description |
|---------|-------------|
| `htmlcov/` | HTML coverage reports |
| `.coverage` | Coverage data file |
| `.coverage.*` | Parallel coverage data |
| `coverage.xml` | XML coverage report |

**Cleanup commands:**
```bash
# Remove coverage artifacts
rm -rf htmlcov/
rm -f .coverage .coverage.* coverage.xml
```

### 5. IDE Artifacts

Editor and IDE generated files.

| Pattern | Description |
|---------|-------------|
| `.idea/` | PyCharm/IntelliJ |
| `.vscode/` | VS Code (keep settings.json) |
| `*.code-workspace` | VS Code workspaces |
| `.spyproject/` | Spyder IDE |

**Note:** Some IDE settings may be intentionally tracked. Check `.gitignore` first.

### 6. Benchmark Artifacts

Benchmark directories often contain mixed content that needs separation.

| Pattern | Description | Action |
|---------|-------------|--------|
| `benchmarks/reports/` | Timestamped HTML reports | Add to .gitignore |
| `benchmarks/results/` | Timestamped CSV/JSON | Add to .gitignore |
| `benchmarks/legacy_projects/` | Reference test data | Move to tests/fixtures/ |
| `benchmarks/*.py` | Benchmark scripts | Keep tracked |

**Cleanup commands:**
```bash
# Move test fixtures to proper location
mkdir -p tests/fixtures/orcaflex
git mv benchmarks/legacy_projects/* tests/fixtures/orcaflex/

# Untrack generated outputs
git rm -r --cached benchmarks/reports benchmarks/results

# Add to .gitignore
echo "benchmarks/reports/" >> .gitignore
echo "benchmarks/results/" >> .gitignore
```

## Consolidation Patterns

### Agent Directories

Multiple agent-related directories should consolidate to `.claude/agents/`.

**Before:**
```
root/
├── agents/
├── .agents/
├── agent_configs/
└── .agent-os/
```

**After:**
```
.claude/
└── agents/
    ├── core/
    ├── devops/
    └── specialized/
```

**Commands:**
```bash
# Find scattered agent directories
find . -maxdepth 2 -type d -name "*agent*"

# Move to consolidated location
git mv agents/* .claude/agents/ 2>/dev/null
git mv .agents/* .claude/agents/ 2>/dev/null
rm -rf agents .agents agent_configs
```

### Runtime/Coordination Data

Runtime data should go to `.claude-flow/` (gitignored).

**Move to `.claude-flow/`:**
- Session state files
- Coordination lock files
- Runtime cache
- Worker state

**Commands:**
```bash
# Create runtime directory
mkdir -p .claude-flow/state
mkdir -p .claude-flow/cache

# Move runtime files (don't use git mv - these are untracked)
mv .coordination/* .claude-flow/state/ 2>/dev/null
mv .session/* .claude-flow/state/ 2>/dev/null
```

### Prototype Code

Prototype and experimental code should go to `examples/prototypes/`.

**Commands:**
```bash
mkdir -p examples/prototypes
git mv prototype_*.py examples/prototypes/
git mv experimental/ examples/prototypes/
```

### Test Outputs

Test output files should go to `tests/outputs/` (gitignored).

**Commands:**
```bash
mkdir -p tests/outputs
mv tests/*.html tests/outputs/
mv tests/*.json tests/outputs/
mv tests/test_results/ tests/outputs/
```

### Plan Files

Completed specification plans should be archived.

**Pattern:**
- Active plans: `specs/modules/<plan>.md`
- Completed plans: `specs/archive/<plan>.md`

**Commands:**
```bash
# Archive completed plan (check status: completed in YAML frontmatter)
mkdir -p specs/archive
git mv specs/modules/<completed-plan>.md specs/archive/
```

## Hidden Folder Cleanup

Legacy AI and agent hidden folders often accumulate during development. These need review and consolidation.

### Common Hidden Folders

| Folder | Description | Action |
|--------|-------------|--------|
| `.agent-os/` | Legacy agent OS framework | Consolidate to `.claude/` |
| `.ai/` | Legacy AI configuration | Consolidate to `.claude/` |
| `.agent-runtime/` | Runtime symlinks (often dead) | Delete if dead links |
| `.common/` | Orphaned utility scripts | Delete or relocate to `scripts/` |
| `.specify/` | Stale specification templates | Delete if unused |
| `.drcode/` | External tool config (Dr. Code) | Keep if actively used |
| `.slash-commands/` | Command registry | Keep |

### Discovery Commands

```bash
# List all hidden directories with sizes
du -sh .*/ 2>/dev/null | grep -v "^\./\.git"

# Find dead symlinks in hidden folders
find .agent-runtime -type l ! -exec test -e {} \; -print 2>/dev/null

# Count files in each hidden directory
for dir in .claude .agent-os .ai .common .specify; do
  if [ -d "$dir" ]; then
    count=$(find "$dir" -type f | wc -l)
    echo "$dir: $count files"
  fi
done
```

### Cleanup Commands

```bash
# Remove dead symlink directories
rm -rf .agent-runtime/

# Remove stale template directories
rm -rf .specify/

# Remove orphaned utilities (after relocating useful scripts)
rm -rf .common/

# Consolidate .agent-os to .claude
git mv .agent-os/agents/* .claude/agents/ 2>/dev/null
git mv .agent-os/skills/* .claude/skills/ 2>/dev/null
git mv .agent-os/docs/* .claude/docs/ 2>/dev/null
rm -rf .agent-os/

# Consolidate .ai to .claude
git mv .ai/config/* .claude/config/ 2>/dev/null
git mv .ai/prompts/* .claude/prompts/ 2>/dev/null
rm -rf .ai/
```

## Consolidation Merge Strategies

When merging folders, file conflicts are common. Use these strategies to preserve important content while eliminating duplicates.

### Conflict Resolution Patterns

| Conflict Type | Strategy | Example |
|--------------|----------|---------|
| Same filename | Rename with suffix | `README.md` -> `README-legacy.md` |
| Similar content | Use subdirectory | `commands/` -> `commands/legacy-scripts/` |
| Unique content | Preserve in dedicated folder | Keep `implementation-history/` |
| Clear duplicates | Delete after verification | Remove exact copies |

### Merge Commands

```bash
# Rename conflicting files before merge
mv .agent-os/README.md .agent-os/README-legacy.md

# Create legacy subdirectory for scripts
mkdir -p .claude/commands/legacy-scripts
git mv .agent-os/commands/* .claude/commands/legacy-scripts/

# Preserve unique historical content
git mv .agent-os/implementation-history/ .claude/docs/implementation-history/

# Find and remove exact duplicates (verify first)
md5sum .claude/agents/*.md .agent-os/agents/*.md | sort | uniq -w32 -d
```

### Pre-Merge Checklist

- [ ] Compare file lists between source and target
- [ ] Identify naming conflicts
- [ ] Decide rename vs. subdirectory strategy
- [ ] Document unique content to preserve
- [ ] Verify duplicates before deletion

## File Count Verification

Track consolidation progress with file counts to ensure nothing is lost.

### Progress Tracking Commands

```bash
# Count tracked files in each hidden folder
for dir in .claude .agent-os .ai; do
  count=$(git ls-files "$dir" 2>/dev/null | wc -l)
  echo "$dir: $count files"
done

# Count all files (tracked + untracked)
for dir in .claude .agent-os .ai .common .specify; do
  if [ -d "$dir" ]; then
    tracked=$(git ls-files "$dir" 2>/dev/null | wc -l)
    total=$(find "$dir" -type f | wc -l)
    echo "$dir: $tracked tracked, $total total"
  fi
done

# Before/after comparison
echo "=== Before Consolidation ===" > consolidation-log.txt
for dir in .claude .agent-os .ai; do
  count=$(git ls-files "$dir" 2>/dev/null | wc -l)
  echo "$dir: $count files" >> consolidation-log.txt
done
```

### Verification After Merge

```bash
# Verify no files were lost
expected_count=150  # Set to sum of source folders
actual_count=$(git ls-files .claude | wc -l)
echo "Expected: $expected_count, Actual: $actual_count"

# List any untracked files that might have been missed
git status --porcelain | grep "^??" | grep -E "^\?\? \.(claude|agent-os|ai)/"
```

## Discovery Commands

### List Untracked Files

```bash
# All untracked files
git status --porcelain | grep "^??"

# Untracked files with size
git status --porcelain | grep "^??" | cut -c4- | xargs -I {} sh -c 'du -h "{}" 2>/dev/null'
```

### Find Large Files

```bash
# Files larger than 1MB
find . -type f -size +1M -exec ls -lh {} \;

# Files larger than 10MB
find . -type f -size +10M -exec ls -lh {} \;

# Largest files in repo
find . -type f -exec du -h {} + 2>/dev/null | sort -rh | head -20
```

### Find Duplicates

```bash
# Find duplicate markdown files in agent directories
find . -name "*.md" -path "*/agents/*" -type f

# Find files with same name
find . -type f -name "*.py" | xargs -I {} basename {} | sort | uniq -d

# Find duplicate by content (requires md5sum)
find . -type f -exec md5sum {} + | sort | uniq -w32 -d
```

### Find Hidden Directories

```bash
# List all hidden directories
find . -maxdepth 1 -type d -name ".*" | grep -v "^\./\.git$"

# Hidden directories with sizes
du -sh .*/
```

## Safe Deletion Commands

### For Tracked Files (Use git rm)

```bash
# Remove tracked file
git rm path/to/file

# Remove tracked directory
git rm -r path/to/directory

# Remove from git but keep local copy
git rm --cached path/to/file
```

### For Untracked Files (Use rm)

```bash
# Remove untracked file
rm path/to/file

# Remove untracked directory
rm -rf path/to/directory

# Interactive removal (safer)
rm -i path/to/file
```

### Dry Run First

```bash
# Preview what would be deleted
git clean -n -d

# Preview including ignored files
git clean -n -d -x
```

## Gitignore Updates

Add these entries to `.gitignore` after cleanup:

```gitignore
# Build artifacts
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
*.egg
build/
dist/
.eggs/

# Test artifacts
.pytest_cache/
.coverage
.coverage.*
htmlcov/
coverage.xml
*.cover

# IDE
.idea/
.vscode/
*.code-workspace
.spyproject/

# Logs
*.log
*LogFile.txt

# Temp files
*.tmp
*.bak
*.swp
*~
.temp/
cache/

# Runtime data (claude-flow)
.claude-flow/
.coordination/
.session/

# Benchmark generated outputs
benchmarks/reports/
benchmarks/results/

# Test outputs
tests/outputs/
tests/*.html
tests/*.json

# Large binary files
*.sim
*.dat
*.bin
```

## Cleanup Checklist

### Pre-Cleanup
- [ ] Git working directory status documented
- [ ] Important untracked files identified
- [ ] Backup created if needed

### Build Artifacts
- [ ] `__pycache__/` directories removed
- [ ] `*.egg-info/` directories removed
- [ ] `.pytest_cache/` removed
- [ ] `build/` and `dist/` removed if present

### Log Files
- [ ] `*.log` files removed or archived
- [ ] `*LogFile.txt` files removed
- [ ] Rotated logs cleaned

### Temp Files
- [ ] `*.tmp` files removed
- [ ] Editor backup files removed
- [ ] Cache directories cleaned

### Coverage Reports
- [ ] `htmlcov/` removed
- [ ] `.coverage` files removed

### Consolidation
- [ ] Agent directories consolidated to `.claude/agents/`
- [ ] Runtime data moved to `.claude-flow/`
- [ ] Prototypes moved to `examples/prototypes/`
- [ ] Test outputs moved to `tests/outputs/`
- [ ] Benchmark test fixtures moved to `tests/fixtures/`
- [ ] Benchmark generated outputs untracked and gitignored
- [ ] Completed plan files archived to `specs/archive/`

### Hidden Folder Review
- [ ] `.agent-os/` reviewed and consolidated
- [ ] `.ai/` reviewed and consolidated
- [ ] `.agent-runtime/` deleted if dead symlinks
- [ ] `.common/` relocated or deleted
- [ ] `.specify/` deleted if stale

### Post-Cleanup
- [ ] `.gitignore` updated with new patterns
- [ ] `git status` shows clean or expected state
- [ ] Tests still pass after cleanup

## Final Cleanup Checklist

Based on actual cleanup sessions, these folders have been verified for removal or consolidation.

### Folders to DELETE (Confirmed Safe)

| Folder | Reason | Verification |
|--------|--------|--------------|
| `.drcode/` | Legacy AI config (Dr. Code) | Not referenced in any scripts or CI |
| `.benchmarks/` | Empty benchmark folder | `ls .benchmarks/` returns empty or missing |
| `.agent-runtime/` | Dead symlinks only | `find .agent-runtime -type l ! -exec test -e {} \;` |
| `.common/` | Orphaned utilities | No imports reference this folder |
| `.specify/` | Stale specification templates | Specs moved to `specs/templates/` |

### Folders to CONSOLIDATE

| Source | Destination | Command |
|--------|-------------|---------|
| `.slash-commands/` | `.claude/docs/commands/` | `git mv .slash-commands/* .claude/docs/commands/` |
| `.git-commands/` | `scripts/git/` | `git mv .git-commands/* scripts/git/` |
| `.agent-os/` | `.claude/` | See module-based-refactor skill |
| `.ai/` | `.claude/` | See module-based-refactor skill |

### Folders to KEEP

| Folder | Reason |
|--------|--------|
| `.githooks/` | Standard location for git hooks |
| `.github/` | GitHub workflows and templates |
| `.claude/` | Authoritative AI configuration |
| `.vscode/` | Team VS Code settings (if tracked) |

### Cleanup Commands

```bash
# Delete legacy config folders
rm -rf .drcode/
rm -rf .benchmarks/

# Consolidate slash-commands to docs
mkdir -p .claude/docs/commands
git mv .slash-commands/* .claude/docs/commands/ 2>/dev/null
rm -rf .slash-commands/

# Consolidate git-commands to scripts
mkdir -p scripts/git
git mv .git-commands/* scripts/git/ 2>/dev/null
rm -rf .git-commands/

# Verify cleanup
ls -la .* 2>/dev/null | grep "^d"
```

## README Update Checklist

After cleanup, update the README to reflect the new structure.

### Structure Section Updates

- [ ] Update directory tree to show new structure
- [ ] Remove references to deleted folders
- [ ] Add `.claude/` folder description
- [ ] Document `scripts/git/` consolidation
- [ ] Note module-based architecture in src/

### Example README Structure Section

```markdown
## Repository Structure

project/
├── .claude/              # AI configuration and documentation
│   ├── agents/           # Agent definitions
│   ├── docs/             # Reference documentation
│   ├── skills/           # Skill definitions
│   └── settings.json     # Claude Code settings
├── .githooks/            # Git hooks
├── scripts/              # Utility scripts
│   └── git/              # Git-related scripts
├── src/<pkg>/modules/    # Source modules (5-layer architecture)
├── tests/modules/        # Test modules
├── specs/modules/        # Specification modules
├── docs/modules/         # Documentation modules
└── examples/modules/     # Example modules
```

### References to Remove

- [ ] `.agent-os/` - consolidated to `.claude/`
- [ ] `.ai/` - consolidated to `.claude/`
- [ ] `.drcode/` - deleted (legacy)
- [ ] `.slash-commands/` - consolidated to `.claude/docs/commands/`
- [ ] `.git-commands/` - consolidated to `scripts/git/`

## Best Practices

1. **Always verify before deleting** - Use `find` and `ls` before `rm`
2. **Use git rm for tracked files** - Preserves history and staging
3. **Update .gitignore first** - Prevents re-adding cleaned files
4. **Commit cleanup separately** - Keep cleanup commits distinct from feature work
5. **Document what was removed** - Use clear commit messages
6. **Check file sizes** - Large files may need special handling (Git LFS)

## Related Skills

- [module-based-refactor](../module-based-refactor/SKILL.md) - For restructuring after cleanup
- [session-start-routine](../session-start-routine/SKILL.md) - Session initialization

## References

- Git clean documentation: https://git-scm.com/docs/git-clean
- Git rm documentation: https://git-scm.com/docs/git-rm
- Gitignore patterns: https://git-scm.com/docs/gitignore

---

## Version History

- **2.2.0** (2026-01-20): Added Benchmark Cleanup and Plan File Archival patterns
  - Added Benchmark Artifacts section for handling benchmark directories
  - Added Plan Files section for archiving completed specifications
  - Added benchmark patterns to .gitignore recommendations
  - Updated checklist with benchmark and plan archival items
- **2.1.0** (2026-01-20): Added Final Cleanup Checklist and README Update Checklist
  - Added Final Cleanup Checklist with verified DELETE/CONSOLIDATE/KEEP tables
  - Confirmed .drcode/ as safe to delete (legacy AI config)
  - Added .slash-commands/ consolidation to .claude/docs/commands/
  - Added .git-commands/ consolidation to scripts/git/
  - Added .benchmarks/ as safe to delete if empty
  - Added README Update Checklist for structure documentation
  - Added example README structure section template
  - Added references to remove checklist
- **2.0.0** (2026-01-20): Major update with hidden folder cleanup learnings
  - Added Hidden Folder Cleanup section with legacy AI folder patterns
  - Added Consolidation Merge Strategies for conflict resolution
  - Added File Count Verification for tracking consolidation progress
  - Updated Cleanup Checklist with hidden folder review items
  - Documented patterns for .agent-os, .ai, .agent-runtime, .common, .specify, .drcode, .slash-commands
- **1.0.0** (2025-01-20): Initial release based on digitalmodel repository cleanup session
