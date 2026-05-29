---
name: codex-skill
description: 'Leverage OpenAI Codex/GPT models for autonomous code implementation. Triggers: "codex", "use gpt", "gpt-5", "let openai", "full-auto", "用codex", "让gpt实现". Use this skill whenever the user wants to delegate coding tasks to OpenAI models, run code reviews via codex, or execute tasks in a sandboxed environment.'
allowed-tools: Read, Write, Glob, Grep, Task, Bash(cat:*), Bash(ls:*), Bash(tree:*), Bash(codex:*), Bash(codex *), Bash(which:*), Bash(npm:*), Bash(brew:*)
---

# Codex

You are operating in **codex exec** - a non-interactive automation mode for hands-off task execution.

## Prerequisites

Before using this skill, ensure Codex CLI is installed and configured:

1. **Installation verification**:

   ```bash
   codex --version
   ```

2. **First-time setup**: If not installed, guide the user to install Codex CLI with command `npm i -g @openai/codex` or `brew install codex`.

## Core Principles

### Autonomous Execution

- Execute tasks from start to finish without seeking approval for each action
- Make confident decisions based on best practices and task requirements
- Only ask questions if critical information is genuinely missing
- Prioritize completing the workflow over explaining every step

### Output Behavior

- Stream progress updates as you work
- Provide a clear, structured final summary upon completion
- Focus on actionable results and metrics over lengthy explanations
- Report what was done, not what could have been done

### Operating Modes

Codex uses sandbox policies to control what operations are permitted:

**Read-Only Mode (Default)**

- Analyze code, search files, read documentation
- Provide insights, recommendations, and execution plans
- No modifications to the codebase
- **This is the default mode when running `codex exec`**

**Workspace-Write Mode (Recommended for Programming)**

- Read and write files within the workspace
- Implement features, fix bugs, refactor code
- Create, modify, and delete files in the workspace
- Execute build commands and tests
- **Use `--full-auto` or `-s workspace-write` to enable file editing**
- **This is the recommended mode for most programming tasks**

**Danger-Full-Access Mode**

- All workspace-write capabilities
- Network access for fetching dependencies
- System-level operations outside workspace
- Access to all files on the system
- **Use only when explicitly requested and necessary**
- Use flag: `-s danger-full-access`

## Codex CLI Commands

### Model Selection

Codex uses the model configured in `~/.codex/config.toml` by default. Do NOT pass `-m`/`--model` unless the user explicitly asks to use a specific model.

```bash
# Default: uses model from config.toml (recommended)
codex exec --full-auto "refactor the payment processing module"

# Only when user specifies a model explicitly:
codex exec -m gpt-5.2 --full-auto "implement the user authentication feature"
```

### Sandbox Modes

Control execution permissions with `-s` or `--sandbox` (possible values: read-only, workspace-write, danger-full-access):

#### Read-Only Mode

```bash
codex exec "analyze the codebase structure and count lines of code"
codex exec -s read-only "review code quality and suggest improvements"
```

Analyze code without making any modifications.

#### Workspace-Write Mode (Recommended for Programming)

```bash
codex exec -s workspace-write "implement the user authentication feature"
codex exec --full-auto "fix the bug in login flow"
```

Read and write files within the workspace. **Must be explicitly enabled (not the default). Use this for most programming tasks.**

#### Danger-Full-Access Mode

```bash
codex exec -s danger-full-access "install dependencies and update the API integration"
```

Network access and system-level operations. Use only when necessary.

### Full-Auto Mode (Convenience Alias)

```bash
codex exec --full-auto "implement the user authentication feature"
```

**Convenience alias for**: `-s workspace-write` (enables file editing).
This is the **recommended command for most programming tasks** since it allows codex to make changes to your codebase.

### Config Overrides

Override any `config.toml` value inline with `-c` or `--config`:

```bash
# Override model for a single run
codex exec -c model="o3" --full-auto "implement the feature"

# Override sandbox permissions
codex exec -c 'sandbox_permissions=["disk-full-read-access"]' "analyze all files"

# Override nested config values using dotted paths
codex exec -c shell_environment_policy.inherit=all --full-auto "run build"
```

### Feature Toggles

Enable or disable features with `--enable` and `--disable`:

```bash
codex exec --enable multi_agent --full-auto "implement feature across multiple files"
codex exec --disable plan_tool --full-auto "quick fix for typo"
```

Equivalent to `-c features.<name>=true` or `-c features.<name>=false`.

### Image Attachments

Attach images to the prompt with `-i` or `--image`:

```bash
codex exec -i screenshot.png "implement the UI shown in this screenshot"
codex exec -i mockup.png -i spec.png --full-auto "build this component matching the design"
```

### Code Review

Run code reviews with `codex exec review`:

```bash
# Review uncommitted changes (staged, unstaged, and untracked)
codex exec review --uncommitted

# Review changes against a base branch
codex exec review --base main

# Review a specific commit
codex exec review --commit abc1234

# Custom review instructions
codex exec review --base main "focus on security vulnerabilities and error handling"

# Review with a title for the summary
codex exec review --base main --title "Auth feature review"

# Output review as JSON
codex exec review --uncommitted --json -o review.json
```

### Configuration Profiles

Use saved profiles from `~/.codex/config.toml` with `-p` or `--profile`:

```bash
codex exec -p production "deploy the latest changes"
codex exec --profile development "run integration tests"
```

Profiles can specify default model, sandbox mode, and other options.

### Working Directory

Specify a different working directory with `-C` or `--cd`:

```bash
codex exec -C /path/to/project --full-auto "implement the feature"
codex exec --cd ~/projects/myapp --full-auto "run tests and fix failures"
```

### Additional Writable Directories

Allow writing to additional directories outside the main workspace with `--add-dir`:

```bash
codex exec --full-auto --add-dir /tmp/output --add-dir ~/shared "generate reports in multiple locations"
```

### JSON Output

```bash
codex exec --json "run tests and report results"
codex exec --json -s read-only "analyze security vulnerabilities"
```

Outputs structured JSON Lines format with reasoning, commands, file changes, and metrics.

### Structured Output Schema

Constrain the model's final response to match a JSON schema:

```bash
codex exec --output-schema schema.json "analyze the codebase and report findings"
```

### Save Output to File

```bash
codex exec -o report.txt "generate a security audit report"
codex exec -o results.json --json "run performance benchmarks"
```

Writes the final message to a file instead of stdout.

### Ephemeral Mode

Run without persisting session files to disk:

```bash
codex exec --ephemeral --full-auto "quick one-off fix"
```

### Skip Git Repository Check

```bash
codex exec --skip-git-repo-check "analyze this non-git directory"
```

Bypasses the requirement for the directory to be a git repository.

### Resume Previous Session

```bash
# Resume the most recent session
codex exec resume --last "now implement the next feature"

# Resume a specific session by ID
codex exec resume <session-id> "continue working on the API"

# Show all sessions (not filtered by current directory)
codex exec resume --all
```

### Open-Source / Local Models

Use open-source models via local providers:

```bash
codex exec --oss "analyze this code"
codex exec --oss --local-provider ollama "refactor this function"
codex exec --oss --local-provider lmstudio "implement the feature"
```

### Bypass Approvals and Sandbox

**EXTREMELY DANGEROUS — only use in externally sandboxed environments (containers, VMs)**

```bash
codex exec --dangerously-bypass-approvals-and-sandbox "perform the task"
```

Skips ALL confirmation prompts and executes commands WITHOUT sandboxing.

### Combined Examples

Combine multiple flags for complex scenarios:

```bash
# Workspace write with JSON output
codex exec -s workspace-write --json "implement authentication and output results"

# Use profile with custom working directory
codex exec -p production -C /var/www/app "deploy updates"

# Full-auto with additional directories and output file
codex exec --full-auto --add-dir /tmp/logs -o summary.txt "refactor and log changes"

# Image-driven implementation with full-auto
codex exec -i design.png --full-auto "implement the UI matching this design"

# Config override with ephemeral mode
codex exec -c model_reasoning_effort="high" --ephemeral --full-auto "solve this complex bug"

# Code review with JSON output saved to file
codex exec review --base main --json -o review-report.json
```

## Execution Workflow

1. **Parse the Request**: Understand the complete objective and scope
2. **Plan Efficiently**: Create a minimal, focused execution plan
3. **Execute Autonomously**: Implement the solution with confidence
4. **Verify Results**: Run tests, checks, or validations as appropriate
5. **Report Clearly**: Provide a structured summary of accomplishments

## Best Practices

### Speed and Efficiency

- Make reasonable assumptions when minor details are ambiguous
- Use parallel operations whenever possible (read multiple files, run multiple commands)
- Avoid verbose explanations during execution - focus on doing
- Don't seek confirmation for standard operations

### Scope Management

- Focus strictly on the requested task
- Don't add unrequested features or improvements
- Avoid refactoring code that isn't part of the task
- Keep solutions minimal and direct

### Quality Standards

- Follow existing code patterns and conventions
- Run relevant tests after making changes
- Verify the solution actually works
- Report any errors or limitations encountered

## When to Interrupt Execution

Only pause for user input when encountering:

- **Destructive operations**: Deleting databases, force pushing to main, dropping tables
- **Security decisions**: Exposing credentials, changing authentication, opening ports
- **Ambiguous requirements**: Multiple valid approaches with significant trade-offs
- **Missing critical information**: Cannot proceed without user-specific data

For all other decisions, proceed autonomously using best judgment.

## Final Output Format

Always conclude with a structured summary:

```
✓ Task completed successfully

Changes made:
- [List of files modified/created]
- [Key code changes]

Results:
- [Metrics: lines changed, files affected, tests run]
- [What now works that didn't before]

Verification:
- [Tests run, checks performed]

Next steps (if applicable):
- [Suggestions for follow-up tasks]
```

## Example Usage Scenarios

### Code Analysis (Read-Only)

**User**: "Count the lines of code in this project by language"

```bash
codex exec "count the total number of lines of code in this project, broken down by language"
```

### Bug Fixing (Workspace-Write)

**User**: "Fix the authentication bug in the login flow"

```bash
codex exec --full-auto "fix the authentication bug in the login flow"
```

### Feature Implementation (Workspace-Write)

**User**: "Let codex implement dark mode support for the UI"

```bash
codex exec --full-auto "add dark mode support to the UI with theme context and style updates"
```

### Code Review

**User**: "Review my changes before I push"

```bash
codex exec review --uncommitted
```

### Image-Based Implementation

**User**: "Build the UI from this mockup"

```bash
codex exec -i mockup.png --full-auto "implement the UI component matching this design"
```

### Install Dependencies and Integrate API (Danger-Full-Access)

**User**: "Install the new payment SDK and integrate it"

```bash
codex exec -s danger-full-access "install the payment SDK dependencies and integrate the API"
```

### Multi-Project Work (Custom Directory)

**User**: "Implement the API in the backend project"

```bash
codex exec -C ~/projects/backend --full-auto "implement the REST API endpoints for user management"
```

### Non-Git Project Analysis

**User**: "Analyze this legacy codebase that's not in git"

```bash
codex exec --skip-git-repo-check "analyze the architecture and suggest modernization approach"
```

## Error Handling

When errors occur:

1. Attempt automatic recovery if possible
2. Log the error clearly in the output
3. Continue with remaining tasks if error is non-blocking
4. Report all errors in the final summary
5. Only stop if the error makes continuation impossible

## Resumable Execution

If execution is interrupted:

- Clearly state what was completed
- Provide exact commands/steps to resume
- List any state that needs to be preserved
- Explain what remains to be done
