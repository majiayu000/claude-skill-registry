---
name: tool-selection
description: Use when selecting between MCP tools based on task complexity and requirements - provides a structured selection workflow and decision rationale.
---

# Tool Selection

## Overview
Select the optimal MCP tool by evaluating task complexity, accuracy needs, and performance trade-offs.

## When to Use
- Choosing between Codanna and Morphllm
- Routing tasks based on complexity
- Explaining tool selection rationale

Avoid when:
- The tool is explicitly specified by the user

## Quick Reference

| Task | Load reference |
| --- | --- |
| Tool selection | `skills/tool-selection/references/select.md` |

## Workflow
1. Parse the operation requirements.
2. Load the tool selection reference.
3. Apply the scoring and decision matrix.
4. Report the chosen tool and rationale.

## Output
- Selected tool and confidence
- Rationale and trade-offs

## Common Mistakes
- Ignoring explicit user tool preferences
- Overweighting speed vs accuracy without justification
