---
name: audit-my-app
description: Sweep a whole running web app for what is broken, without writing a script or knowing the codebase. Clicks every reachable control and reports dead buttons, console errors, failed requests, and places where the API and the screen disagree. Use on an unfamiliar codebase, before a release, after a big merge or dependency bump, when the user asks for a smoke test or a health check, or when someone says "just check everything still works".
license: Apache-2.0
metadata:
  version: 2.14.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# Sweep the whole app and report what is broken

You do not need to understand the codebase to check it. **Reticle** drives every reachable control in the running app and reports the anomalies. Not installed? `RETICLE_INSTALL_SOURCE=npx_skill npx @reticlehq/server@latest init`, then the [`install-and-verify`](https://github.com/reticlehq/reticle/blob/main/skills/install-and-verify/SKILL.md) skill.

## 1. Ask the app what it can do

```
reticle_capabilities({ sessionId })
```

About 1 KB, and it is the app describing its own testable surface: every registered testid, every domain signal, the stores, and the saved flows with their steps. That beats snapshotting the DOM and inferring intent from element names, and it is the cheapest orientation available.

## 2. Click everything

```
reticle_run({ tool: "reticle_verify", sessionId, args: { action: "crawl", maxSteps: 25 } })
```

```json
{
  "interactiveFound": 3,
  "stepsRun": 3,
  "anomalies": [],
  "counts": { "consoleErrors": 0, "failedRequests": 0, "deadControls": 0, "contradictions": 0 },
  "visited": ["- textbox \"Email\"", "- button \"Sign in\""],
  "truncated": false
}
```

**`deadControls` and `contradictions` are the two counts that mean a real problem.** Console errors and failed requests are worth reading but a busy app produces both innocently. A dead control is a button wired to nothing; a contradiction is a channel disagreeing with what the screen showed.

It clicks **everything**, so point it at a dev environment. `maxSteps` bounds it and defaults to 25. Want a non-destructive pass first: what is reachable, without touching it? `reticle_run({ tool: "reticle_explore", sessionId })`.

Do not hand-roll this sweep. The obvious version (click each control, assert no console error) **passes on exactly the bug you are sweeping for**, because a dead button throws nothing.

## 3. Compare what the API said against what rendered

```
reticle_run({ tool: "reticle_reconcile", sessionId })
```

The API returned ten rows, the table shows nine, nothing errored. Neither the network log nor the DOM is wrong on its own. Only the comparison catches it, and nothing else you can run makes that comparison.

## 4. Find the parts nobody exercised

```
reticle_run({ tool: "reticle_verify", sessionId, args: { action: "coverage" } })   // { total, exercised, untouched }
```

And if the project already has saved flows, ask whether they prove anything:

```
reticle_run({ tool: "reticle_domain", sessionId })
// → { flowCount, coverage: { asserted, presenceOnly, assertionFree }, gaps: { declaredUntestedSignals, … } }
```

A suite of forty flows where thirty-one assert nothing is a suite that will stay green through any regression. That number is usually the most alarming thing in the whole audit, and nothing else reports it.

## 5. Report

Lead with the counts, then one line per real finding with its `file:line` from `reticle_inspect`. Separate:

- **Broken**: dead controls, contradictions, failed requests, errors thrown during the sweep.
- **Unverified**: `untouched` controls and `assertionFree` flows. Not known to be broken; known to be unchecked.
- **Pre-existing**: console errors that were already there before the sweep started. Say so, so nobody attributes them to today's change.

**Do not report a clean audit over a partial one.** If `truncated` is true or `maxSteps` cut the sweep short, say what was not reached. A silent cap reads as "everything is fine" when it means "I stopped".

---

Full capability reference: `curl https://docs.reticle.sh/capabilities.md`. Everything else: `curl https://docs.reticle.sh/llms.txt`.
