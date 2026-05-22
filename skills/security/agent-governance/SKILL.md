---
name: agent-governance
description: Implement hooks for permission control and security in custom agents. Use when adding security controls, blocking dangerous operations, implementing audit trails, or designing permission governance.
allowed-tools: Read, Grep, Glob
---

# Agent Governance Skill

Implement security and governance controls for custom agents using hooks.

## Purpose

Design and implement hook-based governance that controls agent permissions, blocks dangerous operations, and provides audit trails.

## When to Use

- Building agents with security requirements
- Need to block access to sensitive files/operations
- Require audit logging of agent actions
- Implementing permission policies

## Hook Architecture

### Hook Types

> **Documentation Verification:** Hook event types (PreToolUse, PostToolUse, etc.) are Claude Code internal types. For authoritative current types, verify via `hook-management` skill → `docs-management`.

| Hook | When | Use Case |
| --- | --- | --- |
| `PreToolUse` | Before tool executes | Block, validate, log |
| `PostToolUse` | After tool executes | Log results, audit |

### Hook Function Signature

```python
async def hook_function(
    input_data: dict,     # Tool call information
    tool_use_id: str,     # Unique tool call ID
    context: HookContext  # Session context
) -> dict:
    # Return empty dict to allow
    # Return with permissionDecision to block
    pass
```

## Design Process

### Step 1: Identify Security Requirements

Questions to answer:

- What files should be blocked? (e.g., .env, credentials)
- What commands should be blocked? (e.g., rm -rf)
- What operations need logging?
- What tool access needs validation?

### Step 2: Design Hook Matchers

```python
from claude_agent_sdk import HookMatcher

hooks = {
    "PreToolUse": [
        # Match specific tool
        HookMatcher(matcher="Read", hooks=[block_sensitive_files]),

        # Match all tools
        HookMatcher(hooks=[log_all_tool_usage]),
    ],
    "PostToolUse": [
        HookMatcher(hooks=[audit_tool_results]),
    ],
}
```

### Step 3: Implement Hook Functions

**Security Hook (Block Pattern)**:

```python
BLOCKED_PATTERNS = [".env", "credentials", "secrets", ".pem", ".key"]

async def block_sensitive_files(
    input_data: dict,
    tool_use_id: str,
    context: HookContext
) -> dict:
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only check file operations
    if tool_name not in ["Read", "Write", "Edit"]:
        return {}

    file_path = tool_input.get("file_path", "")

    # Check for blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if pattern in file_path.lower():
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"Security: Access to {pattern} files blocked",
                }
            }

    return {}  # Allow
```

**Audit Hook (Log Pattern)**:

```python
async def log_all_tool_usage(
    input_data: dict,
    tool_use_id: str,
    context: HookContext
) -> dict:
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    session_id = input_data.get("session_id", "unknown")

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "tool": tool_name,
        "input": tool_input,
    }

    # Write to audit log
    log_file = Path("audit_logs") / f"{session_id}.jsonl"
    log_file.parent.mkdir(exist_ok=True)
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return {}  # Always allow (logging only)
```

**Validation Hook (Conditional Pattern)**:

```python
async def validate_bash_commands(
    input_data: dict,
    tool_use_id: str,
    context: HookContext
) -> dict:
    tool_name = input_data.get("tool_name", "")

    if tool_name != "Bash":
        return {}

    command = input_data.get("tool_input", {}).get("command", "")

    DANGEROUS_PATTERNS = [
        r"rm\s+-rf\s+/",
        r"sudo\s+rm",
        r":(){ :|:& };:",  # Fork bomb
    ]

    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command):
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"Security: Dangerous command blocked",
                }
            }

    return {}
```

### Step 4: Configure Agent with Hooks

```python
hooks = {
    "PreToolUse": [
        HookMatcher(matcher="Read", hooks=[block_sensitive_files]),
        HookMatcher(matcher="Bash", hooks=[validate_bash_commands]),
        HookMatcher(hooks=[log_all_tool_usage]),
    ],
    "PostToolUse": [
        HookMatcher(hooks=[audit_tool_results]),
    ],
}

options = ClaudeAgentOptions(
    system_prompt=system_prompt,
    model="opus",
    hooks=hooks,
)
```

## Common Governance Patterns

### File Access Control

```python
ALLOWED_DIRECTORIES = ["src/", "docs/", "tests/"]

async def restrict_file_access(input_data, tool_use_id, context) -> dict:
    file_path = input_data.get("tool_input", {}).get("file_path", "")

    if not any(file_path.startswith(d) for d in ALLOWED_DIRECTORIES):
        return deny_response("Access restricted to allowed directories")

    return {}
```

### Rate Limiting

```python
tool_call_counts = defaultdict(int)
RATE_LIMITS = {"WebFetch": 10, "Bash": 50}

async def rate_limit_tools(input_data, tool_use_id, context) -> dict:
    tool_name = input_data.get("tool_name", "")

    if tool_name in RATE_LIMITS:
        tool_call_counts[tool_name] += 1
        if tool_call_counts[tool_name] > RATE_LIMITS[tool_name]:
            return deny_response(f"Rate limit exceeded for {tool_name}")

    return {}
```

### Content Filtering

```python
BLOCKED_CONTENT = ["api_key", "password", "secret"]

async def filter_output_content(input_data, tool_use_id, context) -> dict:
    tool_output = input_data.get("tool_output", "")

    for blocked in BLOCKED_CONTENT:
        if blocked.lower() in tool_output.lower():
            return deny_response("Output contains sensitive content")

    return {}
```

## Output Format

When designing governance:

```markdown
## Governance Design

**Agent:** [agent name]
**Security Level:** [low/medium/high]

### Requirements

- [ ] Requirement 1
- [ ] Requirement 2

### Hooks

**PreToolUse:**
| Matcher | Hook | Purpose |
| --- | --- | --- |
| Read | block_sensitive_files | Block .env, credentials |
| Bash | validate_commands | Block dangerous commands |
| * | log_usage | Audit all tool calls |

**PostToolUse:**
| Matcher | Hook | Purpose |
| --- | --- | --- |
| * | audit_results | Log tool outputs |

### Implementation

[Hook function implementations]

### Test Scenarios

| Scenario | Expected | Actual |
| --- | --- | --- |
| Read .env file | Blocked |  |
| Read src/main.py | Allowed |  |
| rm -rf / | Blocked |  |
```

## Design Checklist

- [ ] Security requirements identified
- [ ] File access controls defined
- [ ] Command validation rules defined
- [ ] Audit logging implemented
- [ ] Hook matchers configured
- [ ] Test scenarios documented
- [ ] Error messages are helpful

## Key Insight

> "Hooks enable governance and permission checks in custom agents."

Hooks work for both main agent and subagents spawned via Task tool.

## Cross-References

- @custom-agent-design skill - Agent design workflow
- @core-four-custom.md - Governance in Core Four
- @hook-management skill - Hook management patterns

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
