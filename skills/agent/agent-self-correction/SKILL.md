---
name: Agent Self-Correction
description: Protocols for the agent to autonomously detect failures, analyze root causes, and attempt recovery strategies before requesting user intervention.
---

# Agent Self-Correction

[Context: Errors and roadblocks are inevitable. An efficient agent does not stop at the first sign of failure; it analyzes the error, adjusts its approach, and retries. This skill defines the cognitive loop for autonomous self-correction.]

## 1. Core Principles
- **Analyze First**: Never retry the exact same action without understanding *why* it failed.
- **Fail Fast, recover Faster**: Identify failure modes immediately (tech stack mismatch, syntax error, hallucination).
- **Graceful Escalation**: Attempt 2-3 autonomous fixes before escalating to the user.
- **State Preservation**: Don't destroy partial progress when fixing a specific bug.

## 2. Step-by-Step Implementation

### Phase 1: Failure Detection & Analysis
When a tool returns an error or a check fails:
1. **Stop**: Do not proceed to the next step of the plan.
2. **Read**: Analyze the error message thoroughly.
   - Is it a syntax error? -> Fix code.
   - Is it a logic error? -> Rethink algorithm.
   - Is it a tool misuse? -> Check tool definition.
   - Is it environmental? -> Check paths/permissions.
3. **Hypothesize**: Formulate a hypothesis for the fix.

### Phase 2: autonomous Recovery Loop
1. **Attempt 1 (Quick Fix)**: Address the obvious error (e.g., install missing package, fix typo).
2. **Verify**: Run the verification command (e.g., `npm run build` or `pytest`).
3. **Attempt 2 (Alternative Approach)**: If Attempt 1 fails, try a different distinct strategy (e.g., switch library, rewrite logic).
4. **Attempt 3 (Simplify)**: Reduce complexity or scope to isolate the issue.

### Phase 3: Escalation
If Attempt 3 fails:
1. **Gather Context**: Collect error logs and the 3 failed attempts.
2. **Propose solution**: Present the user with the situation and a proposed manual intervention or request for clarification.

## 3. Templates & Examples

### Internal Monologue for Debugging
```text
ERROR DETECTED: [Error Message]
ANALYSIS: The error implies [Cause].
HYPOTHESIS: If I change [X] to [Y], it should resolve.
ACTION: Applying fix [X->Y].
```

### Self-Correction Checklist
- [ ] Did I read the *entire* error message?
- [ ] Have I checked if the file path is correct?
- [ ] Did I verify the library version compatibility?
- [ ] Is this a hallucinated import?

## 4. Common Pitfalls
- **Don't**: Blindly loop the same command hoping it works eventually.
- **Don't**: Delete the user's codebase to "start over" without permission.
- **Do**: Use `common_sense` to judge if an error is a simple typo or a fundamental design flaw.
