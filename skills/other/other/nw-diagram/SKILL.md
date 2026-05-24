---
name: nw-diagram
description: "Generates C4 architecture diagrams (context, container, component) in Mermaid or PlantUML. Use when creating or updating architecture visualizations."
user-invocable: true
argument-hint: '[diagram-type] - Optional: --format=[mermaid|plantuml|c4] --level=[context|container|component]'
---

# NW-DIAGRAM: Architecture Diagram Generation

**Wave**: CROSS_WAVE | **Agent**: Morgan (nw-solution-architect) | **Command**: `*create-diagrams`

## Overview

Generate architecture diagrams from design documents. Supports C4 model levels (context|container|component) in Mermaid|PlantUML|C4 format. Audience-appropriate: high-level context for stakeholders|component details for developers|deployment topology for operations.

## Context Files Required

- docs/product/architecture/brief.md (SSOT — component boundaries, technology stack, design decisions)

## Workflow

1. **Read Context** — Load `docs/product/architecture/brief.md`. Extract component boundaries, technology stack, and design decisions. Gate: architecture brief loaded.
2. **Resolve Configuration** — Determine `diagram_type` (component|deployment|sequence|data|context), `format` (mermaid|plantuml|c4), `level` (context|container|component), and `output_directory`. Gate: all configuration parameters resolved.
3. **Invoke Agent** — Delegate to `@nw-solution-architect` with `*create-diagrams` for `{architecture-component}`, passing context files and resolved configuration. Gate: agent invoked with all parameters.
4. **Validate Output** — Verify diagrams render without syntax errors and files exist in `output_directory`. Gate: all success criteria pass.
5. **Handoff** — Return deliverables to invoking agent. Gate: architecture diagrams available in configured format.

## Success Criteria

- [ ] Diagrams accurately represent current architecture
- [ ] Audience-appropriate detail level applied
- [ ] Diagrams render without syntax errors
- [ ] Output files created in configured directory

## Next Wave

**Handoff To**: {invoking-agent-returns-to-workflow}
**Deliverables**: Architecture diagrams in configured format

## Examples

### Example 1: Generate C4 container diagram
```
/nw-diagram payment-service --diagram_type=component --format=mermaid --level=container
```
Morgan reads architecture docs and produces a Mermaid container diagram showing service boundaries, data stores, and external integrations.

## Expected Outputs

```
docs/product/architecture/
  system-context.{ext}
  component-architecture.{ext}
  deployment-architecture.{ext}
```
