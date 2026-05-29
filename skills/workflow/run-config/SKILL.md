---
name: run-config
description: Run configuration handling for persistent command configuration storage
allowed-tools: Read, Write, Edit, Bash
---

# Run Config Skill

Run configuration handling for persistent command configuration storage.

## What This Skill Provides

- Read and update run configuration entries
- Track command execution history
- Manage acceptable warnings and skip lists
- Manage profile-to-canonical mappings
- Store extension-specific defaults
- Adaptive timeout management
- Validate run configuration format

## When to Activate This Skill

Activate this skill when:
- Recording command execution results
- Managing acceptable warnings lists
- Managing profile mappings for build profiles
- Setting extension defaults during initialization
- Managing command timeouts
- Validating run configuration structure

---

## Run Configuration Structure

```json
{
  "version": 1,
  "commands": {
    "<command-name>": {
      "last_execution": {"date": "...", "status": "SUCCESS|FAILURE"},
      "acceptable_warnings": [],
      "skipped_files": []
    }
  },
  "maven": {
    "acceptable_warnings": {
      "transitive_dependency": [],
      "plugin_compatibility": [],
      "platform_specific": []
    }
  },
  "profile_mappings": {},
  "extension_defaults": {}
}
```

See [references/run-config-format.md](references/run-config-format.md) for complete schema.

---

## Scripts

| Script | Notation |
|--------|----------|
| init | `plan-marshall:run-config:run_config init` |
| validate | `plan-marshall:run-config:run_config validate` |
| timeout get | `plan-marshall:run-config:run_config timeout get` |
| timeout set | `plan-marshall:run-config:run_config timeout set` |
| warning add | `plan-marshall:run-config:run_config warning add` |
| warning list | `plan-marshall:run-config:run_config warning list` |
| warning remove | `plan-marshall:run-config:run_config warning remove` |
| profile-mapping set | `plan-marshall:run-config:run_config profile-mapping set` |
| profile-mapping get | `plan-marshall:run-config:run_config profile-mapping get` |
| profile-mapping list | `plan-marshall:run-config:run_config profile-mapping list` |
| profile-mapping remove | `plan-marshall:run-config:run_config profile-mapping remove` |
| profile-mapping batch-set | `plan-marshall:run-config:run_config profile-mapping batch-set` |
| extension-defaults get | `plan-marshall:run-config:run_config extension-defaults get` |
| extension-defaults set | `plan-marshall:run-config:run_config extension-defaults set` |
| extension-defaults set-default | `plan-marshall:run-config:run_config extension-defaults set-default` |
| extension-defaults list | `plan-marshall:run-config:run_config extension-defaults list` |
| extension-defaults remove | `plan-marshall:run-config:run_config extension-defaults remove` |
| cleanup | `plan-marshall:run-config:cleanup` |

Script characteristics:
- Uses Python stdlib only (json, argparse, pathlib)
- Outputs JSON (init/validate) or TOON (timeout/cleanup) to stdout
- Exit code 0 for success, 1 for errors
- Supports `--help` flag

---

## Standards

| Document | Purpose | When to Read |
|----------|---------|--------------|
| [timeout-handling.md](standards/timeout-handling.md) | Adaptive timeout management | Managing command timeouts |
| [profile-mapping.md](standards/profile-mapping.md) | Profile-to-canonical mappings | Handling unmapped build profiles |
| [warning-handling.md](standards/warning-handling.md) | Acceptable warning patterns | Filtering build warnings |
| [extension-defaults.md](standards/extension-defaults.md) | Extension configuration | Setting extension defaults |
| [cleanup-operations.md](standards/cleanup-operations.md) | Directory cleanup | Cleaning old files |

---

## Quick Start

### Initialize Configuration

```bash
python3 .plan/execute-script.py plan-marshall:run-config:run_config init
```

### Validate Configuration

```bash
python3 .plan/execute-script.py plan-marshall:run-config:run_config validate
```

---

## Integration Points

### With json-file-operations Skill
- Uses generic JSON operations for field access and updates
- All CRUD operations delegate to json-file-operations

### With planning Bundle
- Commands record execution history to run configuration

### With lessons-learned Skill
- Lessons learned are stored separately via `plan-marshall:lessons-learned` skill
- Run configuration tracks execution state only

---

## References

- `references/run-config-format.md` - Complete schema documentation
- `standards/timeout-handling.md` - Adaptive timeout management
- `standards/profile-mapping.md` - Profile-to-canonical mappings
- `standards/warning-handling.md` - Acceptable warning patterns
- `standards/extension-defaults.md` - Extension configuration storage
- `standards/cleanup-operations.md` - Directory cleanup operations
