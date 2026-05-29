---
name: observe
description: Watch and report current state of a target system, process, or entity. Use when monitoring status, inspecting live systems, checking current conditions, or observing runtime behavior.
argument-hint: "[target] [aspects] [duration]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Bash
context: fork
agent: explore
layer: PERCEIVE
---

## Intent

Observe and report the current state of a specified target without modifying it. This is the foundation for situational awareness and state modeling.

**Success criteria:**
- Current state accurately captured with timestamp
- Relevant aspects of the target documented
- At least one evidence anchor per observation
- Uncertainty explicitly noted where state is ambiguous

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `target` | Yes | string | What to observe (file path, URL, process, system) |
| `aspects` | No | array[string] | Specific aspects to focus on (e.g., ["status", "errors", "metrics"]) |
| `depth` | No | string | Observation depth: surface, detailed, exhaustive |

## Procedure

1) **Identify observation target**: Clarify exactly what system, process, or entity to observe
   - Validate target is accessible and observable
   - Determine appropriate observation method (read file, query API, check process)

2) **Select observation aspects**: Determine what properties/attributes to capture
   - If aspects not specified, observe: status, configuration, recent changes, anomalies
   - Prioritize aspects relevant to apparent context or goal

3) **Capture current state**: Execute observation without modifying target
   - Use Read for file-based targets
   - Use Bash for process/system state (ps, systemctl status, etc.)
   - Record timestamp of observation

4) **Document observations**: Structure findings with evidence
   - Note what was observed and when
   - Highlight notable conditions or anomalies
   - Record uncertainty where state is unclear

5) **Ground claims**: Attach evidence anchors to all observations
   - Format: `file:line` for file content
   - Format: `command:output` for system observations

## Output Contract

Return a structured object:

```yaml
observation:
  target: string  # What was observed
  timestamp: string  # ISO 8601 timestamp
  status: string  # Overall status assessment
  aspects:
    - aspect: string  # Name of observed aspect
      value: any  # Observed value or state
      notable: boolean  # Whether this is noteworthy
  anomalies: array[string]  # Unexpected findings
confidence: 0..1  # Based on observation quality
evidence_anchors: ["file:line", "command:output"]
assumptions: []  # What was assumed about the target
next_actions: array[string]  # 0-3 suggested follow-ups
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `observation.target` | string | Identifier of what was observed |
| `observation.timestamp` | string | When observation was made |
| `observation.status` | string | Summary status (healthy, degraded, error, unknown) |
| `observation.aspects` | array | List of observed aspects with values |
| `confidence` | number | 0.0-1.0 based on observation completeness |
| `evidence_anchors` | array[string] | References to raw observation data |

## Examples

### Example 1: Observe Process Status

**Input:**
```yaml
target: "web-server process"
aspects: ["running", "memory", "connections"]
```

**Output:**
```yaml
observation:
  target: "nginx process (PID 1234)"
  timestamp: "2024-01-15T10:30:00Z"
  status: "healthy"
  aspects:
    - aspect: "running"
      value: true
      notable: false
    - aspect: "memory"
      value: "125MB RSS"
      notable: false
    - aspect: "connections"
      value: 847
      notable: true
  anomalies:
    - "Connection count higher than typical (avg: 200)"
confidence: 0.95
evidence_anchors:
  - "command:ps aux | grep nginx"
  - "command:netstat -an | grep :80"
assumptions:
  - "Process identified by name 'nginx'"
next_actions:
  - "Monitor connection trend over time"
  - "Check for connection leak if count continues rising"
```

### Example 2: Observe File State

**Input:**
```yaml
target: "config/database.yml"
aspects: ["content", "permissions", "modified"]
```

**Output:**
```yaml
observation:
  target: "config/database.yml"
  timestamp: "2024-01-15T10:35:00Z"
  status: "present"
  aspects:
    - aspect: "content"
      value: "PostgreSQL configuration with production credentials"
      notable: true
    - aspect: "permissions"
      value: "644"
      notable: true
    - aspect: "modified"
      value: "2024-01-14T15:22:00Z"
      notable: false
  anomalies:
    - "File permissions allow group/other read (sensitive credentials)"
confidence: 0.9
evidence_anchors:
  - "config/database.yml:1-25"
  - "command:ls -la config/database.yml"
assumptions:
  - "File contains database credentials based on content inspection"
next_actions:
  - "Review file permissions for security"
  - "Consider using environment variables for credentials"
```

## Verification

- [ ] Observation timestamp is current (within observation window)
- [ ] At least one aspect was observed and documented
- [ ] Evidence anchors exist for each notable observation
- [ ] Target was not modified during observation
- [ ] Anomalies are supported by evidence

**Verification tools:** Read (to verify file observations)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- NEVER modify the target during observation
- Do not access targets outside authorized scope
- Report access failures rather than attempting workarounds
- Note uncertainty when observations may be stale or incomplete

## Composition Patterns

**Commonly follows:**
- `search` - Observe specific targets found through search
- `retrieve` - Observe content retrieved by reference

**Commonly precedes:**
- `state` - Observations feed into world state modeling
- `detect` - Observations provide data for pattern detection
- `compare` - Observations enable comparison with expected state

**Anti-patterns:**
- Never use observe for modification (use `mutate`)
- Avoid observe for pattern matching (use `detect`)

**Workflow references:**
- See `reference/workflow_catalog.yaml#debug_code_change` for observation in debugging
- See `reference/workflow_catalog.yaml#world_model_build` for observation in modeling
