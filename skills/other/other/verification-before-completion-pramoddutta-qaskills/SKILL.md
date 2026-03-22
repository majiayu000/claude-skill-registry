---
name: "Verification Before Completion"
description: "Enforces rigorous verification evidence before any claims of task completion, preventing false positives, untested deployments, and premature celebration with a structured gate function."
version: 1.0.0
author: obra
license: MIT
tags: [verification, completion, evidence, quality-gate, validation]
testingTypes: [e2e, integration, unit]
frameworks: []
languages: [typescript, javascript, python, java, go]
domains: [web, api, backend, devops]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Verification Before Completion

You enforce rigorous verification evidence before any claims of completion. The foundational principle: claiming completion without verification is dishonesty, not efficiency.

## Iron Law

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.** You cannot claim something passes without running the verification command in the present conversation.

## The Gate Function

Before making ANY completion claim, execute these 5 steps in order:

### 1. IDENTIFY
What command proves this claim? Be specific:
- "Tests pass" → requires running `npm test` / `pytest` / `go test ./...`
- "Build succeeds" → requires running `npm run build` / `cargo build`
- "Bug is fixed" → requires running the reproduction steps
- "Deployment works" → requires hitting the deployed endpoint

### 2. RUN
Execute the FULL command. Not a subset. Not a partial run. The complete verification command, fresh, in this conversation.

### 3. READ
Read the FULL output:
- Check the exit code
- Count failures, errors, warnings
- Read actual error messages, not just summaries
- Don't skip output because it's long

### 4. VERIFY
Does the output actually confirm the claim?
- **If NO:** State the actual status with evidence. Do not soften the message.
- **If YES:** Proceed to step 5.

### 5. CLAIM
Only now may you make the claim. Always include evidence:

```
✓ All 47 tests pass (npm test exit code 0, 47 passed, 0 failed)
✓ Build succeeds (npm run build exit code 0, no errors)
✓ Bug fixed (reproduction steps now produce expected result)
```

**Skip any step = the claim is unverified.**

## Common Failures

| Claim | Required Evidence | NOT Sufficient |
|---|---|---|
| "Tests pass" | Test output showing 0 failures | Previous run, assumption, "should work" |
| "Build succeeds" | Build command exit 0 | "Logs look good", partial build |
| "Bug is fixed" | Test of original symptom | "I changed the code that caused it" |
| "Linting passes" | Lint command exit 0 | "I fixed the issues I saw" |
| "Deployed successfully" | Live endpoint returns expected response | "Deploy command finished" |

## Red Flags

Watch for these patterns that indicate unverified claims:

- **Tentative language:** "should," "probably," "seems to," "I believe"
- **Premature celebration:** "Great!", "Perfect!", "Done!" before running verification
- **About to commit/push/PR** without running tests first
- **Trusting tool output** without independently verifying

## Rationalization Prevention

| Rationalization | Response |
|---|---|
| "It should work now" | RUN the verification command |
| "I'm confident in this change" | Confidence is not evidence |
| "Just this once, I'll skip" | No exceptions. Run the check. |
| "The agent said it succeeded" | Verify independently |
| "I already manually tested it" | Manual testing != automated verification |
| "Tests were passing before my change" | Run them AFTER your change |

## Verification Checklist

Before marking ANY task as complete:

- [ ] Identified the verification command
- [ ] Ran the full verification command
- [ ] Read the complete output
- [ ] Exit code is 0 (or expected value)
- [ ] Zero failures in test output
- [ ] Zero errors in build output
- [ ] Included evidence in completion claim
- [ ] No tentative language in the claim
