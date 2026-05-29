---
name: Workflow Validate
description: Validates workflow YAML files to ensure structure and schema correctness.
---

# Workflow Validate

## Purpose
Ensures that workflow YAML files are valid before execution.
Checks required fields (`steps`, `skill`, `args`) and field types.

## How to Use
```bash
python skills/workflow.validate/workflow_validate.py workflows/example.yaml
```

## Inputs

* `workflow_path` – Path to the workflow file.

## Outputs

* JSON printed to stdout with `ok`, `errors`, `status`, and `path` fields.

## Example

Input (`invalid_workflow.yaml`):

```yaml
steps:
  - args: ["foo"]
```

Output:

```json
{
  "valid": false,
  "errors": ["Step 1 missing 'skill'"],
  "status": "failed"
}
```

## Dependencies

* `context.schema`

## Version

v0.1.0
