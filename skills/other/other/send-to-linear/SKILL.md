---
name: send-to-linear
description: >
  Extract actionable Linear tickets from ambiguous input — Slack conversations, call transcripts,
  screenshots, meeting notes, or any unstructured material. Proposes tickets in a scratchpad file
  for user review, then creates them in Linear on approval. Use when the user wants to turn
  conversations, transcripts, screenshots, or notes into Linear tickets. Also use when user says
  "create tickets from this", "send to linear", "make issues from this call/chat", or provides
  raw material and asks for tickets.
user-invocable: true
---

# Send to Linear

Turn unstructured input into well-structured Linear tickets.

## Setup

### Config resolution

Look for team configuration in this order (first match wins):

1. `~/.claude/skills/send-to-linear/references/config.local.json`
2. `~/.agents/skills/send-to-linear/references/config.local.json`
3. `references/config.json` (bundled defaults, relative to this skill file)

Use the first `.local` config found. Otherwise fall back to the bundled `config.json`.

If no `.local` file exists anywhere AND the bundled config has empty required fields (`team`, `default_assignee`), **stop and prompt the user**:

> No local config found. The bundled `references/config.json` has empty defaults and will be overwritten whenever this skill updates.
>
> Create a local override at one of these paths:
> - `~/.claude/skills/send-to-linear/references/config.local.json`
> - `~/.agents/skills/send-to-linear/references/config.local.json`
>
> Copy the bundled `references/config.json` as a starting point and fill in your team, project, assignee, labels, and conventions.

### Template resolution

Same pattern for the ticket template:

1. `~/.claude/skills/send-to-linear/references/ticket-template.local.md`
2. `~/.agents/skills/send-to-linear/references/ticket-template.local.md`
3. `references/ticket-template.md` (bundled default)

The template rarely needs customization, so no prompt if only the bundled version exists.

## Phase 1: Ingest Input

Accept any combination of:

- **Slack dump** — pasted messages or fetched via Slack MCP tools
- **Call transcript** — from Fireflies (`mcp__fireflies__*` tools), pasted text, or a file
- **Screenshots** — read image files with the Read tool
- **Meeting notes / docs** — any markdown, text, or document content
- **User description** — freeform "we need X, Y, Z"

If the user's input is ambiguous or incomplete, ask one clarifying question before proceeding. Do not over-interrogate.

For Fireflies transcripts specifically: fetch both the summary (`fireflies_get_summary`) and full transcript (`fireflies_get_transcript`). Use the summary for topic identification, the full transcript for detail extraction.

## Phase 2: Extract Topics and Actionable Items

For **short input** (<5K chars): extract directly in the main context.

For **long input** (>5K chars, e.g. full call transcripts): launch parallel subagents, one per major topic or time segment, to extract:

1. **Concrete examples and use cases** — the most critical output. Capture specific scenarios, companies/tickers, KPIs, exact quotes, timestamps, and reasoning chains. A ticket saying "fix interpretation errors" is useless. A ticket saying "fix interpretation errors — e.g., when commentary says 'flat to down' for Intel CapEx but consensus expects 'down', recognize this as upward revision" is actionable.
2. **Feature requirements** — what needs to be built or changed
3. **Limitations/boundaries** — things explicitly ruled out
4. **Acceptance criteria** — testable conditions

### Categorize items as:

- **Actionable tickets** — clear scope, can be worked on immediately
- **Ideas / needs more thought** — visionary or exploratory, tracked but not immediately actionable

## Phase 3: Draft Tickets to Scratchpad

Write to `.claude/scratchpad/linear-tickets-YYYY-MM-DD.md` using the format from `references/ticket-template.md`.

Every ticket with a real-world example from the source MUST include that example verbatim — do not summarize away specifics.

## Phase 4: Verification (for long-form input only)

Skip for short/simple input. For call transcripts or long Slack threads:

Launch a verification subagent that reads the full source material and the drafted tickets, then produces a gap list:
- Use cases mentioned but missing from tickets
- Action items assigned to people but not captured
- Design decisions agreed upon but not in acceptance criteria
- Any "we need to do X" statements not in any ticket

Update the draft with any gaps found.

## Phase 5: User Review

**STOP.** Tell the user the file is ready and wait for explicit instruction before creating anything in Linear.

The user may restructure, merge, split, rename, add notes, or tell you to skip items. Apply all feedback to the scratchpad file before proceeding.

## Phase 6: Create in Linear (only on explicit approval)

Read config using the resolution order from Setup, then:

1. `mcp__linear__list_teams` — resolve team ID
2. `mcp__linear__list_issue_labels` — resolve label IDs
3. `mcp__linear__list_projects` — resolve project ID (if configured)
4. `mcp__linear__list_cycles` with `type: "current"` — resolve current cycle (if `assign_to_current_cycle` is true)

Create each approved ticket with `mcp__linear__create_issue`:
- `team`: from config
- `project`: from config
- `assignee`: from config
- `cycle`: current cycle number
- `state`: from config `default_status`
- `labels`: matched from ticket's Labels field
- `title`: from ticket
- `description`: full ticket body in markdown
- `links`: source link if available (e.g. Fireflies transcript URL, Slack permalink)

Report created ticket identifiers back to the user.

## Key Rules

1. **Concrete examples are non-negotiable.** Engineers understand what to build from specific scenarios, not abstract descriptions. Preserve full reasoning chains, exact quotes, and real-world context.
2. **Never create tickets without user approval.** Always draft to scratchpad first.
3. **Config is defaults, not constraints.** User can override team, assignee, labels, or any other field per invocation.
4. **Don't over-consolidate.** If two items are independent work, they're separate tickets. Group only when items are truly part of the same deliverable.
5. **Standalone requirements buried in conversation are tickets too.** Things said in passing like "we also need to compare dates" represent distinct work items.
