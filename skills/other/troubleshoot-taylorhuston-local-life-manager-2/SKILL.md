---
name: troubleshoot
description: "Systematic debugging with 5-step loop for issues in spaces/[project]/. Use when encountering bugs, test failures, or unexpected behavior."
model: claude-sonnet-4-20250514
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /troubleshoot

Systematic debugging using a 5-step loop: Research → Hypothesize → Implement → Test → Document.

## Usage

```bash
/troubleshoot yourbench "tests failing after auth changes"
/troubleshoot yourbench 001       # Debug in context of issue
/troubleshoot coordinatr          # General debugging session
```

## The 5-Step Loop

```
┌─────────────────────────────────────────────┐
│                                             │
│  1. Research → 2. Hypothesize → 3. Implement│
│       ↑                              ↓      │
│       │                              │      │
│       └──────── 5. Document ← 4. Test ──────│
│                     │                       │
│                     ↓                       │
│              (if not fixed, repeat)         │
│                                             │
└─────────────────────────────────────────────┘
```

## Step Details

### Step 1: Research

**Before guessing, understand:**

```bash
# Check existing research
Glob: resources/research/*.md
Glob: ideas/[project]/notes/research/*.md

# Search for similar issues in codebase
Grep: spaces/[project]/ for error message

# Check library docs via Context7
# WebSearch for error messages, known issues
```

Spawn research-specialist agent for:
- Unfamiliar error messages
- Library/framework behavior
- Best practices for the pattern

### Step 2: Hypothesize

**Form ONE hypothesis:**

```markdown
Hypothesis: Query fires before auth state is set

Evidence:
- isLoading is true when query executes
- Error occurs only on initial load
- Works after manual refresh

Debug Plan:
1. Add console.log before query
2. Check auth state timing
3. Verify order of operations
```

**Only one hypothesis at a time.** Multiple theories = confusion.

### Step 3: Implement

**Apply fix + add debugging:**

```typescript
// Add liberal debug logging
console.log('[Auth] State before query:', authState);
console.log('[Query] Executing with user:', user?.id);

// Implement the fix
if (!authState.isReady) {
  console.log('[Query] Waiting for auth...');
  return;
}
```

### Step 4: Test

**Validate the fix:**

```bash
cd spaces/[project]

# Run specific tests
npm test -- --grep "auth"

# Run full suite
npm test

# Manual verification if needed
npm run dev
```

**NEVER claim "fixed" without tests passing.**

### Step 5: Document

**Update WORKLOG with findings:**

```markdown
## YYYY-MM-DD - Troubleshooting Loop 1

**Hypothesis**: Query fires before auth state is set

**Debug findings**:
- isLoading was true when query executed
- Auth state not propagating to component
- Race condition between auth init and query

**Implementation**: Added auth state check before query

**Result**: ✓ Fixed - 47/47 tests passing

**Gotcha**: Auth state needs explicit ready check, not just truthy
```

### If Not Fixed

1. **Rollback changes**: `git checkout -- .`
2. **Document what you learned**
3. **Return to Step 1** with new information

## Execution Modes

### Mode 1: During TASK Implementation

```bash
/troubleshoot yourbench 001 "tests failing"
```

1. Read: TASK.md, PLAN.md, WORKLOG.md for context
2. Execute 5-step loop
3. Document in issue's WORKLOG.md
4. Continue with `/implement` when fixed

### Mode 2: Standalone Debugging

```bash
/troubleshoot yourbench "login broken on Safari"
```

1. Investigate without issue context
2. Document findings
3. Suggest creating BUG issue if significant

## Key Rules

1. **Research BEFORE guessing**
2. **ONE hypothesis at a time**
3. **Liberal debug logging** - `console.log('[Component] State:', data)`
4. **NEVER claim "fixed"** without tests passing
5. **Rollback on failure** before next attempt
6. **Document everything** for future reference

## Workflow

```
/implement → (issue occurs) → /troubleshoot → /worklog → /implement
```

**After fixing:**
- Add WORKLOG entry with findings
- Continue implementation
- Or create BUG issue if recurring problem
