---
name: hooks-manager
description: Create, validate, and deploy Claude Code hooks for workflow automation. Hooks enable event-driven automation at 8 lifecycle points (PreToolUse, PostToolUse, UserPromptSubmit, etc.) with structured JSON control. Use when automating code formatting, security gates, observability integration, validation enforcement, or any event-driven workflow automation in Claude Code.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Hooks Manager

## Overview

hooks-manager enables sophisticated workflow automation through Claude Code's hooks system (released June 2025).

**Purpose**: Create event-driven automation for code formatting, security gates, observability, and validation

**Pattern**: Task-based (8 operations, one per hook event + management)

**Key Innovation**: Hooks transform Claude Code from interactive to automated - reducing manual work by up to 92%

**Hook Events Available** (8):
1. **UserPromptSubmit** - Before Claude sees prompts
2. **PreToolUse** - Before tool execution
3. **PostToolUse** - After tool execution
4. **PermissionRequest** - When permissions requested
5. **Notification** - Important events
6. **SessionStart** - Session initialization
7. **SessionEnd** - Session cleanup
8. **Stop** - Conversation termination

---

## When to Use

Use hooks-manager when:

- Auto-formatting code (PostToolUse after Write/Edit)
- Security gates (PreToolUse to block dangerous operations)
- Observability integration (send telemetry on all tool calls)
- Validation enforcement (block invalid operations)
- Workflow automation (trigger actions on events)
- Team standardization (enforce coding standards)

**Production Impact**: Companies report 92% reduction in style review time with PostToolUse formatting hooks

---

## Prerequisites

### Required
- Claude Code (hooks support added June 2025)
- Basic understanding of event-driven programming

### Recommended
- Linter/formatter installed (ESLint, Prettier, Black)
- Security tools (if using security hooks)
- Observability platform (if using telemetry hooks)

---

## Hook Operations

### Operation 1: Create Formatting Hook (PostToolUse)

**Purpose**: Auto-format code after AI writes/edits files

**Use Case**: Enforce coding standards without manual intervention

**Process**:

1. **Choose Formatter**:
   ```bash
   # JavaScript/TypeScript
   npm install --save-dev prettier

   # Python
   pip install black

   # Multi-language
   npm install --save-dev prettier @prettier/plugin-python
   ```

2. **Create Hook Configuration**:
   ```json
   {
     "event": "PostToolUse",
     "tools": ["Write", "Edit"],
     "description": "Auto-format code after Claude writes/edits files",
     "handler": {
       "command": "npx prettier --write \"$FILE\"",
       "timeout": 5000
     },
     "filters": {
       "filePatterns": ["**/*.{ts,tsx,js,jsx,py}"],
       "excludePatterns": ["node_modules/**", "*.min.js"]
     }
   }
   ```

3. **Install Hook**:
   ```bash
   # Global hook (all projects)
   mkdir -p ~/.claude/hooks
   echo '[above-json]' > ~/.claude/hooks/auto-format.json

   # Project-specific
   mkdir -p .claude/hooks
   echo '[above-json]' > .claude/hooks/auto-format.json
   ```

4. **Test Hook**:
   ```bash
   # Have Claude write unformatted code
   # Hook should auto-format after Write/Edit
   # Verify formatted correctly
   ```

**Outputs**:
- Hook configuration file
- Auto-formatting on all code changes
- 92% reduction in style review time

**Validation**:
- [ ] Hook file created
- [ ] Formatter configured correctly
- [ ] File patterns appropriate
- [ ] Tested with Claude Code
- [ ] Formatting works automatically

**Time Estimate**: 30-45 minutes

---

### Operation 2: Create Security Hook (PreToolUse)

**Purpose**: Block dangerous operations before execution

**Use Case**: Prevent accidental production file modifications, destructive commands

**Process**:

1. **Define Security Rules**:
   ```json
   {
     "event": "PreToolUse",
     "tools": ["Write", "Edit", "Bash"],
     "description": "Block dangerous operations",
     "handler": {
       "command": ".claude/hooks/security-check.sh \"$TOOL\" \"$FILE\" \"$COMMAND\""
     },
     "structuredOutput": true
   }
   ```

2. **Create Security Check Script**:
   ```bash
   #!/bin/bash
   # .claude/hooks/security-check.sh

   TOOL=$1
   FILE=$2
   COMMAND=$3

   # Block production file modifications
   if [[ "$FILE" == "/etc/"* ]] || [[ "$FILE" == "/usr/"* ]]; then
     echo '{"continue": false, "stopReason": "Cannot modify system files", "suppressOutput": true}'
     exit 1
   fi

   # Block destructive commands
   if [[ "$COMMAND" =~ rm\ -rf\ / ]] || [[ "$COMMAND" =~ dd\ if ]]; then
     echo '{"continue": false, "stopReason": "Destructive command blocked", "suppressOutput": true}'
     exit 1
   fi

   # Block curl/wget (security risk)
   if [[ "$COMMAND" =~ curl|wget ]]; then
     echo '{"continue": false, "stopReason": "Network commands disabled", "suppressOutput": false}'
     exit 1
   fi

   # Allow operation
   echo '{"continue": true}'
   exit 0
   ```

3. **Install Security Hook**:
   ```bash
   chmod +x .claude/hooks/security-check.sh
   # Hook JSON already configured in step 1
   ```

**Outputs**:
- Security hook blocking dangerous operations
- Protection against accidental damage
- Audit trail of blocked operations

**Validation**:
- [ ] Hook blocks system file modifications
- [ ] Hook blocks destructive commands
- [ ] Hook allows safe operations
- [ ] Structured JSON output correct

**Time Estimate**: 45-60 minutes

---

### Operation 3: Create Observability Hook (Notification)

**Purpose**: Send telemetry to observability platform on important events

**Use Case**: Track AI agent decisions, tool usage, errors

**Process**:

1. **Create Telemetry Hook**:
   ```json
   {
     "event": "Notification",
     "description": "Send telemetry to observability platform",
     "handler": {
       "command": ".claude/hooks/send-telemetry.sh \"$EVENT_TYPE\" \"$MESSAGE\""
     }
   }
   ```

2. **Create Telemetry Script**:
   ```bash
   #!/bin/bash
   # .claude/hooks/send-telemetry.sh

   EVENT_TYPE=$1
   MESSAGE=$2

   # Send to observability platform (example: Victoria Metrics)
   curl -X POST http://localhost:8428/api/v1/write \
     -d "claude_event{type=\"$EVENT_TYPE\"} 1" \
     -d "claude_message{event=\"$EVENT_TYPE\",msg=\"$MESSAGE\"} 1"

   # Or log to file
   echo "$(date -Iseconds) | $EVENT_TYPE | $MESSAGE" >> .claude/telemetry.log

   # Or send to webhook
   # curl -X POST https://your-webhook.com/telemetry \
   #   -H "Content-Type: application/json" \
   #   -d "{\"event\": \"$EVENT_TYPE\", \"message\": \"$MESSAGE\"}"
   ```

3. **Test Telemetry**:
   ```bash
   # Trigger notification in Claude Code
   # Check telemetry.log or observability platform
   cat .claude/telemetry.log
   ```

**Outputs**:
- Telemetry hook sending data
- Observability integration
- Decision tracking

**Validation**:
- [ ] Hook configured
- [ ] Telemetry script working
- [ ] Data reaches destination
- [ ] No performance impact

**Time Estimate**: 30-45 minutes

---

### Operation 4: Create Validation Hook (PreToolUse)

**Purpose**: Validate inputs before tool execution

**Use Case**: Ensure files exist, validate JSON, check permissions

**Process**:

1. **Create Validation Hook**:
   ```json
   {
     "event": "PreToolUse",
     "tools": ["Write"],
     "description": "Validate JSON before writing",
     "handler": {
       "command": ".claude/hooks/validate-json.sh \"$FILE\" \"$CONTENT\""
     },
     "structuredOutput": true
   }
   ```

2. **Create Validation Script**:
   ```bash
   #!/bin/bash
   # .claude/hooks/validate-json.sh

   FILE=$1
   CONTENT=$2

   # Only validate .json files
   if [[ "$FILE" != *.json ]]; then
     echo '{"continue": true}'
     exit 0
   fi

   # Validate JSON syntax
   if echo "$CONTENT" | jq empty 2>/dev/null; then
     echo '{"continue": true}'
     exit 0
   else
     echo '{"continue": false, "stopReason": "Invalid JSON syntax", "suppressOutput": false}'
     exit 1
   fi
   ```

**Outputs**:
- Validation hook preventing invalid writes
- JSON syntax enforcement
- Error prevention

**Validation**:
- [ ] Hook validates JSON files
- [ ] Hook allows non-JSON files
- [ ] Invalid JSON blocked
- [ ] Valid JSON allowed

**Time Estimate**: 20-30 minutes

---

### Operation 5: Create MCP Tool Hook (PreToolUse)

**Purpose**: Control MCP tool access granularly

**Use Case**: Block specific MCP servers or tools

**Process**:

1. **MCP Tool Targeting**:
   ```json
   {
     "event": "PreToolUse",
     "tools": ["mcp__filesystem__*"],
     "description": "Block all filesystem MCP operations",
     "handler": {
       "command": "echo '{\"continue\": false, \"stopReason\": \"Filesystem MCP disabled\"}'"
     },
     "structuredOutput": true
   }
   ```

2. **Selective MCP Control**:
   ```json
   {
     "event": "PreToolUse",
     "tools": ["mcp__github__delete_repository"],
     "description": "Block dangerous GitHub operations",
     "handler": {
       "command": "echo '{\"continue\": false, \"stopReason\": \"Repository deletion disabled\"}'"
     },
     "structuredOutput": true
   }
   ```

**Outputs**:
- Fine-grained MCP control
- Security for MCP operations
- Prevent accidental damage

**Validation**:
- [ ] MCP tools blocked correctly
- [ ] Tool targeting works (mcp__server__tool pattern)
- [ ] Safe operations allowed

**Time Estimate**: 20-30 minutes

---

### Operation 6: Create Comprehensive Hook (SessionStart)

**Purpose**: Initialize environment on session start

**Use Case**: Load context, set variables, validate environment

**Process**:

1. **Session Start Hook**:
   ```json
   {
     "event": "SessionStart",
     "description": "Initialize session with context and validation",
     "handler": {
       "command": ".claude/hooks/session-init.sh"
     }
   }
   ```

2. **Initialization Script**:
   ```bash
   #!/bin/bash
   # .claude/hooks/session-init.sh

   echo "🚀 Claude Code Session Starting..."

   # Load project context
   if [ -f ".claude/PROJECT_CONTEXT.md" ]; then
     echo "📋 Project context available"
   fi

   # Check git status
   if git status --porcelain | grep -q .; then
     echo "⚠️  Uncommitted changes detected"
   fi

   # Load environment
   if [ -f ".env" ]; then
     echo "🔐 Environment variables available"
   fi

   # Run pre-flight checks
   if [ -f ".claude/hooks/pre-flight-check.sh" ]; then
     bash .claude/hooks/pre-flight-check.sh
   fi

   echo "✅ Session initialized"
   ```

**Outputs**:
- Session initialization automation
- Context loading
- Environment validation

**Validation**:
- [ ] Hook runs on session start
- [ ] Context loaded correctly
- [ ] Environment validated

**Time Estimate**: 15-20 minutes

---

### Operation 7: Deploy and Manage Hooks

**Purpose**: Install, update, remove, and audit hooks

**Process**:

1. **Deploy Hook** (global or project):
   ```bash
   # Deploy to global (~/.claude/hooks/)
   deploy-hook --global formatting-hook.json

   # Deploy to project (.claude/hooks/)
   deploy-hook --project security-hook.json
   ```

2. **List Active Hooks**:
   ```bash
   # List all hooks
   ls -la ~/.claude/hooks/
   ls -la .claude/hooks/

   # Parse and display
   for hook in .claude/hooks/*.json; do
     echo "Hook: $(basename $hook)"
     jq '.event, .description' $hook
   done
   ```

3. **Validate Hook**:
   ```bash
   # Test hook in safe environment
   validate-hook formatting-hook.json

   # Expected:
   # ✅ JSON valid
   # ✅ Handler command exists
   # ✅ Event type valid
   # ✅ Structured output correct
   ```

4. **Remove Hook**:
   ```bash
   # Disable hook
   rm .claude/hooks/formatting-hook.json

   # Or rename to .disabled
   mv .claude/hooks/security-hook.json .claude/hooks/security-hook.json.disabled
   ```

**Outputs**:
- Hook deployment automation
- Hook management interface
- Validation before deployment

**Validation**:
- [ ] Can deploy hooks globally and per-project
- [ ] Can list active hooks
- [ ] Can validate hooks safely
- [ ] Can remove/disable hooks

**Time Estimate**: 30-45 minutes

---

### Operation 8: Security Audit Hooks

**Purpose**: Review all active hooks for security issues

**Process**:

1. **Audit All Hooks**:
   ```bash
   # Scan all hook files
   for hook in ~/.claude/hooks/*.json .claude/hooks/*.json; do
     echo "Auditing: $hook"

     # Check for dangerous patterns
     if grep -q "rm -rf\|dd if\|curl.*sudo" $hook; then
       echo "⚠️  Dangerous command detected"
     fi

     # Check for credential leaks
     if grep -q "password\|secret\|token\|api_key" $hook; then
       echo "⚠️  Potential credential exposure"
     fi

     # Validate JSON structure
     jq empty $hook 2>/dev/null || echo "❌ Invalid JSON"
   done
   ```

2. **Generate Security Report**:
   ```markdown
   # Hook Security Audit

   ## Hooks Scanned: 8

   ### HIGH RISK
   None

   ### MEDIUM RISK
   1. observability-hook.json
      - Issue: Sends data to external URL
      - Recommendation: Validate URL is trusted

   ### LOW RISK
   2. formatting-hook.json
      - Info: Executes npx prettier (safe)

   ## Recommendations
   - Review observability destination
   - Consider encrypting telemetry data
   ```

**Outputs**:
- Security audit report
- Risk assessment
- Recommendations

**Validation**:
- [ ] All hooks scanned
- [ ] Security issues identified
- [ ] Recommendations provided

**Time Estimate**: 20-30 minutes

---

## Hook Templates

### Template 1: Auto-Format (PostToolUse)

```json
{
  "event": "PostToolUse",
  "tools": ["Write", "Edit"],
  "description": "Auto-format code after Claude writes",
  "handler": {
    "command": "npx prettier --write \"$FILE\"",
    "timeout": 5000
  },
  "filters": {
    "filePatterns": ["**/*.{ts,tsx,js,jsx}"],
    "excludePatterns": ["node_modules/**", "dist/**", "build/**"]
  }
}
```

**Impact**: 92% reduction in style review time

---

### Template 2: Security Gate (PreToolUse)

```json
{
  "event": "PreToolUse",
  "tools": ["Write", "Edit", "Bash"],
  "description": "Block modifications to production files",
  "handler": {
    "command": ".claude/hooks/security-gate.sh \"$TOOL\" \"$FILE\" \"$COMMAND\""
  },
  "structuredOutput": true
}
```

**Impact**: Prevents accidental production damage

---

### Template 3: Telemetry (Notification)

```json
{
  "event": "Notification",
  "description": "Send telemetry on important events",
  "handler": {
    "command": ".claude/hooks/telemetry.sh \"$EVENT_TYPE\" \"$MESSAGE\""
  }
}
```

**Impact**: Full observability of AI agent behavior

---

### Template 4: Validation (PreToolUse)

```json
{
  "event": "PreToolUse",
  "tools": ["Write"],
  "description": "Validate JSON/YAML before writing",
  "handler": {
    "command": ".claude/hooks/validate-syntax.sh \"$FILE\" \"$CONTENT\""
  },
  "structuredOutput": true
}
```

**Impact**: Prevent invalid file writes

---

### Template 5: Context Loading (SessionStart)

```json
{
  "event": "SessionStart",
  "description": "Load project context on session start",
  "handler": {
    "command": ".claude/hooks/load-context.sh"
  }
}
```

**Impact**: Automatic context initialization

---

### Template 6: Cleanup (SessionEnd)

```json
{
  "event": "SessionEnd",
  "description": "Save state and cleanup on session end",
  "handler": {
    "command": ".claude/hooks/session-cleanup.sh"
  }
}
```

**Impact**: Automatic state preservation

---

## Best Practices

### 1. Structured JSON Output (For Control)

**Standard Exit Codes** (Simple):
- 0: Continue
- Non-zero: Block

**Structured JSON** (Advanced):
```json
{
  "continue": false,
  "stopReason": "Custom blocking reason shown to user",
  "suppressOutput": true
}
```

**When to Use**:
- Need custom error messages
- Want to suppress default output
- Complex control flow

---

### 2. MCP Tool Targeting

**Patterns**:
- `mcp__*`: All MCP tools
- `mcp__server__*`: All tools from specific server
- `mcp__server__tool`: Specific tool only

**Examples**:
```json
// Block all filesystem MCP
"tools": ["mcp__filesystem__*"]

// Block specific GitHub operation
"tools": ["mcp__github__delete_repository"]

// Allow specific, block others
"tools": ["mcp__github__*"],
"handler": "allow-list-check.sh"
```

---

### 3. File Pattern Filters

```json
{
  "filePatterns": [
    "src/**/*.ts",           // Include source files
    "tests/**/*.test.ts"     // Include tests
  ],
  "excludePatterns": [
    "node_modules/**",       // Exclude dependencies
    "**/*.min.js",           // Exclude minified
    ".git/**"                // Exclude git internals
  ]
}
```

**Tip**: Start inclusive, add exclusions as needed

---

### 4. Performance Considerations

**Hook Execution**:
- Hooks run synchronously (blocking)
- Keep handlers fast (<5 seconds)
- Use timeouts to prevent hangs
- Async operations: spawn background process, return immediately

**Example** (Fast hook):
```bash
#!/bin/bash
# Quick validation
if [ ! -f "$FILE" ]; then
  echo '{"continue": false, "stopReason": "File does not exist"}'
  exit 1
fi
echo '{"continue": true}'
exit 0
```

**Example** (Slow operation - backgrounded):
```bash
#!/bin/bash
# Start slow operation in background
(sleep 10 && heavy-operation.sh "$FILE") &

# Return immediately
echo '{"continue": true}'
exit 0
```

---

### 5. Security Best Practices

**Never** in hooks:
- Hardcode credentials
- Execute untrusted input
- Modify critical system files
- Expose sensitive data in logs

**Always** in hooks:
- Validate all inputs
- Use allowlists (not denylists)
- Log security events
- Fail securely (deny by default)

---

## Common Hook Patterns

### Pattern 1: Code Quality Enforcement

**PostToolUse Chain**:
```
Write/Edit → Prettier (format) → ESLint (lint) → TypeScript (type check)
```

**Implementation**:
```json
[
  {
    "event": "PostToolUse",
    "tools": ["Write", "Edit"],
    "handler": "npx prettier --write \"$FILE\""
  },
  {
    "event": "PostToolUse",
    "tools": ["Write", "Edit"],
    "handler": "npx eslint --fix \"$FILE\""
  }
]
```

**Result**: All AI code automatically meets quality standards

---

### Pattern 2: Test-on-Save

**PostToolUse Test Runner**:
```json
{
  "event": "PostToolUse",
  "tools": ["Write", "Edit"],
  "description": "Run tests after code changes",
  "handler": {
    "command": ".claude/hooks/run-tests.sh \"$FILE\""
  },
  "filters": {
    "filePatterns": ["src/**/*.ts"]
  }
}
```

**run-tests.sh**:
```bash
#!/bin/bash
FILE=$1

# Find corresponding test file
TEST_FILE="${FILE/.ts/.test.ts}"
TEST_FILE="${TEST_FILE/src\//tests\/}"

if [ -f "$TEST_FILE" ]; then
  npm test -- "$TEST_FILE" --silent
fi
```

**Result**: Immediate test feedback on every change

---

### Pattern 3: Security Guardrails

**Multi-Layer Security**:
```
PreToolUse → Path traversal check → Permission check → Allowlist check → Allow/Block
```

**Result**: Comprehensive security enforcement

---

### Pattern 4: Observability Pipeline

**Multi-Hook Telemetry**:
```
SessionStart → Log session init
PreToolUse → Log tool attempts
PostToolUse → Log tool results + timing
Notification → Log important events
SessionEnd → Log session summary + metrics
```

**Result**: Complete observability of AI behavior

---

## Troubleshooting

### Hook Not Firing

**Checklist**:
- [ ] Hook file in correct location (~/.claude/hooks/ or .claude/hooks/)
- [ ] Hook file is valid JSON (test with `jq empty hook.json`)
- [ ] Event type correct (UserPromptSubmit, PreToolUse, etc.)
- [ ] Tool name matches (case-sensitive)
- [ ] Claude Code version supports hooks (June 2025+)

**Debug**:
```bash
# Test hook JSON
jq empty .claude/hooks/my-hook.json

# Check hook location
ls -la .claude/hooks/

# Test handler command manually
bash .claude/hooks/handler.sh "test args"
```

---

### Hook Blocking Everything

**Issue**: PreToolUse hook with `{"continue": false}` blocks all operations

**Fix**:
- Check handler script logic
- Ensure conditions are correct
- Add fallback: if unsure, allow (fail open vs. fail closed)
- Test with specific files before deploying

---

### Performance Impact

**Issue**: Hook adds 2-5 seconds to every operation

**Solutions**:
- Optimize handler script (remove slow operations)
- Use background processes for slow tasks
- Add caching (don't re-validate unchanged files)
- Set timeout limits
- Consider removing hook if not valuable

---

## Appendix A: Hook Event Reference

### UserPromptSubmit
**Trigger**: Before Claude processes user prompt
**Use**: Validate prompts, inject context, enhance prompts
**Variables**: `$PROMPT`

### PreToolUse
**Trigger**: Before tool execution
**Use**: Security gates, validation, logging
**Variables**: `$TOOL`, `$FILE`, `$COMMAND`, `$CONTENT`
**Control**: Can block operation

### PostToolUse
**Trigger**: After tool execution
**Use**: Auto-format, linting, testing, cleanup
**Variables**: `$TOOL`, `$FILE`, `$RESULT`

### PermissionRequest
**Trigger**: When Claude requests permissions
**Use**: Auto-approve safe operations, log requests
**Variables**: `$PERMISSION_TYPE`

### Notification
**Trigger**: Important events
**Use**: Telemetry, alerting, logging
**Variables**: `$EVENT_TYPE`, `$MESSAGE`

### SessionStart
**Trigger**: Session initialization
**Use**: Load context, validate environment
**Variables**: None

### SessionEnd
**Trigger**: Session termination
**Use**: Save state, cleanup, metrics
**Variables**: None

### Stop
**Trigger**: Conversation stop
**Use**: Final cleanup, state saving
**Variables**: `$REASON`

---

## Appendix B: Structured JSON Control

### Basic Control (Exit Codes)
```bash
# Allow
exit 0

# Block
exit 1
```

### Advanced Control (JSON)
```json
{
  "continue": boolean,        // Allow operation?
  "stopReason": "string",     // Why blocked (shown to user)
  "suppressOutput": boolean   // Hide default blocking message?
}
```

**When to Use JSON**:
- Custom error messages
- Silent blocking
- Complex control logic

---

## Quick Reference

### The 8 Hook Events

| Event | When | Use For | Can Block? |
|-------|------|---------|------------|
| **UserPromptSubmit** | Before prompt processed | Prompt validation/enhancement | Yes |
| **PreToolUse** | Before tool runs | Security, validation | Yes |
| **PostToolUse** | After tool runs | Format, lint, test | No |
| **PermissionRequest** | Permissions requested | Auto-approve, logging | Yes |
| **Notification** | Important events | Telemetry, alerts | No |
| **SessionStart** | Session begins | Init, context load | No |
| **SessionEnd** | Session ends | Cleanup, save state | No |
| **Stop** | Conversation stops | Final cleanup | No |

### Common Use Cases

| Use Case | Hook Event | Typical Impact |
|----------|------------|----------------|
| **Auto-format code** | PostToolUse | 92% style review reduction |
| **Security gates** | PreToolUse | Prevent production damage |
| **Run tests on save** | PostToolUse | Immediate feedback |
| **Observability** | Notification | Full behavior tracking |
| **JSON validation** | PreToolUse | Prevent invalid writes |
| **Context loading** | SessionStart | Auto-initialization |
| **State saving** | SessionEnd | Preserve progress |
| **MCP control** | PreToolUse | Granular tool access |

---

**hooks-manager enables transformative automation in Claude Code through event-driven hooks, reducing manual work by up to 92% while enforcing security, quality, and observability standards.**

For templates, see examples/. For troubleshooting, see Troubleshooting section.
