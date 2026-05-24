---
name: witness-observer
description: PMU observation pattern for agent health monitoring. Runs patrol loops, detects stalled agents, sends nudges, and escalates persistent failures to the mayor. Never modifies agent work or resolves conflicts.
---

# Witness Observer

Per-rig observer that monitors polecat health and reports anomalies. The witness is the PMU (Performance Monitoring Unit) of the Gastown chipset -- it watches execution units for stalls, detects degraded performance, and raises alerts without interfering with computation. The witness is strictly read-only with respect to agent work. It observes and reports; it never modifies.

## Activation Triggers

This skill activates when:

- The agent is assigned to monitor a rig's worker agents
- Multiple polecats are running and health monitoring is needed
- Stall detection is required for long-running work items
- The mayor needs a supervisory agent to watch active polecats

## Core Capabilities

### Patrol Loop

The witness runs a periodic patrol that checks all active agents in its rig for health indicators.

**Patrol cycle:**

```
SCAN            EVALUATE         ACT              WAIT
  |                |               |                |
  v                v               v                v
list agents -> check each  ->  nudge/escalate -> sleep interval
(active ones)   for stalls     if needed         (default 5 min)
```

**Implementation:**

```typescript
const state = new StateManager({ stateDir: '.chipset/state/' });
const patrolInterval = 5 * 60 * 1000; // 5 minutes (configurable)
const stallThreshold = 30 * 60 * 1000; // 30 minutes (configurable)

async function patrol(): Promise<void> {
  // Get all agents that should be working
  const agents = await state.listAgents({ role: 'polecat' });
  const active = agents.filter(a => a.status === 'active');

  for (const agent of active) {
    const hook = await state.getHook(agent.id);
    if (!hook || hook.status !== 'active') continue;

    // Check last activity timestamp
    const lastActivity = new Date(hook.lastActivity).getTime();
    const elapsed = Date.now() - lastActivity;

    if (elapsed > stallThreshold) {
      await handleStall(agent, hook, elapsed);
    }
  }
}
```

### Stall Detection

A stall is detected when an agent has hooked work but has not updated its activity timestamp within the threshold period (default 30 minutes).

**Stall indicators:**

| Indicator | What It Means |
|-----------|--------------|
| Hook active, no activity for 30+ min | Agent may be stuck, crashed, or idle |
| Agent status is 'active' but hook timestamp stale | Session may have ended without cleanup |
| Multiple consecutive patrol cycles with no change | Persistent stall, needs escalation |

**Stall classification:**

```typescript
type StallSeverity = 'warning' | 'alert' | 'critical';

function classifyStall(elapsed: number, nudgesSent: number): StallSeverity {
  if (nudgesSent >= 2) return 'critical';    // Nudged twice, still stalled
  if (elapsed > 60 * 60 * 1000) return 'alert';  // Over 1 hour
  return 'warning';                            // First detection
}
```

### Nudge Protocol

When a stall is detected, the witness follows a graduated escalation protocol.

**Step 1 -- Send nudge to stalled agent:**

```typescript
async function handleStall(
  agent: AgentIdentity,
  hook: HookState,
  elapsed: number
): Promise<void> {
  const severity = classifyStall(elapsed, getNudgeCount(agent.id));

  if (severity === 'warning') {
    // First nudge: ask agent if it's still working
    const nudge: AgentMessage = {
      from: witnessId,
      to: agent.id,
      channel: 'nudge',
      payload: `HEALTH_CHECK: no activity for ${Math.floor(elapsed / 60000)}m on ${hook.workItem?.beadId}`,
      timestamp: new Date().toISOString(),
      durable: false,
    };
    // Write nudge file
    recordNudge(agent.id);
    return;
  }

  if (severity === 'alert' || severity === 'critical') {
    // Escalate to mayor
    await escalateToMayor(agent, hook, severity, elapsed);
  }
}
```

**Step 2 -- Wait for response (next patrol cycle):**

If the agent responds to the nudge (updates its hook activity timestamp or sends mail), the stall is resolved. No further action needed.

**Step 3 -- Escalate if unresolved:**

```typescript
async function escalateToMayor(
  agent: AgentIdentity,
  hook: HookState,
  severity: StallSeverity,
  elapsed: number
): Promise<void> {
  const escalation: AgentMessage = {
    from: witnessId,
    to: 'mayor',
    channel: 'mail',
    payload: `STALL_${severity.toUpperCase()}: ${agent.id} idle ${Math.floor(elapsed / 60000)}m on ${hook.workItem?.beadId}`,
    timestamp: new Date().toISOString(),
    durable: true,
  };
  // Write escalation to .chipset/state/mail/mayor/{timestamp}-{witnessId}.json
}
```

### Health Reporting

The witness provides aggregate health summaries when queried by the mayor.

```typescript
interface RigHealthReport {
  rigName: string;
  timestamp: string;
  totalAgents: number;
  activeAgents: number;
  stalledAgents: number;
  idleAgents: number;
  terminatedAgents: number;
  stalledDetails: Array<{
    agentId: string;
    beadId: string;
    stalledMinutes: number;
    nudgesSent: number;
  }>;
}
```

## Communication Protocol

### Messages the Witness SENDS

| Channel | Target | Purpose | Durability |
|---------|--------|---------|------------|
| `nudge` | Stalled polecats | "Are you still working?" health check | Non-durable |
| `mail` | Mayor | Stall alerts (warning, alert, critical) | Durable |
| `mail` | Mayor | Health report summaries | Durable |

### Messages the Witness RECEIVES

| Channel | Source | Content |
|---------|--------|---------|
| `mail` | Mayor | Instructions (adjust thresholds, focus on specific agent) |
| `mail` | Polecats | Status responses to nudges |

## Error Handling

### False Positive Stalls

If an agent is working but updates are slow (large commits, long test runs), the witness may detect a false positive. The nudge protocol handles this: the agent responds to the nudge, and the witness records the response as activity.

### Witness Restart

If the witness itself restarts, it resumes patrol from scratch. It reads current agent and hook state from the filesystem -- there is no witness-specific state that needs recovery. The patrol loop is stateless between cycles.

### Unresponsive Agent

If an agent does not respond to two nudges across two patrol cycles, the witness sends a `critical` escalation to the mayor. The mayor decides whether to terminate and replace the agent.

## Boundary: What the Witness Does NOT Do

The witness NEVER:

- **Modifies agent work** -- does not edit files, change branches, or alter code
- **Resolves conflicts** -- conflict resolution is outside the observer's scope
- **Terminates agents** -- only the mayor can terminate; the witness recommends
- **Reassigns work** -- hook management belongs to the mayor
- **Changes agent status** -- the witness reads status but does not write it (except its own)
- **Runs tests or builds** -- the witness observes; it does not validate output quality

The witness is a sensor. It detects anomalies and reports them. It does not act on them.

## Integration with Other Gastown Skills

| Skill | Relationship |
|-------|-------------|
| `mayor-coordinator` | Witness reports stalls and health TO mayor |
| `polecat-worker` | Witness monitors polecat health, sends nudges |
| `refinery-merge` | Witness can observe refinery queue depth and merge failures |
| `beads-state` | Witness reads state via StateManager (read-only) |

## References

- `references/gastown-origin.md` -- How this pattern derives from Gastown's witness.go patrol
- `references/boundaries.md` -- Read-only constraints and observation-only scope
