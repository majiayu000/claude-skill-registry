---
name: implementation
description: "Use when implementing features from feature-list.json, writing code following project patterns, or using MCP tools efficiently. Load in IMPLEMENT state. Covers coding patterns, test writing, health checks, and token-efficient MCP usage (defer_loading for 85% savings)."
keywords: implement, code, develop, mcp, patterns, health-check
---

# Implementation

Feature development for IMPLEMENT state.

## Instructions

1. Get current feature: `scripts/get-current-feature.sh`
2. Query context graph for similar work
3. Implement following project patterns (see references/)
4. Write tests alongside code
5. Run health check: `scripts/health-check.sh`
6. **Git commit**: `scripts/feature-commit.sh <feature-id>`
7. Mark complete: `scripts/mark-feature-complete.sh`

## Exit Criteria (Code Verified)

```bash
# All must pass
scripts/health-check.sh && echo "Health OK"
[ -f "tests/test_*.py" ] || [ -f "*.test.ts" ]
[ -z "$(git status --porcelain)" ] && echo "Changes committed"
jq '.features[] | select(.id=="'$FEATURE_ID'") | .status == "implemented"' .claude/progress/feature-list.json
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/feature-commit.sh` | Commit with feature ID message |
| `scripts/session-commit.sh` | Checkpoint commit at session end |

## References

| File | Load When |
|------|-----------|
| references/coding-patterns.md | Writing implementation code |
| references/mcp-usage.md | Using MCP tools efficiently |
| references/health-checks.md | Verifying implementation |
| references/async-parallel-operations.md | Running independent operations in parallel |
