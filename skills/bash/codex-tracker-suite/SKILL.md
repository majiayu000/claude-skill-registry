---
name: codex-tracker-suite
description: This skill should be used to search, inspect, list, and recover local Codex sessions through Codex's native App Server APIs. Trigger for requests such as find a prior Codex conversation, search Codex transcript text, list recent Codex work, locate matches inside a session, or produce a safe Codex resume command. Do not use for Claude Code sessions, project source-code search, or web search.
---

# Codex Tracker Suite

Use the bundled wrapper instead of reading Codex's private SQLite databases or rollout files. It talks to the version-matched `codex app-server` protocol and leaves Codex as the source of truth.

```bash
codex-tracker search "topic"
```

## Route the request

- Find a session by topic or transcript text: `search QUERY`
- Locate every visible match inside one session: `occurrences SESSION_ID QUERY`
- Browse recent work: `recent`
- Inspect metadata or the visible conversation: `show SESSION_ID`
- See sessions loaded in a shared managed runtime: `alive`
- Produce a shell-safe command for continuing work: `resume SESSION_ID`

Run any command with `--help` for filters and JSON output. Add `--include-non-interactive` for `codex exec` and App Server sessions, or `--all-sources` for subagents too. Ordinary searches default to interactive CLI and IDE sessions, matching Codex's native behavior.

## Operating rules

- Keep lookup operations read-only. `resume` prints a command; it does not launch an interactive process.
- Return the matching session ID, title, working directory, snippet, and resume command when available.
- Prefer `--json` when another program or agent will consume the result.
- Native transcript search is experimental and may take a minute or two on a large history. The wrapper prints progress while waiting and uses a configurable timeout.
- If native full-text search is unavailable, report the compatibility error and suggest `codex resume --all`; do not silently scrape private databases.
- App Server may update its own state metadata during a read. In a restricted Codex sandbox, request approval for the wrapper command instead of bypassing the sandbox.
- Do not archive, delete, rename, or otherwise mutate sessions unless the user separately asks for that operation. This wrapper intentionally exposes no destructive commands.
- Treat `alive` as a managed-daemon view. Without the shared App Server daemon, use Codex's own session UI or process-level diagnostics instead.

For protocol choices, compatibility behavior, and parity boundaries, read [references/architecture.md](references/architecture.md) only when maintaining or extending the wrapper.
