---
name: ai-coding-agents
description: "Creates coding agents on Claude Code, Codex, and Agent SDK. Use when defining review, test, refactor, or team agents — not building a runtime."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# AI Coding Agents — Creation Hub

Use this skill to go from a coding agent idea to a working agent definition, whether a single-purpose agent or a coordinated multi-agent coding team.

This skill owns the coding-domain-specific creation workflow, templates, and patterns. For agent architecture decisions and build-vs-not gates, start with [`../ai-agents/SKILL.md`](../ai-agents/SKILL.md).

## Two Different Tracks

This skill (and its siblings prefixed `ai-coding-agents-*`) split into two tracks with different audiences. Pick the right one before going deeper.

**Track A — Create an agent on an existing platform (this skill).**
Use this umbrella when the platform exists (Claude Code, Codex, or Agent SDK) and you need to define an agent on top of it: frontmatter, tools, archetype, multi-agent coordination. This is the common case.

**Track B — Build a coding-agent runtime from scratch (the 14 sibling skills).**
Use the dedicated curriculum when you are building the runtime itself — the thing that loads agents, sandboxes execution, routes tool calls, manages sessions. Each skill captures known traps, patterns, and anti-patterns for one subsystem:

| Concern | Skills |
|---------|--------|
| Runtime architecture | [`ai-coding-agents-command-runtime`](../ai-coding-agents-command-runtime/SKILL.md), [`ai-coding-agents-provider-runtime`](../ai-coding-agents-provider-runtime/SKILL.md), [`ai-coding-agents-terminal-ui`](../ai-coding-agents-terminal-ui/SKILL.md) |
| Execution & safety | [`ai-coding-agents-execution-sandbox`](../ai-coding-agents-execution-sandbox/SKILL.md), [`ai-coding-agents-permissions`](../ai-coding-agents-permissions/SKILL.md), [`ai-coding-agents-settings-policy`](../ai-coding-agents-settings-policy/SKILL.md) |
| State & lifecycle | [`ai-coding-agents-sessions`](../ai-coding-agents-sessions/SKILL.md), [`ai-coding-agents-tasks`](../ai-coding-agents-tasks/SKILL.md), [`ai-coding-agents-remote-runtime`](../ai-coding-agents-remote-runtime/SKILL.md) |
| Extensibility | [`ai-coding-agents-plugins`](../ai-coding-agents-plugins/SKILL.md), [`ai-coding-agents-tools`](../ai-coding-agents-tools/SKILL.md) |
| Delivery | [`ai-coding-agents-release-distribution`](../ai-coding-agents-release-distribution/SKILL.md), [`ai-coding-agents-observability-evals`](../ai-coding-agents-observability-evals/SKILL.md) |

If the request is "how do I add a slash command to my runtime?" or "how should I design approval prompts?", route to Track B. If it's "how do I define a code-review agent on Claude Code?", stay here.

## ASCII Flow

```text
user need
  |
  v
classify: define agent on existing platform OR build runtime subsystem
  |
  +--> existing platform
  |      -> choose platform: Claude Code | Codex | Agent SDK
  |      -> choose archetype or team pattern
  |      -> scope tools + context + verification
  |      -> smoke test on representative coding tasks
  |
  +--> runtime subsystem
         -> route to ai-coding-agents-* sibling skill
         -> design subsystem contract + invariants + failure modes
         -> validate with host/runtime-specific tests
```

## Quick Reference

| Question | Read | Outcome |
|----------|------|---------|
| How do I create a coding agent end-to-end? | [`references/creation-workflow.md`](references/creation-workflow.md) | Step-by-step from idea to running agent |
| Which platform should I target? | [`references/platform-patterns.md`](references/platform-patterns.md) | Decision tree: `.md` vs `.toml` vs SDK |
| What single-agent archetypes exist? | [`references/agent-archetypes.md`](references/agent-archetypes.md) | Six patterns with frontmatter and tools |
| When should I use a multi-agent team? | [`references/multi-agent-coding-patterns.md`](references/multi-agent-coding-patterns.md) | Three architectures: coordinator, fork, swarm |
| How do I manage context for code-heavy work? | [`references/context-management.md`](references/context-management.md) | Token budgets, file selection, progressive disclosure |
| How do I wrap dev tools for agents? | [`references/tool-integration.md`](references/tool-integration.md) | Linter, formatter, test runner, type checker patterns |
| My agent is broken | [`references/debugging-guide.md`](references/debugging-guide.md) | Failure taxonomy and fixes |
| What do production coding agents look like? | [`references/production-patterns.md`](references/production-patterns.md) | Real patterns from Claude Code source |
| How does Claude Code define and validate agents? | [`references/claude-code-agent-runtime-patterns.md`](references/claude-code-agent-runtime-patterns.md) | File format, validation, and persistence rules |
| How do swarms, teammates, and worktrees behave? | [`references/claude-code-swarm-and-worktree-patterns.md`](references/claude-code-swarm-and-worktree-patterns.md) | Team files, inherited flags, worktree lifecycle |
| How are skills and built-in plugins loaded? | [`references/claude-code-skill-and-plugin-loading.md`](references/claude-code-skill-and-plugin-loading.md) | Frontmatter loading, plugin-backed skills, prompt budgets |
| Which prompt recipes steer a Claude Code session to a specific outcome? | [`references/claude-code-prompt-recipes.md`](references/claude-code-prompt-recipes.md) | 35 named recipes covering setup, planning, execution, review, debug/recovery, and session economics |
| Should I route a coding task to a cheap or premium model? | [`references/multi-model-routing-economics.md`](references/multi-model-routing-economics.md) | 85/15 routing pattern, cost/context tradeoffs — re-verify live numbers before costing |

## When To Use

- Create a new coding agent from scratch on any supported platform
- Choose the right archetype for a coding task (review, test generation, refactoring, migration, docs, security)
- Design a multi-agent team for complex coding tasks (parallel reviews, bug investigation, migration fleets)
- Design context loading strategy for agents working with large codebases
- Wrap existing dev tools (linters, formatters, test runners, type checkers) for agent use
- Debug a coding agent producing poor results, hallucinated files, or scope creep
- Port a coding agent between platforms (Claude Code ↔ Codex ↔ Agent SDK)

## Use Other Skills

| Need | Use Instead |
|------|-------------|
| Agent architecture decisions, build-vs-not | [`../ai-agents/SKILL.md`](../ai-agents/SKILL.md) |
| Subagent frontmatter, delegation contracts | `agents-subagents` — current fields include `name`, `description`, `model` (alias `fable` valid), `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `initialPrompt`, `background`, `isolation` (`worktree` only value), `color`; `permissionMode` field noted but `auto` value and plugin-subagent restrictions apply — see [`../ai-coding-agents-permissions/SKILL.md`](../ai-coding-agents-permissions/SKILL.md); `Agent(type)` tool-scoping syntax gates spawnable subagent types |
| MCP server setup and integration | [`../agents-mcp/SKILL.md`](../agents-mcp/SKILL.md) |
| Hook guardrails and lifecycle events | [`../agents-hooks/SKILL.md`](../agents-hooks/SKILL.md) |
| Skill packaging and SKILL.md conventions | [`../agents-skills/SKILL.md`](../agents-skills/SKILL.md) |
| Generic multi-agent orchestration, wave dispatch | [`../agents-swarm-orchestration/SKILL.md`](../agents-swarm-orchestration/SKILL.md) |
| AGENTS.md (Codex-originated convention) and CLAUDE.md (Claude Code equivalent) configuration | [`../agents-memory/SKILL.md`](../agents-memory/SKILL.md) |
| Slash-command runtime architecture for coding-agent CLIs | [`../ai-coding-agents-command-runtime/SKILL.md`](../ai-coding-agents-command-runtime/SKILL.md) |
| Trace, replay, regression evals, and cost accounting | [`../ai-coding-agents-observability-evals/SKILL.md`](../ai-coding-agents-observability-evals/SKILL.md) |
| Plugin and extension architecture for coding agents | [`../ai-coding-agents-plugins/SKILL.md`](../ai-coding-agents-plugins/SKILL.md) |
| Tool approvals, allow/ask/deny rules, and permission routing | [`../ai-coding-agents-permissions/SKILL.md`](../ai-coding-agents-permissions/SKILL.md) |
| Model-provider abstraction, streaming normalization, and fallback routing | [`../ai-coding-agents-provider-runtime/SKILL.md`](../ai-coding-agents-provider-runtime/SKILL.md) |
| Packaging, update channels, cache migrations, and plugin compatibility | [`../ai-coding-agents-release-distribution/SKILL.md`](../ai-coding-agents-release-distribution/SKILL.md) |
| Session lifecycle, resume, rewind, and transcript restoration | [`../ai-coding-agents-sessions/SKILL.md`](../ai-coding-agents-sessions/SKILL.md) |
| Local UI plus remote execution architecture | [`../ai-coding-agents-remote-runtime/SKILL.md`](../ai-coding-agents-remote-runtime/SKILL.md) |
| Process isolation, filesystem policy, network controls, and destructive-command boundaries | [`../ai-coding-agents-execution-sandbox/SKILL.md`](../ai-coding-agents-execution-sandbox/SKILL.md) |
| Settings precedence, managed policy, and runtime config reload | [`../ai-coding-agents-settings-policy/SKILL.md`](../ai-coding-agents-settings-policy/SKILL.md) |
| Terminal-first REPL and coding-agent interaction design | [`../ai-coding-agents-terminal-ui/SKILL.md`](../ai-coding-agents-terminal-ui/SKILL.md) |
| Background task runtimes, teammate queues, and task ownership | [`../ai-coding-agents-tasks/SKILL.md`](../ai-coding-agents-tasks/SKILL.md) |
| Tool registry, tool search, and tool execution architecture | [`../ai-coding-agents-tools/SKILL.md`](../ai-coding-agents-tools/SKILL.md) |
| Testing coding agents (evals, regression) | [`../qa-agent-testing/SKILL.md`](../qa-agent-testing/SKILL.md) |
| Context loading strategies (generic) | [`../dev-context-engineering/SKILL.md`](../dev-context-engineering/SKILL.md) |
| Measuring coding agent ROI | [`../dev-ai-coding-metrics/SKILL.md`](../dev-ai-coding-metrics/SKILL.md) |
| Claude API and Agent SDK reference | claude-api skill |

## Default Workflow

1. **Classify the task**: What code does the agent touch? What tools does it need? What is the output?
2. **Single agent or team?** One bounded task → single agent. Multiple interdependent tasks, parallel reviews, or complex investigation → multi-agent team.
3. **Pick the archetype** closest to your need from the [archetypes](#single-agent-archetype-index) or [multi-agent patterns](#multi-agent-pattern-index).
4. **Choose the platform**: Claude Code `.md` for repo-level agents, Codex `.toml` for Codex workflows, Agent SDK for programmatic integration.
5. **Start from the matching template** in [`assets/templates/`](assets/templates/).
6. **Scope tools** to the minimum needed. Read-only agents get Read, Grep, Glob. Edit agents add Edit, Write, Bash.
7. **Design the context strategy**: What files does the agent need? How does it discover them? What is the token budget?
8. **Add verification**: How does the agent check its own work? For teams: assign a separate verifier.
9. **Smoke test**: Run on 3+ representative tasks before deploying.
10. **Iterate**: Observe real behavior, tighten scope, improve prompts.

## Known Traps

- giving a coding agent repo-wide edit authority before the owned files and verification surface are clear
- asking the same agent to implement, review, and approve its own high-risk changes
- inheriting parent context blindly across phases instead of re-briefing from current repo truth
- building a multi-agent coding team before the task graph, file ownership, and merge plan exist
- assuming Claude Code, Codex, and SDK workers expose equivalent tools, hooks, and approval semantics

## Common Anti-Patterns

- "full-stack fixer" agents with no bounded artifact, path, or runtime scope
- tool wrappers that hide destructive commands behind vague natural-language instructions
- edit-capable workers launched in parallel on the same branch with no ownership contract
- context strategies that preload too much code instead of progressive disclosure and file selection
- smoke tests skipped because the prompt "looks right"

## OpenAI Internal Practice (Codex, 2026-05)

Source: [*How OpenAI uses Codex*](https://cdn.openai.com/pdf/6a2631dc-783e-479b-b1a4-af0cfbd38630/how-openai-uses-codex.pdf), May 2026 — internal-usage report across Security, Product, Frontend, API, Infrastructure, and Performance Engineering teams. These patterns are validated by daily use inside OpenAI; cite this source rather than restating as your own observations.

### Two-stage Ask → Code flow for non-trivial changes

- **Pattern:** for any change above the trivial single-file fix, run Ask Mode first to produce an implementation plan. Then switch to Code Mode and feed the plan as input to follow-up prompts.
- **Why:** keeps the agent grounded; the plan becomes a self-correction surface — if the plan is wrong, the human catches it before generation rather than after.
- **Anti-pattern:** going straight to Code Mode for a multi-file change. The agent will improvise structure that the human then has to reverse-engineer at review time.
- **Recipe:** *"Plan the implementation for X. Do not write code yet."* → review plan → *"Execute the plan above, file by file."*

### Environment-as-prompt (compoundable)

- **Pattern:** treat the agent's runtime environment — startup script, env vars, internet access — as part of the persistent prompt. Iterate on env config every time a build error appears and ask whether the env should have prevented it.
- **Why:** env improvements compound. A startup script that installs the right toolchain once removes a category of errors from every future task in the repo.
- **Anti-pattern:** treating env failures as one-off prompt fixes. The agent re-discovers the same gap on every new task.
- **Recipe:** maintain a single `setup.sh` (or equivalent) that the agent runs at session start; add to it when a class of build error recurs.

### Prompt-as-GitHub-Issue

- **Pattern:** structure prompts the way you would write a PR description or issue — file paths, component names, diffs, doc snippets, and "implement this the same way it's done in [module X]" anchors.
- **Why:** the model already responds well to PR/issue-shaped text from training distribution; this is free signal that doesn't require new tooling.
- **Anti-pattern:** chat-shaped prompts ("can you change the auth flow?") that omit the repo coordinates the agent needs to act precisely.

### Task queue as lightweight backlog

- **Pattern:** fire off tangential ideas, partial work, or incidental fixes as separate Codex tasks rather than holding them in human working memory. The queue *is* the backlog; no obligation to produce a full PR per task.
- **Why:** captures drive-by fixes without forcing context switches; staging area mirrors the engineer's working set.
- **Where this lives in this skill:** see [`../ai-coding-agents-tasks/SKILL.md`](../ai-coding-agents-tasks/SKILL.md) for the task-runtime detail and the sizing heuristic (~1 hour of human work / a few hundred LOC).

### Best-of-N as a generation primitive

- **Pattern:** generate N parallel solutions for a single task and either pick the best or combine parts of multiple outputs.
- **Why:** for ambiguous or open-ended tasks, the cheapest quality-improving move is variance, not better prompting.
- **Anti-pattern:** running Best-of-N on tasks with one obviously correct shape (mechanical refactors, type fixes). Wasted compute; pick prompt engineering instead.
- **Vendor scope:** Codex-specific feature surface. The equivalent on other runtimes is parallel subagent dispatch — see [`../agents-swarm-orchestration/SKILL.md`](../agents-swarm-orchestration/SKILL.md).

## Platform Decision Tree

| Scenario | Platform | Why |
|----------|----------|-----|
| Repo-team agent, auto-delegated by description | Claude Code `.md` | Description-driven routing, shared via `.claude/agents/` |
| Codex thread workers | Codex `.toml` | Explicit spawning, sandbox-mode scoped |
| Codex as tool inside an editor or AI orchestrator | `codex mcp-server` (stdio) | Codex acts as an MCP server; editor drives it over MCP wire protocol |
| Non-interactive code review in CI | `codex review` subcommand | Headless, no terminal UI; structured output for pipelines |
| Programmatic, CI, or API integration | Agent SDK | Full control, custom tools, hook callbacks |
| Quick prototype | Claude Code `.md` | Fastest path to working agent |
| Multi-agent coordinator team | Claude Code `.md` | Native coordinator mode, fork, and team support |
| Custom orchestration logic | Agent SDK | Programmatic control over spawning, routing, results |
| Local-first OSS coding agent, editor-integrated via ACP (Zed, JetBrains, IntelliJ) | Goose (Rust) + recipe YAML | ACP server mode; 70+ MCP extensions; custom-distros; Apache-2.0 |
| Enterprise white-label coding agent with pinned providers and extensions | Goose Custom Distribution | Distro manifest baked into the binary; supply-chain gates (`deny.toml`); AAIF/LF governance |
| GitHub-centric repo, lightweight PR-aware agent, no multi-agent need | GitHub Copilot CLI custom agent (`.agent.md`) | Pre-wired GitHub MCP server, PR-scoped agent versioning; see Copilot CLI section below for its ceiling |

See [`references/platform-patterns.md`](references/platform-patterns.md) for side-by-side comparison and porting guide.

### Goose as a fourth platform (2026)

Goose (github.com/aaif-goose/goose, formerly github.com/block/goose) is a 50k+-star Rust-based OSS coding agent donated by Block to the Agentic AI Foundation (AAIF) under the Linux Foundation. It is a meaningfully different platform from Claude Code / Codex / Agent SDK:

- **Protocols:** first-class MCP *and* ACP. Goose runs as an ACP server (`goose acp`) so editors drive it over stdio; Goose can also delegate to external ACP agents (Claude Code, Codex) as providers.
- **Unit of work:** a **recipe** — YAML with `version / title / description / instructions / extensions / activities / prompt / parameters`. Recipes are portable, statically validated, and declare their extension dependencies inline.
- **Distribution:** supports custom distros (white-label, pinned providers/extensions, branded binaries) as a first-class shipping class.
- **Project hints:** uses `.goosehints` alongside `AGENTS.md` — one more member of the narrative-hint family (see `../agents-memory/SKILL.md`).

Treat it as the target when a coding agent must be OSS, editor-embedded, locally-operated, or enterprise-forkable. Detailed patterns live in the subsystem skills under "Cross-Platform Patterns (Goose)" sections — most relevantly in `ai-coding-agents-provider-runtime` (toolshim, agent-as-provider), `ai-coding-agents-remote-runtime` (ACP stdio, daemon+OpenAPI), `ai-coding-agents-tasks` (recipes as typed blueprints), and `ai-coding-agents-release-distribution` (custom distros).

### GitHub Copilot CLI — a fifth, lighter-weight platform (revised 2026)

GitHub Copilot CLI outgrew its "explains shell commands" origin during 2026. It now defines **custom agents** as Markdown files with YAML frontmatter (`.agent.md`, resolvable at repo or org scope), supports a **plugin system** (`/plugin install owner/repo`) that bundles MCP servers, agents, skills, and hooks, and ships with the GitHub MCP server pre-wired plus built-in `Explore` and `Task` agents. This makes Track A (define an agent on an existing platform) applicable to Copilot CLI in a way it was not a year earlier — treat the earlier "not a coding-agent platform" framing as retired.

**Frontmatter shape:** `description` (required), `name`, `target` (`vscode` | `github-copilot`), `tools` (omit or `["*"]` for all; empty list disables all; MCP tools namespaced as `server-name/tool-name`), `model`, `disable-model-invocation`, `user-invocable`. Body is Markdown instructions, capped at 30,000 characters. Versioning rides on git commit SHAs rather than a semantic `version` field.

**Where it still falls short of Track B territory:** no native multi-agent orchestration (agents can invoke each other via an `agent` tool alias, but there is no coordinator/fork/team primitive), no formal session-resume or task-graph model, and no sandbox-mode equivalent to Codex's `workspace-write` / `read-only` / `network-off`. Do not port a coordinator-led team or peer-swarm design onto it — the primitives that make those patterns safe (worktree isolation, mailbox protocol, owned-files enforcement) are absent.

**When to prefer Copilot CLI:** a GitHub-centric repo where a lightweight, PR-aware custom agent is enough — GitHub MCP tools and PR-scoped agent versioning are first-class — and you do not need multi-agent coordination or fine-grained sandbox modes. Prefer Claude Code or Codex when the task needs a coordinator/team pattern, worktree isolation, or a documented permission-mode ladder. Verify current field names and limits against `docs.github.com/en/copilot` before depending on specifics — this surface is still moving faster than the rest of the platform list. Use [`scripts/smoke_test.sh`](scripts/smoke_test.sh) to validate that your primary coding-agent setup (Claude Code, Codex, or Agent SDK) is healthy independent of which platform you pick for a given repo.

## Single Agent Archetype Index

| Archetype | Core Tools | maxTurns | Key Constraint | Template |
|-----------|-----------|----------|----------------|----------|
| Code Reviewer | Read, Grep, Glob, Bash | 8 | Read-only, findings-first output | [`code-reviewer.md`](assets/templates/code-reviewer.md) |
| Test Generator | Read, Write, Edit, Bash, Grep | 15 | Must run generated tests | [`test-generator.md`](assets/templates/test-generator.md) |
| Refactoring Agent | Read, Edit, Bash, Grep, Glob | 20 | Preserve behavior, run existing tests | [`refactoring-agent.md`](assets/templates/refactoring-agent.md) |
| Migration Agent | Read, Write, Edit, Bash, Grep, Glob | 25 | Pattern-at-a-time, checkpoint between batches | [`migration-agent.md`](assets/templates/migration-agent.md) |
| Documentation Agent | Read, Write, Grep, Glob | 12 | Source-anchored, no invented APIs | Universal template |
| Security Scanner | Read, Grep, Glob, Bash | 10 | Read-only, severity-ordered output | [`security-scanner.md`](assets/templates/security-scanner.md) |

Each archetype is detailed in [`references/agent-archetypes.md`](references/agent-archetypes.md) with full frontmatter, system prompt structure, and failure modes.

## Multi-Agent Pattern Index

| Pattern | Communication | Isolation | Best For | Template |
|---------|--------------|-----------|----------|----------|
| Coordinator-Led Team | `<task-notification>` XML | Workers in background | Research → implement → verify loops | [`coordinator-coding-team.md`](assets/templates/coordinator-coding-team.md) |
| Fork Subagents | Implicit (context inherited) | Shared prompt cache | Parallel background exploration | See fork guidance below |
| Agent Teams (Peer Swarm) | Mailbox messaging (SendMessage) | Git worktrees per teammate | Self-coordinating specialists | [`swarm-investigation.md`](assets/templates/swarm-investigation.md) |
| Background Agents | Daemon-supervised processes; `claude --bg`, `/bg`, `claude agents` dashboard | Git worktree per session (auto-created under `.claude/worktrees/`) | Long-running parallel tasks, tasks dispatched and monitored without keeping a terminal open | See background agent guidance below |
| ACP-Delegated Subagent | ACP stdio (line-delimited JSON) | Separate process; approvals round-trip through orchestrator | Cross-platform delegation (Goose → Claude Code, Goose → Codex, etc.) | See ACP delegation note below |

### When to use which pattern

**Coordinator-Led Team** — You want a single leader that synthesizes findings and directs workers. Workers run in background, report via notifications. The coordinator retains full understanding and authority. Best for structured multi-phase workflows: parallel research → coordinator synthesis → directed implementation → independent verification.

**Fork Subagents** — You want cheap parallel background work that inherits your current context. Forks share the parent's prompt cache (fast, low cost). The parent doesn't see intermediate work — only the final report. Best for: "search these 5 modules in parallel while I continue thinking."

**Agent Teams (Peer Swarm)** — You want teammates that communicate directly with each other via mailboxes. Each teammate has its own worktree for isolation. They share a task list and can self-coordinate without the lead directing every step. Best for: complex investigations where specialists need to discuss findings, large-scale migrations with many independent workers.

**Background Agents** — You want to dispatch tasks that run without a terminal attached and resume at any time. Start with `claude --bg "<task>"` from the shell, `/bg` inside a session, or the dispatch input in `claude agents`. The daemon supervisor keeps sessions alive; each session gets an isolated git worktree under `.claude/worktrees/`. Monitor all sessions in the `claude agents` dashboard (grouped by Needs input / Working / Completed); peek without attaching via Space; use `claude agents --json` to list sessions in CI. Session state lives under `~/.claude/jobs/<id>/state.json`; the roster is at `~/.claude/daemon/roster.json`. Disable with the `disableAgentView` managed setting or `CLAUDE_CODE_DISABLE_AGENT_VIEW` env var. Best for: long parallel tasks, tasks that outlive your terminal session, fleet-style coding work. Source: `code.claude.com/docs/en/agent-view` and `claude.com/blog/agent-view-in-claude-code`.

**ACP-Delegated Subagent** — You want one coding agent to spawn another coding agent over the **Agent Client Protocol** (stdio) and treat the delegated agent as either a turn-scoped provider or a session-scoped subagent. The orchestrator retains approval authority; approvals raised by the delegated agent round-trip back through ACP. Best for: cross-platform delegation (Goose orchestrating Claude Code; Claude Code delegating a specialist Codex session), heterogeneous teams where different agents have different provider access, and keeping a single approval surface across multi-agent work. The provider-side framing lives in `../ai-coding-agents-provider-runtime/SKILL.md` (agent-as-provider); the remote-runtime framing lives in `../ai-coding-agents-remote-runtime/SKILL.md` (ACP stdio transport, agent-delegating mode).

See [`references/multi-agent-coding-patterns.md`](references/multi-agent-coding-patterns.md) for full architecture details, coding workflows, and anti-patterns.

### Multi-agent principles (from Claude Code source)

These apply across all patterns:

1. **Never delegate understanding.** The coordinator/lead must synthesize findings before directing implementation. Never write "based on your findings, fix it" — include file paths, line numbers, exact changes.
2. **Freeze interfaces before dispatch.** Define contracts, owned files, and expected outputs before launching workers.
3. **Give every worker exclusive owned_files.** Prevents merge conflicts in parallel edit scenarios.
4. **Use separate verifiers.** Never let an agent verify its own work. Spawn a fresh worker with adversarial posture.
5. **Spawn fresh at phase boundaries.** Exploration → implementation is a context rotation point. Don't reuse a research worker for implementation — spawn fresh with synthesized specs.
6. **Persist state in files.** Task graphs, decisions, and dependency outputs go in JSON/YAML/Markdown files, not just conversation memory.
7. **Escalation, not retry.** Worker self-corrects once → escalates to lead → lead diagnoses and reassigns → human if still stuck.
8. **Background is the default now — plan around notifications, not blocking.** As of Claude Code v2.1.198, every `Agent` spawn (named or fork) defaults to background execution; Claude only runs a subagent in the foreground when it needs the result immediately. Don't add `background: true` out of habit — it's the resting state. What still matters: background workers surface their own permission prompts in the main session (since v2.1.186), so a worker needing an approval does not silently stall — expect and handle that interruption in the workflow, not just the happy path.
9. **Nesting is allowed to depth 5 — that's a ceiling, not a target.** Since v2.1.172, subagents (including forks, which count toward the cap since v2.1.187) can spawn their own subagents up to 5 levels below the main conversation; a depth-5 agent loses Agent-tool access entirely. Treat this the way you'd treat recursion depth in code: technically available doesn't mean advisable. Each level compounds cost and loses synthesis fidelity — a depth-3 worker's "findings" have already been summarized twice before the lead sees them. Default to flat coordinator/fork/team patterns (depth 1-2) and only reach for deeper nesting when a sub-problem is itself decomposable into independent, boundable sub-tasks — not as a way to avoid writing a clear brief.

## Context Management Essentials

Coding agents consume context differently from general agents because code files are large and interdependent.

**Token budget model**: Split the context window into three buckets:
- **Instructions** (~15-20%): System prompt, skill content, agent rules
- **Code** (~50-60%): File contents the agent reads during work
- **Output** (~20-30%): The agent's reasoning, tool calls, and generated code

**File selection strategy**:
- **Known paths**: Use Read directly when you know which file to examine
- **Discovery**: Use Grep/Glob first to find relevant files, then Read targeted sections
- **Progressive disclosure**: Start with directory structure (ls), then key files (package.json, tsconfig), then specific code

**The explore-then-act pattern** (from Claude Code's built-in architecture): Separate read-only exploration from editing. The Explore agent uses a strict read-only constraint with parallel tool calls for speed. After exploration, a fresh agent receives synthesized findings and makes focused edits.

**When to split into subagents**: If the task touches more than 5-10 files across different modules, or the agent starts losing track of earlier context, split into focused subagents with clear file ownership.

**Skill-subagent context isolation**: Skills and subagents can reference each other bidirectionally. A subagent can preload skills via the `skills:` field (role with baked-in domain knowledge), or a skill can delegate to a subagent via `context: fork` (task isolation without a full agent file). See `agents-subagents` for the full pattern and decision table.

See [`references/context-management.md`](references/context-management.md) for detailed strategies including multi-agent context management.

## Templates and Entry Points

### Single Agent Templates

| Template | Use Case |
|----------|----------|
| [`claude-code-agent.md`](assets/templates/claude-code-agent.md) | Universal Claude Code coding agent starting point |
| [`code-reviewer.md`](assets/templates/code-reviewer.md) | Read-only code review with severity-ordered findings |
| [`test-generator.md`](assets/templates/test-generator.md) | Test creation with self-validation |
| [`refactoring-agent.md`](assets/templates/refactoring-agent.md) | Behavior-preserving structural changes |
| [`migration-agent.md`](assets/templates/migration-agent.md) | Batch pattern transformation with checkpoints |
| [`security-scanner.md`](assets/templates/security-scanner.md) | Security analysis with evidence-based findings |

### Multi-Agent Templates

| Template | Use Case |
|----------|----------|
| [`coordinator-coding-team.md`](assets/templates/coordinator-coding-team.md) | Leader-directed research → implement → verify team |
| [`swarm-investigation.md`](assets/templates/swarm-investigation.md) | Peer-coordinated bug investigation with specialists |
| [`parallel-review-team.md`](assets/templates/parallel-review-team.md) | Parallel code review with security, performance, and style specialists |

### Cross-Platform Templates

| Template | Use Case |
|----------|----------|
| [`codex-agent.toml`](assets/templates/codex-agent.toml) | Codex custom agent definition |
| [`sdk-agent-py.py`](assets/templates/sdk-agent-py.py) | Python Agent SDK scaffolding with custom tools |
| [`sdk-agent-ts.ts`](assets/templates/sdk-agent-ts.ts) | TypeScript Agent SDK scaffolding |

### Checklists

| Checklist | Use Case |
|-----------|----------|
| [`agent-design-checklist.md`](assets/checklists/agent-design-checklist.md) | Pre-creation validation for single agents |
| [`multi-agent-checklist.md`](assets/checklists/multi-agent-checklist.md) | Pre-dispatch validation for coding teams |
| [`production-readiness.md`](assets/checklists/production-readiness.md) | Deployment readiness gate |

### Recommended Build Order

For a new CLI coding-agent runtime, implement subsystems in this order:

1. settings and policy layering
2. command registry and lazy command loading
3. provider abstraction, streaming normalization, and context-window policy
4. execution sandbox, workspace mounts, network policy, and destructive-command guards
5. tool contract, built-in enumeration, and tool-pool assembly
6. permission context and approval routing
7. central tool-execution pipeline
8. session persistence, history, and resume
9. remote transport and permission bridging
10. task runtime and teammate orchestration
11. terminal UI, background-task surfaces, and virtualization
12. plugin loading, versioned cache, and managed extension policy
13. observability, replay, regression evals, and release gates
14. packaging, update channels, migrations, and distribution

Why this order:

- earlier layers define the contracts later layers consume
- permission and session flows are hard to retrofit once tools and UI exist
- remote runtime, tasks, and terminal UI depend on stable command, tool, and settings semantics
- plugins should land after the host runtime has clear ownership of precedence and trust boundaries

## Core Runtime Spine

Treat a serious coding-agent runtime as a fixed spine of cooperating subsystems, not as one prompt plus a tool runner.

1. settings and policy define what the runtime is allowed to do
2. command runtime defines how users and the host invoke higher-level actions
3. provider runtime defines how model traffic is normalized and recovered
4. execution sandbox defines the real security envelope
5. tools define callable capabilities and execution stages
6. permissions decide when risky actions are allowed
7. sessions decide what state survives and resumes
8. remote runtime bridges local UI to remote execution when needed
9. tasks represent long-running and delegated work
10. terminal UI renders and controls runtime state without owning it
11. plugins extend the host through controlled capability points and layered refresh
12. observability and evals close the feedback loop
13. release and distribution keep upgrades, caches, and compatibility survivable

If one of these is missing, the usual outcome is not “slightly worse UX.” The usual outcome is hidden fragility that appears under reconnects, long sessions, remote control, worker delegation, or upgrades.

### Cross-platform validation (2026)

The spine above is rebuilt-and-verified against the Claude Code lineage and, as of 2026-04, cross-checked against Goose (Rust, MCP+ACP, OSS under AAIF/Linux Foundation). Patterns that only appeared in the Claude Code snapshot but missed in Goose have been imported into the subsystem skills as "Cross-Platform Patterns (Goose)" sections. When designing a new runtime, read the Claude-Code-derived core *and* the Goose additions in each subsystem skill before committing to an architecture.

## Core Invariants

- one host-owned state model per subsystem
- typed contracts between subsystems instead of implicit shared assumptions
- cache invalidation is explicit and event-driven, not "restart and hope"
- recovery behavior classified by failure family, not generic retry loops
- approvals and sandboxing treated as runtime architecture, not prompt wording
- resume, remote control, and background work designed before polish layers
- telemetry keeps causal order and low-cardinality dimensions
- observability able to explain why the runtime did what it did

## Common False Shortcuts

- building the agent as “LLM + tools + prompt” with no subsystem boundaries
- adding permissions before sandboxing or vice versa and pretending they are interchangeable
- bolting on session resume after tools, UI, and remote flows already exist
- treating remote execution as “the same session over the network”
- memoizing discovery and registry state with no invalidation plan
- shipping plugins before the host owns precedence, trust, and cache policy
- letting cache identity ignore install context, path, or versioned state
- adding evals only after incidents instead of using them as a design constraint
- assuming a good local prototype will survive upgrades, worktrees, and delegation unchanged

## Navigation

### References
- [`references/creation-workflow.md`](references/creation-workflow.md) — End-to-end creation guide
- [`references/platform-patterns.md`](references/platform-patterns.md) — Claude Code vs Codex vs Agent SDK
- [`references/agent-archetypes.md`](references/agent-archetypes.md) — Six single-agent coding patterns
- [`references/multi-agent-coding-patterns.md`](references/multi-agent-coding-patterns.md) — Three multi-agent architectures
- [`references/context-management.md`](references/context-management.md) — Token budgets and file strategies
- [`references/tool-integration.md`](references/tool-integration.md) — Dev tool wrapping patterns
- [`references/debugging-guide.md`](references/debugging-guide.md) — Failure taxonomy and fixes
- [`references/production-patterns.md`](references/production-patterns.md) — Real patterns from Claude Code source
- [`references/claude-code-agent-runtime-patterns.md`](references/claude-code-agent-runtime-patterns.md) — Agent file shape, validation, and persistence
- [`references/claude-code-swarm-and-worktree-patterns.md`](references/claude-code-swarm-and-worktree-patterns.md) — Team files, teammate spawn inheritance, and worktree rules
- [`references/claude-code-skill-and-plugin-loading.md`](references/claude-code-skill-and-plugin-loading.md) — Skill frontmatter loading and built-in plugin behavior
- [`references/claude-code-prompt-recipes.md`](references/claude-code-prompt-recipes.md) — Named prompt recipes for setup, planning, execution, review, and debug/recovery
- [`references/multi-model-routing-economics.md`](references/multi-model-routing-economics.md) — Cheap-vs-premium routing pattern and CLI/MCP operational surfaces (time-decaying numbers — re-verify before costing)

### Assets
- [`assets/templates/`](assets/templates/) — Agent definition and team templates
- [`assets/checklists/`](assets/checklists/) — Design, dispatch, and deployment checklists

### Data
- [`data/sources.json`](data/sources.json) — Primary documentation and research references
- [`data/claude-code/`](data/claude-code/) — Moved graph/profile/report artifacts from the local `claude_code` source snapshot

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Agent definition field semantics come from the Claude Code source (`BaseAgentDefinition` type in `loadAgentsDir.ts`). If a field is described here, verify it against current runtime behavior before depending on it.
- The Claude Code implementation notes in the `claude-code-*` references are grounded in a local source snapshot and should be refreshed against live docs or upstream source before relying on volatile details.
- Multi-agent patterns (coordinator, fork, teams) are documented from Claude Code source and were re-verified against live docs as of 2026-07-11, including the depth-5 nesting cap (v2.1.172) and background-by-default Agent spawns (v2.1.198). Both are runtime constants/defaults that can change without notice — re-check `code.claude.com/docs/en/sub-agents` before depending on the exact figures.
- Platform-specific capabilities (Codex sandbox modes and current model names, SDK hook patterns, GitHub Copilot CLI's custom-agent and plugin surface) should be verified against current platform documentation — the Copilot CLI section in particular changed materially during 2026 and moves faster than the rest of this platform list.
- Star counts, model names, and other numeric/product-name claims cited for Goose, career-ops, and similar community projects drift continuously; treat any figure here as a snapshot, not a live value.
- Templates are starting points. Always test with real tasks before deploying.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

