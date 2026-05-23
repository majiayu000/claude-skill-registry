---
name: workflow-tooling
description: Validate and maintain workflow JSON and workflow utilities. Use when: editing workflows in workflows/, validating node connections, updating workflow serialization or loaders.
---

# Workflow Tooling

Use the workflow utilities and validation scripts when editing workflow JSON or serialization logic.

## Start Here

- `docs/user-guide/core-concepts/workflows.md`
- `docs/agent/nodes.md` (node rules that affect workflow JSON)

## Key Files

- Workflow JSON examples: `workflows/`
- Loader/serializer: `src/casare_rpa/utils/workflow/`
  - `workflow_loader.py`
  - `workflow_serializer.py`
  - `workflow_deserializer.py`
  - `workflow_file_io.py`

## Validation and Execution

- Validate baseline workflows: `python scripts/validate_test_workflows.py`
- Execute test workflows: `python scripts/execute_test_workflows.py`
- Sandbox validator: `casare_rpa.infrastructure.ai.agent.sandbox.HeadlessWorkflowSandbox`

## Common Checks

- All node IDs exist and are registered.
- Port names and data types match node definitions.
- Start node exists and graph has no invalid cycles.
