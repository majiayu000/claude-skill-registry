# Agent environment reference

You (the agent) need to know which agent harness you are running inside, and which environment constraints apply. This page is the single source of truth — no helper scripts, just facts you read and act on.

## Detecting which agent you are

Run this in bash (or the equivalent in your environment):

```bash
env | grep -E '^(CLAUDECODE|CODEX_THREAD_ID|OPENCODE_CLIENT|GEMINI_CLI)=' | cut -d= -f1
```

Match the result against this table. Precedence is top to bottom — if multiple markers are set (e.g. Codex started inside a Claude Code shell), take the innermost agent.

| Env var present | Agent | Notes |
|---|---|---|
| `CODEX_THREAD_ID` | `codex` | Set per session by `codex-rs/config/src/shell_environment.rs`. Codex clears the parent env and re-populates a strict allowlist, so other markers do not survive into a Codex shell. |
| `CLAUDECODE` | `claude-code` | Value is always `1`. Source: docs at `code.claude.com/docs/en/env-vars`. |
| `GEMINI_CLI` | `gemini` | Value is always `1`. Source: `gemini-cli-core/services/shellExecutionService.js` (`GEMINI_CLI_IDENTIFICATION_ENV_VAR`). |
| `OPENCODE_CLIENT` | `opencode` | Value is always `1`. |
| none | `unknown` | Proceed with universal fallbacks (OSS MCPs, IMAP). |

Store the result. Every later branch in `setup.md` / `audit.md` depends on it.

## Sandbox constraints per agent

When you know which agent you are, you know what the shell can and cannot do. This is critical — do not waste time fighting the sandbox; adapt.

### `codex`

Codex CLI on macOS runs all tool calls through a **seatbelt sandbox**. The sandbox mode is controlled by the `-s` / `--sandbox` flag or the `--full-auto` convenience alias.

**`codex exec --full-auto` uses `workspace-write` by default. In `workspace-write` the entire network stack is blocked — empirically verified (April 2026):**

| Test | Result |
|---|---|
| `curl https://www.google.com` | exit 6 — `Could not resolve host: www.google.com` (DNS refused at syscall level) |
| `curl http://localhost:5600/api/0/info` | exit 7 — `Couldn't connect to server` (TCP connect refused at 0ms) |

DNS resolution is blocked, outbound TCP is blocked, and **localhost is not exempt**. Running ActivityWatch or any other local HTTP service on the host does NOT make it reachable from Codex's sandboxed bash — the seatbelt denies `connect()` before the TCP stack even tries. This is not a FlowHunt bug and not a config issue on the host — it is the default sandbox policy.

Other confirmed blocked operations in `workspace-write`:

- `open -a <App>` — launching GUI applications is refused by the seatbelt policy. Codex wraps the failure as `SandboxDenied`, and stdout is moved to stderr in the error envelope.
- `nohup <cmd> &` — the `nice` syscall is refused (`zsh:1: nice(5) failed: operation not permitted`).
- Binding network sockets on arbitrary ports (`python3 -m http.server 5600`, `aw-server`) — refused with `PermissionError: [Errno 1] Operation not permitted`.
- Writing to `~/Library/Logs/`, `~/Library/Application Support/` outside the workspace root — refused.
- `open` with http/https URLs — macOS LaunchServices rejects the URL scheme from sandboxed shells with `kLSExecutableIncorrectFormat`.

**FlowHunt is unusable under `workspace-write`** because the audit depends on reading ActivityWatch and MCP tools over HTTP. If you (the agent) detect `CODEX_THREAD_ID` set AND a baseline network probe fails (see probe below), stop the setup/audit immediately and tell the user one of these:

1. **Easiest:** run `flowhunt setup` / `flowhunt audit` from **interactive `codex`** (just `codex` without `exec --full-auto`). Interactive mode defaults to `on-request` approval which prompts per command and does not blanket-block network.
2. **Dev-only:** `codex exec -s danger-full-access --full-auto "flowhunt setup"` — bypasses the entire sandbox, only acceptable if the user has accepted the risk and is running inside an already-isolated environment.
3. **Different agent:** Claude Code, Gemini CLI, or OpenCode — none of them ship with a default sandbox that blocks localhost.

**The network probe (use at the start of setup.md Step 2 and audit.md Step 0 when agent = `codex`):**

```bash
curl -fsS --max-time 2 http://localhost:5600/api/0/info > /dev/null 2>&1
```

If exit code is 7 AND the user confirms ActivityWatch is running on the host (browser at `http://localhost:5600` shows the dashboard), you are in a sandboxed Codex session and cannot proceed. Print the three options above and stop.

**What `workspace-write` does allow** (also verified empirically or via the Codex source):
- Reading files in the workspace and in standard user config paths
- Running `jq`, `grep`, `python` (short non-binding scripts), `git`, `node`, `uvx`, most Unix tools
- Writing files inside the workspace directory and `$TMPDIR`
- Reading from `~/.codex/config.toml`, `~/.agents/skills/`, `~/.claude/skills/`
- Executing other `codex` subcommands (`codex --help`, `codex mcp list`, etc.) although those emit a `WARNING: proceeding, even though we could not update PATH: Operation not permitted` because the subshell cannot mutate PATH

Use this for reading/writing config files (opencode.json, config.toml, etc.) but not for anything that touches network or GUI.

### Owning the past mistake

Earlier versions of this file claimed "Running `curl` to localhost endpoints (unrestricted outbound to `127.0.0.1`)" under Codex `workspace-write`. **That was wrong — written from assumption, not from test.** Empirical verification (running `curl http://localhost:5600` and `curl https://www.google.com` from inside a real `codex exec --full-auto` session) showed both fail with different exit codes confirming a full network block. The claim is now corrected above. Lesson: never write environment facts without running them.

### `claude-code`

Claude Code's bash tool has per-command permissions controlled by the user's `settings.json`. By default `curl`, `open`, `brew`, most Unix tools work. GUI launching via `open -a` typically works on macOS. No systematic seatbelt-style denial.

If a command you want to run is not on the user's allowlist, you will get a permission prompt; let the user approve or deny, don't try to work around it.

### `gemini`

Gemini CLI inherits the user's shell environment without a hard sandbox by default. Same expectations as Claude Code. You can `open -a` on macOS, launch background processes, bind ports.

### `opencode`

OpenCode runs bash via its built-in tool with user-controlled permissions (`permission.bash` in `opencode.json`). Similar to Claude Code. No default sandbox.

### `unknown`

Assume minimum: curl to localhost works, file reads work, nothing else is guaranteed. Degrade gracefully: ask the user to run anything complex themselves.

## Rule of thumb

Before running any Bash command that could touch the sandbox (GUI app launch, port binding, system directory write), **check the agent**. If `codex`, skip the attempt and ask the user. If anything else, try it.

This is not a quirk — it is the permanent shape of the constraint. Codex's sandbox is not going to change. Plan around it.
