---
name: localsetup-tmux-shared-session-workflow
description: Server/ops in tmux; use tmux_ops tool to pick session (idle = prompt on current line) and probe sudo; run commands only in chosen session. Supports REMOTE_TMUX_HOST for VMs/remote/Docker.
metadata:
  version: "4.0"
---

# tmux shared session workflow (ops)

**Rule:** Any request that involves running commands on the host uses this workflow. Sudo is always assumed required. Use the **tmux_ops** tool to pick session and probe; do not infer busy from `tmux ls` or parse raw capture yourself.

## Tool (use this)

- **Entrypoint:** From repo root run `./_localsetup/tools/tmux_ops` (or set `REMOTE_TMUX_HOST` to run the same tool on a remote host via SSH; see Remote below).
- **Pick session:** `./_localsetup/tools/tmux_ops pick` → JSON e.g. `{"session": "ops", "reason": "idle"}` or `{"reason": "created"}` or `{"reason": "waiting_sudo"}`. Use that `session` for the whole run.
- **Probe sudo:** `./_localsetup/tools/tmux_ops probe -t <session>` → JSON `{"sudo": "ready"}` or `{"sudo": "password_required"}`.
- **Send command:** `./_localsetup/tools/tmux_ops send -t <session> '...'` sends the command and applies a short pylon-guard delay (default 0.5 s) to prevent commands racing ahead of output on high-latency links. Does **not** wait for the command to finish unless `--wait` is passed.
- **Send and wait:** `./_localsetup/tools/tmux_ops send -t <session> --wait '...'` sends and then polls for idle. Returns the moment the prompt reappears. Use for commands expected to finish in < 30 s.
- **Wait (standalone):** `./_localsetup/tools/tmux_ops wait -t <session> [--timeout N]` polls pane for idle. Use after `send` (without `--wait`) for long-running ops. Returns `{"idle": true, "elapsed_s": X, "polls": N}` or `{"idle": false, "timed_out": true, "cursor_line": "..."}`.
- **Idle definition:** Idle = cursor line matches a shell prompt (`$` or `#`) AND cursor Y moved from its pre-send position (cursor-delta guard prevents false positives).

### Subcommand reference

| Subcommand | Key args | Returns |
|---|---|---|
| `pick` | | `{session, reason}` |
| `probe -t SESSION` | | `{sudo: ready\|password_required\|unknown}` |
| `send -t SESSION CMD` | `--delay`, `--wait`, `--wait-timeout`, `--idle-re` | `{sent, delay_s[, idle, elapsed_s, polls, timed_out, cursor_line]}` |
| `wait -t SESSION` | `--timeout`, `--idle-re`, `--pre-cursor-y` | `{idle, elapsed_s, polls[, timed_out, cursor_line]}` |

Optional: `--idle-re PATTERN` overrides the prompt regex (also env `TMUX_OPS_IDLE_RE`). `--pre-cursor-y N` enables the cursor-delta guard on standalone `wait` calls.

## Sequence (follow exactly)

1. **Pick session.** Run `./_localsetup/tools/tmux_ops pick`. Parse JSON; use the returned `session` for the whole run. If the tool errors, report and stop.

2. **Show attach command immediately.** Right after pick (whether the session was created or already existed), display the join command in a **copy-paste code block** so the user can attach at any time. Do not wait for the user to confirm they joined.
   - Put this in a fenced code block:
     `tmux new-session -A -s <session>`
   - **If pick returned `reason: "waiting_sudo"`:** cancel any abandoned command first: send `tmux send-keys -t <session> C-c`, wait ~0.5 s, then run the probe.
   - Then run the probe.

3. **Gate on probe only.** If the probe returns `"sudo": "password_required"`: stop. Ask the user to attach to the session, enter the password in that pane, and reply "sudo ready". Only after they reply may you send the first command. If `"sudo": "ready"`, continue to step 4.

4. **Send one step at a time.** Send one logical step at a time.
   - **Short command (< 30 s expected):** use `send --wait`. Returns the moment idle is confirmed; no sleep needed.
   - **Long command (builds, installs, deploys):** use `send` (no `--wait`), then call `wait --timeout N` where N is your best estimate.
     - `idle=true` → continue to next step.
     - `timed_out=true` → inspect `cursor_line` field; extend wait, read log, or escalate.
   - **Never use arbitrary `sleep` calls as a completion signal.**
   - Use a log: `/tmp/agent-<session>-YYYYmmdd-HHMMSS.log` (e.g. `|& tee -a $LOG`). Read the log yourself.

5. **Run.** Commands go via `./_localsetup/tools/tmux_ops send -t <session> '...'`. Use a log path. Never run those commands in the agent shell.

6. **Re-gate if sudo expires.** If a later command fails (e.g. sudo timeout), run the probe again; if `password_required`, stop and ask for "sudo ready"; only then continue.

## Waiting strategy

```
After send, choose:

  Command expected in < 30 s?
    YES → send --wait
          Returns idle=true the moment done. Continue immediately.

  Command expected in > 30 s or unknown?
    → send (no --wait), then wait --timeout N
      idle=true      → continue
      timed_out=true → inspect cursor_line; extend wait, read log, or escalate

  Need exact latency, zero polling (advanced)?
    → append "; tmux wait-for -S done-$$" to command
      then run: tmux wait-for done-<PID>
      Blocks until shell signals completion. Use only when you fully control the command string.
```

### Sentinel PS1 (advanced, zero false positives)

If you want completely unambiguous idle detection, inject a known prompt right after `pick`:

```bash
tmux_ops send -t ops 'export PS1="__OPS__\$ "'
# Then pass --idle-re '^__OPS__[$#]\s*$' to all subsequent wait calls
```

This makes the prompt unique and removes any chance of a false match on command output.

## Remote (VMs, remote SSH, Docker)

When the tmux server runs on a different host (e.g. Cursor on laptop, tmux on VM or remote server):

- Set **REMOTE_TMUX_HOST** to that host (e.g. `export REMOTE_TMUX_HOST=sh0t`). Optionally **REMOTE_TMUX_CWD** to the repo path on the remote (default `/opt/devzone/devops`).
- Run `tmux_ops pick`, `probe`, `send`, and `wait` as usual; the wrapper runs the tool over SSH and returns the same JSON.

## Checklist

| Step | Do | Do not |
|------|-----|--------|
| 1 | Run `tmux_ops pick`; use returned session for whole run. | Infer session from `tmux ls` or "(attached)". |
| 2 | Right after pick, show attach in code block. If `reason: waiting_sudo`, send C-c first, then probe. | Wait for "I joined"; skip cancel when `waiting_sudo`. |
| 3 | If probe says `password_required`, stop and ask user; only then send commands. If ready, continue. | Send commands before user says "sudo ready" when probe said `password_required`. |
| 4 (short cmd) | `send --wait`; continue on `idle=true`. | Sleep then assume done. |
| 4 (long cmd) | `send`, then `wait --timeout N`; handle `timed_out`. | Guess a sleep duration. |
| 5 | Run in chosen session via `tmux_ops send`; tee to log; read log. | Run in agent shell; skip log. |
| 6 | If sudo expired, probe again; if `password_required`, stop. | Assume sudo still valid. |

## Session and log

- Session: the one returned by `tmux_ops pick` (e.g. `ops` or `ops1`).
- Log: `/tmp/agent-<session>-YYYYmmdd-HHMMSS.log`. Commands: `... |& tee -a $LOG`. After run: read log (e.g. `tail -n 200` that file).

## Hard rules

1. Server/ops commands run only in tmux. Use `tmux_ops` to pick session and probe; never in the agent shell.
2. If probe returns ready, continue immediately; do not stop for a chat "sudo ready". Only stop when probe returns `password_required`.
3. If `password_required`: ask user to enter password in the ops pane and reply "sudo ready"; then proceed.
4. Right after pick, display the attach command in a copy-paste code block; do not wait for user to confirm join before probing.
5. Capture output to the log path; the agent reads the log. State what you are about to do before running commands.
6. Never use `sleep` as a completion signal. Use `send --wait` or `wait --timeout N`.
