---
name: agents-bootstrap
description: Generate a project-specific AGENTS.md from a user goal, then confirm before overwriting.
metadata:
  short-description: Bootstrap AGENTS.md for a real project
---

# AGENTS Bootstrap

Generate a concise, project-specific `AGENTS.md` tailored to the user's goal.

## Core rules
- Use `assets/agents-template.md` as the base structure.
- No placeholders in the final `AGENTS.md`.
- Keep the file concise and enforceable.
- Draft in chat first; ask for confirmation before writing.
- Before overwriting, create a backup: `AGENTS.md.bak.<timestamp>`.
- If MCP tools are in scope and `docs/mcp-tools.md` is missing or stale, instruct to use the `mcp-tools-catalog` skill before finalizing `AGENTS.md`.

## Required inputs
Collect these if not provided:
- Role and objective
- Non-negotiable constraints
- Stack and data sources
- Testing toolchain (unit/integration/e2e commands, frameworks, MCP tools)
- Whether Issue CSV workflow is in scope

Ask at most 2 clarification questions, then proceed with stated assumptions.
If the task continues across turns, re-invoke this skill to keep the rules active.

## Output requirements
The final `AGENTS.md` must include (when applicable):
- Role & objective
- Constraints
- Tech & data sources
- Project testing strategy (tools + commands)
- E2E loop (plan → issues → implement → test → review → commit → regression)
- Plan & issue generation reference (use `plan` skill)
- Issue CSV policy (if Issue CSV workflow is in scope)
- Tool usage (MCP usage guidance)
- Testing policy reference (`docs/testing-policy.md`)
- Safety and output style

## Write flow
1) Draft the tailored `AGENTS.md` in chat.
2) Ask: "Reply CONFIRM to overwrite AGENTS.md."
3) On confirmation:
   - Backup current file to `AGENTS.md.bak.<timestamp>` if it exists.
   - Write the new `AGENTS.md`.

Do not edit other files.
