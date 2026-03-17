---
name: dialogue-log-decision
description: Log a decision to the decision log. Supports OPERATIONAL, TACTICAL, DESIGN, and ADR types. Use when recording decisions made by human or AI. Triggers on "decision", "decided", "log decision", "record decision", "document choice".
allowed-tools: Bash
---

# Dialogue: Decision Logger

Log a decision to the decision log. The decision log is a chronological audit trail of all decisions, from routine operational choices to architectural decisions.

## Decision Type Hierarchy

| Type | When to Use | Required Fields | Framework Grounding |
|------|-------------|-----------------|---------------------|
| **OPERATIONAL** | Routine choices during task execution | outcome, rationale | WRK domain, Ephemeral, documentable knowledge |
| **TACTICAL** | Approach changes affecting method | outcome, rationale | WRK domain, Ephemeral-Dynamic, elicitable knowledge |
| **DESIGN** | Component/schema decisions with rationale | outcome, rationale, **context** | STR domain, Dynamic-Standing, elicitable with rationale |
| **ADR** | Cross-reference to Architecture Decision Record | outcome, rationale, **context**, ref | STR domain, Standing, formal alternatives analysis |

### Choosing the Right Type

```
Did you formally evaluate multiple alternatives with trade-offs?
  YES → Use ADR type (create ADR document first, then log with ref)
  NO  → Continue...

Does this affect how a component or schema works?
  YES → Use DESIGN
  NO  → Continue...

Does this change your approach to the current task?
  YES → Use TACTICAL
  NO  → Use OPERATIONAL
```

## How to Log a Decision

Execute the following bash command:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-log-decision/scripts/log-decision.sh <type> <actor> <subject> <outcome> <rationale> [context] [tags] [ref]
```

### Required Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `type` | `OPERATIONAL`, `TACTICAL`, `DESIGN`, or `ADR` | Decision significance level |
| `actor` | `ai:claude` or `human:<id>` | Who made the decision |
| `subject` | text | Brief description of what the decision concerns |
| `outcome` | text | What was decided or done |
| `rationale` | text | Single-line reasoning (why this choice) |

### Conditionally Required Parameters

| Parameter | Required For | Description |
|-----------|--------------|-------------|
| `context` | DESIGN, ADR | Additional surrounding situation—what led to this decision |

### Optional Parameters

| Parameter | Description |
|-----------|-------------|
| `context` | Additional context (optional for OPERATIONAL/TACTICAL) |
| `tags` | Comma-separated categorisation tags |
| `ref` | Reference to related document (e.g., `ADR-001` for ADR type) |

## Examples

### OPERATIONAL Decision
```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-log-decision/scripts/log-decision.sh OPERATIONAL "ai:claude" "Test failure response" "Added null check to validateInput()" "TypeError indicated undefined parameter" "" "fix,validation"
```

### TACTICAL Decision
```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-log-decision/scripts/log-decision.sh TACTICAL "human:pidster" "Refactoring approach" "Refactor auth module before adding feature" "Reduce complexity before extending" "" "refactor,auth"
```

### DESIGN Decision
```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-log-decision/scripts/log-decision.sh DESIGN "human:pidster" "Information reference schema approach" "Simplified from URI format to self-describing IDs" "Simpler format reduces cognitive load, maintains backward compatibility" "Initial v1 had complex URI format; user directed simplification" "schema,simplification"
```

### ADR Cross-Reference
```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-log-decision/scripts/log-decision.sh ADR "human:pidster" "Graph storage approach" "Created ADR-001 for filesystem-first strategy" "Architectural decision requiring formal alternatives analysis" "Evaluated Kuzu, Neo4j, filesystem options" "architecture,storage" "ADR-001"
```

## Output

The script returns the generated decision ID (e.g., `DEC-20260113-143215`).

## When to Use ADR vs DESIGN

**Use DESIGN when:**
- You chose an approach but didn't formally document alternatives
- The decision affects a component but not the whole system
- Rationale matters but a full ADR would be overkill

**Use ADR when:**
- You formally evaluated 2+ alternatives with pros/cons
- The decision has system-wide architectural impact
- You need to document consequences and trade-offs
- Future developers will need to understand why

**Process for ADR:**
1. Create ADR document using `dialogue-create-adr` skill
2. Log cross-reference using this skill with type=ADR and ref=ADR-NNN

## Granularity Guidelines

### One Decision Per Distinct Choice

Log **one decision entry per distinct choice**. Do not batch multiple decisions into a single entry.

### Why Granularity Matters

- **Audit trail**: Each decision can be reviewed independently
- **Traceability**: Specific rationale for each choice is preserved
- **Search**: Can find all decisions about a specific subject
- **Compliance verification**: Can count decisions against expected count

### When Batching Is Acceptable

Batch only when:
- The decisions are truly identical (same rationale applies to all)
- The items being decided have no individual identity
- Example: "Applied consistent formatting to all 15 files" (one formatting decision, multiple files)

## Sharing

**Always commit and push immediately after logging a decision.** Decisions capture rationale that is otherwise tacit—delayed sharing means delayed theory-building for the team.

```bash
git add .dialogue/logs/decisions/ && git commit -m "DEC-YYYYMMDD-HHMMSS: <subject>" && git push
```
