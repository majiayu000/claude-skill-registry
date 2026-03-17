---
name: "code-quality-tools"
description: "Automated code quality fixes for linting, types, unused variables, and error handling; use when fixing code quality issues in bulk"
version: "1.0.0"
---

# Code Quality Tools

## When to Use This Skill

Use this skill when:
- Fixing lint errors in bulk
- Removing unused variables
- Fixing TypeScript `any` types
- Validating error handling patterns
- Optimizing images

## Scripts

**Location**: `.claude/skills/code-quality-tools/scripts/`

| Script | Description |
|--------|-------------|
| `fix-any-types.sh` | Replace `any` types with proper types |
| `fix-lint-comprehensive.sh` | Comprehensive lint fixes |
| `fix-unused-vars.sh` | Remove unused variables |
| `fix-service-errors.sh` | Fix service error patterns |
| `fix-service-error-calls.py` | Python script for service error fixes |
| `validate-error-handling.sh` | Validate error handling patterns |
| `optimize-images.sh` | Optimize image assets |

## Quick Start

```bash
# Fix all lint issues
./.claude/skills/code-quality-tools/scripts/fix-lint-comprehensive.sh

# Remove unused variables
./.claude/skills/code-quality-tools/scripts/fix-unused-vars.sh

# Validate error handling
./.claude/skills/code-quality-tools/scripts/validate-error-handling.sh
```

## Common Workflows

### Pre-Commit Quality Check

```bash
# 1. Fix lint issues
./.claude/skills/code-quality-tools/scripts/fix-lint-comprehensive.sh

# 2. Remove unused vars
./.claude/skills/code-quality-tools/scripts/fix-unused-vars.sh

# 3. Run pnpm quality
pnpm quality
```

### Image Optimization

```bash
./.claude/skills/code-quality-tools/scripts/optimize-images.sh
```
