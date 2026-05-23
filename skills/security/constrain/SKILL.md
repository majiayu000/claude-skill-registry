---
name: constrain
description: Enforce policies, guardrails, and permission boundaries; refuse unsafe actions and apply least privilege. Use when evaluating actions against policies, checking permissions, or reducing scope to safe boundaries.
argument-hint: "[action] [policy_id] [scope] [enforcement_level]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
---

## Intent

Execute **constrain** to evaluate proposed actions against defined policies, enforce permission boundaries, and reduce scope to the minimum required for safe operation. This is the gatekeeper that prevents unsafe actions before they execute.

**Success criteria:**
- All relevant policies evaluated for the proposed action
- Clear allow/deny decision with rationale
- Scope reduced to minimum necessary permissions
- Violation actions documented (block, warn, log)

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `action` | Yes | object | The proposed action to evaluate (capability, target, parameters) |
| `policy_id` | No | string | Specific policy to evaluate against (default: all applicable) |
| `scope` | No | object | Current permission scope to constrain |
| `enforcement_level` | No | enum | strict (block), advisory (warn), audit (log only) |
| `context` | No | object | Additional context for policy evaluation (user, session, etc.) |

## Procedure

1) **Identify applicable policies**: Find all policies relevant to the action
   - Load policy definitions from `.policies/` or policy registry
   - Match action type to policy triggers
   - Consider context (user role, environment, time) for policy selection

2) **Evaluate preconditions**: Check if action meets basic safety requirements
   - Is action within workspace boundaries?
   - Does action target sensitive resources (.env, credentials)?
   - Is checkpoint required but missing?
   - Is approval required but not obtained?

3) **Apply policy rules**: Evaluate each policy condition
   - Parse policy conditions (AND/OR/NOT expressions)
   - Check each condition against action parameters
   - Record which conditions pass and which fail
   - Determine overall policy verdict (allow/deny/conditional)

4) **Reduce scope**: Apply least privilege principle
   - Identify minimum permissions needed for action
   - Remove unnecessary permissions from scope
   - Document removed permissions and rationale

5) **Determine enforcement action**: Based on policy verdict
   - `block`: Prevent action from executing
   - `warn`: Allow but alert user to risk
   - `log`: Record violation but allow action

6) **Ground claims**: Document policy evaluation evidence
   - Format: `policy:<policy_id>:<condition>`, decision rationale
   - Include any scope reductions applied

## Output Contract

Return a structured object:

```yaml
constraints_applied:
  - name: string  # Policy or constraint name
    type: policy | permission | rate_limit | scope
    target: string  # What the constraint applies to
    enforced: boolean  # Whether constraint was enforced
    violation_action: block | warn | log
policy_evaluation:
  policy_id: string  # Which policy was evaluated
  result: allow | deny | conditional
  conditions_met: array[string]  # Conditions that passed
  conditions_failed: array[string]  # Conditions that failed
scope_reduction:
  original_scope: object  # Permissions before constraining
  constrained_scope: object  # Permissions after constraining
  removed_permissions: array[string]  # What was removed
safe_to_proceed: boolean  # Overall go/no-go
blocked_reason: string | null  # Why blocked (if applicable)
confidence: number  # 0.0-1.0
evidence_anchors: ["policy:...", "file:..."]
assumptions: []
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `constraints_applied` | array | List of constraints evaluated and their enforcement |
| `policy_evaluation` | object | Result of primary policy evaluation |
| `scope_reduction` | object | How permissions were reduced |
| `safe_to_proceed` | boolean | Overall decision: can action proceed? |
| `blocked_reason` | string | Explanation if action is blocked |
| `confidence` | number | 0.0-1.0 based on policy coverage |
| `evidence_anchors` | array | References to policies evaluated |
| `assumptions` | array | Policy assumptions made |

## Examples

### Example 1: Constrain File Access to Safe Boundaries

**Input:**
```yaml
action:
  capability: "edit"
  target: "/etc/passwd"
  parameters:
    content: "..."
enforcement_level: strict
```

**Output:**
```yaml
constraints_applied:
  - name: "workspace_boundary"
    type: scope
    target: "/etc/passwd"
    enforced: true
    violation_action: block
  - name: "sensitive_file_protection"
    type: policy
    target: "/etc/passwd"
    enforced: true
    violation_action: block
policy_evaluation:
  policy_id: "sys_file_protection"
  result: deny
  conditions_met: []
  conditions_failed:
    - "path must be within workspace"
    - "system files are read-only"
scope_reduction:
  original_scope:
    paths: ["/**"]
  constrained_scope:
    paths: ["/workspace/**"]
  removed_permissions:
    - "write to system paths"
safe_to_proceed: false
blocked_reason: "Action targets system file outside workspace boundary. Editing /etc/passwd is prohibited."
confidence: 1.0
evidence_anchors:
  - "policy:workspace_boundary:path_check"
  - "policy:sys_file_protection:sensitive_paths"
assumptions: []
```

**Evidence pattern:** Policy definitions, path matching against workspace boundary.

---

### Example 2: Constrain API Call with Rate Limiting

**Input:**
```yaml
action:
  capability: "send"
  target: "https://api.external.com/data"
  parameters:
    method: "POST"
    payload: {...}
context:
  session_id: "abc123"
  requests_this_hour: 95
enforcement_level: advisory
```

**Output:**
```yaml
constraints_applied:
  - name: "external_api_rate_limit"
    type: rate_limit
    target: "api.external.com"
    enforced: true
    violation_action: warn
  - name: "checkpoint_before_send"
    type: policy
    target: "send capability"
    enforced: true
    violation_action: block
policy_evaluation:
  policy_id: "external_communication"
  result: conditional
  conditions_met:
    - "destination is allowed domain"
    - "payload size within limits"
  conditions_failed:
    - "approaching rate limit (95/100 this hour)"
scope_reduction:
  original_scope:
    rate_limit: 100
    burst_allowed: true
  constrained_scope:
    rate_limit: 5
    burst_allowed: false
  removed_permissions:
    - "burst requests"
safe_to_proceed: true
blocked_reason: null
confidence: 0.9
evidence_anchors:
  - "policy:external_api_rate_limit:hourly_quota"
  - "context:requests_this_hour:95"
assumptions:
  - "Rate limit counter is accurate"
  - "Hour boundary resets at :00"
```

---

### Example 3: Constrain Before Act-Plan

**Input:**
```yaml
action:
  capability: "act-plan"
  target: "refactor_handlers_plan"
  parameters:
    plan_id: "plan_20240115_refactor"
enforcement_level: strict
```

**Output:**
```yaml
constraints_applied:
  - name: "checkpoint_required"
    type: policy
    target: "act-plan"
    enforced: true
    violation_action: block
policy_evaluation:
  policy_id: "mutation_safety"
  result: conditional
  conditions_met:
    - "plan exists and is valid"
    - "files in scope are editable"
  conditions_failed:
    - "checkpoint not found for scope"
scope_reduction:
  original_scope:
    mutation_allowed: true
  constrained_scope:
    mutation_allowed: false
  removed_permissions:
    - "file mutation (pending checkpoint)"
safe_to_proceed: false
blocked_reason: "act-plan requires checkpoint. Call 'checkpoint' first with scope matching the plan."
confidence: 1.0
evidence_anchors:
  - "policy:mutation_safety:checkpoint_gate"
  - "composition_patterns.md:CAVR"
assumptions: []
```

## Verification

Apply the following verification patterns:

- [ ] **Policy Coverage**: All applicable policies were evaluated
- [ ] **Evidence Grounding**: Decisions linked to specific policy conditions
- [ ] **Scope Reduction Valid**: Constrained scope is subset of original
- [ ] **Safety Boundary Check**: No sensitive files in allowed scope

**Verification tools:** Read (for policy files), Grep (for policy search)

## Safety Constraints

- `mutation`: false (constrain is evaluation only)
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Always evaluate workspace boundary policy
- Always check for sensitive file patterns (.env, credentials, secrets, .pem, .key)
- Apply strictest enforcement when ambiguous
- Never downgrade enforcement level silently
- Log all policy evaluations for audit

## Composition Patterns

**Commonly follows:**
- `plan` - Constrain the planned actions before checkpoint
- `critique` - After identifying risks, constrain to mitigate

**Commonly precedes:**
- `checkpoint` - After constrain approves, create checkpoint
- `send` - REQUIRED: constrain before any external communication
- `act-plan` - Constrain as part of pre-execution checks

**Anti-patterns:**
- CRITICAL: Never skip constrain before send (no unchecked external comms)
- Never ignore blocked_reason and proceed anyway
- Never silently weaken policy enforcement
- Never evaluate constrain after mutation has begun

**Workflow references:**
- See `reference/composition_patterns.md#digital-twin-sync-loop` for constrain-before-act
- See `reference/composition_patterns.md#risk-assessment` for constrain placement
- See `reference/verification_patterns.md#safety-boundary` for boundary checks
