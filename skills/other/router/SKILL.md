---
name: router
description: Spawn agents and verify their output — route work, never do it. Use when the work splits into pieces agents can carry and the session should route and check, not execute.
---

## Extract

From the conversation/context/user:

- The **work** on the table — the goal as given.
- Its **pieces** — the parts it splits into, each one an agent could carry alone.

## Gate

Proceed only when: the work splits into pieces an agent can carry alone, and each returned piece can be checked for less than the cost of doing it.

Anything else, say which in one plain line — never route anyway:

- The work is one piece — a single pass, or a plain answer → do it yourself, plainly, and proceed with what it produces; there is nothing to split.
- A piece only this session can do → stop.
- Verifying a piece's return would mean redoing the piece → stop.
- The work will run without a human watching, optimizing toward something, and how it's judged is undefined before it runs → use **target** skill.

## Hold

For as long as the loop below runs, you are a router, not a worker:

- Anything that touches files, shell, or the web is work — it goes to an agent, never to you.
- Your own turns go to spawning, verifying, and talking to the user — never doing.
- Prefer a turn spent checking an agent's work over a turn spent doing the work yourself.
- An explicit order from the user to do something yourself overrides this.

## Route

1. Dispatch the pieces. Each agent starts blind: write its prompt to carry the piece's goal, the constraints, why it matters, and what is out of scope. Independent pieces dispatch together, never one at a time.
2. Verify each return against what its prompt asked. An agent's summary is what it intended, not what it did — read what it produced, never what it reported. Nothing reaches the user unverified.
3. Keep dispatching and verifying while a piece waits to dispatch or a return waits to be verified. The loop ends when every piece has returned verified, or the user lifts the routing stance.

## Output

The verified pieces are the result — hand them to the user. If the loop ended because the user lifted the routing stance, hand back what stands: each piece that passed its check as verified, and any return not yet checked named as unverified, never claimed as verified.

Then check whether anything still unresolved would change what gets built:

- Nothing would → return to the work the routing interrupted.
- A claim about a returned piece needs a committed verdict → use **judge** skill.
- The user is missing something already settled → use **explain** skill.

The routing is spent once the loop ends — anything further runs under the branch picked here, never as another round of routing.
