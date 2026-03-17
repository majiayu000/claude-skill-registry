---
name: managing-tags
description: Manage and consolidate tags. Use when asked to "clean up tags", "consolidate tags", "tag audit", "merge tags", or "rename tag".
allowed-tools: Read, Glob, Grep, Edit
---

# Managing Tags

This skill helps maintain tag hygiene by finding inconsistencies and consolidating similar tags.

## Workflow

### 1. Extract All Tags

```bash
# Find all tags across content
grep -h "^tags:" content/*.md
```

Build a complete tag inventory with usage counts.

### 2. Identify Issues

#### Similar Tags (Candidates for Merge)
Look for tags that likely mean the same thing:
- `ai` vs `artificial-intelligence`
- `dev` vs `development`
- `js` vs `javascript`
- Plural vs singular: `habit` vs `habits`

#### Inconsistent Naming
Check for violations of kebab-case convention:
- `camelCase` tags
- `Capitalized` tags
- `under_score` tags
- Tags with spaces

#### Rarely Used Tags
- Tags appearing only once (may indicate typo)
- Tags used 2-3 times (consider consolidation)

### 3. Generate Report

```markdown
## Tag Audit Report

### Tag Inventory (by frequency)
| Tag | Count |
|-----|-------|
| vue | 5 |
| testing | 4 |
| ai | 3 |
| ...

### Similar Tags (Merge Candidates)
- `ai` (3) + `artificial-intelligence` (1) → suggest: `ai`
- `habit` (2) + `habits` (1) → suggest: `habits`

### Naming Issues
- `JavaScript` → should be `javascript`
- `local_first` → should be `local-first`

### Rarely Used (1 occurrence)
- `obscure-tag` - only in `one-note.md`
```

### 4. Perform Merges (When Requested)

To merge tags, edit the frontmatter of affected files:

```yaml
# Before
tags:
  - artificial-intelligence
  - machine-learning

# After
tags:
  - ai
  - machine-learning
```

Use the Edit tool to update each file's frontmatter.

## Tag Naming Convention

All tags should be:
- **Lowercase**: `vue` not `Vue`
- **Kebab-case**: `local-first` not `local_first` or `localFirst`
- **Singular or plural consistently**: Pick one and stick to it
- **Meaningful**: Avoid overly generic tags like `stuff` or `misc`

## Common Merge Patterns

| Variations | Preferred |
|------------|-----------|
| `ai`, `artificial-intelligence`, `AI` | `ai` |
| `js`, `javascript`, `JavaScript` | `javascript` |
| `vue`, `vuejs`, `vue-js` | `vue` |
| `dev`, `development`, `developer` | `development` |
| `test`, `testing`, `tests` | `testing` |

## Quality Checklist

Before suggesting changes:
- [ ] Extracted all tags from all files
- [ ] Counted usage per tag
- [ ] Identified similar tags
- [ ] Checked naming consistency
- [ ] Flagged rarely used tags
- [ ] Proposed specific merge actions
