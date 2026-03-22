---
name: file-ticket
description: Use after brainstorming to create a ticket in the project tracker with full context from the design session
---

# File Ticket

Create a ticket in the project tracker with context from the brainstorm/design session.

## Process

1. Gather from the session:
   - **Title** — concise, action-oriented
   - **Description** — what needs to be built and why
   - **Spec reference** — path to the design spec (if written)
   - **Priority** — infer from context (default: normal)
   - **Type** — feature, bugfix, refactor

2. Create the ticket using available tools (Linear MCP, GitHub Issues, etc.)

3. Confirm with the user — show ticket ID and title

## Ticket Content

The ticket description should include:
- Summary of what was decided during brainstorming
- Link/path to the design spec
- Key constraints or decisions worth highlighting
- NOT the full spec (that lives in the spec file)

## Notes

- This skill is tracker-agnostic — use whatever MCP tools are available
- If no tracker tools are available, output the ticket content for the user to create manually
- The ticket ID becomes the branch name in `dodi-dev:pickup`
