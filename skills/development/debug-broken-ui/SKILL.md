---
name: debug-broken-ui
description: Find out why something in a running web app does not work, when the console is empty and the code looks correct. Reads the click, the request, the store and the console together and returns the file:line to open. Use when a button does nothing, a form will not submit, data will not load, a page renders blank or stale, a modal will not close, or the user says "it's broken" and the code review says it is fine.
license: Apache-2.0
metadata:
  version: 2.14.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# The app is broken and the code looks fine

Reading the source again will not tell you why. The evidence is in the running app, and most of it never reaches the screen: the request that failed, the store that never moved, the handler that was never bound, the element covered by something invisible.

**Reticle** reads all of it from inside the page. Not installed? `RETICLE_INSTALL_SOURCE=npx_skill npx @reticlehq/server@latest init`, then the [`install-and-verify`](https://github.com/reticlehq/reticle/blob/main/skills/install-and-verify/SKILL.md) skill.

## Do not start by guessing. Start by reproducing.

```
reticle_snapshot({ sessionId, mode: "interactive" })   // controls only, with refs
reticle_act_and_wait({ sessionId, ref, action: "click", until: { kind: "element", query: { testid: "..." } } })
```

The verdict already narrows it: `no` / `contradicted` means a channel saw something incompatible with the UI: you have the bug. `unknown` means Reticle drove it and could not tell, which is a different investigation from "it failed".

**Read the act result before you call anything else.** Its `summary` block already carries the whole causal window of that one click: `net {total, errors, headline}`, `consoleErrors`, `stateDiffs [{path, from, to}]`, `storageDiffs [{key, from, to}]`, `route`, `signals`, `layoutShift`, `longTasks`: real before→after diffs, not counts. The console, network, storage and state calls below are for going DEEPER into something the summary already pointed at. Calling all three straight after an act pays three model round trips (and, in an approval-gated client, three human clicks) for evidence you were already holding.

`summary.stateUnwatched: true` means the state channel is dark: no subscribable store is registered, so an empty `stateDiffs` means _unwatched_, not _unchanged_, and no state-based conclusion is available until someone registers the store. It is the one field here that is about your instrumentation rather than about the app.

When the summary does point somewhere, read that channel **scoped to what you just did**: pass `since` from the act result, or you are reading a buffer that predates the click:

```
reticle_console({ sessionId, since })
reticle_network({ sessionId, since })
reticle_state({ sessionId, store })
```

## The diagnosis table

| What you see | What it is | Next |
| --- | --- | --- |
| No request fired at all | the handler is not bound, or a client cache served a stale value | `reticle_inspect` the element for its `file:line`; check the cache if it is TanStack Query |
| Request fired, `4xx`/`5xx` | a real backend failure the UI swallowed | the response body is in the network entry |
| `2xx` but nothing changed | the app never read the response: verdict says `outcome_unread` | usually a real bug in the success path |
| Request fine, DOM fine, **store stale** | UI-vs-state desync, invisible to any screenshot | `reticle_state` is the only witness; this is the highest-value read here |
| Click did nothing, no error | the control is dead, occluded, or disabled | `reticle_inspect` returns `occluded`, `box` (0×0), `styles.cursor`, `opacity` |
| Element "not found" that you can see | virtualised list has not mounted it | `reticle_scroll_to`. A `query` that misses is not evidence of absence |
| Looks logged in, behaves logged out | the token never persisted | `reticle_storage` |
| Console error that predates your click | a pre-existing fault, not your bug | call it out before continuing |

## Get the file, not a theory

```
reticle_inspect({ sessionId, ref })
```

Returns the component and `source: { file, line }` for the element you are looking at, plus whether it is occluded, sized, disabled or off-theme. That is the pointer to open. End the investigation with a location, not a hypothesis.

## When the flow is long

Do not ping-pong act → snapshot → act → snapshot to find the failing step. Drive the journey with `reticle_act_sequence` and assert once; the first step whose consequence fails is the one to look at, and you paid a fraction of the calls to find it.

## Before you say it is fixed

Re-run the reproduction as a verdict (`reticle_act_and_wait` with the consequence named up front) rather than eyeballing the page. A fix confirmed by looking at it is the failure mode that created this ticket.

**And never weaken the check to make it pass.**

---

Troubleshooting Reticle itself (as opposed to the app): `curl https://docs.reticle.sh/troubleshooting.md`. Everything else: `curl https://docs.reticle.sh/llms.txt`. If Reticle could not see something you needed, `reticle_feedback` with `kind: "gap"`.
