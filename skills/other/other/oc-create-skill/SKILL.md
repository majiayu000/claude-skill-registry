---
name: oc-create-skill
description: >-
  Guides through creating a new OpenCode-compatible skill with interactive
  interview, best-practice enforcement, and validation. Use when user says
  "create opencode skill", "new opencode skill", "build skill for opencode",
  or wants to create an OpenCode SKILL.md file.
user-invocable: true
disable-model-invocation: false
allowed-tools: AskUserQuestion, Task, Read, Write, Edit, Glob, Grep
---

# Create OpenCode Skill

You are initiating the OpenCode skill creation workflow. This process guides the user through an interactive interview to gather requirements, generates a properly formatted SKILL.md file, and validates the result.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

- Every interview question → AskUserQuestion
- Confirmation questions → AskUserQuestion
- Clarifying questions → AskUserQuestion

Text output should only be used for summaries, explanations, and presenting information.

---

## Phase 1: Load References

Read the OpenCode platform overview and skill guide:

1. Read `${CLAUDE_PLUGIN_ROOT}/references/platform-overview.md`
2. Read `${CLAUDE_PLUGIN_ROOT}/references/skill-guide.md`

Store the reference content internally for use throughout the workflow.

---

## Phase 2: Interview

Gather requirements through a structured interview using `AskUserQuestion`.

### Round 1: Basics

Ask these questions using `AskUserQuestion` (max 4 per call):

**Question 1 — Skill Name:**
- Header: "Skill Name"
- Question: "What should this skill be named? Use kebab-case (e.g., `code-review`, `deploy-check`)."
- Options:
  - "I'll type the name" — Let me provide a custom name

**Question 2 — Purpose:**
- Header: "Purpose"
- Question: "What does this skill do? Describe its main function."
- Options:
  - "Code analysis" — Analyzes code for patterns, issues, or quality
  - "Workflow automation" — Automates a multi-step process
  - "Content generation" — Generates code, docs, or other content

**Question 3 — User-Invocable:**
- Header: "Invocable"
- Question: "Should users be able to invoke this skill directly (via `/skill-name`)?"
- Options:
  - "Yes (Recommended)" — Users can invoke it from the command dialog
  - "No" — Helper skill only loaded by other skills
- multiSelect: false

### Round 2: Details

**Question 1 — Target Audience:**
- Header: "Audience"
- Question: "Who is the primary user of this skill?"
- Options:
  - "Developers" — Software developers working on code
  - "DevOps/SRE" — Operations and reliability engineers
  - "All users" — General-purpose, no specific expertise needed

**Question 2 — Variables:**
- Header: "Variables"
- Question: "Does the skill need user input via $VARIABLE placeholders? (e.g., $FILE_PATH, $TARGET_BRANCH)"
- Options:
  - "Yes" — I need specific input values from the user
  - "No" — The skill works without user-provided variables
  - "Just $ARGUMENTS" — A single free-text argument is enough
- multiSelect: false

**Question 3 — Complexity:**
- Header: "Complexity"
- Question: "How complex is the workflow?"
- Options:
  - "Simple" — Single phase, straightforward instructions
  - "Multi-phase" — 2-4 distinct phases with clear boundaries
  - "Complex" — 5+ phases or spawns subagents via task tool
- multiSelect: false

### Round 3: Content (if multi-phase or complex)

If the user selected multi-phase or complex:

**Question 1 — Phases:**
- Header: "Phases"
- Question: "Describe the main phases of the workflow (what happens in each step)."
- Options:
  - "I'll describe them" — Let me explain the phases

**Question 2 — Tools:**
- Header: "Tools"
- Question: "Which tools should the skill primarily use?"
- Options:
  - "Read-only" — read, glob, grep only
  - "Read + write" — read, glob, grep, write, edit
  - "Full access" — All tools including bash
  - "Custom" — I'll specify which tools
- multiSelect: false

### Round 4: Location and Metadata

**Question 1 — Location:**
- Header: "Location"
- Question: "Where should the skill be created?"
- Options:
  - "Project (.opencode/skills/)" — Available only in this project
  - "Global (~/.config/opencode/skills/)" — Available in all projects
  - "Custom path" — I'll specify the directory
- multiSelect: false

**Question 2 — Additional metadata:**
- Header: "Metadata"
- Question: "Any additional metadata to include?"
- Options:
  - "Add license (MIT)" — Include MIT license field
  - "Add compatibility range" — Specify OpenCode version range
  - "Skip metadata" — No additional metadata needed
- multiSelect: true

### Interview Summary

After completing the interview rounds, present a summary of the gathered requirements:

```
## Skill Summary

- **Name**: {name}
- **Description**: {generated from purpose + details}
- **User-invocable**: {yes/no}
- **Variables**: {list or "none"}
- **Phases**: {count and brief description}
- **Tools**: {tool set}
- **Location**: {path}
```

Use `AskUserQuestion` to confirm:
- Header: "Confirm"
- Question: "Does this look correct? Ready to generate the skill?"
- Options:
  - "Yes, generate it" — Proceed with generation
  - "Make changes" — I want to adjust something

If "Make changes", ask what to change and update accordingly.

---

## Phase 3: Generate

Spawn the generator agent to create the skill file:

```
Task:
  subagent_type: "agent-alchemy-opencode-tools:oc-generator"
  prompt: |
    Generate an OpenCode skill with these specifications:

    Type: skill
    Name: {name}
    Description: {description}
    User-invocable: {true/false}
    Variables: {list of $VARIABLE placeholders}
    Phases: {phase descriptions}
    Tool guidance: {which tools to use/avoid}
    Target path: {target directory}/skills/{name}/SKILL.md

    IMPORTANT: The `name` field is REQUIRED in frontmatter. Set it to "{name}" (must match the directory name).

    Reference guide: ${CLAUDE_PLUGIN_ROOT}/references/skill-guide.md
    Template: ${CLAUDE_PLUGIN_ROOT}/references/templates/skill-template.md

    Interview notes:
    {all gathered requirements}
```

---

## Phase 4: Validate

Spawn the validator agent to check the generated file:

```
Task:
  subagent_type: "agent-alchemy-opencode-tools:oc-validator"
  prompt: |
    Validate the following OpenCode artifact:

    Type: skill
    Path: {path to generated file}
    Reference guide: ${CLAUDE_PLUGIN_ROOT}/references/skill-guide.md
```

If validation fails with errors, fix the issues and re-validate.

---

## Phase 5: Present

Present the generated skill to the user:

1. Read the generated file
2. Show the file contents with syntax highlighting
3. Explain key design decisions:
   - Why certain frontmatter fields were included/excluded
   - How phases were structured
   - How $VARIABLE placeholders work
4. Show the validation results (pass/warnings)
5. Explain how to invoke the skill: `/{name}` in the OpenCode TUI

**CRITICAL**: Complete ALL 5 phases before finishing.
