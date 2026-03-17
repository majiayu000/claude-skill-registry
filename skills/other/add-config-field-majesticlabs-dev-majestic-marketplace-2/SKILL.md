---
name: add-config-field
description: Add new field to .agents.yml config schema (updates init.md templates, version, migration)
allowed-tools: Read, Edit, Glob, Grep
---

# Add Config Field

Add a new field to the `.agents.yml` config schema with proper versioning and migration support.

## Files Changed

| File | Purpose |
|------|---------|
| `plugins/majestic-engineer/commands/workflows/init.md` | 4 YAML templates that generate .agents.yml |
| `plugins/majestic-engineer/config-schema-version` | Schema version number |
| `plugins/majestic-engineer/agents/config-reader.md` | Changelog + migration logic |
| `plugins/majestic-engineer/.claude-plugin/plugin.json` | Plugin version |
| `.claude-plugin/marketplace.json` | Marketplace version |

## Input

- **Field name**: e.g., `auto_commit`
- **Default value**: e.g., `false` or multi-line YAML
- **Section**: Where in template (Workflow, Quality Gate, etc.)
- **Comment**: Inline explanation
- **Used by**: Agent/command that reads this field

## Steps

### 1. Update init.md Templates

**File:** `plugins/majestic-engineer/commands/workflows/init.md`

Add field to ALL 4 templates (Rails, Python, Node, Generic). Find the appropriate section and add:

```yaml
new_field: value              # Comment explaining purpose
```

Or for multi-line:
```yaml
new_field:                    # Comment
  - item1
  - item2
```

### 2. Bump Schema Version

**File:** `plugins/majestic-engineer/config-schema-version`

Increment: `1.1` → `1.2`

### 3. Update config-reader.md

**File:** `plugins/majestic-engineer/agents/config-reader.md`

**A) Add to Version Changelog table:**
```markdown
| 1.2 | `new_field` | Description |
```

**B) Update migration YAML block** (in "Outdated config_version" section):
```yaml
new_field: default_value
```

### 4. Bump Plugin Versions

**Files:**
- `plugins/majestic-engineer/.claude-plugin/plugin.json`: `3.15.0` → `3.16.0`
- `.claude-plugin/marketplace.json`: Update majestic-engineer entry version

### 5. Update Consumer Docs (if needed)

If a specific agent/command reads this field, update its documentation to mention the config.

## Verification

```bash
# Count field in init.md (should be 4 - one per template)
grep -c "new_field" plugins/majestic-engineer/commands/workflows/init.md

# Check schema version
cat plugins/majestic-engineer/config-schema-version

# Check changelog entry
grep "new_field" plugins/majestic-engineer/agents/config-reader.md
```
