---
description: Update a specific crate skill to latest version
argument-hint: <crate_name> [version]
---

# Update Crate Skill

Force regenerate a crate skill with the latest documentation.

Arguments: $ARGUMENTS
- `crate_name` (required): The crate to update
- `version` (optional): Specific version to target

---

## Instructions

### 1. Check Current Skill

```bash
# Check if skill exists
cat ~/.claude/skills/{crate_name}*/SKILL.md | head -20
```

Display current version info if exists:
```
Current skill:
- Crate: tokio
- Version: 1.38.0
- Last Updated: 2025-01-01
```

### 2. Get Latest Version

If version not provided, fetch latest from crates.io:
```bash
cargo search {crate_name} --limit 1
```

Or use crate-researcher agent to get latest version.

### 3. Remove Old Skill

```bash
rm -rf ~/.claude/skills/{crate_name}*
```

### 4. Generate Fresh llms.txt

```
/create-llms-for-skills https://docs.rs/{crate_name}/{version}/{crate_name}/
```

### 5. Create Updated Skill

```
/create-skills-via-llms {crate_name} {llms_path} {version}
```

### 6. Report Results

```
Updated skill:
- Crate: tokio
- Old Version: 1.38.0
- New Version: 1.40.0
- Location: ~/.claude/skills/tokio/
```

---

## Example Usage

```bash
# Update tokio to latest version
/update-crate-skill tokio

# Update to specific version
/update-crate-skill tokio 1.40.0

# Update serde
/update-crate-skill serde
```

---

## When to Update

- Crate has new major/minor release
- API has changed significantly
- Existing skill has incorrect information
- Documentation has improved
