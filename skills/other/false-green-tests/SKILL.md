---
name: false-green-tests
description: 'Find out why the tests pass but the app is broken. Catches false greens: a green suite over a feature that does not work, a mocked API standing in for a real one, an assertion that holds no matter what the app does, a click handler wired to nothing. Use when the suite is green and the user says it is broken, when a test never fails, when coverage looks fine but bugs still ship, or before trusting a passing run you did not watch.'
license: Apache-2.0
metadata:
  version: 2.14.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# The suite is green and the app is broken

A green test is evidence about the test, not about the app. This skill separates the two by running the real app and comparing what it _does_ against what the test _claims_.

It uses **Reticle**, which observes the running app from the inside: DOM, network, console, routing, and framework state. Not installed? `RETICLE_INSTALL_SOURCE=npx_skill npx @reticlehq/server@latest init`, then see the [`install-and-verify`](https://github.com/reticlehq/reticle/blob/main/skills/install-and-verify/SKILL.md) skill.

## The five shapes, in the order they are worth checking

**1. The assertion cannot fail.** Read the test the user trusts. If it only asserts absence (no console error, no thrown exception, no rejected promise) it passes on a control wired to nothing. A dead button throws nothing, fires nothing, and changes nothing. Prove it in the app instead:

```
reticle_act_and_wait({ sessionId, ref, action: "click", until: { kind: "allOf", predicates: [
  { kind: "net",    method: "POST", urlContains: "/api/...", status: 200 },
  { kind: "signal", name: "..." },
]}})
```

A verdict of `no` here, against a green suite, is the false green.

**2. The test drove a mock and the app drives an API.** Compare what the app actually requested with what the test stubbed:

```
reticle_network({ sessionId, since })
```

No request where the test asserted one means the suite verified a fixture. A stale client cache is the same failure with no request at all to look at, which is why registering TanStack Query matters: the cache is the only witness.

**3. The UI moved and the state did not.** The strongest false green, and invisible to any DOM or screenshot check:

```
reticle_state({ sessionId, store, path })
```

A view rendering one value while the store holds another is a bug the render tree cannot show you. If this returns empty or `hasCapabilities` is false, no store was registered: say so, because every state check above is vacuous until it is.

**4. Nobody read the response.** A 2xx that the app never consumed shows as `verified: "unknown"` with `verifiedReason: "outcome_unread"`. That is usually a real app bug, and a test asserting on the request alone would call it a pass.

**5. Whole surfaces nobody exercised.**

```
reticle_run({ tool: "reticle_verify", sessionId, args: { action: "crawl" } })      // click sweep, returns anomalies
reticle_run({ tool: "reticle_verify", sessionId, args: { action: "coverage" } })   // { total, exercised, untouched }
```

`crawl` exists because the obvious hand-rolled sweep (click each control, assert no console error) is itself shape 1.

## What counts as proof

A false green is confirmed when the app **contradicts** the test, not when you feel uneasy. Reticle names that case directly: `verified: "no"` with `verifiedReason: "contradicted"` means a channel observed something incompatible with what the UI claimed: a request that failed while the screen advanced, a signal disagreeing with the DOM, a field echoing a value nobody asked for.

`unknown` is not a false green and not a pass. It means Reticle could not tell. Report it as unknown.

## Then fix the test, not just the app

For every false green you confirm, the test that missed it is still there and will miss it again. Rewrite its assertion to name a consequence the app must produce (a request with a status, a signal, a state path) rather than an absence. **Never weaken a check to make a verdict green**; that is how the false green got in.

---

Index of everything, one page at a time: `curl https://docs.reticle.sh/llms.txt`. Found a case Reticle could not see? `reticle_feedback` with `kind: "gap"`: that is the signal that decides what gets built.
