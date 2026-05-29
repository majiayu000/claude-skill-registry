---
name: project-standardization
description: "Guides correct usage of @j0kz/mcp-agents standardization and automation scripts including version.json single source of truth, test count automation, URL casing rules, and critical workflow pattern..."
---

# Project Standardization & Automation for @j0kz/mcp-agents

Ensure consistency across monorepo using automated scripts and established patterns.

## 4 Critical Rules (NEVER VIOLATE)

### Rule 1: version.json is Single Source of Truth
- ❌ NEVER manually edit package.json versions
- ✅ ALWAYS use: `npm run version:sync`
- 11 packages must stay in sync

### Rule 2: URL Casing Rules
- GitHub: `j0KZ` (capital K, Z)
- npm: `@j0kz` (lowercase)
- Mixing breaks links and installations

### Rule 3: Test Count Automation
- ❌ NEVER manually edit test badges
- ✅ ALWAYS use: `npm run update:test-count`
- Currently: 632 tests passing

### Rule 4: @latest in Documentation
- ❌ WRONG: `npx @j0kz/mcp-agents@1.0.36`
- ✅ RIGHT: `npx @j0kz/mcp-agents@latest`

## Quick Command Reference

```bash
# Version management
npm run version:sync              # Sync all versions from version.json
npm run version:check-shared      # Verify shared package versions

# Testing
npm test                          # Run all tests
npm run update:test-count         # Update test count in docs

# Building
npm run build                     # Build all packages
npm run dev                       # Watch mode

# Publishing
npm run publish-all               # Publish all packages
```

## Version Management Workflow

### Quick Start: New Release

```bash
# 1. Update version.json
echo '{"version": "1.1.0"}' > version.json

# 2. Sync and build
npm run version:sync
npm run version:check-shared
npm test
npm run build

# 3. Publish
npm run publish-all
cd installer && npm publish && cd ..

# 4. Git operations
git add . && git commit -m "release: v1.1.0"
git tag v1.1.0 && git push origin main --tags
```

**For detailed release workflow with all steps:**
```bash
cat .claude/skills/project-standardization/references/version-management-guide.md
```

## Test Count Management

```bash
# After adding/removing tests
npm run update:test-count

# Updates 3 files automatically:
# - README.md badge
# - wiki/Home.md badge and table
# - CHANGELOG.md metrics
```

**For test automation details and patterns:**
```bash
cat .claude/skills/project-standardization/references/test-automation-guide.md
```

## URL & Link Standards

**Critical:** GitHub uses `j0KZ`, npm uses `@j0kz`

**For complete URL standards and examples:**
```bash
cat .claude/skills/project-standardization/references/url-standards-guide.md
```

## tools.json Management

**Location:** `tools.json` at repository root - Single source of truth for all MCP tool metadata

**When to update:**
- Adding new MCP tool
- Changing tool features/descriptions
- Adding new category

**Structure includes:** tool id, name, package, description, category, features, wikiPage

## Workspace Management

### Adding New Package

```bash
mkdir packages/new-tool
npm install                       # Auto-discovers workspace
npm ls --workspaces              # Verify recognized
```

### Dependency Installation

```bash
npm install typescript -w packages/new-tool  # Specific workspace
npm install typescript --workspaces          # All workspaces
npm install vitest -D                        # Root only
```

## Common Mistakes and Quick Fixes

| Mistake | Fix |
|---------|-----|
| Manually edited package.json version | `npm run version:sync` |
| Hardcoded version instead of @latest | Use `@latest` in docs |
| Wrong URL casing (GitHub/npm) | GitHub: `j0KZ`, npm: `@j0kz` |
| Manually updated test count | `npm run update:test-count` |
| Forgot to sync after version.json change | Always run `version:sync` first |

## Validation & Checklists

**For complete validation checklists (pre-commit, pre-publish, post-publish):**
```bash
cat .claude/skills/project-standardization/references/validation-checklists.md
```

## Key File Locations

```
version.json                      # Single source of truth for versions
tools.json                        # MCP tool metadata
scripts/sync-versions.js          # Version sync automation
scripts/update-test-count.js      # Test count automation
scripts/enforce-shared-version.js # Shared version validation
```

## Getting Help

```bash
# Check current state
cat version.json                  # Current version
npm run version:check-shared      # Package consistency
git status                        # Uncommitted changes

# Review scripts
ls scripts/                       # List all automation
cat scripts/sync-versions.js      # Read script details
```

## Related Skills

- **monorepo-package-workflow:** Creating new MCP packages
- **release-publishing-workflow:** Complete release process
- **git-pr-workflow:** Git operations and PR creation

## Additional Resources

- **CLAUDE.md:** Repository-wide standards and patterns
- **Wiki:** https://github.com/j0KZ/mcp-agents/wiki
