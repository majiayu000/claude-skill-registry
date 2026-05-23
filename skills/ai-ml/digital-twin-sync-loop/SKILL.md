---
name: digital-twin-sync-workflow
description: Run the digital twin sync loop to synchronize real-world signals with a digital model. Use when updating digital twins, detecting drift, managing real-time state synchronization, or maintaining model-reality alignment.
argument-hint: "[sources] [world_id] [constraints]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Web, Bash, Edit, Git
context: fork
agent: general-purpose
---

## Intent

Synchronize a **digital twin** with real-time signals and keep it **grounded, safe, and auditable**. This workflow maintains alignment between the real world and its digital representation.

This workflow is designed to **model both real and digital systems** using the canonical world-state schema:
- `reference/world_state_schema.yaml`

**Success criteria:**
- Twin snapshot updated with latest signals
- All drift and anomalies detected and documented
- Risk assessed and forecasted with evidence
- Actions executed only after checkpoint and approval
- Complete audit trail with provenance
- Rollback available if verification fails

**Compatible schemas:**
- `reference/world_state_schema.yaml`
- `reference/event_schema.yaml`
- `reference/workflow_catalog.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `sources` | Yes | array | Data sources to ingest (APIs, files, streams, sensors) |
| `world_id` | Yes | string | Identifier for the digital twin being synchronized |
| `constraints` | No | object | Policy limits, thresholds, timing constraints |
| `prior_snapshot` | No | object | Previous twin state for delta computation |
| `sync_mode` | No | enum | full \| incremental \| delta_only (default: incremental) |

## Preconditions (hard gates)

1. **Policy constraints must exist** (`/constrain`)
2. **Checkpoint before mutation** (`/checkpoint`)
3. Any external side effects require explicit approval (do not `send` without approval)

## Procedure

0) **Ensure baseline exists**: If no twin snapshot exists, start with `/world-model-workflow`

Then execute the sync loop:

1) **Invoke `/receive`** → store `receive_out`
   - Ingest signals from configured sources

2) **Invoke `/transform`** to normalize to canonical events → `transform_out`
   - Convert raw signals to event schema format

3) **Invoke `/integrate`** to merge events with prior twin snapshot → `integrate_out`
   - Combine new events with existing state

4) **Invoke `/identity-resolution`** → `identity_resolution_out`
   - Resolve entity references across sources

5) **Invoke `/world-state`** producing canonical snapshot → `world_state_out`
   - Generate updated twin representation

6) **Invoke `/state-transition`** apply rules → `state_transition_out`
   - Apply business rules and state machine logic

7) **Invoke `/detect-anomaly`** drift detection → `detect_anomaly_out`
   - Identify deviations from expected behavior

8) **Invoke `/estimate-risk`** risk estimate → `estimate_risk_out`
   - Assess current risk based on anomalies

9) **Invoke `/forecast-risk`** risk forecast → `forecast_risk_out`
   - Project future risk trajectory

10) **Invoke `/plan`** remediation plan + verification criteria + rollback plan → `plan_out`
    - Create action plan if intervention needed

11) **Invoke `/constrain`** enforce policy constraints → `constrain_out`
    - Validate plan against policy limits

12) **Invoke `/checkpoint`** create mutation gate marker → `checkpoint_out`
    - Establish restore point before action

13) **Invoke `/act-plan`** execute if safe/approved → `act_plan_out`
    - Execute remediation actions

14) **Invoke `/verify`** PASS/FAIL → `verify_out`
    - Confirm actions achieved intended outcome

15) **Invoke `/audit`** provenance + tool log → `audit_out`
    - Record complete audit trail

16) **If FAIL or side effects** → `/rollback` → `rollback_out`
    - Restore previous state if needed

17) **Invoke `/summarize`** decision-ready report → `summarize_out`
    - Generate executive summary

## Output Contract

Return a structured object:

```yaml
workflow_id: string  # Unique sync execution ID
world_id: string  # Digital twin identifier
sync_timestamp: string  # ISO timestamp of sync
status: synced | drift_detected | action_taken | rolled_back | failed
twin_snapshot:
  version: string
  state: object  # Canonical world state
  hash: string  # Integrity hash
  evidence_anchors: array[string]
drift_report:
  anomalies_detected: integer
  severity: low | medium | high | critical
  triggers: array[string]
  evidence_anchors: array[string]
risk_assessment:
  current_risk: number  # 0.0-1.0
  forecasted_risk: number  # 0.0-1.0
  risk_factors: array[string]
  evidence_anchors: array[string]
actions:
  executed: boolean
  plan_summary: string
  changes: array[string]
  safety_gates_passed: boolean
  evidence_anchors: array[string]
verification:
  result: PASS | FAIL | SKIPPED
  criteria_met: array[string]
  evidence_anchors: array[string]
audit:
  log_path: string
  provenance_chain: array[string]
  evidence_anchors: array[string]
rollback:
  available: boolean
  executed: boolean
  restore_point: string | null
  command: string | null
next_sync:
  recommended_interval: string  # e.g., "5m", "1h"
  triggers: array[string]  # Conditions for immediate resync
confidence: number  # 0.0-1.0
evidence_anchors: array[string]
assumptions: array[string]
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `workflow_id` | string | Unique identifier for this sync execution |
| `world_id` | string | Digital twin being synchronized |
| `twin_snapshot` | object | Updated canonical world state with integrity hash |
| `drift_report` | object | Detected anomalies and their severity |
| `risk_assessment` | object | Current and forecasted risk levels |
| `actions` | object | What remediation was taken (if any) |
| `verification` | object | Whether actions achieved intended outcome |
| `audit` | object | Complete provenance and audit trail |
| `rollback` | object | Rollback availability and status |
| `next_sync` | object | Recommended timing for next synchronization |
| `confidence` | number | 0.0-1.0 based on evidence quality |
| `evidence_anchors` | array | All evidence references collected |
| `assumptions` | array | Explicit assumptions made during sync |

## Examples

### Example 1: IoT Sensor Sync with Anomaly Detection

**Input:**
```yaml
sources:
  - type: mqtt
    endpoint: "mqtt://sensors.example.com/floor-3"
  - type: api
    endpoint: "https://building.api/hvac/status"
world_id: "building-floor-3-twin"
constraints:
  max_drift_threshold: 0.15
  require_approval_above_risk: 0.7
sync_mode: incremental
```

**Output:**
```yaml
workflow_id: "sync_20240115_160000_floor3"
world_id: "building-floor-3-twin"
sync_timestamp: "2024-01-15T16:00:00Z"
status: drift_detected
twin_snapshot:
  version: "v47"
  state:
    entities:
      - id: "hvac-unit-3a"
        type: "hvac_controller"
        temperature: 23.5
        setpoint: 22.0
        status: "cooling"
      - id: "sensor-temp-301"
        type: "temperature_sensor"
        reading: 24.1
        last_updated: "2024-01-15T15:59:45Z"
    relationships:
      - subject: "hvac-unit-3a"
        predicate: "controls"
        object: "zone-3a"
  hash: "sha256:abc123def456..."
  evidence_anchors:
    - "tool:mqtt:sensors.example.com/floor-3"
    - "tool:api:building.api/hvac/status"
drift_report:
  anomalies_detected: 1
  severity: medium
  triggers:
    - "Temperature 1.5°C above setpoint for >10 minutes"
  evidence_anchors:
    - "file:state/floor-3-twin-v46.yaml:temperature_history"
    - "tool:detect-anomaly:threshold_breach"
risk_assessment:
  current_risk: 0.35
  forecasted_risk: 0.45
  risk_factors:
    - "HVAC may be undersized for current load"
    - "Trending toward comfort threshold breach"
  evidence_anchors:
    - "tool:estimate-risk:hvac_capacity"
    - "tool:forecast-risk:temperature_trend"
actions:
  executed: false
  plan_summary: "Monitor for 15 more minutes before intervention"
  changes: []
  safety_gates_passed: true
  evidence_anchors:
    - "tool:plan:remediation_decision"
verification:
  result: SKIPPED
  criteria_met: []
  evidence_anchors: []
audit:
  log_path: ".claude/audit/sync_20240115_160000_floor3.log"
  provenance_chain:
    - "mqtt://sensors.example.com → receive"
    - "receive → transform"
    - "transform → integrate"
    - "integrate → world-state"
  evidence_anchors:
    - "file:.claude/audit/sync_20240115_160000_floor3.log"
rollback:
  available: false
  executed: false
  restore_point: null
  command: null
next_sync:
  recommended_interval: "5m"
  triggers:
    - "Temperature exceeds 25°C"
    - "HVAC status changes"
confidence: 0.88
evidence_anchors:
  - "tool:mqtt:sensors.example.com/floor-3"
  - "tool:api:building.api/hvac/status"
  - "tool:detect-anomaly:threshold_breach"
  - "file:.claude/audit/sync_20240115_160000_floor3.log"
assumptions:
  - "Sensor readings are accurate within ±0.1°C"
  - "MQTT connection is reliable"
  - "Building API returns real-time status"
```

**Evidence pattern:** Multi-source signal ingestion, anomaly detection against historical baseline, risk forecasting with trend analysis.

## Verification

- [ ] **Source Ingestion**: All configured sources successfully polled
- [ ] **Transform Success**: Events conform to canonical schema
- [ ] **Identity Resolved**: No unresolved entity references
- [ ] **Drift Detection**: Anomaly check completed with evidence
- [ ] **Risk Assessment**: Both current and forecast risk computed
- [ ] **Policy Compliance**: Constraints checked before any action
- [ ] **Checkpoint Valid**: Restore point exists if actions taken
- [ ] **Audit Complete**: Provenance chain documented
- [ ] **Next Sync Scheduled**: Recommended interval provided

**Verification tools:** Web (for API checks), Bash (for MQTT), Read (for state files)

## Safety Constraints

- `mutation`: true
- `requires_checkpoint`: true
- `requires_approval`: true (for actions above risk threshold)
- `risk`: high

**Capability-specific rules:**
- STOP on low confidence from any perception step
- NEVER execute mutation without checkpoint
- NEVER emit external side effects without explicit approval
- Validate all source data before integration
- Preserve previous snapshot for rollback
- Rate-limit sync frequency to prevent thrashing

## Composition Patterns

**Commonly follows:**
- `world-model-workflow` - Initial twin creation before first sync
- `receive` - When triggered by external event

**Commonly precedes:**
- `summarize` - Create executive report after sync
- `send` - Notify stakeholders of drift or actions
- Self (recursive) - Next sync iteration

**Anti-patterns:**
- Never sync without prior world model established
- Never skip anomaly detection to proceed directly to action
- Never execute actions without policy constraint check
- Never delete audit logs before retention period

**Workflow references:**
- See `reference/workflow_catalog.yaml#digital-twin-sync-loop` for step definitions
- See `reference/world_state_schema.yaml` for canonical state format
- See `reference/composition_patterns.md#checkpoint-act-verify-rollback` for CAVR pattern
