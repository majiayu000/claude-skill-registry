---
name: gupp-propulsion
description: Interrupt controller converting polled to proactive agent execution. Per-runtime strategies, configurable thresholds, Deacon heartbeat supervision. Fights LLM passivity bias.
---

# GUPP Propulsion

The Gas Town Universal Propulsion Principle: **If there is work on your hook, YOU MUST RUN IT.**

GUPP is the interrupt controller of the Gastown chipset. In a real processor, the interrupt controller converts external events (keyboard press, network packet, timer tick) into CPU interrupts that force immediate handling. Without it, the CPU would have to poll every device continuously, wasting cycles on checks that almost always find nothing. GUPP does the same for AI coding agents: it converts the polled model (agent checks periodically, waits for user input) into an interrupt-driven model (work appears on hook, agent executes immediately).

## Why GUPP Exists

LLM coding assistants are trained through RLHF to be helpful, harmless, and honest. A side effect of this training is a strong bias toward *waiting for the user* -- asking clarifying questions, seeking confirmation before acting, pausing between steps for feedback. This is appropriate in interactive chat but catastrophic for autonomous multi-agent orchestration, where every moment of idle waiting is a moment the pipeline stalls.

Gastown discovered this empirically. Agents spawned with a work item would introduce themselves, summarize their understanding of the task, and then *wait*. They would ask "Shall I proceed?" when the answer was already on their hook. GUPP was created to override this trained passivity with an explicit, non-negotiable execution mandate.

The principle is simple: if you have hooked work, you do not wait. You do not ask for confirmation. You do not summarize your plan and pause for feedback. You begin execution immediately. This is physics, not politeness. Gastown is a steam engine and you are a piston.

## Activation Triggers

This skill activates when:

- An agent has work assigned to its hook and is not yet executing
- Stall detection identifies an agent with hooked work that has gone idle
- A new agent is spawned and needs GUPP enforcement injected into its context
- Runtime-specific GUPP strategy selection is needed
- Heartbeat supervision needs to be configured for active agents
- An agent has been nudged but remains stalled

## Per-Runtime Enforcement Strategies

GUPP enforcement adapts to each runtime's capabilities through the Runtime HAL. The HAL detects the active runtime and GUPP selects the highest-fidelity enforcement mechanism available.

### Claude Code

Claude Code provides the richest enforcement surface through its session hooks system.

| Layer | Mechanism | Details |
|-------|-----------|---------|
| Primary | `hook_injection` | SessionStart hook in `.claude/settings.json` injects GUPP rules and work context before the agent's first prompt. The agent starts in autonomous mode with zero setup latency. |
| Secondary | `prompt_preamble` | AUTONOMOUS WORK MODE template prepended to agent context. Reinforces GUPP when hooks fire inconsistently. |
| Enforcement | `deacon_heartbeat` | Witness runs the Deacon heartbeat patrol at 2-minute intervals. Detects agents that received hooks but stalled before beginning work. |
| Watchdog | `boot_restart` | If an agent remains stalled for 5+ minutes after hook injection, the watchdog requests a session restart. The restarted session re-fires the SessionStart hook, giving GUPP another chance. |

### Codex

Codex lacks session hooks. GUPP uses startup command injection as the primary strategy.

| Layer | Mechanism | Details |
|-------|-----------|---------|
| Primary | `startup_fallback` | `gt prime` command injected via tmux sends the agent's role, bead assignment, and GUPP rules through the startup context. |
| Secondary | `prompt_preamble` | AUTONOMOUS WORK MODE template in agent context. |
| Enforcement | `nudge_loop` | Witness sends nudges at 1-minute intervals for stall detection. Shorter interval compensates for lower hook fidelity. |
| Watchdog | `boot_restart` | Session restart after sustained stall. |

### Gemini

Gemini has no hook support and limited startup injection. GUPP relies on polling.

| Layer | Mechanism | Details |
|-------|-----------|---------|
| Primary | `prompt_preamble` | GUPP rules prepended to the agent's prompt context. This is the only reliable injection point. |
| Secondary | `polling` | Agent polls `state/hooks/{agentId}.json` on a timer to detect new work assignments. |
| Enforcement | `nudge_loop` | Witness sends nudges at the configured interval. |
| Watchdog | `boot_restart` | Session restart after sustained stall. |

### Strategy Selection

The Runtime HAL exposes `getGUPPStrategy()` which returns the primary strategy for the detected runtime. Other chipset skills call this method without knowing which runtime is active:

```typescript
const hal = detectRuntime();
const strategy = hal.getGUPPStrategy();

switch (strategy) {
  case 'hook_injection':
    // Claude Code path: inject via SessionStart hook
    break;
  case 'startup_fallback':
    // Codex path: inject via gt prime command
    break;
  case 'polling':
    // Gemini/unknown path: agent polls for assignments
    break;
}
```

## Configurable Thresholds

All GUPP timing parameters are configurable through the chipset YAML. Defaults are tuned for typical LLM agent behavior but can be adjusted per-project or per-runtime based on observed performance.

```yaml
gupp:
  thresholds:
    stall_detection: 300    # seconds (5 min) -- time before declaring an agent stalled
    nudge_interval: 120     # seconds (2 min) -- time between heartbeat checks
    restart_threshold: 600  # seconds (10 min) -- time before requesting session restart
```

### Threshold Reference

| Parameter | Default | Range | Purpose |
|-----------|---------|-------|---------|
| `stall_detection` | 300s (5 min) | 60s - 1800s | How long an agent can be idle with hooked work before it is considered stalled |
| `nudge_interval` | 120s (2 min) | 30s - 600s | How often the Deacon heartbeat checks each active agent |
| `restart_threshold` | 600s (10 min) | 120s - 1800s | How long a stalled agent can remain unresponsive before a restart is requested |

The Runtime HAL provides per-runtime defaults that override the chipset YAML defaults when a specific runtime is detected. For example, Claude Code uses a 120s stall threshold (the hook system makes stalls more detectable) while Gemini uses 300s (polling introduces latency).

## Deacon Heartbeat Pattern

The Deacon heartbeat is the supervision loop that enforces GUPP across all active agents. It runs independently of any individual agent session -- typically inside the witness-observer or as a standalone patrol process.

```
1. Timer fires (every nudge_interval seconds)
2. For each agent with an active hook:
   a. Read last_activity timestamp from state file
   b. If now - last_activity > stall_detection:
      i.  Send nudge via nudge-sync
      ii. Record nudge timestamp and count
3. For each previously nudged agent:
   a. If still stalled after nudge_interval:
      i.  Escalate to witness-observer
      ii. Witness sends health_escalation mail to mayor
4. For each agent past restart_threshold:
   a. Request boot restart via Runtime HAL
   b. Increment restart counter for this bead
   c. If restart_count >= 3: escalate to human
```

The full heartbeat protocol is documented in `heartbeat.md`.

## Observable Metrics

GUPP exposes these metrics for skill-creator's pattern detection and adaptive learning. Over time, skill-creator proposes refinements to thresholds and strategy selections based on observed effectiveness.

### GUPP Response Time

Time elapsed from hook assignment to first work activity (first commit, first file edit, or first status update). Measured per-agent, per-session.

```
gupp_response_time_seconds{agent="polecat-alpha", runtime="claude"} 12.4
```

Ideal: under 30 seconds for Claude Code (hook injection), under 60 seconds for Codex (startup fallback), under 120 seconds for Gemini (polling).

### Nudge Effectiveness

Boolean per-nudge: did the agent resume work within `nudge_interval` seconds after receiving the nudge? Tracks whether nudges are actually fixing stalls or just adding noise.

```
gupp_nudge_effective{agent="polecat-alpha", nudge_id="n-001"} true
gupp_nudge_effective{agent="polecat-beta", nudge_id="n-002"} false
```

A nudge effectiveness rate below 50% suggests the stall detection threshold is too aggressive (false positives) or the agent is genuinely stuck and needs restart rather than nudging.

### Strategy Success Rate

Per-runtime success rate: what percentage of GUPP activations result in the agent beginning work within the expected response window? Tracks which primary strategy produces the fastest, most reliable GUPP response.

```
gupp_strategy_success_rate{runtime="claude", strategy="hook_injection"} 0.94
gupp_strategy_success_rate{runtime="codex", strategy="startup_fallback"} 0.78
gupp_strategy_success_rate{runtime="gemini", strategy="polling"} 0.65
```

### Stall Frequency

How often agents stall per session. A session with zero stalls is ideal. High stall frequency may indicate a systemic issue (context window exhaustion, ambiguous work items, missing dependencies).

```
gupp_stalls_per_session{runtime="claude"} 0.3
gupp_stalls_per_session{runtime="codex"} 1.1
```

### Learning Feedback Loop

Skill-creator observes these metrics across sessions and proposes adjustments:

1. **Threshold tuning:** If stall detection fires frequently but nudge effectiveness is low, increase `stall_detection` to reduce false positives
2. **Strategy switching:** If a runtime's primary strategy has low success rate, recommend switching to the secondary
3. **Interval optimization:** If nudge effectiveness is high but response time is long, decrease `nudge_interval` for faster recovery
4. **Restart policy:** If restarts consistently fix stalls, the agent may need better initial context (improve hook injection quality)

## Safety Boundaries

### GUPP Is Advisory in GSD

GUPP enforcement is ADVISORY within GSD's structured workflow. The GSD orchestrator's phase gates, verification steps, and checkpoint protocols take precedence over GUPP urgency. If a GSD checkpoint requires human verification, GUPP does not override it. If a phase gate blocks progress pending approval, GUPP does not force execution past the gate.

The hierarchy is:

```
GSD orchestrator (highest authority)
  |
  v
Phase gates and checkpoints
  |
  v
GUPP propulsion (execution enforcement)
  |
  v
Agent autonomy (lowest -- must obey all above)
```

GUPP operates between the orchestrator's structural gates. Within a phase, within an approved plan, within a committed task -- GUPP demands immediate execution. But it never overrides the orchestrator's decision about *what* to execute or *when* a phase is complete.

### Restart Limits

The watchdog restart mechanism has strict limits to prevent infinite restart loops:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Max restart threshold | 1800s (30 min) | Hard cap on how long before restart. Cannot be configured higher. |
| Max restarts per bead | 3 | After 3 restarts for the same work item, escalation to human is mandatory. |
| Restart cooldown | 60s | Minimum time between consecutive restarts for the same agent. |

### Human Escalation

After 3 restarts for the same bead without resolution, GUPP stops attempting automated recovery and escalates to a human operator:

```typescript
if (restartCount >= 3) {
  const escalation: AgentMessage = {
    from: witnessId,
    to: 'mayor',
    channel: 'mail',
    payload: `HUMAN_ESCALATION: ${beadId} has stalled ${restartCount} times. ` +
             `Automated recovery exhausted. Requires human intervention.`,
    timestamp: new Date().toISOString(),
    durable: true,
  };
  // Mayor surfaces this to the human operator
}
```

The mayor receives the escalation and surfaces it through whatever channel the human is monitoring (terminal output, notification file, log). GUPP does not attempt a fourth restart.

### No Data Destruction

GUPP enforcement never destroys work in progress. Restarts preserve the agent's branch and commits. Nudges are non-destructive signals. Escalations are informational. At no point does GUPP delete files, reset branches, or discard uncommitted changes.

## Integration with Other Gastown Skills

| Skill | How GUPP Integrates |
|-------|-------------------|
| `runtime-hal` | HAL provides `getGUPPStrategy()`, stall thresholds, and restart capability detection |
| `polecat-worker` | Polecats are the primary GUPP enforcement target -- they must act on hooked work |
| `witness-observer` | Witness runs the Deacon heartbeat loop that enforces GUPP timing |
| `nudge-sync` | GUPP sends nudges through the nudge channel for stall recovery |
| `mail-async` | GUPP escalations use durable mail for mayor notifications |
| `beads-state` | GUPP reads agent activity timestamps and hook status from state files |
| `hook-persistence` | GUPP monitors hook assignments to detect when agents have pending work |
| `mayor-coordinator` | Mayor receives escalations and decides on restarts or reassignment |
| `sling-dispatch` | Sling sets hooks that activate GUPP enforcement for the assigned agent |

## References

- `references/gastown-origin.md` -- The GUPP principle from Gastown, how it fights model training bias
- `references/boundaries.md` -- Advisory nature, restart limits, human escalation rules
- `heartbeat.md` -- Deacon heartbeat supervision pattern and integration points
