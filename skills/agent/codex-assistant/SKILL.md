---
name: codex-assistant
description: Run AI-powered tasks using OpenAI Codex CLI. Use when Claude needs to (1) delegate code analysis or generation tasks to Codex, (2) get a second opinion on code changes, (3) perform parallel AI review, or (4) leverage Codex for specific tasks. Triggers on requests like "use codex to...", "run codex", "ask codex", "codex review".
---

# Codex Assistant

Execute tasks using OpenAI Codex CLI and analyze results.

## Important Limitations

**Codex runs in read-only sandbox mode.** It cannot:
- Create or modify files
- Execute scripts or commands that write to disk
- Run generated code

**Always ask Codex to output results directly to stdout.** Do not request file creation or modification - instead, ask Codex to print/output the code or results, which Claude can then save if needed.

## Command

```bash
codex exec --model gpt-5.2-codex "PROMPT"
```

## Prompt Format

Structure prompts with three sections:

```
# Role
[Describe the role/persona for the task]

# Context
[Include relevant information:]
- File paths and links to documentation
- Memory files or conversation context
- Additional task-relevant details

# Task
[Clear task description]
[Expected deliverables]
```

## Workflow

1. **Construct prompt** - Build structured prompt with Role, Context, Task
2. **Execute codex** - Run command with the formatted prompt
3. **Analyze output** - Review results for:
   - Completeness of task execution
   - Quality and accuracy of output
   - Issues or recommendations identified
   - Actionable items to address

## Example

```bash
codex exec --model gpt-5.2-codex "# Role
Senior code reviewer with expertise in security and best practices.

# Context
Repository: /path/to/project
Files changed: src/auth.py, src/api.py
Branch: feature/user-auth

# Task
Review changes against develop branch.
Search for security issues, bugs, and suggest improvements.
Output your findings and recommendations to stdout."
```

**Note:** Always phrase tasks to output results rather than create/modify files. For code generation, ask Codex to "print the code" or "output the script" instead of "create a file".

## Output Analysis

After codex completes, evaluate:

- **Findings** - Key issues or insights discovered
- **Recommendations** - Suggested improvements or fixes
- **Action items** - Concrete next steps to implement
- **Quality** - Overall assessment of the analysis
