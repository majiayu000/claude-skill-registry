---
name: oc-update-skill
description: >-
  Updates an existing OpenCode skill to match current platform best practices,
  fixes deprecated patterns, and validates the result. Use when user says
  "update opencode skill", "fix opencode skill", "migrate skill to opencode",
  or wants to modernize an existing OpenCode SKILL.md file.
user-invocable: true
disable-model-invocation: false
allowed-tools: AskUserQuestion, Task, Read, Write, Edit, Glob, Grep
---

# Update OpenCode Skill

You are initiating the OpenCode skill update workflow. This process locates an existing skill, researches current platform best practices, analyzes the skill for outdated patterns, and applies updates with validation.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

---

## Phase 1: Load References

Read the OpenCode platform overview and skill guide:

1. Read `${CLAUDE_PLUGIN_ROOT}/references/platform-overview.md`
2. Read `${CLAUDE_PLUGIN_ROOT}/references/skill-guide.md`

---

## Phase 2: Locate Skill

Find the skill to update.

If `$ARGUMENTS` is provided:
1. Check if the argument is a file path — read it directly
2. If it's a skill name — search for it in known discovery paths

If no arguments:
1. Search for OpenCode skills in the workspace:
   - `Glob` for `.opencode/skills/*/SKILL.md`
   - `Glob` for `.claude/skills/*/SKILL.md`
   - `Glob` for `.agents/skills/*/SKILL.md`
2. Present found skills using `AskUserQuestion`:
   - Header: "Select Skill"
   - Question: "Which skill would you like to update?"
   - Options: List found skills (up to 4; include "Other" for custom path)

Read the selected skill file and store its contents.

---

## Phase 3: Research

Spawn the researcher agent to check latest OpenCode documentation:

```
Task:
  subagent_type: "agent-alchemy-opencode-tools:oc-researcher"
  prompt: |
    Research the latest OpenCode documentation for skill format compatibility.

    Artifact type: skill
    Current artifact content:
    ---
    {contents of the skill file}
    ---

    Specific questions:
    1. Are there any new skill frontmatter fields since v1.2.10?
    2. Have any existing fields been deprecated?
    3. Are there new best practices for skill body structure?
    4. Any changes to $VARIABLE placeholder handling?

    Reference guide: ${CLAUDE_PLUGIN_ROOT}/references/skill-guide.md
```

---

## Phase 4: Analyze

Compare the existing skill against current best practices. Check for:

### Frontmatter Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| `name` field missing | Required — must match directory name | Add `name:` matching the parent directory |
| `name` doesn't match directory | Name and directory must be identical | Fix to match |
| `allowed-tools` present | Experimental field (Agent Skills spec) | Keep if intentional; note as experimental |
| `model` field present | Not supported for skills | Remove; configure in opencode.json |
| `disable-model-invocation` | Not supported | Remove |
| `argument-hint` present | Not a valid OpenCode field | Remove; improve description |
| `arguments` present | Not supported; use $VARIABLES | Remove; convert to $VARIABLE patterns |
| Missing `description` | Required field | Add based on skill content |
| Description too vague | Should include trigger phrases | Improve with specific use cases |

### Body Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| File-path skill references | `Read .../SKILL.md` patterns | Convert to `skill({ name: "..." })` |
| `${CLAUDE_PLUGIN_ROOT}` refs | Claude Code path variable | Remove; use name-based loading |
| `mcp__` tool names | Double-underscore MCP format | Convert to `{name}_{tool}` single-underscore |
| Assumes `question` in subagent | Subagents can't use question | Restructure to gather info upfront |
| No phase markers | Complex skill without structure | Add numbered phases |
| Missing completion directive | No "complete ALL phases" note | Add critical completion note |

### Research-Based Issues

Apply any findings from the researcher agent:
- New features to leverage
- Deprecated patterns to remove
- Updated best practices to adopt

---

## Phase 5: Present Findings

Present the analysis results using text output, organized by severity:

```
## Update Analysis: {skill-name}

### Errors (must fix)
{list of errors with explanations}

### Warnings (should fix)
{list of warnings with explanations}

### Suggestions (consider)
{list of suggestions}

### Research Notes
{any findings from the researcher agent}
```

Use `AskUserQuestion` to get user approval:
- Header: "Apply Updates"
- Question: "Would you like to apply these updates?"
- Options:
  - "Apply all" — Fix all issues (errors + warnings + suggestions)
  - "Errors and warnings only" — Fix errors and warnings, skip suggestions
  - "Errors only" — Fix only the must-fix items
  - "Cancel" — Don't make changes
- multiSelect: false

---

## Phase 6: Apply Updates

Based on user selection, apply the changes:

1. Use `Edit` to modify the skill file
2. Fix issues in order: frontmatter first, then body content
3. Preserve the skill's intent — don't rewrite working content unnecessarily

---

## Phase 7: Validate

Spawn the validator agent on the updated file:

```
Task:
  subagent_type: "agent-alchemy-opencode-tools:oc-validator"
  prompt: |
    Validate the following OpenCode artifact:

    Type: skill
    Path: {path to updated file}
    Reference guide: ${CLAUDE_PLUGIN_ROOT}/references/skill-guide.md
```

Present the validation results. If errors remain, offer to fix them.

Show a before/after summary of the changes made.

**CRITICAL**: Complete ALL 7 phases before finishing.
