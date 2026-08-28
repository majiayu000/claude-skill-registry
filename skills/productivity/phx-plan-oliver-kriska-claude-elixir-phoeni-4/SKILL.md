---
name: phx-plan
description: 'Plan features spanning multiple domains: billing (Stripe), auth (RBAC),
  real-time (Presence), webhooks, jobs (Oban). Use when designing interconnected systems
  or converting review findings into tasks.'
---

# Plan Elixir/Phoenix Feature

Plan a feature by researching the relevant Elixir/Phoenix concerns, then
output a structured plan with checkboxes.

## What Makes /phx-plan Different from /plan

1. Covers relevant concerns through resumable research tracks
2. Plans with `[ecto]`, `[liveview]`, `[oban]` task routing
3. Checks for Iron Law compliance in the plan
4. Includes `mix compile/format/credo/test` verification
5. Understands Phoenix context boundaries

## Usage

```
/phx-plan Add user avatars with S3 upload
/phx-plan .claude/plans/notifications/reviews/notifications-review.md
/phx-plan Implement notifications --depth deep
/phx-plan .claude/plans/auth/plan.md --existing
```

## Arguments

- Text after the skill name = feature description, review file, or existing plan
- `--depth quick|standard|deep` = Planning depth (auto-detected)
- `--existing` = Enhance an existing plan with deeper research

## Workflow

1. **Gather context** — File path (skip to research), brainstorm
   interview.md (skip clarification), clear description, or vague
2. **Clarify if vague** — Ask questions ONE at a time (skip if
   brainstorm interview.md exists with Status: COMPLETE)
3. **Detect depth** — Auto-detect quick/standard/deep
4. **Create research state** — Before research, create
   `.claude/plans/{slug}/scratchpad.md` with a concern-track checklist
5. **Gather optional runtime context** — Only when Tidewave tools are independently
   configured and exposed; otherwise inspect source, routes, schemas, and tests
6. **Research selectively** — Cover only relevant concerns. Native generic
   subagents may run independent tracks in parallel, but they are optional.
   Without them, run every selected track sequentially in this session and
   save evidence under `.claude/plans/{slug}/research/`
7. **Finish ALL research tracks** — Maintain the scratchpad checklist,
   marking each selected track `[x]` only after its evidence is captured.
   NEVER write the plan while any selected track remains unchecked
8. **Breadboard** (LiveView) — Produce the system map from collected evidence
9. **Completeness check** — MANDATORY when planning from review
10. **Split decision** — One plan or multiple, concrete options
11. **Generate plan** — Checkboxes, phased tasks, code patterns.
    Reuse `.claude/plans/{slug}/scratchpad.md` for decisions and dead-ends
12. **Self-check** (deep only) — Three questions in Risks section
13. **Present and ask** — STOP, show summary, let user decide

**When planning from review**: Every finding must appear in the
plan — either as a task OR explicitly deferred by the user.

See `references/planning-workflow.md` for detailed step-by-step.

### --existing Mode (Deepening)

Enhance an existing plan without relying on named agents:

1. Load the plan and create or update `.claude/plans/{slug}/scratchpad.md`
2. Identify thin sections and add a checklist of relevant concern tracks
3. Complete every track in this session, sequentially by default; generic workers
   are optional only for independent tracks and must write evidence under
   `.claude/plans/{slug}/research/`
4. Produce breadboarding and infrastructure notes directly from the gathered
   evidence, independent of whether workers were used
5. Add implementation detail, resolve spikes, and strengthen verification
6. Present a diff summary; never delete or silently rewrite existing tasks

## Iron Laws

1. **NEVER auto-start /phx-work** — Always present plan and ask
2. **Research before assuming** — Web-search unfamiliar tech
3. **Select research tracks narrowly** — Only relevant concerns, not all
4. **NEVER write the plan while selected research tracks remain incomplete**
5. **NEVER skip input findings** — Every finding MUST have a task
6. **Do NOT run a library-selection track for existing dependencies**
7. **Skip research when planning from review/investigation** — When
   input is a review file or `/phx-investigate` output, the findings
   ARE the research. Do NOT spawn agents to re-discover what the
   review already found. Convert findings directly to plan tasks.
   (Confirmed: 56-session analysis showed same findings discovered
   3-4x across review→investigate→plan phases, wasting ~96K tokens)

## Integration with Workflow

```text
/phx-plan {feature}  <-- YOU ARE HERE
       |
   /phx-plan --existing (optional enhancement)
       |
   ASK USER -> /phx-work .claude/plans/{feature}/plan.md
       |
/phx-review → /phx-compound
```

## Notes

- Plans saved to `.claude/plans/{slug}/plan.md`
- Research reports in `.claude/plans/{slug}/research/` can be deleted after

## CRITICAL: After Writing the Plan

**STOP. Do NOT proceed to implementation.**

After writing `.claude/plans/{slug}/plan.md`:

1. Summarize: task count, phases, key decisions
2. Ask the user a normal conversational question with these options:
   - "Start in fresh session" (recommended for 5+ tasks)
   - "Get a briefing" (`/phx-brief` — interactive walkthrough)
   - "Start here"
   - "Review or adjust the plan"
3. Wait for user response. Never auto-start work.

**When user selects "Start in fresh session"**, print:

```
1. Run `/new` to start a fresh session
2. Then run one of:
   /phx-work .claude/plans/{slug}/plan.md
   /phx-full .claude/plans/{slug}/plan.md  (includes review + compound)
```

This is Iron Law #1. Violating it wastes user context.

## References (DO NOT read — for human reference only)

- `references/planning-workflow.md` — Detailed step-by-step
- `references/plan-template.md`
- `references/complexity-detail.md`
- `references/example-plan.md`
- `references/agent-selection.md`
- `references/breadboarding.md`
