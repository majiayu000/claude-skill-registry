---
name: migrate-docs
version: "1.0.0"
description: Automate documentation structure migration using rename + rebuild + index generation strategy
last-updated: "2026-03-16"
---

# Migrate Docs - Automated Documentation Structure Migration

> Safely migrate existing project documentation to ai-dev standard structure

## Overview

This skill automates documentation structure migration for existing projects:

**What it does:**
1. Validates target project and captures baseline score
2. Renames old `docs/` to `docs.old/` (backup)
3. Rebuilds standard `docs/` structure (`/init-docs`)
4. Verifies DOCUMENTATION_MANUAL.md was copied
5. Generates migration mapping (COPY/MERGE/MOVE operations)
6. Executes content migration from `docs.old/`
7. Auto-generates `docs/README.md` index
8. Validates new structure (`/check-docs`)
9. Generates detailed migration report

**Why it's needed:**
Manual documentation migration is error-prone and time-consuming (2-3 hours). This skill automates the entire process in ~10 minutes with safety checks and rollback capability.

**When to use:**
- Migrating buffer, u-safe, or other projects to ai-dev doc standards
- Project documentation structure is non-standard
- Need to preserve content while adopting new structure

**Migration strategy:**
- ✅ Rename + Rebuild (not direct `git mv`)
- ✅ Backup-first approach (`docs.old/`)
- ✅ Selective content migration
- ✅ Auto-generated index
- ✅ Easy rollback capability

## Arguments

```bash
/migrate-docs <target-project-path> [options]
```

**Common usage:**
```bash
# Basic migration
/migrate-docs ../buffer

# Preview mode (dry-run)
/migrate-docs ../buffer --dry-run

# Migration with backup cleanup
/migrate-docs ../buffer --delete-old

# Quiet mode (minimal output)
/migrate-docs ../u-safe --quiet
```

**Required:**
- `<target-project-path>` - Path to target project (e.g., `../buffer`)

**Options:**
- `--dry-run` - Preview migration without making changes
- `--delete-old` - Delete `docs.old/` after successful migration
- `--quiet` - Minimal output (only errors and summary)
- `--force` - Skip confirmation prompts

## TRIGGER Conditions

**Invoke this skill when user wants to:**
- "migrate docs for buffer project"
- "apply ai-dev doc structure to u-safe"
- "run documentation migration on ../buffer"
- "convert project docs to standard format"

**DO NOT invoke when:**
- User wants to initialize NEW docs (use `/init-docs`)
- User wants to validate docs (use `/check-docs`)
- User wants to update doc references (use `/update-doc-refs`)

## Execution Steps

### Step 1: Validate Target Project

**Purpose**: Ensure target project is ready for migration

```bash
# Check target project exists
if [ ! -d "$TARGET_PROJECT" ]; then
    echo "❌ Target project not found: $TARGET_PROJECT"
    exit 1
fi

# Check docs/ directory exists
if [ ! -d "$TARGET_PROJECT/docs" ]; then
    echo "❌ No docs/ directory found in target project"
    exit 1
fi

# Get baseline score
cd $TARGET_PROJECT
BASELINE_SCORE=$(/check-docs --score-only)
echo "📊 Baseline score: $BASELINE_SCORE/100"

# Detect project profile
PROFILE=$(cat .framework-install 2>/dev/null | grep -oP 'profile=\K\w+' || echo "unknown")
echo "🔍 Detected profile: $PROFILE"
```

**Output**:
- Target project path validated
- Current docs/ structure exists
- Baseline score recorded
- Project profile detected

### Step 2: Rename Old docs

**Purpose**: Create backup of existing documentation

```bash
cd $TARGET_PROJECT

# Safety check: docs.old should not exist
if [ -d "docs.old" ]; then
    echo "⚠️  docs.old/ already exists"
    echo "Options:"
    echo "  1. Delete docs.old/ and continue"
    echo "  2. Abort migration"
    read -p "Your choice [1/2]: " choice

    if [ "$choice" = "1" ]; then
        rm -rf docs.old
    else
        exit 1
    fi
fi

# Rename docs to docs.old
mv docs docs.old
echo "✅ Backup created: docs.old/"

# Verify backup
if [ ! -d "docs.old" ]; then
    echo "❌ Backup failed"
    exit 1
fi
```

**Output**:
- `docs/` renamed to `docs.old/`
- Backup verified and path recorded
- Original structure preserved

### Step 3: Rebuild Standard Structure

**Purpose**: Create clean ai-dev standard documentation structure

```bash
cd $TARGET_PROJECT

# Call /init-docs to create standard structure
/init-docs

# Verify standard structure created
EXPECTED_DIRS=("product" "arch" "dev" "qa" "ADRs")
if [ "$PROFILE" = "nextjs-aws" ] || [ "$PROFILE" = "tauri-aws" ]; then
    EXPECTED_DIRS+=("ops")
fi

for dir in "${EXPECTED_DIRS[@]}"; do
    if [ ! -d "docs/$dir" ]; then
        echo "❌ Expected directory not created: docs/$dir"
        # Rollback
        rm -rf docs
        mv docs.old docs
        exit 1
    fi
done

# Verify DOCUMENTATION_MANUAL.md was copied
if [ ! -f "docs/DOCUMENTATION_MANUAL.md" ]; then
    echo "⚠️  DOCUMENTATION_MANUAL.md not found (expected from /init-docs)"
    echo "This manual provides documentation standards reference"
fi

echo "✅ Standard structure created (includes 10 files)"
```

**Output**:
- Standard `docs/` structure created
- All required directories present
- DOCUMENTATION_MANUAL.md copied to docs/
- Ready for content migration

### Step 4: Generate Migration Mapping

**Purpose**: Analyze `docs.old/` and create migration plan

```bash
cd $TARGET_PROJECT

# Scan docs.old/ structure
echo "📋 Analyzing docs.old/ structure..."

# Generate migration mapping
MIGRATION_MAP=$(cat <<'EOF'
# Migration Mapping Plan
# Generated: $(date)

## COPY Operations (file duplication)
docs.old/deployment/AWS.md → docs/ops/AWS.md
docs.old/deployment/MONITORING.md → docs/ops/MONITORING.md
docs.old/testing/TEST_PLAN.md → docs/qa/TEST_PLAN.md

## MERGE Operations (combine multiple files)
docs.old/workflow/*.md → docs/dev/WORKFLOW.md
docs.old/api/*.md → docs/arch/API.md

## MOVE Operations (direct mapping)
docs.old/ROADMAP.md → docs/product/roadmap.md
docs.old/dev/SETUP.md → docs/dev/SETUP.md
docs.old/ARCHITECTURE.md → docs/arch/ARCHITECTURE.md

## REVIEW Operations (manual confirmation needed)
docs.old/custom-doc.md → ??? (unmapped file)
docs.old/legacy/old-notes.txt → ??? (legacy content)
EOF
)

echo "$MIGRATION_MAP"

# Ask for confirmation
if [ "$DRY_RUN" != "true" ] && [ "$FORCE" != "true" ]; then
    read -p "Proceed with migration? [y/N]: " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "❌ Migration aborted"
        exit 1
    fi
fi
```

**Output**:
- Complete migration mapping generated
- COPY/MERGE/MOVE/REVIEW operations identified
- User confirmation obtained

### Step 5: Execute Migration

**Purpose**: Migrate content from `docs.old/` to `docs/`

```bash
cd $TARGET_PROJECT

# Execute COPY operations
echo "📂 Copying files..."
cp docs.old/deployment/AWS.md docs/ops/AWS.md
cp docs.old/deployment/MONITORING.md docs/ops/MONITORING.md
cp docs.old/testing/TEST_PLAN.md docs/qa/TEST_PLAN.md

# Execute MERGE operations
echo "🔄 Merging files..."
cat docs.old/workflow/*.md > docs/dev/WORKFLOW.md
cat docs.old/api/*.md > docs/arch/API.md

# Execute MOVE operations
echo "📝 Moving files..."
cp docs.old/ROADMAP.md docs/product/roadmap.md
cp docs.old/dev/SETUP.md docs/dev/SETUP.md
cp docs.old/ARCHITECTURE.md docs/arch/ARCHITECTURE.md

# Handle REVIEW operations
echo "⚠️  Files needing manual review:"
echo "  - docs.old/custom-doc.md"
echo "  - docs.old/legacy/old-notes.txt"
echo ""
echo "Please review these files manually and place in appropriate locations."

# Record migration statistics
FILES_COPIED=3
FILES_MERGED=2
FILES_MOVED=3
FILES_REVIEW=2

echo "✅ Migration complete"
echo "  📋 Files copied: $FILES_COPIED"
echo "  🔄 Files merged: $FILES_MERGED"
echo "  📝 Files moved: $FILES_MOVED"
echo "  ⚠️  Files needing review: $FILES_REVIEW"
```

**Output**:
- Content migrated from `docs.old/` to `docs/`
- Migration statistics recorded
- Manual review items flagged

### Step 6: Generate Documentation Index

**Purpose**: Auto-generate `docs/README.md` with complete index

```bash
cd $TARGET_PROJECT

# Generate docs/README.md
cat > docs/README.md <<'EOF'
# [Project Name] Documentation

> This documentation structure follows the [ai-dev documentation standards](../../ai-dev/docs/DOCUMENTATION_MANUAL.md)

## 📁 Documentation Structure

### Product Documentation
- [PRD.md](product/PRD.md) - Product Requirements Document
- [roadmap.md](product/roadmap.md) - Product Roadmap

### Architecture Documentation
- [ARCHITECTURE.md](arch/ARCHITECTURE.md) - System Architecture Overview
- [SCHEMA.md](arch/SCHEMA.md) - Data Model Design
- [API.md](arch/API.md) - API Documentation

### Development Documentation
- [SETUP.md](dev/SETUP.md) - Development Environment Setup
- [WORKFLOW.md](dev/WORKFLOW.md) - Development Workflow
- [CONTRIBUTING.md](dev/CONTRIBUTING.md) - Contribution Guidelines

### Quality Assurance
- [TEST_PLAN.md](qa/TEST_PLAN.md) - Testing Strategy
- [TEST_CASES.md](qa/TEST_CASES.md) - Test Cases

### Operations Documentation
- [DEPLOYMENT.md](ops/DEPLOYMENT.md) - Deployment Guide
- [MONITORING.md](ops/MONITORING.md) - Monitoring Setup

### Architecture Decision Records
- [ADRs/](ADRs/) - Technical Decision Records

## 🔍 Quick Reference

| I want to... | See documentation |
|--------------|-------------------|
| Understand product features | [PRD.md](product/PRD.md) |
| Set up development environment | [SETUP.md](dev/SETUP.md) |
| Understand system architecture | [ARCHITECTURE.md](arch/ARCHITECTURE.md) |
| Learn development workflow | [WORKFLOW.md](dev/WORKFLOW.md) |
| Review testing strategy | [TEST_PLAN.md](qa/TEST_PLAN.md) |
| Deploy the application | [DEPLOYMENT.md](ops/DEPLOYMENT.md) |

## 📏 Documentation Standards

- 📘 [Complete Standards](DOCUMENTATION_MANUAL.md) - Local copy in this project
- 📋 [Migration Guide](../../ai-dev/docs/DOCUMENTATION_MIGRATION_GUIDE.md) - Framework reference
- ✅ [Validation Tool](/check-docs)

---

**Last Updated**: $(date +%Y-%m-%d) | **Check Score**: Run `/check-docs` to see current score
EOF

echo "✅ Documentation index generated: docs/README.md"
```

**Output**:
- `docs/README.md` created with complete index
- Quick reference table included
- Links to framework standards included

### Step 7: Validate New Structure

**Purpose**: Verify migration success and measure improvement

```bash
cd $TARGET_PROJECT

# Run /check-docs to get new score
NEW_SCORE=$(/check-docs --score-only)
echo "📊 New score: $NEW_SCORE/100"

# Calculate improvement
IMPROVEMENT=$((NEW_SCORE - BASELINE_SCORE))
echo "📈 Improvement: +$IMPROVEMENT points"

# Check if target met (≥95/100)
if [ $NEW_SCORE -ge 95 ]; then
    echo "✅ Target score achieved (≥95/100)"
else
    echo "⚠️  Target score not yet met (need ≥95/100)"
    echo "Run /check-docs --verbose for details"
fi
```

**Output**:
- New documentation score calculated
- Improvement measured
- Target achievement status

### Step 8: Generate Migration Report

**Purpose**: Provide comprehensive migration summary

```bash
cd $TARGET_PROJECT

# Generate final report
cat <<EOF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Documentation Migration Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Scores
  Before: $BASELINE_SCORE/100
  After:  $NEW_SCORE/100
  Change: +$IMPROVEMENT points

📂 Structure
  Before: docs.old/ (preserved as backup)
  After:  docs/ (ai-dev standard)

📋 Migration Statistics
  ✅ $FILES_COPIED files copied
  🔄 $FILES_MERGED file sets merged
  📝 $FILES_MOVED files moved
  ⚠️  $FILES_REVIEW files need manual review

💾 Backup
  Location: docs.old/
  Status: Preserved (use --delete-old to remove)

⚠️  Next Steps
  1. Review new docs/ structure
  2. Handle files needing manual review
  3. Run: /update-doc-refs (update code references)
  4. Test all documentation links
  5. Delete docs.old/ when confident (or use --delete-old)

📘 Documentation
  - Index: docs/README.md
  - Standards: ../../ai-dev/docs/DOCUMENTATION_MANUAL.md
  - Validation: Run /check-docs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF

# Handle --delete-old option
if [ "$DELETE_OLD" = "true" ]; then
    rm -rf docs.old
    echo "🗑️  Deleted docs.old/ backup"
fi
```

**Output**:
- Complete migration summary
- Before/after comparison
- Next steps clearly outlined
- Backup status indicated

## Error Handling & Rollback

**Rollback mechanism:**
```bash
rollback_migration() {
    echo "❌ Migration failed - rolling back..."

    # Remove new docs/ if it exists
    if [ -d "docs" ]; then
        rm -rf docs
        echo "  ✅ Removed new docs/"
    fi

    # Restore docs.old/ to docs/
    if [ -d "docs.old" ]; then
        mv docs.old docs
        echo "  ✅ Restored docs/ from backup"
    fi

    echo "✅ Rollback complete - project unchanged"
    exit 1
}

# Use trap to catch errors
trap rollback_migration ERR
```

**Common errors:**
- Target project not found → Abort with clear message
- docs/ doesn't exist → Abort with guidance
- docs.old/ already exists → Prompt user for action
- /init-docs fails → Automatic rollback
- /check-docs fails → Warning (not critical)

## Integration with Other Skills

**Depends on:**
- `/init-docs` - Creates standard documentation structure
- `/check-docs` - Validates documentation quality

**Works with:**
- `/update-doc-refs` - Updates code references to docs (run after migration)

**Workflow sequence:**
```
1. /migrate-docs ../buffer      # This skill
2. /update-doc-refs ../buffer   # Fix code references
3. /check-docs                  # Validate result
```

## Examples

### Example 1: Basic Migration

```bash
cd ~/dev/ai-dev
/migrate-docs ../buffer

# Output:
# 📊 Baseline score: 65/100
# 🔍 Detected profile: tauri
# ✅ Backup created: docs.old/
# ✅ Standard structure created (includes 10 files)
# ✅ DOCUMENTATION_MANUAL.md copied
# 📋 Migration mapping...
# ✅ Migration complete
# 📊 New score: 95/100
# 📈 Improvement: +30 points
```

### Example 2: Dry Run

```bash
/migrate-docs ../buffer --dry-run

# Output:
# 🔍 DRY RUN MODE - No changes will be made
# 📊 Baseline score: 65/100
# 📋 Migration plan:
#   - 12 files to copy
#   - 3 file sets to merge
#   - 5 files to move
#   - 2 files need review
# ℹ️  Run without --dry-run to execute migration
```

### Example 3: Migration with Cleanup

```bash
/migrate-docs ../u-safe --delete-old

# After successful migration:
# ✅ Migration complete
# 🗑️  Deleted docs.old/ backup
```

## Best Practices

1. **Always run dry-run first** - Preview changes before execution
2. **Review migration mapping** - Verify COPY/MERGE/MOVE plan
3. **Keep docs.old/** - Don't use `--delete-old` until confident
4. **Run update-doc-refs** - Fix code references after migration
5. **Validate links** - Test all documentation links work
6. **Commit strategically** - Commit migration as separate PR

## Performance

- **Dry run**: <5 seconds
- **Full migration**: 30-60 seconds
- **Validation**: 5-10 seconds
- **Total**: ~1-2 minutes

Fast because:
- Automated structure creation
- Efficient file operations
- Minimal user interaction (with --force)

## Related Skills

- **/init-docs** - Initialize documentation structure (called by this skill)
- **/check-docs** - Validate documentation quality (called by this skill)
- **/update-doc-refs** - Update code references (run after migration)

## Related Documentation

- **[DOCUMENTATION_MIGRATION_GUIDE.md](../../docs/DOCUMENTATION_MIGRATION_GUIDE.md)** - Complete migration guide
- **[DOCUMENTATION_MANUAL.md](../../docs/DOCUMENTATION_MANUAL.md)** - Documentation standards

---

**Version:** 1.0.0
**Last Updated:** 2026-03-16
**Changelog:**
- v1.0.0 (2026-03-16): Initial release - documentation migration skill

**Pattern:** Tool-Reference (automated migration workflow)
**Compliance:** ADR-001 ✅
