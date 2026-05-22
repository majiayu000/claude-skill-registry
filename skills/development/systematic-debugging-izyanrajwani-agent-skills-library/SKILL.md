---
name: systematic-debugging
description: Root cause analysis for debugging. Use when bugs, test failures, or unexpected behavior have non-obvious causes, or after multiple fix attempts have failed.
---

# Systematic Debugging

**Core principle:** Find root cause before attempting fixes. Symptom fixes are failure.

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Read stack traces completely
   - Note line numbers, file paths, error codes
   - Don't skip warnings

2. **Reproduce Consistently**
   - What are the exact steps?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - Git diff, recent commits
   - New dependencies, config changes
   - Environmental differences

4. **Gather Evidence in Multi-Component Systems**

   **WHEN system has multiple components (CI → build → signing, API → service → database):**

   Add diagnostic instrumentation before proposing fixes:
   ```
   For EACH component boundary:
     - Log what data enters/exits component
     - Verify environment/config propagation
     - Check state at each layer

   Run once to gather evidence → analyze → identify failing component
   ```

   Example:
   ```bash
   # Layer 1: Workflow
   echo "=== Secrets available: ==="
   echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

   # Layer 2: Build script
   env | grep IDENTITY || echo "IDENTITY not in environment"

   # Layer 3: Signing
   security find-identity -v
   ```

5. **Trace Data Flow**

   See `references/root-cause-tracing.md` for backward tracing technique.

   Quick version: Where does bad value originate? Trace up call chain until you find the source. Fix at source.

## Phase 2: Pattern Analysis

1. **Find Working Examples** - Similar working code in codebase
2. **Compare Against References** - Read reference implementations COMPLETELY, don't skim
3. **Identify Differences** - List every difference, don't assume "that can't matter"
4. **Understand Dependencies** - Components, config, environment, assumptions

## Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis** - "I think X is root cause because Y" - be specific
2. **Test Minimally** - SMALLEST possible change, one variable at a time
3. **Verify** - Worked → Phase 4. Didn't work → form NEW hypothesis, don't stack fixes
4. **When You Don't Know** - Say so. Don't pretend.

## Phase 4: Implementation

1. **Create Failing Test Case**
   - Use the `test-driven-development` skill
   - MUST have before fixing

2. **Implement Single Fix**
   - ONE change at a time
   - No "while I'm here" improvements

3. **Verify Fix**
   - Test passes? Other tests still pass? Issue resolved?

4. **If Fix Doesn't Work**
   - Count attempts
   - If < 3: Return to Phase 1 with new information
   - **If ≥ 3: Escalate (below)**

## Escalation: 3+ Failed Fixes

**Pattern indicating architectural problem:**
- Each fix reveals new problems elsewhere
- Fixes require massive refactoring
- Shared state/coupling keeps surfacing

**Action:** STOP. Question fundamentals:
- Is this pattern fundamentally sound?
- Are we continuing through inertia?
- Refactor architecture vs. continue fixing symptoms?

**Discuss with human partner before more fix attempts.** This is wrong architecture, not failed hypothesis.

## Red Flags → STOP and Return to Phase 1

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X"
- "I'll skip the test"
- "It's probably X"
- "Pattern says X but I'll adapt it differently"
- Proposing solutions before tracing data flow
- "One more fix" after 2+ failures

## Human Signals You're Off Track

- "Is that not happening?" → You assumed without verifying
- "Will it show us...?" → You should have added evidence gathering
- "Stop guessing" → You're proposing fixes without understanding
- "Ultrathink this" → Question fundamentals
- Frustrated "We're stuck?" → Your approach isn't working

**Response:** Return to Phase 1.

## Supporting Techniques

Reference files in `references/`:
- **`root-cause-tracing.md`** - Trace bugs backward through call stack
- **`defense-in-depth.md`** - Add validation at multiple layers after finding root cause
- **`condition-based-waiting.md`** - Replace arbitrary timeouts with condition polling

Related skills:
- **`test-driven-development`** - Creating failing test case (Phase 4)
- **`verification-before-completion`** - Verify fix before claiming success
