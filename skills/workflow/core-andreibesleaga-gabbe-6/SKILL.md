---
name: sdlc-checkpoint
description: Save SDLC milestone snapshot, verify phase gates, advance tracking, and tag git commit
triggers: [checkpoint, milestone, end of phase, requirements approved, design done, ready to code, sprint done, phase complete]
context_cost: low
---

# SDLC Checkpoint Skill

## Goal
Create durable snapshots at each SDLC gate so the project can be resumed, audited, or rolled back to any milestone. Verify all gate criteria before advancing to the next phase.

## SDLC Phases

| Phase | Name | Gate Criteria |
|---|---|---|
| S01 | REQUIREMENTS | PRD.md with EARS syntax, ambiguities resolved, human approval |
| S02 | DESIGN | Architecture decided, C4 model documented, ADRs written, threats modeled |
| S03 | SPECIFICATION | Technical spec finalized, API contracts defined, migration plan ready |
| S04 | TASKS | Tasks decomposed to ~15-min units, all accepted |
| S05 | IMPLEMENTATION | All tasks in project/tasks.md have status DONE |
| S06 | TESTING | All tests passing, coverage > 96%, 7-gate quality passed |
| S07 | SECURITY | SECURITY_CHECKLIST.md completed, no critical CVEs, threat mitigations verified |
| S08 | REVIEW | Human code review approved, all blocking feedback addressed |
| S09 | STAGING | Deployed to staging, smoke tests passing |
| S10 | PRODUCTION | Production deployed, rollback plan documented, monitoring active |

## Steps

1. **Identify which phase is completing**
   - Determine the phase number (S01-S10) from current context
   - Retrieve the gate criteria for this phase from the table above

2. **Verify gate criteria are met**
   ```
   S01 gate check:
   [ ] PRD.md exists with EARS-formatted requirements
   [ ] No unresolved ambiguities in requirements
   [ ] Human has explicitly approved the PRD

   S02 gate check:
   [ ] PLAN.md or architecture document exists
   [ ] C4 diagrams exist in docs/architecture/ (or documented reason for exception)
   [ ] ADR created for any significant technology decision
   [ ] Threat model created for security-sensitive features

   S05 gate check:
   [ ] All tasks in project/tasks.md have status: DONE (none TODO, IN_PROGRESS, or BLOCKED)
   [ ] No task has "pending human decision" that hasn't been resolved

   S06 gate check:
   [ ] All tests passing: [run test command, confirm green]
   [ ] Coverage >= 96%: [run coverage command, confirm threshold]
   [ ] Lint: zero errors
   [ ] Typecheck: zero errors
   [ ] agentic-linter: no architecture violations

   S07 gate check:
   [ ] templates/security/SECURITY_CHECKLIST.md fully completed
   [ ] No critical CVEs in dependency audit
   [ ] All High/Critical threats from threat model have mitigations implemented
   ```

3. **If gate criteria NOT met**
   - List what is missing
   - Do NOT advance to next phase
   - Report to human: "Phase [X] checkpoint cannot be created — gate criteria not met: [list]"

4. **Create the SESSION_SNAPSHOT** (when gate criteria are met)

   Write file: `agents/memory/episodic/SESSION_SNAPSHOT/S0[X]_[phase-name].md`

   Content:
   ```markdown
   # Snapshot S0[X] — [Phase Name]
   Timestamp: [ISO 8601 datetime]
   Phase: S0[X]
   Created by: [agent persona or "human"]

   ## What Was Decided / Built
   [Summary of key decisions and artifacts produced in this phase]

   ## Artifact Status
   - PRD.md: [✓ exists / ✗ missing]
   - PLAN.md: [✓ exists / ✗ missing]
   - project/tasks.md: [✓ exists / N/M tasks done]

   ## Test Status
   - Last run: [timestamp]
   - Pass: [N] | Fail: [0] | Skip: [0]
   - Coverage: [X]%

   ## Security Status
   - Last audit: [timestamp or N/A]
   - Open CVEs: [0 critical, 0 high]
   - SECURITY_CHECKLIST: [X]% complete

   ## Key Decisions Made This Phase
   - [decision 1 with rationale]
   - ADRs created: [list]

   ## Open Issues / Known Debt
   - [any unresolved issues that the NEXT phase should be aware of]

   ## Gate Criteria Verified
   [✓] [criterion 1]
   [✓] [criterion 2]

   ## Next Phase Entry Criteria
   [what needs to happen to start the next phase]
   ```

5. **Update PROJECT_STATE.md**
   - Change current phase to the NEXT phase (or mark project complete at S10)
   - Update "Last checkpoint" timestamp and phase
   - Clear "Current Blockers" if resolved

6. **Write to AUDIT_LOG.md**
   ```
   | [timestamp] | [session] | [agent] | PHASE_TRANSITION | S0[X] [Phase] checkpoint created | SUCCESS | episodic/SESSION_SNAPSHOT/S0[X]_[name].md |
   ```

7. **Tag git commit**
   ```bash
   git tag checkpoint/S0[X]-[phase-name] -m "SDLC checkpoint: [phase] completed"
   # Note: only tag if working directory is clean (all changes committed)
   ```

## Constraints
- NEVER create a checkpoint if gate criteria are not met
- NEVER advance to next phase without human approval at S01, S02, S07, S08
- Snapshots are immutable — never overwrite a snapshot file (create a new one if re-doing a phase)
- Git tag must match snapshot filename for traceability

## Output Format
Created snapshot file path + updated PROJECT_STATE.md + AUDIT_LOG.md entry + git tag. Report: "Checkpoint S0[X] created. Next phase: S0[X+1]."
