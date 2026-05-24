---
name: oc-create-command
description: >-
  Guides through creating a new OpenCode command with interactive interview,
  $VARIABLE configuration, and validation. Use when user says "create opencode
  command", "new opencode command", "build command for opencode", or wants to
  create an OpenCode command markdown file.
user-invocable: true
disable-model-invocation: false
allowed-tools: AskUserQuestion, Task, Read, Write, Edit, Glob, Grep
---

# Create OpenCode Command

You are initiating the OpenCode command creation workflow. This process guides the user through an interactive interview to gather requirements, generates a properly formatted command markdown file, and validates the result.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

---

## Phase 1: Load References

Read the OpenCode platform overview and command guide:

1. Read `${CLAUDE_PLUGIN_ROOT}/references/platform-overview.md`
2. Read `${CLAUDE_PLUGIN_ROOT}/references/command-guide.md`

---

## Phase 2: Interview

Gather requirements through a structured interview.

### Round 1: Basics

**Question 1 — Command Name:**
- Header: "Command Name"
- Question: "What should this command be named? It will be invoked as `/{name}`. Use kebab-case."
- Options:
  - "I'll type the name" — Let me provide a custom name

**Question 2 — Purpose:**
- Header: "Purpose"
- Question: "What does this command do?"
- Options:
  - "Workflow shortcut" — Automates a frequently used multi-step process
  - "Template task" — Structured prompt with variable inputs
  - "Scripted operation" — Executes specific tool sequences
  - "Custom" — I'll describe it

**Question 3 — Description:**
- Header: "Description"
- Question: "Briefly describe what this command does (shown in the command list)."
- Options:
  - "I'll type a description" — Let me write a custom description

### Round 2: Variables & Model

**Question 1 — Variables:**
- Header: "Variables"
- Question: "Does the command need user-provided input via $VARIABLE placeholders?"
- Options:
  - "Yes, I'll list them" — I need specific named variables
  - "Just $ARGUMENTS" — A single free-text argument
  - "No variables" — The command works without user input
- multiSelect: false

If "Yes":

**Question 2 — Variable Names:**
- Header: "Var Names"
- Question: "List the variable names (e.g., FILE_PATH, TARGET_BRANCH, OUTPUT_FORMAT). Each becomes a $VARIABLE prompt."
- Options:
  - "I'll type them" — Let me list the variable names

**Question 3 — Model Override:**
- Header: "Model"
- Question: "Should this command use a specific model? (Commands are the only extension type with per-invocation model override.)"
- Options:
  - "No override (Recommended)" — Use the session's current model
  - "Opus" — Use anthropic/claude-opus-4-6 for complex reasoning
  - "Sonnet" — Use anthropic/claude-sonnet-4-6 for balanced performance
  - "Haiku" — Use anthropic/claude-haiku-4-5 for speed
- multiSelect: false

**Question 4 — Agent Routing:**
- Header: "Agent"
- Question: "Should this command be routed to a specific agent?"
- Options:
  - "No (Recommended)" — Use the current agent context
  - "Yes" — Route to a specific named agent
- multiSelect: false

### Round 3: Location

**Question 1 — Location:**
- Header: "Location"
- Question: "Where should the command be created?"
- Options:
  - "Project (.opencode/commands/)" — Available only in this project
  - "Global (~/.config/opencode/commands/)" — Available in all projects
  - "Custom path" — I'll specify the directory
- multiSelect: false

### Interview Summary

Present a summary:

```
## Command Summary

- **Name**: {name} (invoked as /{name})
- **Description**: {description}
- **Variables**: {list of $VARIABLE names or "none"}
- **Model override**: {model or "none"}
- **Agent**: {agent name or "none"}
- **Location**: {path}
```

Use `AskUserQuestion` to confirm:
- Header: "Confirm"
- Question: "Does this look correct? Ready to generate the command?"
- Options:
  - "Yes, generate it"
  - "Make changes"

---

## Phase 3: Generate

Spawn the generator agent:

```
Task:
  subagent_type: "agent-alchemy-opencode-tools:oc-generator"
  prompt: |
    Generate an OpenCode command with these specifications:

    Type: command
    Name: {name}
    Description: {description}
    Variables: {list of $VARIABLE names}
    Model override: {model or "none"}
    Agent: {agent name or "none"}
    Subtask: {true/false}
    Purpose: {detailed purpose from interview}
    Target path: {target directory}/commands/{name}.md

    NOTE: Commands support `agent` (which agent executes) and `subtask` (force subagent execution) frontmatter fields in addition to `model` and `description`.

    Reference guide: ${CLAUDE_PLUGIN_ROOT}/references/command-guide.md
    Template: ${CLAUDE_PLUGIN_ROOT}/references/templates/command-template.md

    Interview notes:
    {all gathered requirements}
```

---

## Phase 4: Validate

Spawn the validator agent:

```
Task:
  subagent_type: "agent-alchemy-opencode-tools:oc-validator"
  prompt: |
    Validate the following OpenCode artifact:

    Type: command
    Path: {path to generated file}
    Reference guide: ${CLAUDE_PLUGIN_ROOT}/references/command-guide.md
```

If validation fails with errors, fix and re-validate.

---

## Phase 5: Present

Present the generated command:

1. Read the generated file
2. Show the file contents
3. Explain key design decisions:
   - $VARIABLE placeholder usage
   - Model override rationale (if applicable)
   - Why command vs skill was the right choice
4. Show validation results
5. Explain how to invoke: `/{name}` in the OpenCode TUI
6. If variables are present, show what the user will be prompted for

**CRITICAL**: Complete ALL 5 phases before finishing.
