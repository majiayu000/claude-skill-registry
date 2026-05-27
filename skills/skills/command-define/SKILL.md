---
name: Command Define
description: Validates and registers command manifest files (YAML) to integrate new slash commands into Betty.
---

# command.define Skill

Validates and registers command manifest files (YAML) to integrate new slash commands into Betty.

## Purpose

The `command.define` skill acts as the "compiler" for Betty Commands. It ensures a command manifest meets all schema requirements and then updates the Command Registry (`/registry/commands.json`) with the new command.

This skill is part of Betty's Layer 1 (Commands) infrastructure, enabling developers to create user-facing slash commands that delegate to agents, workflows, or skills.

## Usage

```bash
python skills/command.define/command_define.py <path_to_command.yaml>
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| manifest_path | string | Yes | Path to the command manifest YAML to validate and register |

## Behavior

1. **Schema Validation** – Checks that required fields (`name`, `version`, `description`, `execution`) are present and correctly formatted (e.g., name must start with `/`).

2. **Parameter Verification** – Verifies each parameter in the manifest has `name`, `type`, and `description`, and that the execution target (agent/skill/workflow) actually exists in the system.

3. **Registry Update** – On success, adds the command entry to `/registry/commands.json` with status `active`.

## Validation Rules

### Required Fields

- **name**: Command name (must start with `/`, e.g., `/api-design`)
- **version**: Semantic version (e.g., `0.1.0`)
- **description**: Human-readable description of what the command does
- **execution**: Object specifying how to execute the command

### Execution Configuration

The `execution` field must contain:

- **type**: One of `skill`, `agent`, or `workflow`
- **target**: Name of the skill/agent/workflow to invoke
  - For skills: Must exist in `/registry/skills.json`
  - For agents: Must exist in `/registry/agents.json`
  - For workflows: File must exist at `/workflows/{target}.yaml`

### Optional Fields

- **parameters**: Array of parameter objects, each with:
  - `name` (required): Parameter name
  - `type` (required): Parameter type (string, number, boolean, etc.)
  - `required` (optional): Whether parameter is required
  - `description` (optional): Parameter description
  - `default` (optional): Default value
- **status**: Command status (`draft` or `active`, defaults to `draft`)
- **tags**: Array of tags for categorization

## Outputs

### Success Response

```json
{
  "ok": true,
  "status": "registered",
  "errors": [],
  "path": "commands/hello.yaml",
  "details": {
    "valid": true,
    "status": "registered",
    "registry_updated": true,
    "manifest": {
      "name": "/hello",
      "version": "0.1.0",
      "description": "Prints Hello World",
      "execution": {
        "type": "skill",
        "target": "test.hello"
      }
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
    "Skill 'test.hello' not found in skill registry"
  ],
  "path": "commands/hello.yaml",
  "details": {
    "valid": false,
    "errors": [
      "Skill 'test.hello' not found in skill registry"
    ],
    "path": "commands/hello.yaml"
  }
}
```

## Example

### Valid Command Manifest

```yaml
# commands/api-design.yaml
name: /api-design
version: 0.1.0
description: "Design a new API following enterprise guidelines"

parameters:
  - name: service_name
    type: string
    required: true
    description: "Name of the service/API"

  - name: spec_type
    type: string
    required: false
    default: openapi
    description: "Type of API specification (openapi or asyncapi)"

execution:
  type: agent
  target: api.designer

status: active
tags: [api, design, enterprise]
```

### Running the Validator

```bash
$ python skills/command.define/command_define.py commands/api-design.yaml
{
  "ok": true,
  "status": "registered",
  "errors": [],
  "path": "commands/api-design.yaml",
  "details": {
    "valid": true,
    "status": "registered",
    "registry_updated": true
  }
}
```

### Invalid Command Example

If the target agent doesn't exist:

```bash
$ python skills/command.define/command_define.py commands/hello.yaml
{
  "ok": false,
  "status": "failed",
  "errors": [
    "Agent 'api.designer' not found in agent registry"
  ],
  "path": "commands/hello.yaml"
}
```

## Integration

### With Workflows

Commands can be validated as part of a workflow:

```yaml
# workflows/register_command.yaml
steps:
  - skill: command.define
    args:
      - "commands/my-command.yaml"
    required: true
```

### With Hooks

Validate commands automatically when they're edited:

```bash
# Create a hook that validates command manifests on save
python skills/hook.define/hook_define.py \
  --event on_file_save \
  --pattern "commands/**/*.yaml" \
  --command "python skills/command.define/command_define.py" \
  --blocking true
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Missing required fields: name" | Command manifest missing `name` field | Add `name` field with value starting with `/` |
| "Invalid name: Command name must start with /" | Name doesn't start with `/` | Update name to start with `/` (e.g., `/api-design`) |
| "Skill 'X' not found in skill registry" | Referenced skill doesn't exist | Register the skill first using `skill.define` or fix the target name |
| "Agent 'X' not found in agent registry" | Referenced agent doesn't exist | Register the agent first using `agent.define` or fix the target name |
| "Workflow file not found" | Referenced workflow file doesn't exist | Create the workflow file at `/workflows/{target}.yaml` |
| "execution.type is required" | Missing execution type | Add `execution.type` field with value `skill`, `agent`, or `workflow` |

## See Also

- **Command Manifest Schema** – documented in [Command and Hook Infrastructure](../../docs/COMMAND_HOOK_INFRASTRUCTURE.md)
- **Slash Commands Usage** – overview in [.claude/commands/README.md](../../.claude/commands/README.md)
- **Betty Architecture** – [Five-Layer Model](../../docs/betty-architecture.md) for understanding how commands fit into the framework
- **agent.define** – for validating and registering agents that commands can invoke
- **hook.define** – for creating validation hooks that can trigger command validation

## Exit Codes

- **0**: Success (manifest valid and registered)
- **1**: Failure (validation errors or registry update failed)

## Files Modified

- **Registry**: `/registry/commands.json` – updated with new or modified command entry
- **Logs**: Command validation and registration logged to Betty's logging system

## Dependencies

- **Skill Registry** (`/registry/skills.json`) – for validating skill targets
- **Agent Registry** (`/registry/agents.json`) – for validating agent targets
- **Workflow Files** (`/workflows/*.yaml`) – for validating workflow targets

## Status

**Active** – This skill is production-ready and actively used in Betty's command infrastructure.

## Version History

- **0.1.0** (Oct 2025) – Initial implementation with full validation and registry management
