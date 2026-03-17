---
name: documentation-reviewer
description: Review and update MkDocs documentation when code changes. This skill should be used when completing feature implementation, after making code changes that affect user-facing functionality, when reviewing PRs for documentation completeness, or when auditing documentation coverage. Analyzes git diffs to identify documentation gaps and provides MkDocs Material formatting patterns.
---

# Documentation Reviewer

## Overview

Ensure documentation stays synchronized with code changes. Analyze git diffs, identify impacted documentation, and update MkDocs Material docs with proper formatting.

## Workflow

```
1. Analyze Changes → 2. Map to Docs → 3. Identify Gaps → 4. Update Docs → 5. Verify
```

### Step 1: Analyze Changes

Run the change analysis script or manually check:

```bash
# Using script (from project root)
python3 ~/.claude/skills/documentation-reviewer/scripts/analyze_changes.py

# Manual check
git diff --name-only HEAD~1  # or specify commit range
git diff --stat HEAD~1
```

### Step 2: Map Changes to Documentation

| Change Type | Documentation Impact |
|-------------|---------------------|
| New API endpoint | `docs/api/endpoints.md` |
| New feature/component | `docs/features/` or `docs/architecture/` |
| Config changes | `docs/getting-started/` or `docs/development/` |
| New invoke task | `docs/development/invoke-tasks.md` |
| Docker changes | `docs/architecture/docker.md` |
| Model changes | `docs/api/endpoints.md`, `docs/architecture/backend.md` |
| Frontend component | `docs/architecture/frontend.md` |

See `references/change-mapping.md` for complete mapping rules.

### Step 3: Identify Documentation Gaps

Check for missing documentation:

1. **New exports** - Public functions/classes need documentation
2. **Changed behavior** - Updated logic needs updated docs
3. **New config options** - Environment variables, settings
4. **Breaking changes** - Migration guides required
5. **New dependencies** - Installation instructions

### Step 4: Update Documentation

Use MkDocs Material syntax from `references/mkdocs-material-syntax.md`:

- Admonitions for warnings/tips
- Code blocks with titles and line numbers
- Tabbed content for multi-platform instructions
- Tables for structured data
- Mermaid diagrams for architecture

### Step 5: Verify

```bash
# Serve docs locally
mkdocs serve

# Check for broken links and build
mkdocs build --strict
```

## Quick Reference

### Must-Document Changes

- [ ] New API endpoints
- [ ] New CLI commands/invoke tasks
- [ ] Configuration changes
- [ ] Breaking changes
- [ ] New features
- [ ] Security-related changes

### Documentation Checklist

- [ ] Updated relevant docs page(s)
- [ ] Added to mkdocs.yml nav if new page
- [ ] Code examples are accurate and tested
- [ ] Links are valid
- [ ] Consistent with existing style

## Resources

- `references/mkdocs-material-syntax.md` - Formatting patterns and examples
- `references/change-mapping.md` - Code-to-docs mapping rules
- `references/documentation-standards.md` - Writing style and structure
- `scripts/analyze_changes.py` - Git diff analysis tool
