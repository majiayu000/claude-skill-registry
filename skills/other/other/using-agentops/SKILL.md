---
name: using-agentops
description: Explain AgentOps workflows.
practices:
- wiki-knowledge-surface
- pragmatic-programmer
- agile-manifesto
hexagonal_role: generic
consumes: []
produces:
- documentation
context_rel: []
skill_api_version: 1
user-invocable: false
context:
  window: isolated
  intent:
    mode: none
  sections:
    exclude:
    - HISTORY
    - INTEL
    - TASK
  intel_scope: none
metadata:
  tier: meta
  dependencies: []
  internal: true
output_contract: 'stdout: operating guide'
---
# AgentOps Operating Model

AgentOps is the operational layer for coding agents.

Publicly, it gives you four things:

- **Bookkeeping** — captured learnings, findings, and reusable context
- **Validation** — plan and code review before work ships
- **Primitives** — single skills, hooks, and CLI surfaces
- **Flows** — named compositions like `/research`, `/validation`, and `/rpi`

Technically, AgentOps acts as a context compiler: raw session signal becomes reusable knowledge, compiled prevention, and better next work.

## Core Flow: RPI

```
Research → Plan → Implement → Validate
    ↑                            │
    └──── Knowledge Flywheel ────┘
```

### Research Phase

```bash
/research <topic>      # Deep codebase exploration
ao search "<query>"    # Search existing knowledge
ao search "<query>" --cite retrieved  # Record adoption when a search result is reused
ao lookup <id>         # Pull full content of specific learning
ao lookup --query "x"  # Search knowledge by relevance
```

**Output:** `.agents/research/<topic>.md`

### Plan Phase

```bash
/pre-mortem <spec>     # Simulate failures (error/rescue map, scope modes, prediction tracking)
/plan <goal>           # Decompose into trackable issues
```

**Output:** Beads issues with dependencies

### Implement Phase

```bash
/implement <issue>     # Single issue execution
/crank <epic>          # Autonomous epic loop (uses swarm for waves)
/swarm                 # Parallel execution (fresh context per agent)
```

**Output:** Code changes, tests, documentation

### Validate Phase

```bash
/vibe [target]         # Code validation (finding classification + suppression + domain checklists)
/post-mortem           # Validation + streak tracking + prediction accuracy + retro history
/retro                 # Quick-capture a single learning
```

**Output:** `.agents/learnings/`, `.agents/patterns/`

## Phase-to-Skill Mapping

| Phase | Primary Skill | Supporting Skills |
|-------|---------------|-------------------|
| **Discovery** | `/discovery` | `/brainstorm`, `/research`, `/plan`, `/pre-mortem` |
| **Implement** | `/crank` | `/implement` (single issue), `/swarm` (parallel execution) |
| **Validate** | `/validation` | `/vibe`, `/post-mortem`, `/retro`, `/forge` |

**Choosing the skill:**
- Use `/implement` for **single issue** execution. **Now defaults to TDD-first** — writes failing tests before implementing. Skip with `--no-tdd`.
- Use `/crank` for **autonomous epic execution** (loops waves via swarm until done). Auto-generates file-ownership maps to prevent worker conflicts.
- Use `/discovery` for the **discovery phase only** (brainstorm → search → research → plan → pre-mortem).
- Use `/validation` for the **validation phase only** (vibe → post-mortem → retro → forge).
- Use `/rpi` for **full lifecycle** — delegates to `/discovery` → `/crank` → `/validation`.
- Use `/ratchet` to **gate/record progress** through RPI.

## Start Here (12 starters)

These are the skills every user needs first. Everything else is available when you need it.

| Skill | Purpose |
|-------|---------|
| `/quickstart` | Guided onboarding — run this first |
| `/bootstrap` | One-command full AgentOps setup — fills gaps only |
| `/research` | Deep codebase exploration |
| `/council` | Multi-model consensus review + finding auto-extraction |
| `/validate` | Canonical PASS/WARN/FAIL verdict over an artifact, plan, code change, PR, or gate |
| `/vibe` | Code validation (classification + suppression + domain checklists) |
| `/rpi` | Full RPI lifecycle orchestrator (`/discovery` → `/crank` → `/validation`) |
| `/implement` | Execute single issue |
| `/retro --quick` | Quick-capture a single learning into the flywheel |
| `/status` | Single-screen dashboard of current work and suggested next action |
| `/goals` | Maintain GOALS.yaml fitness specification |
| `/push` | Atomic test-commit-push workflow |

## Advanced Skills (when you need them)

| Skill | Purpose |
|-------|---------|
| `/compile`, `/flywheel` | Active knowledge intelligence and flywheel health — Mine → Grow → Defrag cycle |
| `/curate` | Canonical miner role for transcripts, `.agents/`, bd, git, skill diffs, and rare wiki entries |
| `/llm-wiki` | External reading wiki proposal — raw sources to compiled wiki |
| `/expert-council` | Alias for `/council --mode=debate` (kept 1 release) — adversarial named-persona duel |
| `/harvest` | Cross-rig knowledge consolidation — sweep, dedup, promote to global hub |
| `/knowledge-activation` | Operationalize a mature `.agents` corpus into beliefs, playbooks, briefings, and gap surfaces |
| `/brainstorm` | Structured idea exploration before planning |
| `/discovery` | Full discovery phase orchestrator (brainstorm → search → research → plan → pre-mortem) |
| `/plan` | Epic decomposition into issues |
| `/design` | Product validation gate — goal alignment, persona fit, competitive differentiation |
| `/pre-mortem` | Failure simulation (error/rescue, scope modes, temporal, predictions) |
| `/post-mortem` | Validation + streak tracking + prediction accuracy + retro history |
| `/bug-hunt` | Root cause analysis |
| `/release` | Pre-flight, changelog, version bumps, tag |
| `/crank` | Autonomous epic loop (uses swarm for each wave) |
| `/swarm` | Fresh-context parallel execution (Ralph pattern) |
| `/evolve` | Goal-driven fitness-scored improvement loop |
| `/autodev` | PROGRAM.md autonomous development contract setup and validation |
| `/dream` | Interactive Dream operator surface for setup, bedtime runs, and morning reports |
| `/doc` | Documentation generation |
| `/retro` | Quick-capture a learning (full retro → /post-mortem) |
| `/validation` | Full validation phase orchestrator (vibe → post-mortem → retro → forge) |
| `/ratchet` | Brownian Ratchet progress gates for RPI workflow |
| `/forge` | Mine transcripts for knowledge — decisions, learnings, patterns |
| `/readme` | Generate gold-standard README for any project |
| `/security` | Continuous repository security scanning and release gating |
| `/security-suite` | Binary and prompt-surface security suite — static analysis, dynamic tracing, offline redteam, policy gating |
| `/test` | Test generation, coverage analysis, and TDD workflow |
| `/hooks-authoring` | Author and validate AgentOps runtime hooks |
| `/red-team` | Persona-based adversarial validation — probe docs and skills from constrained user perspectives |
| `/review` | Review incoming PRs, agent output, or diffs — SCORED checklist |
| `/refactor` | Safe, verified refactoring with regression testing at each step |
| `/deps` | Dependency audit, update, vulnerability scanning, and license compliance |
| `/perf` | Performance profiling, benchmarking, regression detection, and optimization |
| `/system-tuning` | Restore system responsiveness via safe, ordered process cleanup and agent-swarm hygiene |
| `/scaffold` | Project scaffolding, component generation, and boilerplate setup |
| `/scenario` | Author and manage holdout scenarios for behavioral validation |
| `/skill-auditor` | Two-pass audit of an existing SKILL.md against the unified template (15 checks) |
| `/skill-builder` | Scaffold or absorb new SKILL.md files against the unified template |

## Expert Skills (specialized workflows)

| Skill | Purpose |
|-------|---------|
| `/grafana-platform-dashboard` | Build Grafana platform dashboards from templates/contracts |
| `/codex-team` | Parallel Codex agent execution |
| `/openai-docs` | Official OpenAI docs lookup with citations |
| `/oss-docs` | OSS documentation scaffold and audit |
| `/reverse-engineer-rpi` | Reverse-engineer a product into feature catalog and specs |
| `/pr-research` | Upstream repository research before contribution |
| `/pr-plan` | External contribution planning |
| `/pr-implement` | Fork-based PR implementation |
| `/pr-validate` | PR-specific validation and isolation checks |
| `/pr-prep` | PR preparation and structured body generation |
| `/pr-retro` | Learn from PR outcomes |
| `/complexity` | Code complexity analysis |
| `/product` | Interactive PRODUCT.md generation |
| `/handoff` | Session handoff for continuation |
| `/recover` | Post-compaction context recovery |
| `/trace` | Trace design decisions through history |
| `/provenance` | Trace artifact lineage to sources |
| `/beads` | Issue tracking operations |
| `/heal-skill` | Detect and fix skill hygiene issues |
| `/converter` | Convert skills to Codex/Cursor formats |
| `/update` | Reinstall all AgentOps skills from latest source |

## Knowledge Flywheel

Every `/post-mortem` promotes learnings and patterns into `.agents/` so future `/research` starts with better context instead of zero.

Inspect, lint, and triage the `.agents/` write surface contract via `ao agents inspect | lint | doctor` (`doctor` rolls up inspect + lint + orphan/stray-dir report; `--strict` fails on orphans).

## Runtime Modes

AgentOps has four runtime modes. Do not assume hook automation exists everywhere.

| Mode | When it applies | Start path | Closeout path | Guarantees |
|------|-----------------|------------|---------------|------------|
| `gc` | Gas City (`gc`) binary available and `city.toml` present | gc controller manages sessions; `ao rpi` auto-selects gc executor | gc event bus captures phase/gate/failure/metric events | Default when gc is available. Phase execution via gc sessions, events via gc event bus, agent health via gc health patrol |
| `hook-capable` | Claude/OpenCode with lifecycle hooks installed (no gc) | Runtime hook or `ao inject` / `ao lookup` | Runtime hook or `ao forge transcript` + `ao flywheel close-loop` | Automatic startup/context injection and session-end maintenance when hooks are installed |
| `codex-native-hooks` | Codex CLI v0.115.0+ with native hook support (March 2026) | Runtime hooks (same as hook-capable) | Runtime hooks (same as hook-capable) | Native lifecycle hooks — same guarantees as hook-capable mode |
| `codex-hookless-fallback` | Codex Desktop / Codex CLI pre-v0.115.0 without hook surfaces | `ao codex start` | `ao codex stop` | Explicit startup context, citation tracking, transcript fallback, and close-loop metrics without hooks |
| `manual` | No hooks and no Codex-native runtime detection | `ao inject` / `ao lookup` | `ao forge transcript` + `ao flywheel close-loop` | Works everywhere, but lifecycle actions are operator-driven |

## Issue Tracking

This workflow uses beads for git-native issue tracking:

```bash
bd ready              # Unblocked issues
bd show <id>          # Issue details
bd close <id>         # Close issue
bd vc status          # Inspect Dolt state if needed (JSONL auto-sync is automatic)
```

## Examples

**Startup context loading.** Hook-capable runtimes run `session-start.sh` at session start (`manual` mode auto-loads MEMORY.md and points to `ao search`/`ao lookup`; `lean` mode injects prior learnings on a reduced token budget). Codex v0.115.0+ fires hooks automatically; pre-v0.115.0 runs `ao codex start` / `ao codex stop` explicitly. Either way the agent gets the RPI workflow, prior context, and a citation path.

**Workflow reference during planning.** When a user asks how to approach a feature, the agent uses this skill's RPI section to recommend Research → Plan → Implement → Validate — `/research` for exploration, `/plan` for decomposition, `/pre-mortem` for failure simulation — instead of an ad-hoc approach.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Skill not auto-loaded | Hook runtime unavailable or startup path not run | Hook-capable runtimes: verify `hooks/session-start.sh` exists and is enabled. Codex: run `ao codex start` explicitly |
| Outdated skill catalog | This file not synced with actual skills/ directory | Update skill list in this file after adding/removing skills |
| Wrong skill suggested | Natural language trigger ambiguous | User explicitly calls skill with `/skill-name` syntax |
| Workflow unclear | RPI phases not well-documented here | Read full workflow guide in README.md or docs/ARCHITECTURE.md |
