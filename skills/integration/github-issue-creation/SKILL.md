---
name: github-issue-creation
description: Create GitHub issues with proper task classification. Classification determines which Skills will be used when working on the issue.
---

# GitHub Issue Creation

Create issues with proper classification. **Labels determine which Skills are used.**

## Prerequisites

- **Load label-context-mapping skill**: Use for all label → skill/context mappings
  - See [label-context-mapping](../label-context-mapping/SKILL.md)

## Label Selection Rules

### Required Labels

Every issue must have:
1. **One Type label** (`bug`, `enhancement`, `refactoring`, `documentation`, `security`, `technical-debt`, `test`)
2. **One Language OR Scope label** (`lang:*` or `scope:*`)

### Optional Labels

- **Chain label**: Only for cryptocurrency-specific code
- **Test Scope label**: Only when Type is `test`

## Issue Creation Process

### 1. Classify Task

From user request, determine:
- Type (bug, enhancement, refactoring, documentation, security, technical-debt, test)
- Language OR Scope
- Test scope (if applicable)
- Chain (if applicable)

Use `label-context-mapping` skill for label → skill/context mappings.

### 2. Create Proposal

```markdown
## Proposed Issue

**Title**: [Clear title - 50-72 chars]

**Labels**: [type], [lang/scope], [test scope if applicable], [chain if applicable]

**Skills**: [git-workflow] + [skill based on label-context-mapping]

**Body**:
## Description
[What needs to be done]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### 3. Create Issue (After Approval)

```bash
gh issue create \
  --title "Title" \
  --body "Body" \
  --label "type,lang/scope,chain"
```

## Quick Reference

```
Required: [Type] + [Language OR Scope]
Optional: [Test Scope] + [Chain]

→ Labels determine Skills (see label-context-mapping)
→ Skills determine workflow
```

## Related

- [label-context-mapping](../label-context-mapping/SKILL.md) - Label → Skill/Context mapping
- [Task Classification SSOT](../../../docs/standards/task-classification.md) - Label definitions
- [fix-issue command](../../commands/fix-issue.md) - Working on issues
