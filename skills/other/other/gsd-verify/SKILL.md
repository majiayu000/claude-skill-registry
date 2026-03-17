---
name: gsd-verify
description: Verify completed work against plan requirements
argument-hint: "[<phase-number>]"
tags: [orchestration, verification, gsd, quality]
user-invocable: true
---

# GSD Verify -- Work Verification

Verify completed work meets requirements defined in the plan.

## What To Do

1. **Load verification criteria** from ROADMAP.md for the phase.
2. **Run automated checks**: build, tests, lint, custom verify commands.
3. **Check deliverables**: all files exist, all done criteria met, no regressions.
4. **Generate verification report**:
   ```
   ## Phase N Verification Report
   - Build: PASS
   - Tests: 22/22 PASS
   - Coverage: 87% (threshold: 80%)
   - Files created: 8/8
   - Regressions: NONE
   ```
5. **If verification fails**: Create fix tasks, update STATE.md with failures.

## Arguments
- `<phase-number>`: Verify specific phase (default: latest completed)
- `--all`: Verify all completed phases
- `--strict`: Fail on any warning