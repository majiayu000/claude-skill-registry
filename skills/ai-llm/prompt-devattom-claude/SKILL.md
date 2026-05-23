---
name: prompt
description: Load and execute a prompt from the project's .claude/prompts/ directory
argument-hint: <prompt-name>
---

# Prompt Loader

Load and execute prompts stored in the project's `.claude/prompts/` directory.

## Behavior

### If `$ARGUMENTS` is empty → list available prompts

1. Use the Glob tool to find all `.md` files in `.claude/prompts/` (relative to the project root)
2. Display them as a numbered list with just the name (without `.md` extension)
3. Example output:
   ```
   Available prompts:
   1. e2e-student-journey-tests
   2. refactor-auth-module
   3. api-design-review
   ```

### If `$ARGUMENTS` is provided → load and execute the prompt

1. Read the file at `.claude/prompts/$ARGUMENTS.md` (relative to the project root)
   - If the file doesn't exist, also try `.claude/prompts/$ARGUMENTS` (without `.md`)
   - If still not found, list available prompts and suggest the closest match
2. Execute the content of that file as your instructions — follow them exactly as if the user had typed the prompt content directly
