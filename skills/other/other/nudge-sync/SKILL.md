---
name: nudge-sync
description: Synchronous immediate signaling channel for inter-agent communication. Implements latest-wins single-file nudge pattern for health checks, stall detection, and urgent pings.
---

# Nudge Sync

Lightweight synchronous signaling for multi-agent orchestration. Each agent has a single nudge file that is overwritten on every new nudge -- latest wins, no accumulation. Agents check their nudge file on every state poll, making this the fastest communication channel in the chipset.

## Purpose

Nudge is the low-bandwidth, urgent signal channel in the Gastown chipset -- the SMI (System Management Interrupt) equivalent. It carries health checks from the witness, stall recovery prompts, and urgent coordination signals. Unlike mail (which accumulates), nudge is intentionally ephemeral: only the latest nudge matters.

The witness uses nudge to implement Gastown's Deacon heartbeat pattern. When an agent has hooked work but hasn't reported activity, the witness sends a nudge asking "are you working?" If the agent doesn't respond within the nudge interval, the witness escalates to the mayor via mail.

## Filesystem Contract

```
.chipset/state/nudge/{agent-id}/latest.json
```

Each agent has a dedicated nudge directory containing exactly one file: `latest.json`. This file is overwritten on every new nudge. Reading the file always returns the most recent nudge (or null if no nudge has been sent).

**Example paths:**

```
.chipset/state/nudge/polecat-alpha/latest.json
.chipset/state/nudge/mayor-a1b2c/latest.json
.chipset/state/nudge/refinery-f5g6h/latest.json
```

## Message Format

```json
{
  "from": "witness-d3e4f",
  "type": "health_check",
  "message": "You have hooked work (gt-abc12). Are you working on it?",
  "timestamp": "2026-03-05T10:35:00Z",
  "requires_response": true
}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `from` | string | yes | Sender agent ID |
| `type` | string | yes | Nudge type (see Nudge Types below) |
| `message` | string | yes | Human-readable nudge content |
| `timestamp` | string | yes | ISO 8601 creation timestamp |
| `requires_response` | boolean | yes | Whether the recipient must respond |

### Nudge Types

| Type | Sender | Purpose |
|------|--------|---------|
| `health_check` | witness | Verify agent is alive and working |
| `stall_warning` | witness | Agent has not reported activity |
| `priority_change` | mayor | Work item priority has changed |
| `abort` | mayor | Stop current work immediately |
| `sync_request` | any | Request state synchronization |

## Sending a Nudge

The send protocol overwrites the recipient's `latest.json` atomically.

### Protocol

1. **Construct** the nudge JSON with all required fields
2. **Serialize** with sorted keys for deterministic output
3. **Write** to a temporary file: `.chipset/state/nudge/{agent-id}/.nudge.tmp`
4. **Fsync** the temporary file
5. **Rename** to `latest.json` (atomic overwrite)

### Pseudocode

```typescript
async function sendNudge(nudge: NudgeMessage): Promise<void> {
  const nudgeDir = join(stateDir, 'nudge', nudge.to);
  await mkdir(nudgeDir, { recursive: true });

  const filePath = join(nudgeDir, 'latest.json');
  const content = serializeSorted(nudge);
  const tmpPath = join(nudgeDir, '.nudge.tmp');

  const fd = await open(tmpPath, 'w');
  try {
    await fd.writeFile(content, 'utf-8');
    await fd.sync();
  } finally {
    await fd.close();
  }
  await rename(tmpPath, filePath);
}
```

Note: The nudge message includes a `to` field implicitly via the directory path. The JSON itself does not store `to` -- the recipient is identified by the directory.

## Receiving a Nudge

### Polling

Agents read their `latest.json` on every state poll cycle. If the file exists and has a newer timestamp than the last processed nudge, the agent processes it.

```typescript
async function checkNudge(agentId: string): Promise<NudgeMessage | null> {
  const filePath = join(stateDir, 'nudge', agentId, 'latest.json');
  return readJson<NudgeMessage>(filePath);
}
```

### Processing Decision

When an agent reads a nudge, it decides how to respond based on type and `requires_response`:

```typescript
async function processNudge(agentId: string, lastSeen: string): Promise<void> {
  const nudge = await checkNudge(agentId);
  if (!nudge) return;
  if (nudge.timestamp <= lastSeen) return; // Already processed

  switch (nudge.type) {
    case 'health_check':
      if (nudge.requires_response) {
        await respondToNudge(agentId, nudge);
      }
      break;
    case 'stall_warning':
      // Log warning, update activity timestamp
      await updateActivity(agentId);
      if (nudge.requires_response) {
        await respondToNudge(agentId, nudge);
      }
      break;
    case 'abort':
      // Stop current work, clear hook
      await abortWork(agentId);
      break;
    case 'priority_change':
      // Re-read hook for updated priority
      await refreshHook(agentId);
      break;
    case 'sync_request':
      // Synchronize state
      await syncState(agentId);
      break;
  }
}
```

## Responding to a Nudge

When `requires_response` is true, the agent must write a response within the nudge interval. Responses are written to the sender's nudge directory (the sender becomes the recipient).

### Response Protocol

1. Read the incoming nudge
2. Construct a response nudge with `type: "nudge_response"`
3. Write to the sender's nudge directory as `latest.json`

```typescript
async function respondToNudge(
  agentId: string,
  incoming: NudgeMessage
): Promise<void> {
  const response: NudgeMessage = {
    from: agentId,
    type: 'nudge_response',
    message: `Acknowledged. Working on hooked bead. Last activity: ${new Date().toISOString()}`,
    timestamp: new Date().toISOString(),
    requires_response: false,
  };
  // Write to the sender's nudge directory
  await sendNudge({ ...response, to: incoming.from });
}
```

### Nudge Interval

The nudge interval defines how long a sender waits for a response before escalating. Default: 60 seconds. Configurable per-agent in the chipset configuration.

If no response arrives within the interval:
1. Witness logs the agent as unresponsive
2. Witness sends a `health_escalation` mail to the mayor
3. Mayor decides whether to reassign the hooked work

## Deacon Heartbeat Pattern

The witness implements Gastown's Deacon pattern using nudge:

```
[Witness] --health_check--> [Polecat]
                                |
                          (working? yes)
                                |
[Witness] <--nudge_response-- [Polecat]
```

If the polecat doesn't respond:

```
[Witness] --health_check--> [Polecat]
                                |
                          (no response)
                                |
[Witness] --health_escalation (mail)--> [Mayor]
                                            |
                                      (reassign work)
```

The witness runs the Deacon loop on a configurable interval, checking all agents with active hooks.

## Latest-Wins Semantics

Nudge intentionally discards history. If two nudges arrive in rapid succession, only the second one is visible to the recipient. This is by design:

- Health checks only need the latest status
- Stall warnings escalate through mail if unresolved
- Abort signals are terminal -- only the most recent matters
- No message queue to overflow or drain

This contrasts with mail-async, which accumulates all messages.

## Cross-Channel Integration

Nudge works with the other channels in the escalation flow:

1. **Hook set** (hook-persistence): Agent gets work
2. **Nudge sent** (nudge-sync): Witness checks if agent is active
3. **No response** within interval
4. **Mail sent** (mail-async): Witness escalates to mayor
5. **Hook reassigned** (hook-persistence): Mayor moves work to another agent

Nudge is the detection layer. Mail is the escalation layer. Hook is the assignment layer.

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Nudge directory doesn't exist | Created automatically on first send |
| Corrupt `latest.json` | Returns null, treated as no nudge pending |
| Concurrent nudge writes | Last writer wins (atomic rename) |
| Agent terminated | Nudge file persists but is stale (timestamp check prevents reprocessing) |
| Response timeout | Escalation via mail-async to mayor |

## Constraints

- **Filesystem only:** No sockets, no tmux, no network
- **Latest-wins:** Only one nudge file per agent. No accumulation, no history
- **Single file:** Always `latest.json`. No filename variations
- **Ephemeral:** Nudges are not archived. Old nudges are overwritten
- **Not durable for audit:** Use mail-async for messages that need persistence
- **Response is optional:** Only required when `requires_response` is true
