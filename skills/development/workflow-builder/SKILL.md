---
name: workflow-builder
description: 'Scaffold an explicit one-shot workflow adapter without lifecycle authority. Triggers: "build a workflow adapter", "scaffold a one-shot workflow".'
practices:
- pragmatic-programmer
- hexagonal-architecture
- agile-manifesto
hexagonal_role: supporting
consumes: []
produces:
- workflow-script
context_rel:
- kind: customer-of
  with: automation-shape-routing
- kind: shared-kernel
  with: operationalize
skill_api_version: 1
context:
  window: fork
  intent:
    mode: questions
  sections:
    exclude:
    - HISTORY
  intel_scope: topic
metadata:
  capabilities: [workflow_builder]
  effects: []
  canonical_status: canonical
  disposition: keep_specialist
  tier: meta
  dependencies: []
output_contract: a runnable one-shot workflow with explicit inputs and outputs
---
# Workflow Builder — one-shot adapter authoring

Build a thin adapter only when a caller needs to dispatch an explicit set of
independent operations. A workflow is convenience code, never a correctness or
lifecycle authority.

## Contract

- Inputs, executors, write scopes, and outputs are supplied explicitly.
- Each operation is dispatched at most once.
- Parallel operations must have caller-proven disjoint write scopes.
- The workflow reports per-operation output or error and then stops.
- It contains no work selection, retry, budget, queue, tracker, validation, Git,
  integration, closure, release, or delivery logic.
- Optional substrate state cannot be translated into RPI or verdict state.

Prefer the smallest script supported by the target runtime. Include a dry-run or
fixture demonstrating exact dispatch count and failure reporting. Do not create a
new framework or SDK abstraction unless the caller explicitly requests one.
