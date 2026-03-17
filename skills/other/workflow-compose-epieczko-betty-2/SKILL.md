---
name: Workflow Compose
description: Executes multi-step workflows by chaining Betty Framework skills.
---

# workflow.compose

## Purpose

Allows declarative execution of Betty Framework workflows by reading a YAML definition and chaining skills like `skill.create`, `skill.define`, and `registry.update`.

Enables complex multi-step processes to be defined once and executed reliably with proper error handling and audit logging.

## Usage

### Basic Usage

```bash
python skills/workflow.compose/workflow_compose.py <path_to_workflow.yaml>
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| workflow_path | string | Yes | Path to the workflow YAML file to execute |

## Workflow YAML Structure

```yaml
# workflows/create_and_register.yaml
name: "Create and Register Skill"
description: "Complete lifecycle: create, validate, and register a new skill"

steps:
  - skill: skill.create
    args: ["workflow.validate", "Validates workflow definitions"]
    required: true

  - skill: skill.define
    args: ["skills/workflow.validate/skill.yaml"]
    required: true

  - skill: registry.update
    args: ["skills/workflow.validate/skill.yaml"]
    required: false  # Continue even if this fails
```

### Workflow Fields

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `name` | No | Workflow name | `"API Design Workflow"` |
| `description` | No | What the workflow does | `"Complete API lifecycle"` |
| `steps` | Yes | Array of steps to execute | See below |

### Step Fields

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `skill` | Yes | Skill name to execute | `api.validate` |
| `args` | No | Arguments to pass to skill | `["specs/api.yaml", "zalando"]` |
| `required` | No | Stop workflow if step fails | `true` (default: `false`) |

## Behavior

1. **Load Workflow**: Parses the workflow YAML file
2. **Sequential Execution**: Runs each step in order
3. **Error Handling**:
   - If `required: true`, workflow stops on failure
   - If `required: false`, workflow continues and logs error
4. **Audit Logging**: Calls `audit.log` skill (if available) for each step
5. **History Tracking**: Records execution history in `/registry/workflow_history.json`

## Outputs

### Success Response

```json
{
  "ok": true,
  "status": "success",
  "errors": [],
  "path": "workflows/create_and_register.yaml",
  "details": {
    "workflow_name": "Create and Register Skill",
    "steps_executed": 3,
    "steps_succeeded": 3,
    "steps_failed": 0,
    "duration_ms": 1234,
    "history_file": "/registry/workflow_history.json"
  }
}
```

### Partial Failure Response

```json
{
  "ok": false,
  "status": "failed",
  "errors": [
    "Step 2 (skill.define) failed: Missing required fields: version"
  ],
  "path": "workflows/create_and_register.yaml",
  "details": {
    "workflow_name": "Create and Register Skill",
    "steps_executed": 2,
    "steps_succeeded": 1,
    "steps_failed": 1,
    "failed_step": "skill.define",
    "failed_step_index": 1
  }
}
```

## Example Workflow Files

### Example 1: Complete Skill Lifecycle

```yaml
# workflows/create_and_register.yaml
name: "Create and Register Skill"
description: "Scaffold, validate, and register a new skill"

steps:
  - skill: skill.create
    args: ["workflow.validate", "Validates workflow definitions"]
    required: true

  - skill: skill.define
    args: ["skills/workflow.validate/skill.yaml"]
    required: true

  - skill: registry.update
    args: ["skills/workflow.validate/skill.yaml"]
    required: true
```

**Execution**:

```bash
$ python skills/workflow.compose/workflow_compose.py workflows/create_and_register.yaml
{
  "ok": true,
  "status": "success",
  "details": {
    "steps_executed": 3,
    "steps_succeeded": 3
  }
}
```

### Example 2: API Design Workflow

```yaml
# workflows/api_design.yaml
name: "API Design Workflow"
description: "Design, validate, and generate models for new API"

steps:
  - skill: api.define
    args: ["user-service", "openapi", "zalando", "specs", "1.0.0"]
    required: true

  - skill: api.validate
    args: ["specs/user-service.openapi.yaml", "zalando", "true"]
    required: true

  - skill: api.generate-models
    args: ["specs/user-service.openapi.yaml", "typescript", "src/models"]
    required: false  # Continue even if model generation fails
```

### Example 3: Multi-Spec Validation

```yaml
# workflows/validate_all_specs.yaml
name: "Validate All API Specs"
description: "Validate all OpenAPI specifications in specs directory"

steps:
  - skill: api.validate
    args: ["specs/users.openapi.yaml", "zalando"]
    required: false

  - skill: api.validate
    args: ["specs/orders.openapi.yaml", "zalando"]
    required: false

  - skill: api.validate
    args: ["specs/payments.openapi.yaml", "zalando"]
    required: false
```

## Workflow History

Execution history is logged to `/registry/workflow_history.json`:

```json
{
  "executions": [
    {
      "workflow_path": "workflows/create_and_register.yaml",
      "workflow_name": "Create and Register Skill",
      "timestamp": "2025-10-23T12:34:56Z",
      "status": "success",
      "steps_executed": 3,
      "steps_succeeded": 3,
      "duration_ms": 1234
    }
  ]
}
```

## Audit Integration

If `audit.log` skill is available, each step execution is logged:

```python
log_audit_entry(
    skill_name="api.validate",
    status="success",
    duration_ms=456,
    metadata={"workflow": "api_design.yaml", "step": 1}
)
```

## Integration

### With workflow.validate

Validate workflow syntax before execution:

```bash
# Validate first
python skills/workflow.validate/workflow_validate.py workflows/my-workflow.yaml

# Then execute
python skills/workflow.compose/workflow_compose.py workflows/my-workflow.yaml
```

### With Hooks

Auto-validate workflows when saved:

```bash
python skills/hook.define/hook_define.py \
  --event on_file_save \
  --pattern "workflows/*.yaml" \
  --command "python skills/workflow.validate/workflow_validate.py {file_path}" \
  --blocking true
```

### In CI/CD

```yaml
# .github/workflows/test.yml
- name: Run workflow tests
  run: |
    python skills/workflow.compose/workflow_compose.py workflows/test_suite.yaml
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Workflow file not found" | Path incorrect | Check workflow file path |
| "Invalid YAML in workflow" | Malformed YAML | Fix YAML syntax errors |
| "Skill handler not found" | Referenced skill doesn't exist | Ensure skill is registered or path is correct |
| "Step X failed" | Skill execution failed | Check skill's error output, fix issues |
| "Skill execution timed out" | Skill took >5 minutes | Optimize skill or increase timeout in code |

## Best Practices

1. **Validate First**: Run `workflow.validate` before executing workflows
2. **Use Required Judiciously**: Only mark critical steps as `required: true`
3. **Small Workflows**: Keep workflows focused on single logical task
4. **Error Handling**: Plan for partial failures in non-required steps
5. **Test Workflows**: Test workflows in development before using in production
6. **Version Control**: Keep workflow files in git

## Files Modified

- **History**: `/registry/workflow_history.json` – Execution history
- **Logs**: Step execution logged to Betty's logging system

## Exit Codes

- **0**: Success (all required steps succeeded)
- **1**: Failure (at least one required step failed)

## Timeout

Each skill has a 5-minute (300 second) timeout by default. If a skill exceeds this, the workflow fails.

## See Also

- **workflow.validate** – Validate workflow syntax ([workflow.validate SKILL.md](../workflow.validate/SKILL.md))
- **Betty Architecture** – [Five-Layer Model](../../docs/betty-architecture.md) for understanding workflows
- **API-Driven Development** – [Example workflows](../../docs/api-driven-development.md)

## Status

**Active** – Production-ready, core orchestration skill

## Version History

- **0.1.0** (Oct 2025) – Initial implementation with sequential execution, error handling, and audit logging
