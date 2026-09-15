---
name: replay-user-flows
description: Turn a user journey you just clicked through into a saved regression check that re-runs deterministically, with no model in the loop and no test code to write. Use when you have driven the same flow twice, when the user wants regression coverage without a Playwright suite, when a refactor needs proving against every existing journey, or when re-verifying by hand is costing a full drive every time.
license: Apache-2.0
metadata:
  version: 2.14.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# Record a journey once, re-verify it forever

Exploring an app to find a journey is the expensive part, and re-driving it with a model pays that cost again on every change. **Reticle flows** pay it once: the journey is saved with semantic anchors and replayed deterministically afterwards.

Needs Reticle wired in the project. Not there? `RETICLE_INSTALL_SOURCE=npx_skill npx @reticlehq/server@latest init`, then the [`install-and-verify`](https://github.com/reticlehq/reticle/blob/main/skills/install-and-verify/SKILL.md) skill.

## Record

```
reticle_run({ tool: "reticle_record", sessionId, args: { action: "start", recordingName: "create-task" } })
   … drive the golden path with reticle_act / reticle_act_sequence …
reticle_run({ tool: "reticle_record", sessionId, args: { action: "stop", recordingName: "create-task" } })
reticle_run({ tool: "reticle_flow_save", sessionId, args: { flowName: "create-task" } })
```

That writes `.reticle/flows/create-task.json`. **Commit it**: any agent on the repo can then replay it.

Annotate the business outcome, not just the clicks, so a replay proves the journey _achieved_ something:

```
reticle_run({ tool: "reticle_annotate", sessionId, args: { flow: "create-task", kind: "intent", text: "create a task and see it in the list" } })
reticle_run({ tool: "reticle_annotate", sessionId, args: { flow: "create-task", kind: "success-state", signal: "task:created" } })
```

**You do not need to add `data-testid` first.** A step whose element has no testid is anchored on its component and source location automatically, and a testid-preserving refactor still replays green.

## Replay

```
reticle_run({ tool: "reticle_flow_replay", sessionId, args: { flowName: "create-task" } })
```

Three statuses, and the failures are legible rather than blind:

| status | means | next |
| --- | --- | --- |
| `ok` | every anchor resolved, every expectation held | done |
| `drift` | an anchor missed: a renamed testid, a signal that never fired | read `decision.nextAction`; it names the file:line and the closest surviving anchor |
| `error` | the flow file is missing or invalid, or a step failed at runtime | fix from the error envelope's failed step |

On drift, `reticle_flow_heal` proposes the nearest-match rebind so flows do not rot. Apply it when the rename was intentional; treat it as a finding when it was not.

## Re-verify the whole suite after any change

```
reticle_run({ tool: "reticle_verify", sessionId, args: { action: "flows" } })
// → { status, total, passed, failed, failures: [{ flow, verdict, whatChanged, whereInSource, nextAction }] }
```

One call, every saved flow, no model per flow. Only failures carry detail, so a green suite is cheap to check. Build → `flow_verify` → fix from each `nextAction` → repeat is the regression loop, and it is the point of recording in the first place.

### Only the flows your change could have broken

On a large suite, replaying everything after a one-file edit is waste. Hand it the diff instead:

```
reticle_run({ tool: "reticle_verify", sessionId, args: { action: "change", since: "HEAD~1" } })
```

It works out which saved flows cover the files you edited and replays only those. Give it a git ref or the file list. Use this in the inner loop and `flow_verify` before you ship: the narrow one is fast, the whole one is the guarantee.

### Which of your flows actually prove anything

```
reticle_run({ tool: "reticle_domain", sessionId })
// → { flowCount, coverage: { asserted, presenceOnly, assertionFree }, gaps: { declaredUntestedSignals, … } }
```

A recorded flow that asserts nothing replays green through any regression: it proves the clicks still resolve, not that the app still works. Check this after a recording session: anything landing in `assertionFree` needs an `annotate` pass with a `success-state`, or it is decoration.

## When NOT to record

A journey you will run once is cheaper to drive with `reticle_act_and_wait` and forget. Record the flows that define the product (the ones a regression in would be a bad day) and leave exploratory drives unsaved. A suite of forty half-meant flows costs more attention than it returns.

## Honesty

A replay reports what happened. `drift` is not a pass, and healing a flow to make it green when the app genuinely broke is the one thing that makes the whole suite worthless. If the rename was not intentional, the drift **is** the finding: report it with the `whereInSource` pointer.

---

Full flow reference, one page: `curl https://docs.reticle.sh/flows.md`. Index of everything: `curl https://docs.reticle.sh/llms.txt`.
