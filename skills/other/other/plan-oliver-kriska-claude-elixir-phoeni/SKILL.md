---
name: phx:plan
description: Use for any multi-file feature, new context, or change that benefits from upfront design. Also accepts review output files to create follow-up plans from findings. Use --existing to enhance an existing plan with research. Spawns specialist agents for architecture, Ecto schema, and security analysis.
effort: high
argument-hint: <feature description OR path to review/plan file>
disable-model-invocation: true
---

# Plan Elixir/Phoenix Feature

Plan a feature by spawning Elixir specialist agents, then output
structured plan with checkboxes.

## What Makes /phx:plan Different from /plan

1. Spawns Elixir specialist agents for research
2. Plans with `[ecto]`, `[liveview]`, `[oban]` task routing
3. Checks for Iron Law compliance in the plan
4. Includes `mix compile/format/credo/test` verification
5. Understands Phoenix context boundaries

## Usage

```
/phx:plan Add user avatars with S3 upload
/phx:plan .claude/plans/notifications/reviews/notifications-review.md
/phx:plan Implement notifications --depth deep
/phx:plan .claude/plans/auth/plan.md --existing
```

## Arguments

- `$ARGUMENTS` = Feature description, review file, or existing plan
- `--depth quick|standard|deep` = Planning depth (auto-detected)
- `--existing` = Enhance an existing plan with deeper research

## Workflow

1. **Gather context** — File path (skip to agents), clear
   description, or vague/fuzzy (needs clarification)
2. **Clarify if vague** — Ask questions ONE at a time
3. **Detect depth** — Auto-detect quick/standard/deep
4. **Runtime context** (Tidewave) — Gather live schemas, routes,
   and warnings before spawning agents (see planning-orchestrator)
5. **Spawn research agents** — Selective, parallel, based on need.
   Create a Claude Code task per agent for progress visibility:
   `TaskCreate({subject: "{Agent} research", activeForm: "Researching..."})`,
   mark `in_progress` on spawn, `completed` when done
6. **Wait for ALL agents** — Do NOT proceed until all return
   "completed". NEVER write plan while any agent is still running
7. **Breadboard** (LiveView) — System map for multi-page features
8. **Completeness check** — MANDATORY when planning from review
9. **Split decision** — One plan or multiple, concrete options
10. **Generate plan** — Checkboxes, phased tasks, code patterns
11. **Self-check** (deep only) — Three questions in Risks section
12. **Present and ask** — STOP, show summary, let user decide

**When planning from review**: Every finding must appear in the
plan — either as a task OR explicitly deferred by the user.

See `${CLAUDE_SKILL_DIR}/references/planning-workflow.md` for detailed step-by-step.

### --existing Mode (Deepening)

Enhances an existing plan instead of creating a new one:

1. Load plan, search `.claude/solutions/` for known risks
2. Spawn SPECIALIST agents (not Explore) for thin sections.
   Each agent writes to `.claude/plans/{slug}/research/` and
   returns only a 500-word summary. Same agent selection rules
3. Wait for ALL agents (mark tasks `completed` as each finishes)
4. Add implementation detail, resolve spikes, add verification
5. Present diff summary — **NEVER delete existing tasks**

## Iron Laws

1. **NEVER auto-start /phx:work** — Always present plan and ask
2. **Research before assuming** — Web-search unfamiliar tech
3. **Spawn agents selectively** — Only relevant, not all
4. **NEVER write plan while agents still running**
5. **NEVER skip input findings** — Every finding MUST have a task
6. **Do NOT spawn hex-library-researcher for existing deps**
7. **Skip research when planning from review/investigation** — When
   input is a review file or `/phx:investigate` output, the findings
   ARE the research. Do NOT spawn agents to re-discover what the
   review already found. Convert findings directly to plan tasks.
   (Confirmed: 56-session analysis showed same findings discovered
   3-4x across review→investigate→plan phases, wasting ~96K tokens)

## Integration with Workflow

```text
/phx:plan {feature}  <-- YOU ARE HERE
       |
   /phx:plan --existing (optional enhancement)
       |
   ASK USER -> /phx:work .claude/plans/{feature}/plan.md
       |
/phx:review → /phx:compound
```

## Notes

- Plans saved to `.claude/plans/{slug}/plan.md`
- Research reports in `.claude/plans/{slug}/research/` can be deleted after

## CRITICAL: After Writing the Plan

**STOP. Do NOT proceed to implementation.**

After writing `.claude/plans/{slug}/plan.md`:

1. Summarize: task count, phases, key decisions
2. Use `AskUserQuestion` with options:
   - "Start in fresh session" (recommended for 5+ tasks)
   - "Get a briefing" (`/phx:brief` — interactive walkthrough)
   - "Start here"
   - "Review the plan"
   - "Adjust the plan"
3. Wait for user response. Never auto-start work.

**When user selects "Start in fresh session"**, print:

```
1. Run `/new` to start a fresh session
2. Then run one of:
   /phx:work .claude/plans/{slug}/plan.md
   /phx:full .claude/plans/{slug}/plan.md  (includes review + compound)
```

This is Iron Law #1. Violating it wastes user context.

## References (DO NOT read — for human reference only)

- `${CLAUDE_SKILL_DIR}/references/planning-workflow.md` — Detailed step-by-step
- `${CLAUDE_SKILL_DIR}/references/plan-template.md`
- `${CLAUDE_SKILL_DIR}/references/complexity-detail.md`
- `${CLAUDE_SKILL_DIR}/references/example-plan.md`
- `${CLAUDE_SKILL_DIR}/references/agent-selection.md`
- `${CLAUDE_SKILL_DIR}/references/breadboarding.md`
