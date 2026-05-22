---
name: dialogue-create-adr
description: Creates Architecture Decision Records for significant architectural decisions. Use when the user wants to create an ADR, make an ADR, record an architecture decision, document architecture choice, perform formal alternatives analysis, or when formally evaluating multiple alternatives with trade-offs. Appropriate for decisions with system-wide or long-term impact requiring structured alternatives documentation.
allowed-tools: Bash
---

# Dialogue: ADR Creator

Creates Architecture Decision Records for significant architectural decisions that require formal alternatives analysis.

## When to Use

Use this skill when:
- Formally evaluating 2+ alternatives with pros/cons
- The decision has system-wide or long-term architectural impact
- Consequences and trade-offs need documentation
- Future developers will need to understand why this choice was made

**Do NOT use for:**
- Routine operational choices → use `dialogue-log-decision` with OPERATIONAL type
- Tactical approach changes → use `dialogue-log-decision` with TACTICAL type
- Component decisions without formal alternatives → use `dialogue-log-decision` with DESIGN type

## Dependencies

This skill requires:
- **dialogue-log-decision skill** — Used to automatically cross-reference ADRs in the decision log

## How to Create an ADR

Execute the following bash command:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-create-adr/scripts/create-adr.sh <title> <actor> <context> <decision> <alternatives> <consequences> <rationale> [tags]
```

### Required Parameters

| Parameter | Description |
|-----------|-------------|
| `title` | Short descriptive title (will be slugified for filename) |
| `actor` | Who made the decision — must be `human:<id>` or `ai:<id>` format |
| `context` | What issue motivated this decision? |
| `decision` | What change are we making? |
| `alternatives` | Alternatives considered with pros/cons |
| `consequences` | What becomes easier or harder? (use check marks/warnings for clarity) |
| `rationale` | Why is this the right choice? What evidence supports it? |

### Optional Parameters

| Parameter | Description |
|-----------|-------------|
| `tags` | Comma-separated categorisation tags (defaults to "architecture" if omitted) |

## Example

```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-create-adr/scripts/create-adr.sh \
  "Use filesystem for initial Context Graph storage" \
  "human:pidster" \
  "Need to store Context Graph data for TMS operations. Must support location-agnostic access and future migration to graph database." \
  "Start with filesystem + YAML storage; design abstractions for future Kuzu migration" \
  "1. Kuzu (embedded graph): Pros - native graph queries, good performance. Cons - additional dependency, learning curve. 2. Neo4j: Pros - mature, well-documented. Cons - server dependency, overkill for current scale. 3. Filesystem + YAML: Pros - simple, no dependencies, human-readable. Cons - no native graph queries, manual relationship traversal." \
  "Positive: Simple implementation, no new dependencies. Positive: Human-readable storage. Trade-off: Manual graph traversal required. Trade-off: Will need migration when scale requires it." \
  "Start simple, evolve when needed. Filesystem provides immediate value without premature optimisation. Resolver abstraction enables future migration." \
  "architecture,storage,context-graph"
```

## Output

The script:
1. Creates ADR file at `decisions/ADR-NNN-<slugified-title>.md`
2. Automatically logs to decision log with type=ADR and ref to the ADR file
3. Returns both the ADR ID and decision log ID

Example output:
```
ADR-001: /path/to/project/decisions/ADR-001-use-filesystem-for-initial-context-graph-storage.md
DEC-20260114-153000: Cross-reference logged
```

## ADR File Structure

The created ADR follows the template from `guidance_implementation.md`:

```markdown
# ADR-NNN: [Title]

Date: YYYY-MM-DD
Status: Proposed
Actor: human:pidster

## Context
[What issue motivated this decision?]

## Decision
[What change are we making?]

## Alternatives Considered
[Each alternative with pros/cons]

## Consequences
[What becomes easier or harder?]

## Rationale
[Why is this the right choice?]
```

A template file is available at `templates/adr-template.md` in this skill directory.

## ADR Lifecycle

| Status | Meaning |
|--------|---------|
| **Proposed** | Initial state; under consideration |
| **Accepted** | Approved and in effect |
| **Deprecated** | No longer recommended; kept for history |
| **Superseded** | Replaced by another ADR (note which one) |

To change status, edit the ADR file directly. The decision log entry is immutable (captures the moment of decision).

## Error Handling

The script validates:
- Actor format (must be `human:<id>` or `ai:<id>`)
- Required parameters (all 7 must be provided)

If the decision log cross-reference fails, a warning is shown but the ADR file is still created.

## Framework Grounding

ADRs are:
- **Content Domain**: STR (Strategy) — rationale, decisions, business justification
- **Temporal Class**: Standing — quarterly or less updates, years lifespan
- **Knowledge Type**: Attempting to capture embedded knowledge through formal alternatives analysis

The decision log cross-reference ensures the decision log remains a complete audit trail while ADRs provide the detailed Standing document.
