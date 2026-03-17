---
name: mcp-integration
description: MCP server integration using Occam's Razor escalation. Start minimal, escalate on failure, find limitation boundaries. Use when adding new MCP servers, debugging MCP adoption, or optimizing MCP configuration.
---

# MCP Integration Skill

**Principle**: #34 (Occam's Razor Implementation)

**Source**: Empirical testing in claude-code-playground (2026-01-27/28). 12 tests across agent-kernel and blackboard MCPs.

---

## When to Use This Skill

Use the mcp-integration skill when:
- Adding a new MCP server to a project
- Claude doesn't use MCP tools as expected
- Debugging why an MCP works in one project but not another
- Optimizing MCP config (removing unnecessary layers)

**DO NOT use this skill for:**
- Building MCP servers (use MCP SDK docs)
- General Claude Code configuration (not MCP-specific)

---

## The Escalation Ladder

```
Level 0: .mcp.json only           <- Start here (always)
Level 1: + CLAUDE.md paragraph    <- Most tools land here
Level 2: + UserPromptSubmit hook  <- For protocol enforcement
Level 3: + Hook script            <- For context pre-loading
Level 4: + allowedTools           <- For permission issues
--------------------------------------------------
Level 5: Approach limitation      <- Stop. Rethink.
```

---

## Level 0: MCP Registration Only

**Add**: `.mcp.json`

```json
{
  "mcpServers": {
    "my-mcp": {
      "command": "node",
      "args": ["path/to/build/index.js"]
    }
  }
}
```

**Test**: Ask Claude to explicitly use a tool from this MCP.

**Works when**: User explicitly requests tool functionality.

**Evidence**: Test 2.1 — Blackboard `contribute_fact` worked with zero config when prompt explicitly asked to "contribute a fact".

**Escalate when**: Claude doesn't use MCP tools spontaneously (without explicit mention).

---

## Level 1: + CLAUDE.md Instruction

**Add**: A short paragraph in `CLAUDE.md` expressing **intent** (not API reference).

```markdown
## [MCP Name]

BEFORE starting work, [do X with MCP tool].
AFTER completing work, [do Y with MCP tool].
```

**Test**: Give Claude a task where the MCP is relevant but **not mentioned** in the prompt.

**Works when**: Claude spontaneously uses MCP tools at appropriate moments. Works in both interactive and pipe (`-p`) mode.

**Evidence**: Test 9 — Claude spontaneously called `list_sessions` + `read_facts` when CLAUDE.md said "check blackboard before work", even though the prompt only said "review sample_code.py".

**Key insight**: Express **intent** ("check for prior context"), not **API** ("call mcp__blackboard__list_sessions"). Claude discovers tool names from MCP registration.

**Escalate when**: Claude reads instruction but doesn't reliably follow it (inconsistent adoption).

---

## Level 2: + UserPromptSubmit Hook (Inline)

**Add**: `.claude/settings.json` with inline hook.

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "cat <<'EOF'\n{\"additionalContext\":\"<system-instruction>\\nYou MUST call tool_x before work.\\n</system-instruction>\"}\nEOF"
      }]
    }]
  }
}
```

**Test**: Run several tasks and verify tool is called **every turn**.

**Works when**: Need mandatory protocol enforcement (e.g., agent-kernel tuple_init/evaluate_gradient on every turn).

**Evidence**: Tests 2-3 — Agent-kernel protocol was reliably enforced with hook injection. Without hooks (tests 1-5), CLAUDE.md alone was insufficient for per-turn protocol compliance.

**Limitation**: Hooks **do not fire** in pipe mode (`claude -p "..."`). Only interactive sessions.

**Escalate when**: Need to pre-load context (not just instructions), or need optimization.

---

## Level 3: + Hook Script (Context Injection)

**Add**: Replace inline hook with a script.

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "bash scripts/context-hook.sh"
      }]
    }]
  }
}
```

The script reads state files and outputs JSON with `additionalContext` containing pre-loaded data.

**Works when**: Reduces tool calls by injecting data that would otherwise require tool calls (e.g., blackboard facts as `<episodic-memory>` tags).

**Evidence**: `blackboard-context-hook.sh` saves 2 tool calls per turn by pre-loading facts.

**Limitation**: Still doesn't fire in pipe mode. Adds shell execution latency.

**Escalate when**: Permission denials prevent tool usage.

---

## Level 4: + Explicit allowedTools

**Add**: Permission grants in `.claude/settings.json`.

```json
{
  "permissions": {
    "allow": ["mcp__my-mcp__*"]
  }
}
```

**Works when**: Removes permission prompts that cause Claude to abandon tool usage.

**Evidence**: Test 2 showed Claude *attempted* agent-kernel tools but was DENIED by permissions.

**This is the last configuration lever.**

---

## Level 5: Approach Limitation

If all levels active and Claude still doesn't use the MCP as intended:

| Limitation | Symptom | Resolution |
|-----------|---------|------------|
| **Tool design** | Claude calls tool but misuses it | Redesign tool schema/description |
| **Task mismatch** | Tool not relevant to task type | MCP doesn't fit this use case |
| **Context window** | Too many tools, Claude ignores some | Reduce tool count, use ToolSearch |
| **Model capability** | Claude can't reason about tool correctly | Simplify tool interface |

---

## Quick Decision Matrix

| Behavior Desired | Minimum Level |
|------------------|---------------|
| Use tools when user explicitly asks | **Level 0** |
| Use tools spontaneously (both modes) | **Level 1** |
| Enforce mandatory protocol per turn | **Level 2** |
| Pre-load context to save tool calls | **Level 3** |
| Bypass permission prompts | **Level 4** |

---

## Patterns (from empirical testing)

### P1: CLAUDE.md is the Universal Injection Mechanism
Loads in every mode (interactive, pipe, Task agents). Hooks only fire in interactive mode. For guaranteed behavior across all contexts, CLAUDE.md is the foundation.

### P2: Hooks Complement, Don't Replace
Hooks add enforcement (Level 2) and optimization (Level 3) on top of CLAUDE.md. Not a substitute — pipe mode proves this.

### P3: Tool Discovery is Automatic
Claude discovers MCP tools from registration alone. Never list tool names in CLAUDE.md. Express **intent**, not **API reference**.

### P4: Spontaneous != Explicit
Write path (explicit request -> tool use) works at Level 0. Read path (spontaneous retrieval) requires Level 1 minimum.

### P5: Escalation is Reversible
If Level 1 sufficient after testing Level 2, remove the hook. Keep config minimal.

---

## Test Protocol (for new MCP servers)

```
1. Register in .mcp.json only (Level 0)
2. Test: Does Claude use tools when explicitly asked?
   -> YES: Level 0 sufficient for explicit use
   -> NO: Fix MCP tool schema/description

3. Add CLAUDE.md paragraph (Level 1)
4. Test: Does Claude use tools spontaneously?
   -> YES: Done. Level 1 is your config.
   -> NO: Escalate

5. Add UserPromptSubmit hook (Level 2)
6. Test: Is protocol enforced per turn?
   -> YES: Done.
   -> NO: Check hook JSON format

7. Add hook script (Level 3) — only for context pre-loading
8. Add allowedTools (Level 4) — only for permission denials

9. All levels exhausted? -> Level 5: Rethink approach
```

---

## Anti-Patterns

### A1: Cargo-Cult Configuration
Adding all levels at once "just in case".

### A2: Tool API Docs in CLAUDE.md
Listing every tool name and parameter. Claude gets this from MCP registration. CLAUDE.md should express **intent**.

### A3: Hook Without CLAUDE.md
Relying only on hooks. Breaks in pipe mode and Task agents.

### A4: Assuming Failure Without Testing
Jumping to Level 3 without observing Level 0 behavior first.

---

## Evidence Source

All findings from systematic testing in `claude-code-playground`:
- Tests 1-9: Agent-kernel MCP adoption
- Tests 2.1-2.3: Blackboard MCP adoption
- Tests 4-9: Blackboard read path (spontaneous retrieval)
- See `claude-code-playground/docs/TEST_FINDINGS.md` for raw data
