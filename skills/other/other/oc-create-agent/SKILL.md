---
name: oc-create-agent
description: >-
  Guides through creating a new OpenCode-compatible agent with interactive
  interview, permission configuration, and validation. Use when user says
  "create opencode agent", "new opencode agent", "build agent for opencode",
  or wants to create an OpenCode agent markdown file.
user-invocable: true
disable-model-invocation: false
allowed-tools: AskUserQuestion, Task, Read, Write, Edit, Glob, Grep
---

# Create OpenCode Agent

You are initiating the OpenCode agent creation workflow. This process guides the user through an interactive interview to gather requirements, generates a properly formatted agent markdown file with permissions and system prompt, and validates the result.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

---

## Phase 1: Load References

Read the OpenCode platform overview and agent guide:

1. Read `${CLAUDE_PLUGIN_ROOT}/references/platform-overview.md`
2. Read `${CLAUDE_PLUGIN_ROOT}/references/agent-guide.md`

---

## Phase 2: Interview

Gather requirements through a structured interview.

### Round 1: Identity

**Question 1 — Agent Name:**
- Header: "Agent Name"
- Question: "What should this agent be named? Use kebab-case (e.g., `code-reviewer`, `test-runner`)."
- Options:
  - "I'll type the name" — Let me provide a custom name

**Question 2 — Purpose:**
- Header: "Purpose"
- Question: "What does this agent do? Describe its main function."
- Options:
  - "Code analysis" — Reviews or analyzes code
  - "Code generation" — Writes new code or modifies existing code
  - "Research" — Gathers information from docs, web, or codebase
  - "Automation" — Executes multi-step workflows

**Question 3 — Mode:**
- Header: "Mode"
- Question: "How will this agent be used?"
- Options:
  - "Primary (Recommended)" — Interactive agent the user switches to via @name
  - "Subagent" — Spawned by other skills/agents via the task tool
  - "Both" — Works as primary and subagent
- multiSelect: false

### Round 2: Model & Behavior

**Question 1 — Model Tier:**
- Header: "Model"
- Question: "What model tier should this agent use?"
- Options:
  - "Sonnet (Recommended)" — Good balance of capability and speed
  - "Opus" — Maximum reasoning capability for complex tasks
  - "Haiku" — Fast and lightweight for simple tasks
  - "Default" — Use the session's current model
- multiSelect: false

**Question 2 — Temperature:**
- Header: "Temperature"
- Question: "How deterministic should responses be?"
- Options:
  - "Low (0.3)" — More consistent, factual responses
  - "Default (0.7)" — Balanced creativity and consistency
  - "High (0.9)" — More creative and varied responses
- multiSelect: false

**Question 3 — Steps Limit:**
- Header: "Steps"
- Question: "Should there be a limit on agentic iterations?"
- Options:
  - "Default" — No explicit limit
  - "Conservative (25)" — Limit to prevent runaway loops
  - "Generous (100)" — Allow extended multi-step workflows
  - "Custom" — I'll specify a number
- multiSelect: false

### Round 3: Permissions

**Question 1 — Permission Level:**
- Header: "Permissions"
- Question: "What permission level should the agent have?"
- Options:
  - "Read-only" — Can read, glob, grep only. No writes, edits, or bash.
  - "Standard" — Read allowed, write/edit/bash require approval
  - "Full access" — All tools auto-allowed
  - "Custom" — I'll configure per-tool permissions
- multiSelect: false

If "Custom" selected:

**Question 2 — File Operations:**
- Header: "File Ops"
- Question: "File operation permissions?"
- Options:
  - "read: allow, write: ask, edit: ask" — Read freely, ask for writes
  - "read: allow, write: allow, edit: allow" — Full file access
  - "read: allow, write: deny, edit: deny" — Read only
- multiSelect: false

**Question 3 — Execution:**
- Header: "Execution"
- Question: "Bash execution permission?"
- Options:
  - "deny" — No shell access
  - "ask" — Require approval for each command
  - "allow" — Auto-approve all commands
- multiSelect: false

**Question 4 — Web Access:**
- Header: "Web"
- Question: "Web access permissions?"
- Options:
  - "No web access" — Deny websearch and webfetch
  - "Search only" — Allow websearch, deny webfetch
  - "Full web access" — Allow both websearch and webfetch
- multiSelect: false

### Round 4: System Prompt

**Question 1 — Prompt Focus:**
- Header: "Focus Areas"
- Question: "What should the system prompt emphasize? Select all that apply."
- Options:
  - "Structured output" — Agent produces formatted reports or specific formats
  - "Tool usage patterns" — Agent follows specific tool usage workflows
  - "Domain expertise" — Agent has specialized knowledge in a domain
  - "Phase-based workflow" — Agent works through numbered phases
- multiSelect: true

**Question 2 — Constraints:**
- Header: "Constraints"
- Question: "Any important constraints for the agent?"
- Options:
  - "No destructive actions" — Never delete files or drop data
  - "Stay in scope" — Don't explore beyond the assigned area
  - "Concise output" — Keep responses short and focused
  - "No constraints" — Let the agent operate freely
- multiSelect: true

### Round 5: Location & Display

**Question 1 — Location:**
- Header: "Location"
- Question: "Where should the agent be created?"
- Options:
  - "Project (.opencode/agents/)" — Available only in this project
  - "Global (~/.config/opencode/agents/)" — Available in all projects
  - "Custom path" — I'll specify the directory
- multiSelect: false

**Question 2 — Display:**
- Header: "Display"
- Question: "Agent display preferences?"
- Options:
  - "Default" — Standard display, visible in @-mention list
  - "Custom color" — I'll pick a color
  - "Hidden" — Don't show in @-mention list
- multiSelect: false

### Interview Summary

Present a comprehensive summary:

```
## Agent Summary

- **Name**: {name}
- **Description**: {generated description}
- **Mode**: {primary/subagent/all}
- **Model**: {provider/model-id}
- **Temperature**: {value}
- **Steps**: {value or "default"}
- **Permissions**: {summary}
- **Focus areas**: {list}
- **Constraints**: {list}
- **Location**: {path}
```

Use `AskUserQuestion` to confirm:
- Header: "Confirm"
- Question: "Does this look correct? Ready to generate the agent?"
- Options:
  - "Yes, generate it" — Proceed with generation
  - "Make changes" — I want to adjust something

---

## Phase 3: Generate

Spawn the generator agent:

```
Task:
  subagent_type: "agent-alchemy-opencode-tools:oc-generator"
  prompt: |
    Generate an OpenCode agent with these specifications:

    Type: agent
    Name: {name}
    Description: {description}
    Mode: {mode}
    Model: {model}
    Temperature: {temperature}
    Steps: {steps}
    Permissions: {permission object}
    Color: {color or null}
    Hidden: {true/false}
    System prompt focus: {focus areas}
    Constraints: {constraints}
    Target path: {target directory}/agents/{name}.md

    Reference guide: ${CLAUDE_PLUGIN_ROOT}/references/agent-guide.md
    Template: ${CLAUDE_PLUGIN_ROOT}/references/templates/agent-template.md

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

    Type: agent
    Path: {path to generated file}
    Reference guide: ${CLAUDE_PLUGIN_ROOT}/references/agent-guide.md
```

If validation fails with errors, fix the issues and re-validate.

---

## Phase 5: Present

Present the generated agent:

1. Read the generated file
2. Show the file contents with syntax highlighting
3. Explain key design decisions:
   - Permission model rationale
   - Why certain mode was chosen
   - Model tier selection reasoning
   - System prompt structure
4. Show validation results
5. Explain how to use the agent:
   - Primary: `@{name}` in the TUI
   - Subagent: `task({ prompt: "...", command: "{name}" })`
6. If applicable, explain how to configure the model in `opencode.json`

**CRITICAL**: Complete ALL 5 phases before finishing.
