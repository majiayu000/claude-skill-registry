---
name: update-lib-docs
description: Update library documentation in .claude/docs/libraries/ with latest information from web search.
disable-model-invocation: true
---

# Update Library Documentation

Update documentation in `.claude/docs/libraries/` with latest information.

## Steps

### 1. Check Existing Documents

List current library documentation:

```bash
ls .claude/docs/libraries/
```

### 2. Web Search for Latest Info

For each documented library, search for:

- Latest version
- Breaking changes
- Deprecated features
- New features
- Security updates

### 3. Update Documents

For each library with changes:

1. Update version information
2. Add new features/constraints
3. Mark deprecated APIs
4. Update code examples if needed
5. Record update date at the top

### 4. Check Impact on Code

After updating docs, verify:

- Using any deprecated APIs?
- Any breaking change impacts?
- Need to update project dependencies?

## Key Items to Check

| Category | What to Look For |
|----------|------------------|
| Security | CVEs, security patches |
| Breaking | API changes, removed features |
| Deprecated | APIs marked for removal |
| Performance | Optimization improvements |
| New Features | Useful additions |

## Update Format

Add update notice at top of file:

```markdown
# {Library Name}

> **Last Updated**: {Date}
> **Version Checked**: {version}

## Recent Changes

- {Change 1}
- {Change 2}

---

{Rest of documentation}
```

## Report

After updating, report to user (in Japanese):

- Which libraries were updated
- Significant changes found
- Any action items for the project
