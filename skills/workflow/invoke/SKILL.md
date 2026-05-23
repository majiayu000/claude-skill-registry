---
name: invoke
description: Execute a composed workflow by name. Use when running predefined workflows, orchestrating multi-step processes, or delegating to workflow templates.
argument-hint: "[workflow] [input] [options]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Bash, Edit, Write
context: fork
agent: general-purpose
layer: COORDINATE
---

## Intent

Invoke a predefined workflow by name, passing input parameters and receiving aggregated results. This enables reuse of common capability compositions and supports hierarchical workflow organization.

**Success criteria:**
- Workflow executed according to definition
- All steps completed or gracefully failed
- Results aggregated and returned
- Execution trace available for debugging

**Compatible schemas:**
- `schemas/output_schema.yaml`
- `reference/workflow_catalog.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `workflow` | Yes | string | Workflow name from workflow catalog |
| `input` | No | object | Input parameters for workflow |
| `options` | No | object | Execution options (timeout, retry, etc.) |

## Procedure

1) **Resolve workflow**: Find workflow definition
   - Look up workflow in workflow_catalog.yaml
   - Validate workflow exists
   - Load workflow specification

2) **Validate inputs**: Check input against workflow schema
   - Verify required inputs provided
   - Validate input types
   - Apply defaults for missing optional inputs

3) **Initialize execution**: Set up workflow context
   - Create execution ID
   - Initialize step tracking
   - Set up data flow context

4) **Execute steps**: Run workflow steps in order
   - Execute each capability in sequence
   - Handle step dependencies
   - Propagate data between steps via store_as

5) **Handle failures**: Respond to step failures
   - Execute failure_modes actions
   - Attempt recovery if specified
   - Trigger rollback if needed

6) **Aggregate results**: Collect workflow outputs
   - Gather outputs from each step
   - Evaluate success criteria
   - Compute overall result

7) **Return results**: Provide complete execution record
   - Include all step outputs
   - Provide execution trace
   - Report success/failure

## Output Contract

Return a structured object:

```yaml
result:
  success: boolean  # Whether workflow completed successfully
  workflow: string  # Workflow that was executed
  output: any  # Primary workflow output
steps_executed:
  - step_id: string  # Capability name
    status: string  # success, failed, skipped
    output_key: string  # store_as value
    duration: string
execution:
  id: string  # Unique execution ID
  started_at: string  # ISO timestamp
  completed_at: string  # ISO timestamp
  duration: string  # Total execution time
failures:
  - step: string
    error: string
    recovery_attempted: boolean
evidence_anchors: ["workflow:step:output"]
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `result.success` | boolean | Whether workflow completed |
| `result.workflow` | string | Name of executed workflow |
| `result.output` | any | Final workflow output |
| `steps_executed` | array | Record of each step's execution |
| `execution` | object | Execution metadata |
| `failures` | array | Any failures encountered |

## Examples

### Example 1: Invoke World Model Build

**Input:**
```yaml
workflow: "world_model_build"
input:
  domain: "user authentication"
  constraints:
    scope: "backend services"
```

**Output:**
```yaml
result:
  success: true
  workflow: "world_model_build"
  output:
    world_state:
      world_id: "auth-model-001"
      entities: 12
      relationships: 18
    summary: "Authentication system model with 12 entities"
steps_executed:
  - step_id: "retrieve"
    status: "success"
    output_key: "retrieve_out"
    duration: "1.2s"
  - step_id: "observe"
    status: "success"
    output_key: "observe_out"
    duration: "2.5s"
  - step_id: "state"
    status: "success"
    output_key: "state_out"
    duration: "3.1s"
  - step_id: "transition"
    status: "success"
    output_key: "transition_out"
    duration: "2.8s"
  - step_id: "ground"
    status: "success"
    output_key: "ground_out"
    duration: "1.5s"
  - step_id: "simulate"
    status: "success"
    output_key: "simulate_out"
    duration: "4.2s"
  - step_id: "explain"
    status: "success"
    output_key: "explain_out"
    duration: "1.1s"
execution:
  id: "exec-20240115-001"
  started_at: "2024-01-15T10:00:00Z"
  completed_at: "2024-01-15T10:00:16Z"
  duration: "16.4s"
failures: []
evidence_anchors:
  - "workflow:world_model_build:retrieve_out"
  - "workflow:world_model_build:state_out"
```

### Example 2: Invoke with Failure Recovery

**Input:**
```yaml
workflow: "digital_twin_sync_loop"
input:
  world_state: "${previous_state}"
options:
  max_retries: 3
```

**Output:**
```yaml
result:
  success: true
  workflow: "digital_twin_sync_loop"
  output:
    drift_detected: true
    actions_taken: 2
    verification: "PASS"
steps_executed:
  - step_id: "receive"
    status: "success"
    output_key: "receive_out"
    duration: "0.5s"
  - step_id: "detect"
    status: "success"
    output_key: "detect_out"
    duration: "1.2s"
  - step_id: "measure"
    status: "success"
    output_key: "measure_out"
    duration: "0.8s"
  - step_id: "plan"
    status: "success"
    output_key: "plan_out"
    duration: "2.1s"
  - step_id: "checkpoint"
    status: "success"
    output_key: "checkpoint_out"
    duration: "0.3s"
  - step_id: "mutate"
    status: "failed"
    output_key: "mutate_out"
    duration: "1.5s"
  - step_id: "mutate"
    status: "success"
    output_key: "mutate_out"
    duration: "1.2s"
  - step_id: "verify"
    status: "success"
    output_key: "verify_out"
    duration: "2.0s"
execution:
  id: "exec-20240115-002"
  started_at: "2024-01-15T11:00:00Z"
  completed_at: "2024-01-15T11:00:10Z"
  duration: "9.6s"
failures:
  - step: "mutate"
    error: "Connection timeout"
    recovery_attempted: true
evidence_anchors:
  - "workflow:digital_twin_sync_loop:verify_out"
```

### Example 3: Nested Workflow Invocation

**Input:**
```yaml
workflow: "digital_twin_bootstrap"
input:
  domain: "payment processing"
```

**Output:**
```yaml
result:
  success: true
  workflow: "digital_twin_bootstrap"
  output:
    world_model: "${world_model_out}"
    first_sync: "${sync_out}"
steps_executed:
  - step_id: "invoke"
    status: "success"
    output_key: "world_model_out"
    duration: "18.5s"
    nested_workflow: "world_model_build"
  - step_id: "invoke"
    status: "success"
    output_key: "sync_out"
    duration: "12.3s"
    nested_workflow: "digital_twin_sync_loop"
execution:
  id: "exec-20240115-003"
  started_at: "2024-01-15T12:00:00Z"
  completed_at: "2024-01-15T12:00:31Z"
  duration: "30.8s"
failures: []
evidence_anchors:
  - "workflow:digital_twin_bootstrap:world_model_out"
  - "workflow:digital_twin_bootstrap:sync_out"
```

## Verification

- [ ] Workflow name resolves to valid definition
- [ ] All required inputs provided
- [ ] Each step executed or skipped with reason
- [ ] Failures handled according to failure_modes
- [ ] Success criteria evaluated

**Verification tools:** Read (to verify workflow catalog)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: medium

**Capability-specific rules:**
- Workflow must exist in workflow_catalog.yaml
- Respect step-level safety constraints
- Propagate checkpoint requirements to mutating steps
- Do not modify workflow definitions at runtime
- Log all step executions for audit

## Composition Patterns

**Commonly follows:**
- `plan` - Invoke workflow to execute plan
- `decompose` - Invoke sub-workflows for sub-problems

**Commonly precedes:**
- `verify` - Verify workflow results
- `audit` - Record workflow execution
- `explain` - Explain workflow results

**Anti-patterns:**
- Avoid deeply nested invocations (max 3 levels)
- Never invoke workflows recursively
- Do not invoke without understanding workflow effects

**Workflow references:**
- See `reference/workflow_catalog.yaml#digital_twin_bootstrap` for nested invocation
- This capability is the entry point for all workflow execution
