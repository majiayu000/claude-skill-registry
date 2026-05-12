---
name: system-tuning
description: 'Restore system responsiveness via safe, ordered process cleanup and agent-swarm hygiene.'
practices: [sre, resilience-patterns, ebpf-observability]
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: execution
  dependencies: []
output_contract: "stdout: triage report; stderr: warnings on protected processes"
---
# System Tuning Skill

> **Quick Ref:** Triage a sluggish dev box without nuking work in flight. Order: diagnose → cleanup zombies and exited sessions → kill stuck children → fix confused parents → renice survivors → verify.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

When the box feels slow — high load, swap thrash, agent sprawl, or compile storms — work the kill hierarchy from the safest move outward and treat parent agents as the real cleanup target, not their children.

## When To Use

| Symptom | Use This Skill |
|---|---|
| Load average drifts above core count and stays there | yes |
| Multiple agents respawn the same `cargo` / `cc1plus` after kills | yes — see [whack-a-mole-anti-pattern.md](references/whack-a-mole-anti-pattern.md) |
| Tmux / zellij session list grew past sanity | yes — see [agent-swarm-cleanup.md](references/agent-swarm-cleanup.md) |
| One process is genuinely the hot path | use `/perf` first; come back if cleanup is still needed |
| Production incident on a server you do not own | escalate; do not run kills blind |

## Method

The skill drives three loops, in order. Each loop has a check, an action set, and a verification.

### 1. Diagnose Without Touching

Read pressure metrics before signalling anything.

```bash
uptime && nproc
cat /proc/pressure/cpu /proc/pressure/io /proc/pressure/memory 2>/dev/null
ps -eo stat | grep -c '^Z'                  # zombie count
ps aux --sort=-%cpu | head -10
```

Capture this as the baseline. Every kill below should move at least one of these numbers; if nothing moves, you killed the wrong thing.

### 2. Walk the Kill Hierarchy

Work from least-invasive to most-invasive. Full ordering and signal escalation rules live in [references/kill-hierarchy.md](references/kill-hierarchy.md).

```
zombies & exited sessions   →  reap, no risk
stuck child processes       →  SIGTERM, wait 3s, escalate to SIGKILL
confused parent agents      →  kill the parent so it stops respawning children
renice the survivors        →  give interactive work room without termination
```

Stop at the first loop that restores responsiveness. Do not run later steps "just in case."

### 3. Clean Up The Swarm

If the box hosts multiple coding agents, the second-order problem is duplicated work, not slow code. The patterns to look for are catalogued in [references/agent-swarm-cleanup.md](references/agent-swarm-cleanup.md): competing build target dirs, orphaned MCP children, abandoned tmux/zellij sessions, agents older than the work they were spawned for.

### 4. Verify

After every loop, re-read the same commands from step 1. Write a one-line delta:

```
load: 38.4 -> 12.1   |   cpu_pressure_avg10: 61% -> 8%   |   zombies: 14 -> 0
```

No delta written → the cleanup is not done.

## Quick-Start Checklist

```bash
# Baseline
uptime; cat /proc/pressure/cpu

# Reap free wins
ps -eo stat | grep -c '^Z'                                    # zombies present?
zellij list-sessions 2>&1 | grep -c EXITED                    # dead sessions present?
zellij delete-all-sessions --yes 2>/dev/null

# Find stuck children (12h+ tests, idle dev servers)
ps -eo pid,etimes,args --sort=-etimes | awk '$2 > 43200' | head

# Find confused parents (16h+ agents)
ps -eo pid,etimes,args | grep -E 'claude|codex' | awk '$2 > 57600'

# Renice live compilation rather than killing it
for pid in $(pgrep -f /bin/cargo) $(pgrep cc1plus); do
  renice 19 -p "$pid" 2>/dev/null
  ionice -c 3 -p "$pid" 2>/dev/null
done

# Verify
sleep 10 && uptime && cat /proc/pressure/cpu
```

## Protected Processes

Never signal these without explicit operator approval:

```
systemd, sshd, dbus, cron
postgres, mysql, redis, nginx, caddy
docker, containerd, k3d, kubelet
the multiplexer your sessions live inside (tmux server, wezterm-mux-server, zellij)
```

If unsure, leave it running and document the candidate instead. The cost of a wrong kill is much higher than the cost of waiting.

## Output

Run reports go to `.agents/system-tuning/YYYY-MM-DD-triage.md`. Each report includes:

1. Baseline metrics (uptime, pressure, zombies, top CPU)
2. Kill log with reason per signal
3. Renice / ionice changes
4. Post-cleanup metrics
5. Anything escalated for operator decision

## See Also

- [perf](../perf/SKILL.md) — Optimize a single hot path once the system is responsive
- [bug-hunt](../bug-hunt/SKILL.md) — Investigate why a process loops or hangs
- [scope](../scope/SKILL.md) — Lock edit scope before running cleanup in a shared workspace

## Reference Documents

- [references/kill-hierarchy.md](references/kill-hierarchy.md)
- [references/whack-a-mole-anti-pattern.md](references/whack-a-mole-anti-pattern.md)
- [references/agent-swarm-cleanup.md](references/agent-swarm-cleanup.md)

## Attribution

Methodology pattern-adopted from the jsm `system-performance-remediation` skill. See `LICENSE.md` in this skill directory for full attribution. No source text reused.
