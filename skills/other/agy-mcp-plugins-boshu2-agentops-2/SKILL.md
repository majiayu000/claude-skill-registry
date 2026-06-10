---
name: agy-mcp-plugins
user-invocable: false
description: |-
  Wire MCP servers and AgentOps plugin bundles into the AGY image with least-privilege access, rollback evidence, and validation hooks.
practices:
- data-contracts
- least-privilege
hexagonal_role: driven-adapter
consumes:
- mcp-server
- skill-bundle
produces:
- agy-mcp-config
- agy-plugin-install
context_rel:
- kind: supplier-to
  with: agy-native
skill_api_version: 1
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: execution
  dependencies: [agy-native, agent-mail, beads-br, dcg]
  stability: experimental
output_contract: "Idempotent MCP-server + plugin wiring on the AGY image, verified by `agy plugin list` and `agy plugin validate`, plus before/after tool-surface lists and rollback commands."
---

# agy-mcp-plugins

Wire MCP servers and package/install plugins into Google's **Antigravity (AGY)**
image so an AGY worker can reach the flywheel substrate (Agent-Mail, the br/beads
bridge) and run the AgentOps corpus in its own harness. Sibling of `agy-native`,
which drives the loop; this skill supplies the tool surface that loop runs against.

## Overview / When to Use

AGY's extension surface is **plugins** — a plugin tree (`plugin.json` + `skills/`,
`subagents/`, `hooks.json`, and a `mcpServers` declaration) imported, validated,
and enabled through `agy plugin {import,validate,install,enable,disable,uninstall,link,list}`.
MCP servers reach AGY *through* that plugin model (declared in a plugin's
`mcpServers`, or via the AGY settings at `~/.gemini/settings.json`), not through a
standalone gemini-cli `mcp` subcommand. A bare `SKILL.md` under `~/.gemini/skills/`
is portable and needs no `plugin.json` just to expose a skill — but a *tool server*
must be declared, enabled, and reachable before any skill that depends on it runs.

Use this skill when standing up the AGY lane in the flywheel, when a freshly built
MCP server must become reachable to an AGY worker, or when distributing the
AgentOps bundle to AGY as a plugin.

This is **operator-side**: it drives the flywheel harness. Never surface these
commands or this framing in client-facing AI Partner content.

**AGY ≠ gemini-cli.** Do not reach for `gemini mcp`, `gemini extensions`, or
`gemini -p` — those belong to the retired gemini-cli image. AGY's runtime is
`agy` / `agy -p`, and its extension unit is the **plugin**.

## ⚠️ Critical Constraints

- **Rule 1 — Verify the live surface first.** Run `agy plugin help` (and
  `agy plugin <sub> --help`) before acting. **Why:** the subcommand shape shifts
  between Antigravity releases; acting on a remembered shape silently writes a
  malformed plugin or settings entry that breaks later `agy` runs.
- **Rule 2 — List before and after every mutation.** Run `agy plugin list` before
  and after import/install/enable/disable. **Why:** the effective tool surface is
  the list output, not the command you believed you ran.
- **Rule 3 — Declare only scoped MCP servers.** Register only the servers the AGY
  task actually needs (Agent-Mail, the br bridge, a specific connector). **Why:**
  every registered server widens the tool blast radius an AGY worker can call.
- **Rule 4 — Disable before uninstall when uncertain.** Prefer
  `agy plugin disable <name>` as the reversible first step over `uninstall`.
  **Why:** uninstalling a working plugin destroys config that may belong to
  another lane; disable is recoverable.
- **Rule 5 — Never inline secrets.** Declare MCP tokens by env-var reference in
  the plugin's `mcpServers` / settings, never as a literal in a tracked file.
  **Why:** `plugin.json` and `~/.gemini/settings.json` are plaintext and often
  synced across the fleet — an inlined token leaks everywhere.
- **Rule 6 — Keep the `dcg` guard wired.** `~/.gemini/settings.json` carries a
  `BeforeTool` → `dcg` hook on `run_shell_command`; do not remove or shadow it
  when adding plugins/servers. **Why:** it blocks destructive commands that an
  auto-approved AGY worker would otherwise run.
- **Rule 7 — Operator-side; invoke-never-rebuild.** Drive `agy`; do not re-author
  AGY, do not write under `~/dev/agentops`, do not push agentops. **Why:** AGY is
  Emanuel's substrate — own a thin adapter, not the tool.

## Workflow / Methodology

### Phase 1: Inventory the current surface
```bash
agy plugin help               # confirm the live subcommand shape (Rule 1)
agy plugin list               # installed plugins + enabled state (the BEFORE list)
```
Record installed plugins, their enabled state, and any MCP servers already declared
in `~/.gemini/settings.json` / enabled plugins.
**Checkpoint:** the target plugin/server name is NOT already present, OR you have
decided repair vs. leave-as-is. Do not blind-add over an existing name.

### Phase 2: Declare an MCP server (the tool-reach path)
AGY reaches an MCP server through a plugin's `mcpServers` declaration (or the AGY
settings). A minimal plugin tree exposing one server:
```
agy-tools/
  plugin.json     # { "name":"agy-tools", "version":"0.1.0",
                  #   "mcpServers": { "agent-mail": { "command":"mcp-agent-mail" },
                  #     "beads-br": { "command":"br", "args":["mcp"],
                  #                   "env": { "BR_DB": "$BR_DB" } } } }
```
For a remote/HTTP MCP, declare its `url` and a `*_ENV_VAR` token reference (never
the literal token — Rule 5). Validate, then install + enable:
```bash
agy plugin validate ./agy-tools
agy plugin install ./agy-tools     # reads plugin.json (or name@marketplace)
agy plugin enable agy-tools
agy plugin list                    # the AFTER list — server-bearing plugin enabled
```
**Checkpoint:** `agy plugin list` shows the plugin enabled; the declared server
appears in the effective surface with the expected scope.

### Phase 3: Ship a plugin bundle (the distribution path)
Distribute the AgentOps bundle the AGY-native way — import an existing tree or
install from a `plugin.json` / marketplace reference:
```bash
agy plugin import claude            # pull an existing Claude plugin tree into AGY
agy plugin import gemini            # or an existing gemini plugin tree
agy plugin validate ./agentops-bundle
agy plugin install ./agentops-bundle        # local tree
agy plugin install agentops@<marketplace>   # or a marketplace reference
agy plugin enable agentops
```
Portable-skill note: the corpus already lives at `~/.gemini/skills/<name>/SKILL.md`
and AGY reads `SKILL.md` directly — no `plugin.json` is needed *just* to expose a
skill; the plugin path is for servers, subagents, hooks, and bundled distribution.
**Checkpoint:** `agy plugin list` shows the bundle installed and enabled from the
expected source.

### Phase 4: Smoke-test the tool surface
Run a read-only AGY worker that exercises the wiring; capture output and exit code:
```bash
agy -p --add-dir "$REPO" \
  "List your available MCP tools and call one safe read-only tool. Do not edit."
```
**Checkpoint:** the worker enumerates the expected servers and reaches at least
one tool. The config is not "wired" until a worker actually uses it.

## Output Specification

**Format:** plugin/MCP wiring on the AGY image + machine-/human-readable
verification output.
**Filename / path:** plugin trees live in their own dirs (`plugin.json` owns the
declaration); AGY-global MCP/hook settings live in `~/.gemini/settings.json`
(let `agy plugin` own plugin writes; edit settings only for AGY-global MCP/hooks).
**Structure:** for each change report — before/after `agy plugin list`; plugin and
server names imported/installed/enabled/disabled/uninstalled; smoke-test command +
exit code; explicit rollback commands (`agy plugin disable`/`uninstall`).

## Quality Rubric

- [ ] Ran `agy plugin help` before acting — no remembered subcommand shape (Rule 1)
- [ ] Captured before/after `agy plugin list` for every mutation (Rule 2)
- [ ] Declared only the MCP servers the task needs — scoped surface (Rule 3)
- [ ] Used `disable` before `uninstall` when uncertain — reversible first (Rule 4)
- [ ] No secret inlined; tokens by env-var reference in plugin/settings (Rule 5)
- [ ] `dcg` BeforeTool hook still present in `~/.gemini/settings.json` (Rule 6)
- [ ] Nothing written under `~/dev/agentops`; no agentops push (Rule 7)
- [ ] `agy plugin validate` passed; end-to-end verified by a real AGY worker
- [ ] No gemini-cli surface used (`gemini mcp`/`gemini extensions`/`gemini -p`)
- [ ] Backstage: no client-facing surface mentions these commands or framing

## Examples

- **Reach Agent-Mail from an AGY flywheel worker:** declare `agent-mail` in a
  plugin's `mcpServers`, `agy plugin validate && agy plugin install ./agy-tools &&
  agy plugin enable agy-tools`, then `agy plugin list` to confirm.
- **Reach br/beads via an MCP bridge:** declare `beads-br` with `command: br`,
  `args: ["mcp"]`, and `env.BR_DB: "$BR_DB"` (env-ref, not literal).
- **Ship the staged AgentOps bundle to AGY:** `agy plugin import claude` to pull
  the existing tree, then `agy plugin install ./agentops-bundle && agy plugin enable agentops`.
- **Reversible removal:** `agy plugin disable agy-tools` (confirm via list) before
  `agy plugin uninstall agy-tools`.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `agy plugin install` fails: "failed to read plugin.json" | target isn't a plugin dir / missing `plugin.json` | point at a dir containing `plugin.json`, or use `name@marketplace`; for a bare skill use `~/.gemini/skills/` |
| Plugin installed but its MCP tools never appear | plugin not enabled, or `mcpServers` malformed | `agy plugin enable <name>`; re-validate; check `~/.gemini/settings.json` for the effective server entry |
| MCP server command/url wrong | bad `command`/`args`/`url` in `mcpServers` | test the server outside AGY, fix the declaration, re-validate + re-enable |
| Worker tried a destructive command | auto-approve under `--dangerously-skip-permissions` | the `dcg` BeforeTool hook should block it — confirm it's wired in `~/.gemini/settings.json` (Rule 6) |
| Unknown plugin/server appears | shared local AGY config from another lane | `agy plugin disable <name>` first, then ask before `uninstall` (Rule 4) |
| Reached for `gemini mcp` and it failed | gemini-cli surface, retired | AGY uses plugins + `~/.gemini/settings.json`, not `gemini mcp`/`extensions` |

## See Also / References

- `agy-native` — drives the loop this skill supplies tools to (sibling AGY skill)
- `agy plugin help`, `agy plugin <sub> --help` — the live, authoritative surface
- `agent-mail` — the multi-agent coordination MCP most often wired
- `beads-br` — the br/beads tracker reached via an MCP bridge
- `dcg` — the destructive-command guard wired as AGY's `BeforeTool` hook
- `~/.gemini/settings.json` — AGY-global MCP/hook settings backing the image
