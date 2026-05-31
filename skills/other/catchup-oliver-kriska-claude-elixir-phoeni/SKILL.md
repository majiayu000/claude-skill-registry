---
name: catchup
description: "Summarize and review what changed while you were away. Use after a weekend, vacation, or flight to check missed PRs, git commits, Linear tickets, and meetings — one prioritized brief, not a firehose."
effort: medium
disable-model-invocation: true
argument-hint: "[--since \"friday\"|\"2h\"|\"last-active\"|\"last-commit\"] [--scope repo|all] [--sources github,git,linear,calendar] [--depth quick|standard|deep] [--focus prs,reviews-requested,mentions,impact]"
allowed-tools: Read, Grep, Glob, Bash, Write, WebFetch, Agent
---

# Catchup — Async-Team Return Briefing

You've been away. This skill is a **thin orchestrator**: it resolves
the window + sources here, then delegates the I/O fan-out, impact
analysis, and brief assembly to the `catchup-runner` agent (Sonnet) so
your (often Opus) session does not pay for summarization. You only
print what the agent returns.

## Usage

```
/catchup                                  # since you were last active
/catchup --since "friday"
/catchup --since "2h" --focus reviews-requested
/catchup --since last-commit --depth deep
/catchup --scope all                      # include cross-repo pings/reviews
```

Default is **repo-scoped**: every GitHub signal (reviews requested,
notifications, mentions) is filtered to the repo you ran it in. Pass
`--scope all` to also include cross-repo activity, which is then listed
in its own separate section — never mixed into this repo's lists.

## Iron Laws

1. **Delegate the heavy work** — spawn `catchup-runner` (sonnet) for
   fan-out + assembly. Do NOT run the `gh`/`git` fan-out in this
   session; that defeats the cost/speed purpose.
2. **Resolve the window here, once** — the agent must never re-resolve
   it. Pass absolute `SINCE_*` values.
3. **MCP runs here, not in the agent** — Linear/Calendar MCP tools are
   unreliable in subagents. If present, fetch in this context and pass
   the text to the agent; else mark absent.
4. **Validate `--since` before any shell** — match the grammar; on no
   match fall back to 24h and note the assumption.
5. **Stop after the brief** — print the agent's summary, never
   auto-transition to another command.
6. **Repo-scoped by default** — pass `SCOPE=repo` unless the user
   passed `--scope all`. A brief run inside one repo must not leak
   another repo's reviews/notifications. Cross-repo is opt-in only.

## Workflow

### 1. Parse arguments

From `$ARGUMENTS`: `--since`, `--scope`, `--sources`, `--depth`,
`--focus`. Defaults: `--since last-active`, **`--scope repo`**, all
detected sources, `--depth standard`, no focus. `--scope` accepts
`repo` (default — every GitHub signal filtered to the current repo) or
`all` (cross-repo allowed, listed in its own section).

### 2. Resolve the time window (here, in this context)

Read `${CLAUDE_SKILL_DIR}/references/time-window.md`. Resolve calendar
words (`friday`, `yesterday`, a date) in the **user's local timezone**
(this machine = the user's TZ), pivot through `SINCE_EPOCH`, derive
`SINCE_ISO` (UTC) + `SINCE_LABEL` (with TZ abbrev) + `LOCAL_TZ`.

Default `last-active` = MAX of: newest Claude session mtime for this
repo, your last own commit (`git log --author=<you> -1 --format=%ct`),
your last own PR **in this repo** (`gh pr list --repo <repo> --author
@me --state all`, repo-scoped — a global search would anchor to other
repos). The latest footprint is "you were last here". Record which
signal won. Variants: `last-session` (sessions only),
`last-commit`/`last-mine` (your git/PR only). No signal → 24h, noted.

### 3. Detect sources + pull MCP data (here)

```
gh:   command -v gh && gh auth status               → github ON
git:  git rev-parse --is-inside-work-tree           → git ON
linear/calendar: a Linear / Google-Calendar MCP tool present?
```

If Linear/Calendar MCP is present, query it **in this context now**
(assigned/updated tickets since `SINCE_ISO`; missed + today's
meetings in `LOCAL_TZ`) and keep the short text as `LINEAR_DATA` /
`CALENDAR_DATA`. If absent, set them to `absent` (the agent will
proxy-harvest `XXX-####` refs for Linear; skip calendar with a note).

### 4. Delegate to `catchup-runner` (Sonnet)

Spawn one agent, foreground, passing a self-contained prompt:

```
Agent(subagent_type: "catchup-runner", prompt: """
SINCE_EPOCH={…}  SINCE_ISO={…Z}  SINCE_LABEL="{… local TZ}"
LOCAL_TZ={…}  SOURCES={github,git}  SCOPE={repo|all}  DEPTH={…}  FOCUS={…}
OUT_PATH={cwd}/.claude/catchup/brief-{YYYY-MM-DD}.md   # local date (date +%F), not UTC
LINEAR_DATA={text or "absent"}
CALENDAR_DATA={text or "absent"}
Window anchor signal: {which one won, for the Risks note}
Do the gh+git fan-out, impact analysis, and brief assembly per your
instructions. Write the file. Return ONLY the inline summary.
""")
```

The agent inlines all recipes (it cannot read this plugin's
references). Do not re-implement its work here.

### 5. Present + stop

Print the agent's returned summary verbatim and the brief path.

**If the agent returned no summary** (e.g. it hit its turn budget
mid-assembly — the brief file is usually already written): do NOT
re-summarize the brief yourself; that pulls the expensive step back
into this (often Opus) session, defeating the delegation. Instead
`SendMessage` the agent by the `agentId` from its stop usage:
*"Return only the inline summary now."* — it finishes cheaply in
Sonnet. Only if that also fails, read the brief's Intent + Top
priorities section (not the whole file) and print that.

**Do NOT** auto-invoke any other command. The user decides what's
first.

## Sources at MVP

GitHub (`gh`), Git (`git`), Linear MCP (optional), Google Calendar MCP
(optional). Slack/Gmail are **v2 opt-in** — never queried, never piped
raw. Scheduling + per-project config are designed in
`${CLAUDE_SKILL_DIR}/references/config-schema.md`, not built at MVP.

## Graceful degradation contract

A missing source degrades the brief, never breaks it. `git log` alone
(always available in a repo) is a valid minimum brief. Every absent or
failed source becomes one honest line under the brief's
Risks/assumptions block, so the reader knows what it does *not* cover.
