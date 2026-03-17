---
name: release
description: Plugin release workflow skill for version bumping, git tagging, and GitHub release creation. Use when releasing plugin versions with automated CHANGELOG generation and version synchronization.
---

# SKILL: Plugin Release Workflow

> **Purpose**: Execute plugin release workflow with version bumping, git tagging, and GitHub release
> **Target**: Plugin maintainers releasing new versions

---

## Quick Start

### When to Use This Skill
- Release new plugin version
- Bump version (patch/minor/major)
- Create git tag and GitHub release

### Quick Reference
```bash
# Standard release (patch version, CI handles GitHub release)
/999_release

# Minor version
/999_release minor

# Force local GitHub release
/999_release patch --create-gh

# Dry run (preview)
/999_release patch --dry-run
```

---

## What This Skill Covers

### In Scope
- Version synchronization (plugin.json, marketplace.json)
- Git tagging and pushing
- CHANGELOG auto-generation from commits
- GitHub release creation (optional)
- Pre-flight validation

### Out of Scope
- Plugin architecture → @CLAUDE.md
- Git workflow patterns → @.claude/skills/git-master/SKILL.md
- Migration guide → MIGRATION.md

---

## Core Concepts

### Single Source of Truth

**plugin.json** is the PRIMARY version source:
```json
{
  "version": "4.2.0"  // Always update this file
}
```

**Auto-synced file** (DO NOT edit manually):
- marketplace.json - Plugin entry version

### Release Workflow

**Pre-flight** → Version bump → CHANGELOG → Git tag → GitHub release

1. **Pre-flight Checks**: Validate jq, git, working tree, plugin manifests
2. **Version Bump**: Update version files atomically
3. **CHANGELOG**: Auto-generate from git commits (conventional commit format)
4. **Git Operations**: Commit, tag, push to remote
5. **GitHub Release**: Optional (local or CI/CD)

### CI/CD Integration

**Hybrid model**: Local tagging + CI/CD release creation
- Local: Bump version, create tag, push
- CI: Validates versions, creates GitHub release

**Benefits**:
- No API rate limits
- No authentication setup
- Runs on GitHub's infrastructure

---

## Execution Steps (Summary)

### Parse Arguments
- `VERSION_BUMP="${1:-patch}"` - Default: patch
- `--dry-run` - Preview changes
- `--skip-gh` - Skip local GitHub release (default)
- `--create-gh` - Force local GitHub release

### Phase 1: Pre-flight Checks
- Verify jq installed
- Check git working tree is clean
- Validate plugin manifest (single plugin standard)
- Check marketplace.json version sync
- Validate plugin.json fields (no unsupported fields like `agents`)

### Phase 2: Version Bump
- Read current version from plugin.json
- Parse version components (MAJOR.MINOR.PATCH)
- Calculate new version based on bump type
- Check for existing tag
- Update plugin.json (PRIMARY source)
- Update marketplace.json (sync all version fields)
- Verify version consistency

### Phase 3: Auto-Generate CHANGELOG
- Get previous tag
- Parse git commits since previous tag
- Categorize by conventional commit type (feat, fix, docs, etc.)
- Group into categories (Added, Changed, Fixed, Documentation)
- Insert at top of CHANGELOG.md

### Phase 4: Git Operations
- Preview changes (if --dry-run)
- Stage version files
- Commit with conventional commit format
- Create annotated tag
- Push commit and tag to remote

### Phase 5: GitHub Release (Optional)
- Check if gh CLI installed
- Extract CHANGELOG section for version
- Create GitHub release using gh CLI
- Skip by default (CI/CD handles it)

---

## Further Reading

**Internal**: @.claude/skills/release/REFERENCE.md - Full release workflow implementation details, troubleshooting, CI/CD integration, version tracking | @.claude/skills/git-master/SKILL.md - Git operations and commits | @.claude/commands/999_release.md - Release command

**External**: [Semantic Versioning](https://semver.org/) | [Conventional Commits](https://www.conventionalcommits.org/) | [Keep a Changelog](https://keepachangelog.com/)
