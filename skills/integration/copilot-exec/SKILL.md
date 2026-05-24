---
name: copilot-exec
description: Execute development tasks using GitHub Copilot CLI for code generation, refactoring, feature implementation, and bug fixes. Use when the user asks to create code, add features, refactor, fix bugs, or generate tests. Requires Copilot CLI installed.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Copilot Exec Skill

Use GitHub Copilot CLI to execute development tasks that involve code modifications. This skill modifies code.

## When to Use

- User asks to add, create, implement, or generate code
- User wants to refactor existing code
- User needs to fix a bug
- User wants to create tests
- User asks to update or modify code

## Prerequisites

Verify GitHub Copilot CLI is available:

```bash
copilot --version
```

Note: Copilot will ask you to trust the files in the current folder before it can read them.

## Basic Usage

### Step 1: Understand the Task

Clarify:

- What to create/modify?
- Which files are affected?
- Expected outcome?
- Constraints or requirements?

### Step 2: Gather Context

Review current state:

```bash
git status
git diff
```

Read relevant files to understand patterns.

### Step 3: Launch Copilot CLI

```bash
cd /path/to/project
copilot
```

### Step 4: Execute the Task

Provide clear instructions:

```
[TASK DESCRIPTION]

Follow these guidelines:
- Follow existing code patterns and conventions
- Add appropriate error handling
- Include necessary imports
- Maintain readability and style
- Use proper types if applicable
- Add comments for complex logic

Project context:
- Language: [e.g., TypeScript + React]
- Build tool: [e.g., Vite, webpack]
- Package manager: [e.g., npm, pnpm, yarn]
- Coding style: [e.g., see eslint config]

Preview all changes before applying them.
```

### Step 5: Review and Approve

Copilot CLI will ask for approvals before it changes files or runs commands. Review each action and approve only what is correct.

### Step 6: Verify Changes

```bash
git status
git diff
```

Run lint/tests if available.

### Step 7: Report Results

Provide:

- Files modified/created
- Summary of changes
- Verification results
- Issues or follow-ups

## Tips

- Use `@path/to/file` to focus Copilot on a file.
- Use `/agent` to pick a custom agent, or run:

  ```bash
  copilot --agent=refactor-agent --prompt "Refactor src/auth/*"
  ```

- Use `/add-dir` or `--add-dir` to add extra directories.
- Use `/cwd` or `--cwd` to set the working directory.
- Use `/model` to pick another model if needed.

## Use Custom Instructions

Copilot CLI automatically loads repository instructions if present:

- `.github/copilot-instructions.md`
- `.github/copilot-instructions/**/*.instructions.md`
- `AGENTS.md` (agent instructions)

## Error Handling

- If Copilot is not found, ensure it is installed per the prerequisites in README.md and available in PATH.
- If authentication fails, run `/login` and follow prompts.
- If results are off, refine the prompt and include file paths.

## Related Skills

- `copilot-ask` for read-only questions
- `copilot-review` for code reviews

## Limitations

- Interactive mode by default
- Requires explicit approvals for file edits and commands
- Limited by current codebase context
