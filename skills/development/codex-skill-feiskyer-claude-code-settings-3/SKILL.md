---
name: codex-skill
description: 'Leverage OpenAI Codex/GPT models for autonomous code implementation. Triggers: "codex", "use gpt", "gpt-5", "gpt-5.2", "let openai", "full-auto", "用codex", "让gpt实现".'
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
- Safe for exploration and analysis tasks
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
- Use flag: `-s danger-full-access` or `--sandbox danger-full-access`

## Codex CLI Commands

**Note**: The following commands include both documented features from the Codex exec documentation and additional flags available in the CLI (verified via `codex exec --help`).

### Model Selection

Specify which model to use with `-m` or `--model` when asked from user (use default model without -m/--model when not):

```bash
codex exec -m gpt-5.2 "refactor the payment processing module"
codex exec -m gpt-5.2-codex "implement the user authentication feature"
codex exec -m gpt-5.2-codex-max "analyze the codebase architecture"
```

### Sandbox Modes

Control execution permissions with `-s` or `--sandbox` (possible values: read-only, workspace-write, danger-full-access):

#### Read-Only Mode

```bash
codex exec -s read-only "analyze the codebase structure and count lines of code"
codex exec --sandbox read-only "review code quality and suggest improvements"
```

Analyze code without making any modifications.

#### Workspace-Write Mode (Recommended for Programming)

```bash
codex exec -s workspace-write "implement the user authentication feature"
codex exec --sandbox workspace-write "fix the bug in login flow"
```

Read and write files within the workspace. **Must be explicitly enabled (not the default). Use this for most programming tasks.**

#### Danger-Full-Access Mode

```bash
codex exec -s danger-full-access "install dependencies and update the API integration"
codex exec --sandbox danger-full-access "setup development environment with npm packages"
```

Network access and system-level operations. Use only when necessary.

### Full-Auto Mode (Convenience Alias)

```bash
codex exec --full-auto "implement the user authentication feature"
```

**Convenience alias for**: `-s workspace-write` (enables file editing).
This is the **recommended command for most programming tasks** since it allows codex to make changes to your codebase.

### Configuration Profiles

Use saved profiles from `~/.codex/config.toml` with `-p` or `--profile` (if supported in your version):

```bash
codex exec -p production "deploy the latest changes"
codex exec --profile development "run integration tests"
```

Profiles can specify default model, sandbox mode, and other options.
*Verify availability with `codex exec --help`*

### Working Directory

Specify a different working directory with `-C` or `--cd` (if supported in your version):

```bash
codex exec -C /path/to/project "implement the feature"
codex exec --cd ~/projects/myapp "run tests and fix failures"
```

*Verify availability with `codex exec --help`*

### Additional Writable Directories

Allow writing to additional directories outside the main workspace with `--add-dir` (if supported in your version):

```bash
codex exec --add-dir /tmp/output --add-dir ~/shared "generate reports in multiple locations"
```

Useful when the task needs to write to specific external directories.
*Verify availability with `codex exec --help`*

### JSON Output

```bash
codex exec --json "run tests and report results"
codex exec --json -s read-only "analyze security vulnerabilities"
```

Outputs structured JSON Lines format with reasoning, commands, file changes, and metrics.

### Save Output to File

```bash
codex exec -o report.txt "generate a security audit report"
codex exec -o results.json --json "run performance benchmarks"
```

Writes the final message to a file instead of stdout.

### Skip Git Repository Check

```bash
codex exec --skip-git-repo-check "analyze this non-git directory"
```

Bypasses the requirement for the directory to be a git repository.

### Resume Previous Session

```bash
codex exec resume --last "now implement the next feature"
```

Resumes the last session and continues with a new task.

### Bypass Approvals and Sandbox (If Available)

**⚠️ WARNING: Verify this flag exists before using ⚠️**

Some versions of Codex may support `--dangerously-bypass-approvals-and-sandbox`:

```bash
codex exec --dangerously-bypass-approvals-and-sandbox "perform the task"
```

**If this flag is available**:
- Skips ALL confirmation prompts
- Executes commands WITHOUT sandboxing
- Should ONLY be used in externally sandboxed environments (containers, VMs)
- **EXTREMELY DANGEROUS - NEVER use on your development machine**

**Verify availability first**: Run `codex exec --help` to check if this flag is supported in your version.

### Combined Examples

Combine multiple flags for complex scenarios:

```bash
# Use specific model with workspace write and JSON output
codex exec -m gpt-5.1-codex -s workspace-write --json "implement authentication and output results"

# Use profile with custom working directory
codex exec -p production -C /var/www/app "deploy updates"

# Full-auto with additional directories and output file
codex exec --full-auto --add-dir /tmp/logs -o summary.txt "refactor and log changes"

# Skip git check with specific model in different directory
codex exec -m gpt-5.1-codex -C ~/non-git-project --skip-git-repo-check "analyze and improve code"
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
**Mode**: Read-only
**Command**:

```bash
codex exec -s read-only "count the total number of lines of code in this project, broken down by language"
```

**Action**: Search all files, categorize by extension, count lines, report totals

### Bug Fixing (Workspace-Write)

**User**: "Use gpt-5 to fix the authentication bug in the login flow"
**Mode**: Workspace-write
**Command**:

```bash
codex exec -m gpt-5 --full-auto "fix the authentication bug in the login flow"
```

**Action**: Find the bug, implement fix, run tests, commit changes

### Feature Implementation (Workspace-Write)

**User**: "Let codex implement dark mode support for the UI"
**Mode**: Workspace-write
**Command**:

```bash
codex exec --full-auto "add dark mode support to the UI with theme context and style updates"
```

**Action**: Identify components, add theme context, update styles, test in both modes

### Batch Operations (Workspace-Write)

**User**: "Have gpt-5.1 update all imports from old-lib to new-lib"
**Mode**: Workspace-write
**Command**:

```bash
codex exec -m gpt-5.1 -s workspace-write "update all imports from old-lib to new-lib across the entire codebase"
```

**Action**: Find all imports, perform replacements, verify syntax, run tests

### Generate Report with JSON Output (Read-Only)

**User**: "Analyze security vulnerabilities and output as JSON"
**Mode**: Read-only
**Command**:

```bash
codex exec -s read-only --json "analyze the codebase for security vulnerabilities and provide a detailed report"
```

**Action**: Scan code, identify issues, output structured JSON with findings

### Install Dependencies and Integrate API (Danger-Full-Access)

**User**: "Install the new payment SDK and integrate it"
**Mode**: Danger-Full-Access
**Command**:

```bash
codex exec -s danger-full-access "install the payment SDK dependencies and integrate the API"
```

**Action**: Install packages, update code, add integration points, test functionality

### Multi-Project Work (Custom Directory)

**User**: "Use codex to implement the API in the backend project"
**Mode**: Workspace-write
**Command**:

```bash
codex exec -C ~/projects/backend --full-auto "implement the REST API endpoints for user management"
```

**Action**: Switch to backend directory, implement API endpoints, write tests

### Refactoring with Logging (Additional Directories)

**User**: "Refactor the database layer and log changes"
**Mode**: Workspace-write
**Command**:

```bash
codex exec --full-auto --add-dir /tmp/refactor-logs "refactor the database layer for better performance and log all changes"
```

**Action**: Refactor code, write logs to external directory, run tests

### Production Deployment (Using Profile)

**User**: "Deploy using the production profile"
**Mode**: Profile-based
**Command**:

```bash
codex exec -p production "deploy the latest changes to production environment"
```

**Action**: Use production config, deploy code, verify deployment

### Non-Git Project Analysis

**User**: "Analyze this legacy codebase that's not in git"
**Mode**: Read-only
**Command**:

```bash
codex exec -s read-only --skip-git-repo-check "analyze the architecture and suggest modernization approach"
```

**Action**: Analyze code structure, provide modernization recommendations

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
