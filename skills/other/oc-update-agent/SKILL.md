---
name: oc-update-agent
description: >-
  Updates an existing OpenCode agent to match current platform best practices,
  fixes deprecated patterns, and validates the result. Use when user says
  "update opencode agent", "fix opencode agent", "migrate agent to opencode",
  or wants to modernize an existing OpenCode agent file.
user-invocable: true
disable-model-invocation: false
allowed-tools: AskUserQuestion, Task, Read, Write, Edit, Glob, Grep
---

# Update OpenCode Agent

You are initiating the OpenCode agent update workflow. This process locates an existing agent, researches current platform best practices, analyzes the agent for outdated patterns, and applies updates with validation.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

---

## Phase 1: Load References

Read the OpenCode platform overview and agent guide:

1. Read `${CLAUDE_PLUGIN_ROOT}/references/platform-overview.md`
2. Read `${CLAUDE_PLUGIN_ROOT}/references/agent-guide.md`

---

## Phase 2: Locate Agent

Find the agent to update.

If `$ARGUMENTS` is provided:
1. Check if the argument is a file path — read it directly
2. If it's an agent name — search for `{name}.md` in known directories

If no arguments:
1. Search for OpenCode agents in the workspace:
   - `Glob` for `.opencode/agents/*.md`
   - `Glob` for `~/.config/opencode/agents/*.md`
2. Present found agents using `AskUserQuestion`:
   - Header: "Select Agent"
   - Question: "Which agent would you like to update?"
   - Options: List found agents (up to 4; include "Other" for custom path)

Read the selected agent file and store its contents.

---

## Phase 3: Research

Spawn the researcher agent to check latest documentation:

```
Task:
  subagent_type: "agent-alchemy-opencode-tools:oc-researcher"
  prompt: |
    Research the latest OpenCode documentation for agent format compatibility.

    Artifact type: agent
    Current artifact content:
    ---
    {contents of the agent file}
    ---

    Specific questions:
    1. Are there any new agent frontmatter fields?
    2. Have permission syntax rules changed?
    3. Are there new agent modes or capabilities?
    4. Any changes to subagent behavior or limitations?

    Reference guide: ${CLAUDE_PLUGIN_ROOT}/references/agent-guide.md
```

---

## Phase 4: Analyze

Compare the existing agent against current best practices:

### Frontmatter Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| `name` field present | Should not exist — name from filename | Remove |
| `skills` field present | Skills not assignable to agents | Remove |
| Invalid `mode` value | Must be `primary`, `subagent`, or `all` (default: `all`) | Fix or default to `all` |
| Wrong model format | Must be `provider/model-id` | Convert |
| Temperature out of range | Must be 0.0-1.0 | Clamp to valid range |
| `top_p` out of range | Must be 0.0-1.0 if present | Clamp to valid range |
| Invalid permission syntax | Values must be allow/ask/deny/true/false | Fix syntax |
| Missing `description` | Required field | Add based on agent content |

### Body Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| Subagent uses `question` | Subagents can't use question tool | Add note or restructure |
| Claude Code tool names | `AskUserQuestion` instead of `question` | Convert to OpenCode names |
| `mcp__` format | Double-underscore MCP naming | Convert to single-underscore |
| `${CLAUDE_PLUGIN_ROOT}` refs | Claude Code path variable | Remove or convert |
| Missing purpose statement | No clear first sentence | Add purpose statement |
| No output format section | Agent should specify output | Add output format |

### Permission Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| Glob pattern syntax errors | Invalid patterns in permission rules | Fix syntax |
| Overly permissive subagent | Subagent with full write/bash access | Suggest tightening |
| Missing common tools | No read/glob/grep permissions set | Add basic permissions |

---

## Phase 5: Present Findings

Present the analysis organized by severity:

```
## Update Analysis: {agent-name}

### Errors (must fix)
{list with explanations}

### Warnings (should fix)
{list with explanations}

### Suggestions
{list with explanations}

### Research Notes
{findings from researcher agent}
```

Use `AskUserQuestion` for approval:
- Header: "Apply Updates"
- Question: "Would you like to apply these updates?"
- Options:
  - "Apply all" — Fix everything
  - "Errors and warnings only"
  - "Errors only"
  - "Cancel"
- multiSelect: false

---

## Phase 6: Apply Updates

Apply changes based on user selection:

1. Use `Edit` to modify the agent file
2. Fix frontmatter first, then body content
3. Preserve the agent's intent and system prompt personality

---

## Phase 7: Validate

Spawn the validator agent:

```
Task:
  subagent_type: "agent-alchemy-opencode-tools:oc-validator"
  prompt: |
    Validate the following OpenCode artifact:

    Type: agent
    Path: {path to updated file}
    Reference guide: ${CLAUDE_PLUGIN_ROOT}/references/agent-guide.md
```

Present validation results and a before/after summary of changes.

**CRITICAL**: Complete ALL 7 phases before finishing.
