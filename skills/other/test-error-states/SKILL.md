---
name: test-error-states
description: Force the states a happy-path run never reaches (a failing API, an empty list, a slow request, a timeout, an expired session, a toast that auto-dismisses) and check the UI actually handles them. Use when error handling was written but never run, when a loading or empty state needs verifying, when a bug only happens on a slow connection, or when a timer, poll, debounce or retry needs testing without sleeping.
license: Apache-2.0
metadata:
  version: 2.14.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# The error state has never run

Every app has a `catch` block nobody has executed and an empty state nobody has seen. They are written from imagination, shipped untested, and discovered by a user on a bad day.

**Reticle** can force those conditions in the running app. Not installed? `RETICLE_INSTALL_SOURCE=npx_skill npx @reticlehq/server@latest init`, then the [`install-and-verify`](https://github.com/reticlehq/reticle/blob/main/skills/install-and-verify/SKILL.md) skill.

## Read this before you start: network mocking needs a driven or leased browser

`reticle_network_mock` intercepts requests in a browser Reticle owns, and **the always-on SDK cannot do it.** A connected tab with neither `reticle drive` nor a lease still returns `{ ok: false, reason: "no-cdp-provider" }`.

Your route is a leased Playwright tab (`reticle_lease acquire`) or `RETICLE_CDP_URL` pointed at a Chrome started with remote debugging:

```bash
# macOS — the user runs this once, in their own Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

RETICLE_CDP_URL=http://localhost:9222 npx @reticlehq/server@latest mcp
```

If you have neither a lease nor a driven browser, **say so in one line and offer the clock half of this skill anyway**: `reticle_clock` needs none of it. What you may not do is drive the happy path, watch it pass, and report that error handling works.

## Force a failure

```
reticle_run({ tool: "reticle_network_mock", sessionId, args: {
  mocks: [{ urlContains: "/api/deploys", status: 500 }],
}})
```

Then drive the flow and **name the recovery you expect before you act**:

```
reticle_act_and_wait({ sessionId, ref, action: "click", until: { kind: "allOf", predicates: [
  { kind: "element", query: { testid: "error-banner" } },
  { kind: "console", level: "error", absent: true },
]}})
```

Note the second predicate. A UI that "handles" an error by logging an uncaught exception has not handled it. Clear mocks with `{ clear: true }` when you are done, or every later check runs against a lie.

Worth forcing, in rough order of how often they are broken: `500`, a `4xx` with a real error body, an empty `200` (`[]`, the empty state), a malformed payload, and a request that never resolves (the spinner that spins forever).

## Skip time instead of sleeping

```
reticle_clock({ sessionId, freeze: true })
reticle_clock({ sessionId, advanceMs: 5000 })
reticle_clock({ sessionId, reset: true })
```

Toasts that auto-dismiss, debounced search, polling, session timeouts, retry backoff. All of these are normally verified by sleeping, which is slow and flaky in equal measure. A timing assertion is a statement about the machine, so it passes on your laptop and fails in CI.

Freeze, advance by exactly the interval, assert the consequence. Same result on a fast laptop and a loaded runner. **Always `reset` when you finish**, or a frozen clock silently breaks everything that runs after you.

## What to assert

The recovery, not the absence of a crash:

1. The error is **shown to the user**: a specific element, not just "the page did not blank".
2. The app **stayed usable**: retry works, the form still has its input, navigation is not stuck.
3. **State is honest**: `reticle_state` shows the failure, not a half-applied optimistic update. A UI that rolled back visually while the store kept the optimistic value is the classic bug here, and only the store read finds it.
4. **No uncaught error** in the console.

## Honesty

Mocking changes the app's world, so a verdict taken under a mock is a statement about the mocked condition and nothing else. Say which mock was active when you report a pass, and clear every mock and reset the clock before handing back. An audit that leaves a `500` pinned on `/api/deploys` breaks the next person's session and looks like a real outage.

---

Capability reference: `curl https://docs.reticle.sh/capabilities.md`. Everything else: `curl https://docs.reticle.sh/llms.txt`.
