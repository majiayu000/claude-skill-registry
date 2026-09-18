---
name: cordon-install
description: Install Cordon, a deterministic layer between untrusted content and agent
  actions, and verify the harness actually calls it. Strips the hidden layer from
  what the agent reads, keeps provenance of every piece of data, and refuses calls
  outside the effect classes the user's own instruction allows. No model call on the
  hot path.
---
# Installing Cordon

Cordon stands between untrusted text and what the agent does with it. It ships
as a Claude Code plugin bound to four harness events: the user's message, a tool
call, a tool result, the display of the answer.

Node 22 or newer. No keys, no tokens, no network access: there are no network
requests and no model calls on the hot path.

## Install

```
/plugin marketplace add ilyautov/cordon
/plugin install cordon@cordon
```

No build step. `plugin/dist/cli.js` ships ready to run, because an installed
plugin has neither `node_modules` nor `package.json` beside it, and a file with
external imports would crash `node` on the first event. The harness reads a
crashed hook as «pass», so the defence would switch off silently.

## Verify, and do not confuse the two questions

`/hooks` answers «is it registered». It does not answer «does it work».

`cordon doctor` answers the second one: it reads the effective policy, runs a
built-in attack sample through the whole path, and names the dangerous parts of
the configuration. The plugin path carries the marketplace name and the version,
so it changes on every update. Ask the harness instead of hard-coding it:

```bash
CORDON=$(node -e "
  const p = require(process.env.HOME + '/.claude/plugins/installed_plugins.json')
  const key = Object.keys(p.plugins).find(k => k.startsWith('cordon@'))
  if (!key) { console.error('plugin is not installed'); process.exit(1) }
  console.log(p.plugins[key][0].installPath + '/dist/cli.js')
")
node "$CORDON" doctor
```

`self-check: ok` means the hidden layer is stripped, a call outside the
certificate is refused, and a call inside it goes through. A hook that is never
called looks, from outside, exactly like a hook that had no reason to fire.

## What to tell the user honestly

Say how far this has been proven, and do not round it up. The wiring was
exercised on a live Claude Code session, 2.1.236: all four events fire, the
certificate refuses, provenance refuses, the footer is drawn, argument
quarantine is applied. The Gemini CLI adapter, the MCP gateway and the LangChain
middleware **have not been run live**. Their install guides are
`docs/install-gemini.md`, `docs/install-mcp.md`, `docs/install-langchain.md`.

The price of the data axis is friction: after reading untrusted content, a
consequential call waits until the user names its destination in their own
message. On the adversarial battery's working profile this took attack success
from 79% to 7%. The rule switches off with `exposure: false` in the policy, and
`cordon doctor` says out loud when it is off.

## What Cordon keeps on disk

Policy in `~/.cordon/policy.yaml`, session state in `~/.cordon/sessions/`,
drafts in `~/.cordon/drafts/`, the decision journal at the path from
`notify.file`. Session state and drafts hold content that came from untrusted
sources, so expired files are deleted automatically.

## Nearby

[github.com/ilyautov](https://github.com/ilyautov), lab
[AI Frontier](https://aifrontier.tech).
