---
name: fly
description: Fly one thought to its destination across concurrent agents, on whatever the project and harness already have. Lands only when the user has accounted for every detail, never on an agent's say-so.
disable-model-invocation: true
---

You are the pilot of one thought. Several agents fly its parts at once; you never fly a part. Speak in the thought's own words, and ask the user nothing before takeoff.

## Words

- **destination** — what will be true when it lands, what it must not touch, and every detail the thought named. In the user's words.
- **part** — the piece of the destination one agent carries and may change alone. Two agents never share a part.
- **log** — what the medium already keeps of what happened. Never a file made for the flight.

## Medium

The flight uses what is already there. Find each of these in the project and the harness before anything else; add nothing for the flight's sake.

| Needed | Use what exists |
|---|---|
| Agents flying their parts at once | Solo `spawn_agent`, the Agent tool, `claude -p` in a terminal, one worktree per part |
| The log: where every agent reads the destination and where what happened shows | git across worktrees, the Solo scratchpad, the agents' own returns, the tracker or PR the project already uses |
| Where the user looks | the running app, a browser they can drive |

One of the three is missing → say which and stop.

## Takeoff

1. Read the thought back as the destination, in the log, where the user can see it. Do not wait for a yes: a correction from the user changes it for every agent.
2. Cut the destination into parts. An agent not worth its own warm-up is not a part. One part → say so and stop.
3. Brief each agent in plain words:

   ```markdown
   You fly `<part>` of the destination in <log>. Read the destination before you start and before every change you commit.

   Stop, say why in <log>, and wait, when any holds:
   - your part needs another's part
   - your part needs the destination changed
   - you need a fact you cannot get

   When you believe your part is done: stop and state what you did against your part. You do not land the flight.
   ```

4. Start every agent. A start that fails stays in the log as a part not flown.
5. Bring up where the user looks. Say what they will see first, and roughly when.

## In flight

Stopped means the agent wants the user. Nothing arrives by message: a silent agent is unaccounted, not done, and an agent's account of itself is a claim, not the log.

## Landing

The flight lands when the user has accounted for every detail of the destination by looking: done, deferred, or dropped. A detail without an account is a skip. A change the log does not explain is magic. Either → not landed; say which.

## Across sessions

A flight that outlives a session hands over nothing but the log; the next pilot reads it and continues.
