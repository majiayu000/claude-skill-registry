---
name: shell-process-patterns
description: "Safely start, supervise, and terminate shell processes: background jobs, PID capture, signals, traps, cleanup verification."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
routing:
  triggers:
    - "background process"
    - "nohup"
    - "kill process"
    - "pid lookup"
    - "shell cleanup"
    - "trap handler"
    - "signal handling"
    - "set -e"
    - "bash process"
  pairs_with:
    - condition-based-waiting
    - service-health-check
    - cron-job-auditor
  category: process
---

# Shell Process Patterns

Start, supervise, and terminate shell processes safely -- background jobs, subshells, signal handlers, and cleanup. The dominant failure mode in this domain is silent state: a process that looks killed but still holds a port, a trap that looked fine but never fired on the child, a `set -e` script that kept running because `|| true` swallowed the error. This skill picks the right pattern, implements it with the real PID (not the wrapper), and verifies the observable state afterward.

| Pattern | Use When | Key Safety Bound |
|---------|----------|------------------|
| Background start | Ad-hoc long-running child in a script or session | Redirect fd 0/1/2, capture real PID, disown if parent exits |
| Daemonization | Process must survive terminal close, become session leader | `setsid` + fd redirect + write PID file atomically |
| PID resolution | Need to kill / inspect the actual worker | Re-query with `ss`/`pgrep`/`lsof`; `$!` is advisory, not authoritative |
| Signal discipline | Graceful shutdown of a supervisor + children | SIGTERM first with timeout, SIGKILL as last resort, propagate to process group |
| Trap + cleanup | Script must leave no orphans, lock files, or temp dirs | `trap ... EXIT` + verification (file gone, port free, PID dead) |
| Strict-mode scripts | Any non-trivial bash script | `set -euo pipefail` with understood `||` and `if !` escape hatches |

## Scope

**In scope:**
- Starting background processes (`&`, `nohup`, `disown`, `setsid`, daemonization).
- Capturing the actual child PID and reconciling it against observed system state.
- Signal handling -- SIGTERM vs SIGKILL, `exec` semantics, process groups, subshell inheritance.
- Trap discipline -- `EXIT` vs signal traps, ordering, inheritance in subshells and functions.
- Cleanup verification -- kill-and-check, not kill-and-assume.
- `set -e` / `set -u` / `set -o pipefail` interactions and the `||` escape hatch.
- `wait` semantics, reaping children, race conditions between background-start and resource readiness.

**Out of scope:**
- Cron scripts and scheduled job reliability (owned by `cron-job-auditor`).
- Polling, retry, backoff, health-check loops (owned by `condition-based-waiting`).
- Service health reporting (owned by `service-health-check`).
- Fish shell configuration (owned by `fish-shell-config`).
- Shell language features unrelated to process lifecycle -- parameter expansion, arrays, etc.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| starting a background process, `&`, `nohup`, `disown`, `setsid`, daemonize | `starting-processes.md` | Launch-time patterns and fd/session rules |
| capturing the child PID, `$!` lies, port still listening after kill | `pid-resolution.md` | How to get the real PID and reconcile with observed state |
| trap ordering, SIGTERM/SIGKILL, subshell signal inheritance, `exec` | `signals-and-traps.md` | Signal and trap discipline |
| verifying a process is actually gone, lock file still present, port still bound | `cleanup-verification.md` | Kill-and-check pattern |
| implementation patterns, detection commands, fix snippets, `set -e` + `||` | `preferred-patterns.md` | Catalog of gotchas with `rg`/`grep` detection and paired fixes |

## Instructions

Before implementing any pattern, read the repository CLAUDE.md and search the codebase for existing process-management patterns so the new code matches what is already there. Consistency with existing scripts beats local optimization.

### Step 1: Pick the pattern

Walk this decision tree. Pick exactly one pattern per task -- do not pre-emptively wrap a background process in a daemon, and do not add a trap handler for a script that runs for 50ms.

```
1. Are you starting a new process?
   YES -> Is the parent going to exit before the child?
          YES -> Daemonization (Step 3, load references/starting-processes.md)
          NO  -> Background start (Step 2, load references/starting-processes.md)
   NO  -> Continue

2. Do you need to kill or inspect a process someone else started?
   YES -> PID resolution (Step 4, load references/pid-resolution.md)
   NO  -> Continue

3. Are you writing a supervisor (script that manages children)?
   YES -> Signal + trap discipline (Step 5, load references/signals-and-traps.md)
   NO  -> Continue

4. Are you finishing a destructive operation (kill, rm, release)?
   YES -> Cleanup verification (Step 6, load references/cleanup-verification.md)
   NO  -> Stop. The task may not belong in this skill.
```

### Step 2: Start a background process

A background process in the same session (terminal open, parent stays alive). Load `references/starting-processes.md` for full rationale.

Minimum discipline:

1. **Redirect all three fds.** `cmd > log 2>&1 < /dev/null &` -- because an un-redirected background process inherits the terminal, and stray stdin reads block forever.
2. **Capture the PID defensively.** `$!` is the last backgrounded job's shell-level PID. If you wrap in `nohup`, you get the nohup PID, not the child. Re-query before acting on it (Step 4).
3. **Decide if `disown` is needed.** `disown $!` removes the job from the shell's job table so the shell does not send SIGHUP when it exits. Needed for scripts that start long-running children and return.

Minimal correct pattern (in-session, parent stays alive):

```bash
cmd > /tmp/cmd.log 2>&1 < /dev/null &
pid=$!
kill -0 "$pid" 2>/dev/null || { echo "failed to start" >&2; exit 1; }
```

Constraint: never use `cmd &` with no redirection in a non-interactive script -- because inherited stdout can deadlock when the terminal closes, and inherited stderr pollutes the parent's log.

Gate: run `kill -0 $pid` (no-op signal, checks existence) before treating the PID as valid -- because `$!` may name a process that died in the first millisecond (misspelled command, missing binary) and the script will happily `kill` a nonexistent PID later.

### Step 3: Daemonize a process

Daemonization is needed when the child must outlive the parent session (SSH logout, terminal close, script exit). Load `references/starting-processes.md` for the `setsid`/`nohup` differences.

Decision: do you need the child to be a session leader (independent of the parent's controlling TTY)?
- YES -> `setsid cmd > log 2>&1 < /dev/null &` -- creates a new session, detaches from the TTY.
- NO, just survive SIGHUP -> `nohup cmd > log 2>&1 < /dev/null &` -- ignores SIGHUP, inherits session.

Constraint: `nohup` prints `nohup: ignoring input and appending output to 'nohup.out'` if you do not redirect stdin/stdout/stderr. Redirect all three explicitly to keep logs where you control them -- because `nohup.out` in the working directory creates sprawl and may fail on read-only volumes.

### Step 4: Resolve the real PID

Load `references/pid-resolution.md` -- this is the most-frequent failure class in the skill.

Problem: `$!` tells you the shell-level PID of the last backgrounded job. That is often a wrapper (`nohup`, `time`, `stdbuf`, `env`, `sh -c '...'`) and not the process doing the work.

Resolve by querying the observable state:

| Goal | Command | Returns |
|------|---------|---------|
| Who owns TCP port N | `ss -tlnp "sport = :N"` | PID, command |
| Who owns UDP port N | `ss -ulnp "sport = :N"` | PID, command |
| Find by command name | `pgrep -fa 'pattern'` | PID(s) + full command line |
| Find by open file | `lsof -t /path/to/file` | PID(s) |
| Children of parent | `pgrep -P $parent_pid` | direct child PIDs |

Constraint: when you `kill` a wrapper PID, the wrapper dies and the orphaned child re-parents to PID 1 but keeps running. Always re-query after a kill -- the port still bound, the file still locked, `pgrep` still matches -- because assuming the kill worked is how production incidents start.

Gate: before declaring a process killed, run the same discovery query again and confirm it returns nothing -- see Step 6.

### Step 5: Signal and trap discipline

Load `references/signals-and-traps.md`.

Key rules:

1. **SIGTERM first, SIGKILL last.** SIGTERM lets the process run its cleanup (flush buffers, release locks, delete PID files). SIGKILL is unmaskable and leaves lock files behind. Send SIGTERM, wait a bounded interval (typically 10s), then escalate.
2. **Signal the process group, not the PID, when you want the whole tree.** `kill -TERM -$pgid` (note the leading dash). Alternatively launch with `setsid` so the group ID equals the child's PID.
3. **Subshells need their own trap setup.** A trap set in a parent does not fire inside `$(...)` or `(...)`. If the subshell has work to clean up, set the trap inside it.
4. **`exec cmd` replaces the shell.** All traps set before `exec` are gone -- because `exec` overlays the process image. If you need a wrapping shell with traps, do not `exec`; run the command as a child and `wait` for it.
5. **`trap 'handler' EXIT` fires on normal exit, `set -e` exit, and most signals -- but not SIGKILL and not `kill -9`.** Treat cleanup on SIGKILL as "impossible"; design the on-disk state to survive a hard kill.

Constraint: traps that call `exit` inside the handler can mask the real exit code. Use `trap 'rc=$?; cleanup; exit $rc' EXIT` to preserve it -- because losing the non-zero exit hides failures from CI.

### Step 6: Verify cleanup

Load `references/cleanup-verification.md`.

Every destructive operation on a process ends with a verification query that asks the system "is it really gone?" -- not "did kill return 0?"

Pattern:

```bash
# 1. send SIGTERM
kill -TERM "$pid" 2>/dev/null || true

# 2. wait with a bound (condition-based-waiting covers the generic shape;
#    here we specialize to the kill-and-check shape)
for _ in {1..10}; do
    kill -0 "$pid" 2>/dev/null || break
    sleep 1
done

# 3. escalate if still alive
if kill -0 "$pid" 2>/dev/null; then
    kill -KILL "$pid" 2>/dev/null || true
    sleep 1
fi

# 4. verify the observable state, not just the PID
if kill -0 "$pid" 2>/dev/null; then
    echo "FATAL: $pid still alive after SIGKILL" >&2
    exit 1
fi
# Also re-query whatever resource this process was holding:
# ss -tlnp "sport = :8080" | grep -q . && echo "port still bound"
```

Constraint: the check must target the resource (port, lock file, device), not just the PID -- because a re-spawned process under a different PID can re-bind the port immediately, and "PID gone" is not the same as "resource free".

Gate: if the verification query still returns the resource as held, do not proceed. Surface the state, do not auto-escalate beyond SIGKILL -- because the next steps (reboot, `fuser -k`, kernel intervention) require a human decision.

### Step 7: Strict-mode scripts

Default header for bash scripts that manage processes:

```bash
#!/usr/bin/env bash
set -euo pipefail

cleanup() {
    local rc=$?
    [[ -n "${child_pid:-}" ]] && kill -TERM "$child_pid" 2>/dev/null || true
    rm -f "${lock_file:-/dev/null}"
    exit "$rc"
}
trap cleanup EXIT
trap 'echo "ERROR: line $LINENO exit $?" >&2' ERR
```

Constraint: a command followed by `|| something` has its exit code masked -- `set -e` does not fire, and neither does the ERR trap. Use `|| true` only where failure is genuinely harmless, and prefer `if ! cmd; then handle; fi` when you want to act on the failure -- because silent-swallow `|| true` is the top failure mode in this domain (see `references/preferred-patterns.md`).

### Step 8: Verify

After implementing any pattern from Steps 2-7:

- Success path: child started, PID captured correctly, trap fires on normal exit.
- Failure path: child fails to start -> clear error, no orphan, no stale lock file.
- Kill path: SIGTERM received -> child exits cleanly; SIGKILL received -> no lock/PID file remains (if your design supports it) or the next run tolerates leftover state.
- Verification: port / lock / PID file is genuinely released, re-checked with `ss` / `ls` / `kill -0`.

## Error Handling

### Error: "kill: (1234): No such process" but the port is still bound

Cause: `$!` captured the PID of a wrapper (`nohup`, `sh -c`, `time`), not the real child. You killed the wrapper; the child re-parented to init and kept listening.

Solution: re-query with `ss -tlnp "sport = :PORT"` to get the real PID, then kill that. See `references/pid-resolution.md`. Fix the start-time code so the real PID is captured up front.

### Error: trap handler never fires

Cause: one of (a) trap was set inside a subshell that already exited, (b) the script was replaced by `exec`, (c) the process received SIGKILL, (d) the trap was overwritten by a later `trap 'other_handler' EXIT`.

Solution: move the `trap` into the shell that actually owns the state. Do not `exec` if you need traps. Accept that SIGKILL bypasses traps and design the on-disk state to survive it.

### Error: script hangs forever in `wait`

Cause: waiting on a PID that was already reaped, or on a PID that belongs to a different process group than the shell expects. Or SIGCHLD is being caught by a trap that never returns.

Solution: use `wait -n` (bash 4.3+) to wait for any child and return its exit code, or use a bounded loop with `kill -0` checks. Audit SIGCHLD traps.

### Error: `set -e` script "succeeds" but did not actually do the work

Cause: a command was followed by `|| true` or `|| :`, swallowing the real failure. Or the failing command was on the left side of a pipeline without `pipefail`.

Solution: remove `|| true` unless you genuinely do not care. Add `set -o pipefail`. See `references/preferred-patterns.md` for the `set -e` + `||` swallowing pattern with detection command.

## References

### Loading Table

| Task Type | Signal Keywords | Load |
|-----------|----------------|------|
| Starting any new process | "nohup", "disown", "setsid", "background", "daemonize", "&" | `starting-processes.md` |
| Killing or finding a process | "kill the process", "find the pid", "port still bound", "$!", "pgrep", "ss", "lsof" | `pid-resolution.md` |
| Writing signal handlers / traps | "trap", "SIGTERM", "SIGKILL", "cleanup handler", "EXIT trap", "exec" | `signals-and-traps.md` |
| Verifying a kill actually worked | "verify kill", "still running", "lock file", "stale pid", "port in use" | `cleanup-verification.md` |
| Reviewing a script for gotchas | "audit bash", "shell failure mode", "set -e", "|| true", "code review bash" | `preferred-patterns.md` |

### Reference Files

- `references/starting-processes.md` -- `&`, `nohup`, `disown`, `setsid`, daemonization, fd redirection.
- `references/pid-resolution.md` -- why `$!` lies, reliable PID capture, `ss`/`pgrep`/`lsof` recipes.
- `references/signals-and-traps.md` -- SIGTERM/SIGKILL, trap ordering, subshell inheritance, `exec` semantics, process groups.
- `references/cleanup-verification.md` -- kill-and-check pattern, state re-query after destructive operations.
- `references/preferred-patterns.md` -- concrete gotchas (`nohup` + `$!` wrapper PID, `set -e` + `||` swallowing, and more) with `rg` detection commands and paired fix snippets.
