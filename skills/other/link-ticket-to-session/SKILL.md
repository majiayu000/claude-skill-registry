---
name: link-ticket-to-session
description: Link the current Claude Code session to a ticket (Linear, Jira, GitHub Issues, or GitHub Pull Requests) and cache its title/status in karma. Use when the user explicitly asks to link, attach, associate, or connect this session to a ticket, issue, or PR — e.g. "/link-ticket-to-session ABC-123", "link this session to LINEAR-42", "associate this work with issue #15", "attach session to PR octocat/repo#7". Do NOT auto-invoke from passing ticket-key mentions in normal conversation.
argument-hint: <ticket-ref-or-url>
allowed-tools: Bash, mcp__linear, mcp__claude_ai_Linear, mcp__plugin_github_github, mcp__atlassian
---

You are linking the current Claude Code session (`${CLAUDE_SESSION_ID}`) to: **$ARGUMENTS**

Karma is a read-only observer on the user's machine. It stores the link
and caches title/status for display, but never writes back to the ticket
provider. You fetch metadata via the user's already-configured MCP server.

Karma's API URL comes from `KARMA_API_URL` (set by users on non-default
ports/hosts) with `http://localhost:8000` as fallback. Inline
`${KARMA_API_URL:-http://localhost:8000}` in **every** curl below — bash
variables don't persist across separate Bash tool calls, so a top-of-script
assignment would be empty by the time the next curl runs.

## Step 1 — Parse $ARGUMENTS

Recognized forms:

| Provider           | Short ref           | URL forms                                              |
|--------------------|---------------------|--------------------------------------------------------|
| Linear             | `LINEAR-123`        | `https://linear.app/.../issue/ABC-123`                 |
| Jira               | `PROJ-45`           | `https://*.atlassian.net/browse/PROJ-45`               |
| GitHub **Issue**   | `owner/repo#42`     | `https://github.com/owner/repo/issues/42`              |
| GitHub **PR**      | `owner/repo#42`     | `https://github.com/owner/repo/pull/42`                |

GitHub issues and pull requests share a single numbering namespace —
`owner/repo#42` could be either. **The URL kind (`/issues/` vs `/pull/`)
is the only signal**, and karma's backend preserves it, so when you have
a URL keep it intact when POSTing (Step 4). For a bare `owner/repo#N`
with no URL, default to `/issues/N` — GitHub auto-redirects to `/pull/N`
when N is actually a PR, so the link still resolves.

A bare `#N` (no owner/repo) is **not** accepted — always qualify with
`owner/repo#N`.

## Step 2 — Identify provider and (for GitHub) kind

Set two variables you'll use below:

- `<provider>` ∈ `linear` | `jira` | `github`
- For GitHub: `<kind>` ∈ `issue` | `pull_request` (derived from URL path)

For Linear and Jira this collapses to just `<provider>`.

## Step 3 — Fetch metadata via MCP (when available)

Pick the right MCP tool for the provider and kind:

| Provider · Kind             | MCP tool                                                |
|-----------------------------|---------------------------------------------------------|
| `linear`                    | Linear MCP — search/fetch issue by key                  |
| `jira`                      | Atlassian MCP — fetch by key                            |
| `github` · `issue`          | `mcp__plugin_github_github__issue_read`, method `get`   |
| `github` · `pull_request`   | `mcp__plugin_github_github__pull_request_read`, method `get` |

Calling the wrong GitHub method silently returns the wrong thing because
both shapes look superficially similar — so derive the kind first.

If the relevant MCP isn't installed, **skip this step** and proceed to
Step 4 without title/status. Karma will create the link; the title/status
fields stay NULL and can be refreshed later via Step 5.

Pull at minimum: `title`, `status` (or state), `url`. **Strip large
fields** — karma caps `metadata_json` at 64 KB and a full PR payload
easily exceeds that. Specifically drop:

- GitHub PR: `body`, `commits`, `files`, `reviewers`, `comments`, `labels`,
  `requested_reviewers`, `head` / `base` blobs beyond `ref`
- GitHub issue: `body`, `comments`, `reactions`, `labels`
- Linear / Jira: `description`, `comments`, `subscribers`, `attachments`

### Status semantics by kind

The `status` you cache should reflect *what the provider says now*, not a
generic "open/closed". Karma's UI normalizes these to canonical buckets
at render time, so faithful provider language is the right input:

- **Linear**: workflow state name verbatim — e.g. `Backlog`, `In Progress`,
  `In Review`, `Done`, `Cancelled` (workspace-defined; don't normalize).
- **Jira**: workflow state name — e.g. `To Do`, `In Progress`, `In Review`,
  `Done`.
- **GitHub issue**: `open` or `closed`.
- **GitHub PR**: derive from the flags the PR API returns:

  | `state`  | `draft` | `merged` | Cache as     |
  |----------|---------|----------|--------------|
  | `open`   | `true`  | —        | `draft`      |
  | `open`   | `false` | —        | `open`       |
  | `closed` | —       | `true`   | `MERGED`     |
  | `closed` | —       | `false`  | `closed`     |

## Step 4 — POST the link

The `url` field should be the URL you actually have — `/pull/N` for PRs,
`/issues/N` for issues. **Don't rewrite it.** Karma's parser preserves
the path segment; the UI uses it to distinguish PRs from issues.

```bash
curl -s -X POST "${KARMA_API_URL:-http://localhost:8000}/sessions/${CLAUDE_SESSION_ID}/tickets" \
     -H 'Content-Type: application/json' \
     -d '{"ref":"<key>","provider":"<provider>","url":"<url>","source":"slash_command"}'
```

For GitHub, `<key>` is always `owner/repo#N` regardless of kind — the
URL field carries the issue/PR distinction.

## Step 5 — PUT the metadata (only if Step 3 succeeded)

```bash
curl -s -X PUT "${KARMA_API_URL:-http://localhost:8000}/tickets/<provider>/<key>" \
     -H 'Content-Type: application/json' \
     -d '{"title":"<title>","status":"<status>"}'
```

For GitHub keys with `/` and `#`, URL-encode the key in the path:
`octocat/repo#42` → `octocat%2Frepo%2342`.

## Step 6 — Confirm to the user

One line. For GitHub, distinguish the kind so the user knows what they
just attached:

- `Linked session to LINEAR-123 (Fix login bug, In Progress) — open at https://linear.app/...`
- `Linked session to PROJ-45 (Migrate auth, Done) — open at https://acme.atlassian.net/browse/PROJ-45`
- `Linked session to octocat/repo#42 [issue] (Empty state lies, open) — open at .../issues/42`
- `Linked session to octocat/repo#42 [PR] (Fix linting, MERGED) — open at .../pull/42`

## Notes

- Karma is loopback-only by default. `KARMA_API_URL` overrides for custom
  port or remote host.
- POST is idempotent on `(session, ticket)`; re-running upgrades the
  `link_source` if previously set by branch-detect or dashboard. Order:
  `slash_command > dashboard > branch`.
- If the API is unreachable, tell the user
  `karma not running at ${KARMA_API_URL:-http://localhost:8000}` so they
  see what was tried. Don't silently succeed.
- GitHub issues and PRs sharing `#N` means a single karma row (one
  `(provider, external_key)` pair) covers both views of that number.
  The URL field is what tells karma's UI which one to render. Send the
  URL you actually have.
