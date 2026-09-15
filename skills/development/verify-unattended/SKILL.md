---
name: verify-unattended
description: 'Install, instrument and verify a web app end to end without pausing for a human. Use in an autonomous or goal-mode agent, in CI, or in any client that asks for approval on every command: it never says "restart your client" or "open a browser", because it takes a route that needs neither. Prefer the normal install-and-verify skill when a human is present and can answer.'
license: Apache-2.0
metadata:
  version: 2.14.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# Reticle, unattended

Same product, same verdicts, one difference: **nothing here waits for a human.**

The normal skill has two places where it hands control back: "restart your client so it picks up the MCP server" and "open the app in a browser". Both are correct when someone is sitting there. In goal mode they are dead ends: the restart ends the context holding these instructions, and there is nobody to open a tab.

So this skill takes the route that needs neither, and stops only when it has a verdict or a reason.

## The one rule that makes this work

**You cannot add MCP tools to your own running process.** No slash command, no config edit, no re-registration reaches the tool list you already have. Your client read it before Reticle existed. Do not try, and do not ask to be restarted.

Instead, branch once on what you already have:

- **`reticle_*` tools present** → drive with them. Best evidence, source-mapped, full verdicts.
- **not present** → use the CLI. `reticle verify` produces a verdict and an exit code with no MCP involvement at all.

Both routes end in a verdict. Pick the one your process allows and go.

## Step 1: wire it, once, quietly

```
export RETICLE_INSTALL_SOURCE=npx_skill
npx -y @reticlehq/server@latest init
```

The `export` is on its own line on purpose. Every other copy of this command carries the marker inline, but this skill runs where commands are matched against a prefix allowlist (see "Keep commands plain" below), and `RETICLE_INSTALL_SOURCE=... npx ...` no longer starts with `npx`. Inline, it would stop matching the very rule this file tells you to rely on.

Then read the report rather than assuming it. Two lines matter:

- **`⚠` on the app's build config**: the wiring did not land. Apply the printed edit yourself; do not carry on as if it had.
- **`ℹ` naming a version fallback**: the pinned SDK was refused and a different one installed. The SDK and the daemon must agree; if a later call reports a protocol error, this is why.

`init` is idempotent. A step reading `already wired` is a pass, not a skip.

**If `init` reports every step already done, the app was instrumented before you arrived.** That is fine, but it means this run has not proved the install. Say so rather than claiming you set it up.

## Step 2: make sure the app is actually running

The daemon needs a page to look at, and a page needs a server. Do not ask whether to start one.

1. Read the dev script out of `package.json`.
2. Start it in the background, on the port the script implies.
3. Poll the port until it answers. A dev server that has to compile a route can take 30 seconds on first hit; a timeout here is not a failure yet.

If a server is **already** listening on that port, use it. Starting a second one on a different port gives you an app nobody is verifying, and leaves a process behind.

**Restarting matters after `init`.** A build plugin added to a config the running server already read is not in the bundle. If the server was up before step 1, restart it now or nothing you do next will find an instrumented page.

## Step 3: get a page connected

With the MCP tools:

```
reticle_sessions
```

A listed session is the proof. Nothing else in this skill can tell you anything about the app until one appears.

No session, and no human to open a tab? Take one yourself:

```
reticle_lease { action: "acquire", url: "http://localhost:<port>/" }
```

The lease opens a browser Reticle owns and drives. It is the whole answer to "there is nobody here to open the page".

Without the MCP tools, skip to step 4: `verify` opens its own browser.

## Step 4: the verdict

**Declare the consequence before you act.** This is the difference between a check and a rationalisation, and it is the entire reason this tool exists:

```
reticle_act_and_wait { ref, action, until: { … } }
```

Assert what the app _did_, not what it _shows_. A UI that renders the value it just sent, rather than the value the server returned, passes every DOM-level check ever written:

```
until: { kind: "net", method: "POST", urlContains: "/api/refund",
         status: 200, bodyContains: "\"refunded\":1187.01" }
```

`bodyContains` reads the **response**: what the server answered. It needs body capture, which `init` writes into the app's config; if a verdict comes back `outcome_unread`, that is what is missing.

Without the MCP tools:

```
npx @reticlehq/server verify http://localhost:<port>/
```

Exit 0 is a pass. It drives the app and re-verifies **saved flows**, so if the project has none, it will tell you nothing was checked. That is not a pass. Record one first, or say plainly that there was nothing to verify.

## Step 5: read the verdict honestly

- **`verified: "yes"`**: proved. Say what held.
- **`verified: "no"`**: the app is wrong, or your expectation was. Both are results. Report it.
- **`verified: "unknown"`**: Reticle drove the app and could not tell. **Not a pass.** Never round it up, and never weaken the assertion until it goes green. That converts a real signal into a false one, which is the failure this product exists to prevent.

A drive that ends without `act_and_wait` or `assert` has no result, however many tools it used.

## When you are genuinely stuck

Stop and say which of these it is. A precise dead end beats a green report.

| What you see | What it means |
| --- | --- |
| tools absent, `verify` says no saved flows | nothing to verify yet: record a flow, or report that |
| `reticle_sessions` empty, port listening | the bundle has no SDK: restart the dev server after `init` |
| `verified: "unknown"`, `outcome_unread` | the response body was not recorded: check the plugin options `init` wrote |
| lease loads the page but never connects | the app refused to dial; on a non-localhost host it needs a pairing token as well as `allowNonLocalhost` |

## Notes for approval-gated clients

Some clients ask a human to approve each command. Two things reduce that to near zero:

- **Keep commands plain.** `npx @reticlehq/server init` matches a prefix rule; the same command wrapped in a subshell or a `$(…)` usually does not.
- **Expect one prompt about the home directory.** The daemon keeps its state in `~/.reticle`, which is outside the workspace. Approving that family once covers every later call.

If your client offers an autonomous or goal mode, this skill is written for it. Turn it on before starting rather than approving forty prompts. Approval fatigue is a real reason runs are abandoned half-installed, with the tools connected and nothing ever verified.

## Report feedback

Reticle is built for agents, so your experience is the signal that decides what gets fixed, and it disappears when your context does. One call, then carry on:

```
reticle_feedback { kind: "bug" | "gap" | "ambiguity" | "feature_request" | "improvement", text: "…" }
```

Unreachable? `npx @reticlehq/server feedback --agent --kind <kind> "what happened"`. Report defects in **Reticle**; a bug you find in the app under test is Reticle working, and belongs in your answer.
