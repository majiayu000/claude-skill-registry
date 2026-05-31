---
name: pm-planning
description: Decomposition methodology for pm agent — turns an approved ARCH document into a Beads task list with explicit dependencies, time-boxes, and acceptance criteria. The pipeline can only orchestrate work it can see; this skill defines what "seeable work" looks like.
when_to_use: |
  Apply when:
  - pm agent receives an approved ARCH-*.md from architect
  - pm needs to write PLAN-*.md
  - pm creates Beads tasks for senior-dev to claim
  Do NOT apply for:
  - nano archetypes (pm phase is skipped — senior-dev claims one task directly)
  - bug-fixes with a one-line repro (no decomposition needed)
effort: medium
allowed-tools: Read, Write, Bash(bd:*)
paths:
  - "docs/architecture/**"
  - "docs/plans/**"
---

# PM planning — decompose ARCH into tasks

The pm agent's job is to take the architect's ARCH document and produce
2 things:
1. A `PLAN-<feature>.md` for humans
2. A sequence of `bd create` tasks for senior-dev to claim

The plan is good if a fresh senior-dev (no prior context) can pick up
the bd tasks and ship without coming back for clarification.

## The decomposition rules

### Rule 1. Tasks ≤ 4 hours

Anything bigger gets split. If the task is "build the auth system",
split into:
- Schema migration for user table
- Signup endpoint with hashing
- Login endpoint with JWT issuance
- Logout / token revocation
- Tests

Each ≤ 4h. If you can't split, the task is unclear — go back to ARCH
and clarify.

### Rule 2. Single output artefact per task

Each task produces ONE of:
- A code file (new or modified)
- A database migration
- A test file
- A documentation update
- A config change

If a task produces multiple unrelated artefacts, split it.

### Rule 3. Explicit dependencies via `--blocks`

When task B requires task A's output:

```bash
bd create "Task A: schema migration" -p P1
# returns id: my-proj-001-abc

bd create "Task B: signup endpoint" -p P1 \
  --blocks-on my-proj-001-abc \
  --label senior-dev
```

The pipeline orchestrator reads `bd ready --assignee senior-dev` to know
what's claimable. Tasks blocked on incomplete predecessors don't appear.

### Rule 4. Acceptance criteria — what does "done" mean?

Every task description ends with a bulleted "Done when:" section.

```markdown
## Done when:
- [ ] POST /signup returns 201 with user_id on success
- [ ] Bad email returns 400 with "invalid_email"
- [ ] Duplicate email returns 409 with "email_taken"
- [ ] Password is hashed with argon2 (no plaintext in DB)
- [ ] Unit test in `tests/auth/signup.test.ts` covers all 4 cases
- [ ] `npm test` passes
```

Senior-dev knows EXACTLY what to ship and when to stop.

### Rule 5. Owners and parallelism

If 3 tasks can run in parallel, mark each with the agent it goes to.
Don't bundle them.

```bash
bd create "..." --label senior-dev
bd create "..." --label senior-dev   # parallel
bd create "..." --label devops       # parallel, different agent
```

## The PLAN-*.md template

```markdown
# PLAN — <feature>

Date: <ISO>
Architect ARCH: docs/architecture/ARCH-<feature>.md
Owner: pm

## Summary

2-3 sentences. What problem, what solution. Reference ARCH for detail.

## Cost estimate

(Follow skill: cost-model)

## Tasks

1. **<title>** [P1, ≤2h, senior-dev]
   - Goal: <one-sentence>
   - Done when: <bulleted criteria>
   - bd id: <ID after create>

2. **<title>** [P1, ≤4h, senior-dev]
   - Blocked on: 1
   - Goal: ...
   - Done when: ...

3. **<title>** [P2, ≤1h, qa-engineer]
   - Blocked on: 1, 2

## Pre-mortem

(Follow skill: pre-mortem)

## Gates

(Follow GATES_BY_ARCHETYPE for this archetype + project_size)
- [ ] gate:plan — after pm finishes, before senior-dev starts
- [ ] gate:qa — after qa-engineer, before ship
- [ ] gate:ship — after security-officer, before devops
```

## When pm should push back instead of plan

The pm agent is allowed — and EXPECTED — to refuse a plan if the ARCH is
incomplete. Specifically:

❌ **ARCH is missing acceptance criteria for the feature itself.**
Push back: "ARCH says 'build webhook handler' but doesn't specify what
counts as success. Re-architect with explicit success criteria."

❌ **ARCH doesn't specify the failure mode.**
Push back: "ARCH says 'handle errors gracefully' but doesn't say what
'graceful' means. Define: log + ack? log + retry? log + alert?"

❌ **ARCH conflicts with existing ADRs.**
Push back: "ARCH proposes Postgres but ADR-005 mandated DynamoDB.
Resolve before plan."

Push-back goes to the architect with `bd update` + label `re-arch`. The
plan is BLOCKED until ARCH is refined.

## Anti-patterns

❌ **Tasks named after components, not goals.** "Build UserService" is
ambiguous. "Add POST /signup endpoint that hashes password with argon2"
is clear.

❌ **No dependencies declared.** Two tasks editing the same file with
no `--blocks-on` will conflict. Always declare.

❌ **Estimating without doing one task.** If you genuinely don't know
how long task 1 takes, ask senior-dev to do task 1 first and report
back. THEN estimate 2–N.

❌ **Tasks > 8 hours.** Split. No exceptions.
