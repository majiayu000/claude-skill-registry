---
name: ai-coding-agents-tools
description: "Designs tool runtimes for coding agents. Use when modeling tool registries, deferred loading, permission-aware execution, tool search, or remote tool rendering."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# AI Coding Agents Tools

Use this skill to design or review the tool runtime of a coding-agent CLI: tool contracts, tool pool assembly, deferred loading, tool-search behavior, permission-aware execution, and remote rendering of tool results.

This skill owns tool-runtime architecture for coding agents. For command architecture, use [`../ai-coding-agents-command-runtime/SKILL.md`](../ai-coding-agents-command-runtime/SKILL.md).

## ASCII Flow

```text
tool sources
  built-ins + MCP + plugins + remote server + deferred catalog
  LSP tools (activated when plugin supplies lspServers config; always-load semantics)
       |
       v
tool pool assembly
  shared contract + stable ordering + mode filtering + deny-before-exposure
  Agent(type) tool: parameterized by type discriminator gating spawnable subagent types
       |
       v
model-visible tools
  always-loaded subset + ToolSearch discovery path
       |
       v
execution pipeline
  validate -> permission -> hooks -> run -> shape result -> persist -> render
       |
       v
local or remote result
  normalized into the same session message model
```

## Quick Reference

| Question | Read | Outcome |
|----------|------|---------|
| How should tools be modeled and assembled? | [`references/tool-registry-and-pool-assembly.md`](references/tool-registry-and-pool-assembly.md) | Tool contract, built-in vs MCP pool, deny filtering, prompt-cache-stable ordering |
| How should deferred tools, execution, and remote results work? | [`references/deferred-loading-execution-and-remote-results.md`](references/deferred-loading-execution-and-remote-results.md) | ToolSearch, defer rules, execution pipeline, remote tool-result rendering |
| Should this tool be deferred or always-loaded? | [`references/deferral-eligibility-decision-tree.md`](references/deferral-eligibility-decision-tree.md) | Decision tree, criteria table, `alwaysLoad` vs `shouldDefer`, override settings |
| How do I implement the ToolSearch schema-load pattern? | [`scripts/toolsearch_schema_loader_example.py`](scripts/toolsearch_schema_loader_example.py) | Annotated stdlib-only example: deferred pool, handler, reconnect, policy scope |
| How does OpenAI Codex model unified exec and composable CLI tools? | [`references/openai-codex-unified-exec-and-tool-contracts.md`](references/openai-codex-unified-exec-and-tool-contracts.md) | PTY sessions, stdin writes, output budgets, permission-aware params, CLI-wrapper pattern |

## When To Use

- Design a tool registry for a coding-agent runtime
- Add built-in, MCP, or plugin-provided tools to an agent CLI
- Model tool permission checks, result rendering, progress events, or interrupt behavior
- Decide which tools should be deferred behind tool search
- Review how remote or bridged sessions should render tool uses and tool results

## Use Other Skills

| Need | Use Instead |
|------|-------------|
| Broader coding-agent architecture | [`../ai-coding-agents/SKILL.md`](../ai-coding-agents/SKILL.md) |
| Slash-command architecture | [`../ai-coding-agents-command-runtime/SKILL.md`](../ai-coding-agents-command-runtime/SKILL.md) |
| Plugin extension architecture | [`../ai-coding-agents-plugins/SKILL.md`](../ai-coding-agents-plugins/SKILL.md) |
| Permission mode design | [`../ai-coding-agents-permissions/SKILL.md`](../ai-coding-agents-permissions/SKILL.md) |
| MCP server design | [`../agents-mcp/SKILL.md`](../agents-mcp/SKILL.md) |

## Default Workflow

1. **Define the tool contract.** Keep execution, validation, permissions, rendering, and interruption behavior on the tool type itself, ideally through a shared base-tool or factory pattern rather than ad hoc implementations.
2. **Separate built-ins from external tools.** Assemble the full pool from built-ins plus MCP or other external tools through one shared function.
3. **Filter before the model sees tools.** Apply blanket deny rules and mode-specific filtering at assembly time, not only at call time.
4. **Keep ordering stable.** Built-ins should stay a contiguous prefix when prompt-cache behavior depends on tool order.
5. **Mark deferred tools explicitly.** Use a first-class deferred flag plus a never-defer override for tools that must appear on turn one.
6. **Keep ToolSearch separate from execution.** Discovery is one tool; calling the loaded tool is another phase.
7. **Refresh tool access after topology changes.** MCP reconnects, plugin reloads, or coordinator-mode transitions should rebuild the visible tool set through one path instead of mutating scattered registries.
8. **Normalize remote results.** Convert server-side tool uses and tool results into the same local message model used by the REPL, including fallback rendering for tools the local client does not know how to execute directly.
9. **Make the execution pipeline explicit.** Validation, permission checks, telemetry, hook calls, execution, shaping, persistence, and rendering should be separate stages even if they share one host entrypoint.
10. **Test hostile cases.** Cover duplicate tool names, denied MCP tools, disappearing deferred tools, partial server reconnects, coordinator-mode filtering, and remote rendering mismatches.

## Host Rules

- Keep one tool interface for every tool source so built-ins and remote tools share the same lifecycle.
- Put validation and permission checks close to the tool, but keep global policy orchestration outside individual tools.
- Exclude blanket-denied tools from the visible registry so the model never plans around unavailable tools.
- Prefer explicit `shouldDefer` and `alwaysLoad` semantics over heuristic deferral.
- Keep built-ins as a stable contiguous prefix when ordering affects prompt-cache reuse or provider planning behavior.
- Rebuild or refresh the visible tool pool after MCP connection changes instead of assuming the registry is static for the whole session.
- Unknown remote tools should degrade to renderable stubs, not invisible failures.
- Treat transparent wrapper tools differently from direct tools when rendering results.
- Keep the execution pipeline responsible for telemetry, hooks, permission reasons, and storage-side result shaping.

## Build Order

1. Define one shared tool interface and execution contract.
2. Implement built-in tool registration separately from external tool ingestion.
3. Add assembly-time filtering for deny rules and mode-specific visibility.
4. Add deferred loading and ToolSearch as explicit phases.
5. Build one host execution pipeline from validation through rendering.
6. Add remote normalization so server-side tool traffic can render locally.

## Core Invariants

- The model should only see tools that are truly callable in the current mode.
- Built-ins and external tools must share one lifecycle contract.
- Tool discovery is separate from tool execution.
- Ordering must stay stable when provider behavior depends on tool order.
- Remote tool uses must be renderable even if the local client cannot execute them.

## Failure Modes

- Duplicate tool names with inconsistent semantics.
- Blanket-denied tools still being advertised to the model.
- Deferred tools disappearing after discovery due to stale registry state.
- MCP reconnects leaving the visible tool pool stale.
- Remote tool uses becoming invisible because the local client lacks the implementation.

## Minimal Viable Version

- One tool interface with execution, validation, and rendering hooks.
- One assembly path for built-ins and one for external tools.
- One deny filter applied before tool exposure.
- One ToolSearch-style mechanism for deferred capability discovery.
- One central execution pipeline with permission and telemetry hooks.

## What Strong Implementations Add

- Base-tool factory patterns for consistent contracts.
- Feature-gated built-in enumeration and coordinator-mode filtering.
- Refreshable registries after plugin or MCP topology changes.
- Wrapper-tool versus direct-tool rendering distinctions.
- Storage-aware result shaping and normalized remote replay.

## Known Traps

- Treating built-ins, wrappers, and MCP tools as separate conceptual systems and ending up with different permission, telemetry, and rendering semantics.
- Filtering tools only at execution time after the model has already planned around capabilities that are unavailable in the current mode.
- Binding the registry once at startup and never rebuilding it after plugin reloads, MCP topology changes, or feature-gate updates.
- Assuming remote tool execution can always be replayed or rendered locally without transport-aware adaptation.
- Using deferred loading heuristics that the runtime itself cannot inspect, explain, or invalidate.
- Assuming subagent dispatch is synchronous by default. Since v2.1.198 that assumption is backwards for the reference implementation, and any runtime copying the pattern needs an explicit background-completion event, not a blocking call.

## Common Anti-Patterns

- Treating MCP tools as a side registry with different semantics from built-ins.
- Deferring tools with heuristics that the rest of the runtime cannot inspect.
- Filtering only at call time after the model has already planned around a tool.
- Binding registry state once at startup and never refreshing it.
- Assuming remote tool execution can always be replayed locally without adaptation.

## Claude Code Tool System Extensions (2026)

### LSP tools as a built-in always-load origin class

The `LSP` tool is a built-in tool that activates automatically when a plugin supplies `lspServers` configuration. It is not an MCP-backed tool and not deferred. Origin class: `plugin-activated-builtin`. Semantics: always-load — the LSP tool is added to the model-visible tool set for the session as soon as the plugin activates; no ToolSearch step is needed.

Capabilities the LSP tool exposes: GoToDefinition, FindReferences, hover type info, ListSymbols, SearchSymbols, FindImplementations, CallHierarchy, and automatic post-edit diagnostics injection. The diagnostics injection is the highest-value path: after every `Edit` or `Write` the runtime sends a `textDocument/publishDiagnostics` notification and the LSP tool surfaces the result to Claude without a separate tool call. This shortens the write → observe → fix loop from a Bash round-trip to an in-pipeline event.

Implications for tool pool assembly: a `lspServers`-providing plugin expands the always-load set. Tool pool rebuild on plugin reload must include LSP tool activation/deactivation. Deny rules against `LSP(path:...)` follow the same path-pattern format as `Read` rules.

### Agent(type) — parameterized subagent tool

`Agent` is the tool name for subagent spawning. In v2.1.63 it replaced the legacy `Task` tool name. The rule format `Agent(type)` gates which subagent types are spawnable in a given permission context. `type` is the subagent's `name` field from its agent definition file. Permission rules use this format: `Agent(code-reviewer)` allows spawning the `code-reviewer` subagent; `Agent(*)` allows all; `deny: [Agent(*)]` blocks subagent spawning entirely.

This is a parameterized tool in the same family as `Bash(command)`, `Read(path)`, `Edit(path)`, and `WebFetch(domain:...)`. The `type` specifier is matched against the subagent name at spawn time, not at tool-registration time, so the rule can be written before the subagent definition exists.

### Agent tool: background-by-default, nested depth cap, and fork mode (v2.1.172–v2.1.198)

Three dispatch-mode changes to the `Agent` tool matter for execution-pipeline design, not just for end users:

- **Background-by-default (v2.1.198).** Subagents launched via `Agent` now run in the background by default; the parent runs one in the foreground only when it needs the result before continuing. This flips the historical default (foreground, blocking) — a runtime that still assumes synchronous return-on-call will race or hang on background completions. Design the execution pipeline so tool dispatch returns a handle immediately and completion is a separate event, not a return value.
- **Background permission routing (v2.1.186) is not optional.** Before v2.1.186, a background subagent's tool call that would otherwise prompt was auto-denied silently and the subagent kept going without that capability — a silent-failure trap. Current behavior surfaces the prompt in the parent session, named by subagent, with a per-call deny that doesn't kill the subagent. Any tool runtime that adds background dispatch must route permission prompts to a session the user can actually see, not fail closed silently.
- **Nested spawn depth is capped at 5, server-enforced, no override (since v2.1.172).** A subagent at depth 5 does not receive the `Agent` tool at all. Model the depth counter as part of the `Agent(type)` dispatch contract itself — the runtime should refuse a depth-6 spawn attempt locally with a clear error, rather than letting it round-trip to a server rejection.
- **Fork mode is a third dispatch mode, not a variant of foreground/background.** A forked subagent inherits the full parent conversation (rather than starting fresh) and always runs in the background, but still surfaces permission prompts in the parent's terminal like a foreground call would. Treat fork, named-background, and named-foreground as three branches of the same dispatch contract, each with its own inheritance and visibility rules — collapsing them into one code path tends to leak conversation state or silently swallow prompts.

Cross-cutting judgment call: a message delivered to a resumed or running subagent (via `SendMessage`) is task direction from its own launcher, not user consent or approval for a permission-gated action — the same trust boundary that applies to any agent-to-agent message applies here. A tool runtime's permission layer must not treat "another agent said so" as equivalent to a human granting a permission.

## Cross-Platform Patterns (Goose)

Goose's tool runtime lines up with this skill's existing tool contract, but two patterns are worth lifting explicitly.

### Unified tool origin (`type:` + `name:`)

Goose tools come from extensions declared as `{type: builtin|mcp, name: ...}`. Every tool surfaces to the model under one addressing scheme regardless of origin, and the tool registry's entry type carries `origin` rather than splitting across parallel registries.

- **Pattern:** model tool entries with a single discriminated shape: `{origin: Builtin|Mcp|AcpDelegated, name, schema, schema_version, activation_scope}`. Prompt-cache ordering and deny filtering apply uniformly.
- **Anti-pattern:** a "built-in tools table" separate from an "MCP tools table" with parallel permission and rendering semantics — exactly the pattern this skill already flags, but worth reinforcing.

### Toolshim as a tool-layer adapter

When the provider is a non-function-calling model (see `ai-coding-agents-provider-runtime`), the toolshim presents normalized tool-call events to the tool registry. The tool runtime does not care that the provider synthesized the call from text — the contract at the registry boundary stays the same.

- **Pattern:** the tool registry's call-in interface must not assume native function calling exists. The registry receives a `ToolInvocation` event; who produced it (native provider, toolshim adapter, ACP-delegated agent) is a provenance field, not a branching condition.
- **Anti-pattern:** tool registry code that reaches back into provider internals to decide whether to execute a call. That couples tool dispatch to provider brand and makes toolshim-wrapped providers unusable.
- **Recipe:** every `ToolInvocation` carries `invoked_by: ProviderId | ToolshimId | AcpAgentId`. Telemetry attributes cost, latency, and failure back to the invoker class, but execution flow does not branch on it.

### Codex dual role: MCP client AND MCP server

OpenAI Codex is both an MCP client (it connects to external MCP servers to acquire tools) and an MCP server (via `codex mcp-server`, it exposes itself as a tool to editors and orchestrators). This dual role matters for tool-runtime design: a runtime that acts as a server must apply its full tool-permission model (`exec_approval`, `patch_approval`) to requests arriving over the MCP wire, not just to local interactive sessions. Approval bypasses for "trusted AI callers" are architectural holes — the server-side `AskForApproval` policy applies regardless of caller identity.

For the server-side detail — wire protocol, crate structure, contrast with the HTTP app-server-daemon — see [`../ai-coding-agents-remote-runtime/references/openai-codex-as-mcp-server.md`](../ai-coding-agents-remote-runtime/references/openai-codex-as-mcp-server.md).

### Remote / ACP-delegated tool rendering

When a delegated ACP agent uses tools, their invocations and results must render in the orchestrator's REPL like local tool uses. This extends the skill's existing "normalize remote results" rule across the agent-delegation boundary.

- **Pattern:** the REPL treats tool events with `origin: AcpAgentId` identically to local tool events for rendering purposes; differences are in permission routing (orchestrator approves for the delegated agent) and accounting (costs attributed to the delegated agent row).

## Navigation

### References

- [`references/tool-registry-and-pool-assembly.md`](references/tool-registry-and-pool-assembly.md) — Tool contract, registry composition, and pool assembly
- [`references/deferred-loading-execution-and-remote-results.md`](references/deferred-loading-execution-and-remote-results.md) — Tool search, execution pipeline, and remote result normalization
- [`references/deferral-eligibility-decision-tree.md`](references/deferral-eligibility-decision-tree.md) — When a tool should be deferred behind ToolSearch
- [`references/openai-codex-unified-exec-and-tool-contracts.md`](references/openai-codex-unified-exec-and-tool-contracts.md) — OpenAI Codex unified exec, output budgeting, permission-aware execution, and composable CLI tools

### Scripts

- [`scripts/toolsearch_schema_loader_example.py`](scripts/toolsearch_schema_loader_example.py) — Annotated stdlib-only example of the ToolSearch schema-load pattern

### Data

- [`data/sources.json`](data/sources.json) — Primary documentation and implementation references for tool-runtime guidance

### Related Skills

- [`../ai-coding-agents-command-runtime/SKILL.md`](../ai-coding-agents-command-runtime/SKILL.md) — Command registry and forked command execution
- [`../ai-coding-agents-permissions/SKILL.md`](../ai-coding-agents-permissions/SKILL.md) — Approval and permission routing
- [`../agents-mcp/SKILL.md`](../agents-mcp/SKILL.md) — MCP server connectivity and capability design

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- These patterns are grounded in a local April 2026 `claude_code` source snapshot, cross-checked against the July 2026 hosted `tools-reference` and `sub-agents` docs (`code.claude.com/docs/en`) and the `anthropics/claude-code` changelog through v2.1.206. Re-check upstream code or docs before relying on volatile runtime details — version gates cited here (v2.1.63, v2.1.69, v2.1.172, v2.1.186, v2.1.198) are the ones verified live; anything else in this file should be treated as architectural pattern, not a version-pinned fact.
- Tool-search semantics, deferred loading, and remote rendering paths are especially product-specific. Preserve the architecture, but verify the target runtime’s exact tool transport and UI contract.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
