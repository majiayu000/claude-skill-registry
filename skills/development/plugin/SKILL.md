---
name: reticle
description: Install, instrument and verify this running web app from the inside (DOM, network, routing, console and framework state) instead of screenshots or guessing. Drives one real flow end to end and returns a verdict with the file:line to fix. Use when the user asks to set up or install Reticle, when a user-facing change needs proving before you call it done, when a test passes but the UI is broken, or when the user types /reticle.
license: Apache-2.0
metadata:
  version: 2.14.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# Reticle

Reticle embeds a dev-only SDK in the running app and exposes it to you as `reticle_*` MCP tools. You look, act, observe, and assert against the real app. No screenshots.

## Setup runs to the end without you

**The plugin already registered the MCP server, so this whole file runs with no client restart and no human input at all.** Do not stop, and do not ask the user anything, until their app is running with Reticle inside it and a session is connected. Everything between here and that point is yours to do: run `init`, fix the wiring it could not, start the dev server, open the browser.

Questions you must not ask, because the repo you are sitting in already answers them: which framework, which package manager, which port, whether to start the dev server, whether to open the browser, whether to carry on. Decide, act, and say what you did in one line. A setup turn that ends in a question ends with nothing verified, and that is the most common way this fails in the field.

There are exactly two places you may stop, and neither is a question about a preference:

1. **No recognisable dev script in `package.json`.** Say so; do not invent one.
2. **Your host asks the human to approve a command.** That prompt belongs to the host. Never bypass or suppress it, and take a refusal as the answer. `init` writing a pre-approval rule for the `reticle` server is not that: it is a scoped, announced config change the human asked for by running the command, and it covers only Reticle's own tools.

## Run this branch first

```bash
cat .reticle.json 2>/dev/null || echo NOT_FOUND
```

- `NOT_FOUND` → **ONBOARD**, then **VERIFY**. Do not stop between them.
- File exists → **VERIFY**.

Either way you are finished only when `reticle_act_and_wait` or `reticle_assert` has produced a verdict. Config files are not an install, and a listed session is not a result.

---

# ONBOARD

**One command. It does all of it, and it ends with a verdict.**

```bash
npx @reticlehq/server@latest init --flow "<the journey worth proving>"
```

It detects the framework and package manager, wires the build config, installs the SDK, registers the MCP server, starts the dev server, opens the app, waits for a session to connect from inside it, drives one flow, and saves it so every later check is one call with no model in the loop. It exits non-zero if no verdict was produced, and prints exactly what is left to do.

## What YOU decide, and pass in

The command reads the repository. It cannot read the request, and three things live only there.

| flag | what only you know |
| --- | --- |
| `--flow "<what>"` | which journey proves the thing the user asked for. Code can list the buttons; it cannot know checkout matters and the theme toggle does not. |
| `--env KEY=VALUE` | what the app needs to reach a usable state: the key from `.env.example`, the mock backend, the variable that skips an auth wall. Repeatable. |
| `--app <dir>` | which app in a monorepo. It can list the servable ones; only the request says which is being worked on. |

Add `--license <key>` if the user gave you one: it writes `RETICLE_LICENSE_KEY` to `.env` and keeps `.env` out of git.

**Ask the user nothing else.** Framework, package manager, port, editor, MCP client: every one is answerable from the repo you are sitting in.

## Then read what it gives you back

A non-zero exit is a to-do list, not a failed install. The command names the cause and prints the REMAINING steps from wherever it stopped; it will not tell you to redo a phase that already worked. Do those and re-run, which is safe.

**It is not finished until a verdict exists.** Writing files is not an install, and neither is a connected session.

## If that command could not run it

**Do not choose this path.** It is not the thorough version of the one above; it is what you fall back to when the command physically could not do the work. Use it only when `init` exited without ever printing `starting:` or `▸ WATCH` (an older CLI that stops after writing files), or when it stopped in the same place twice after you did what it asked. A `⚠` in the report is not a reason: re-run the command, which is idempotent and names what is still outstanding.

```bash
curl https://docs.reticle.sh/install-manual.md      # register the MCP, wire the SDK, prove it
curl https://docs.reticle.sh/troubleshooting.md     # nothing connected, click did nothing, verdict unknown
```

---

# VERIFY

**Only `reticle_act_and_wait` and `reticle_assert` produce a verdict.** Everything else (`act`, `snapshot`, `query`, `navigate`, `observe`, `network`, `console`) moves or reads the app and proves nothing, however many tools it used.

`verified: "unknown"` is not a pass. It means Reticle drove the app and could not tell what happened, so report it as unknown. `verified: "no-fault"` is not a pass either: the page settled and no channel complained, but nothing was declared to prove. **Never weaken a check to make it pass.** That converts a real signal into a false one, which is the failure this product exists to prevent.

## Take the cheapest path that answers the question

Stop at the first row that fits.

| The question | The call | Calls |
| --- | --- | --- |
| "Did my edit break anything?" | `reticle_run({ tool: "reticle_verify", args: { action: "change", files: ["src/App.tsx"] } })` | 1 |
| "Does this known journey still work?" | `reticle_run({ tool: "reticle_flow_replay", args: { flowName: "login" } })` | 1 |
| "Does this new behaviour work?" | `reticle_act_sequence` for the setup, then ONE `reticle_act_and_wait` | 2 |
| No MCP reachable at all | `npx @reticlehq/server verify <url>` in the shell | 1, no MCP |

`reticle_verify` and `reticle_flow_replay` are **not on the advertised tool list**. They are reached through `reticle_run` exactly as written, which is the supported call shape and why you have to be told they exist. `reticle_verify {action:"change"}` answers `unknown` when no saved flow covers the files you changed: nothing ran, so nothing was proved. That is the honest answer and the signal to record one, never a pass.

## Driving by hand

Four calls for a login, not fourteen. Every call is a full model turn, and in a client that approves each one it is also a click.

1. `reticle_snapshot({ mode: "interactive" })` **once**, for the whole flow. Elements are addressable by role and name, so you do not need to add `data-testid` anywhere.
2. `reticle_act_sequence` for the setup: every fill and every intermediate click in ONE call.
3. `reticle_act_and_wait({ ref, action, until })` for the final step only. `until` names the expected consequence **before** the action fires, which is the difference between a check and a rationalisation.
4. `reticle_state()` once at the end. If it comes back empty or `hasCapabilities` is false, the capabilities file `init` generated registered nothing, which is what its `ℹ AGENT: finish the capabilities file` line was telling you. Finish it yourself before you drive: open `src/reticle-dev.*`, register the app's store if it has one, and list the `testids` the flow you picked actually touches. Do not offer, and do not ask; it is a few lines in a file `init` already wrote for you. Never report a clean install over an empty state read.

Assert what the app _did_, not what it _shows_. A UI that renders the value it just sent, rather than the value the server returned, passes every DOM-level check ever written:

```
until: { kind: "allOf", predicates: [
  { kind: "net", method: "POST", urlContains: "/api/refund", status: 200, bodyContains: "\"refunded\":1187.01" },
  { kind: "element", query: { testid: "receipt" } },
  { kind: "console", level: "error", absent: true },
]}
```

Then report what you drove, what it produced, and the `file:line` for anything broken.

---

# License key

Enterprise features are unlocked by a signed key, verified locally with Ed25519 and **no network call**. If the user hands you one, at any point:

1. Append `RETICLE_LICENSE_KEY=<key>` to the project's `.env` (create it if absent). The CLI loads a project-local `.env` on every invocation, so nothing else has to change.
2. Make sure `.env` is in `.gitignore`. A license key in git is a leaked credential, so check before you write and add the line if it is missing.
3. Confirm: `npx @reticlehq/server license` prints `active`, `eval`, `missing` or `expired`.

Never echo the key back in your reply, and never put it in a commit, a comment, or a feedback report. Details: `curl https://docs.reticle.sh/enterprise.md`.

---

# Feedback is first-class

Reticle is built for agents. You are its user, and your experience is the only signal that decides what gets built or fixed, and it disappears when your context does. The moment Reticle breaks, lies, cannot see something you needed, costs too many calls, or gives you trouble during setup:

```
reticle_feedback { kind, text }
```

`kind` is one of `bug`, `gap`, `ambiguity`, `feature_request`, `improvement`. One call, then carry on. If the tools are unreachable, file the same report from the shell:

```bash
npx @reticlehq/server feedback --agent --kind <bug|gap|ambiguity|feature_request|improvement> "what happened"
```

Nothing is too minor. Report defects in **Reticle**; a bug you find in the app under test is Reticle working, and belongs in your answer to the user. Never put app source, secrets, or user data in a report.

# Going deeper

Fetch the one page that answers the question rather than re-reading this file. **Appending `.md` to any docs URL returns its source with no site chrome.**

```bash
curl https://docs.reticle.sh/llms.txt              # every page title and URL; read this first
curl https://docs.reticle.sh/frameworks.md         # per-framework SDK wiring
curl https://docs.reticle.sh/troubleshooting.md    # nothing connected, click did nothing, verdict unknown
curl https://docs.reticle.sh/agent-cheatsheet.md   # the verify loop on one screen
curl https://docs.reticle.sh/predicates.md         # every `until` predicate
```
