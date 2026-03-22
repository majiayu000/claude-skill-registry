---
disable-model-invocation: true
name: process-cleanup
description: This skill should be used when the user asks to "find zombies", "kill zombie processes", "clean up zombies", "check for zombie processes", "reap zombies", or mentions zombie process detection, cleanup, or process state monitoring.
---

# Process Cleanup

Detect and reap zombie processes using `/bin/ps`.

## Background

A zombie (state `Z`) is a process that has exited but whose parent hasn't called `wait()` to collect its exit status. Zombies consume no CPU or memory, but they hold a PID slot and can accumulate. You can't `kill` a zombie — it's already dead. The only remedies are:

1. **Signal the parent** with `SIGCHLD` so it reaps the child
2. **Kill the parent** so `init`/`launchd` adopts and reaps the orphan

## Important: use `ps` for process state queries

Always use `ps` (BSD) for process state queries. If `ps` is aliased, use `/bin/ps` to bypass it.

```bash
# List zombies
/bin/ps ax -o pid,state,ppid,user,command | awk '$2 ~ /Z/'

# List all processes with state
/bin/ps ax -o pid,state,ppid,etime,args
```

## Usage

Run the helper script to scan for zombies:

```bash
# Detect only (default) — list zombie processes
bash scripts/kill-zombies.sh

# Reap zombies — send SIGCHLD to parent processes
bash scripts/kill-zombies.sh --kill
```

## Safety

- Default mode is **detect-only** — no processes are signaled
- With `--kill`, the script sends `SIGCHLD` to parent processes (non-destructive nudge to reap)
- If a parent ignores `SIGCHLD`, the script reports the parent PID — **confirm with the user** before killing it
- Never kill PID 1 (`init`/`launchd`)
