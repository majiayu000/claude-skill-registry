---
name: debugger-detective
description: "⚡ PRIMARY TOOL for: 'why is X broken', 'find bug source', 'root cause analysis', 'trace error', 'debug issue', 'find where X fails'. Uses claudemem v0.3.0 AST with context command for call chain analysis. GREP/FIND/GLOB ARE FORBIDDEN."
allowed-tools: Bash, Task, Read, AskUserQuestion
---

# ⛔⛔⛔ CRITICAL: AST STRUCTURAL ANALYSIS ONLY ⛔⛔⛔

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🧠 THIS SKILL USES claudemem v0.3.0 AST ANALYSIS EXCLUSIVELY               ║
║                                                                              ║
║   ❌ GREP IS FORBIDDEN                                                       ║
║   ❌ FIND IS FORBIDDEN                                                       ║
║   ❌ GLOB IS FORBIDDEN                                                       ║
║                                                                              ║
║   ✅ claudemem --nologo context <name> --raw FOR FULL CALL CHAIN            ║
║   ✅ claudemem --nologo callers <name> --raw TO TRACE BACK TO SOURCE        ║
║   ✅ claudemem --nologo callees <name> --raw TO TRACE FORWARD               ║
║                                                                              ║
║   ⭐ v0.3.0: context shows full call chain for root cause analysis          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

# Debugger Detective Skill

**Version:** 3.3.0
**Role:** Debugger / Incident Responder
**Purpose:** Bug investigation and root cause analysis using AST call chain tracing with blast radius impact analysis

## Role Context

You are investigating this codebase as a **Debugger**. Your focus is on:
- **Error origins** - Where exceptions are thrown
- **Call chains** - How execution flows to the failure point
- **State mutations** - What changed the data before failure
- **Root causes** - The actual source of problems (not just symptoms)
- **Impact radius** - What else might be affected

## Why `context` is Perfect for Debugging

The `context` command shows you:
- **Symbol definition** = Where the buggy code is
- **Callers** = How we got here (trace backwards)
- **Callees** = What happens next (trace forward)
- **Full call chain** = Complete picture for root cause analysis

## Debugger-Focused Commands (v0.3.0)

### Find the Bug Location

```bash
# Find the function mentioned in error
claudemem --nologo symbol authenticate --raw

# Get full context (callers + callees)
claudemem --nologo context authenticate --raw
```

### Trace Back to Source (callers)

```bash
# Who called this function? (trace backwards)
claudemem --nologo callers authenticate --raw

# Follow the chain backwards
claudemem --nologo callers LoginController --raw
claudemem --nologo callers handleRequest --raw
```

### Trace Forward to Effect (callees)

```bash
# What does this function call? (trace forward)
claudemem --nologo callees authenticate --raw

# Find where state changes happen
claudemem --nologo callees updateSession --raw
```

### Blast Radius Analysis (v0.4.0+ Required)

```bash
# After finding the bug, check what else is affected
IMPACT=$(claudemem --nologo impact buggyFunction --raw)

if [ -z "$IMPACT" ] || echo "$IMPACT" | grep -q "No callers"; then
  echo "No static callers - bug is isolated (or dynamically called)"
else
  echo "$IMPACT"
  echo ""
  echo "This shows:"
  echo "- Direct callers (immediately affected)"
  echo "- Transitive callers (potentially affected)"
  echo "- Complete list for testing after fix"
fi
```

**Use for**:
- Post-fix verification (test all impacted code)
- Regression prevention (know what to test)
- Incident documentation (impact scope)

**Limitations:**
Event-driven/callback architectures may have callers not visible to static analysis.

### Error Origin Hunting

```bash
# Map error handling code
claudemem --nologo map "throw error exception" --raw

# Find specific error types
claudemem --nologo symbol AuthenticationError --raw

# Who throws this error?
claudemem --nologo callers AuthenticationError --raw
```

### State Mutation Tracking

```bash
# Find where state changes
claudemem --nologo map "set state update mutate" --raw

# Find the mutation function
claudemem --nologo symbol updateUserState --raw

# Who calls this mutation?
claudemem --nologo callers updateUserState --raw
```

## PHASE 0: MANDATORY SETUP

### Step 1: Verify claudemem v0.3.0

```bash
which claudemem && claudemem --version
# Must be 0.3.0+
```

### Step 2: If Not Installed → STOP

Use AskUserQuestion (see ultrathink-detective for template)

### Step 3: Check Index Status

```bash
# Check claudemem installation and index
claudemem --version && ls -la .claudemem/index.db 2>/dev/null
```

### Step 3.5: Check Index Freshness

Before proceeding with investigation, verify the index is current:

```bash
# First check if index exists
if [ ! -d ".claudemem" ] || [ ! -f ".claudemem/index.db" ]; then
  # Use AskUserQuestion to prompt for index creation
  # Options: [1] Create index now (Recommended), [2] Cancel investigation
  exit 1
fi

# Count files modified since last index
STALE_COUNT=$(find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" \) \
  -newer .claudemem/index.db 2>/dev/null | grep -v "node_modules" | grep -v ".git" | grep -v "dist" | grep -v "build" | wc -l)
STALE_COUNT=$((STALE_COUNT + 0))  # Normalize to integer

if [ "$STALE_COUNT" -gt 0 ]; then
  # Get index time with explicit platform detection
  if [[ "$OSTYPE" == "darwin"* ]]; then
    INDEX_TIME=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" .claudemem/index.db 2>/dev/null)
  else
    INDEX_TIME=$(stat -c "%y" .claudemem/index.db 2>/dev/null | cut -d'.' -f1)
  fi
  INDEX_TIME=${INDEX_TIME:-"unknown time"}

  # Get sample of stale files
  STALE_SAMPLE=$(find . -type f \( -name "*.ts" -o -name "*.tsx" \) \
    -newer .claudemem/index.db 2>/dev/null | grep -v "node_modules" | grep -v ".git" | head -5)

  # Use AskUserQuestion (see template in ultrathink-detective)
fi
```

### Step 4: Index if Needed

```bash
claudemem index
```

---

## Workflow: Bug Investigation (v0.3.0)

### Phase 1: Locate the Symptom

```bash
# Find where the error appears
claudemem --nologo map "error message keywords" --raw

# Or find the specific function
claudemem --nologo symbol failingFunction --raw
```

### Phase 2: Get Full Context

```bash
# Get callers + callees in one command
claudemem --nologo context failingFunction --raw
```

### Phase 3: Trace Backwards (Find Root Cause)

```bash
# For each caller, check if it's the source
claudemem --nologo callers caller1 --raw
claudemem --nologo callers caller2 --raw

# Keep tracing until you find the root
```

### Phase 4: Verify the Chain

```bash
# Once you suspect a root cause, verify the path
claudemem --nologo callees suspectedRoot --raw

# Does it lead to the symptom?
```

### Phase 5: Check Impact

```bash
# What else calls the buggy code?
claudemem --nologo callers buggyFunction --raw

# These are all potentially affected
```

## Output Format: Bug Investigation Report

### 1. Symptom Summary

```
┌─────────────────────────────────────────────────────────┐
│                    BUG INVESTIGATION                     │
├─────────────────────────────────────────────────────────┤
│  Symptom: User sees "undefined" in profile name          │
│  Location: src/components/Profile.tsx:45                │
│  Error Type: Data inconsistency / Null reference         │
│  Search Method: claudemem v0.3.0 (AST call chain)       │
└─────────────────────────────────────────────────────────┘
```

### 2. Call Chain Trace

```
❌ SYMPTOM: undefined rendered
   └── src/components/Profile.tsx:45
       └── user.name is undefined

↑ CALLER CHAIN (trace backwards):
   └── useUser hook (src/hooks/useUser.ts:23)
       ↑
   └── fetchUser API (src/api/user.ts:67)
       ↑
   └── userMapper (src/mappers/user.ts:12)
       ↑
🔍 ROOT CAUSE FOUND HERE
```

### 3. Root Cause Analysis

```
🔍 ROOT CAUSE IDENTIFIED:

Location: src/mappers/user.ts:12
Problem: Field name mismatch

API Response:       { fullName: "John Doe" }
Mapper Expects:     { full_name: "..." }
Result:             name = undefined

Evidence:
- callees of fetchUser → userMapper
- callers of userMapper → useUser → Profile
- Complete chain verified via context command
```

### 4. Impact Analysis

```
⚠️ OTHER AFFECTED CODE:

claudemem --nologo callers userMapper --raw shows:
  - useUser hook (main app)
  - useAdmin hook (admin panel)
  - tests/user.test.ts

All 3 locations may have the same bug!
```

## Scenarios

### Scenario: Null Pointer Exception

```bash
# Step 1: Find where undefined is used
claudemem --nologo map "undefined null" --raw

# Step 2: Get context of the failing function
claudemem --nologo context renderProfile --raw

# Step 3: Trace backwards through callers
claudemem --nologo callers getUserData --raw

# Step 4: Find where null was introduced
claudemem --nologo callees fetchUser --raw
```

### Scenario: Race Condition

```bash
# Step 1: Find async operations
claudemem --nologo map "async await promise" --raw

# Step 2: Find shared state
claudemem --nologo symbol sharedState --raw

# Step 3: Who reads it?
claudemem --nologo callers sharedState --raw

# Step 4: Who writes it?
claudemem --nologo callees updateState --raw
```

### Scenario: Incorrect Behavior

```bash
# Step 1: Find the function with wrong behavior
claudemem --nologo symbol calculateTotal --raw

# Step 2: What does it depend on?
claudemem --nologo callees calculateTotal --raw

# Step 3: Who provides input?
claudemem --nologo callers calculateTotal --raw
```

## Result Validation Pattern

After EVERY claudemem command, validate results:

### Context Validation for Debugging

When tracing call chains:

```bash
CONTEXT=$(claudemem --nologo context failingFunction --raw)
EXIT_CODE=$?

# Check for failure
if [ "$EXIT_CODE" -ne 0 ]; then
  DIAGNOSIS=$(claudemem status 2>&1)
  # Use AskUserQuestion
fi

# Validate all sections present
if ! echo "$CONTEXT" | grep -q "\[symbol\]"; then
  # Missing symbol section - function not found
  # Use AskUserQuestion: Reindex, Different name, or Cancel
fi

if ! echo "$CONTEXT" | grep -q "\[callers\]"; then
  # Missing callers - may be entry point or index issue
  # Entry points (API handlers, main) have 0 callers - this is expected
fi

if ! echo "$CONTEXT" | grep -q "\[callees\]"; then
  # Missing callees - may be leaf function or index issue
  # Leaf functions (console.log, throw) have 0 callees - this is expected
fi
```

### Empty Results Handling

```bash
CALLERS=$(claudemem --nologo callers suspectedBug --raw)

# 0 callers could mean:
# 1. Entry point (main, API handler) - expected
# 2. Dead code - use dead-code command (v0.4.0+)
# 3. Dynamically called - check for import(), eval, reflection

if echo "$CALLERS" | grep -qi "error\|not found"; then
  # Actual error vs no callers
  # Use AskUserQuestion
fi
```

---

## FALLBACK PROTOCOL

**CRITICAL: Never use grep/find/Glob without explicit user approval.**

If claudemem fails or returns irrelevant results:

1. **STOP** - Do not silently switch tools
2. **DIAGNOSE** - Run `claudemem status`
3. **REPORT** - Tell user what happened
4. **ASK** - Use AskUserQuestion for next steps

```typescript
// Fallback options (in order of preference)
AskUserQuestion({
  questions: [{
    question: "claudemem bug investigation failed or found no call chain. How should I proceed?",
    header: "Debugging Issue",
    multiSelect: false,
    options: [
      { label: "Reindex codebase", description: "Run claudemem index (~1-2 min)" },
      { label: "Try different function name", description: "Search for related functions" },
      { label: "Use grep (not recommended)", description: "Traditional search - loses call chain tracing" },
      { label: "Cancel", description: "Stop investigation" }
    ]
  }]
})
```

**See ultrathink-detective skill for complete Fallback Protocol documentation.**

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| `grep "error"` | No call relationships | `claudemem --nologo context func --raw` |
| Read random files | No direction | Trace callers/callees systematically |
| Fix symptom only | Bug returns | Trace to root cause with `callers` |
| Skip impact check | Miss related bugs | ALWAYS check all `callers` |

## Debugging Tips

1. **Start at symptom** - Use `symbol` to find where error appears
2. **Get full context** - Use `context` for callers + callees together
3. **Trace backwards** - Follow `callers` chain to root cause
4. **Verify forward** - Use `callees` to confirm the path
5. **Check impact** - All `callers` of buggy code may be affected

## Notes

- **`context` is your primary tool** - Shows full call chain
- **Trace backwards with `callers`** - Find root cause, not just symptom
- **Verify with `callees`** - Confirm the execution path
- **Check all callers after fixing** - Don't leave other bugs
- Works best with TypeScript, Go, Python, Rust codebases

---

**Maintained by:** MadAppGang
**Plugin:** code-analysis v2.7.0
**Last Updated:** December 2025 (v3.3.0 - Cross-platform compatibility, inline templates, improved validation)
