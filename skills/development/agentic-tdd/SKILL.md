---
name: agentic-tdd
description: Test-driven development for behaviour a unit test cannot reach, by writing the expectation against the running app before writing the code. Declare the consequence first, watch it fail, implement, watch it pass. Use when building a user-facing feature, when the user asks for TDD on UI or full-stack work, when a unit test cannot express the outcome that matters, or when you want a red-green loop that runs against the real app instead of mocks.
license: Apache-2.0
metadata:
  version: 2.14.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# Red, green, refactor: against the running app

Unit tests drive the units. They cannot say "clicking Deploy posts to `/api/deploy`, moves the store to `deploying`, and shows the banner": that outcome only exists when the whole app runs. So the loop stalls exactly where the interesting bugs are, and the agent falls back to writing code and hoping.

This runs the same discipline one level up, using **Reticle** to drive the real app. Not installed? `RETICLE_INSTALL_SOURCE=npx_skill npx @reticlehq/server@latest init`, then the [`install-and-verify`](https://github.com/reticlehq/reticle/blob/main/skills/install-and-verify/SKILL.md) skill.

## Why this is TDD and not just testing afterwards

The whole value of test-first is that the oracle is written while you still do not know the answer. An expectation written **after** seeing the result can always be adjusted into agreeing with whatever happened, and an agent is especially good at that adjustment. It will find a reading of the output under which the code it just wrote is correct.

`reticle_act_and_wait({ ref, action, until })` enforces the order structurally: `until` is an argument to the action, so the consequence is named before the action runs. That is the red-green loop, made unfakeable.

## 1. RED: write the expectation, watch it fail

Before you write the feature, state what the app must do:

```
reticle_act_and_wait({ sessionId, ref, action: "click", until: { kind: "allOf", predicates: [
  { kind: "net",     method: "POST", urlContains: "/api/deploy", status: 200 },
  { kind: "signal",  name: "deploy:started" },
  { kind: "element", query: { testid: "deploy-banner" } },
  { kind: "console", level: "error", absent: true },
]}})
```

You want `verified: "no"` here. **A red you did not see is a test you cannot trust.** If this comes back `yes` before you have written anything, the expectation is not specific enough to the change. Tighten it until it fails for the right reason.

`verified: "unknown"` is not a red. It means Reticle could not tell, so the loop has no signal at all. Fix that before writing code, usually by naming a consequence the app can actually produce.

## 2. GREEN: implement until the same call passes

Write the smallest change that makes it hold, then re-run **the same call, unchanged**. That last word is the discipline: editing the predicate to match what you built converts TDD into narration. If the assertion has to change, say out loud why the original expectation was wrong.

Prefer re-asserting over re-driving when the verdict was `unknown` / `unsettled`: `reticle_assert({ predicate, since, timeout_ms: 8000 })`. Re-driving repeats a side effect that already happened.

## 3. REFACTOR: the expectation is the safety net

Now change the implementation freely and re-run. Predicates are bound to behaviour (a request, a signal, a state path), not to markup, so a refactor that preserves behaviour stays green while a DOM-shaped test would go red for no reason.

## 4. Keep the loop for the next change

A journey worth writing test-first is a journey worth re-running forever. Save it once:

```
reticle_run({ tool: "reticle_flow_save", sessionId, args: { flowName: "deploy" } })
reticle_run({ tool: "reticle_verify", sessionId, args: { action: "flows" } })   // every saved flow, no model per flow
```

That turns the red-green loop into a regression suite you never hand-wrote.

## What to assert on, in order of strength

1. **A signal the app fires itself** (`{ kind: "signal" }`): the app declaring success in its own vocabulary. Strongest available.
2. **State** (`reticle_state`): what the app believes. Catches a UI that moved while the store did not.
3. **Network**: the request, method and status. Catches a mock standing in for the real thing.
4. **An element appearing**: necessary, never sufficient. Anything can render.
5. **Absence of console errors**: always include it, never rely on it alone. Absence-only predicates pass on a control wired to nothing.

## Honesty

**Never weaken a check to turn a verdict green.** In this loop that is not a small sin: it is the loop running backwards, and it produces a green suite over a feature that does not work.

---

Predicate reference: `curl https://docs.reticle.sh/predicates.md`. Everything else: `curl https://docs.reticle.sh/llms.txt`.
