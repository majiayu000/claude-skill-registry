---
name: install-and-verify
description: Verify that a web app change actually works by driving the running app from the inside (DOM, network, routing, console, framework state) instead of screenshots or guessing. Use after any user-facing change, when a fix is claimed but unproven, when a test passes but the UI is broken, or when you need a real verdict rather than "looks right". Also use to install and wire up Reticle in a project that does not have it yet.
license: Apache-2.0
metadata:
  version: 2.14.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# Reticle: prove the change, do not guess

Reticle embeds a dev-only SDK in the user's running app and exposes it to you as `reticle_*` MCP tools. You look, act, observe, and assert against the real app. No screenshots, and no browser download for the verify loop: it drives the tab the user already has open. (A driven browser, which `reticle_lease` and `--drive` use, does need Chromium; Reticle says so when it needs one.)

## Where the rest of the documentation is

Everything not in this file is at `https://docs.reticle.sh`, and it is built to be fetched rather than browsed. **Append `.md` to any page URL to get its source with no site chrome**, so you can pull one page instead of a whole document you mostly do not need:

```bash
curl https://docs.reticle.sh/llms.txt                  # every page title and URL, small enough to read whole
curl https://docs.reticle.sh/cli/doctor.md             # one CLI command: flags, real output, exit codes
curl https://docs.reticle.sh/tools-act-and-wait.md     # one tool: arguments and what a verdict means
curl https://docs.reticle.sh/troubleshooting.md        # the failures people actually hit
```

Read `llms.txt` first and pick the one page that answers the question. That is almost always cheaper than pulling a large file and hoping the part you need survived. There is a `/llms-full.txt` with the entire site in one file; use it only to seed a context window deliberately.

Every page arrives with the four rules that matter prepended, whether you asked for them or not, so a single fetch orients you without a second call.

## Which path am I on

```bash
cat .reticle.json 2>/dev/null || echo NOT_FOUND
```

- `NOT_FOUND` → **SETUP** below.
- File exists → **VERIFY** below. If `reticle_sessions` then returns an empty list, go to [references/troubleshooting.md](references/troubleshooting.md); do not restart setup.

## Read this before you touch SETUP

**Installed means a verdict was produced. Writing config files is not installed.**

Every earlier point looks like success and is not:

- `init` exited 0. Files were written. Nothing connected.
- The `reticle_*` tools appeared. Your client can reach a daemon. The app is very likely still uninstrumented.
- A session is listed. The app dialled in. The user has still seen nothing happen.

**Do not tell the user Reticle is set up until step 5 has produced a verdict.** The single most common outcome in the field is an agent that finishes step 1, reports success, and leaves a user with config files and no instrumented page.

## Setup runs to the end without you

**Do not stop, and do not ask the user anything, until their app is running with Reticle inside it and a session is connected.** Everything between here and that point is yours to do: run `init`, fix the wiring it could not, start the dev server, open the browser. Not one of those needs a human, and every one of them has been the place an onboarding turn died with nothing to show.

Questions you must not ask, because the repo you are sitting in already answers them: which framework, which package manager, which port, which editor or MCP client, whether to start the dev server, whether to open the browser, whether to carry on. Decide, act, and say what you did in one line.

There are exactly three places you may stop, and none is a question about a preference:

1. **No recognisable dev script in `package.json`.** Say so; do not invent one.
2. **Your host asks the human to approve a command.** That prompt belongs to the host. Never bypass or suppress it, and take a refusal as the answer. `init` writing a pre-approval rule for the `reticle` server is not that: it is a scoped, announced config change the human asked for by running the command, and it covers only Reticle's own tools.
3. **On a first install only, the client restart that loads the MCP tools** (step 2). Even then, keep going until the app is running and connected, and stop for the restart last, with only the drive left.

Setup requires a client restart, which ends your turn. This skill survives that restart. **After the restart, re-read this file and resume at the step you were on.** Do not start over, and do not skip forward.

---

# SETUP

**One command. It does all of it, and it ends with a verdict.**

```bash
RETICLE_INSTALL_SOURCE=npx_skill npx @reticlehq/server@latest init --flow "<the journey worth proving>"
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

# License key

Enterprise features are unlocked by a signed key, verified locally with Ed25519 and **no network call**. If the user hands you one, during setup or at any later point:

1. Append `RETICLE_LICENSE_KEY=<key>` to the project's `.env`, creating the file if it is not there. The CLI folds a project-local `.env` into the environment on every invocation, so nothing else has to change.
2. Make sure `.env` is in `.gitignore`. A license key in git is a leaked credential, so check before you write and add the line if it is missing.
3. Confirm with `npx @reticlehq/server license`, which prints `active`, `eval`, `missing` or `expired`.

Never echo the key back in your reply, and never put it in a commit, a code comment, or a feedback report. The rest: `curl https://docs.reticle.sh/enterprise.md`.

---

# VERIFY

**Only `reticle_act_and_wait` and `reticle_assert` produce a verdict.** Everything else (`act`, `snapshot`, `query`, `navigate`, `observe`, `network`, `console`) moves or reads the app and proves nothing. A drive that ends without one of those two has no result, however many tools it used.

Prefer `reticle_act_and_wait({ ref, action, until })`. It names the expected consequence before the action, which is the difference between a check and a rationalisation.

A verdict of `verified: "unknown"` is not a pass. It means Reticle drove the app and could not tell what happened. Report it as unknown.

Never weaken a check to make it pass.

## Take the cheapest path that answers the question

Stop at the first row that fits. Do not hand-drive a flow you could replay.

| The question | The call | Calls |
| --- | --- | --- |
| "Did my edit break anything?" | `reticle_run({ tool: "reticle_verify", args: { action: "change", files: ["src/App.tsx"] } })` | 1 |
| "Does this known journey still work?" | `reticle_run({ tool: "reticle_flow_replay", args: { flowName: "login" } })` | 1 |
| "Does this new behaviour work?" | `reticle_act_sequence` for the setup, then ONE `reticle_act_and_wait` | 2 |
| No MCP available at all | `npx @reticlehq/server verify <url>` in the shell | 1, no MCP |

The first two are **not on the advertised tool list**: they are reached through `reticle_run` exactly as written. That is the supported call shape, and it is why you have to be told they exist.

`reticle_verify {action:"change"}` answers `unknown` when no saved flow covers the files you changed. Nothing ran, so nothing was proved: that is the honest answer, never a pass, and it is the signal to record one (step 5 above).

The full loop (look, act, observe, assert), how to read a verdict, batching, and regression suites: [references/verify.md](references/verify.md).

---

# Feedback is first-class

Reticle is built for agents. You are its user, and your experience is the only signal that decides what gets built or fixed. It disappears when your context does.

The moment Reticle breaks, lies, cannot see something you needed, costs too many calls, or gives you trouble during setup:

```
reticle_feedback { kind, text }
```

`kind` is one of `bug`, `gap`, `ambiguity`, `feature_request`, `improvement`. One call, then carry on with the task.

If the tools are unreachable (setup unfinished, daemon down), file the same report from the shell:

```bash
npx @reticlehq/server feedback --agent --kind <bug|gap|ambiguity|feature_request|improvement> "what happened"
```

Nothing is too minor. Report defects in **Reticle**; a bug you find in the app under test is Reticle working and belongs in your answer to the user. Never put app source, secrets, or user data in a report.

# References

- [references/setup.md](references/setup.md): per-framework SDK wiring, store registration, desktop apps.
- [references/verify.md](references/verify.md): the look, act, observe, assert loop and reading verdicts.
- [references/troubleshooting.md](references/troubleshooting.md): no session, port mismatch, non-localhost hosts, daemon problems.
