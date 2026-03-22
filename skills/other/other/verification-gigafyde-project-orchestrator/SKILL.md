---
name: project-orchestrator:verification
description: Use before claiming ANY work is complete — ensures evidence-based verification across all affected services, correct git state, and deployment confirmation.
user-invocable: false
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## Config Loading

1. Check if `.project-orchestrator/project.yml` exists
2. If yes: parse and extract `services` (test commands, auto_deploy), `plans_dir`, `plans_structure`
3. If no: use defaults (monorepo, root, auto-detect test command)

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

---

## Verification Checklist

### 1. Run affected service tests

Every affected service MUST have its tests run fresh.

Test commands come from `config.services[name].test`, the project's root CLAUDE.md, or auto-detection.

**Multi-service rule:** When a change spans services, verify ALL affected services — not just the one you changed.

### 2. Cross-service contract verification

If API shapes changed between services:

| Check | How |
|-------|-----|
| Producer response matches contract | Read the controller/endpoint, verify shape |
| Consumer expects correct shape | Read the API call site, verify it parses correctly |
| Event payload matches | Verify publisher and consumer agree on schema |

### 3. Git state verification

Verify each affected service has clean git state:
```bash
# Verify correct service repo and branch
cd <service> && git branch --show-current

# Verify changes are committed
cd <service> && git status

# Verify no unrelated files staged
cd <service> && git diff --staged --name-only
```

### 4. Deployment verification (auto-deploy services)

For services where `config.services[name].auto_deploy` is `true`:
1. Wait for deployment to complete
2. Ask user to confirm deployment success (check logs, verify endpoint)
3. Do NOT claim "deployed and working" without user confirmation

### 5. Living state doc update

If working from a plan in `{config.plans_dir}/`:
- Update task status in Implementation Tasks table
- Log verification results in Implementation Log
- Update overall status if all tasks complete
- When status becomes `complete`:
  - If `config.plans_structure` is `standard`: move doc to `{plans_dir}/completed/` and update `{plans_dir}/INDEX.md`
  - If `flat`: just update status in the doc

---

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| "Tests pass" | Test command output: 0 failures | Previous run, "should pass" |
| "Build succeeds" | Build command: exit 0 | "Linter passed" |
| "Bug fixed" | Test original symptom: passes | "Code changed, assumed fixed" |
| "All services verified" | Test output from EACH service | Testing only one of three affected |
| "Deployed and working" | User confirmed endpoint works | "Push succeeded" |
| "Committed to right branch" | `git branch` output | Assumption |
| "No regressions" | Full test suite: 0 failures | Spot-checking one test |

---

## Red Flags — STOP

If you catch yourself:
- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Done!")
- About to commit/push without running tests
- Trusting a teammate agent's success report without checking
- Only testing the service you changed, not consumers/producers
- Saying "deployed" without user confirming the endpoint

**ALL of these mean: STOP. Run the verification.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Linter passed" | Linter ≠ tests ≠ build |
| "Agent said success" | Verify independently |
| "Only changed one file" | One file can break everything |
| "Tests passed earlier" | Earlier ≠ now. Run again. |
| "Other service wasn't touched" | Contract changes affect consumers too |

---

## Quick Reference

| Phase | What to Verify | How |
|-------|---------------|-----|
| Tests | Each affected service | Run `config.services[name].test` or auto-detected command |
| Contracts | Producer + consumer match | Read both sides, compare shapes |
| Git | Correct repo, branch, clean state | `git branch`, `git status` per service |
| Deploy | Endpoint works | User confirms after push |
| State doc | Updated with results | Edit `{plans_dir}/*.md`, move to `completed/` when done (standard structure) |

---

## Related Commands & Skills

| When | Action |
|------|--------|
| Verification passed, ready to merge | Suggest user run `/project:finish` |
| Changelog needed | Suggest user run `/project:changelog` |
