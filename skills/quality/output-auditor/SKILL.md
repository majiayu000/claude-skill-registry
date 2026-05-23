---
name: output-auditor
description: Multi-angle review of responses before delivery. Audits from 4 perspectives -- factual accuracy, logical consistency, completeness, and safety. Use for high-stakes responses where errors have real consequences.
---

# Output Auditor: 4-Angle Response Review

Review every response from 4 independent angles before delivery.

## The 4 audit angles

### Angle 1: Factual accuracy
Is every claim true?

Check:
- File paths exist
- Function names are correct
- Code quotes match actual files
- Version numbers are current
- Behavior descriptions match actual code

### Angle 2: Logical consistency
Does the response contradict itself?

Check:
- Does the diagnosis match the suggested fix?
- Are the steps in the right order?
- Do dependencies match (step 3 doesn't require something from step 5)?
- Are there circular arguments?
- Does the explanation match the code?

### Angle 3: Completeness
Is anything missing?

Check:
- Does it answer the actual question?
- Are edge cases covered?
- Are prerequisites mentioned?
- Is there a rollback plan for risky changes?
- Are there obvious alternatives not mentioned?

### Angle 4: Safety
Could this cause harm?

Check:
- Could this code change break existing functionality?
- Could this advice create a security vulnerability?
- Could this command cause data loss?
- Are there race conditions or concurrency issues?
- Is error handling adequate?

## Audit process

1. Write the response
2. Run each angle as a mental checkpoint
3. For each issue found, fix it before delivering
4. If you can't fix it, flag it clearly in the response

## Severity levels

CRITICAL: Wrong information that would cause harm (wrong security advice, data-destroying command)
-> Must fix before delivering. If you can't fix, do not deliver.

WARNING: Incomplete or potentially misleading information
-> Fix if possible. If not, add a clear caveat.

MINOR: Style issues, missing context that isn't essential
-> Fix if quick. Otherwise note for follow-up.

## Quick audit checklist

Before sending any response with code or technical advice:

[ ] Every file path verified with Glob
[ ] Every function/variable verified with Grep or Read
[ ] Steps are in correct order
[ ] No self-contradictions
[ ] The actual question is answered
[ ] Dangerous operations have warnings
[ ] Rollback path exists for destructive changes
