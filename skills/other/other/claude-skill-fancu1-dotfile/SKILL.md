---
name: claude-skill
description: 'Use when user asks to leverage claude or claude code to do something (e.g. implement a feature design or review codes, etc). Provides non-interactive automation mode for hands-off task execution without approval prompts.'
---

# Claude Code Headless Mode

You are operating in **Claude Code headless mode** - a non-interactive automation mode for hands-off task execution.

## Prerequisites

Before using this skill, ensure Claude Code CLI is installed and configured:

1. **Installation verification**:

   ```bash
   claude --version
   ```

2. **First-time setup**: If not installed, guide the user to install Claude Code CLI with command `npm install -g @anthropic-ai/claude-code`.

## References

- For extended usage scenarios, see `references/examples.md`.

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

### Permission Modes

Claude Code uses permission modes to control what operations are permitted. Set via `--permission-mode` flag:

| Mode | Description |
|------|-------------|
| `default` | Standard behavior - prompts for permission on first use of each tool |
| `acceptEdits` | Automatically accepts file edit permissions for the session **(Default for this skill)** |
| `plan` | Plan Mode - Claude can analyze but not modify files or execute commands |
| `bypassPermissions` | Skips all permission prompts (requires safe environment - see warning below) |

**Accept Edits Mode (`--permission-mode acceptEdits`)** - Default

- Automatically accepts file edits without prompts
- Still requires approval for shell commands
- **Recommended for most programming tasks**
- **This is the default mode for this skill**

**Default Mode (`--permission-mode default`)**

- Requires approval for file edits and command execution
- Safe for exploration and analysis tasks

**Plan Mode (`--permission-mode plan`)**

- Read-only analysis mode
- Claude can explore and analyze but cannot modify files
- Cannot execute commands
- Useful for code review and architecture analysis

**Bypass Permissions Mode (`--permission-mode bypassPermissions`)**

- Skips ALL permission prompts
- **⚠️ WARNING: Only use in externally sandboxed environments (containers, VMs)**
- **NEVER use on your development machine without proper isolation**
- Use with `--allowedTools` to restrict specific tools for safety

## Claude Code CLI Commands

**Note**: The following commands are based on the official Claude Code headless mode documentation.

### Basic Headless Execution

Use the `--print` (or `-p`) flag to run in non-interactive mode:

```bash
claude -p "analyze the codebase structure and explain the architecture"
```

### Tool Permissions

Control which tools Claude can use with `--allowedTools` and `--disallowedTools`:

```bash
# Allow specific tools
claude -p "stage my changes and write commits" \
  --allowedTools "Bash,Read" \
  --permission-mode acceptEdits

# Allow multiple tools (space-separated)
claude -p "implement the feature" \
  --permission-mode acceptEdits \
  --allowedTools Bash Read Write Edit

# Allow tools with restrictions (comma-separated string)
claude -p "run tests" \
  --permission-mode acceptEdits \
  --allowedTools "Bash(npm test),Read"

# Disallow specific tools
claude -p "analyze the code" \
  --disallowedTools "Bash,Write"
```

### Using Permission Modes

Control how permissions are handled:

```bash
# Accept file edits automatically (recommended for programming)
claude -p "implement the user authentication feature" \
  --permission-mode acceptEdits \
  --allowedTools "Bash,Read,Write,Edit"

# Combine with allowed tools for safe automation
claude -p "fix the bug in login flow" \
  --permission-mode acceptEdits \
  --allowedTools "Read,Write,Edit,Bash(npm test)"
```

### Output Formats

#### Text Output (Default)

```bash
claude -p "explain file src/components/Header.tsx"
# Output: Plain text response
```

#### JSON Output

Returns structured data including metadata:

```bash
claude -p "how does the data layer work?" --output-format json
```

Response format:

```json
{
  "type": "result",
  "subtype": "success",
  "total_cost_usd": 0.003,
  "is_error": false,
  "duration_ms": 1234,
  "duration_api_ms": 800,
  "num_turns": 6,
  "result": "The response text here...",
  "session_id": "abc123"
}
```

#### Streaming JSON Output

Streams each message as it is received:

```bash
claude -p "build an application" \
  --permission-mode acceptEdits \
  --output-format stream-json
```

Each conversation begins with an initial `init` system message, followed by user and assistant messages, followed by a final `result` system message with stats.

### Multi-Turn Conversations

For multi-turn conversations, you can resume or continue sessions:

```bash
# Continue the most recent conversation
claude --continue --permission-mode acceptEdits "now refactor this for better performance"

# Resume a specific conversation by session ID
claude --resume 550e8400-e29b-41d4-a716-446655440000 \
  --permission-mode acceptEdits "update the tests"

# Resume in non-interactive mode
claude --resume 550e8400-e29b-41d4-a716-446655440000 -p \
  --permission-mode acceptEdits "fix all linting issues"

# Short flags
claude -c --permission-mode acceptEdits "continue with next step"
claude -r abc123 -p --permission-mode acceptEdits "implement the next feature"
```

### System Prompt Customization

Append custom instructions to the system prompt:

```bash
claude -p "review this code" \
  --append-system-prompt "Focus on security vulnerabilities and performance issues"
```

### MCP Server Configuration

Load MCP servers from a JSON configuration file:

```bash
claude -p "analyze the metrics" \
  --mcp-config monitoring-tools.json \
  --allowedTools "mcp__datadog,mcp__prometheus"
```

### Verbose Logging

Enable verbose output for debugging:

```bash
claude -p "debug this issue" --verbose
```

### Combined Examples

Combine multiple flags for complex scenarios:

```bash
# Full automation with JSON output
claude -p "implement authentication and output results" \
  --permission-mode acceptEdits \
  --allowedTools "Bash,Read,Write,Edit" \
  --output-format json

# Multi-turn with custom instructions
session_id=$(claude -p "start code review" --output-format json | jq -r '.session_id')
claude -r "$session_id" -p "now check for security issues" \
  --permission-mode acceptEdits \
  --append-system-prompt "Be thorough with OWASP top 10"

# Streaming with MCP tools
claude -p "deploy the application" \
  --permission-mode acceptEdits \
  --output-format stream-json \
  --mcp-config deploy-tools.json \
  --allowedTools "mcp__kubernetes,mcp__docker"
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

### Error Handling

- Check exit codes and stderr for errors
- Use timeouts for long-running operations:

  ```bash
  timeout 300 claude -p "$complex_prompt" --permission-mode acceptEdits || echo "Timed out after 5 minutes"
  ```

- Respect rate limits when making multiple requests by adding delays between calls

## When to Interrupt Execution

Only pause for user input when encountering:

- **Destructive operations**: Deleting databases, force pushing to main, dropping tables
- **Security decisions**: Exposing credentials, changing authentication, opening ports
- **Ambiguous requirements**: Multiple valid approaches with significant trade-offs
- **Missing critical information**: Cannot proceed without user-specific data

For all other decisions, proceed autonomously using best judgment.

## Final Output Format

Always conclude with a structured summary:

```text
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

## Examples

See `references/examples.md` for extended usage scenarios.

## Handling Errors

When errors occur:

1. Attempt automatic recovery if possible
2. Log the error clearly in the output
3. Continue with remaining tasks if error is non-blocking
4. Report all errors in the final summary
5. Only stop if the error makes continuation impossible

## Resumable Execution

If execution is interrupted:

- Clearly state what was completed
- Provide the session ID for resuming: `claude --resume <session_id> -p "continue" --permission-mode acceptEdits`
- List any state that needs to be preserved
- Explain what remains to be done
