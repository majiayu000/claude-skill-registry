---
name: retrospective
description: |
  After completing a significant task or experiment, documents what worked,
  what failed, and key learnings. Activates when a multi-step task finishes
  or when user says "done", "finished", "that worked", or asks for a summary.
  Failed attempts get documented first - they're read more than successes.
allowed-tools: |
  file: read, write
---

# Retrospective

<purpose>
Knowledge capture at task completion. The Sionic AI insight: "Failed Attempts"
tables get read more than any other documentation section. Success paths are
nice. Failure paths save real time. This skill ensures both get documented
before context is lost.
</purpose>

## When To Activate

<triggers>
After completing significant work:

- Multi-step implementations (3+ distinct phases)
- Debugging sessions that found the root cause
- Experiments or spikes that reached a conclusion
- Tasks where you tried multiple approaches

User signals completion:
- "That worked"
- "Done" / "Finished" / "Ship it"
- "Can you summarize what we did?"
- Explicit request for retrospective
</triggers>

## Instructions

### Step 1: Capture Failed Attempts First

Document what DIDN'T work before it fades from memory:

```markdown
## Failed Attempts

| Approach | Why It Failed | Time Spent |
|----------|---------------|------------|
| [First thing tried] | [Specific reason] | [Estimate] |
| [Second thing tried] | [Specific reason] | [Estimate] |
```

Be specific about WHY it failed. "Didn't work" is useless. "Race condition
between auth callback and state update" is useful.

### Step 2: Document The Working Solution

```markdown
## What Worked

**Final approach:** [One sentence summary]

**Key insight:** [The "aha" moment that unlocked the solution]

**Implementation:**
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

### Step 3: Extract Learnings

```markdown
## Learnings

**Would do differently:**
- [What you'd change next time]

**Surprised by:**
- [Unexpected discoveries]

**Reusable patterns:**
- [Anything worth extracting into a skill or snippet]
```

### Step 4: Create Artifact (Optional)

If the learnings are significant, offer to create:

- A skill (if pattern will recur) → invoke `learn-from-this`
- A snippet (if code is reusable)
- A doc (if context is project-specific)

## Output Format

```markdown
# Retrospective: [Task Name]

## Failed Attempts

| Approach | Why It Failed | Time Spent |
|----------|---------------|------------|
| ... | ... | ... |

## What Worked

**Final approach:** ...

**Key insight:** ...

**Implementation:**
1. ...

## Learnings

**Would do differently:**
- ...

**Surprised by:**
- ...

**Reusable patterns:**
- ...

---
*Generated: [timestamp]*
```

## Examples

### Example: Debugging Session

```markdown
# Retrospective: Fix Login Race Condition

## Failed Attempts

| Approach | Why It Failed | Time Spent |
|----------|---------------|------------|
| Added setTimeout delay | Worked locally, flaky in prod | 20 min |
| Moved auth check earlier | Still raced with state hydration | 15 min |
| Added loading state | Masked the bug, didn't fix it | 10 min |

## What Worked

**Final approach:** Used auth state machine with explicit "initializing" state

**Key insight:** The bug wasn't timing - it was a missing state. Auth had
three states (logged-in, logged-out, unknown) but code only handled two.

**Implementation:**
1. Added AuthState enum with INITIALIZING state
2. Protected routes check for INITIALIZING, show skeleton
3. Auth callback sets state atomically after validation

## Learnings

**Would do differently:**
- Check for missing states FIRST before adding timing hacks

**Surprised by:**
- The "loading" state we added was actually correct, just incomplete

**Reusable patterns:**
- State machines for auth (avoid boolean flags)
```

### Example: Feature Implementation

```markdown
# Retrospective: Add CSV Export

## Failed Attempts

| Approach | Why It Failed | Time Spent |
|----------|---------------|------------|
| Client-side blob generation | Crashed on 10k+ rows | 30 min |
| Streaming response | CORS issues with download | 20 min |

## What Worked

**Final approach:** Server generates CSV, returns signed URL, client redirects

**Key insight:** Don't fight the browser. Redirecting to a file URL is the
native download UX.

**Implementation:**
1. POST /api/export triggers server-side generation
2. CSV written to temp storage with 5-min expiry
3. Return signed URL
4. Client does window.location = url

## Learnings

**Would do differently:**
- Start with server-side for any "export" feature

**Surprised by:**
- Signed URLs are trivial with modern cloud storage

**Reusable patterns:**
- Export pattern: generate server-side, return URL, redirect
```

## NEVER

- Skip the Failed Attempts section (it's the most valuable part)
- Write vague failure reasons ("didn't work", "broken", "issues")
- Document only successes (survivorship bias)
- Wait until the next session (context will be lost)

## ALWAYS

- Document failures FIRST while memory is fresh
- Include time estimates (helps calibrate future estimates)
- Extract the key insight (the "aha" moment)
- Offer to create skills from significant patterns
- Be honest about what took longer than expected
