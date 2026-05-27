---
name: cross-skill-references-test
description: Test skill with cross-skill reference notation
allowed-tools: Read, Skill
---

# Cross-Skill References Test Skill

This skill tests that cross-skill references (using bundle:skill notation) are properly recognized.

## Workflow

### Step 1: Load Foundation Skills

```
Skill: pm-plugin-development:plugin-architecture
Skill: cui-utilities:cui-diagnostic-patterns
```

### Step 2: Load External Reference

Read plugin-architecture:references/script-standards.md

### Step 3: Load Local Reference

Read references/local-guide.md

## Notes

The cross-skill reference `plugin-architecture:references/script-standards.md` should NOT be
flagged as missing - it loads from another skill at runtime.
