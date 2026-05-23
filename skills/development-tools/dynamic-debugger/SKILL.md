---
name: dynamic-debugger
description: Interactive debugging via DAP-MCP for multiple languages with natural language commands
version: 1.0.0
disableModelInvocation: true
activation_conditions:
  - intent_keywords:
      [
        "debug",
        "breakpoint",
        "step through",
        "step into",
        "step over",
        "inspect",
        "trace execution",
        "call stack",
      ]
  - confidence_threshold: 0.8
  - ask_confirmation_below: 0.8
supported_languages: [python, c, cpp, rust]
planned_languages: [javascript, typescript, go, java, csharp]
dependencies:
  external: [dap-mcp]
  internal: [claude-code-sdk]
resource_requirements:
  memory_mb: 4096
  timeout_minutes: 30
token_budget:
  skill_md: 2000
  reference_md: 4000
  examples_md: 3000
  patterns_md: 2000
---

# Dynamic Debugger Skill

Interactive debugging capability fer Claude Code via DAP-MCP integration. Debug yer code in natural language without leavin' the conversation.

## Overview

This skill enables interactive debuggin' through the Debug Adapter Protocol (DAP) via MCP server integration. Set breakpoints, step through code, inspect variables, and control execution flow across multiple programming languages using natural language commands.

**What ye get:**

- Natural language debugging commands ("set breakpoint at line 42")
- **Current support:** Python (debugpy), C/C++/Rust (lldb)
- **Planned support:** JavaScript/TypeScript, Go, Java, .NET (see configs/future/)
- Automatic intent and language detection
- Session management with resource limits
- Graceful error handling and recovery

## Activation (Opt-In)

**This skill is DISABLED by default** (`disableModelInvocation: true`).

**To enable:**

1. **Explicit invocation** (recommended):

   ```
   "Use the dynamic-debugger skill to debug this function"
   ```

2. **Auto-activation** (edit SKILL.md frontmatter):
   ```yaml
   disableModelInvocation: false # or remove this line
   ```

**Why opt-in?**

- Requires external dap-mcp server installation
- Starts debugger processes (resource intensive)
- Full filesystem access needed
- Best enabled only when actively debugging

## Prerequisites

**Required:**

- dap-mcp server installed (`pip install dap-mcp` or `uv pip install dap-mcp`)
- Language-specific debuggers (current support):
  - Python: debugpy (`pip install debugpy`)
  - C/C++/Rust: lldb-dap (install lldb with DAP support)

**Verification:**

```bash
# Check dap-mcp installation
python3 -m dap_mcp --help

# Check language debuggers
python -c "import debugpy; print('debugpy ready')"
which gdb
dlv version
```

## Quick Start

### Scenario 1: Python Async Bug

**User:** "This async function isn't awaiting properly. Debug it."

**Skill activates automatically:**

1. Detects debugging intent (high confidence)
2. Identifies Python from file extensions
3. Starts debugpy session
4. Sets breakpoint at async function
5. Shows await state and variable values

### Scenario 2: C++ Segfault

**User:** "Getting segfault in malloc. Set a breakpoint."

**Skill response:**

1. Explicit trigger detected ("set a breakpoint")
2. Identifies C++ from file extensions
3. Starts gdb session
4. Catches segfault with stack trace
5. Inspects pointer values at crash point

### Scenario 3: JavaScript Promise Chain

**User:** "Why is this Promise chain not resolving?"

**Skill response:**

1. Implicit trigger detected ("why is")
2. Asks confirmation (medium confidence)
3. Identifies JavaScript from package.json
4. Sets breakpoints in .then() handlers
5. Steps through async flow

## Common Workflows

### Starting a Debug Session

Explicit triggers (auto-start):

- "debug this"
- "set a breakpoint at line X"
- "step through this function"
- "inspect variable X"

Implicit triggers (may ask confirmation):

- "Why is X wrong?"
- "This isn't working"
- "Trace execution of X"
- "Test is failing in X"

### Debugging Commands

**Breakpoint management:**

- "Set breakpoint at line 42"
- "Remove breakpoint at line 42"
- "List all breakpoints"

**Execution control:**

- "Step over" (execute current line)
- "Step into" (enter function call)
- "Step out" (exit current function)
- "Continue" (run until next breakpoint)

**Variable inspection:**

- "What's the value of userId?"
- "Show all local variables"
- "Evaluate expression: x + y"

**Session management:**

- "Show call stack"
- "List threads/goroutines"
- "Stop debugging"

## Navigation Guide (MANDATORY)

**Load these files on demand based on context:**

### When to Load reference.md

**Trigger:** User needs specific API details, configuration syntax, or error codes
**Contains:** Complete API reference, language configurations, session management API, error handling details, resource limits
**Size:** 3,000-4,000 tokens
**Example queries:** "How do I configure the Go debugger?", "What are the resource limits?", "Show me all error codes"

### When to Load examples.md

**Trigger:** User wants working code examples or specific debugging scenarios
**Contains:** Production-ready debugging examples for all 6 languages with complete workflows
**Size:** 2,000-3,000 tokens
**Example queries:** "Show me a Python async debugging example", "How do I debug a Rust panic?", "Example of goroutine deadlock debugging"

### When to Load patterns.md

**Trigger:** User asks about best practices, architectural patterns, or debugging strategies
**Contains:** Production debugging patterns, performance techniques, security best practices, common pitfalls
**Size:** 1,500-2,000 tokens
**Example queries:** "What are best practices for debugging?", "How do I debug performance issues?", "Common security mistakes?"

**Default behavior:** Use only SKILL.md for basic debugging commands. Load supporting files only when explicitly needed.

## Session Management

**Single concurrent session:** Only one debugging session per user at a time
**Timeouts:**

- Session idle: 30 minutes
- Connection idle: 5 minutes
- Startup: 10 seconds max

**Resource limits:**

- Memory: 4GB max for debugged process
- No CPU limits (debugging is resource-intensive)
- Automatic cleanup on session end

## Language Detection

**Automatic detection** via:

1. File extensions (primary signal)
2. Manifest files (package.json, Cargo.toml, go.mod)
3. Project structure analysis

**Confidence thresholds:**

- High (>90%): Auto-select language
- Medium (70-90%): Ask user confirmation
- Low (<70%): Prompt user to specify

**Manual override:** "Debug this as Python code" (bypasses auto-detection)

## Troubleshooting

### dap-mcp Server Not Found

**Symptom:** "dap-mcp server not available"
**Solution:**

```bash
npm install -g dap-mcp
npx dap-mcp --version
```

### Language Debugger Missing

**Symptom:** "debugpy not found" or "gdb not available"
**Solution:** Install language-specific debugger (see Prerequisites)

### Session Timeout

**Symptom:** "Session timed out after 30 minutes"
**Solution:** Start new session with "debug this"

### Concurrent Session Blocked

**Symptom:** "Another debugging session is active"
**Solution:** Stop existing session with "stop debugging" or wait for timeout

### Memory Limit Exceeded

**Symptom:** "Debugged process exceeded 4GB memory limit"
**Solution:** Reduce data structures or use sampling for large datasets

## Error Recovery

All errors provide:

1. Clear description of what failed
2. Actionable recovery steps
3. Manual fallback commands if needed

**Graceful degradation:** If dap-mcp unavailable, skill suggests manual debugger commands.

## Token Budget

- Orchestration overhead: <100 tokens per command
- Intent detection: <20 tokens
- Language detection: <30 tokens (cached after first detection)
- Error messages: <50 tokens

**Design philosophy:** Keep skill orchestration minimal. Most tokens spent on actual debugging interaction, not overhead.

## Security

⚠️ **IMPORTANT SECURITY CONSIDERATIONS:**

- **Full Filesystem Access:** This skill can read/write ANY file on your system (required for debugging)
- **Process Execution:** Starts debugger processes with full system permissions
- **No Sandboxing:** Debugged code runs with your user privileges
- **Local-Only Default:** Server binds to localhost only (do NOT expose to network)
- **Sensitive Data:** Debugger can access memory, environment variables, credentials in running processes

**Best Practices:**

- Only debug code you trust
- Review debugger configurations before use
- Be cautious with production credentials in environment
- Use dedicated development environments for sensitive projects
- Never debug untrusted binaries

**Process Isolation:**

- Debugger runs in separate process from Claude Code
- Cleanup script terminates all debugger processes on exit

## Performance Targets

- Server startup: <10 seconds
- Breakpoint operations: <2 seconds
- Step operations: <3 seconds
- Variable inspection: <2 seconds

## Next Steps

1. **Verify prerequisites** (see Prerequisites section)
2. **Start debugging** with natural language ("debug this")
3. **Load supporting files** only when needed (see Navigation Guide)
4. **Review examples** for specific scenarios (see examples.md)
5. **Learn patterns** for production debugging (see patterns.md)

---

**Philosophy:** Ruthlessly simple orchestration. All complexity lives in dap-mcp server, not in this skill. We're just the friendly pirate captain givin' orders to the debugger crew.
