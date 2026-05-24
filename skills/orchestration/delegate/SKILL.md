---
name: delegate
description: Split work across subagents with explicit contracts, interfaces, and merge strategies. Use when parallelizing tasks, distributing workload, or orchestrating multi-agent workflows.
argument-hint: "[task] [agents] [contracts]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
---

## Intent

Delegate a complex task to one or more subagents by defining clear contracts, input/output interfaces, and strategies for merging results. Ensure coordinated execution with conflict resolution.

**Success criteria:**
- Task decomposed into delegatable subtasks
- Each subtask has explicit contract (inputs, outputs, constraints)
- Interface between tasks is well-defined
- Merge strategy handles conflicts and failures
- Dependencies between subtasks are clear

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `task` | Yes | string or object | The overall task to delegate |
| `agents` | No | array | Available agents/workers for delegation |
| `constraints` | No | object | Global constraints (timeout, resource limits) |
| `merge_strategy` | No | string | How to combine results (first_wins, consensus, aggregate) |
| `failure_policy` | No | string | What to do on subtask failure (abort, continue, retry) |

## Procedure

1) **Analyze task**: Understand the overall objective
   - Identify the goal and success criteria
   - Determine if task is parallelizable
   - Identify shared state or resources
   - Assess complexity and scope

2) **Decompose into subtasks**: Break into delegatable units
   - Each subtask should be independently executable
   - Minimize dependencies between subtasks
   - Identify natural parallelization boundaries
   - Use `decompose` capability patterns

3) **Define contracts**: Specify expectations for each subtask
   - Input: what data/context each subtask receives
   - Output: what each subtask must produce
   - Constraints: limits on time, resources, scope
   - Verification: how to check subtask completion

4) **Design interfaces**: Specify data flow between subtasks
   - Format of inputs and outputs
   - Required fields and optional extensions
   - Error formats and status codes
   - Handoff protocols

5) **Plan merge strategy**: How to combine results
   - Handle successful completions
   - Resolve conflicts between subtask outputs
   - Aggregate partial results
   - Determine final output format

6) **Handle failures**: Define recovery behavior
   - What happens if a subtask fails
   - Retry policies and limits
   - Fallback strategies
   - Partial result handling

7) **Establish coordination**: Define execution order
   - Parallel vs sequential execution
   - Dependency ordering
   - Synchronization points
   - Progress tracking

## Output Contract

Return a structured object:

```yaml
delegation:
  task: string  # Original task description
  delegated_to: array  # List of agents/subtasks
  status: pending | running | completed | failed
subtasks:
  - id: string  # Subtask identifier
    agent: string  # Assigned agent
    contract:
      inputs: object  # What subtask receives
      outputs: object  # What subtask must produce
      constraints: object  # Limits and requirements
      verification: string  # How to verify completion
    dependencies: array[string]  # Subtask IDs this depends on
    status: pending | running | completed | failed
    result: object | null  # Subtask output when complete
interfaces:
  - from: string  # Source subtask
    to: string  # Destination subtask
    format: object  # Data format specification
    required_fields: array[string]
merge_plan:
  strategy: first_wins | consensus | aggregate | custom
  conflict_resolution: string  # How to handle conflicts
  final_output_format: object  # Expected merged result
failure_handling:
  policy: abort | continue | retry
  max_retries: integer
  fallback: string | null
handoff_context:
  - key: string  # Context key
    value: object  # Shared context data
confidence: 0..1
evidence_anchors: ["task:analysis", "agent:capability"]
assumptions: []
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `delegation` | object | Overall delegation summary |
| `subtasks` | array | Individual subtask definitions with contracts |
| `interfaces` | array | Data flow between subtasks |
| `merge_plan` | object | Strategy for combining results |
| `failure_handling` | object | Recovery policies |
| `handoff_context` | array | Shared context for all subtasks |
| `confidence` | number | 0.0-1.0 based on delegation clarity |
| `evidence_anchors` | array | References supporting delegation design |
| `assumptions` | array | Explicit assumptions about agents/capabilities |

## Examples

### Example 1: Parallel Code Review

**Input:**
```yaml
task: "Review pull request #123 for security, performance, and style"
agents:
  - id: "security-agent"
    capabilities: ["security-analysis", "vulnerability-detection"]
  - id: "perf-agent"
    capabilities: ["performance-analysis", "profiling"]
  - id: "style-agent"
    capabilities: ["lint", "style-check"]
constraints:
  timeout: "10m"
  max_issues_per_category: 20
```

**Output:**
```yaml
delegation:
  task: "Review pull request #123"
  delegated_to: ["security-agent", "perf-agent", "style-agent"]
  status: pending
subtasks:
  - id: "security-review"
    agent: "security-agent"
    contract:
      inputs:
        pr_number: 123
        files: ["src/**/*.ts"]
        focus: "security"
      outputs:
        issues: "array of {severity, file, line, description}"
        summary: "string"
        passed: "boolean"
      constraints:
        timeout: "5m"
        max_issues: 20
      verification: "issues array is valid, severity in [low, medium, high, critical]"
    dependencies: []
    status: pending
    result: null
  - id: "perf-review"
    agent: "perf-agent"
    contract:
      inputs:
        pr_number: 123
        files: ["src/**/*.ts"]
        focus: "performance"
      outputs:
        issues: "array of {severity, file, line, description}"
        metrics: "object with timing estimates"
        passed: "boolean"
      constraints:
        timeout: "5m"
        max_issues: 20
      verification: "issues array is valid, metrics object present"
    dependencies: []
    status: pending
    result: null
  - id: "style-review"
    agent: "style-agent"
    contract:
      inputs:
        pr_number: 123
        files: ["src/**/*.ts"]
        focus: "style"
      outputs:
        issues: "array of {severity, file, line, description}"
        passed: "boolean"
      constraints:
        timeout: "3m"
        max_issues: 20
      verification: "issues array is valid"
    dependencies: []
    status: pending
    result: null
interfaces:
  - from: "all_subtasks"
    to: "merge"
    format:
      issues: "array"
      passed: "boolean"
    required_fields: ["issues", "passed"]
merge_plan:
  strategy: aggregate
  conflict_resolution: "Combine all issues, AND passed flags"
  final_output_format:
    all_issues: "array (combined)"
    passed: "boolean (all must pass)"
    summary: "string (generated)"
failure_handling:
  policy: continue
  max_retries: 1
  fallback: "Return partial results with failed subtask noted"
handoff_context:
  - key: "repository"
    value: { "owner": "org", "repo": "project" }
  - key: "base_branch"
    value: "main"
confidence: 0.9
evidence_anchors:
  - "task:pr-review-decomposition"
  - "agent:security-agent:has-security-analysis"
assumptions:
  - "All agents have access to repository"
  - "PR #123 exists and is accessible"
```

**Evidence pattern:** Task analysis informed decomposition, agent capabilities matched to subtasks.

---

### Example 2: Sequential Data Pipeline

**Input:**
```yaml
task: "Process customer data: validate, enrich, and store"
agents:
  - id: "validator"
  - id: "enricher"
  - id: "persister"
merge_strategy: "sequential"
```

**Output:**
```yaml
delegation:
  task: "Process customer data pipeline"
  delegated_to: ["validator", "enricher", "persister"]
  status: pending
subtasks:
  - id: "validate-data"
    agent: "validator"
    contract:
      inputs:
        data: "raw customer records"
      outputs:
        valid_records: "array of validated records"
        invalid_records: "array with error reasons"
      constraints:
        schema: "customer_v2"
      verification: "All valid_records match schema"
    dependencies: []
    status: pending
    result: null
  - id: "enrich-data"
    agent: "enricher"
    contract:
      inputs:
        records: "${validate-data.valid_records}"
      outputs:
        enriched_records: "array with added fields"
      constraints:
        enrich_fields: ["company_size", "industry"]
      verification: "All records have enrich_fields populated"
    dependencies: ["validate-data"]
    status: pending
    result: null
  - id: "store-data"
    agent: "persister"
    contract:
      inputs:
        records: "${enrich-data.enriched_records}"
      outputs:
        stored_count: "integer"
        storage_location: "string"
      constraints:
        destination: "customer_db"
      verification: "stored_count matches input count"
    dependencies: ["enrich-data"]
    status: pending
    result: null
interfaces:
  - from: "validate-data"
    to: "enrich-data"
    format:
      records: "array of customer objects"
    required_fields: ["id", "name", "email"]
  - from: "enrich-data"
    to: "store-data"
    format:
      records: "array of enriched customer objects"
    required_fields: ["id", "name", "email", "company_size", "industry"]
merge_plan:
  strategy: custom
  conflict_resolution: "N/A - sequential pipeline"
  final_output_format:
    processed: "integer"
    stored: "integer"
    errors: "array"
failure_handling:
  policy: abort
  max_retries: 0
  fallback: null
handoff_context:
  - key: "batch_id"
    value: "batch-2024-01-15"
confidence: 0.85
evidence_anchors:
  - "task:pipeline-stages"
assumptions:
  - "Enrichment service is available"
  - "Database has capacity for new records"
```

## Verification

- [ ] All subtasks have complete contracts
- [ ] Dependencies form a valid DAG
- [ ] Interfaces are compatible between connected subtasks
- [ ] Merge strategy handles all expected outputs
- [ ] Failure handling is defined

**Verification tools:** Read (for contract validation)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Never delegate without explicit contracts
- Ensure all subtasks have verification criteria
- Define failure handling before delegation
- Validate interface compatibility
- Do not delegate tasks requiring approval without noting it

## Composition Patterns

**Commonly follows:**
- `plan` - Delegation is often part of plan execution (REQUIRES plan)
- `decompose` - Break task before delegating
- `prioritize` - Order subtasks by importance

**Commonly precedes:**
- `synchronize` - Merge results from delegated subtasks
- `verify` - Check all subtasks completed correctly
- `audit` - Record delegation and outcomes

**Anti-patterns:**
- Never delegate without failure handling
- Never delegate mutating tasks without noting safety requirements
- Avoid circular dependencies between subtasks

**Workflow references:**
- See `reference/composition_patterns.md#enrichment-pipeline` for parallel delegation
