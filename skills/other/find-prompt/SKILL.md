---
name: find-prompt
description: Route the current task to the right prompt(s) in this library, load them, and adopt them as your operating instructions for the rest of the conversation. Use when the user names a task ("add OAuth", "set up hooks", "review this PR", "pick a model"), asks which prompt to use, or says to "use the right prompt". Also use when you enter this repo and need to orient without reading every file.
argument-hint: [task description — optional; defaults to the current task in the conversation]
---

# Find the right prompt and run with it

You route the current task to the right file(s) in this library, **read them yourself**, and then **continue the existing work** under those instructions — not from scratch, but picking up the conversation and any task already in progress.

`${CLAUDE_SKILL_DIR}` is this skill's own directory (`<library-root>/.claude/skills/find-prompt/`). The library root is `${CLAUDE_SKILL_DIR}/../../..`. All prompt files are under `${CLAUDE_SKILL_DIR}/../../../prompts/english/`. Never hardcode an absolute path — always build it from `${CLAUDE_SKILL_DIR}` so this works for anyone who clones the library, wherever they put it.

If `${CLAUDE_SKILL_DIR}` is not substituted (it shows up literally), fall back: the skill sits next to `SKILL.md`; run `ls` up the tree from your working directory to find the folder containing `prompts/english/agents/claude-agent-system-prompt.md`.

## Steps

1. **Determine the task.** Use `$ARGUMENTS` if given. Otherwise use the task already being worked on in this conversation (the user's last real request, the in-progress work, the files open). If genuinely unclear, ask one short question and stop.

2. **Match the task** to the routing table below. Pick the **base** prompt plus **at most one** specialist or project-type prompt. Note any second optional prompt.

3. **Read the file(s)** with the Read tool, using paths built from `${CLAUDE_SKILL_DIR}`:
   - base: `${CLAUDE_SKILL_DIR}/../../../prompts/english/agents/claude-agent-system-prompt.md`
   - specialist: `${CLAUDE_SKILL_DIR}/../../../prompts/english/<path from the table>`
   If a path does not exist, tell the user to run `/update-prompts` and stop.

4. **Adopt them and continue.** Treat the base prompt as your operating system prompt and the specialist as the domain protocol for this task. Then:
   - Restate the current task in one line (from the conversation, not invented).
   - State the success criteria you'll hold yourself to.
   - Carry over every session constraint already established (no git, no server start, static-only, don't touch X, etc.).
   - Pick up the work where it stands — continue the in-progress task under the new protocol. Do not restart, do not re-ask what was already answered, do not re-explore what was already explored.

5. **Confirm in one short block** which prompts you loaded and what you're now doing, then proceed.

## Routing table

Paths are relative to `prompts/english/`.

### Running Claude Code itself (base prompt not needed — the Claude Code prompt is enough alone)

| Task is about… | Load |
|---|---|
| writing / debugging a skill, `SKILL.md` | `agents/agent-skills-prompt.md` |
| connecting a DB / browser / API / tool via MCP | `agents/mcp-integration-prompt.md` |
| a plugin, a marketplace, bundling/sharing config | `agents/claude-code-plugins-prompt.md` |
| a hook, running something on edit/commit/stop, blocking a command | `agents/hooks-automation-prompt.md` |
| subagents, parallel agents, dynamic workflows, `/batch`, whole-codebase audit, writer/reviewer | `agents/multi-agent-orchestration-prompt.md` |
| CLAUDE.md, settings.json, `.claude/rules`, permissions | `agents/claude-code-workflow-prompt.md` |
| effort levels, `ultrathink`, plan mode, how much to think | `agents/claude-code-modes-prompt.md` |
| which model to use, Opus vs Sonnet vs Haiku vs Fable, pricing | `workflows/model-selection-guide.md` |
| what a current Claude Code build can do — plan mode, rewind, headless, surfaces | `workflows/claude-code-native-features-guide.md` |
| building an agent in Python/TS, the Agent SDK, `query()` | `workflows/agent-sdk-guide.md` |
| AGENTS.md, one config across Cursor/Codex/Aider, the primary source for a claim | `workflows/reference-resources.md` |

### Building software (base = Agent System + the one specialist below)

| Task is about… | Specialist |
|---|---|
| web frontend — React/Vue/Angular/Svelte, a page, a component | `project-types/web-development-prompt.md` |
| a REST/GraphQL/gRPC API, an endpoint, a contract | `project-types/api-development-prompt.md` (+ `agents/api-design-graphql-prompt.md` for schema-first design) |
| an end-to-end app, frontend + backend together | `agents/fullstack-development-prompt.md` |
| iOS / Android / React Native / Flutter / KMP | `project-types/mobile-development-prompt.md` |
| a desktop app — Tauri / Electron / MAUI / Qt | `project-types/desktop-development-prompt.md` |
| a data pipeline — ETL, streaming, Kafka, Airflow, dbt | `agents/data-engineering-prompt.md` |
| an ML model, training, RAG, an LLM feature | `project-types/data-science-ml-prompt.md` (+ `agents/ai-llm-integration-prompt.md` for app-side integration) |
| Kubernetes, CI/CD, Terraform/OpenTofu, Docker, Cloudflare | `project-types/devops-cicd-prompt.md` (+ `agents/cloud-infrastructure-prompt.md` for multi-region / IaC depth) |
| a database schema, SQL, indexing, a slow query | `agents/database-optimization-prompt.md` (+ `project-types/database-sql-prompt.md` for data modeling) |
| a game — Unity / Unreal / Godot / Bevy, netcode | `project-types/game-development-prompt.md` |
| firmware, embedded, IoT, an MCU, an RTOS | `project-types/embedded-iot-prompt.md` |
| a smart contract, Solidity, web3, an L2 | `project-types/blockchain-web3-prompt.md` |
| anything else / language-agnostic | `project-types/general-software-development-prompt.md` |

### Improving existing code (base = Agent System + the one specialist below)

| Task is about… | Specialist |
|---|---|
| reviewing a PR or change set | `agents/code-review-prompt.md`. Also load `agents/ui-design-systems-prompt.md` if the change touches UI, or `agents/security-audit-prompt.md` if it touches auth/data. If git is available and you can see the diff, `/code-review` (the bundled skill) is an option too. |
| security — a vulnerability, threat model, auth, secrets | `agents/security-audit-prompt.md` |
| a production incident, "it's broken", root cause, a bug | `agents/debugging-troubleshooting-prompt.md` |
| reducing complexity or technical debt, cleaning up | `agents/refactoring-prompt.md` |
| adding tests, a test strategy, coverage, a flaky test | `agents/testing-strategies-prompt.md` |
| slowness — latency, throughput, cost, memory, bundle size | `agents/performance-optimization-prompt.md` |
| migrating a framework/runtime/DB, a major version bump | `agents/migration-upgrade-prompt.md` |
| logs, metrics, traces, alerting, observability | `agents/monitoring-observability-prompt.md` |
| fault tolerance — retries, circuit breakers, resilience | `agents/error-handling-resilience-prompt.md` |
| accessibility — WCAG, screen readers, a11y | `agents/accessibility-audit-prompt.md` |

### Deciding (base = Agent System + the one specialist below)

| Task is about… | Specialist |
|---|---|
| system design, an architecture pattern, trade-offs | `agents/architecture-patterns-prompt.md` |
| choosing a tool or library — "what should I use for X" | `agents/technology-stack-prompt.md` |
| GDPR / HIPAA / SOC 2 / PCI, regulated scope | `agents/compliance-governance-prompt.md` |
| branching, commits, the release process | `agents/git-version-control-prompt.md` |
| DX, linting, onboarding, the dev environment | `agents/developer-experience-tooling-prompt.md` |
| a monorepo, multi-package coordination, Turborepo/Nx | `agents/monorepo-complex-projects-prompt.md` |
| writing docs, a README, API reference | `agents/documentation-prompt.md` |
| a design system, tokens, a component library, theming | `agents/ui-design-systems-prompt.md` |

## Rules

- **One base + at most one specialist.** If two specialists seem to fit, load the primary and name the second as optional.
- The base is always `agents/claude-agent-system-prompt.md`, except for a task purely about running Claude Code (then the single Claude Code prompt is enough).
- Tiny task (typo, rename, one-line fix): don't load anything — say so and do it.
- **Continue, don't restart.** After loading, resume the conversation's in-progress work under the new instructions. Keep every fact, decision, and constraint already established.
- If nothing matches cleanly, read `${CLAUDE_SKILL_DIR}/../../../prompts/english/INDEX.md` and route from its task table.

## Confirmation block (output this, then keep working)

```
Loaded: agents/claude-agent-system-prompt.md + <specialist path>   [+ <optional second>]
Task (continuing): <one line, from the conversation>
Success criteria: <measurable>
Constraints carried over: <list, or "none">
```
Then proceed with the task under the loaded protocol — from where it stands, not from zero.
