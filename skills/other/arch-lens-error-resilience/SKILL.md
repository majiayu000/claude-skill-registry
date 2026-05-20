---
name: arch-lens-error-resilience
categories: [arch-lens]
description: Create Error/Resilience architecture diagram showing failure handling, recovery mechanisms, and circuit breakers. Diagnostic lens answering "How are failures handled?"
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo 'Error/Resilience Lens - Analyzing failure handling...'"
          once: true
---

# Error/Resilience Architecture Lens

**Cognitive Mode:** Diagnostic
**Primary Question:** "How are failures handled?"
**Focus:** Error Propagation, Recovery Mechanisms, Circuit Breakers, Validation Gates

## When to Use

- Need to understand error handling architecture
- Documenting recovery and retry mechanisms
- Analyzing validation gates and circuit breakers
- User invokes `/autoskillit:arch-lens-error-resilience` or `/autoskillit:make-arch-diag error`

## Critical Constraints

**NEVER:**
- Modify any source code files
- Show happy path details (that's process flow lens)
- Ignore validation and fail-fast patterns

**ALWAYS:**
- Focus on FAILURE paths and recovery
- Show validation gates and their failure modes
- Document retry limits and circuit breakers
- Include exception hierarchy if present
- BEFORE creating any diagram, LOAD the `/autoskillit:mermaid` skill using the Skill tool - this is MANDATORY

---

## Analysis Workflow

### Step 1: Launch Parallel Exploration Subagents

Spawn Explore subagents to investigate:

**Exception Hierarchy**
- Find custom exception classes
- Map inheritance relationships
- Look for: Exception, Error, raise, error classes, custom exceptions

**Validation Gates**
- Find validation/guard functions
- Identify fail-fast patterns
- Look for: validate_*, check_*, assert, guard, gate, precondition checks

**Error Detection**
- Find error detection points
- Identify how failures are recognized
- Look for: try/except, catch, on_error, handle_error, error handling

**Recovery Mechanisms**
- Find retry logic
- Identify fallback strategies
- Look for: retry, backoff, attempt, max_retries, retry policies

**Circuit Breakers**
- Find patterns that prevent infinite retries
- Identify failure thresholds
- Look for: circuit, breaker, max_failures, trip, failure thresholds

**Error Routing**
- Find how errors are propagated
- Identify error terminal states
- Look for: raise, return Error, error node, ERROR state

### Step 2: Map Error Paths

For each major operation, document:
- **Success Path**: Normal completion
- **Retry Path**: Transient failure recovery
- **Failure Path**: Permanent failure handling
- **Circuit Break Path**: Threshold exceeded

**CRITICAL - Analyze Read/Write Direction:**
For EVERY error handling component:
- **Error context capture**: What data is READ to build error context?
- **Error logging**: Where are errors WRITTEN (logs, database, files)?
- **State updates**: What state is WRITTEN on failure?
- **Recovery reads**: What data is READ during recovery?

Distinguish:
- Error logs (write-only, never read back for logic)
- Failure context in database (may be read for retry/debugging)
- Debug artifacts (write-only diagnostics)

### Step 3: Document Recovery Mechanisms

| Mechanism | Trigger | Action | Limit |
|-----------|---------|--------|-------|
| Retry | Transient error | Repeat operation | max N |
| Fallback | Specific error | Alternative action | - |
| Circuit Breaker | Too many failures | Stop retrying | threshold |

### Step 4: Create the Diagram

Use flowchart with:

**Direction:** `TB` for error flow hierarchy

**Subgraphs:**
- Execution (normal operation)
- Validation Gates (fail-fast checks)
- Error Handling (detection and routing)
- Recovery (retry, fallback)
- Terminals (success, failure states)

**Node Styling:**
- `handler` class: Execution nodes
- `detector` class: Validation gates, error detection
- `gap` class: Failed/error state (yellow warning)
- `stateNode` class: Decision points, circuit breaker
- `output` class: Recovery actions
- `terminal` class: Final states (success, error)

**Connection Types:**
- Solid: Normal flow
- Edge labels: Conditions, error types
- Show loops for retry mechanisms

### Step 5: Write Output

Write the diagram to: `temp/arch-lens-error-resilience/arch_diag_error_resilience_{YYYY-MM-DD_HHMMSS}.md` (relative to the current working directory)

After writing the diagram file, emit a structured output line:

```
diagram_path = {absolute_path_to_diagram_file}
```

---

## Output Template

```markdown
# Error/Resilience Diagram: {System Name}

**Lens:** Error/Resilience (Diagnostic)
**Question:** How are failures handled?
**Date:** {YYYY-MM-DD}
**Scope:** {What was analyzed}

## Exception Hierarchy

```
BaseError
├── ValidationError
├── ProcessingError
│   └── RetryableError
└── FatalError
```

## Resilience Diagram

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 40, 'rankSpacing': 50, 'curve': 'basis'}}}%%
flowchart TB
    %% CLASS DEFINITIONS %%
    classDef terminal fill:#1a237e,stroke:#7986cb,stroke-width:2px,color:#fff;
    classDef stateNode fill:#004d40,stroke:#4db6ac,stroke-width:2px,color:#fff;
    classDef handler fill:#e65100,stroke:#ffb74d,stroke-width:2px,color:#fff;
    classDef phase fill:#6a1b9a,stroke:#ba68c8,stroke-width:2px,color:#fff;
    classDef detector fill:#b71c1c,stroke:#ef5350,stroke-width:2px,color:#fff;
    classDef output fill:#00695c,stroke:#4db6ac,stroke-width:2px,color:#fff;
    classDef gap fill:#ff6f00,stroke:#ffa726,stroke-width:2px,color:#000;

    subgraph Execution ["EXECUTION"]
        EXEC["Execute<br/>━━━━━━━━━━<br/>Main operation"]
        SUCCESS["SUCCESS<br/>━━━━━━━━━━<br/>Completed"]
        RETRY["RETRY<br/>━━━━━━━━━━<br/>Transient failure"]
        FAILED["FAILED<br/>━━━━━━━━━━<br/>Needs handling"]
    end

    subgraph Gates ["VALIDATION GATES (Fail-Fast)"]
        GATE1["Validate Input<br/>━━━━━━━━━━<br/>Check required fields"]
        GATE2["Validate State<br/>━━━━━━━━━━<br/>Check preconditions"]
    end

    subgraph Recovery ["RECOVERY MECHANISMS"]
        direction TB
        R_RETRY["Retry with Backoff<br/>━━━━━━━━━━<br/>Max N attempts"]
        R_FALLBACK["Fallback Action<br/>━━━━━━━━━━<br/>Alternative path"]
        R_CIRCUIT{"Circuit<br/>Breaker<br/>triggered?"}
    end

    subgraph Terminals ["TERMINAL STATES"]
        T_COMPLETE([COMPLETE])
        T_ERROR([ERROR])
        T_CIRCUIT([CIRCUIT_BROKEN])
    end

    %% EXECUTION FLOW %%
    EXEC --> SUCCESS
    EXEC --> RETRY
    EXEC --> FAILED

    SUCCESS --> T_COMPLETE
    RETRY -->|"back to queue"| EXEC

    %% VALIDATION GATES %%
    GATE1 -->|"missing"| T_ERROR
    GATE1 -->|"valid"| GATE2
    GATE2 -->|"invalid"| T_ERROR
    GATE2 -->|"valid"| EXEC

    %% RECOVERY %%
    FAILED --> R_CIRCUIT
    R_CIRCUIT -->|"not triggered"| R_RETRY
    R_CIRCUIT -->|"triggered"| T_CIRCUIT
    R_RETRY --> EXEC
    R_RETRY -->|"exhausted"| R_FALLBACK
    R_FALLBACK --> T_ERROR

    %% CLASS ASSIGNMENTS %%
    class EXEC,SUCCESS handler;
    class RETRY,FAILED gap;
    class GATE1,GATE2 detector;
    class R_RETRY,R_FALLBACK output;
    class R_CIRCUIT stateNode;
    class T_COMPLETE,T_ERROR,T_CIRCUIT terminal;
```

**Color Legend:**
| Color | Category | Description |
|-------|----------|-------------|
| Orange | Execution | Normal operation and success |
| Yellow | Failed | Failure states requiring handling |
| Red | Gates | Validation gates (fail-fast) |
| Dark Teal | Recovery | Retry and fallback mechanisms |
| Teal | Circuit | Circuit breaker decisions |
| Dark Blue | Terminal | Final states |

## Recovery Mechanisms

| Mechanism | Trigger | Action | Max Attempts |
|-----------|---------|--------|--------------|
| {name} | {condition} | {what happens} | {limit} |

## Validation Gates

| Gate | Checks | Failure Mode |
|------|--------|--------------|
| {name} | {what validated} | {error raised} |
```

---

## Pre-Diagram Checklist

Before creating the diagram, verify:

- [ ] LOADED `/autoskillit:mermaid` skill using the Skill tool
- [ ] Using ONLY classDef styles from the mermaid skill (no invented colors)
- [ ] Diagram will include a color legend table

---

## Related Skills

- `/autoskillit:make-arch-diag` - Parent skill for lens selection
- `/autoskillit:mermaid` - MUST BE LOADED before creating diagram
- `/autoskillit:arch-lens-process-flow` - For normal flow view
- `/autoskillit:arch-lens-concurrency` - For parallel failure handling