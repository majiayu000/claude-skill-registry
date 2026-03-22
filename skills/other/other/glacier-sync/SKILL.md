---
name: glacier-sync
description: >
  Optional skill. Syncs work tracking between the current repo and Glacier board.
  Auto-invoke after branch creation (step 1 of implement workflow), PR open, PR merge,
  or when the user mentions board sync, card status, or Glacier tracking.
  Only activates when GLACIER_ENABLED=true, GLACIER_WORKSPACE_ID, and GLACIER_PROJECT_ID are set in the environment.
  If the skill is not enabled or env vars are absent, skip silently — never fail the workflow.
---
# Glacier Sync

Keep the Glacier board in sync with development activity. This skill bridges GitHub workflow events to Glacier cards via MCP.

**This skill is optional.** It enhances the workflow but is never required. If the skill is not loaded, not enabled, or environment variables are missing, the calling workflow (e.g. `/implement`) must continue without interruption.

## Configuration

Three environment variables in `.env.local` (already gitignored in Next.js projects):

```
GLACIER_ENABLED=true
GLACIER_WORKSPACE_ID=<uuid from Project Settings>
GLACIER_PROJECT_ID=<uuid from Project Settings>
```

The MCP server URL is hardcoded: `https://www.getglacier.ai/api/mcp`

Column IDs are resolved dynamically at runtime via `Glacier:list_columns` using column name matching. This keeps config minimal and avoids stale IDs if the board is restructured.

To get your IDs: open Glacier → Project Settings → copy the workspace ID and project ID.

## Activation

This skill only activates when **all** conditions are met:
1. The `glacier-sync` skill is enabled in the current Claude Code session
2. `GLACIER_ENABLED` is `true`
3. `GLACIER_WORKSPACE_ID` is set
4. `GLACIER_PROJECT_ID` is set

If any condition is not met, skip silently — do not prompt the user to configure anything. Do not error. Do not block the workflow.

## MCP call pattern

**Every** Glacier MCP tool call must include `workspace_id` from the `GLACIER_WORKSPACE_ID` env var. This is required because OAuth tokens are user-scoped (not workspace-scoped). Omitting it will cause the call to fail.

Example: `Glacier:list_columns(project_id: $GLACIER_PROJECT_ID, workspace_id: $GLACIER_WORKSPACE_ID)`

Do NOT call `Glacier:list_workspaces` to discover the workspace ID — it is always provided via env var.

## Auto-invoke triggers

This skill should fire automatically at these workflow moments **if activated**:

| Trigger | When | Action |
|---------|------|--------|
| **Branch creation** | Step 1b of `/implement` workflow | Move linked card → **In Progress** |
| **PR opened** | After `gh pr create` (step 9b) | Move linked card → **In Review** |
| **PR merged** | After PR merge confirmed | Move linked card → **Done** |
| **Manual** | User runs `/glacier-sync` | Interactive menu (see Capabilities §3) |

If any trigger fails (MCP unreachable, card not found, skill not loaded), log a one-line warning and continue. Never block the parent workflow.

### Branch creation → In Progress (the key transition)

This is the most important auto-trigger for accurate cycle time tracking. When the implement workflow creates a feature branch:

1. Parse the issue reference from the user's request (e.g. "implement #42")
2. Find the matching Glacier card (see Card matching strategy below)
3. Resolve column IDs: call `Glacier:list_columns` with `project_id` and `workspace_id` from env, match by column name
4. Check the card's current column:
   - If in **Backlog** or **Ready** → move to **In Progress**
   - If already in **In Progress** or later → do nothing (don't regress)
5. Check WIP limit on In Progress column before moving. If at limit, **warn the user** and ask whether to proceed
6. Report: `Moved card "<title>" → In Progress (branch feat/issue-42 created)`

**Why this matters:** Cycle time in Kanban is measured from when work enters the first active column to when it reaches Done. Moving the card at branch creation — not at spec approval, not at PR merge — gives accurate lead time data. The Ready column represents "approved and waiting to be pulled"; In Progress represents "someone is actively working on it."

### PR opened → In Review

After `gh pr create` succeeds:
1. Match the PR's linked issue to a Glacier card
2. If card is in **In Progress** → move to **In Review**
3. If card is already in **In Review** or **Done** → do nothing
4. Report: `Moved card "<title>" → In Review (PR #87 opened)`

### PR merged → Done

After PR merge is confirmed:
1. Match the merged PR's linked issue to a Glacier card
2. If card is not already in **Done** → move to **Done**
3. Report: `Moved card "<title>" → Done (PR #87 merged)`

## Capabilities

### 1. Card status sync (after PR merge or branch work)
- When a PR is merged, check if any linked Glacier cards should move to Done
- Match cards by GitHub issue link on the card (see matching strategy)
- Use `Glacier:list_cards` → find matching card → `Glacier:update_card` to move column
- Always pass `workspace_id` from env to every MCP call

### 2. Card creation from TODOs
- When the user asks to "sync TODOs" or "create cards from issues":
  - Scan for `// TODO(glacier):` comments in files changed on the current branch (`git diff --name-only main...HEAD`)
  - Create cards via `Glacier:create_card` with the TODO text as title
  - Report created cards with their IDs

### 3. Board status report
- When the user asks "what's on the board" or "board status":
  - Use `Glacier:list_columns` → `Glacier:list_cards` for the configured project
  - Report: cards per column, WIP limit status, any blockers
  - Flag columns at or over WIP limit

### 4. Link GitHub issues to cards
- After creating a GitHub issue from Claude Code, offer to link it to an existing or new Glacier card
- Use `Glacier:link_card_to_github` with the issue URL

## Column resolution

Columns are resolved by name at runtime, not stored in config:

1. Call `Glacier:list_columns` with `project_id` and `workspace_id` from env
2. Match column names case-insensitively: "Backlog", "Ready", "In Progress", "In Review", "Done"
3. Cache the mapping for the duration of the session (don't call `list_columns` on every trigger)

Default transition mapping:

| GitHub event          | Glacier transition              |
|-----------------------|---------------------------------|
| Branch created        | Ready / Backlog → In Progress   |
| PR opened             | In Progress → In Review         |
| PR merged             | In Review → Done                |
| PR closed (not merged)| No change (notify only)         |

## Card matching strategy

When looking for the Glacier card to move, try these in order:

1. **GitHub issue link** — use `Glacier:get_card_github_status` to check if a card links to the issue being implemented. This is the most reliable match.
2. **Issue number in branch name** — branch contains `issue-42` or `#42`, match against cards with GitHub issue #42 linked
3. **Title match** — fuzzy match between issue title and card title (last resort, ask for confirmation)

Note: Human-readable card IDs (e.g. `GLACIE-42`) are not yet available — branch name prefix matching will be added when issue #136 ships.

If no match is found, ask the user: "I couldn't find a Glacier card for this work. Want me to create one?"

## MCP tools used

All tools require `workspace_id` parameter from `GLACIER_WORKSPACE_ID` env var.

- `Glacier:list_projects` — verify project exists (fallback/validation only)
- `Glacier:list_columns` — get column IDs and WIP status by name
- `Glacier:list_cards` — find cards by project or column
- `Glacier:get_card` — check card details and linked docs
- `Glacier:get_card_github_status` — verify GitHub issue/PR links on a card
- `Glacier:update_card` — move cards between columns
- `Glacier:create_card` — create new cards from TODOs
- `Glacier:link_card_to_github` — link cards to GitHub issues/PRs

## Rules

- **Always pass `workspace_id`** from env to every Glacier MCP call. Never omit it.
- Never move a card without confirming the match is correct. If ambiguous, ask the user.
- Never create duplicate cards — check existing cards by title before creating.
- Always report what was synced: card title, action taken, column.
- Respect WIP limits — if the target column is at limit, warn instead of moving.
- Keep output concise: card title, action, column. No verbose summaries.
- Never regress a card (e.g. don't move from In Review back to In Progress).
- **Never block the parent workflow.** If anything fails, warn and continue.
