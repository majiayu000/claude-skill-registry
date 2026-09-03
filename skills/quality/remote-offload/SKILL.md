---
name: remote-offload
user-invocable: false
tags: [reference, remote, offload, wave-executor, resource-gate]
model: haiku
model-preference: sonnet
model-preference-codex: gpt-5.4-mini
model-preference-cursor: claude-sonnet-4-6
description: Use when local resource pressure would shrink or coordinator-direct a wave, a wave plan carries heavy build/test/audit roles (test, ui, perf), or the operator says offload, remote host, or auslagern — reference for routing that wave role to a declared SSH-reachable host instead of reducing agent count
---

# Remote Offload — routing a wave role to a declared host instead of shrinking it

Repo-side half of #1160: `remote-hosts:` declares hosts, `wave-resource-gate.mjs` places work on them, `remote-dispatch.mjs` runs it. The host-side `offload` CLI (a separate baseline repo owns its SSOT) is invoked as a subprocess; this skill covers what the repo itself knows about it.

## Quick reference

| Task | Command |
|---|---|
| Host readiness | `offload doctor -H <alias> --brief` |
| Gate (typecheck/lint/test) | `offload gate <repo> -H <alias>` |
| Run a command | `offload run <repo> -H <alias> -- <cmd...>` |
| Read-only analysis | `offload claude <repo> -H <alias> --model <name> < prompt.txt` |
| Implementation + patch | `offload claude <repo> -H <alias> --write --patch <path> < prompt.txt` |
| Remove finished jobs | `offload clean -H <alias> --older-than <hours>` |

Exit codes (`offload --help`, measured 2026-09-02): `0` ok · `1` usage/config · `2` host unreachable/not ready · `3` remote command failed · `4` sync failed · `5` timeout · `6` empty diff on a `--write` run · `7` account quota exhausted (429) · `8` write lock held. Same map as `OFFLOAD_EXIT_REASONS` in `scripts/lib/wave-executor/remote-dispatch.mjs`.

## 1. Decision rule — offload vs reduce

The gate decides, not the coordinator. `applyOffloadDecision()` in `scripts/lib/wave-resource-gate.mjs` only fires when the resource verdict is already `reduce` or `coordinator-direct`, and only AFTER the HR-004 heavy-repo cap — a capped wave that offloads still respects the cap. It never probes the network; the coordinator supplies a readiness WITNESS:

- `opts.remoteReady` — `{ [alias]: boolean }`, built from the SessionStart banner line `Offload <alias>: ready=yes …`, or
- `opts.probeFn` — an async `(alias) => boolean` fallback, consulted only for aliases `remoteReady` doesn't answer for (backed by `remoteDoctor()`, i.e. `offload doctor -H <alias> --brief` parsed by `parseDoctorLine()`).

With neither supplied, no host counts as ready and the wave stays local — the gate fails toward local, never toward an unverified host. A role in `NEVER_FOREIGN_ROLES` (`scripts/lib/wave-executor/foreign-dispatch.mjs`: `impl-core`, `security-review`, `migration`, `release`, `secrets`) is never offloaded regardless of readiness.

## 2. What is declared where

`remote-hosts:` in Session Config (`docs/session-config-reference.md` § Remote Hosts) declares the hosts, in preference order — the gate takes the FIRST host whose `roles-allowed` accepts the wave role and is witnessed ready:

```yaml
remote-hosts:
  - alias: <ssh-alias>                 # required, SAFE slug; reaches argv as `-H <alias>`
    roles-allowed: [test, ui, perf]    # subset of test|ui|perf (default: all three)
    repo-path: ~/path/on/host          # optional; SAFE path; default null
    claude-path: ~/.local/bin/claude   # optional; SAFE path; default null
```

Two enums meet here and must not be conflated: `roles-allowed` holds `agent-mapping` roles (`test`/`ui`/`perf`), not wave roles (`Impl-Core`/`Quality`/…). The translation table is `OFFLOADABLE_WAVE_ROLES` in `wave-resource-gate.mjs` (`quality`→`test`, `test`→`test`, `ui`→`ui`, `perf`→`perf`; a wave role absent from that map stays local by default).

An `agent-mapping` entry of the form `<role>: ssh:<alias>` routes that wave role to Claude running ON the declared host instead of shrinking the wave; the alias must already exist under `remote-hosts`, or the config parse throws.

## 3. Three channels of work

| Channel | Command | Verdict rule |
|---|---|---|
| Gate / arbitrary command | `offload gate` / `offload run` | Exit code decides — use the table above, never the prose in the run's own output |
| Implementation, patch back | `offload claude --write --patch <file>` via `dispatchRemote()` | Empty patch (exit `6`) is a FAILURE regardless of what the run reports; the coordinator READS the patch, then applies it with its own `git apply` — the remote job never touches the repo the coordinator commits from |
| Read-only analysis | `offload claude` (no `--write`) | No patch is produced; treat the transcript as advisory input, same skepticism as any reviewer output (`receiving-review.md`) |

`dispatchRemote()` (`scripts/lib/wave-executor/remote-dispatch.mjs`) is the wave-executor caller for the second and third channels; it emits `orchestrator.remote_dispatch.completed` once per call (`docs/events-schema.md`) — the only ledger record a remote dispatch produces, since a Bash-spawned `offload` child fires no `SubagentStop` hook. Payload: `host`, `role`, `run_id`, `ok`, `exit_code`, `duration_ms`, `patch_files`, `patch_bytes`, `reason` (present on every refusal and every failure class — absence means success). Deliberately excluded from the payload: prompt text, patch body, `patch_path`.

## 4. Rules

- **Supervised, not blind.** Read the gate log or the patch before treating it as a result — completed and correct are not the same claim.
- **Prompt travels on stdin, never argv** (`offload --help`: "prompts travel by file (mode 600), never argv"; argv is visible to every process on the host).
- **The patch is READ, then applied by the coordinator** — never inside the offloaded job.
- **`never_foreign` roles are never offloaded** — checked first in `dispatchRemote()`, before any spawn or side effect.
- **One `--job` per concurrent run.** A job holds ONE set of run artefacts; two parallel runs sharing a job collided until per-run ids were introduced.
- **Rate-limit (exit `7`) carries the reset time in the message** — do not retry blind.
- **Secrets never in output** (SEC-008) — `offload` does not print credentials, and the module deliberately excludes prompt text and patch body from telemetry.
- **Never "clean up" another checkout on the host.** `offload clean` only removes the offload tool's OWN finished job worktrees, never a host's other active checkouts.

## 5. Host readiness checklist

- SSH alias configured with key auth (no password/interactive prompt on connect).
- `tmux` available on the host (for an interactive `offload session`).
- Claude authenticated ON the host — never copy OAuth credentials between machines (refresh-token rotation invalidates the source copy); log in fresh with `/login` there instead.
- Repo cloned on the host with headless git credentials configured (no interactive auth prompt on push/pull).
- Node version matching this repo's `.nvmrc`.
- Toolchain parity with the local checkout (same package manager, same lockfile).

## 6. Pitfalls measured in this repo

- **The pre-push quality gate used to fire on the sync push.** `.husky/pre-push` (#C10) detects a SCRATCH push — an unconfigured remote URL, e.g. the offload tool's own SSH sync target — and skips the gate for it; publish remotes (`origin`, `github`) stay gated regardless. The offload tool has since been fixed upstream to push with `--no-verify` itself, so this repo-side detection is defense-in-depth, not the primary fix.
- **The host installer must follow this repo's committed lockfile.** `package-lock.json` is tracked here (npm-canonical — `.claude/rules/development.md` § Package Management); install with `npm ci`, never a different package manager's install command, or the host checkout's `node_modules` layout diverges from CI's.
- **A linked worktree makes `.git` a file, not a directory.** 13 tracked files used to be flagged as "not in repository" in an unmodified worktree at the same layout, because the file form of `.git` was read as an untracked candidate rather than the repository marker — wave 3 fixed `scripts/lib/validate/check-untracked-test-deps.mjs` to treat a `.git` FILE as the repository marker in a linked worktree; the remote gate then ran 15,829/0.
- **Keychain-route auth shares the host account's usage window with that account's other interactive sessions**, not a dedicated quota — a token-slot profile (`--via slot`) avoids the sharing where a fixed quota matters.
