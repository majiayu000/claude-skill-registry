---
name: Hook Register
description: Validates and registers hook manifest files (YAML) in the Hook Registry for versioned hook management.
---

# hook.register Skill

Validates and registers hook manifest files, adding them to the Hook Registry for automatic enforcement.

## Purpose

While `hook.define` creates hooks on-the-fly and updates the live configuration (`.claude/hooks.yaml`), the `hook.register` skill formalizes this by validating a hook manifest and adding it to a versioned registry (`/registry/hooks.json`). This enables:

- **Version Control**: Track hooks as code with full history
- **Review Process**: Hook manifests can go through code review before activation
- **Centralized Management**: Single source of truth for all hooks in the organization
- **Formal Schema**: Ensures hooks conform to required structure

This skill is part of Betty's Layer 5 (Hooks/Policy) infrastructure, enabling automated governance and validation.

## Difference from hook.define

| Feature | hook.define | hook.register |
|---------|-------------|---------------|
| **Purpose** | Create hooks immediately | Register hook manifests for version control |
| **Output File** | `.claude/hooks.yaml` (live config) | `/registry/hooks.json` (registry) |
| **Use Case** | Quick development, testing | Production deployment, formal tracking |
| **Versioning** | Not tracked | Full version history |
| **Schema Validation** | Basic | Comprehensive |

## Usage

```bash
python skills/hook.register/hook_register.py <path_to_hook_manifest.yaml>
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| manifest_path | string | Yes | Path to the hook manifest YAML file to validate |

## Hook Manifest Schema

### Required Fields

- **name**: Unique hook identifier (kebab-case recommended, e.g., `validate-openapi-specs`)
- **version**: Semantic version (e.g., `0.1.0`)
- **description**: Human-readable description of what the hook does
- **event**: Hook trigger event (see Valid Events table below)
- **command**: Command to execute when hook triggers

### Optional Fields

- **when**: Conditional execution
  - `pattern`: File pattern to match (e.g., `"*.openapi.yaml"`, `"specs/**/*.yaml"`)
- **blocking**: Whether hook should block operation if it fails (default: `false`)
- **timeout**: Timeout in milliseconds (default: `30000`)
- **on_failure**: What to do on failure: `show_errors`, `silent`, `log_only` (default: `show_errors`)
- **status**: Hook status (`draft` or `active`, defaults to `draft`)
- **tags**: Array of tags for categorization (e.g., `["api", "validation", "compliance"]`)

### Valid Events

| Event | Triggers When | Common Use Cases |
|-------|---------------|------------------|
| `on_file_edit` | File is edited in editor | Real-time syntax validation |
| `on_file_save` | File is saved to disk | Code generation, formatting |
| `on_commit` | Git commit attempted | Breaking change detection, linting |
| `on_push` | Git push attempted | Full validation suite, security scans |
| `on_tool_use` | Any tool is used | Audit logging, usage tracking |
| `on_agent_start` | Agent begins execution | Context injection, authorization |
| `on_workflow_end` | Workflow completes | Cleanup, notifications, reporting |

## Validation Rules

The skill performs comprehensive validation:

1. **Required Fields** – Ensures `name`, `version`, `description`, `event`, and `command` are present
2. **Name Format** – Validates hook name is non-empty and follows naming conventions
3. **Version Format** – Ensures version follows semantic versioning (e.g., `0.1.0`)
4. **Event Type** – Verifies event is one of the supported triggers
5. **Command Validation** – Ensures command is non-empty
6. **Type Checking** – Validates `blocking` is boolean, `timeout` is positive number
7. **Pattern Validation** – If `when.pattern` is provided, ensures it's a valid string
8. **Name Uniqueness** – Checks that hook name doesn't conflict with existing hooks in registry

## Outputs

### Success Response

```json
{
  "ok": true,
  "status": "registered",
  "errors": [],
  "path": "hooks/validate-openapi.yaml",
  "details": {
    "valid": true,
    "status": "registered",
    "registry_updated": true,
    "manifest": {
      "name": "validate-openapi-specs",
      "version": "0.1.0",
      "description": "Validate OpenAPI specs against Zalando guidelines",
      "event": "on_file_edit",
      "command": "python skills/api.validate/api_validate.py {file_path} zalando",
      "when": {
        "pattern": "*.openapi.yaml"
      },
      "blocking": true,
      "timeout": 10000,
      "status": "active",
      "tags": ["api", "validation", "openapi"]
    }
  }
}
```

### Failure Response

```json
{
  "ok": false,
  "status": "failed",
  "errors": [
    "Invalid event: 'on_file_change'. Must be one of: on_file_edit, on_file_save, on_commit, on_push, on_tool_use, on_agent_start, on_workflow_end"
  ],
  "path": "hooks/invalid-hook.yaml",
  "details": {
    "valid": false,
    "errors": [
      "Invalid event: 'on_file_change'. Must be one of: on_file_edit, on_file_save, on_commit, on_push, on_tool_use, on_agent_start, on_workflow_end"
    ],
    "path": "hooks/invalid-hook.yaml"
  }
}
```

## Examples

### Example 1: Register OpenAPI Validation Hook

**Hook Manifest** (`hooks/validate-openapi.yaml`):

```yaml
name: validate-openapi-specs
version: 0.1.0
description: "Validate OpenAPI specs against Zalando guidelines on every edit"

event: on_file_edit
command: "python skills/api.validate/api_validate.py {file_path} zalando"

when:
  pattern: "*.openapi.yaml"

blocking: true
timeout: 10000

status: active
tags: [api, validation, openapi, zalando]
```

**Registration Command**:

```bash
$ python skills/hook.register/hook_register.py hooks/validate-openapi.yaml
{
  "ok": true,
  "status": "registered",
  "errors": [],
  "path": "hooks/validate-openapi.yaml",
  "details": {
    "valid": true,
    "status": "registered",
    "registry_updated": true
  }
}
```

### Example 2: Register Breaking Change Detection Hook

**Hook Manifest** (`hooks/prevent-breaking-changes.yaml`):

```yaml
name: prevent-breaking-changes
version: 0.1.0
description: "Block commits that introduce breaking API changes"

event: on_commit
command: "python skills/api.compatibility/check_compatibility.py {file_path} --fail_on_breaking"

when:
  pattern: "specs/**/*.yaml"

blocking: true
timeout: 30000

on_failure: show_errors

status: active
tags: [api, compatibility, breaking-changes, commit-hook]
```

### Example 3: Register Audit Log Hook

**Hook Manifest** (`hooks/audit-tool-usage.yaml`):

```yaml
name: audit-tool-usage
version: 0.1.0
description: "Log all tool usage for compliance audit trail"

event: on_tool_use
command: "python skills/audit.log/log_tool_usage.py {tool_name} {timestamp}"

blocking: false
timeout: 5000

on_failure: log_only

status: active
tags: [audit, compliance, logging]
```

## Integration

### With Workflows

Hooks can be registered as part of a workflow:

```yaml
# workflows/setup_governance.yaml
steps:
  - skill: hook.register
    args:
      - "hooks/validate-openapi.yaml"
    required: true

  - skill: hook.register
    args:
      - "hooks/prevent-breaking-changes.yaml"
    required: true
```

### With CI/CD

Validate hooks in continuous integration:

```yaml
# .github/workflows/validate-hooks.yml
name: Validate Hooks
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate all hooks
        run: |
          for hook in hooks/*.yaml; do
            python skills/hook.register/hook_register.py "$hook" || exit 1
          done
```

### Loading Hooks at Runtime

Once registered, hooks can be loaded from the registry:

```python
import json

with open('/registry/hooks.json') as f:
    registry = json.load(f)

active_hooks = [h for h in registry['hooks'] if h['status'] == 'active']
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Missing required fields: name" | Hook manifest missing required field | Add all required fields: name, version, description, event, command |
| "Invalid event: 'X'" | Event type not recognized | Use one of the valid events: on_file_edit, on_file_save, on_commit, on_push, on_tool_use, on_agent_start, on_workflow_end |
| "command cannot be empty" | Command field is empty or whitespace | Provide a valid command string |
| "blocking must be a boolean" | blocking field is not true/false | Use boolean value: `true` or `false` (not string) |
| "timeout must be a positive number" | timeout is zero or negative | Provide positive number in milliseconds (e.g., 30000) |
| "when.pattern must be a non-empty string" | Pattern is empty or wrong type | Provide valid glob pattern (e.g., "*.yaml") |

## Files Modified

- **Registry**: `/registry/hooks.json` – Updated with new or modified hook entry
- **Logs**: Hook validation and registration logged to Betty's logging system

## Hook Registry Structure

The `/registry/hooks.json` file has this structure:

```json
{
  "registry_version": "1.0.0",
  "generated_at": "2025-10-23T12:00:00Z",
  "hooks": [
    {
      "name": "validate-openapi-specs",
      "version": "0.1.0",
      "description": "Validate OpenAPI specs against Zalando guidelines",
      "event": "on_file_edit",
      "command": "python skills/api.validate/api_validate.py {file_path} zalando",
      "when": {
        "pattern": "*.openapi.yaml"
      },
      "blocking": true,
      "timeout": 10000,
      "on_failure": "show_errors",
      "status": "active",
      "tags": ["api", "validation", "openapi"]
    }
  ]
}
```

## See Also

- **hook.define** – Use this for immediate hook creation in the dev environment (documented in [hook.define SKILL.md](../hook.define/SKILL.md))
- **Hook Manifest Schema** – See [Command & Hook Infrastructure](../../docs/COMMAND_HOOK_INFRASTRUCTURE.md) for field definitions
- **Betty Architecture** – [Five-Layer Model](../../docs/betty-architecture.md) for understanding how hooks fit into the governance layer
- **Hooks in Claude Code** – [Claude Code Hooks Documentation](https://docs.claude.com/en/docs/claude-code/hooks)

## Exit Codes

- **0**: Success (manifest valid and registered)
- **1**: Failure (validation errors or registry update failed)

## Best Practices

1. **Version Control**: Keep hook manifests in your repository (`hooks/` directory)
2. **Review Process**: Require code review for hook changes (they can block operations)
3. **Start with Draft**: Register new hooks with `status: draft`, test them, then promote to `active`
4. **Descriptive Names**: Use clear, kebab-case names that describe the hook's purpose
5. **Appropriate Blocking**: Only set `blocking: true` for critical validations (it will stop operations)
6. **Reasonable Timeouts**: Set realistic timeouts based on hook complexity (avoid too short or too long)
7. **Tag Appropriately**: Use tags for easy filtering and organization
8. **Test Patterns**: Test file patterns thoroughly to avoid unintended matches

## Status

**Active** – This skill is production-ready and actively used in Betty's hook infrastructure.

## Version History

- **0.1.0** (Oct 2025) – Initial implementation with full validation and registry management
