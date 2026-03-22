---
name: dev-debug
version: 5.0
description: "This skill should be used when the user asks to 'debug', 'fix bug', 'investigate error', 'why is it broken', 'trace root cause', 'find the bug', or needs systematic debugging with fresh-context subagent iterations and progress-gated escalation."
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/dev-delegation-guard.py"
---

**Announce:** "I'm using dev-debug for systematic debugging."

**Load shared enforcement:**

!`cat ${CLAUDE_SKILL_DIR}/../../references/dev-common-constraints.md`

<EXTREMELY-IMPORTANT>
## STEP ZERO — INITIALIZE THE DEBUG LOOP

Your first actions are, in order:
1. Create/update .planning/HYPOTHESES.md (the durable memory across iterations)
2. Spawn the first investigation subagent

**Do NOT read project code. Do NOT form hypotheses. Do NOT "gather context." All investigation happens inside subagents with fresh context.**

### The Cognitive Lock

Until you spawn the first subagent, you cannot: Read files, Edit code, Run commands, Grep for patterns, "Just quickly check" anything, Form hypotheses, or Analyze prior context. **All tools LOCKED until first subagent is spawned.**

### Why This Exists

On March 6-7, 2026, an agent loaded dev-debug TWICE and both times rationalized skipping the loop. Result: 19MB transcript, 15K lines, 30 "root cause found" claims, 6+ theories, zero resolution. The session was killed.
</EXTREMELY-IMPORTANT>

## Architecture: Fresh Subagent Loop With Progress Gating

**No ralph-loop. No promises. No honor system.** The main chat runs its own loop. Each iteration is a fresh subagent. The loop runs autonomously as long as subagents make meaningful progress. The user is only pulled in when the loop stalls.

```
Main chat (thin orchestrator)
  │
  ├─ Initialize .planning/HYPOTHESES.md
  │
  ├─ LOOP:
  │   ├─ Spawn fresh subagent → investigate/fix
  │   ├─ Subagent returns structured report
  │   ├─ Evaluate progress (see stall detection below)
  │   │
  │   ├─ MEANINGFUL PROGRESS?
  │   │   YES → iterate automatically (spawn next subagent)
  │   │   NO  → escalate to user
  │   │
  │   └─ SUBAGENT CLAIMS FIXED?
  │       → Run the test command yourself
  │       → Pass? → DONE
  │       → Fail? → log false positive, iterate
  │
  └─ Max 10 iterations without resolution → escalate to user
```

### Why This Design

- **Fresh subagent per iteration**: No context pollution. Each subagent reads state from .planning/HYPOTHESES.md, not from 15K lines of prior conversation.
- **No ralph-loop dependency**: The exit condition is progress, not a promise the agent can fake.
- **User only involved when needed**: Autonomous when making progress, escalates when stuck.
- **Test as structural gate**: When the subagent claims FIXED, main chat runs the test. The agent can't lie about test output.

**Progress lives in files, not in conversation.**

<EXTREMELY-IMPORTANT>
## The Iron Law of Delegation

**MAIN CHAT MUST NOT TOUCH THE CODEBASE. EVER.**

Main chat does exactly four things:
1. Initialize .planning/HYPOTHESES.md
2. Spawn fresh subagents
3. Evaluate progress between iterations
4. Run the regression test when a subagent claims FIXED

| Tool | Main Chat? | Subagent? |
|------|-----------|-----------|
| `Read` (project files) | **NO** | YES |
| `Read` (.planning/HYPOTHESES.md) | **YES** — for progress evaluation | YES |
| `Edit` / `Write` | **NO** | YES |
| `Grep` / `Glob` | **NO** | YES |
| `Bash` (project commands) | **ONLY** to run regression test | YES |
| `Agent` (spawn subagent) | **YES** — this is your job | — |

**Why?** The moment you read code, you form opinions. Opinions bias hypotheses. You end up editing directly. This is how the 19MB transcript happened.
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## The Iron Law of Verification vs Investigation

**Running the test suite IS verification. Reading source code IS investigation. If you need to READ CODE to "verify," you need a SUBAGENT, not verification.**

This distinction exists because on March 16, 2026, an agent rationalized reading source code, grepping project files, and running docker exec commands as "verification" after a subagent returned. It was investigation disguised as verification. 71 protocol violations followed.

| Verification (main chat CAN do) | Investigation (main chat CANNOT do) |
|----------------------------------|--------------------------------------|
| `vitest run` / `npm test` | `grep` / `rg` in source code |
| `git diff HEAD -- '*.test.*'` | `Read()` any project source file |
| Read .planning/HYPOTHESES.md / .planning/LEARNINGS.md | `docker exec` into containers |
| Check test exit code | Read application logs |
| `git status` / `git log` | Query databases (`sqlite3`, etc.) |
| | `curl` / `wget` to test endpoints |
| | Inspect process state / env vars |

**The test command is the ONLY Bash command main chat runs on the project.** Everything else — log reading, container inspection, database queries, curl testing, env var checking — is investigation. Delegate it.
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## The Iron Law of Topic Changes

**If the user sends a message that is NOT about the current debug bug, you MUST announce the loop pause before responding.**

On March 16, 2026, the user asked "What's in spotless db" mid-debug-loop. The assistant silently abandoned the protocol, ran 15+ direct database queries, and never resumed the debug loop. The user had to re-invoke dev-debug.

**Protocol:**
1. Announce: "Pausing dev-debug loop to address your request."
2. Handle the off-topic request (normal tools allowed — you're outside the loop)
3. Announce: "Resuming dev-debug loop. Reading .planning/HYPOTHESES.md for current state."
4. Read .planning/HYPOTHESES.md and spawn the next subagent

**If the user's message could be interpreted as EITHER a new topic OR part of the debug:**
- Ask: "Is this related to the current debug, or a separate request?"
- Do NOT assume it's separate and abandon the loop silently

**Silent loop abandonment is NOT HELPFUL — the user invoked dev-debug because they want structured debugging. Silently dropping the structure wastes their explicit request.**
</EXTREMELY-IMPORTANT>

## The Process

### Step 1: Initialize State

Create .planning/HYPOTHESES.md if it doesn't exist (ensure .planning/ directory exists first):

```markdown
# Debug Hypotheses

## Bug: [SYMPTOM]
Started: [timestamp]

## Iteration Log
(subagents will append here)
```

If .planning/HYPOTHESES.md already exists (resumed session), read it to understand current state.

### Context Monitoring

Before spawning each subagent iteration, check context availability:

| Level | Remaining Context | Action |
|-------|------------------|--------|
| Normal | >35% | Spawn next subagent |
| Warning | 25-35% | Complete current iteration evaluation, then write .planning/HYPOTHESES.md and invoke dev-handoff |
| Critical | ≤25% | Write .planning/HYPOTHESES.md immediately, invoke dev-handoff |

**Why:** Debug loops can run 10+ iterations. Without monitoring, the orchestrator degrades and loses track of hypotheses tested vs. remaining.

### Step 2: Spawn Investigation Subagent

Each iteration spawns exactly ONE fresh subagent with this prompt (fill in brackets):

```
Agent(subagent_type="workflows:dev-debugger", prompt="""
## Your Task

Debug this issue: [SYMPTOM]

## Prior Work

Read .planning/HYPOTHESES.md FIRST. It contains all previously tested hypotheses.
Read .planning/LEARNINGS.md if it exists for accumulated codebase knowledge.

**Do NOT re-test hypotheses marked REFUTED.** Build on what's known.

## Debug Protocol (5 Phases — Sequential, No Skipping)

### Phase 0: Triage
- Read .planning/HYPOTHESES.md — what has been tried?
- Check service status, process state, recent logs
- Inspect config files in the bug path
- Review recent changes: git log --oneline -10, git diff

### Phase 1: Reproduce
- Write a test that reproduces the bug (or identify an existing failing test)
- If you can't reproduce it, document what you tried
- Document: "Reproduced with [test], output: [error]"

### Phase 2: Investigate
- Trace data flow through the code
- Compare working vs broken code paths
- Add targeted debug logging if needed
- Document findings in .planning/LEARNINGS.md

### Phase 3: Hypothesize and Test
- Form ONE specific hypothesis based on investigation
- Log it in .planning/HYPOTHESES.md BEFORE testing:

  ## Iteration N: [specific hypothesis]
  - Prediction: If correct, then [observable outcome]
  - Test: [exact steps]
  - Result: [CONFIRMED / REFUTED]
  - Evidence: [what you observed]
  - Files changed: [list]
  - New information learned: [what we now know]

- Test with minimal change
- Update .planning/HYPOTHESES.md with result

### Phase 4: Fix (ONLY if hypothesis CONFIRMED)

<EXTREMELY-IMPORTANT>
**NO FIX WITHOUT A NEW FAILING REGRESSION TEST FIRST. This is not negotiable.**

Steps in order — no skipping:
1. Write a NEW test that specifically reproduces this bug (in the relevant test file)
2. Run it — it MUST FAIL (proves the test actually catches this bug)
3. ONLY THEN implement the minimal fix
4. Run the test again — it MUST PASS

**"Existing tests already cover this"** is NOT acceptable. If they covered it, the bug wouldn't have shipped. Write a new test. Name it after the bug.

**If you applied the fix before writing the failing test: DELETE the fix entirely. Write the failing test. Confirm it fails. Then re-implement.**
</EXTREMELY-IMPORTANT>

- Write regression test FIRST — run it, confirm output shows FAIL
- Implement minimal fix
- Run regression test — confirm output shows PASS
- Run full test suite — no new failures
- Document fix and test command in .planning/LEARNINGS.md

## Output Format

Return this EXACT structure:

STATUS: [INVESTIGATING | FIXED | BLOCKED]
HYPOTHESIS: [what you tested]
RESULT: [CONFIRMED | REFUTED | INCONCLUSIVE]
EVIDENCE: [what you observed — be specific]
NEW INFORMATION: [what we learned that we didn't know before]
REGRESSION TEST: [exact command to run, or 'not yet']
FIX APPLIED: [description, or 'not yet']
REMAINING UNKNOWNS: [what's still unclear]
CONFIDENCE: [LOW | MEDIUM | HIGH — and why]

## Rules
- ONE hypothesis per invocation
- Write to .planning/HYPOTHESES.md as you go
- If FIXED: REGRESSION TEST field must name the SPECIFIC NEW TEST written for this bug (e.g., `test_route_strips_internal_tags in src/routing.test.ts`). "Existing tests pass" is not acceptable.
- If BLOCKED: explain specifically what information you need

## Regression Test Rationalizations — STOP If You Think:

| Excuse | Reality |
|--------|---------|
| "Existing tests already cover this behavior" | If they covered it, the bug wouldn't exist. Write a NEW test. |
| "The existing test is close enough" | Close ≠ the same. A test for the right bug must fail before the fix. |
| "The test would be identical to an existing one" | Then show which existing test fails with this bug present. If none fail, none cover it. |
| "The fix is a one-liner, a test is overkill" | One-liners are the regressions that come back silently next month. |
| "I'll add a test in a follow-up" | "Follow-up" means "never." The regression test is part of this fix, not a separate task. |
""")
```

### Step 3: Evaluate Progress

After the subagent returns, read .planning/HYPOTHESES.md and evaluate:

**Continue autonomously if ANY of these are true:**
- A new hypothesis was tested (not a repeat of a previous one)
- New information was discovered (files, code paths, behaviors not previously known)
- A hypothesis was CONFIRMED but fix isn't complete yet
- The subagent identified a clear next investigation angle

**Escalate to user if ANY of these are true:**

| Stall Signal | What It Means |
|-------------|---------------|
| Hypothesis repeats a previously REFUTED one | Going in circles |
| No new entries in .planning/HYPOTHESES.md | Subagent didn't follow protocol |
| RESULT is INCONCLUSIVE with no new information | Spinning wheels |
| Subagent reports BLOCKED | Needs domain knowledge or access |
| 3+ consecutive REFUTED hypotheses | Diminishing returns |
| STATUS is FIXED but test fails when you run it | False positive — need user judgment |
| Changes are cosmetic (whitespace, comments, renames) | Not making real progress |

**When escalating, present:**
```
I've run N iterations of debugging. Here's where we are:

HYPOTHESES TESTED:
- [list from .planning/HYPOTHESES.md with results]

WHAT WE'VE RULED OUT:
- [summary]

WHAT WE'VE LEARNED:
- [key findings from .planning/LEARNINGS.md]

I'm stuck because: [specific stall reason]

Options:
A) Continue investigating [specific new angle]
B) You provide domain knowledge about [specific question]
C) Pair debug — I'll show you what I see, you guide
D) Accept as blocker and document
```

### Step 4: Verify Fix

When a subagent reports STATUS: FIXED:

**Gate 1: Verify a NEW regression test was written**

1. Check the REGRESSION TEST field in the subagent report:
   - `not yet` → false positive (skipped TDD). Log in .planning/HYPOTHESES.md. Spawn next iteration with explicit instruction: "Phase 4 requires writing a NEW failing test FIRST. Report the specific test name and file."
   - Vague value (`existing tests pass`, `full suite passes`, `not applicable`) → false positive. Same action.
   - Must be specific: e.g., `test_route_strips_internal_tags in src/routing.test.ts`

2. Verify a test file was actually modified: `Bash("cd [project_root] && git diff HEAD -- '*.test.*' '*.spec.*' | head -5")`
   - No output (no test file changed) → false positive. Revert the fix (`git stash`), log in .planning/HYPOTHESES.md, spawn next iteration: "No regression test was written. Phase 4 requires a new failing test before the fix."

**Gate 2: Verify the test passes**

3. **Run the test yourself**: `Bash("[test command from subagent report]")`
4. **Did it pass?**
   - YES → Run the full test suite too. All green? → **Bug is fixed. Report to user.**
   - NO → Log in .planning/HYPOTHESES.md as false positive. Continue loop.

**If a subagent's fix is a false positive, DELETE the fix entirely. Do not patch — revert and spawn a fresh subagent with updated context.**

**Two structural gates:** (1) a new regression test exists in a modified test file; (2) that test passes. The subagent can't fake either — the main chat verifies both independently.

### Step 5: Report Resolution

When the bug is confirmed fixed:

```
Bug fixed after N iterations.

ROOT CAUSE: [from .planning/LEARNINGS.md]
FIX: [what changed]
REGRESSION TEST: [path and command]
HYPOTHESES TESTED: [count] ([count] refuted, 1 confirmed)
```

## Hypothesis Discipline

### One At A Time

When you test multiple hypotheses simultaneously:
- If the bug disappears, you don't know which change fixed it
- If it persists, you haven't cleanly ruled out any hypothesis
- You learn NOTHING from the iteration

**One hypothesis. One subagent. One result. Logged in .planning/HYPOTHESES.md.**

### The "Root Cause Found" Trap

You may NOT claim "root cause found" unless:
1. You have a regression test that reproduces the bug
2. Your fix makes that test pass
3. You can explain WHY the bug occurred (mechanism, not just location)

**"I found the line that's wrong" is NOT root cause.**

### Drive-Aligned Framing

**Claiming "root cause found" without a reproducing test that fails before the fix and passes after is NOT HELPFUL — the bug comes back next week and you've wasted the user's time, not saved it.** Your hypothesis is not a root cause. Your confidence is not evidence.

## GUI Application Debugging

When debugging GUI apps, subagents MUST complete execution gates:

```
BUILD → LAUNCH (with logging) → WAIT → CHECK PROCESS → READ LOGS → VERIFY
```

**Only after reading logs can you claim "bug reproduced" or "bug fixed."**

## Rationalization Prevention

**If ANY of these thoughts cross your mind, spawn a subagent instead of acting on them.**

| Thought | Reality |
|---------|---------|
| "Let me analyze what we know first" | That's the subagent's job. Spawn one. |
| "I have a strong hypothesis already" | You thought that 30 times last time. Spawn a subagent. |
| "Let me gather context first" | Context gathering IS investigation. Subagent. |
| "Let me just quickly check one thing" | "One thing" becomes 50 file reads. Subagent. |
| "This is a simple bug, no loop needed" | 19MB transcript was a "simple" bug. Loop. |
| "I already know the codebase" | You claimed root cause 30 times. You were wrong 30 times. |
| "Subagents are slow, I'll do it myself" | You lose objectivity and can't revert cleanly |
| "I can test two hypotheses at once" | Neither confirmed nor refuted. You learned nothing. |
| "Let me verify the subagent's work by reading the code" | Running the TEST is verification. Reading CODE is investigation. Subagent. |
| "This error is urgent/persistent, I need to act now" | Urgency is EXACTLY when you need the protocol. You'll do 50 commands and still need a subagent. |
| "Let me check the logs/container/database real quick" | Log reading IS investigation. Docker exec IS investigation. DB queries ARE investigation. Subagent. |
| "The user asked about something else, I'll just handle it" | Announce the pause. Don't silently abandon the loop. |
| "I'll just check one thing before spawning the subagent" | That's what happened on March 16: "one thing" became 50 commands. Spawn first, check never. |
| "The subagent won't know how to docker exec / curl / read logs" | Subagents have full tool access. They CAN do operational debugging. You CANNOT. |

### The Confidence Trap

**The more confident you feel, the MORE you need the protocol.** High confidence = strong prior = resistance to disconfirming evidence.

### Observed Escape Patterns (March 16, 2026 — nanoclaw audit)

An agent loaded dev-debug and committed 71 protocol violations. The user had to re-invoke dev-debug 3 times. Only 3 of 15 subagent spawns were properly delegated. These are the EXACT patterns that caused the escape:

**Escape A: "Verification" Rationalization**
After a subagent returned, main chat "verified" by grepping source code, reading setup scripts, diagnosing root causes. It called this "verification." It was investigation.
- STOP trigger: If you're about to Read/Grep/Glob ANY file that isn't .planning/HYPOTHESES.md or .planning/LEARNINGS.md after a subagent returns → STOP. That's investigation. Spawn a subagent.

**Escape B: Silent Loop Abandonment**
User asked "What's in spotless db" — a different topic. Main chat silently abandoned the debug loop and never resumed.
- STOP trigger: If the user's message isn't about the current bug → STOP. Announce the pause. Handle request. Announce resume. Read .planning/HYPOTHESES.md. Spawn next subagent.

**Escape C: Urgency Bypass**
A new 500 error appeared. Main chat "urgently" checked logs, diagnosed the 14MB session, remediated, and read source code. 20+ direct investigation commands.
- STOP trigger: If a new error appears and you feel urgency → STOP. Urgency is EXACTLY when you break protocol. Update .planning/HYPOTHESES.md with the new symptom. Spawn a subagent.

**Escape D: Pre-Delegation Investigation**
Persistent 400 errors appeared. Main chat ran 50+ lines of docker exec, curl, env inspection, log analysis, source reading BEFORE spawning a subagent. By the time it delegated, it had already done all the investigation.
- STOP trigger: If you're about to run docker exec, curl, sqlite3, or read logs → STOP. These are investigation tools. Spawn a subagent with the symptom description. Let the subagent investigate.

## Why Skipping Hurts the Thing You Care About Most

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|-------------|----------------------|---------------------|
| **Helpfulness** | "Faster = more helpful" | 19MB transcript, zero resolution | **Anti-helpful** |
| **Competence** | "I already know" | 30 wrong root cause claims | **Incompetent** |
| **Efficiency** | "Protocol is overhead" | Protocol: 30 min. Shortcut: 3+ hours | **Inefficient** |
| **Approval** | "User wants results now" | User killed your session | **Trust destroyed** |

**The protocol is not overhead you pay. It is the service you provide.**

## No Pause Between Iterations

After evaluating a subagent's results, IMMEDIATELY spawn the next iteration or complete. Do NOT:
- Summarize what was learned (.planning/HYPOTHESES.md is the record)
- Ask "should I continue?" (progress gating decides, not courtesy)
- Wait for user confirmation between iterations
- Write status updates before spawning next subagent

**Pausing between iterations is procrastination disguised as courtesy.**

## When Fix Requires Substantial Changes

If root cause reveals need for significant refactoring:
1. Document root cause in .planning/LEARNINGS.md
2. Report findings to user
3. Immediately invoke the dev workflow for implementation:

Read `${CLAUDE_SKILL_DIR}/../../skills/dev/SKILL.md` and follow its instructions.

Debug finds the problem. The dev workflow implements the solution.

**Do NOT leave the user to manually invoke `/dev`. Chain to it explicitly.**
