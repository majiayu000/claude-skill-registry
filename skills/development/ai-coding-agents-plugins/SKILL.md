---
name: ai-coding-agents-plugins
description: "Designs plugin systems for coding-agent runtimes and CLIs. Use when adding plugin manifests, extension points, built-in plugins, or reloadable agent integrations."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# AI Coding Agents Plugins

Use this skill to design or review plugin systems for coding-agent runtimes, especially terminal-first CLIs that load skills, hooks, MCP servers, commands, agents, or output styles from installable extensions.

This skill owns plugin architecture for coding agents. For the broader coding-agent creation workflow, start with [`../ai-coding-agents/SKILL.md`](../ai-coding-agents/SKILL.md).

## ASCII Flow

```text
plugin package
  |
  v
manifest validation
  identity + version + capability declarations + trust class
  |
  v
install or load
  built-in | user | project | marketplace | repo-local
  |
  v
registration
  skills + commands + tools + hooks + agents + MCP servers
  |
  v
policy filter + namespace
  only safe capabilities enter the runtime
  |
  v
reload/disable/uninstall invalidates caches and visible registries
```

## Quick Reference

| Question | Read | Outcome |
|----------|------|---------|
| How should a coding-agent plugin be structured? | [`references/plugin-manifest-and-capability-model.md`](references/plugin-manifest-and-capability-model.md) | Package layout, manifest fields, capability families |
| How should plugins load, reload, and register? | [`references/plugin-loading-and-runtime-lifecycle.md`](references/plugin-loading-and-runtime-lifecycle.md) | Discovery order, activation flow, cache and reload rules |
| Where should trust boundaries live? | [`references/plugin-trust-boundaries-and-safety.md`](references/plugin-trust-boundaries-and-safety.md) | Install-time safety, runtime restrictions, policy controls |
| How does OpenAI Codex structure plugin manifests and marketplace lifecycle? | [`references/openai-codex-plugin-manifest-and-marketplace.md`](references/openai-codex-plugin-manifest-and-marketplace.md) | Skills/MCP/apps/hooks paths, interface metadata, path rules, marketplace add/remove/upgrade |
| How does GitHub Copilot CLI structure plugin manifests and marketplaces? | [`references/github-copilot-cli-plugin-manifest-and-marketplace.md`](references/github-copilot-cli-plugin-manifest-and-marketplace.md) | Manifest search order, component paths, marketplace.json shape, install sources, cross-runtime manifest convergence with Claude Code |

## When To Use

- Design a plugin system for a coding-agent CLI or terminal runtime
- Add installable extensions that provide commands, skills, hooks, agents, or MCP servers
- Separate built-in capabilities from marketplace or repo-local plugins
- Define plugin manifests, capability registration, namespacing, or reload behavior
- Review whether a plugin architecture has safe trust boundaries and host-owned precedence

## Use Other Skills

| Need | Use Instead |
|------|-------------|
| End-to-end coding agent or coding team design | [`../ai-coding-agents/SKILL.md`](../ai-coding-agents/SKILL.md) |
| MCP server design and connectivity | [`../agents-mcp/SKILL.md`](../agents-mcp/SKILL.md) |
| Hook authoring and lifecycle automation | [`../agents-hooks/SKILL.md`](../agents-hooks/SKILL.md) |
| Subagent definitions and delegation contracts | `agents-subagents` |
| Generic CLI and SDK design outside agent runtimes | [`../software-devtools/SKILL.md`](../software-devtools/SKILL.md) |
| Skill packaging and shared-skills validation | [`../agents-skills/SKILL.md`](../agents-skills/SKILL.md) |

## Default Workflow

1. **Classify the extension surface.** Decide whether the user actually needs a plugin, or just a local skill, hook, MCP server, or built-in command.
2. **Define capability families first.** Model commands, skills, hooks, agents, output styles, and MCP servers as typed host-owned extension points.
3. **Choose the trust boundary.** Decide what is allowed at install time, what is allowed at runtime, and which fields third-party plugin content is forbidden to control.
4. **Write the manifest contract.** Keep identity, metadata, dependencies, and capability declarations in the manifest instead of relying on implicit folder discovery alone.
5. **Namespace plugin-provided components.** Avoid collisions by having the host prefix commands, agents, and output styles with the plugin name or source.
6. **Define deterministic load order.** Core runtime first, then built-ins, then installed plugins, then session-local overlays or inline plugins.
7. **Split plugin state into layers.** Keep install intent, materialized on-disk plugin contents, and active in-memory components as separate layers.
8. **Design reload semantics explicitly.** Separate cache clearing, component re-registration, and transport reconnection. Do not assume hot reload is safe for every capability type.
9. **Preserve partial success.** A failing plugin should not take down the whole runtime if unaffected capability families can still be swapped safely.
10. **Validate with hostile cases.** Test duplicate names, invalid manifests, blocked plugins, stale caches, plugin disable, and partial reload failures.
11. **Measure activation cost.** Capture schema/instruction tokens, startup latency, spawned processes, and network connections before and after enablement. Package size or capability count is not a proxy for context cost, and installed does not mean active.

## Host Rules

Use these defaults unless the runtime has a better documented model:

- Treat the host as the only authority on precedence, activation, and capability registration.
- Keep plugin manifests declarative. Avoid executing plugin code just to discover metadata.
- Make built-ins look like plugins to the UI and registry, but keep their trust and enablement rules host-controlled.
- Keep plugin-provided component names namespaced by plugin ID or plugin name.
- Allow third-party plugins to contribute capabilities, but do not let nested files silently escalate permissions beyond what the user approved at install time.
- Prefer reloadable registries for commands, agents, hooks, output styles, and MCP connections, but allow restart-required behavior when side effects cannot be safely swapped.
- Version plugin caches by compatibility boundary, not only by plugin display version.
- Treat git-subdir and path-based installs as distinct cache identities so different mounts cannot collide.

## Build Order

1. Define capability families and host-owned extension points.
2. Write the manifest contract and validation path.
3. Define plugin trust boundaries and install-time restrictions.
4. Implement deterministic discovery and activation order.
5. Split plugin state into intent, materialization, and active runtime components.
6. Add reload semantics, cache invalidation, and partial-failure handling.
7. Add managed-policy and built-in-plugin interaction rules.

## Core Invariants

- The host owns precedence, trust, and activation.
- Plugin manifests must be declarative and inspectable without executing plugin code.
- Built-ins may look like plugins in UI, but they are not trusted the same way.
- Capability names must be namespaced or collision-safe.
- Reloading one capability family must not silently corrupt another.
- Cache identity must include compatibility-relevant install context, not only plugin name.

## Failure Modes

- Executing plugin code during metadata discovery.
- Name collisions between built-ins and third-party capabilities.
- Stale caches keeping removed or disabled plugins active.
- Partial reload leaving command registries and MCP state inconsistent.
- Different plugin installs colliding in cache because path or subdir identity was ignored.
- Plugin-provided settings or nested files broadening trust beyond approved scope.

## Minimal Viable Version

- One declarative manifest format.
- One validation path before activation.
- One deterministic discovery and precedence order.
- One namespacing rule for plugin-provided capabilities.
- One explicit boundary between install intent, materialized plugin files, and active runtime registration.
- One restart-required fallback when hot reload is unsafe.

## What Strong Implementations Add

- Versioned cache directories and compatibility probing.
- Layered refresh that loads plugins first, then rebuilds dependent registries, then reconnects transports.
- Built-in plugins with host-controlled enablement semantics.
- Managed-policy interaction for plugin-only capabilities.
- Typed plugin errors and partial-failure recovery.
- Orphaned plugin-version cleanup and compatibility-aware cache keys.
- Reloadable registries for commands, hooks, agents, output styles, and MCP connections.

## Known Traps

- Treating plugin discovery as filesystem scanning alone and ending up with activation behavior that changes by path layout rather than manifest contract.
- Loading untrusted marketplace plugins with the same precedence and capability surface as built-ins or managed extensions.
- Rebuilding active registries in place during reload and leaving commands, hooks, or MCP connections in a half-updated state.
- Ignoring compatibility boundaries between core version, plugin API version, cache schema, and persisted state.
- Assuming every capability family can hot reload safely even when it holds long-lived connections or runtime-owned policy hooks.

## Common Anti-Patterns

- Using folder scanning as the manifest contract.
- Letting third-party plugins decide precedence or trust at runtime.
- Assuming hot reload is safe for every capability family.
- Treating installed files and active runtime state as one undifferentiated layer.
- Treating built-ins and marketplace plugins as identical trust classes.
- Ignoring cache schema and compatibility when plugin APIs evolve.

## Claude Code Plugin System Reference (2026)

Source: `code.claude.com/docs/en/plugins-reference` and `code.claude.com/docs/en/discover-plugins` (verified 2026-06-09).

### plugin.json manifest schema

The manifest lives at `.claude-plugin/plugin.json` and is optional (auto-discovery applies without it). `name` is the only required field if a manifest is present.

**Key fields (complete schema):**

| Field | Type | Notes |
|-------|------|-------|
| `$schema` | string | JSON Schema URL for editor autocomplete; ignored by Claude Code at load time |
| `name` | string | Required if manifest present. Kebab-case, no spaces. Used for component namespacing (`plugin-name:skill-name`). The marketplace entry can list the plugin under a different `name`; that entry name, not the one in `plugin.json`, is what `enabledPlugins` and `/plugin` key on |
| `displayName` | string | Human-readable, may contain spaces; shown in `/plugin` picker |
| `version` | string | Semantic version. Resolution order when a user checks for updates: `plugin.json` version, then the marketplace entry's version, then the git commit SHA of the source, then `"unknown"` (non-git sources). Pin an explicit version only if you will remember to bump it on every release — a stale explicit version silently blocks users from receiving new commits, where an unset version updates on every commit |
| `description` | string | Brief purpose statement |
| `author` | object | `{name, email, url}` |
| `homepage` | string | Documentation URL |
| `repository` | string | Source code URL |
| `license` | string | SPDX identifier |
| `keywords` | array | Discovery tags |
| `defaultEnabled` | boolean | If `false`, installs disabled; user must explicitly enable |
| `skills` | string\|array | Custom skill directories (adds to default `skills/`) |
| `commands` | string\|array | Flat `.md` skill files (replaces default `commands/`) |
| `agents` | string\|array | Agent files (replaces default `agents/`) |
| `hooks` | string\|array\|object | Hook configs (merges) |
| `mcpServers` | string\|array\|object | MCP configs (merges) |
| `lspServers` | string\|array\|object | LSP server configs |
| `outputStyles` | string\|array | Output style files (replaces default) |
| `experimental.themes` | string\|array | Color theme files |
| `experimental.monitors` | string\|array | Background monitor configs |
| `userConfig` | object | Prompted at enable time; values available as `${user_config.KEY}` |
| `channels` | array | Message channel declarations (Telegram/Slack/Discord style; bound to MCP servers) |
| `dependencies` | array | Other plugins this one requires, optionally with semver constraints, e.g. `{"name": "secrets-vault", "version": "~2.1.0"}`. Enabling a plugin transitively enables its dependencies at the same scope; disabling fails (with a chained command in the error) while a dependent is still enabled. `claude plugin prune` removes auto-installed dependencies no longer required by anything |

Two directories round out the package but aren't manifest fields: `bin/` (executables added to the Bash tool's `PATH` while the plugin is enabled — invokable as bare commands) and a root `settings.json` (default configuration applied on enable; only the `agent` and `subagentStatusLine` keys are currently honored). A plugin-root `CLAUDE.md` is **not** loaded as context — ship instructions as a skill instead.

**Component path rules**: `skills` adds to default; `commands`, `agents`, `outputStyles`, `experimental.themes`, `experimental.monitors` replace the default; `hooks`, `mcpServers`, `lspServers` have their own merge rules.

**Unrecognized fields are tolerated, not rejected** — Claude Code ignores top-level keys it doesn't recognize (a type mismatch on a recognized field still fails to load). This lets one `plugin.json` double as an npm `package.json` or a VS Code/Cursor/MCPB manifest. Use `claude plugin validate --strict` in CI to turn unrecognized-field and near-miss-name warnings into errors before publishing, without making every runtime load pedantic.

**Plugin subagent restrictions**: plugin-shipped agents support `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `isolation` (`"worktree"` only). Fields `hooks`, `mcpServers`, and `permissionMode` are explicitly not supported for plugin-shipped agents.

### Skills-directory plugins (`@skills-dir`)

Any folder under a skills directory (`~/.claude/skills/` or `<project>/.claude/skills/`) that contains its own `.claude-plugin/plugin.json` loads automatically as a plugin named `<name>@skills-dir` on the next session — no marketplace, no install step, and the plugin is used in place rather than copied into the plugin cache. `claude plugin init <name>` scaffolds one. This is the fastest path from "a skill with extra opinions" to "a real plugin with bundled agents/hooks/MCP," and it is the mechanism a solo developer or small team should reach for before standing up a marketplace.

Trust follows scope, not source-of-truth intent: a personal-scope (`~/.claude/skills/`) plugin has no extra restrictions, but a project-scope (`<cwd>/.claude/skills/`) plugin — checked into a repo and therefore attacker-controlled if the repo is untrusted — loads only after the workspace trust dialog, and its MCP servers, LSP servers, and background monitors are restricted further (monitors do not load at all from project scope). Design new runtimes with this same scope-to-trust mapping: repo-sourced plugin content should never get the same default trust as a plugin the user personally placed in their home directory.

### LSP plugins as a capability family

Plugins with `lspServers` configuration provide real-time code intelligence via the LSP tool. This is distinct from MCP:

- LSP plugins configure how Claude Code connects to a language server binary (must be installed separately)
- Capabilities: jump to definition, find references, hover type info, list symbols, find implementations, call hierarchies
- Automatic diagnostics: after every file edit, the language server reports errors/warnings; Claude sees them without a separate tool call
- `diagnostics: false` in lspServers config keeps code navigation but suppresses diagnostic injection
- Official LSP plugins in `claude-plugins-official`: `clangd-lsp`, `csharp-lsp`, `gopls-lsp`, `jdtls-lsp`, `kotlin-lsp`, `lua-lsp`, `php-lsp`, `pyright-lsp`, `rust-analyzer-lsp`, `swift-lsp`, `typescript-lsp`

### Marketplaces

**Two Anthropic-run marketplaces, three different registered names — do not assume the install-time name matches the repo name:**

| Marketplace | Install-time `@name` | Source repo | Auto-enabled |
|-------------|----------------------|--------------|--------------|
| Official (curated by Anthropic) | `claude-plugins-official` | `anthropics/claude-plugins-official` | Yes — auto-loaded at startup; auto-update on by default |
| Community (safety-screened third-party, pinned to commit SHA per plugin) | `claude-community` | `anthropics/claude-plugins-community` | No — added manually via `/plugin marketplace add anthropics/claude-plugins-community`; auto-update off by default |
| Demo/example (Anthropic-maintained, not curated) | `claude-code-plugins` | `anthropics/claude-code` | No — added manually via `/plugin marketplace add anthropics/claude-code` |

**Trap:** the community marketplace's repo is `anthropics/claude-plugins-community` but its registered marketplace name is the shorter `claude-community` — installing with `<plugin>@claude-plugins-community` fails. Always confirm the actual name with `/plugin marketplace list` before writing install instructions into docs or onboarding scripts. This name/repo mismatch is a general marketplace-design trap, not unique to Anthropic's catalogs — expect it whenever a marketplace author renames the catalog independently of the repo.

Install syntax: `/plugin install <plugin-name>@<marketplace-name>` (interactive scope picker), or non-interactively `claude plugin install <plugin>@<marketplace> --scope {user|project|local}` (default `user`). `claude plugin details <name>` shows the always-on and per-invoke token cost before you install.

### /plugin tabbed UI

The `/plugin` command opens a four-tab interface (cycle with Tab / Shift+Tab):

- **Discover**: browse available plugins from all marketplaces; context-cost estimate shown per plugin; "Will install" section lists all components before install
- **Installed**: view, enable, disable, uninstall; grouped by scope; errors/unresolved deps at top
- **Marketplaces**: add, remove, update marketplace registries; toggle auto-update per marketplace
- **Errors**: plugin load errors and diagnostics

### Install scopes

| Scope | Settings file | Use case |
|-------|--------------|----------|
| `user` | `~/.claude/settings.json` | Personal, all projects (default) |
| `project` | `.claude/settings.json` | Shared via version control |
| `local` | `.claude/settings.local.json` | Project-specific, gitignored |
| `managed` | Managed settings | Read-only, admin-installed, update-only |

### /reload-plugins

Run `/reload-plugins` to activate newly installed, enabled, or disabled plugins without restarting. Shows counts for plugins, skills, agents, hooks, MCP servers, and LSP servers reloaded. If a plugin provides MCP servers, reloading invalidates the prompt cache; a warning is shown; pass `--force` to apply anyway.

### Context-cost estimate

The details pane and `claude plugin details <name>` command show per-component always-on token cost and per-invoke token cost before installation.

### Plugin subagent restrictions (security)

Plugin-shipped agents cannot set `hooks`, `mcpServers`, or `permissionMode`. These fields are silently ignored when the agent is defined inside a plugin. This prevents plugins from escalating privileges through agent definitions.

### Policy gates

| Setting | Effect |
|---------|--------|
| `disableBundledSkills` | Disables skills bundled with Claude Code itself (not marketplace plugins) |
| `strictPluginOnlyCustomization` | Restricts customization sources to plugins and managed settings only; blocks user/project skills, hooks, MCP from non-plugin paths |
| `strictKnownMarketplaces` | Limits installable plugins to admin-allowlisted marketplaces |
| `blockedMarketplaces` | Blocks specific marketplaces (including `skills-dir` source) |

## GitHub Copilot CLI Plugin System Reference (2026)

Source: `docs.github.com/en/copilot/concepts/agents/copilot-cli/about-cli-plugins` and `docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference` (verified 2026-07-11). Copilot CLI went GA 2026-02-27; enterprise-managed plugins hit public preview 2026-05-06. Full field tables in [`references/github-copilot-cli-plugin-manifest-and-marketplace.md`](references/github-copilot-cli-plugin-manifest-and-marketplace.md).

Copilot CLI converged on essentially the same capability model as Claude Code: agents (`*.agent.md`), skills (`SKILL.md`), hooks, MCP servers, and LSP servers, discovered from a `plugin.json` manifest whose required field is `name` and whose install sources include `owner/repo`, `owner/repo:path/to/plugin`, git URLs, local paths, or `plugin@marketplace`. Two marketplaces (`copilot-plugins`, `awesome-copilot`) are registered by default.

**The load-bearing fact for anyone building a new coding-agent plugin host**: Copilot CLI's manifest loader checks `.plugin/plugin.json`, then `plugin.json`, then `.github/plugin/plugin.json`, then falls back to **`.claude-plugin/plugin.json`** — the exact Claude Code manifest location — before giving up. That is a deliberate compatibility decision, not coincidence: a plugin authored for Claude Code loads on Copilot CLI without modification for the fields both hosts share. Treat `.claude-plugin/plugin.json` plus the `skills/`, `agents/`, `hooks/hooks.json`, `.mcp.json` conventions as the emerging cross-vendor baseline, and design any new runtime to read that shape rather than inventing a fourth one. Do not oversell the convergence, though — host-specific fields (Copilot's `extensions` block with an `exclusive` flag, Claude Code's `experimental.themes`/`experimental.monitors`/`channels`) have no counterpart on the other host and are silently dropped there, not migrated.

## Cross-Platform Patterns (Goose)

Goose unifies the "plugin" and "MCP extension" concepts into a single typed extension model, and shows what manifest-in-recipe delivery looks like when tasks ship with their own extension declarations.

### Unified extension kind with `type:` discriminator

Goose recipes declare extensions inline:

```yaml
extensions:
  - type: builtin
    name: developer
  - type: mcp
    name: github
```

Both are `extension` entries; the `type` discriminator selects transport and trust. This collapses the dual-track "built-ins vs MCP" mental model into one ontology with two transports.

- **Pattern:** model the extension registry with a single type whose `origin` or `transport` field carries `builtin | mcp | ...`. Manifest, precedence, namespacing, and cache identity apply uniformly.
- **Anti-pattern:** maintaining parallel "plugin registry" and "MCP registry" APIs with subtly different lifecycle, reload, and trust semantics. Future transports (ACP-delegated extensions, WASM plugins) then each need their own track.
- **Recipe:** one `Extension` trait / interface, one activation path, one cache-identity rule. The `transport` field is free to evolve — `builtin`, `mcp-stdio`, `mcp-sse`, `acp-client` — without new mental models.

### Manifest-in-recipe (task-level extension declaration)

In Goose, the unit of work (recipe) declares its extension dependencies inline. This differs from classic plugin systems where plugins are enabled globally at runtime-config level.

- **Pattern:** allow plugin/extension declaration at multiple layers: host config, project/repo config, *and* task artifact. Task-layer declarations are subsets of what the project/host allows and define the active envelope for that task only.
- **Anti-pattern:** forcing all plugin activation to happen at CLI startup. Coding agents that support shareable task blueprints need blueprint-local extension sets — a recipe shared between teammates should carry its dependencies, not assume the receiver pre-enabled them.
- **Recipe:** the plugin resolver is called with a scope: `(host_config, project_config, task_manifest)`. The resolver intersects them — task can narrow but not broaden. A task's declared extensions must be subsets of the project's allowlist; violations are install-time errors, not runtime surprises.

### Runtime-shipped official plugins (Codex Build iOS/Mac)

OpenAI's Codex CLI ships first-party plugins ("Build iOS Apps", "Build macOS Apps", authored by Thomas Ricouard / @Dimillian) that auto-update with each Codex release. They package skills (SwiftUI Liquid Glass, Performance Audit, View Refactor, App Intents, AppKit interop, signing/notarization) behind a single plugin identity.

- **Pattern:** treat host-shipped plugins as a distinct trust class. They look like marketplace plugins in the registry but update in lockstep with the runtime version, so their compatibility key is the runtime version itself, not a separate plugin version.
- **Anti-pattern:** giving official plugins the same cache identity and update cadence as user-installed plugins. Their staleness model is different — a runtime upgrade should invalidate them automatically.
- **Recipe:** carry an `origin: official | builtin | marketplace | local` tag on every plugin record. Tie `official` cache keys to `(runtime_version, plugin_id)` and refresh on runtime upgrade without prompting the user. Source: https://github.com/openai/codex

### Schema validation as a first-class gate

Goose's `recipe-scanner/` validates YAML recipes (and therefore their declared extensions) at build/ship time. This generalizes: plugin manifests and task manifests should face static validation before activation, not just at runtime load.

- **Pattern:** manifests are structured data; ship a validator and run it in CI, at install, and at activation. Treat an invalid manifest as a shipping defect, not a runtime edge case.

## Navigation

### References

- [`references/plugin-manifest-and-capability-model.md`](references/plugin-manifest-and-capability-model.md) — Package layout, manifest structure, and capability typing
- [`references/plugin-loading-and-runtime-lifecycle.md`](references/plugin-loading-and-runtime-lifecycle.md) — Discovery, caching, reload, and activation flow
- [`references/plugin-trust-boundaries-and-safety.md`](references/plugin-trust-boundaries-and-safety.md) — Trust model, validation, and policy guardrails
- [`references/openai-codex-plugin-manifest-and-marketplace.md`](references/openai-codex-plugin-manifest-and-marketplace.md) — OpenAI Codex plugin manifest fields, interface metadata, path validation, and marketplace lifecycle
- [`references/github-copilot-cli-plugin-manifest-and-marketplace.md`](references/github-copilot-cli-plugin-manifest-and-marketplace.md) — GitHub Copilot CLI manifest search order, component paths, marketplace.json shape, and cross-runtime convergence with Claude Code

### Data

- [`data/sources.json`](data/sources.json) — Primary documentation and source references for plugin-runtime guidance

### Related Skills

- [`../ai-coding-agents/SKILL.md`](../ai-coding-agents/SKILL.md) — Broader coding-agent architecture and creation workflow
- [`../agents-hooks/SKILL.md`](../agents-hooks/SKILL.md) — Hook lifecycle design
- [`../agents-mcp/SKILL.md`](../agents-mcp/SKILL.md) — MCP server integration

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- The patterns in these references are grounded in a local April 2026 `claude_code` source snapshot. Re-check upstream code or docs before relying on volatile runtime details.
- Plugin manifest and loader semantics change faster than shared-skill guidance. Validate field names, reload behavior, and trust restrictions against the current runtime before shipping.
- If the target runtime differs from Claude Code, preserve the architecture principles but re-check the concrete capability and policy surfaces.

## Learnings Loop

When prior decisions or pitfalls are relevant, consult `learnings.consolidated.md` if present; use `learnings.md` only for needed history or as the available fallback. Otherwise skip both.

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
