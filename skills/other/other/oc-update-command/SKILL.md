---
name: oc-update-command
description: >-
  Updates an existing OpenCode command to match current platform best practices,
  fixes deprecated patterns, and validates the result. Use when user says
  "update opencode command", "fix opencode command", "migrate command to opencode",
  or wants to modernize an existing OpenCode command file.
user-invocable: true
disable-model-invocation: false
allowed-tools: AskUserQuestion, Task, Read, Write, Edit, Glob, Grep
---

# Update OpenCode Command

You are initiating the OpenCode command update workflow. This process locates an existing command, researches current platform best practices, analyzes the command for issues, and applies updates with validation.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

---

## Phase 1: Load References

Read the OpenCode platform overview and command guide:

1. Read `${CLAUDE_PLUGIN_ROOT}/references/platform-overview.md`
2. Read `${CLAUDE_PLUGIN_ROOT}/references/command-guide.md`

---

## Phase 2: Locate Command

Find the command to update.

If `$ARGUMENTS` is provided:
1. Check if the argument is a file path — read it directly
2. If it's a command name — search for `{name}.md` in known directories

If no arguments:
1. Search for OpenCode commands in the workspace:
   - `Glob` for `.opencode/commands/*.md`
   - `Glob` for `~/.config/opencode/commands/*.md`
2. Present found commands using `AskUserQuestion`:
   - Header: "Select Command"
   - Question: "Which command would you like to update?"
   - Options: List found commands (up to 4; include "Other" for custom path)

Read the selected command file and store its contents.

---

## Phase 3: Research

Spawn the researcher agent to check latest documentation:

```
Task:
  subagent_type: "agent-alchemy-opencode-tools:oc-researcher"
  prompt: |
    Research the latest OpenCode documentation for command format compatibility.

    Artifact type: command
    Current artifact content:
    ---
    {contents of the command file}
    ---

    Specific questions:
    1. Are there any new command frontmatter fields?
    2. Has the $VARIABLE system changed?
    3. Are there new command discovery paths?
    4. Any changes to the model override behavior?

    Reference guide: ${CLAUDE_PLUGIN_ROOT}/references/command-guide.md
```

---

## Phase 4: Analyze

Compare the existing command against current best practices:

### Frontmatter Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| Wrong model format | Must be `provider/model-id` if present | Convert format |
| Skill-only frontmatter | Fields like `user-invocable`, `name`, `allowed-tools` | Remove |
| Missing `description` | Should have for command listing | Add |
| Unknown `agent` value | If `agent` field present, agent must exist | Verify or remove |
| `subtask` type | Must be boolean if present | Fix type |

### Body Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| Inconsistent $VARIABLEs | Mixed case or invalid patterns | Standardize to uppercase |
| Claude Code tool names | `AskUserQuestion` instead of `question` | Convert |
| `mcp__` format | Double-underscore MCP naming | Convert to single-underscore |
| Hardcoded paths | System-specific absolute paths | Convert to relative, $VARIABLE, or `@filepath` reference |
| Very long body | Commands should be concise workflow shortcuts | Suggest splitting into a skill |
| Missing shell injection | Could use `` !`command` `` for dynamic context | Suggest where appropriate |

### Structure Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| No clear steps | Unstructured instructions | Add numbered steps |
| Missing output specification | No description of expected output | Add output section |
| Unused variables | $VARIABLEs declared but never used in body | Remove or use |

---

## Phase 5: Present Findings

Present the analysis:

```
## Update Analysis: {command-name}

### Errors (must fix)
{list}

### Warnings (should fix)
{list}

### Suggestions
{list}

### Research Notes
{findings}
```

Use `AskUserQuestion` for approval:
- Header: "Apply Updates"
- Question: "Would you like to apply these updates?"
- Options:
  - "Apply all"
  - "Errors and warnings only"
  - "Errors only"
  - "Cancel"
- multiSelect: false

---

## Phase 6: Apply Updates

Apply changes based on user selection:

1. Use `Edit` to modify the command file
2. Fix frontmatter first, then body content
3. Preserve the command's intent

---

## Phase 7: Validate

Spawn the validator agent:

```
Task:
  subagent_type: "agent-alchemy-opencode-tools:oc-validator"
  prompt: |
    Validate the following OpenCode artifact:

    Type: command
    Path: {path to updated file}
    Reference guide: ${CLAUDE_PLUGIN_ROOT}/references/command-guide.md
```

Present validation results and a before/after summary.

**CRITICAL**: Complete ALL 7 phases before finishing.
