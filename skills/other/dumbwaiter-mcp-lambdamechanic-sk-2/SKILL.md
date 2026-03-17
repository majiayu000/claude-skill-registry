---
name: dumbwaiter-mcp
description: Provider-agnostic wait-for-change skill that uses the Dumbwaiter MCP server to wait on PR events (GitHub first) via wait.start/status/cancel/await, with progress notifications and durable state.
---

# Dumbwaiter MCP: Wait-for-Change

Goal: give Claude a single, stable way to “wait until X happens” on a code host (GitHub now; GitLab next). This skill teaches Claude when and how to use the Dumbwaiter MCP server’s tools.

Prerequisites
- Server: this repo builds a stdio MCP server (`cargo build && target/debug/dumbwaiter-mcp`).
- Auth: `export GITHUB_TOKEN=…` (repo read permissions are sufficient for commit statuses).
- Persistence (optional): `DUMBWAITER_DB` to override `./state/dumbwaiter.sqlite`.
- Await settings (optional): `DUMBWAITER_AWAIT_TTL_SECS` (default 900), `DUMBWAITER_WATCHER=1` to enable background polling.

When to use this skill
- You need to pause orchestration until PR checks turn green, a PR is merged, or checks fail.
- You want durable waits with a `wait_id`, cancellable and recoverable after restarts.
- You want progress updates visible to the host via MCP `notify_progress`.

Tools overview
- `wait.start` → returns `{ wait_id }` for a condition on a selector
- `wait.status` → returns current state: `pending|satisfied|failed|timeout|cancelled|unknown`
- `wait.cancel` → cancels a pending wait
- `wait.await` → polls provider with exponential backoff; emits progress notifications; resolves to terminal state or timeout

Selectors and conditions (GitHub)
- selector: `{ "owner": "ORG", "repo": "REPO", "pr": 123 }`
- Supported `condition` tokens:
  - `checks_succeeded` — combined status success
  - `checks_failed` — combined status failure/error
  - `pr_merged` — merged flag true
  - `pr_approved` — at least one approved review
  - `changes_requested` — an open review with changes requested
  - `workflow_completed` — at least one completed workflow run
  - `comment_received` — any new PR comment/review/reaction event (see streaming section below)

For `comment_received`, optional `filters` refine which events count. If omitted, `since` defaults to the wait's `created_at` timestamp so Dumbwaiter streams everything posted after the wait was created.

Happy-path flow
1) Start wait
   - name: `wait.start`
   - arguments: `{ "provider": "github", "selector": {…}, "condition": "checks_succeeded" }`
   - capture `wait_id`
2) Await
   - name: `wait.await`
   - arguments: `{ "wait_id": "…" }`
   - Observe progress notifications; handle final result
3) Query or cancel as needed
   - `wait.status` or `wait.cancel`

Guidelines
- Prefer `wait.await` when a host can display progress; otherwise poll with `wait.status` on an interval < backoff cap (default 30s).
- Always report final state back to the orchestrator and link the `wait_id` in logs/notes.
- On auth errors or rate limits, surface a clear, actionable message; do not retry aggressively (respect backoff).
- On timeouts, return `timeout` with elapsed seconds; let the caller decide next steps.
- Security: never echo tokens; require least scopes.

## Streaming GitHub comment events

Set `condition` to `comment_received` plus optional filters:

```json
{
  "provider": "github",
  "selector": { "owner": "acme", "repo": "widgets", "pr": 42 },
  "condition": "comment_received",
  "filters": {
    "since": "2025-01-01T00:00:00Z",
    "include_bots": true,
    "author_allowlist": ["alice"],
    "author_denylist": ["bot"]
  }
}
```

`wait.await` emits `notify_progress` for every matching comment/review/reaction (body + URL + reaction counts + code context) before returning the terminal payload that mirrors the streamed events. Use this when an orchestrator needs to react to each individual discussion event.

Examples
- “Wait for PR 42 in acme/widgets until checks pass.”
  - start → `{ provider: "github", selector: { owner: "acme", repo: "widgets", pr: 42 }, condition: "checks_succeeded" }`
  - await → `{ wait_id }`
- “Stream every new comment on PR 42 since midnight UTC.”
  - start → `{ provider: "github", selector: { owner: "acme", repo: "widgets", pr: 42 }, condition: "comment_received", filters: { since: "2025-01-01T00:00:00Z", include_bots: true } }`
  - await → receives per-comment progress events plus the final summary payload

Troubleshooting
- `unknown` status: the `wait_id` was not found (DB purge or wrong project).
- No progress events: confirm host supports MCP notifications and server is connected.
- Auth failures: ensure `GITHUB_TOKEN` is set and valid for the target repo.
