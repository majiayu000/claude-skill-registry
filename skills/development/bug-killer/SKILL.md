---
name: bug-killer
description: >-
  Systematic, hypothesis-driven debugging workflow with triage-based track routing.
  Use when asked to "fix this bug", "debug this", "why is this failing",
  "this is broken", "investigate this error", "track down this issue",
  or any debugging situation. Supports --deep flag to force full investigation.
argument-hint: <bug-description-or-error> [--deep]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TaskCreate, TaskUpdate, TaskList, TaskGet, SendMessage
---

# Bug Killer — Hypothesis-Driven Debugging Workflow

Execute a systematic debugging workflow that enforces investigation before fixes. Every bug gets a hypothesis journal, evidence gathering, and root cause confirmation before any code changes.

**CRITICAL: Complete ALL 5 phases.** The workflow is not complete until Phase 5: Wrap-up & Report is finished. After completing each phase, immediately proceed to the next phase without waiting for user prompts.

## Phase Overview

1. **Triage & Reproduction** — Understand, reproduce, route to quick or deep track
2. **Investigation** — Gather evidence with language-specific techniques
3. **Root Cause Analysis** — Confirm root cause through hypothesis testing
4. **Fix & Verify** — Fix with proof, regression test, quality check
5. **Wrap-up & Report** — Document trail, capture learnings

---

## Phase 1: Triage & Reproduction

**Goal:** Understand the bug, reproduce it, and decide the investigation track.

### 1.1 Parse Context

Extract from `$ARGUMENTS` and conversation context:
- **Bug description**: What's failing? Error messages, symptoms
- **Reproduction steps**: How to trigger the bug (test command, user action, etc.)
- **Environment**: Language, framework, test runner, relevant config
- **Prior attempts**: Has the user already tried fixes? What didn't work?
- **Deep flag**: If `--deep` is present, skip triage and go directly to deep track (jump to Phase 2 deep track)

### 1.2 Reproduce the Bug

Attempt to reproduce before investigating:

1. If a failing test was mentioned, run it:
   ```bash
   # Run the specific test to confirm the failure
   <test-runner> <test-file>::<test-name>
   ```
2. If an error was described, find and trigger it
3. If neither, search for related test files and run them

**Capture the exact error output** — this is your primary evidence.

If the bug cannot be reproduced:
- Ask the user for more context via AskUserQuestion
- Check if it's environment-specific or intermittent
- Note "not yet reproduced" in the hypothesis journal

### 1.3 Form Initial Hypothesis

Based on the error message and context, form your first hypothesis:

```markdown
### H1: [Title]
- Hypothesis: [What you think is causing the bug]
- Evidence for: [What supports this — error message, stack trace, etc.]
- Evidence against: [Anything that contradicts it — if none yet, say "None yet"]
- Test plan: [Specific steps to confirm or reject]
- Status: Pending
```

### 1.4 Route to Track

**Quick-fix signals** (ALL must be true):
- Clear, specific error message pointing to exact location
- Localized to 1-2 files (not spread across the codebase)
- Obvious fix visible from reading the error location
- No concurrency, timing, or state management involved

**Deep-track signals** (ANY one triggers deep track):
- Bug spans 3+ files or modules
- Root cause unclear from the error message alone
- Intermittent or environment-dependent failure
- Involves concurrency, timing, shared state, or async behavior
- User already tried fixes that didn't work
- Generic error message (e.g., "null reference" without clear origin)
- Stack trace points to library/framework code rather than application code

**Present your assessment** via AskUserQuestion:
- Summarize the bug and your initial hypothesis
- Recommend quick or deep track with justification
- Options: "Quick track (Recommended)" / "Deep track" / "Deep track" / "Quick track" — depending on your assessment
- Let the user override your recommendation

**Track escalation rule:** If during quick track execution, 2 hypotheses are rejected, automatically escalate to deep track. Preserve all hypothesis journal entries when escalating.

---

## Phase 2: Investigation

**Goal:** Gather evidence systematically, guided by language-specific techniques.

### 2.1 Load Language Reference

Detect the primary language of the bug's context and load the appropriate reference:

| Language | Reference File |
|----------|---------------|
| Python | `Read ${CLAUDE_PLUGIN_ROOT}/skills/bug-killer/references/python-debugging.md` |
| TypeScript / JavaScript | `Read ${CLAUDE_PLUGIN_ROOT}/skills/bug-killer/references/typescript-debugging.md` |
| Other / Multiple | `Read ${CLAUDE_PLUGIN_ROOT}/skills/bug-killer/references/general-debugging.md` |

Always also load `general-debugging.md` as a supplement when using a language-specific reference.

### 2.2 Quick Track Investigation

For quick-track bugs, investigate directly:

1. **Read the error location** — the file and function where the error occurs
2. **Read the immediate callers** — 1-2 files up the call chain
3. **Check recent changes** — `git log --oneline -5 -- <file>` for the affected files
4. **Update hypothesis** — does the evidence support H1? Add evidence for/against

Proceed to Phase 3 (quick track).

### 2.3 Deep Track Investigation

For deep-track bugs, use parallel exploration agents:

1. **Plan exploration areas** — identify 2-3 focus areas based on the bug:
   - Focus 1: The error site and immediate code path
   - Focus 2: Data flow and state management leading to the error
   - Focus 3: Related subsystems, configuration, or external dependencies

2. **Launch code-explorer agents:**

   Spawn 2-3 code-explorer agents from core-tools:

   ```
   Use Task tool with subagent_type: "agent-alchemy-core-tools:code-explorer"

   Prompt for each agent:
   Bug context: [description of the bug and error]
   Focus area: [specific area for this agent]

   Investigate this focus area in relation to the bug:
   - Find all relevant files
   - Trace the execution/data path
   - Identify where behavior diverges from expected
   - Note any suspicious patterns, recent changes, or known issues
   - Report structured findings
   ```

   Launch agents in parallel for independent focus areas.

3. **Synthesize exploration results:**
   - Collect findings from all agents
   - Identify convergence (multiple agents pointing to same area)
   - Update hypothesis journal with new evidence
   - Form additional hypotheses if evidence warrants (aim for 2-3 total)

Proceed to Phase 3 (deep track).

---

## Phase 3: Root Cause Analysis

**Goal:** Confirm the root cause through systematic hypothesis testing.

### 3.1 Quick Track Root Cause

For quick-track bugs:

1. **Verify the hypothesis:**
   - Read the specific code identified in Phase 2
   - Trace the logic step-by-step
   - Confirm that the hypothesized cause produces the observed error

2. **If confirmed** (Status → Confirmed):
   - Update H1 with confirming evidence
   - Proceed to Phase 4

3. **If rejected** (Status → Rejected):
   - Update H1 with evidence against and reason for rejection
   - Form a new hypothesis (H2) based on what you learned
   - Investigate H2 following Phase 2 quick track steps
   - **If H2 is also rejected → escalate to deep track**
   - Preserve all journal entries, continue with Phase 2 deep track

### 3.2 Deep Track Root Cause

For deep-track bugs:

1. **Prepare hypotheses for testing:**
   - You should have 2-3 hypotheses from Phase 2
   - Each needs a concrete test plan (how to confirm or reject)

2. **Launch bug-investigator agents:**

   Spawn 1-3 bug-investigator agents to test hypotheses in parallel:

   ```
   Use Task tool with subagent_type: "bug-investigator"

   Prompt for each agent:
   Bug context: [description of the bug and error]

   Hypothesis to test: [specific hypothesis]
   Test plan:
   1. [Step 1 — e.g., run this specific test with these arguments]
   2. [Step 2 — e.g., check git blame for this function]
   3. [Step 3 — e.g., trace the data from input to error site]

   Report your findings with verdict (confirmed/rejected/inconclusive),
   evidence, and recommendations.
   ```

   Launch agents in parallel when they test independent hypotheses.

3. **Evaluate results:**
   - Update hypothesis journal with each agent's findings
   - If one hypothesis is confirmed → proceed to Phase 4
   - If all are rejected/inconclusive → apply 5 Whys technique:

     Take the strongest "inconclusive" finding and ask "why?" iteratively:
     ```
     Observed: [what actually happens]
     Why? → [first-level cause]
     Why? → [second-level cause]
     Why? → [root cause]
     ```
   - Form new hypotheses from 5 Whys analysis and repeat investigation

4. **If stuck after 2 rounds of investigation:**
   - Present all findings to the user via AskUserQuestion
   - Share the hypothesis journal
   - Ask for additional context or direction
   - Options: "Continue investigating", "Try a different angle", "Provide more context"

---

## Phase 4: Fix & Verify

**Goal:** Fix the root cause and prove the fix works.

### 4.1 Design the Fix

Before writing any code:

1. **Explain the root cause** — state clearly what's wrong and why
2. **Explain the fix** — describe what will change and WHY it addresses the root cause
3. **Identify affected files** — list every file that needs modification
4. **Consider side effects** — could this fix break other behavior?

### 4.2 Implement the Fix

1. **Read all files** that will be modified before making changes
2. **Apply the fix** using Edit tool — minimal, focused changes
3. **Match existing patterns** — follow the codebase's conventions

### 4.3 Run Tests

1. **Run the originally failing test** — it should now pass:
   ```bash
   <test-runner> <test-file>::<test-name>
   ```

2. **Run related tests** — tests in the same file and nearby test files:
   ```bash
   <test-runner> <test-directory>
   ```

3. If tests fail:
   - Determine if the failure is related to the fix or pre-existing
   - If related, revise the fix (do NOT revert to a different approach without updating the hypothesis journal)
   - If pre-existing, note it but don't let it block the fix

### 4.4 Write Regression Test

Write a test that would have caught this bug:

1. The test should fail WITHOUT the fix (verifying it tests the right thing)
2. The test should pass WITH the fix
3. The test should be minimal — test the specific behavior that was broken
4. Place it in the appropriate test file following project conventions

### 4.5 Deep Track: Quality Check and Related Issues

**Deep track only — skip on quick track.**

1. **Load code-quality skill:**
   ```
   Read ${CLAUDE_PLUGIN_ROOT}/skills/code-quality/SKILL.md
   ```
   Review the fix against code quality principles.

2. **Check for related issues:**
   - Search for the same pattern elsewhere in the codebase:
     ```
     Grep for the pattern that caused the bug
     ```
   - If the same bug exists in other locations, report them to the user
   - Ask via AskUserQuestion: "Fix all related instances now?" / "Fix only the reported bug" / "Create tasks for related fixes"

---

## Phase 5: Wrap-up & Report

**Goal:** Document the investigation trail and capture learnings.

### 5.1 Bug Fix Summary

Present to the user:

```markdown
## Bug Fix Summary

### Bug
[One-line description of the bug]

### Root Cause
[What was actually wrong and why]

### Fix Applied
[What was changed, with file:line references]

### Tests
- [Originally failing test]: Now passing
- [Regression test added]: [test name and location]
- [Related tests]: All passing

### Track
[Quick / Deep] [Escalated from quick: Yes/No]
```

### 5.2 Hypothesis Journal Recap

Present the complete hypothesis journal showing the investigation trail:

```markdown
### Investigation Trail

#### H1: [Title]
- Status: Confirmed / Rejected
- [Key evidence summary]

#### H2: [Title] (if applicable)
- Status: Confirmed / Rejected
- [Key evidence summary]

[... additional hypotheses ...]
```

### 5.3 Project Learnings

Load the `project-learnings` skill to evaluate whether this bug reveals project-specific knowledge worth capturing:

```
Read ${CLAUDE_PLUGIN_ROOT}/skills/project-learnings/SKILL.md
```

Follow its workflow to evaluate the finding. Common debugging discoveries that qualify:
- Surprising API behavior specific to this project
- Undocumented conventions that caused the bug
- Architectural constraints that aren't obvious from the code

### 5.4 Deep Track: Future Recommendations

**Deep track only:**

If the investigation revealed broader concerns, present recommendations:
- Architecture improvements to prevent similar bugs
- Missing test coverage areas
- Documentation gaps
- Monitoring or alerting suggestions

### 5.5 Next Steps

Offer the user options via AskUserQuestion:
- "Commit the fix" — proceed to commit workflow
- "Review the changes" — show a diff of all modifications
- "Run full test suite" — run the complete test suite to verify no regressions
- "Done" — wrap up the session

---

## Hypothesis Journal

The hypothesis journal is the core artifact of this workflow. Maintain it throughout all phases.

### Format

```markdown
## Hypothesis Journal — [Bug Title]

### H1: [Descriptive Title]
- **Hypothesis:** [What's causing the bug — be specific]
- **Evidence for:** [Supporting observations with file:line references]
- **Evidence against:** [Contradicting observations]
- **Test plan:** [Concrete steps to confirm or reject]
- **Status:** Pending / Confirmed / Rejected
- **Notes:** [Additional context, timestamps, agent findings]

### H2: [Descriptive Title]
[Same format]
```

### Rules

- **Minimum hypotheses:** 1 on quick track, 2-3 on deep track
- **Never delete entries** — rejected hypotheses are valuable context
- **Update incrementally** — add evidence as you find it, don't wait
- **Be specific** — "the data is wrong" is not a hypothesis; "processOrder receives dollars but expects cents" is

---

## Track Reference

| Aspect | Quick Track | Deep Track |
|--------|-------------|------------|
| Investigation | Read error location + 1-2 callers | 2-3 code-explorer agents in parallel |
| Hypotheses | Minimum 1 | Minimum 2-3 |
| Root cause testing | Manual verification | 1-3 bug-investigator agents in parallel |
| Fix validation | Run failing + related tests | Tests + code-quality skill + related issue scan |
| Auto-escalation | After 2 rejected hypotheses | N/A |
| Typical complexity | Off-by-one, typo, wrong argument, missing null check | Race condition, state corruption, multi-file logic error |

---

## Agent Coordination

### Code Explorers (Phase 2, deep track)

Use cross-plugin agent reference:
```
subagent_type: "agent-alchemy-core-tools:code-explorer"
```

These are Sonnet-model read-only agents that explore codebase areas. Give each a distinct focus area related to the bug. They report structured findings.

### Bug Investigators (Phase 3, deep track)

Use same-plugin agent reference:
```
subagent_type: "bug-investigator"
```

These are Sonnet-model agents with Bash access for running tests and git commands, but no Write/Edit — they investigate and report evidence, they don't fix code. Give each a specific hypothesis to test.

### Error Handling

- If an agent fails, continue with remaining agents' results
- If all agents fail in a phase, fall back to manual investigation
- Never block on a single agent — partial results are better than no results

---

## Error Recovery

If any phase fails:
1. Explain what went wrong and what you've learned so far
2. Present the hypothesis journal as-is
3. Ask the user how to proceed via AskUserQuestion:
   - "Retry this phase"
   - "Skip to fix" (if you have enough evidence)
   - "Provide more context"
   - "Abort"
