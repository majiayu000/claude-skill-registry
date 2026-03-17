---
name: self-heal
description: Autonomous diagnose-research-fix-verify loop — up to 5 attempts before human escalation
triggers: [test failing, error, self-heal, stuck, broken, can't fix, autonomous fix, retry, fix this]
context_cost: medium
---

# Self-Heal Skill

## Goal
When an agent encounters a failure, autonomously diagnose, research (if needed), fix, and verify — escalating to human only after exhausting all autonomous options (max 5 attempts).

## Self-Healing Loop

```
FAIL detected
  -> Attempt 1: Diagnose error type
  -> Apply fix
  -> Verify
  -> PASS? Done (log to AUDIT_LOG.md)
  -> FAIL? Attempt 2...
  -> ...
  -> Attempt 5 fails? ESCALATE TO HUMAN (stop all action)
```

## Steps

### Pre-Healing: Check CONTINUITY.md (Dynamic Optimization)
Before starting, read `agents/memory/CONTINUITY.md`:
- Has this exact error or approach been tried before?
- If yes: **STOP**. Apply the recorded solution directly (skip re-discovery).
- If no: proceed with diagnosis. This allows the system to "learn" from past mistakes dynamically.

### Per-Attempt Procedure

0. **Safety Check (Loop Avoidance)**
   - Check `production-health.skill.md` rules:
   - Is this the 3rd time trying the exact same fix? -> **STOP**.
   - Is the recursion depth > 10? -> **STOP**.

1. **Diagnose the error**
   - Read the full error message and stack trace
   - Classify the error type:
     - **Known error** (in CONTINUITY.md) → apply past solution
     - **Type error** → fix types without changing logic
     - **Test failure** → determine: is test wrong (false positive) OR implementation wrong?
     - **Import/dependency error** → check package installed, correct version
     - **Runtime error** → check data shape, null guards, async/await
     - **Build error** → check syntax, missing exports, circular imports
     - **Unknown error** → invoke research.skill

2. **Classify: automation vs human decision**

   **Agents may self-heal autonomously:**
   - Type errors and lint errors
   - Test assertion updates (when behavior spec changed, not logic)
   - Deprecated API calls (verified via Context-7 MCP)
   - Import path corrections
   - Missing await on async calls
   - Patch/minor version dependency bumps
   - Formatting issues

   **Requires human decision (STOP immediately):**
   - Architecture or library changes
   - Breaking API changes
   - Security-affecting changes
   - Major version dependency bumps
   - Any change to CONSTITUTION.md
   - Unknown error after research finds no solution

3. **Research if needed (for unknown errors)**
   - Invoke research.skill with the error message + library version
   - Check Context-7 MCP for library-specific error patterns
   - Check GitHub issues for the library (via GitHub MCP)
   - If past-knowledge (knowledge cutoff) might be wrong: research current version

4. **Hypothesize and implement fix**
   - State the hypothesis explicitly before fixing
   - Apply the MINIMAL change needed to fix the error
   - Do not refactor or improve other code during self-heal

5. **Verify**
   - Run the failing test/build
   - Run the full test suite (must not introduce regressions)
   - If PASS: log to AUDIT_LOG.md and done
   - If FAIL: increment attempt counter, go to next attempt with new hypothesis

### On Attempt 5 Failure: Human Escalation

Stop ALL autonomous action. Create escalation report:

```markdown
## ESCALATION REQUIRED

**Error:** [exact error message]

**Context:** [what was being implemented when this occurred]

**Attempt 1:**
- Hypothesis: [what I thought the cause was]
- Fix tried: [what I changed]
- Result: [how it failed]

**Attempt 2:** [same format]
**Attempt 3:** [same format]
**Attempt 4:** [same format]
**Attempt 5:** [same format]

**Research Findings:**
[what authoritative sources say about this error, if anything]

**Options for human decision:**
1. [option A] — [what this would mean]
2. [option B] — [what this would mean]

**Recommended:** [option X because Y]

**Awaiting:** Your decision on which option to proceed with.
```

Then:
- Write escalation to AUDIT_LOG.md (action type: HUMAN_ESCALATION)
- Update task in project/tasks.md → status: BLOCKED
- Do nothing else until human responds

### After Resolution
Once human provides direction:
- Record the resolution in CONTINUITY.md (to prevent future repetition)
- Apply the human-approved fix
- Verify all tests pass
- Update AUDIT_LOG.md with resolution

## Constraints
- Maximum 5 autonomous attempts before escalation — never exceed this
- Never change architecture or library during self-heal (these require human approval)
- Always check CONTINUITY.md first (prevents repeating known failed approaches)
- Escalation report must be complete and specific — vague reports delay resolution

## Output Format
Either: "SELF-HEALED — fixed on attempt [N]. All tests passing." OR "ESCALATION REQUIRED — [report]"
