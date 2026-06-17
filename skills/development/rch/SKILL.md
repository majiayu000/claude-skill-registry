---
name: rch
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: "Use when offloading slow builds to remote workers or recovering RCH worker, hook, SSH, sync, or disk issues."
practices:
- pragmatic-programmer
---
# RCH — Remote Compilation Helper

`rch` transparently offloads compilation commands to remote workers via a Claude Code PreToolUse hook. The daemon picks the fastest healthy worker, rsync's the workspace, runs the build, syncs artifacts back, and exits with the worker's exit code.

This skill is the operational layer agents use when something about that pipeline isn't working — and the much more common case where it *thinks* it's working but is silently falling back to local execution. The skill is built around a single principle: **self-resolve before asking the human.** Every recovery path here is one the agent can run on its own.

Tested against rch v1.0.18; concepts apply to v1.0.16+.

---

## Read This First

When a build feels slow, run **one** thing:

```bash
RCH_VISIBILITY=verbose <your-command> 2>&1 | grep -E '^\[RCH\]'
```

The summary line is a contract:

| Pattern | What to do |
|---|---|
| `[RCH] remote <worker> (...)` | Healthy. Done. |
| `[RCH] remote <worker> failed [RCH-Exxx] ...` | Real build/env failure. See `references/ERROR_CODES.md`. |
| `[RCH] local (<reason>)` | **Fail-open.** See `references/FAIL_OPEN.md` and look up the reason verbatim. |
| *no `[RCH]` line at all* | Hook didn't fire. Run `scripts/protocol_test.sh "<your-command>"`. |

If you can't see why offload isn't happening, **prove the path works in isolation** before doing anything else:

```bash
rch exec -- env CARGO_TARGET_DIR="${TMPDIR:-/tmp}/rch_target_$(basename "$PWD")" cargo check --workspace --all-targets
```

If that prints `[RCH] remote <worker> (...)`, the offload pipeline is healthy. The problem is upstream of `rch exec` — usually the hook classifier or the agent's invocation form. If it also fails, follow `references/RECOVERY_PLAYBOOKS.md`.

---

## Quick Start

```bash
rch check                                                  # quick health
rch status --workers --jobs                                # full status
rch workers probe --all                                    # connectivity
rch hook status                                            # hook installed?
rch agents status                                          # which agents are wrapped
rch diagnose --dry-run "cargo check --workspace --all-targets"
rch exec -- env CARGO_TARGET_DIR="${TMPDIR:-/tmp}/rch_target_$(basename "$PWD")" cargo check --workspace --all-targets
rch self-test --all                                        # end-to-end verify
rch doctor                                                 # comprehensive checks
rch doctor --fix --dry-run                                 # see what doctor would auto-fix
```

If `rch status` shows storage pressure, always check both `/` and `/tmp` on the worker before deciding what to fix:

```bash
ssh ubuntu@<host> 'df -h / /tmp && free -h && cat /proc/pressure/memory && cat /proc/pressure/io'
```

---

## Fast Triage Order

Run in this order and stop at the first failing stage:

1. **Availability**
```bash
rch check
rch status --workers --jobs
rch workers probe --all
rch queue
```

2. **Config + socket consistency**
```bash
rch config show --sources
rch --json config get general.socket_path
rch --json daemon status
```

3. **Hook integration**
```bash
rch hook status
rch agents status
rch hook install                       # idempotent
```

4. **Command classification + path closure**
```bash
rch diagnose "cargo build --release"
rch diagnose --dry-run "cargo test --workspace"
```

5. **Remote compile proof**
```bash
rch exec -- env CARGO_TARGET_DIR="${TMPDIR:-/tmp}/rch_target_<name>" cargo check --workspace --all-targets
```

6. **If sync fails or storage looks bad, inspect the worker directly**
```bash
ssh ubuntu@<host> 'df -h / /tmp'
ssh ubuntu@<host> 'du -sh /tmp/rch-* /tmp/rch_target_* 2>/dev/null | sort -h'
ssh ubuntu@<host> 'find /data/projects -maxdepth 2 -type d \( -name "target_rch_*" -o -name "target_*" -o -name "target-*" -o -name target \) -exec du -sh {} + 2>/dev/null | sort -h | tail'
```

---

## Quick Fixes

| Symptom | Command |
|---------|---------|
| Hook not installed | `rch hook install && rch hook status` |
| Daemon not running | `rch daemon start` |
| Daemon version drift after upgrade | `rch daemon restart -y` (it drains gracefully — safe by default) |
| Socket mismatch / stale daemon state | `rch daemon restart -y` then `rch --json daemon status` |
| No workers configured | `rch workers discover --add --yes && rch workers setup --all` |
| Workers unreachable | `rch workers probe --all` then fix SSH key/host reachability — or `references/SSH_KEY_RECOVERY.md` if keys are missing |
| All workers busy | Queueing is on by default; if you still see fail-open, bump `RCH_DAEMON_WAIT_RESPONSE_TIMEOUT_SECS=120 <your-command>` (or raise `total_slots`) |
| Need a per-command priority bump | `RCH_PRIORITY=high <your-command>` (low\|normal\|high) |
| Want CARGO_TARGET_DIR / RUSTFLAGS forwarded to remote | `RCH_ENV_ALLOWLIST=CARGO_TARGET_DIR,RUSTFLAGS <cmd>` |
| Transfer churn under target dirs | Add excludes in `~/.config/rch/config.toml`, then `rch daemon reload` |
| Path dependency missing remotely | See `references/PATH_DEPENDENCIES.md` (now configurable via `[path_topology]`) |
| Sync fails with `Permission denied` in `/data/projects/<repo>` | Fix remote mirror ownership: `ssh ubuntu@<host> 'sudo chown -R ubuntu:ubuntu /data/projects/<repo> && sudo chmod 775 /data/projects/<repo>'` |
| Worker shows disk pressure (RCH-E210/211/...) | `references/DISK_AND_PRESSURE.md` — hand off to the `sbh` skill |
| Telemetry / SpeedScore broken | `references/TELEMETRY_RECOVERY.md` — move db aside, restart |
| Hook says installed but isn't intercepting | `scripts/protocol_test.sh "<your-command>"` |
| Worker shows pressure warning | Check `/` and `/tmp` separately, then inspect stale `rch_target_*`, `rch-*`, and `target_rch_*` dirs before broader cleanup |
| Multiple agents racing on fleet ops | Wrap with `scripts/multi_agent_safety.sh <cmd>` and use Agent Mail file reservations |
| Need full environment diagnosis | `rch doctor --json` and `rch config doctor` |

---

## Anti-Asking Rules

These are the questions agents historically ask the human that they should *just answer themselves*. The answer is in this skill or trivially derivable. **Do not ask. Do.**

- "Can I restart the daemon?" — Yes. `rch daemon restart -y` drains in-flight builds gracefully. It's the documented upgrade path.
- "Can I clean up `/tmp/rch_target_*`?" — If `sudo lsof +D <dir>` is empty, yes. See `references/DISK_AND_PRESSURE.md`. If non-empty, never.
- "Should I fix the chown on the worker?" — If the symptom matches the Permission denied recipe, yes. It's documented.
- "Should I disable an unreachable worker and continue?" — Yes. `rch workers disable <id> --reason "..." --drain -y`, then proceed with what's healthy.
- "Should I reinstall the hook?" — If `rch hook status` says missing, yes. `rch hook install` is idempotent.
- "Should I sync the toolchain to the workers?" — If `RCH-E205` or "toolchain missing on X" appears, yes. `rch workers sync-toolchain --all`.
- "The cooldown is blocking my retry — should I delete it?" — No. Wait `auto_start_cooldown_secs`. If you really need to bypass, use `rch daemon start` directly (it's not gated by the hook autostart cooldown).
- "Can I drop the corrupt telemetry db?" — Yes. `references/TELEMETRY_RECOVERY.md`. Telemetry is derived data.
- "Should I recover SSH keys from a sibling host?" — If the keys are missing on this host but reachable on another, yes. `references/SSH_KEY_RECOVERY.md` Step 3.

When in genuine doubt, capture the escalation packet (Playbook end of `references/RECOVERY_PLAYBOOKS.md`) and surface that — not a wall of text — to the human.

---

## Knobs Worth Knowing (Env Vars)

| Variable | Use |
|---|---|
| `RCH_VISIBILITY=summary\|verbose\|none` | Force a `[RCH] ...` summary line on every offloaded build. **Use `verbose` to debug fail-opens.** |
| `RCH_QUEUE_WHEN_BUSY` | Wait for a slot instead of falling back to local. **Default is `1` (wait).** Set `=0` to opt out (e.g., for benchmarking). |
| `RCH_PRIORITY=low\|normal\|high` | Per-command priority hint to the daemon scheduler. |
| `RCH_ENV_ALLOWLIST=K1,K2,...` | Forward extra env vars to the remote build. Common: `CARGO_TARGET_DIR,RUSTFLAGS,RUST_LOG`. |
| `RCH_LOG_LEVEL=debug` | Verbose diagnostics on stderr — use to surface what fail-open path was taken. |
| `RCH_PROFILE=dev\|prod\|test` | Switch the active config profile. |
| `RCH_DAEMON_SOCKET=...` | Override socket path (CLI side). |
| `RCH_DAEMON_TIMEOUT_MS` | IPC timeout for hook→daemon. |
| `RCH_DAEMON_RESPONSE_TIMEOUT_SECS` / `RCH_DAEMON_WAIT_RESPONSE_TIMEOUT_SECS` | Daemon RPC timeouts (immediate vs queued-wait modes). |
| `RCH_SSH_KEY` | Default SSH identity if not set per-worker. |
| `RCH_SSH_SERVER_ALIVE_INTERVAL_SECS` | Keepalive for long-running remote builds (recommend 15). |
| `RCH_SSH_CONTROL_PERSIST_SECS` | Enable ControlMaster persistence (default OFF — see `references/SSH_TUNING.md`). |
| `RCH_TRANSFER_ZSTD_LEVEL` | rsync compression (1-22, default 3). |
| `RCH_OUTPUT_FORMAT=json\|toon` / `TOON_DEFAULT_FORMAT` | Machine output format. |
| `RCH_CANONICAL_PROJECT_ROOT` / `RCH_ALIAS_PROJECT_ROOT` | Override `[path_topology]` roots without editing config. See `references/PATH_DEPENDENCIES.md`. |

---

## Reference Index

Everything below ships in the skill. Read whichever is relevant.

**Recognising what's wrong:**
- `references/FAIL_OPEN.md` — every `[RCH] local (...)` reason mapped to a self-fix
- `references/ERROR_CODES.md` — full RCH-Exxx catalog with skill-doc cross-refs
- `references/TROUBLESHOOTING.md` — diagnostic flow + common errors

**Solving specific failure classes:**
- `references/RECOVERY_PLAYBOOKS.md` — symptom → fix in ≤90s, organized as 12 lettered playbooks
- `references/SSH_KEY_RECOVERY.md` — when workers.toml references keys this host doesn't have
- `references/PATH_DEPENDENCIES.md` — multi-repo workspaces, closure planner, `[path_topology]`
- `references/DISK_AND_PRESSURE.md` — RCH-E210..217 + the `sbh` handoff
- `references/TELEMETRY_RECOVERY.md` — corrupt `~/.local/share/rch/telemetry/telemetry.db`
- `references/SELF_HEALING.md` — autostart cooldown, daemon supervision, `[self_healing]`
- `references/SSH_TUNING.md` — ControlMaster, keepalives, retry classification

**Operating in fleets and swarms:**
- `references/MULTI_AGENT_CONTENTION.md` — TOCTOU, fleet deploy races, autostart cooldown sharing
- `references/OPERATIONS.md` — full runbook + worker fleet lifecycle
- `references/WORKERS.md` — worker config, drain/disable/enable, deploy
- `references/CONFIGURATION.md` — config precedence, env vars, runtime paths
- `references/HOOKS.md` — hook protocol, install, test
- `references/MACHINE_INTROSPECTION.md` — `--json`, `--schema`, `--help-json`, `--capabilities`

**Automation scripts (in `scripts/`):**
- `auto_recover.sh` — heuristic, dry-run-by-default fleet recovery
- `worker_disk_triage.sh` — read-only mount-aware disk report per worker
- `protocol_test.sh` — directly probe the hook protocol with synthetic input
- `multi_agent_safety.sh` — flock wrapper for fleet/setup operations
- `mine_rch_history.sh` — find prior agent sessions that hit a given failure
- `diagnose-rch.sh` — comprehensive end-to-end diagnostic (the original)

**Templates and project docs:**
- `assets/workers-template.toml`
- Source: <https://github.com/Dicklesworthstone/remote_compilation_helper>

---

## Adjacent Skills

- **`sbh`** — disk-pressure defense for AI coding workloads. Use when `RCH-E210/211/215/216` fires.
- **`agent-mail`** — file reservations and messaging between agents. Use before `rch fleet deploy` or any worker config edit in a swarm.
- **`ntm`** / **`vibing-with-ntm`** — multi-agent tmux orchestration; common parent context for agents that hit rch failures.
- **`cass`** — search prior agent sessions; the skill ships `scripts/mine_rch_history.sh` as a fallback when cass index has dead pointers.

---

## Reading Output: TUI vs Hook

`rch` itself, when invoked with **no subcommand**, runs in PreToolUse hook mode (reads JSON from stdin, writes JSON to stdout). Don't run bare `rch` from a terminal expecting help — use `rch --help`. Bare TUIs are at `rch dashboard` (terminal) and `rch web` (browser); both block your session.

- [FAIL_OPEN](references/FAIL_OPEN.md)

- [OPERATIONS](references/OPERATIONS.md)

- [RECOVERY_PLAYBOOKS](references/RECOVERY_PLAYBOOKS.md)

- [TROUBLESHOOTING](references/TROUBLESHOOTING.md)

- [ERROR_CODES](references/ERROR_CODES.md)

- [SELF_HEALING](references/SELF_HEALING.md)

- [WORKERS](references/WORKERS.md)

- [MACHINE_INTROSPECTION](references/MACHINE_INTROSPECTION.md)

- [DISK_AND_PRESSURE](references/DISK_AND_PRESSURE.md)

- [CONFIGURATION](references/CONFIGURATION.md)

- [SSH_TUNING](references/SSH_TUNING.md)

- [MULTI_AGENT_CONTENTION](references/MULTI_AGENT_CONTENTION.md)

- [PATH_DEPENDENCIES](references/PATH_DEPENDENCIES.md)

- [HOOKS](references/HOOKS.md)

- [SSH_KEY_RECOVERY](references/SSH_KEY_RECOVERY.md)

- [TELEMETRY_RECOVERY](references/TELEMETRY_RECOVERY.md)
