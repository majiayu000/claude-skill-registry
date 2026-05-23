---
name: copilot-ask
description: Ask GitHub Copilot CLI questions about code to understand implementations, architecture, patterns, and debugging. Use when the user asks how code works, where something is implemented, what patterns are used, or needs read-only understanding. Requires Copilot CLI installed.
allowed-tools: Bash, Read, Grep, Glob
---

# Copilot Ask Skill

Use GitHub Copilot CLI to answer questions about code without making modifications. This is a read-only analysis skill.

## When to Use

- User asks "how does X work?"
- User wants to find where something is implemented
- User needs to understand architecture or patterns
- User is debugging and needs to understand code flow
- User asks "what does this code do?"

## Prerequisites

Verify GitHub Copilot CLI is available:

```bash
copilot --version
```

Note: Copilot will ask you to trust the files in the current folder before it can read them.

## Basic Usage

### Step 1: Parse the Question

Extract what the user wants to know and the scope (files, feature, component).

### Step 2: Launch Copilot CLI

```bash
cd /path/to/project
copilot
```

### Step 3: Ask the Question

Provide a clear prompt:

```
Explain how [FEATURE/COMPONENT] works in this codebase.

Please provide:
1. Direct answer to the question
2. Specific file paths and line numbers
3. Code examples from the actual codebase
4. Related concepts or dependencies

Do NOT make any changes - this is read-only analysis.
```

### Step 4: Present the Answer

Format with:

- Summary (1-2 sentences)
- Details (explanation)
- File references (paths + line numbers)
- Code examples
- Related info (dependencies, gotchas)

## Tips

- Use `@path/to/file` to include a specific file in the prompt.
- Use `/usage` to view session usage details.
- Use `/model` to pick another model if needed.
- Use `?` or `copilot help` to see available commands.

## Use Custom Instructions

Copilot CLI automatically loads repository instructions if present:

- `.github/copilot-instructions.md`
- `.github/copilot-instructions/**/*.instructions.md`
- `AGENTS.md` (agent instructions)

## Error Handling

- If Copilot is not found, ensure it is installed per the prerequisites in README.md and available in PATH.
- If authentication fails, run `/login` and follow prompts.
- If the answer is unclear, narrow the question and include file paths.

## Related Skills

- `copilot-exec` for code modifications
- `copilot-review` for code reviews

## Limitations

- Read-only analysis
- Interactive mode only
- Limited by current codebase context
