# Plan Guardian Skill

## Metadata
- skill_name: plan-guardian
- activation_code: PLAN_GUARDIAN_V1
- version: 1.0.0
- category: monitoring
- phase: all (runs alongside any phase)

## Description

Background monitoring agent that runs alongside active development agents to detect drift from the original plan. Samples work-in-progress and compares against a plan digest to catch misalignment early, before significant rework is needed.

## Architecture

```
                    ┌─────────────────────┐
                    │   PLAN DIGEST       │
                    │  (.claude/plan-     │
                    │   digest.json)      │
                    └──────────┬──────────┘
                               │
                               ▼
┌──────────────┐     ┌─────────────────────┐     ┌──────────────┐
│ ACTIVE AGENT │────▶│   WORK STREAM       │────▶│ PLAN GUARDIAN│
│ (any phase)  │     │ (sampled via hook)  │     │ (background) │
└──────────────┘     └─────────────────────┘     └──────┬───────┘
                                                        │
                               ┌────────────────────────┴─────┐
                               ▼                              ▼
                        [OK - continue]              [DRIFT - inject]
                                                          │
                                                          ▼
                                              ┌─────────────────────┐
                                              │ Warning injected to │
                                              │ active agent context│
                                              └─────────────────────┘
```

## Activation

**Automatic:** Plan Guardian starts automatically when:
- Pipeline begins (PIPELINE_STARTED signal)
- Any phase skill activates
- Explicitly enabled in pipeline config

**Manual:**
- "Enable plan guardian"
- "Start drift monitoring"
- "Watch for plan drift"

## Plan Digest

The guardian operates on a lightweight plan digest created at pipeline start.

### Digest Location
```
.claude/plan-digest.json
```

### Digest Schema
```json
{
  "version": "1.0",
  "created_at": "2025-12-19T10:00:00Z",
  "source_documents": ["PRD.md", ".ideation/ideation-summary.md"],

  "core_problem": {
    "statement": "One-sentence problem description",
    "not_solving": ["Adjacent problems explicitly out of scope"]
  },

  "boundaries": {
    "must_have": ["Essential requirements"],
    "must_not_have": ["Explicit exclusions"],
    "constraints": ["Technical/business constraints"]
  },

  "architecture": {
    "patterns": ["Chosen patterns (e.g., REST API, event-driven)"],
    "stack": ["Technology choices"],
    "anti_patterns": ["Explicitly rejected approaches"]
  },

  "scope_markers": {
    "in_scope": ["Features/capabilities included"],
    "out_of_scope": ["Features explicitly deferred/excluded"],
    "scope_creep_indicators": ["Phrases that suggest scope creep"]
  },

  "key_decisions": [
    {
      "decision": "What was decided",
      "rationale": "Why",
      "alternatives_rejected": ["What was not chosen"]
    }
  ]
}
```

## Sampling Mechanism

### Hook Integration
The guardian receives samples via the `plan-guardian-hook.sh` which fires on:
- File writes (Edit, Write tools)
- Significant bash commands (npm install, docker build, etc.)
- Phase transitions

### Sample Payload
```json
{
  "timestamp": "2025-12-19T10:30:00Z",
  "phase": 7,
  "skill": "tdd-implementer",
  "action": {
    "type": "file_write",
    "path": "src/auth/oauth.ts",
    "summary": "Added OAuth2 authentication flow with Google provider",
    "lines_changed": 145
  },
  "context": {
    "recent_actions": ["Last 5 actions summary"],
    "current_task": "Implement user authentication"
  }
}
```

### Sampling Rate
- **Default:** Every 5 significant actions (writes, major commands)
- **High-sensitivity phases:** Every 2 actions (Phase 7 implementation)
- **Low-sensitivity phases:** Every 10 actions (Phase 9 testing)

Configurable via `.claude/guardian-config.json`:
```json
{
  "sampling_rate": {
    "default": 5,
    "phase_overrides": {
      "7": 2,
      "9": 10
    }
  },
  "sensitivity": "normal"
}
```

## Drift Detection

### Assessment Criteria

The guardian evaluates samples against the plan digest using these criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Scope alignment | 0.3 | Is this within defined scope? |
| Constraint compliance | 0.25 | Does this respect constraints? |
| Architecture adherence | 0.25 | Does this follow chosen patterns? |
| Decision consistency | 0.2 | Does this align with key decisions? |

### Response Levels

```
┌─────────┬───────────┬─────────────────────────────────────────┐
│ Level   │ Threshold │ Action                                  │
├─────────┼───────────┼─────────────────────────────────────────┤
│ OK      │ > 0.8     │ Silent, continue                        │
│ NOTICE  │ 0.6 - 0.8 │ Log concern, no interruption            │
│ WARN    │ 0.4 - 0.6 │ Inject reminder to active agent         │
│ DRIFT   │ 0.2 - 0.4 │ Pause, require acknowledgment           │
│ HALT    │ < 0.2     │ Block work, escalate to human           │
└─────────┴───────────┴─────────────────────────────────────────┘
```

### Injection Format

When drift is detected, the guardian injects a message into the active agent's context:

**WARN level:**
```
[GUARDIAN:WARN] Potential drift detected.
Concern: Implementation adding OAuth flow.
Plan states: "API-key-only authentication for MVP"
Confidence: 0.55
Action: Review and confirm this is intentional, or adjust approach.
```

**DRIFT level:**
```
[GUARDIAN:DRIFT] Significant drift from plan detected.
Concern: Adding real-time WebSocket features.
Plan states: "REST-only API, WebSockets deferred to Phase 2"
Confidence: 0.35
Action: PAUSED. Acknowledge one of:
  1. "Continue anyway" - Proceed with deviation (logged)
  2. "Revert approach" - Return to plan-aligned implementation
  3. "Update plan" - Modify plan digest to include this change
```

**HALT level:**
```
[GUARDIAN:HALT] Critical drift - human review required.
Concern: Implementing payment processing.
Plan states: "No payment handling - use third-party Stripe redirect"
Confidence: 0.15
Action: BLOCKED. Awaiting human decision.
```

## Signal Integration

### Signals Emitted
| Signal | Trigger | Payload |
|--------|---------|---------|
| GUARDIAN_STARTED | Guardian activates | `{phase, digest_hash}` |
| GUARDIAN_WARN | WARN threshold crossed | `{concern, confidence, suggestion}` |
| GUARDIAN_DRIFT | DRIFT threshold crossed | `{concern, confidence, options}` |
| GUARDIAN_HALT | HALT threshold crossed | `{concern, confidence, escalation}` |
| GUARDIAN_ACKNOWLEDGED | Agent responds to drift | `{response, justification}` |

### Signals Consumed
| Signal | Action |
|--------|--------|
| PIPELINE_STARTED | Initialize guardian, create digest if missing |
| PHASE_CHANGED | Adjust sampling rate for new phase |
| PLAN_UPDATED | Reload plan digest |
| GUARDIAN_DISABLE | Temporarily disable monitoring |

## Drift Log

All assessments are logged for audit:

```
.claude/guardian-log.jsonl
```

Format (JSON Lines):
```json
{"ts":"2025-12-19T10:30:00Z","phase":7,"action":"file_write","path":"src/auth/oauth.ts","score":0.55,"level":"WARN","concern":"OAuth not in plan"}
{"ts":"2025-12-19T10:31:00Z","phase":7,"action":"acknowledge","response":"continue","justification":"Product approved OAuth addition"}
```

## Creating the Plan Digest

### Automatic Generation
When pipeline starts, guardian creates digest from:
1. PRD.md (primary source)
2. .ideation/ideation-summary.md (if exists)
3. Architecture decisions in PRD Section 8
4. Scope boundaries in PRD Section 3

### Manual Override
User can provide custom digest:
```
"Use this as plan digest: [paste JSON or key points]"
```

### Digest Refresh
Digest can be updated mid-pipeline:
```
"Update plan digest to include WebSocket support"
```
This logs the change and adjusts future assessments.

## Configuration

### .claude/guardian-config.json
```json
{
  "enabled": true,
  "sampling_rate": {
    "default": 5,
    "phase_overrides": {}
  },
  "sensitivity": "normal",
  "thresholds": {
    "notice": 0.8,
    "warn": 0.6,
    "drift": 0.4,
    "halt": 0.2
  },
  "auto_digest": true,
  "log_all_samples": false,
  "phases_to_monitor": [5, 6, 7, 8, 9, 10, 11]
}
```

### Sensitivity Presets
- **relaxed:** Higher thresholds, fewer interruptions
- **normal:** Balanced detection
- **strict:** Lower thresholds, more aggressive detection

## Usage Examples

### Example 1: Catching Scope Creep

**Scenario:** TDD Implementer adds caching layer not in PRD.

**Sample:**
```json
{
  "action": {"type": "file_write", "path": "src/cache/redis-client.ts"},
  "summary": "Implemented Redis caching for API responses"
}
```

**Guardian Assessment:**
```
Plan digest check:
- core_problem: "User management API" - no mention of caching
- boundaries.must_have: No caching requirement
- scope_markers.out_of_scope: "Performance optimizations deferred"

Score: 0.45 (WARN)
```

**Injection:**
```
[GUARDIAN:WARN] Potential scope creep detected.
Concern: Adding Redis caching layer.
Plan states: "Performance optimizations deferred to post-MVP"
Action: Confirm this is essential for MVP functionality.
```

### Example 2: Architecture Violation

**Scenario:** Implementation uses synchronous file I/O in async codebase.

**Sample:**
```json
{
  "action": {"type": "file_write", "path": "src/services/data-loader.ts"},
  "summary": "Added fs.readFileSync for config loading"
}
```

**Guardian Assessment:**
```
Plan digest check:
- architecture.patterns: ["Fully async/await", "Non-blocking I/O"]
- architecture.anti_patterns: ["Synchronous file operations"]

Score: 0.30 (DRIFT)
```

**Injection:**
```
[GUARDIAN:DRIFT] Architecture violation detected.
Concern: Using synchronous fs.readFileSync.
Plan states: "Fully async/await, non-blocking I/O required"
Action: PAUSED. Use fs.promises.readFile instead.
```

### Example 3: Approved Deviation

**Scenario:** Team decided to add feature not in original plan.

**Agent Response:**
```
Continue anyway - Product approved adding dark mode support in standup.
```

**Guardian Log:**
```json
{
  "ts": "2025-12-19T14:00:00Z",
  "action": "acknowledge",
  "response": "continue",
  "justification": "Product approved adding dark mode support in standup",
  "original_concern": "Dark mode not in PRD scope",
  "logged_by": "agent"
}
```

## Integration with Pipeline

### Phase Lifecycle
1. **Pipeline Start:** Guardian initializes, creates/loads digest
2. **Phase Activation:** Guardian adjusts sampling rate
3. **During Execution:** Samples work, assesses drift
4. **Phase Completion:** Summarizes drift events for phase
5. **Pipeline End:** Generates drift report

### Drift Report (end of pipeline)
```
.claude/reports/guardian-summary.md
```

Contains:
- Total samples assessed
- Drift events by phase
- Deviations approved vs reverted
- Recommendations for plan updates

## Success Criteria

Guardian is effective when:
- Drift caught within 3 actions of occurrence
- False positive rate < 15%
- No HALT-level issues reach phase completion
- Plan digest accurately reflects intent

## See Also

- Pipeline Orchestration skill (starts guardian)
- Signal Manager (guardian signals)
- Hook system (sampling triggers)
