---
name: update-framework
description: |
  Samuel version update workflow. Use when upgrading to a new Samuel version,
  migrating framework configurations, or applying upstream template changes
  while preserving local customizations.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

## When to Use

| Trigger | Action |
|---------|--------|
| New version announced | Full update |
| Want new language/framework skills | Selective update |
| Monthly maintenance | Check for updates |
| New team member needs latest | Verify version parity |
| Security advisory | Urgent update |

---

## Prerequisites

- [ ] Current project has CLAUDE.md installed
- [ ] Git repository (for backup/diff capabilities)
- [ ] Internet access to clone latest version
- [ ] No uncommitted changes (clean working directory recommended)

---

## Process Overview

```
1. Check Current Version
   └── Read CLAUDE.md version
        ↓
2. Fetch Latest Version
   └── Clone/download latest
        ↓
3. Compare Versions
   └── What's new? Breaking changes?
        ↓
4. Identify Customizations
   └── What have you modified?
        ↓
5. Plan Update Strategy
   └── Full replace vs. selective merge
        ↓
6. Execute Update
   └── Backup, copy, merge
        ↓
7. Verify Update
   └── Check files, validate
```

---

## Phase 1: Assess Current Installation

### Version Detection

```bash
# Find current version in CLAUDE.md
grep "Current Version" CLAUDE.md

# Check when CLAUDE.md was last modified
ls -la CLAUDE.md

# List installed skills (language guides and framework skills)
ls .claude/skills/

# List installed workflows
ls .claude/skills/
```

### AI Will Check

1. **Current CLAUDE.md version** (in "Version & Changelog" section)
2. **Which .claude/ files exist** (guides, workflows)
3. **Which files appear customized** (vs. template defaults)
4. **Project-specific files** to preserve:
   - `CLAUDE.md`
   - `CLAUDE.md`
   - `CLAUDE.md`
   - `.claude/memory/*`
   - `.claude/tasks/*`

### Customization Detection

Files that are typically customized:
- CLAUDE.md (custom guardrails, company standards)
- `CLAUDE.md` (always project-specific)
- `CLAUDE.md` (project conventions)
- Any workflow with project-specific modifications

Files that are typically NOT customized:
- Language guide skills (`.claude/skills/*-guide/SKILL.md`)
- Framework skills (`.claude/skills/<framework>/SKILL.md`)
- Standard workflows (unless modified for company process)

---

## Phase 2: Fetch Latest Version

### Method A: Clone Fresh (Recommended)

```bash
# Clone latest version to temporary directory
git clone --depth 1 https://github.com/ar4mirez/samuel.git .ai-update-temp

# Check latest version
grep "Current Version" .ai-update-temp/CLAUDE.md
```

### Method B: If Using Git Subtree

```bash
# Update subtree
git subtree pull --prefix=.ai-template \
    https://github.com/ar4mirez/samuel.git main --squash
```

### Method C: Download ZIP

1. Go to [GitHub Releases](https://github.com/ar4mirez/samuel/releases)
2. Download latest release
3. Extract to temporary directory

---

## Phase 3: Compare Versions

### View Changelog

```bash
# View what's new
cat .ai-update-temp/CHANGELOG.md | head -100

# Compare versions
echo "Current: $(grep 'Current Version' CLAUDE.md)"
echo "Latest:  $(grep 'Current Version' .ai-update-temp/CLAUDE.md)"
```

### AI Will Analyze

1. **New files** - Guides, workflows not in current installation
2. **Modified files** - Changes to existing templates
3. **Deleted files** - Removed from template (rare)
4. **Breaking changes** - Documented in CHANGELOG.md

### Update Summary Format

```markdown
## Update Summary: v1.5.0 → v1.6.0

### New Files (safe to add):
- .claude/skills/new-framework/SKILL.md
- .claude/skills/new-workflow.md

### Modified Files (review recommended):
- CLAUDE.md (guardrails updated)
- .claude/skills/code-review.md (new checks)

### Your Customizations (will preserve):
- CLAUDE.md (project-specific)
- CLAUDE.md (project-specific)
- .claude/memory/* (decision logs)
- .claude/tasks/* (PRDs and tasks)

### Breaking Changes:
- None (or list if any)
```

---

## Phase 4: Plan Update Strategy

### Strategy A: Full Replace (Recommended for minor updates)

Best when:
- No customizations to CLAUDE.md
- Just want latest guides and workflows
- Version jump is small (e.g., 1.5.0 → 1.6.0)

Process:
1. Backup project-specific files
2. Replace all template files
3. Restore project-specific files

### Strategy B: Selective Merge

Best when:
- Heavy customization to CLAUDE.md
- Only want specific new features
- Version jump is large

Process:
1. Keep current files
2. Add only new guides/workflows
3. Manually review and merge changed files

### Strategy C: New Files Only

Best when:
- Significant CLAUDE.md customization
- Only interested in new language/framework skills
- Don't want to risk breaking customizations

Process:
1. Keep all existing files
2. Copy only skill directories that don't exist yet

### AI Will Recommend

Based on:
- Number and type of customizations
- Size of version jump
- Breaking changes in changelog
- User's stated preferences

---

## Phase 5: Execute Update

### Full Replace Steps

```bash
# 1. Create backup directory
mkdir -p .ai-backup

# 2. Backup CLAUDE.md (if customized)
cp CLAUDE.md .ai-backup/

# 3. Backup project-specific files
cp CLAUDE.md .ai-backup/ 2>/dev/null || true
cp CLAUDE.md .ai-backup/ 2>/dev/null || true
cp CLAUDE.md .ai-backup/ 2>/dev/null || true
cp -r .claude/memory .ai-backup/ 2>/dev/null || true
cp -r .claude/tasks .ai-backup/ 2>/dev/null || true

# 4. Copy new template files
cp .ai-update-temp/CLAUDE.md ./
cp -r .ai-update-temp/.claude ./

# 5. Restore project-specific files
cp .ai-backup/project.md .claude/ 2>/dev/null || true
cp .ai-backup/patterns.md .claude/ 2>/dev/null || true
cp .ai-backup/state.md .claude/ 2>/dev/null || true
cp -r .ai-backup/memory/* .claude/memory/ 2>/dev/null || true
cp -r .ai-backup/tasks/* .claude/tasks/ 2>/dev/null || true

# 6. If you had CLAUDE.md customizations, merge them
# (AI will help with this step)

# 7. Clean up
rm -rf .ai-update-temp
rm -rf .ai-backup
```

### Selective Add Steps

```bash
# Add only new language guide skills
cp -r .ai-update-temp/.claude/skills/new-language-guide/ .claude/skills/

# Add only new framework skills
cp -r .ai-update-temp/.claude/skills/new-framework/ .claude/skills/

# Add only new workflows
cp .ai-update-temp/.claude/skills/new-workflow.md .claude/skills/
```

### Handling CLAUDE.md Customizations

If you've customized CLAUDE.md:

1. **Diff the files**:
   ```bash
   diff CLAUDE.md .ai-update-temp/CLAUDE.md
   ```

2. **Identify your customizations** (usually in specific sections)

3. **AI will help merge**:
   - Take new guardrails from template
   - Preserve your custom additions
   - Update version number

---

## Phase 6: Verify Update

### Verification Checklist

- [ ] CLAUDE.md shows new version number
- [ ] New language/framework skills present
- [ ] New workflows present
- [ ] Project-specific files preserved:
  - [ ] `CLAUDE.md`
  - [ ] `CLAUDE.md`
  - [ ] `CLAUDE.md`
  - [ ] `.claude/memory/*`
  - [ ] `.claude/tasks/*`
- [ ] No merge conflicts in customized sections
- [ ] AI assistant loads CLAUDE.md correctly

### Verification Commands

```bash
# Check version
grep "Current Version" CLAUDE.md

# List all skills (language guides and framework skills)
echo "=== Skills ==="
ls .claude/skills/

echo "=== Workflows ==="
ls .claude/skills/

# Verify project files exist
echo "=== Project Files ==="
ls -la CLAUDE.md CLAUDE.md CLAUDE.md 2>/dev/null

# Count memory files
echo "=== Memory Files ==="
ls .claude/memory/ 2>/dev/null | wc -l
```

### Test AI Loading

Start a new AI session and verify:
1. AI acknowledges CLAUDE.md version
2. Guardrails are applied correctly
3. Workflows are accessible

---

## Usage Examples

### Example 1: Standard Update

**User Request:**
```
@.claude/skills/update-framework/SKILL.md

Update to the latest version of Samuel
```

**AI Will:**
1. Check current version
2. Clone latest version
3. Compare and show what's new
4. Ask about customizations
5. Execute update with backups
6. Verify completion

---

### Example 2: Check for Updates Only

**User Request:**
```
@.claude/skills/update-framework/SKILL.md

Check what's new in the latest version (don't update yet)
```

**AI Will:**
1. Check current version
2. Clone latest version
3. Show detailed comparison
4. List new features and changes
5. NOT make any changes

---

### Example 3: Selective Update

**User Request:**
```
@.claude/skills/update-framework/SKILL.md

I only want to add the new React and Next.js framework skills.
Keep everything else as-is.
```

**AI Will:**
1. Verify those skills don't exist yet
2. Clone latest version
3. Copy only the specified skill directories
4. Clean up temporary files

---

### Example 4: Team Version Sync

**User Request:**
```
@.claude/skills/update-framework/SKILL.md

Verify my installation matches version 1.6.0 that the team is using.
```

**AI Will:**
1. Check current version
2. Compare with 1.6.0 requirements
3. List any missing files
4. Suggest updates if needed

---

### Example 5: Update with Customizations

**User Request:**
```
@.claude/skills/update-framework/SKILL.md

Update to latest. I have custom guardrails in CLAUDE.md that I need to keep.
```

**AI Will:**
1. Check current version
2. Identify customized sections in CLAUDE.md
3. Clone latest version
4. Perform intelligent merge:
   - New template content
   - Your custom guardrails preserved
5. Show diff for review before finalizing

---

## Best Practices

### Before Updating

1. **Commit current state** - Ensure clean git history
2. **Document customizations** - Know what you've changed
3. **Read the changelog** - Understand what's new

### During Update

1. **Always backup** - Never skip the backup step
2. **Review diffs** - Especially for CLAUDE.md changes
3. **Test incrementally** - Verify after each major step

### After Updating

1. **Verify functionality** - Test AI loading and workflows
2. **Clean up backups** - Remove .ai-backup when confirmed
3. **Update team** - Inform team of version update
4. **Run cleanup workflow** - Remove unused guides if needed

---

## Related Workflows

| Workflow | Relationship |
|----------|--------------|
| **initialize-project** | For first-time installation |
| **cleanup-project** | Remove unused guides after update |
| **generate-agents-md** | Regenerate AGENTS.md after update |
| **document-work** | Document the update decision |

---

## Reference Documentation

For detailed migration steps, conflict resolution examples, and troubleshooting procedures, see:

- **references/process.md** - Detailed update procedures and rollback steps
