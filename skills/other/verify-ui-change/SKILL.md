---
name: verify-ui-change
description: Check that a change to a web app actually works in the running app before calling it done. Drives the real page and returns a pass/fail verdict with the request that fired, the state that moved, and the file:line to fix. Use after editing a component, a form, a route, or an API call; when you have said "fixed" but have not opened the app; when the user asks "does it actually work?"; or when a change looks right on screen and you cannot prove it.
license: Apache-2.0
metadata:
  version: 2.14.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# Verify the change in the running app

You edited something a user can see. Nothing is proven until the real app has done it and something other than the DOM agrees.

This uses **Reticle**, which embeds a dev-only SDK in the user's running app and exposes it as `reticle_*` MCP tools. No screenshots, no browser download for the verify loop, no dev server of its own.

## 1. Are the tools here?

```
reticle_sessions()
```

- **A session comes back** → go to step 2.
- **Tools do not exist** → Reticle is not installed. Run `RETICLE_INSTALL_SOURCE=npx_skill npx @reticlehq/server@latest init`, then keep going without the tools: fix every `⚠` it printed, start the project's own dev script in the background if nothing is serving the app, and open it with `npx @reticlehq/server open <the url the dev server is serving>`. Only once the app is running and connected, ask for the one thing you cannot do yourself: a client restart, so it picks up the MCP server. Stopping at the `init` command leaves the user with config files and an uninstrumented page. Full setup is in the [`install-and-verify`](https://github.com/reticlehq/reticle/blob/main/skills/install-and-verify/SKILL.md) skill.
- **Tools exist, list is empty** → read the `why` field on the response. It distinguishes "no app running" from "an app is running that never dialled this daemon" from "a tab was here and closed", and each has a different fix. If no app is running, start the project's own dev script from `package.json` in the background yourself and tell the user in one line that it is running and how to stop it: never a second one, never a guessed command, never kill anything, and the permission prompt is your host's. If one IS running, the app is not the missing piece and the SDK is; do not send the user to start what they already started.

## 2. Name the consequence BEFORE you act

This is the whole method. An expectation written after you see the result can be talked into agreeing with whatever happened; one written before cannot.

```
reticle_snapshot({ sessionId, mode: "interactive" })   // controls only, with refs

reticle_act_and_wait({ sessionId, ref, action: "click", until: { kind: "allOf", predicates: [
  { kind: "net",     method: "POST", urlContains: "/api/...", status: 200 },
  { kind: "element", query: { testid: "..." } },
  { kind: "console", level: "error", absent: true },
]}})
```

Multi-step journey? Drive it in one call with `reticle_act_sequence`, then assert the outcome once. Do not act → snapshot → act → snapshot: it proves the same thing at several times the cost.

**Only `reticle_act_and_wait` and `reticle_assert` produce a verdict.** `reticle_act`, `snapshot`, `query`, `navigate`, `network` and `console` move or read the app and prove nothing. A drive that ends without one of the first two has no result, however many calls it made.

## 3. Read the verdict honestly

| `verified` | means | do |
| --- | --- | --- |
| `yes` | the consequence you named happened | report it, with the evidence |
| `no` | it did not happen, or a channel contradicted the UI | a real finding: report it with `because` |
| `unknown` | Reticle drove the app and could not tell | **not a pass.** Say unknown and say why |

On `unknown` / `unsettled`, re-assert rather than re-driving: `reticle_assert({ predicate, since, timeout_ms: 8000 })` using the `since` from the act result. Re-driving repeats a side effect that already happened.

**Never weaken a check to turn a verdict green.** An assertion edited until it passes proves nothing.

## 4. Check what you did not touch

```
reticle_run({ tool: "reticle_verify", sessionId, args: { action: "coverage" } })   // { total, exercised, untouched }
```

If `untouched` still holds controls your change affects, the drive is unfinished. One call, and it is the cheapest guard against reporting a pass over the half you never opened.

## 5. Report

State what you drove, what the verdict was, and the evidence: the request and status, the state that changed, the app's own signal. If something failed, `reticle_inspect({ sessionId, ref })` on the failing element gives the `file:line`: put it in the report.

Then `reticle_session({ action: "yield", mode: "waiting" })` so the human's panel stops reading "live".

---

More detail, fetchable one page at a time: `curl https://docs.reticle.sh/llms.txt` for the index, then the single page you need (`tools-act-and-wait.md`, `predicates.md`, `troubleshooting.md`). If Reticle itself misbehaves, file it with `reticle_feedback`: one call, then carry on.
