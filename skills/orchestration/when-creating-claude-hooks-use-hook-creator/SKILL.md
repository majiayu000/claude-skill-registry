---
name: hook-creator
description: Create Claude Code hooks with proper schemas, RBAC integration, and performance requirements. Use when implementing PreToolUse, PostToolUse, SessionStart, or any of the 10 hook event types for automation, validation, or security enforcement.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
model: sonnet
---

# SKILL: Hook Creator



---

## LIBRARY-FIRST PROTOCOL (MANDATORY)

**Before writing ANY code, you MUST check:**

### Step 1: Library Catalog
- Location: `.claude/library/catalog.json`
- If match >70%: REUSE or ADAPT

### Step 2: Patterns Guide
- Location: `.claude/docs/inventories/LIBRARY-PATTERNS-GUIDE.md`
- If pattern exists: FOLLOW documented approach

### Step 3: Existing Projects
- Location: `D:\Projects\*`
- If found: EXTRACT and adapt

### Decision Matrix
| Match | Action |
|-------|--------|
| Library >90% | REUSE directly |
| Library 70-90% | ADAPT minimally |
| Pattern exists | FOLLOW pattern |
| In project | EXTRACT |
| No match | BUILD (add to library after) |

---

## Purpose

Create production-ready Claude Code hooks that integrate with our RBAC security system,
follow official schemas, and meet performance requirements (<20ms for pre-hooks).

## When to Use This Skill

- Creating new automation hooks (pre/post operations)
- Implementing security validation hooks
- Building audit/logging hooks
- Extending the RBAC permission system
- Adding custom session management hooks

## 8-Stage Hook Creation Methodology

### Stage 1: Hook Type Selection

Identify which of the 10 hook event types you need:

| Category | Hook Type | Purpose |
|----------|-----------|---------|
| **Blocking** | UserPromptSubmit | Validate/modify user prompts |
| **Blocking** | SessionStart | Initialize session state |
| **Blocking** | PreToolUse | Validate tool operations |
| **Blocking** | PermissionRequest | Auto-approve/deny permissions |
| **Observational** | PostToolUse | Log tool results |
| **Observational** | Notification | Forward notifications |
| **Observational** | Stop | Cleanup on agent stop |
| **Observational** | SubagentStop | Track subagent completion |
| **Observational** | PreCompact | Preserve context during compaction |
| **Observational** | SessionEnd | Final session cleanup |

### Stage 2: Schema Definition

Define input/output schemas based on hook type.

**PreToolUse Input**:
```json
{
  "session_id": "string",
  "tool_name": "Bash|Read|Write|Edit|...",
  "tool_input": { "...tool-specific..." }
}
```

**Blocking Output**:
```json
{
  "continue": true|false,
  "decision": "approve|block|modify",
  "reason": "string (if blocked)",
  "suppressOutput": false,
  "updatedInput": { "..." }
}
```

**Non-Blocking Output**:
```json
{
  "suppressOutput": false
}
```

### Stage 3: Template Selection

Use our pre-built templates:

- `pre-hook-template.js` - For blocking hooks (PreToolUse, UserPromptSubmit)
- `post-hook-template.js` - For observational hooks (PostToolUse, SessionEnd)
- `session-hook-template.js` - For session lifecycle hooks

Generate from templates:
```bash
node hook-template-generator.js --type pre --name my-validator --event PreToolUse
```

### Stage 4: Core Logic Implementation

Implement the hook's core logic:

```javascript
#!/usr/bin/env node
const fs = require('fs');

// Read input from stdin
const input = JSON.parse(fs.readFileSync(0, 'utf-8'));

// Your validation/processing logic
function processHook(input) {
  // Implement your logic here
  return { continue: true, decision: "approve" };
}

// Execute and output result
try {
  const result = processHook(input);
  console.log(JSON.stringify(result));
} catch (error) {
  console.error(`[HOOK ERROR] ${error.message}`);
  console.log(JSON.stringify({ continue: true }));  // Fail open
  process.exit(1);
}
```

### Stage 5: RBAC Integration

For security hooks, integrate with our identity system:

```javascript
const { validateAgentIdentity, loadAgentIdentityByName } = require('../utils/identity');

// Verify agent identity
const identity = loadAgentIdentityByName(input.agent_name);
const validation = validateAgentIdentity(identity);

if (!validation.valid) {
  return {
    continue: false,
    decision: "block",
    reason: `Invalid agent identity: ${validation.errors.join(', ')}`
  };
}
```

### Stage 6: Performance Optimization

Meet performance targets:

| Hook Type | Target | Max |
|-----------|--------|-----|
| Pre-hooks | <20ms | 100ms |
| Post-hooks | <100ms | 1000ms |

**Optimization Patterns**:
- Cache identity lookups
- Avoid synchronous I/O in hot paths
- Use matchers to filter events
- Batch logging operations

### Stage 7: Testing

Create test scenarios:

```javascript
// test-my-hook.js
const testCases = [
  {
    name: "Should approve valid operation",
    input: { tool_name: "Read", tool_input: { file_path: "/src/app.js" } },
    expectedOutput: { continue: true, decision: "approve" }
  },
  {
    name: "Should block dangerous command",
    input: { tool_name: "Bash", tool_input: { command: "rm -rf /" } },
    expectedOutput: { continue: false, decision: "block" }
  }
];
```

### Stage 8: Registration

Register in settings.json:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "node /path/to/your/hook.js",
        "timeout": 5000,
        "matcher": { "tool_name_regex": "^(Bash|Write|Edit)$" }
      }
    ]
  }
}
```

## Hook Templates

### Pre-Hook Template (Blocking)

Location: `resources/templates/pre-hook-template.js`

Features:
- Input validation
- Error handling with fail-open
- Performance timing
- RBAC integration point

### Post-Hook Template (Observational)

Location: `resources/templates/post-hook-template.js`

Features:
- Async-safe logging
- Metric collection
- Non-blocking execution
- Error isolation

## Output Artifacts

1. `{hook-name}.js` - Main hook script
2. `{hook-name}.test.js` - Test file
3. Settings entry for `.claude/settings.json`

## Integration Points

- **RBAC System**: `hooks/12fa/utils/identity.js`
- **Permission Checker**: `hooks/12fa/permission-checker.js`
- **Budget Tracker**: `hooks/12fa/budget-tracker.js`
- **Reference Docs**: `hooks/12fa/docs/CLAUDE-CODE-HOOKS-REFERENCE.md`

## Agents Used

| Agent | Role |
|-------|------|
| hook-creator | Generate hook code from templates |
| coder | Implement custom logic |
| reviewer | Validate hook implementation |
| tester | Create and run test scenarios |

## Example Invocations

**Create a command validator hook**:
```
User: "Create a hook that blocks any Bash command containing 'sudo'"

hook-creator:
  1. Hook Type: PreToolUse (blocking)
  2. Schema: PreToolUse input, blocking output
  3. Template: pre-hook-template.js
  4. Logic: Check tool_input.command for 'sudo'
  5. RBAC: Not required (simple validation)
  6. Performance: Target <10ms (regex only)
  7. Tests: Valid command, sudo command, edge cases
  8. Register in settings.json with Bash matcher
```

**Create an audit logging hook**:
```
User: "Create a hook that logs all file writes to an audit trail"

hook-creator:
  1. Hook Type: PostToolUse (observational)
  2. Schema: PostToolUse input, non-blocking output
  3. Template: post-hook-template.js
  4. Logic: Append to audit JSONL file
  5. RBAC: Load agent identity for WHO tag
  6. Performance: Target <50ms (file append)
  7. Tests: Successful write, failed write, large file
  8. Register with Write/Edit matcher
```

## Security Considerations

1. **Never log sensitive data** - Filter passwords, API keys, tokens
2. **Validate all input** - Treat hook input as untrusted
3. **Fail open for non-security hooks** - Don't block on errors
4. **Fail closed for security hooks** - Block on validation errors
5. **Use absolute paths** - Avoid path traversal vulnerabilities

## Shell Script Best Practices (Codex Recommendations)

When creating bash/shell hooks, follow these best practices:

### 1. Enable Strict Mode

Always start shell hooks with strict mode:
```bash
#!/bin/bash
set -euo pipefail

# -e: Exit on error
# -u: Treat unset variables as errors
# -o pipefail: Pipe fails if any command fails
```

### 2. Proper Variable Quoting

Always quote variable expansions to prevent word splitting:
```bash
# GOOD
FILE_PATH="${HOME}/.claude/state.json"
if [[ -f "$FILE_PATH" ]]; then
    cat "$FILE_PATH"
fi

# BAD - unquoted variables can break with spaces
FILE_PATH=${HOME}/.claude/state.json
if [ -f $FILE_PATH ]; then  # Breaks if path has spaces
    cat $FILE_PATH
fi
```

### 3. Defensive jq Usage

Handle jq failures gracefully:
```bash
# GOOD - handle missing keys and errors
VALUE=$(echo "$JSON" | jq -r '.key // "default"' 2>/dev/null || echo "default")

# BAD - crashes if key missing or json invalid
VALUE=$(echo "$JSON" | jq -r '.key')
```

### 4. Ensure Directories Exist

Create directories before writing:
```bash
STATE_DIR="${HOME}/.claude/my-hook"
mkdir -p "$STATE_DIR" 2>/dev/null
```

### 5. Use Environment Variables for Paths

Never hardcode project paths:
```bash
# GOOD - configurable via environment
PROJECT_PATH="${MY_PROJECT_PATH:-/default/path}"

# BAD - hardcoded, breaks on other systems
PROJECT_PATH="/c/Users/john/projects/myapp"
```

## ANTI-PATTERNS TO AVOID

These patterns caused real bugs in production hooks. NEVER use them:

### ANTI-PATTERN 1: Using grep -P (Perl Regex)

**Problem**: `grep -P` requires Perl regex support, not available on all systems.

```bash
# BAD - grep -P not portable
FOUND=$(echo "$TEXT" | grep -oP '(?<=<tag>).*?(?=</tag>)')

# GOOD - use bash regex matching
if [[ "$TEXT" =~ \<tag\>([^\<]+)\</tag\> ]]; then
    FOUND="${BASH_REMATCH[1]}"
fi
```

### ANTI-PATTERN 2: Using sed -i Directly

**Problem**: `sed -i` behaves differently on macOS (requires `''`), Linux, and Windows Git Bash.

```bash
# BAD - not portable
sed -i 's/old/new/' "$FILE"

# ALSO BAD - OS detection is fragile
if [[ "$(uname -s)" == "Darwin" ]]; then
    sed -i '' 's/old/new/' "$FILE"
else
    sed -i 's/old/new/' "$FILE"
fi

# GOOD - portable temp file approach
sed_inplace() {
    local pattern="$1"
    local file="$2"
    local temp_file="${file}.tmp.$$"
    sed "$pattern" "$file" > "$temp_file" && mv "$temp_file" "$file"
}
sed_inplace 's/old/new/' "$FILE"
```

### ANTI-PATTERN 3: Hardcoded Paths

**Problem**: Hardcoded paths break on other systems or when projects move.

```bash
# BAD - hardcoded
cd D:/Projects/connascence
python analyze.py

# GOOD - environment variable with fallback
CONNASCENCE_PATH="${CONNASCENCE_PROJECT_PATH:-D:/Projects/connascence}"
if [[ -d "$CONNASCENCE_PATH" ]]; then
    cd "$CONNASCENCE_PATH"
    python analyze.py
else
    echo "ERROR: Connascence project not found at $CONNASCENCE_PATH" >&2
    exit 1
fi
```

### ANTI-PATTERN 4: Missing Directory Creation

**Problem**: Writing to directories that don't exist causes silent failures.

```bash
# BAD - assumes directory exists
echo "$DATA" > ~/.claude/my-hook/state.json

# GOOD - ensure directory exists first
STATE_DIR="${HOME}/.claude/my-hook"
mkdir -p "$STATE_DIR" 2>/dev/null
echo "$DATA" > "$STATE_DIR/state.json"
```

### ANTI-PATTERN 5: Blocking cat Reads

**Problem**: Using `cat` without timeout can block indefinitely if stdin never closes.

```bash
# BAD - can block forever
INPUT=$(cat)

# GOOD - use timeout or check for input
INPUT=$(timeout 5 cat 2>/dev/null || echo "{}")

# OR check if stdin has data
if [[ -t 0 ]]; then
    # No stdin data, use default
    INPUT="{}"
else
    INPUT=$(cat)
fi
```

### ANTI-PATTERN 6: Silent Failures

**Problem**: Errors are silently swallowed, making debugging impossible.

```bash
# BAD - silent failure
jq '.key' "$FILE" 2>/dev/null

# GOOD - log errors to stderr, handle gracefully
if ! VALUE=$(jq -r '.key' "$FILE" 2>&1); then
    echo "[HOOK ERROR] Failed to parse $FILE: $VALUE" >&2
    VALUE="default"
fi
```

## Hook Validation Checklist

Before deploying a hook, verify:

- [ ] Uses `set -euo pipefail` (or equivalent error handling)
- [ ] All variables are properly quoted
- [ ] No `grep -P` usage (use bash regex or grep -E)
- [ ] No direct `sed -i` (use temp file approach)
- [ ] No hardcoded paths (use environment variables)
- [ ] Directories created before use
- [ ] jq errors handled gracefully
- [ ] Timeout on stdin reads if applicable
- [ ] Errors logged to stderr
- [ ] Tested on target platform (Windows Git Bash/macOS/Linux)

## Performance Monitoring

Add performance logging to all hooks:

```javascript
const start = process.hrtime.bigint();
// ... hook logic ...
const durationMs = Number(process.hrtime.bigint() - start) / 1_000_000;
console.error(`[PERF] ${hookName} completed in ${durationMs.toFixed(2)}ms`);
```

## Related Skills

- `hooks-automation` - General hook automation patterns
- `cicd-intelligent-recovery` - Error recovery patterns
- `cascade-orchestrator` - Multi-hook coordination

---

*Last Updated: 2025-12-30*
*Integrated with: Claude Code Hooks v1.0.0*
