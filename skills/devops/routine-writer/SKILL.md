---
name: routine-writer
description: >
  · Write Claude Code routine prompts for schedules, APIs, and GitHub events. Triggers: 'routine', 'claude routine', 'scheduled claude task', 'unattended claude', '/schedule', '/fire'. Not one-off prompts: prompt-generator.
license: MIT
compatibility: "Routines require a Pro, Max, Team, or Enterprise plan with Claude Code on the web. CLI automation requires the claude binary on PATH"
metadata:
  source: iuliandita/skills
  date_added: "2026-04-14"
  effort: medium
  argument_hint: "<task-description-or-notes>"
---

# Routine Writer

Turn an unattended, repeatable task into a Claude Code routine: a saved prompt plus repositories, connectors, and triggers that runs on Anthropic cloud infrastructure without needing a local machine. Output is a self-contained prompt plus the artifacts to wire it up (a `/schedule` CLI command when available, a `curl` template for the `/fire` endpoint, or a web-UI walkthrough).

**Why routines differ from chat prompts.** A routine runs as a full autonomous Claude Code cloud session. There is no permission-mode picker, no approval prompts, and no human to answer clarifying questions mid-run. A prompt that works fine in a conversation can stall or misfire silently inside a routine because the model has no one to ask. Every routine prompt must be self-contained, state its success criteria, and declare where output goes.

**Research preview context** (May 2026 recheck): routines ship under the beta header `experimental-cc-routine-2026-04-01`. Behavior, limits, and the API surface can change. Pin any beta header references to that value and date so staleness is detectable.

## When to use

- User wants to turn a recurring task into a routine ("every night", "when a PR opens", "after each deploy")
- User says "make this a routine", "schedule this", "run this on autopilot", "put this on cloud"
- Refining an existing routine prompt that is firing but producing poor output
- Wiring an alerting tool, CD pipeline, or webhook to fire a routine via HTTP
- Picking between a schedule, API, GitHub event trigger, or a combination
- Writing the `/schedule` invocation for a scheduled routine from inside Claude Code
- Generating a `curl` template for an existing routine's API trigger

## When NOT to use

- Structuring a one-off prompt for chat or documentation (use **prompt-generator**)
- Polling or waiting inside an open CLI session (that's `/loop`, see the built-in scheduled-tasks docs)
- Desktop scheduled tasks that run on the user's machine with local file access (that's a different product surface)
- Writing the skill file itself rather than the prompt (use **skill-creator**)
- Code review, bug review, or security audit of the routine's target repo (use **code-review**, **security-audit**)
- CI pipeline design (use **ci-cd**) - routines can be triggered from CI but don't replace it
- GitHub Actions workflows (use **ci-cd**) - routines complement them, the routine is called from an Action
- Tasks that inherently need mid-run human judgment (design decisions, scope calls, UX review). Routines cannot pause to ask. If the task's right answer depends on context only a human can supply at run time, it is not a routine - push back and suggest `/loop` or an interactive session instead.

---

## AI Self-Check

Routines are high-stakes: they run unattended, consume daily allowance, and can open PRs or post to Slack without review. Before returning any routine prompt, verify:

- [ ] **Self-contained**: no "ask me" / "clarify with the user" / "if unclear" instructions. The routine cannot ask anything.
- [ ] **Trigger-aware context**: the prompt names how it was triggered and what input it receives (a scheduled wakeup with no args; an API call with a `text` payload; a GitHub event with a PR number). Scheduled routines especially need a "work since last run" framing.
- [ ] **Explicit success criteria**: the prompt states what "done" looks like for this run. Not "improve the code" but "open one PR with passing tests" or "post a one-line summary to #releases".
- [ ] **Idempotent no-op**: handles "nothing to do" cleanly. A nightly docs sweep with no stale docs should exit quietly, not invent work.
- [ ] **Output destination named**: where results land is stated explicitly (PR against `main`, Slack message in `#eng-bot`, Linear issue with label `auto-triage`, a summary comment on the PR).
- [ ] **Scope declared in config**: repositories, connectors, environment variables, and branch policy match what the prompt actually uses. Nothing extra.
- [ ] **Branch policy matches intent**: default is `claude/*` prefix only. If the prompt expects to push to other branches, **Allow unrestricted branch pushes** is documented as a required toggle.
- [ ] **Safety rail present**: what the routine should NOT do (no force-push, no protected-branch changes, no destructive ops, no new connectors, no credential exfil).
- [ ] **No injected slop**: no "certainly", "I'd be happy to", "great question", no ALL CAPS emphasis, no filler preamble. Calm imperatives only.
- [ ] **Cron interval >= 1 hour**: scheduled triggers under one hour are rejected by the platform.
- [ ] **Beta header pinned with date**: prose mentions of `experimental-cc-routine-2026-04-01` carry the header date so future readers can scan for staleness. Inside code blocks the header string itself carries the date, so no parenthetical is needed.
- [ ] **No tokens in output**: environment variable placeholders only. Never paste a real `sk-ant-oat01-...` value.
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **API surface checked**: routine headers, beta names, schedule syntax, and event payloads match current official docs
- [ ] **Unattended risk bounded**: permissions, spending, mutation scope, and notification paths are explicit

---

## Performance

- Keep scheduled jobs narrow; split broad routines into independently observable tasks.
- Set output contracts so downstream automation reads small structured results instead of transcripts.
- Throttle polling and retries to avoid unnecessary API or CI load.


---

## Best Practices

- Use least-privilege tokens and separate credentials per routine.
- Make failure modes visible with logs, alerts, and idempotent retry behavior.
- Pin beta headers with dates and revisit them during maintenance refreshes.


## Workflow

### Step 1: Capture the unattended task

Parse the user's description for:

- **Trigger intent**: "every night", "on each PR", "after deploy", "when Sentry fires", "weekly on Fridays"
- **Input to the run**: scheduled (nothing; compute "since last run"), API (freeform `text` payload, up to 65,536 chars), GitHub (event metadata for the matching PR/push/issue)
- **Action**: concrete verbs - read, scan, label, open PR, post, port, correlate
- **Output destination**: PR, comment, Slack channel, Linear issue, release-channel message
- **Scope**: repositories touched, connectors needed (Slack, Linear, Asana, Google Drive), env vars required
- **Safety boundaries**: what should never happen (no pushes to `main`, no force pushes, no destructive ops)

If the user is already inside a Claude Code session and says "make *this* a routine", extract the task from the conversation context. Do not invent fields they did not imply.

### Step 2: Pick trigger(s)

A single routine can combine trigger types. Use this table to route:

| Intent | Trigger | Notes |
|---|---|---|
| Recurring time-based work | Schedule | 1-hour minimum interval; presets (hourly, daily, weekdays, weekly) or custom cron via `/schedule update` |
| Fired from an external system (alert, deploy, CI failure) | API | Per-routine bearer token, beta header required, 65,536-char `text` payload |
| React to repository activity (PR opened, issue created, push) | GitHub | Needs Claude GitHub App installed; supports filters on author, branch, labels, draft state, etc. |
| Multiple firing modes for the same work | Combine | A PR review routine can run nightly, fire from deploy scripts, and react to every PR |

Read `references/trigger-guide.md` for full cron rules, the GitHub event catalogue, pull request filter fields, stagger behavior, and the hourly webhook caps.

### Step 3: Declare scope

Ask (or infer from context) and record:

- **Repositories**: which repos get cloned. Each is cloned on every run from the default branch.
- **Branch policy**: default is pushes limited to `claude/*` branches. If the routine legitimately needs to push elsewhere (e.g., docs updates to `main`), flag that the user must enable **Allow unrestricted branch pushes** per-repo. Default to leaving it off and have the routine open PRs instead.
- **Connectors**: minimal set. All connected MCP connectors are included by default; remove anything the routine does not actually use.
- **Environment**: network access level, env vars (API keys, tokens), setup script. Custom environments must be created before the routine references them.

Scope each to what the routine actually needs. Routines act under the user's connected identity - commits, PRs, and Slack messages appear as that user.

### Step 4: Draft the prompt using the six-block template

Build the prompt with these six blocks in order. Block titles are for the author (you); the finished prompt can flow as prose or use subheadings when the task is complex.

1. **Context**: when and why this runs, what fires it
2. **Input scope**: what the run should read (and, for schedules, the "since last run" framing)
3. **Steps**: concrete sequenced actions
4. **Success criteria**: what a successful run produces
5. **Output destination**: where results land (PR target, channel, issue tracker)
6. **Safety rail**: what this run must not do; conditions under which to abort cleanly

Read `references/prompt-anatomy.md` for the full template, three worked examples (one per trigger type), idempotency patterns, and how to branch on trigger context when a routine combines schedule, API, and GitHub.

**Complexity rule**: match structure to the task. A single-action nightly summariser gets one paragraph of prose. A multi-step library-port routine gets subheadings per block. Over-structured simple routines waste tokens and drift into slop.

### Step 5: Present for review

Show the user:

1. The drafted routine prompt
2. The trigger config (cron expression or preset / API setup / GitHub event and filters)
3. The scope (repos + branch policy, connectors, env vars, environment choice)
4. Any assumptions you made

**Do not emit automation artifacts yet.** Wait for approval. On edits, revise in place rather than rewriting from scratch.

### Step 6: Emit artifacts

After approval, emit the right artifacts for the chosen trigger(s):

- **Scheduled**: if `claude` is on PATH, a `/schedule` CLI invocation. Otherwise a web-UI walkthrough with the prompt copy-paste ready.
- **API**: a `curl` template for the `/fire` endpoint (with env var placeholders for token and URL), plus a GitHub Actions step when the user is wiring this from CI.
- **GitHub**: a web-UI walkthrough (this trigger type is configured from the web only).
- **Combined**: the scheduled `/schedule` command first (to create the routine), then a web-UI walkthrough for adding API / GitHub triggers to that routine.

Read `references/automation.md` for the harness detection logic, the exact `/schedule` invocation patterns, the `/fire` curl template with the current beta header, and GitHub Actions failure-hook patterns.

---

## Harness detection

Only emit `/schedule` instructions when the `claude` CLI is actually available. Routines can be created only from the web UI, the Desktop app, or `claude`'s `/schedule` command - Codex, OpenCode, Cursor, and other harnesses do not create routines.

Detection logic to run before emitting CLI artifacts:

```bash
if command -v claude >/dev/null 2>&1; then
  # claude binary present - /schedule CLI is available for scheduled routines
  # (API and GitHub triggers still need the web UI)
  HAS_CLAUDE=1
else
  HAS_CLAUDE=0
fi
```

When `HAS_CLAUDE=0`, do not print `/schedule` instructions. Provide the web-UI walkthrough at `claude.ai/code/routines` and print the finished prompt for copy-paste.

Detecting the *running* harness is a weaker signal than binary presence, since a user in Codex might still have `claude` installed. Binary presence is the right gate.

See `references/automation.md` for a fuller detection pattern that also checks for valid credentials before assuming the `/schedule` command will work.

---

## Skill Output

When the skill finishes, the user should have, depending on triggers chosen:

1. **The routine prompt** (always), ready to paste at [claude.ai/code/routines](https://claude.ai/code/routines) or into the `/schedule` CLI
2. **The trigger config**: cron expression or preset name, event + filters for GitHub, URL + token placeholder for API
3. **The scope block**: repos with branch policy, connectors to include, env vars and environment, network access level
4. **Automation artifacts** for each chosen trigger (see Step 6)
5. **Post-setup steps**: any follow-ups the user must do in the web UI (API token generation, GitHub App install, environment creation)

---

## Minimal emitted-artifacts example

For a scheduled nightly triage routine on a machine where `claude` is on PATH, the user gets three things back:

1. The routine prompt (from Step 4, drafted and approved in Step 5).

2. The `/schedule` invocation to paste into Claude Code:

   ```
   /schedule Run every weekday at 07:00 local. Read issues opened in the last 24 hours in myorg/api without the auto-triaged label. Apply area and auto-triaged labels, assign owners from CODEOWNERS, and post a Slack summary in #eng-backlog. If no issues match, exit without output.
   ```

3. The `/fire` curl template (after the user adds an API trigger in the web UI and stores the token as `$ROUTINE_FIRE_TOKEN`):

   ```bash
   curl -X POST "$ROUTINE_FIRE_URL" \
     -H "Authorization: Bearer $ROUTINE_FIRE_TOKEN" \
     -H "anthropic-version: 2023-06-01" \
     -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
     -H "Content-Type: application/json" \
     -d '{"text": "Manual re-fire after CODEOWNERS refresh"}'
   ```

API-only and GitHub-only routines skip artifact #2 and emit a web-UI walkthrough instead. See `references/automation.md` for the full emit matrix.

---

## Reference Files

- `references/trigger-guide.md` - schedule, API, and GitHub trigger rules, filters, limits, and payload shapes.
- `references/prompt-anatomy.md` - six-block prompt template, idempotency patterns, and worked examples.
- `references/automation.md` - `/schedule`, `/fire`, GitHub Actions, and web-UI artifact patterns.

---

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** ROUTINE-WRITER
- **Deliverable bucket:** `deliverables`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content (e.g., review an existing routine for quality), emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/deliverables/routine-writer/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content** (its primary mode, producing a routine for the user), respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **prompt-generator** - structures one-off prompts for chat or documentation. Prompts written with prompt-generator can be refined with user feedback mid-run; routine prompts cannot, which is why this skill exists.
- **skill-creator** - creates reusable skill files (SKILL.md). Routines are not skills; routines are saved Claude Code configurations. A routine can call skills that are committed to its cloned repository, but the routine itself is not one.
- **ci-cd** - designs CI pipelines. A CI job can call a routine via the `/fire` endpoint, and a routine can react to CI webhooks. Use ci-cd for the pipeline and this skill for the routine it calls.
- **mcp** - builds MCP servers. Routines use MCP connectors; this skill does not build the connector, it declares which connectors the routine needs.
- **git** - PR / branch / release workflows. Routines typically produce PRs; `git` covers local and multi-forge git operations, this skill covers the unattended cloud session that opens them.

---

## Rules

1. **Self-contained only.** A routine prompt must never contain "ask the user", "clarify with", "if unclear, confirm". The routine has no one to ask. If the task is ambiguous, resolve it at draft time, not at run time.
2. **Explicit success criteria.** Every routine prompt states what a successful run produces, in terms of concrete artifacts (a PR, a message, an issue, a summary comment). "Improve the code" is not a success criterion.
3. **Idempotent no-op.** Every scheduled or webhook-driven routine handles "nothing to do" cleanly by exiting without producing output. Routines that invent work on empty inputs burn daily allowance.
4. **Minimum scope.** Declare only the repos, connectors, and env vars the prompt actually uses. Each connector is attack surface; each extra repo is extra clone time.
5. **Branch policy off by default.** Do not recommend enabling **Allow unrestricted branch pushes** unless the prompt genuinely needs to write outside `claude/*`. Prefer opening PRs.
6. **Never embed tokens.** Every `Authorization: Bearer` in emitted artifacts uses an env var placeholder (`$ROUTINE_FIRE_TOKEN`). Tokens are shown once in the web UI and cannot be retrieved - emitting a real one in the conversation exposes it.
7. **Never auto-run `/schedule`.** Emit the command for the user to paste or confirm. Routines count against the daily allowance; the skill never consumes that allowance autonomously.
8. **Pin the beta header with its date in prose.** Prose mentions of `experimental-cc-routine-2026-04-01` carry the header date so a reader scanning the docs can spot staleness without parsing the header string. In code blocks the header string itself contains `2026-04-01`, so no extra annotation is needed. The two most recent prior header versions keep working for migration.
9. **Detect before emitting.** Before printing `/schedule` instructions, verify `claude` is on PATH. If not, emit the web-UI walkthrough instead.
10. **Run the AI Self-Check.** Every routine prompt returned to the user passes the checklist above first.
