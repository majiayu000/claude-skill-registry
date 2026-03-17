---
name: tool-quality-audit
description: "Audit tool integrations for deterministic behavior, error contracts, and logging before agents depend on them. Use when adding or updating tools or MCP servers."
license: ""
compatibility: ""
metadata:
  short-description: Tool contract checks and smoke tests
  audience: tool-authors
  stability: draft
  owner: ""
  tags: [tools, validation, mcp]
allowed-tools: ""
---

# Tool Quality Audit

## Overview
Evaluate a tool’s reliability with a checklist and small smoke tests. Emphasize deterministic outputs, clear errors, and stable schemas.

## Quick start
1) Fill `templates/tool_audit.json`.
2) Run smoke tests manually or via your harness.
3) Record findings in `results.json`.

## Core Guidance
- Prefer deterministic checks before LLM-based grading.
- Verify error contracts (consistent codes/messages).
- Validate schemas are stable and documented.
- Record latency and failure modes.

## Resources
- `references/tool-audit-checklist.md`: Reliability and contract checklist.
- `templates/tool_audit.json`: Audit scaffold for a tool.

## Validation
- Ensure audit file is filled and failures are actionable.
