---
name: esper:review
description: Review the current implementation against the approved increment and specs. Identifies drift, regressions, and missing spec maintenance.
---

You are reviewing the current implementation against the approved increment and spec tree.

## Step 1: Read context

Run `esperkit context get` to determine the current state.

If no active increment, tell the user: "No active increment to review. Run `esper:atom` or `esper:batch` first." and stop.

Check for an active run (`active_run` field). If present, this review should also consider run artifacts.

## Step 2: Read the increment and specs

Read the active increment file from `.esper/increments/active/<filename>`.
If the increment references a spec file (`spec:` field), read it: `esperkit spec get <file>`
Read `.esper/CONSTITUTION.md` for project constraints.

**If an autonomous run is active or recently completed:**
- Run `esperkit run get <run-id>` to read the run state
- Run `esperkit run list-tasks <run-id>` to see task status
- Run `esperkit run list-reviews <run-id>` to see previous review rounds
- The review must evaluate against the frozen spec snapshot recorded in the run, not the current spec files

## Step 3: Assess implementation state

Compare the current codebase state against the increment plan:

1. **Scope coverage**: For each item in `## Scope`, check if it has been implemented
2. **Files affected**: For each file in `## Files Affected`, check if the expected changes exist
3. **Verification**: Run the commands in `## Verification` and check results
4. **Spec alignment**: Compare the implementation against the referenced spec — does the code match what the spec describes?

**For autonomous runs, also check:**
5. **Task completion**: Verify all task packets are marked complete
6. **Review findings**: Check if previous review rounds identified issues that were resolved
7. **Repair coverage**: Confirm repair tasks from previous rounds were addressed
8. **Frozen input consistency**: Verify the implementation matches the frozen spec and increment inputs, not drifted versions

## Step 4: Identify issues

Check for:
- **Drift**: Implementation that diverges from the increment plan (extra changes, different approach)
- **Regressions**: Changes that break existing behavior documented in specs
- **Missing spec maintenance**: Implementation changes that require spec updates but specs haven't been updated
- **Scope creep**: Work done beyond what the increment plan describes
- **Incomplete items**: Scope items not yet implemented

**For autonomous runs, also check:**
- **Role separation**: Was the reviewer role distinct from the implementation role?
- **Stop condition compliance**: Did the run respect configured limits?
- **Escalation handling**: Were any escalations properly communicated?

## Step 5: Write findings

Update the active increment file's `## Progress` section with findings:

```markdown
## Progress

### Review Findings — [date]
- [ok] Scope item 1: implemented as planned
- [ok] Scope item 2: implemented as planned
- [drift] Scope item 3: implementation differs — [explanation]
- [incomplete] Scope item 4: not yet implemented
- [spec] product/behavior.md needs updating: [what changed]
```

**If an autonomous run is active**, also persist findings as a review record:
`esperkit run add-review <run-id> '<review-json>'`

The review JSON should include:
- `round`: the review round number
- `candidate_commit`: the current commit hash being reviewed
- `findings`: array of finding descriptions
- `repair_tasks`: array of repair task descriptions (if review fails)
- `result`: "passed" or "failed"

## Step 6: Recommend next actions

Based on findings:
- If all scope items complete and verification passes: "Ready to finish. Run `esper:go` to complete."
- If spec updates needed: "Run `esper:sync` to update specs before finishing."
- If incomplete items remain: "Run `esper:continue` to resume implementation."
- If drift detected: Present the drift and ask the user how to resolve it.

**For autonomous runs with failed review:**
- Convert findings into repair tasks
- Ask the user whether to dispatch repair tasks or escalate
- If dispatching: create repair task packets via `esperkit run add-task`
- If escalating: stop the run via `esperkit run stop <run-id> 'Escalated after review'`

## Available CLI commands

- `esperkit context get` — read context
- `esperkit spec index` — show spec tree
- `esperkit spec get <file>` — read a spec
- `esperkit increment list` — list increments
- `esperkit run get <id>` — read run state
- `esperkit run list-tasks <id>` — list tasks in a run
- `esperkit run list-reviews <id>` — list reviews in a run
- `esperkit run add-review <id> '<json>'` — persist review findings
- `esperkit run add-task <id> '<json>'` — create repair task
- `esperkit run stop <id> [reason]` — stop/escalate a run
