---
name: debug-sessions
description: Persistent debugging with multi-session state, binary search support, and error pattern matching.
---

# Debug Sessions Skill

// Project Autopilot - Persistent Debug Sessions
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Purpose:** Enable multi-session debugging with state preservation, binary search debugging support, and error pattern library matching.

---

## Directory Structure

```
.autopilot/debug/
├── active-session.json      # Current debug session state
├── sessions/
│   ├── session-001.json     # Historical session
│   ├── session-002.json     # Historical session
│   └── session-003.json     # Historical session
└── patterns/
    └── error-patterns.json  # Known error patterns library
```

---

## Session State Structure

### active-session.json

```json
{
  "session_id": "debug-001",
  "created": "2026-01-29T10:00:00Z",
  "updated": "2026-01-29T12:30:00Z",
  "status": "active",
  "bug": {
    "title": "Login fails intermittently",
    "description": "Users report random login failures",
    "symptoms": [
      "401 errors returned",
      "Session token lost",
      "Works on retry"
    ],
    "frequency": "30% of attempts",
    "environment": "production",
    "error_message": "Invalid session token",
    "stack_trace": "at AuthService.validate (auth.ts:42)..."
  },
  "investigation": {
    "phase": "root_cause_analysis",
    "hypotheses": [
      {
        "id": "H1",
        "description": "Race condition in auth token refresh",
        "status": "testing",
        "evidence": [],
        "likelihood": "high"
      },
      {
        "id": "H2",
        "description": "Token expiry edge case",
        "status": "eliminated",
        "evidence": ["Tokens have 24h expiry, issue happens within minutes"],
        "likelihood": "low"
      },
      {
        "id": "H3",
        "description": "Database connection timeout",
        "status": "pending",
        "evidence": [],
        "likelihood": "medium"
      }
    ],
    "tests_run": [
      {
        "hypothesis": "H1",
        "test": "Add logging around token refresh",
        "result": "Confirmed: overlapping refresh calls",
        "timestamp": "2026-01-29T11:00:00Z"
      },
      {
        "hypothesis": "H2",
        "test": "Check token timestamps",
        "result": "No correlation with expiry",
        "timestamp": "2026-01-29T11:30:00Z"
      }
    ],
    "binary_search": null
  },
  "findings": [
    {
      "id": "F1",
      "description": "Token refresh has no mutex",
      "location": "src/services/auth.ts:42",
      "severity": "high",
      "timestamp": "2026-01-29T11:00:00Z"
    }
  ],
  "fix_attempts": [
    {
      "id": "FIX1",
      "description": "Add mutex to token refresh",
      "status": "testing",
      "commit": "abc123",
      "timestamp": "2026-01-29T12:00:00Z"
    }
  ],
  "resolution": null
}
```

---

## Binary Search Debugging

### When to Use

Use binary search debugging when:
- Bug exists now but worked before
- Can identify a known-good commit
- Bug is deterministically reproducible
- Commit history is linear enough to search

### Binary Search State

```json
{
  "binary_search": {
    "active": true,
    "known_good": "abc123",
    "known_good_date": "2026-01-15",
    "known_bad": "def456",
    "known_bad_date": "2026-01-29",
    "current_test": "ghi789",
    "current_test_date": "2026-01-22",
    "range_commits": 12,
    "iterations": 2,
    "max_iterations": 4,
    "history": [
      {
        "commit": "xyz000",
        "result": "good",
        "timestamp": "2026-01-29T10:00:00Z"
      },
      {
        "commit": "ghi789",
        "result": "pending",
        "timestamp": "2026-01-29T10:30:00Z"
      }
    ]
  }
}
```

### Binary Search Protocol

```
FUNCTION binarySearchDebug(known_good, known_bad):
    """
    Start or continue binary search debugging.
    """
    state = loadActiveSession()

    IF NOT state.investigation.binary_search:
        # Initialize binary search
        commits = getCommitsBetween(known_good, known_bad)

        state.investigation.binary_search = {
            active: true,
            known_good: known_good,
            known_bad: known_bad,
            range_commits: commits.length,
            iterations: 0,
            max_iterations: Math.ceil(log2(commits.length)),
            history: []
        }

    bs = state.investigation.binary_search

    # Calculate midpoint
    commits = getCommitsBetween(bs.known_good, bs.known_bad)
    mid_index = Math.floor(commits.length / 2)
    mid_commit = commits[mid_index]

    bs.current_test = mid_commit.hash
    bs.current_test_date = mid_commit.date
    bs.iterations += 1

    saveActiveSession(state)

    LOG "🔍 Binary Search Debug"
    LOG "Remaining range: {commits.length} commits"
    LOG "Testing commit: {mid_commit.hash} ({mid_commit.date})"
    LOG "Iteration: {bs.iterations}/{bs.max_iterations}"
    LOG ""
    LOG "Run your test and report: /autopilot:debug --result good|bad"

    RETURN mid_commit

FUNCTION reportBinarySearchResult(result):
    """
    Report result of testing a commit.
    """
    state = loadActiveSession()
    bs = state.investigation.binary_search

    # Record result
    bs.history.add({
        commit: bs.current_test,
        result: result,
        timestamp: now()
    })

    # Update range
    IF result == "good":
        bs.known_good = bs.current_test
    ELSE IF result == "bad":
        bs.known_bad = bs.current_test

    # Check if found
    commits = getCommitsBetween(bs.known_good, bs.known_bad)

    IF commits.length <= 1:
        # Found the breaking commit
        breaking_commit = bs.known_bad

        LOG "🎯 Found breaking commit!"
        LOG "Commit: {breaking_commit}"
        LOG "Author: {getCommitAuthor(breaking_commit)}"
        LOG "Message: {getCommitMessage(breaking_commit)}"
        LOG ""
        LOG "Changes in this commit:"
        displayCommitChanges(breaking_commit)

        state.findings.add({
            id: "F-BS",
            description: "Breaking commit identified via binary search",
            location: breaking_commit,
            severity: "high"
        })

        bs.active = false
        saveActiveSession(state)

        RETURN breaking_commit
    ELSE:
        # Continue search
        saveActiveSession(state)
        RETURN binarySearchDebug(bs.known_good, bs.known_bad)
```

---

## Error Pattern Library

### patterns/error-patterns.json

```json
{
  "patterns": [
    {
      "id": "ERR001",
      "name": "Null Reference",
      "pattern": "Cannot read propert(y|ies) .* of (null|undefined)",
      "category": "null_reference",
      "common_causes": [
        "Missing null check before property access",
        "Async timing issue - accessing before data loaded",
        "Incorrect data shape from API response",
        "State not initialized before render"
      ],
      "debug_steps": [
        "1. Find where the variable is assigned",
        "2. Trace all paths to the error point",
        "3. Identify which path doesn't set the value",
        "4. Add null check or fix assignment"
      ],
      "example_fix": "Add optional chaining: obj?.property"
    },
    {
      "id": "ERR002",
      "name": "Type Error",
      "pattern": "TypeError: .* is not a function",
      "category": "type_error",
      "common_causes": [
        "Calling method on wrong type",
        "Import/export mismatch",
        "Variable shadowing",
        "Async function not awaited"
      ],
      "debug_steps": [
        "1. Check the type of the variable at runtime",
        "2. Verify imports are correct",
        "3. Check for variable shadowing",
        "4. Ensure async functions are awaited"
      ],
      "example_fix": "Verify import: import { fn } from './module'"
    },
    {
      "id": "ERR003",
      "name": "Race Condition",
      "pattern": "intermittent|sometimes|works on retry|random failure",
      "category": "race_condition",
      "common_causes": [
        "Missing await on async operation",
        "Shared mutable state accessed concurrently",
        "Event ordering assumptions violated",
        "Cache invalidation timing"
      ],
      "debug_steps": [
        "1. Add logging with timestamps",
        "2. Look for async operations without await",
        "3. Check for shared state mutations",
        "4. Test with artificial delays"
      ],
      "example_fix": "Add mutex or use atomic operations"
    },
    {
      "id": "ERR004",
      "name": "Memory Leak",
      "pattern": "memory|heap|OOM|out of memory|growing",
      "category": "memory_leak",
      "common_causes": [
        "Event listeners not removed on cleanup",
        "Closures holding references to large objects",
        "Cache without eviction policy",
        "Circular references preventing GC"
      ],
      "debug_steps": [
        "1. Take heap snapshots over time",
        "2. Compare retained objects",
        "3. Find growing patterns",
        "4. Trace reference chains"
      ],
      "example_fix": "Add cleanup: useEffect cleanup or removeEventListener"
    },
    {
      "id": "ERR005",
      "name": "Connection Error",
      "pattern": "ECONNREFUSED|connection refused|timeout|ETIMEDOUT",
      "category": "connection",
      "common_causes": [
        "Service not running",
        "Firewall blocking connection",
        "Wrong port or host",
        "Network issues"
      ],
      "debug_steps": [
        "1. Verify service is running",
        "2. Check connection string",
        "3. Test connectivity (ping, telnet)",
        "4. Check firewall rules"
      ],
      "example_fix": "Verify DATABASE_URL environment variable"
    }
  ]
}
```

### Pattern Matching Function

```
FUNCTION matchErrorPattern(error_message, stack_trace):
    """
    Match error against known patterns.
    """
    patterns = loadErrorPatterns()
    matches = []

    FOR each pattern IN patterns:
        IF regexMatch(error_message, pattern.pattern) OR
           regexMatch(stack_trace, pattern.pattern):
            matches.add({
                pattern: pattern,
                confidence: calculateConfidence(error_message, pattern)
            })

    # Sort by confidence
    matches.sort(by: confidence, descending: true)

    IF matches.length > 0:
        best = matches[0]
        LOG "🔍 Error Pattern Matched: {best.pattern.name}"
        LOG "Confidence: {best.confidence}%"
        LOG ""
        LOG "Common causes:"
        FOR each cause IN best.pattern.common_causes:
            LOG "  • {cause}"
        LOG ""
        LOG "Debug steps:"
        FOR each step IN best.pattern.debug_steps:
            LOG "  {step}"

        RETURN best

    RETURN null
```

---

## Session Management

### Start New Session

```
FUNCTION startDebugSession(bug_description):
    """
    Start a new debug session.
    """
    session_id = "debug-" + generateId()

    session = {
        session_id: session_id,
        created: now(),
        updated: now(),
        status: "active",
        bug: {
            title: extractTitle(bug_description),
            description: bug_description,
            symptoms: [],
            frequency: "unknown",
            environment: detectEnvironment()
        },
        investigation: {
            phase: "information_gathering",
            hypotheses: [],
            tests_run: [],
            binary_search: null
        },
        findings: [],
        fix_attempts: [],
        resolution: null
    }

    # Check for pattern match
    pattern_match = matchErrorPattern(bug_description, "")
    IF pattern_match:
        session.investigation.pattern_match = pattern_match

    saveActiveSession(session)

    LOG "🐛 Debug Session Started: {session_id}"
    RETURN session
```

### Resume Session

```
FUNCTION resumeDebugSession():
    """
    Resume an active debug session.
    """
    session = loadActiveSession()

    IF NOT session:
        ERROR "No active debug session. Start one with /autopilot:debug --new"

    LOG "🐛 Resuming Debug Session: {session.session_id}"
    LOG "Bug: {session.bug.title}"
    LOG "Phase: {session.investigation.phase}"
    LOG "Hypotheses: {session.investigation.hypotheses.length}"
    LOG "Tests run: {session.investigation.tests_run.length}"
    LOG "Findings: {session.findings.length}"

    IF session.investigation.binary_search?.active:
        LOG ""
        LOG "Binary search in progress:"
        LOG "  Testing: {session.investigation.binary_search.current_test}"
        LOG "  Range: {session.investigation.binary_search.range_commits} commits"

    RETURN session
```

### Close Session

```
FUNCTION closeDebugSession(resolution):
    """
    Close a debug session with resolution.
    """
    session = loadActiveSession()

    session.status = "resolved"
    session.resolution = {
        description: resolution.description,
        fix_commit: resolution.commit,
        root_cause: resolution.root_cause,
        prevention: resolution.prevention,
        resolved_at: now()
    }

    # Archive session
    archivePath = ".autopilot/debug/sessions/{session.session_id}.json"
    writeJSON(archivePath, session)

    # Clear active session
    deleteFile(".autopilot/debug/active-session.json")

    LOG "✅ Debug Session Closed: {session.session_id}"
    LOG "Resolution: {resolution.description}"

    RETURN session
```

---

## Integration Points

### With /autopilot:debug Command

```
debug.md uses:
    - startDebugSession(description)
    - resumeDebugSession()
    - binarySearchDebug(good, bad)
    - matchErrorPattern(error)
    - closeDebugSession(resolution)
```

### With debugger Agent

```
debugger.md reads:
    - Active session state
    - Pattern library
    - Previous findings
    - Binary search state
```

### With /autopilot:cockpit

```
resume.md checks:
    - Active debug session exists
    - Offers to resume debugging
    - Restores debug context
```

---

## Session Persistence

### Save Points

Sessions are automatically saved:
- When new hypothesis added
- When test completed
- When finding recorded
- When binary search state changes
- Every 5 minutes during active debugging

### Recovery

If session interrupted:
1. Load `.autopilot/debug/active-session.json`
2. Display current state
3. Continue from last checkpoint
4. No work lost

---

## Output Formats

### Session Summary

```
🐛 Debug Session: debug-001

Bug: Login fails intermittently
Status: Active
Phase: Root Cause Analysis

Hypotheses:
  [H1] ⏳ Race condition in auth token refresh (HIGH)
  [H2] ❌ Token expiry edge case (ELIMINATED)
  [H3] ⏳ Database connection timeout (MEDIUM)

Tests Run: 2
Findings: 1
Fix Attempts: 1

Binary Search: Not active
```

### Binary Search Progress

```
🔍 Binary Search Debug

Known Good: abc123 (2026-01-15)
Known Bad:  def456 (2026-01-29)
Range:      12 commits
Iteration:  2/4

Currently Testing: ghi789 (2026-01-22)

Report result: /autopilot:debug --result good|bad
```
