---
name: ck-help
version: 1.0.0
description: '[Utilities] ClaudeKit usage guide - just type naturally'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Provide ClaudeKit usage guidance by running the help script and presenting results based on output type.

**Workflow:**

1. **Translate** — Convert user arguments to English if needed
2. **Execute** — Run `python .claude/scripts/ck-help.py "$ARGUMENTS"`
3. **Detect Type** — Read `@CK_OUTPUT_TYPE` marker (comprehensive-docs, category-guide, command-details, search-results, task-recommendations)
4. **Present** — Show COMPLETE script output verbatim, then add practical context and examples

**Key Rules:**

- Never replace or summarize script output; always show it fully then enhance
- `/plan` then `/code` is the correct flow; NEVER suggest `/plan` then `/cook`
- `/cook` is standalone (has its own planning)

Think harder.
All-in-one ClaudeKit guide. Run the script and present output based on type markers.

## Pre-Processing

**IMPORTANT: Always translate `$ARGUMENTS` to English before passing to script.**

The Python script only understands English keywords. If `$ARGUMENTS` is in another language:

1. Translate `$ARGUMENTS` to English
2. Pass the translated English string to the script

## Execution

```bash
python .claude/scripts/ck-help.py "$ARGUMENTS"
```

## Output Type Detection

The script outputs a type marker on the first line: `@CK_OUTPUT_TYPE:<type>`

**Read this marker and adjust your presentation accordingly:**

### `@CK_OUTPUT_TYPE:comprehensive-docs`

Full documentation (config, schema, setup guides).

**Presentation:**

1. Show the **COMPLETE** script output verbatim - every section, every code block
2. **THEN ADD** helpful context:
    - Real-world usage examples ("For example, if you're working on multiple projects...")
    - Common gotchas and tips ("Watch out for: ...")
    - Practical scenarios ("This is useful when...")
3. End with a specific follow-up question

**Example enhancement after showing full output:**

```
## Additional Tips

**When to use global vs local config:**
- Use global (~/.claude/.ck.json) for personal preferences like language, issue prefix style
- Use local (./.claude/.ck.json) for project-specific paths, naming conventions

**Common setup for teams:**
Each team member sets their locale globally, but projects share local config via git.

Need help setting up a specific configuration?
```

### `@CK_OUTPUT_TYPE:category-guide`

Workflow guides for command categories (fix, plan, cook, etc.).

**Presentation:**

1. Show the complete workflow and command list
2. **ADD** practical context:
    - When to use this workflow vs alternatives
    - Real example: "If you encounter a bug in authentication, start with..."
    - Transition tips between commands
3. Offer to help with a specific task

### `@CK_OUTPUT_TYPE:command-details`

Single command documentation.

**Presentation:**

1. Show full command info from script
2. **ADD**:
    - Concrete usage example with realistic input
    - When this command shines vs alternatives
    - Common flags or variations
3. Offer to run the command for them

### `@CK_OUTPUT_TYPE:search-results`

Search matches for a keyword.

**Presentation:**

1. Show all matches from script
2. **HELP** user navigate:
    - Group by relevance if many results
    - Suggest most likely match based on context
    - Offer to explain any specific command
3. Ask what they're trying to accomplish

### `@CK_OUTPUT_TYPE:task-recommendations`

Task-based command suggestions.

**Presentation:**

1. Show recommended commands from script
2. **EXPLAIN** the reasoning:
    - Why these commands fit the task
    - Suggested order of execution
    - What each step accomplishes
3. Offer to start with the first recommended command

## Key Principle

**Script output = foundation. Your additions = value-add.**

Never replace or summarize the script output. Always show it fully, then enhance with your knowledge and context.

## Important: Correct Workflows

- **`/plan` → `/code`**: Plan first, then execute the plan
- **`/cook`**: Standalone - plans internally, no separate `/plan` needed
- **NEVER** suggest `/plan` → `/cook` (cook has its own planning)

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
