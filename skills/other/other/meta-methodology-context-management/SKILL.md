---
name: meta-methodology-context-management
description: Long-term context management protocol - maintain project continuity across sessions through systematic documentation. Progress tracking, decision logging, insight preservation.
---

# Context Management Protocol

> **Quick Guide:** Maintain project continuity across sessions through systematic documentation. Read context files at session start, update during work, leave project ready for next session.

---

<critical_requirements>

## CRITICAL: Maintain Context Across Sessions

**(Read all .claude/ context files at session start)**

**(Update progress.md after each significant change)**

**(Log decisions with rationale in decisions.md)**

**(Document discoveries and gotchas in insights.md)**

**(Leave project in state where next session can start immediately)**

</critical_requirements>

---

<context_management>

## Long-Term Context Management Protocol

Maintain project continuity across sessions through systematic documentation.

**File Structure:**

```
.claude/
  progress.md       # Current state, what's done, what's next
  decisions.md      # Architectural decisions and rationale
  insights.md       # Lessons learned, gotchas discovered
  tests.json        # Structured test tracking (NEVER remove tests)
  patterns.md       # Codebase conventions being followed
```

**Your Responsibilities:**

### At Session Start

```xml
<session_start>
1. Call pwd to verify working directory
2. Read all context files in .claude/ directory:
   - progress.md: What's been accomplished, what's next
   - decisions.md: Past architectural choices and why
   - insights.md: Important learnings from previous sessions
   - tests.json: Test status (never modify test data)
3. Review git logs for recent changes
4. Understand current state from filesystem, not just chat history
</session_start>
```

### During Work

```xml
<during_work>
After each significant change or decision:

1. Update progress.md:
   - What you just accomplished
   - Current status of the task
   - Next steps to take
   - Any blockers or questions

2. Log decisions in decisions.md:
   - What choice was made
   - Why (rationale)
   - Alternatives considered
   - Implications for future work

3. Document insights in insights.md:
   - Gotchas discovered
   - Patterns that work well
   - Things to avoid
   - Non-obvious behaviors

Format:
## [Date] - [Brief Title]

**Decision/Insight:**
[What happened or what you learned]

**Context:**
[Why this matters]

**Impact:**
[What this means going forward]
</during_work>
```

### At Session End

```xml
<session_end>
Before finishing, ensure:

1. progress.md reflects current state accurately
2. All decisions are logged with rationale
3. Any discoveries are documented in insights.md
4. tests.json is updated (never remove test entries)
5. Git commits have descriptive messages

Leave the project in a state where the next session can start immediately without context loss.
</session_end>
```

</context_management>

---

<test_tracking>

### Test Tracking

```xml
<test_tracking>
tests.json format:
{
  "suites": [
    {
      "file": "user-profile.test.ts",
      "added": "2025-11-09",
      "purpose": "User profile editing",
      "status": "passing",
      "tests": [
        {"name": "validates email format", "status": "passing"},
        {"name": "handles network errors", "status": "passing"}
      ]
    }
  ]
}

NEVER delete entries from tests.json - only add or update status.
This preserves test history and prevents regression.
</test_tracking>
```

</test_tracking>

---

<context_overload_prevention>

### Context Overload Prevention

**CRITICAL:** Don't try to load everything into context at once.

**Instead:**

- Provide high-level summaries in progress.md
- Link to specific files for details
- Use git log for historical changes
- Request specific files as needed during work

**Example progress.md:**

```markdown
# Current Status

## Completed

- User profile editing UI (see ProfileEditor.tsx)
- Form validation (see validation.ts)
- Tests for happy path (see profile-editor.test.ts)

## In Progress

- Error handling for network failures
  - Next: Add retry logic following pattern in api-client.ts
  - Tests: Need to add network error scenarios

## Blocked

- Avatar upload feature
  - Reason: Waiting for S3 configuration from DevOps
  - Tracking: Issue #456

## Next Session

Start with: Implementing retry logic in ProfileEditor.tsx
Reference: api-client.ts lines 89-112 for the retry pattern
```

This approach lets you maintain continuity without context bloat.

</context_overload_prevention>

---

<fresh_start_approach>

## Fresh Start Approach

Start each session as if it's the first:

1. Read .claude/ context files to understand state
2. Use git log to see recent changes
3. Examine filesystem to discover what exists
4. Run integration tests to verify current behavior

This "fresh start" approach works better than trying to maintain long chat history.

**Give the RIGHT context, not MORE context.**

- For a React component task: Provide that component + immediate dependencies
- For a store update: Provide the store + related stores
- For API work: Provide the endpoint + client utilities

Don't dump the entire codebase - focus context on what's relevant for the specific task.

</fresh_start_approach>

---

<why_this_matters>

## Why This Matters

Without context files:

- Next session starts from scratch
- You repeat past mistakes
- Decisions are forgotten
- Progress is unclear

With context files:

- Continuity across sessions
- Build on past decisions
- Remember what works/doesn't
- Clear progress tracking

</why_this_matters>

---

<critical_reminders>

## CRITICAL REMINDERS

**(Read all .claude/ context files at session start)**

**(Update progress.md after each significant change)**

**(Log decisions with rationale - not just what, but why)**

**(Document discoveries and gotchas in insights.md)**

**(NEVER remove entries from tests.json - only add or update)**

**(Leave project ready for next session to start immediately)**

</critical_reminders>
