---
name: dacp-assembler
version: 1.0.0
description: "Composes three-part DACP bundles from skill library artifacts. Determines fidelity level, queries catalog, and records assembly rationale."
user-invocable: false
allowed-tools: Read Grep Glob Bash
metadata:
  extensions:
    gsd-skill-creator:
      version: 2
      createdAt: "2026-02-27"
      triggers:
        intents:
          - "handoff"
          - "bundle"
          - "assemble"
          - "dacp"
          - "fidelity"
        contexts:
          - "agent communication"
          - "bundle composition"
          - "handoff assembly"
      domain: "agent-communication"
      fidelity_default: 2
---

# DACP Assembler

Compose deterministic agent communication bundles from skill library artifacts.

## When to Use

- Handing off work between agents (task assignment, verification, escalation)
- Packaging structured data with executable scripts for a receiving agent
- Upgrading prose-only messages to structured bundles for reliability

## Quick Start

1. **Classify handoff** -- identify the handoff type from the taxonomy
2. **Check drift** -- look up historical drift rate for this pattern
3. **Determine fidelity** -- run the decision model (Level 0-3)
4. **Search catalog** -- find matching scripts and schemas
5. **Compose bundle** -- assemble intent + data + code at the decided level

## Fidelity Levels

| Level | Name | Contents |
|-------|------|----------|
| 0 | PROSE | Intent markdown only |
| 1 | PROSE_DATA | Intent + structured JSON data |
| 2 | PROSE_DATA_SCHEMA | Intent + data + JSON Schema validation |
| 3 | PROSE_DATA_CODE | Intent + data + schemas + executable scripts |

For detailed criteria and decision tree, see @references/fidelity-levels.md

## Assembly Process

1. Receive handoff request with intent, data, and context
2. Assess data complexity (none / simple / structured / complex)
3. Count available skills from catalog
4. Build fidelity decision input from request + computed values
5. Run `determineFidelity()` to get proposed level
6. Apply SAFE-02 clamping if changing from current level (max 1 step)
7. Compose artifacts at the decided level
8. Record assembly rationale (justification, skills, artifacts)
9. Build manifest with provenance metadata

For worked examples at each level, see @references/assembly-patterns.md

## Handoff Types

- task-assignment, verification-request, data-transformation
- configuration-update, research-handoff, status-report
- question-escalation, patch-delivery

Full taxonomy at @references/handoff-taxonomy.md

## Safety Boundaries

1. **No code generation** -- assembler selects from existing catalog entries, never generates code
2. **Size limits** -- 50KB data payloads, 10KB scripts, enforced at bundle creation
3. **Bounded learning** -- max 1 fidelity level change per cycle (SAFE-02)
4. **Mandatory provenance** -- every script must have source skill + version
