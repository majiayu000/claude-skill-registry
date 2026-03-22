---
version: 1.1.0
name: meta-skill-catalog
description: >
  Maintains the skill catalog (catalog.json) with metadata about all installed
  skills. Use when adding, removing, or auditing skills. Invoke with
  /meta-skill-catalog to see current inventory, check for issues, or
  rebuild the catalog from disk.
disable-model-invocation: true
---

# Skill Catalog — Inventory Management

Maintains `catalog.json` as the single source of truth for installed skills.

## Commands

### Inventory (`/meta-skill-catalog` or `/meta-skill-catalog inventory`)

1. Scan `.claude/skills/` for all skill directories
2. Read each SKILL.md frontmatter
3. Compare with `catalog.json`
4. Report:
   - Skills on disk but not in catalog (unregistered)
   - Skills in catalog but not on disk (orphaned entries)
   - Skills with mismatched metadata (stale entries)

### Rebuild (`/meta-skill-catalog rebuild`)

1. Scan `.claude/skills/` for all skill directories
2. Read each SKILL.md frontmatter
3. Rebuild `catalog.json` from scratch
4. Report what changed

### Audit (`/meta-skill-catalog audit`)

1. Load `catalog.json`
2. For each skill, check:
   - Does SKILL.md exist and have valid frontmatter?
   - Does the name follow `{category}-{function}` convention?
   - Is the description clear and specific enough for auto-triggering?
   - Are there any trigger overlaps between skills?
   - Is the skill under 500 lines?
   - Does the SKILL.md have a `version` field in frontmatter?
   - Does the catalog version match the SKILL.md version?
3. Report issues with recommendations

## Catalog Format

`catalog.json` structure:

```json
{
  "version": 1,
  "updated": "YYYY-MM-DD",
  "skills": [
    {
      "name": "meta-heartbeat",
      "category": "meta",
      "description": "Session startup ritual...",
      "path": ".claude/skills/meta-heartbeat/",
      "invocation": "user-only",
      "added": "YYYY-MM-DD",
      "version": "1.0.0",
      "installed_from": "agentic-workflow",
      "installed_version": "1.0.0",
      "installed_date": "YYYY-MM-DD"
    }
  ]
}
```

### Fields

| Field | Description |
|-------|-------------|
| `name` | Skill name (matches directory name with category prefix) |
| `category` | Category prefix (meta, dev, ops, tool, viz, doc) |
| `description` | One-line description |
| `path` | Relative path to skill directory |
| `invocation` | `user-only`, `model-only`, or `both` |
| `added` | Date skill was added |
| `version` | Current version at source (from SKILL.md frontmatter) |
| `installed_from` | Provenance: `"agentic-workflow"` or `"local"` |
| `installed_version` | Version that was installed in this project |
| `installed_date` | When this version was installed |
