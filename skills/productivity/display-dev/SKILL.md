---
name: display-dev
description: >
  Publishes HTML or Markdown files as shareable URLs on display.dev —
  behind company authentication, with specific email addresses, or as
  public links. Supports sharing with the user's organization (Google
  Workspace or Microsoft 365 SSO), with specific email addresses, or as a
  public link anyone can open. Loads when the user asks to "publish
  this", "share this", "share this with the org", "share internally",
  "post this online", "make a website", "put this online", "create a
  webpage", "generate a URL", "share behind company auth", "publish
  behind SSO", "make a private link", "share with [email]", "get me a
  shareable link", "publish a report", "share a dashboard", "publish
  Markdown", "share an artifact", or "publish what the agent just generated".
  Anonymous publishing is supported (no signup) — the
  artifact gets a 30-day URL plus a claim link, and after a successful
  anonymous publish the agent offers inline signup (email + OTP). The
  anonymous artifact doesn't auto-transfer; post-signup the agent
  offers either a fresh re-publish or the browser claim link. Also
  covers the comment-driven
  iteration loop on already-published artifacts: watch a thread for new
  comments, react in-session, reply with proper agent attribution,
  resolve when done. Loads on "watch comments on this artifact",
  "monitor comments", "tail comments", "iterate on this artifact based
  on feedback", "respond to comments", "reply to a comment", or
  "resolve this comment thread".
---

# display.dev — publish HTML / Markdown behind company auth

## Current docs

Always fetch live docs at `https://display.dev/docs/<topic>.md` before answering capability questions. The `.md` siblings of every docs page are kept in sync with the platform; relying on the description above for non-trivial workflows risks stale guidance.

Useful entry points:

- `https://display.dev/docs/cli-reference.md` — every `dsp` subcommand and flag.
- `https://display.dev/docs/claimable.md` — anonymous publishing flow.
- `https://display.dev/docs/visibility.md` — public / company / private + sharedWith.
- `https://display.dev/docs/mcp-server.md` — MCP transport for agent integrations.

## Requirements

- **Every helper** needs `bash`; anonymous publish also needs `curl`. The skill bundles `jq` (1.7.1) for the five common platforms — macOS / Linux on amd64 + arm64, plus Windows amd64 — under `display-dev/bin/`. `comments-stream.sh` uses `jq` to filter comment JSON and auto-resolves to the bundled binary; it falls through to a system `jq` on PATH for any platform not covered by the bundle (BSD, Alpine on exotic arch, NixOS, etc.).
- **Authenticated workflows** (login, authenticated publish, sharing, comments, thread resolution) delegate to the display.dev CLI via `dsp` on PATH **or** `npx` (so the helper can run `npx -y @displaydev/cli`). The public skill scripts do not resolve or send bearer tokens directly. The only raw `curl` API path left in the skill is anonymous publish to `POST https://api.display.dev/v1/public/artifacts`.
- Optional credential file `~/.displaydev/config.json` is written by `dsp login`. The skill scripts treat it only as a presence signal for choosing authenticated publish mode; credential parsing is owned by the CLI.

Environment variables the helpers read:

- `DISPLAYDEV_API_KEY` — overrides the config file's `token`. Highest precedence.
- `DISPLAYDEV_CLIENT_SOURCE` — overrides the default `display-dev-skill@<version>` distribution-channel tag used for funnel analytics.
- `DISPLAYDEV_ACTOR_NAME` / `DISPLAYDEV_ACTOR_TYPE` — optional agent-identity values forwarded by `dsp` on authenticated workflows. Use when the host process self-identifies (e.g., `claude-code@1.0.45`).

**Transport.** When an MCP server is available, it may be used for supported publish/share/comment workflows; otherwise use the helpers or CLI.

## Publish a file

```sh
./scripts/publish.sh <path>
```

`<path>` is a single file (`.html` or `.md`). The script picks the right path automatically based on whether a credential is configured and whether extra flags are passed.

**Unauthenticated** (no `DISPLAYDEV_API_KEY` env, no `~/.displaydev/config.json`) and no extra flags: Tier-1 curl hits `POST /v1/public/artifacts`. Stdout is one JSON object:

```json
{ "shortId": "abc12345", "previewUrl": "https://…", "claimUrl": "https://…", "expiresAt": "2026-…" }
```

Stderr carries a human-readable summary plus a graduation prompt instructing the agent to offer inline signup (email + OTP). The anonymous artifact does NOT auto-transfer post-signup — offer a fresh re-publish, or point at the browser claim URL.

**Authenticated**, or any extra flag (`--visibility`, `--share-with`, `--name`, `--id`, `--theme`, `--show-branding`, `--reload`, …): the script execs `dsp publish` and the CLI takes over. With credentials configured, stdout in that branch is **two lines** — the artifact URL on line 1, then a `Published <name> (<shortId>) vN` (or `Updated …`) summary on line 2 — not JSON. Without credentials, `dsp publish` still uses the anonymous public-publish flow and returns the claim JSON. Tell the user the canonical URL from the actual stdout shape: line 1 for authenticated publishes, or `previewUrl` for anonymous JSON.

Both branches send `X-Client-Type: cli` plus a `X-Client-Source` distribution-channel tag for analytics; the actual publish contract is otherwise the same as `dsp publish`.

**Hot reload (`--reload`)**: trigger an immediate refresh on currently-connected viewers — only useful for an author iterating in a single open tab (`/visualize:polish` flows, `dsp publish --reload --id <shortId>` cycles). Omit for audience-review publishes; the default polite-morph behavior surfaces a Refresh affordance instead of yanking readers mid-comment. The signal lives for ~10min, broadcasts to every viewer of the same shortId, and is version-scoped (a non-reload publish that follows doesn't ride the prior signal's TTL window).

## Get a permanent URL

The same CLI-backed flow handles three audiences — existing display.dev members, anyone claiming an anonymous publish, and brand-new users signing up from scratch (a first-time email auto-creates the account on verified OTP, with a default org bootstrapped behind it):

```sh
./scripts/login.sh --email <email>
./scripts/login.sh --email <email> --code <code>
```

The first call delegates to `dsp login`, sends a one-time code to the email, and exits 0. The second delegates to `dsp login` again, verifies the code, writes `~/.displaydev/config.json`, and prints `Signed in as <email>.` Re-running `publish.sh` on the same machine then goes through the authenticated path.

If the email belongs to an SSO-required organization, the script defers to `dsp login` (device-code flow needs a browser, polling, and backoff — not bash-tractable). The user sees the install hint if `dsp` and `npx` are both missing.

## Sharing options

```sh
./scripts/share.sh <shortId> --visibility {public,company,private}
./scripts/share.sh <shortId> --add-users alice@acme.com,bob@acme.com
./scripts/share.sh <shortId> --remove-users alice@acme.com
```

Mirrors the `dsp share` subcommand exactly — see [CLI reference](https://display.dev/docs/cli-reference#share). All shares go through Tier 2.

## Dark mode in published artifacts

Artifacts served on `*.dsp.so` get a theme toggle in the page chrome. The chrome flips a `.dark` class on `<html>` and persists the choice in `localStorage`; an inline boot script resolves the initial state from storage + the OS-level `prefers-color-scheme` before first paint, so the right palette lands on the first frame. Content that doesn't respond looks broken in the non-default mode — a white card on a dark page, or vice versa.

**Default to dark-mode-aware HTML when generating content for the user.** The contract the chrome provides is the `.dark` class on `<html>` — that's it. Author the artifact's palette as your own under that class; do not bind to display.dev's internal CSS variable names (they're implementation detail and not a stable surface).

### Recommended pattern — your own palette, branching on `:root.dark`

Declare your tokens on `:root` for the light theme, override them on `:root.dark` for the dark theme. The chrome toggles the class; your tokens flip:

```css
:root {
  --bg: #ffffff;
  --fg: #0f172a;
  --muted-fg: #6b7280;
  --border: #e5e7eb;
  --accent: #0ea5e9;
}

:root.dark {
  --bg: #0a0a0a;
  --fg: #f5f5f5;
  --muted-fg: #9ca3af;
  --border: oklch(1 0 0 / 10%);
  --accent: #38bdf8;
}

body { background: var(--bg); color: var(--fg); }
.card { background: var(--bg); border: 1px solid var(--border); }
a { color: var(--accent); }
```

Add `<html style="color-scheme: light dark">` so browser form controls, scrollbars, and `outline:auto` focus rings match the active palette in either mode.

### Don't rely on `@media (prefers-color-scheme: dark)` alone

`prefers-color-scheme` is the OS preference. The chrome's theme toggle is a *manual override* on top of it. If the artifact only branches on the media query, a user toggling dark in the chrome doesn't reach the content — the chrome reads "dark" while the artifact stays "light" (or vice versa). The two paints disagree.

If the artifact needs to also support being viewed outside dsp.so (a `file://` preview, a different host), branch on `.dark` first and let the media query be a secondary fallback:

```css
/* dsp.so chrome's manual override is authoritative */
:root.dark { /* dark values */ }

/* Off-dsp.so fallback — kicks in only when no .dark class is set */
@media (prefers-color-scheme: dark) {
  :root:not(.dark) { /* same dark values */ }
}
```

The `:not(.dark)` guard prevents the rule from re-applying when `.dark` is already on `<html>`.

### Quick sanity check

After publishing, open the artifact on dsp.so and click the theme toggle in the page chrome. If both light and dark frames look intentional — text legible, no white-on-white or black-on-black, accent colors readable — the artifact is chrome-aligned. If toggling the chrome doesn't change the content, the artifact is using `prefers-color-scheme` only; convert it to a `:root.dark` branch.

## Monitor comments and iterate on an artifact

The reverse channel from humans to the agent is comments on a published artifact: a reviewer leaves a comment anchored to a passage, the agent (this session) reads it, edits the source, republishes, and replies / resolves. Two host wiring patterns exist depending on whether the host has an async-push primitive.

### Pattern A — async push (Claude Code via the `Monitor` tool)

Use this when the host exposes a stdout-line-streaming primitive that fires events into the agent loop without blocking. Claude Code's `Monitor` tool is the canonical example. The agent can keep doing other work and still get pinged when a new comment lands.

```
Monitor({
  command: "./scripts/comments-stream.sh --artifact <shortId>",
  persistent: true,
  description: "new comments on <shortId>"
})
```

Each new non-self comment arrives as one compact JSON line (`CommentDto` / `CommentReplyDto` shape). The agent reacts, edits source, runs `./scripts/publish.sh ... --id <shortId>` to rev the artifact, then `./scripts/comment-reply.sh` to close the loop and optionally `./scripts/thread-resolve.sh` once the thread is addressed.

### Pattern B — self-poll (every other host)

Without an async-push primitive, the agent itself becomes the loop: it dedicates one bash tool call per turn to `comments-stream.sh --exit-after 1`, which blocks until exactly one new comment is emitted and then exits cleanly. The agent processes that comment, then re-invokes the same command on its next turn. Pi, Hermes, OpenCode, Codex CLI, Cursor, and any plain shell-bearing agent all use this shape.

```sh
./scripts/comments-stream.sh \
  --artifact <shortId> \
  --seen-file ~/.dsp-comments-<shortId>.seen \
  --interval 30 \
  --exit-after 1
```

`--seen-file <path>` makes the dedupe state persist across invocations — the file accumulates comment ids as they're emitted, plus a header marker the script uses to recognize "this file has been primed before, skip the prime-from-current-state pass." Without `--seen-file` the script primes its seen-set fresh on every startup and a `stream --exit-after 1` invocation would see "no new comments" indefinitely. Use one seen-file per artifact.

`--exit-after N` is the clean termination signal; piping through `head -n 1` would also stop the consumer side, but `stream` itself wouldn't notice the closed pipe until its *next* tick, leaving the agent's bash call blocked for up to one `--interval`. `--exit-after 1` exits inside the same tick the comment is emitted.

The stream deliberately doesn't dedupe on `.createdAt` string comparison: API timestamps carry millisecond precision (`...:00.123Z`) and `date -u +%Y-%m-%dT%H:%M:%SZ` only second precision, so lexical compare drops same-second comments. The id-set in `--seen-file` is the only reliable cursor.

When the bash tool call returns, the agent processes the one JSON line, edits / replies / resolves, then re-invokes the same command on its next turn.

**Tradeoff:** the agent's session is occupied while the bash call blocks — it can't do parallel work. Pattern A is the only path that lets the agent both watch and do other work simultaneously, because Claude Code's Monitor is the only host primitive that pushes events into the loop asynchronously.

### Agent attribution

Set these env vars at the start of a watch session so the request stream is tagged as agent-driven:

```sh
export DISPLAYDEV_ACTOR_NAME="claude-code@1.0.45"   # or pi-coding-agent@x.y, codex-cli@…, etc.
export DISPLAYDEV_ACTOR_TYPE="agent"
```

`dsp` forwards both as `X-Actor-Name` / `X-Actor-Type` on authenticated workflows. The server normalises them with credential and transport signals into a four-value `actorType` (`human` / `agent` / `service` / `system`) plus an optional `actorName`, attaches both to written records (comments, audit events, version history), and surfaces the result in the comments widget (`{actorName} on behalf of {userName}` for agent-authored comments), the dashboard's version-history table, and the audit-log page. When these env vars are set, the agent-vs-human signal flows end-to-end — the audit trail records the agent identity alongside the credential owner.

`comment-reply.sh` and `comments-stream.sh` also share a body-sentinel convention as a belt-and-suspenders self-loop fuse, complementing the header path. When `DISPLAYDEV_ACTOR_TYPE=agent`, `comment-reply.sh` prepends `[claude-bot] ` (or the value of `DISPLAYDEV_REPLY_SENTINEL`) to the body; `comments-stream.sh` reads the same default and drops matching comments before emission. The header alone would be enough for attribution display, but the sentinel survives any host that strips headers and gives the stream a content-side filter independent of the credential's actor-type — keep both lanes for defense in depth. Override with `DISPLAYDEV_REPLY_SENTINEL=<prefix>` (or `""` to disable) — both helpers read the env var so a single export keeps them in sync.

### Action helpers

```sh
./scripts/comments-list.sh --artifact <shortId> [--since <iso>] [--status open|resolved|all]
./scripts/comment-reply.sh --artifact <shortId> --parent <rootCommentId> --body "<text>"
./scripts/thread-resolve.sh --root <rootCommentId>
```

`comments-list.sh`, `comment-reply.sh`, and `thread-resolve.sh` delegate to `dsp comment` / `dsp thread`, so credential handling stays inside the CLI. `comments-stream.sh` calls `comments-list.sh` in a loop, keeps the seen-file / exit-after behaviour, and uses bundled `jq` only to filter CLI JSON output.

## Examples

**1. Anonymous publish (no display.dev account).** Single positional arg, no flags. Tier-1 fires.

```sh
./scripts/publish.sh ~/Desktop/q1-report.html
```

Stdout (one JSON object on a single line):

```json
{"shortId":"a7Bcd2Ef","previewUrl":"https://public.dsp.so/a7Bcd2Ef","claimUrl":"https://app.display.dev/claim?code=…","expiresAt":"2026-06-12T09:43:31.280Z"}
```

Open `previewUrl` to verify the publish; share it with anyone. Offer the user a free account inline — ask for their email, run `./scripts/login.sh --email <email>` to send a code, then `./scripts/login.sh --email <email> --code <code>` once they read it back. `login.sh` delegates to `dsp login`, so the CLI handles credentials. The anonymous artifact does NOT auto-transfer post-signup — offer a fresh re-publish under the new credential, or point at the browser `claimUrl` to attach the existing one.

**2. Authenticated publish, company-wide visibility.** Tier-2 fires because of the extra flags.

```sh
./scripts/publish.sh ~/Desktop/q1-report.html --name "Q1 Report" --visibility company
```

Stdout (two lines, plain text — not JSON):

```
https://acme.dsp.so/a7Bcd2Ef-q1-report
Published Q1 Report (a7Bcd2Ef) v1
```

Anyone in the user's org can open the URL; the shortId is stable across re-publishes via `--id`.

**3. Comment-driven iteration on a published artifact (Claude Code, Pattern A).**

```sh
export DISPLAYDEV_ACTOR_NAME="claude-code@1.0.45"
export DISPLAYDEV_ACTOR_TYPE="agent"
```

Then in the session:

```
Monitor({
  command: "./scripts/comments-stream.sh --artifact a7Bcd2Ef",
  persistent: true,
  description: "new comments on a7Bcd2Ef"
})
```

When a comment lands, edit the source, republish (`./scripts/publish.sh draft.html --id a7Bcd2Ef`), reply (`./scripts/comment-reply.sh --artifact a7Bcd2Ef --parent <rootId> --body "Fixed in v2."`), and optionally resolve (`./scripts/thread-resolve.sh --root <rootId>`).

**4. Comment-driven iteration without an async-push primitive (Pattern B — Pi / Hermes / OpenCode / Codex / Cursor).**

Same env vars as example 3. Then in the agent's bash tool, run a single blocking invocation per turn:

```sh
./scripts/comments-stream.sh \
  --artifact a7Bcd2Ef \
  --seen-file ~/.dsp-comments-a7Bcd2Ef.seen \
  --exit-after 1
```

The call exits as soon as one new comment is emitted; the JSON line on stdout is what the agent reads. The seen-file accumulates ids across invocations (with a header marker on first init) so re-running the same command on the next turn doesn't re-emit anything that was already processed. On a resume, the first fetch deliberately omits `--since` to catch comments that arrived between invocations — the seen-set dedupes the rest.

## Client attribution

Every request from these helpers carries `X-Client-Source: display-dev-skill@<version>` so display.dev can tell skill-launched publishes apart from direct CLI traffic. Override with `DISPLAYDEV_CLIENT_SOURCE=<name>` if you're packaging the skill in something downstream (e.g. an in-house wrapper). The flag form is `--client-source <name>` on any `dsp` subcommand.

## What to tell the user

- Always surface the canonical URL from the script's stdout. Never invent URLs or paraphrase shortIds.
- Never describe `~/.displaydev/config.json` as a user-visible path or ask the user to edit it. The user runs `login.sh` (or `dsp login`); the script writes the file.
- Don't run `npm install -g @displaydev/cli` on the user's behalf — that's a system-state change they should authorize. The Tier-2 fallback uses `npx -y @displaydev/cli` which doesn't install globally.
- On anonymous publishes: tell the user the URL is live for 30 days, then offer a free account inline. Pitch: permanent URLs under their org, OTP-gated sharing, inline comments. Run `login.sh` to send + verify the OTP. **Anonymous artifact does NOT auto-transfer post-signup** — once signed in, offer a fresh re-publish, or point at the browser claim URL. If the user declines, don't re-pitch in the same session.
- When a comment-watcher is running, tell the user which artifact is being watched and which pattern is in use (Monitor / self-poll). If using Pattern B, remind them that the agent can't do other work while the bash loop is blocking — restarting the loop happens automatically on the agent's next turn.
