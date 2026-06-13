---
name: go
description: >-
  Zero-config goal-to-tasks engine. Takes any goal (software, pentest, business, learning),
  runs adaptive discovery, generates a validated spec, parses into TaskMaster tasks, creates an
  implementation plan, and executes with built-in CDD verification. Use when user says "PRD",
  "product requirements", "I want to build", or any goal-driven phrase.
user-invocable: true
allowed-tools:
  - Read
  - Skill
  - Bash
  - AskUserQuestion
  - ToolSearch
  - mcp__atlas-engine
  - mcp__plugin_prd_go
  - mcp__plugin_prd-taskmaster_go
  - mcp__plugin_atlas-go_go
---

# go (orchestrator)

Pure routing. Reads pipeline state, dispatches to the correct phase skill.

**Deferred MCP tools:** in Claude Code the engine's MCP tools are often *deferred* — not
callable until loaded. If a tool below is not directly callable, first run
`ToolSearch(query="select:mcp__plugin_prd_go__preflight")` (keyword fallback
`ToolSearch(query="+atlas engine preflight", max_results=10)`) and use whichever prefix
matches (`mcp__plugin_prd_go__` or `mcp__atlas-engine__`).

## Flow

1. Call `mcp__plugin_prd_go__preflight()` — get environment state
2. Call `mcp__plugin_prd_go__current_phase()` — get pipeline state
3. Route via Skill tool:
   - current_phase is null or SETUP → invoke `/prd:setup`
   - current_phase is DISCOVER → invoke `/prd:discover`
   - current_phase is GENERATE → invoke `/prd:generate`
   - current_phase is HANDOFF → invoke `/prd:handoff`
   - current_phase is EXECUTE → invoke `/prd:execute-task`

4. After phase skill returns, re-check current_phase. If it advanced, route to the next phase. If not, report the blocker.

## Stateless routing

This skill does NOT hold procedure. Each phase skill owns its own logic. The orchestrator survives context loss because every phase skill reads `current_phase()` on entry.

## Red flags

These thoughts mean STOP, you're rationalising:
- "I know which phase we're in, skip preflight" → NO. Preflight is cheap.
- "The phase skill already ran, I don't need to re-check" → NO. Context might have died.
- "I can just do the work myself" → NO. Dispatch to the phase skill.
