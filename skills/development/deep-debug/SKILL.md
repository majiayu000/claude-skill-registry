---
name: deep-debug
description: |
  Multi-agent investigation for stubborn bugs. Use when: going in circles debugging, need to investigate browser/API interactions, complex bugs resisting normal debugging, or when symptoms don't match expectations. Launches parallel agents with different perspectives and uses Chrome tools for evidence gathering.
user-invocable: true
---

# Deep Debug - Multi-Agent Investigation

**Status**: Production Ready
**Last Updated**: 2026-02-02
**Dependencies**: Chrome MCP tools (optional), debugger agent, code-reviewer agent

---

## When to Use

- **Going in circles** - You've tried multiple fixes but nothing works
- **Browser + API interaction bugs** - Need to see Network tab, console logs
- **Symptoms don't match expectations** - Something deeper is wrong
- **Complex state management bugs** - React hooks, closures, race conditions

## Quick Start

```
/deep-debug [description of the bug]
```

Or invoke naturally:
- "I'm stuck on this bug, can you do a deep investigation?"
- "This bug is resisting normal debugging"
- "I need you to really dig into this"

---

## The Process

### Phase 1: Gather Evidence (Before Hypothesizing)

**For browser-related bugs**, use Chrome MCP tools:

```typescript
// Get network requests (look for duplicates, failures, timing)
mcp__claude-in-chrome__read_network_requests

// Get console logs (errors, warnings, debug output)
mcp__claude-in-chrome__read_console_messages

// Get page state
mcp__claude-in-chrome__read_page
```

**For backend bugs**, gather:
- Error logs and stack traces
- Request/response payloads
- Database query logs
- Timing information

### Phase 2: Launch Parallel Investigation (3 Agents)

Launch these agents simultaneously with the gathered evidence:

#### Agent 1: Execution Tracer (debugger)
```
Task(subagent_type="debugger", prompt="""
EVIDENCE: [paste network/console evidence]

Trace the execution path that leads to this bug. Find:
1. Where the bug originates
2. What triggers it
3. The exact line/function causing the issue

Focus on TRACING, not guessing.
""")
```

#### Agent 2: Pattern Analyzer (code-reviewer)
```
Task(subagent_type="code-reviewer", prompt="""
EVIDENCE: [paste evidence]

Review the relevant code for common bug patterns:
- React useCallback/useMemo dependency issues
- Stale closures
- Race conditions
- State update ordering
- Missing error handling

Find patterns that EXPLAIN the evidence.
""")
```

#### Agent 3: Entry Point Mapper (Explore)
```
Task(subagent_type="Explore", prompt="""
EVIDENCE: [paste evidence]

Map all entry points that could trigger this behavior:
- All places [function] is called
- All event handlers involved
- All state updates that affect this

Find if something is being called MULTIPLE TIMES or from UNEXPECTED places.
""")
```

### Phase 3: Cross-Reference Findings

After agents complete, look for:

| Signal | Meaning |
|--------|---------|
| All 3 agree on root cause | High confidence - fix it |
| 2 agree, 1 different | Investigate the difference |
| All 3 different | Need more evidence |

### Phase 4: Verify Fix

After implementing the fix, re-gather the same evidence to confirm:
- Network tab shows expected behavior
- Console has no errors
- State updates correctly

---

## Real Example: Duplicate API Calls Bug

### Evidence Gathered
Network tab showed **2 fetch requests** for the same message.

### Parallel Investigation Results

| Agent | Finding |
|-------|---------|
| debugger | `state.messages` in useCallback deps causes callback recreation |
| code-reviewer | Same finding + explained React pattern causing it |
| Explore | Verified UI layer wasn't double-calling (ruled out) |

### Root Cause (Consensus)
`sendMessage` useCallback had `state.messages` in dependency array. Every state update recreated the callback, causing duplicate calls during React re-renders.

### Fix
Use `stateRef` to access current state without including in dependencies:
```typescript
const stateRef = useRef(state);
stateRef.current = state;

const sendMessage = useCallback(async (text) => {
  // Use stateRef.current instead of state
  const messages = stateRef.current.messages;
  // ...
}, [/* state.messages removed */]);
```

---

## Common Bug Patterns This Catches

### React Hook Issues
- `state` in useCallback dependencies causing recreation
- Missing dependencies causing stale closures
- useEffect running multiple times

### API/Network Issues
- Duplicate requests (visible in Network tab)
- Race conditions between requests
- CORS failures
- Timeout handling

### State Management Issues
- State updates not batching correctly
- Optimistic updates conflicting with server response
- Multiple sources of truth

---

## Chrome Tools Quick Reference

| Tool | Use For |
|------|---------|
| `read_network_requests` | See all fetch/XHR calls, duplicates, failures |
| `read_console_messages` | Errors, warnings, debug logs |
| `read_page` | Current DOM state |
| `javascript_tool` | Execute debug code in page context |

---

## Tips for Success

1. **Evidence first, hypotheses second** - Don't guess until you have concrete data
2. **Network tab is gold** - Most frontend bugs show symptoms there
3. **Parallel agents save time** - 3 perspectives at once vs sequential guessing
4. **Cross-reference findings** - Agreement = confidence
5. **Verify with same evidence** - Confirm fix with same tools that found bug
