---
name: council
description: 'Multi-model consensus council. Spawns parallel judges with configurable perspectives. Modes: validate, brainstorm, research. Triggers: "council", "get consensus", "multi-model review", "multi-perspective review", "council validate", "council brainstorm", "council research".'
skill_api_version: 1
context:
  window: isolated
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: full
metadata:
  tier: judgment
  dependencies:
    - standards   # optional - loaded for code validation context
  replaces: judge
output_contract: skills/council/schemas/verdict.json
---

# /council — Multi-Model Consensus Council

Spawn parallel judges with different perspectives, consolidate into consensus. Works for any task — validation, research, brainstorming.

## Quick Start

```bash
/council --quick validate recent                               # fast inline check
/council validate this plan                                    # validation (2 agents)
/council brainstorm caching approaches                         # brainstorm
/council research kubernetes upgrade strategies                # research
/council --preset=security-audit validate the auth system      # preset personas
/council --deep --explorers=3 research upgrade automation      # deep + explorers
/council --debate validate the auth system                     # adversarial 2-round review
/council                                                       # infers from context
```

Council works independently — no RPI workflow, no ratchet chain, no `ao` CLI required.

## Modes

| Mode | Agents | Execution Backend | Use Case |
|------|--------|-------------------|----------|
| `--quick` | 0 (inline) | Self | Fast single-agent check, no spawning |
| default | 2 | Runtime-native (Codex sub-agents preferred; Claude teams fallback) | Independent judges (no perspective labels) |
| `--deep` | 3 | Runtime-native | Thorough review |
| `--mixed` | 3+3 | Runtime-native + Codex CLI | Cross-vendor consensus |
| `--debate` | 2+ | Runtime-native | Adversarial refinement (2 rounds) |

### Spawn Backend (MANDATORY)

Council requires a runtime that can **spawn parallel subagents** and (for `--debate`) **send messages between agents**. Use whatever multi-agent primitives your runtime provides. If no multi-agent capability is detected, fall back to `--quick` (inline single-agent).

**Required capabilities:**
- **Spawn subagent** — create a parallel agent with a prompt (required for all modes except `--quick`)
- **Agent messaging** — send a message to a specific agent (required for `--debate`)

Skills describe WHAT to do, not WHICH tool to call. See `skills/shared/SKILL.md` for the capability contract.

**After detecting your backend, read the matching reference for concrete spawn/wait/message/cleanup examples:**
- Shared Claude feature contract → `skills/shared/references/claude-code-latest-features.md`
- Local mirrored contract for runtime-local reads → `references/claude-code-latest-features.md`
- Claude Native Teams → `references/backend-claude-teams.md`
- Codex Sub-Agents / CLI → `references/backend-codex-subagents.md`
- Background Tasks → `references/backend-background-tasks.md`
- Inline (`--quick`) → `references/backend-inline.md`

See also `references/cli-spawning.md` for council-specific spawning flow (phases, timeouts, output collection).

## When to Use `--debate`

Use `--debate` for high-stakes or ambiguous reviews where judges are likely to disagree:
- Security audits, architecture decisions, migration plans
- Reviews where multiple valid perspectives exist
- Cases where a missed finding has real consequences

Skip `--debate` for routine validation where consensus is expected. Debate adds R2 latency (judges stay alive and process a second round via backend messaging).

**Incompatibilities:**
- `--quick` and `--debate` cannot be combined. `--quick` runs inline with no spawning; `--debate` requires multi-agent rounds. If both are passed, exit with error: "Error: --quick and --debate are incompatible."
- `--debate` is only supported with validate mode. Brainstorm and research do not produce PASS/WARN/FAIL verdicts. If combined, exit with error: "Error: --debate is only supported with validate mode."

## Task Types

Council infers task type from natural language. Trigger words: **validate** (validate, check, review, assess, critique, feedback, improve), **brainstorm** (brainstorm, explore, options, approaches), **research** (research, investigate, deep dive, analyze, examine, evaluate, compare).

See [references/task-type-rigor-gate.md](references/task-type-rigor-gate.md) for the trigger-word table, the MANDATORY first-pass rigor gate for plan/spec validation, and the full `--quick` single-agent inline mode contract.

---

## Architecture

See [references/architecture-flow.md](references/architecture-flow.md) for the context-budget rule, full Phase 1→3 execution flow diagram, reviewer-config loading, graceful degradation table, effort levels, and pre-flight checks.

---

## Packet Format (JSON)

See [references/packet-format.md](references/packet-format.md) for the full JSON packet schema (fields, output_schema, judge-prompt boundary rules) and the Empirical Evidence Rule for feasibility reviews.

---

## Perspectives

> **Perspectives & Presets:** Use `Read` tool on `skills/council/references/personas.md` for persona definitions, preset configurations, and custom perspective details.

**Auto-Escalation:** When `--preset` or `--perspectives` specifies more perspectives than the current judge count, automatically escalate judge count to match. The `--count` flag overrides auto-escalation.

---

## Named Perspectives & Consensus

See [references/consensus-and-output.md](references/consensus-and-output.md) for named-perspective usage (`--perspectives`, `--perspectives-file`, YAML format, flag priority), consensus verdict rules (PASS/WARN/FAIL combination table, DISAGREE resolution), and the finding-extraction flywheel protocol. See [references/personas.md](references/personas.md) for built-in presets.

---

## Explorer Sub-Agents

> **Explorer Details:** Use `Read` tool on `skills/council/references/explorers.md` for explorer architecture, prompts, sub-question generation, and timeout configuration.

**Summary:** Judges can spawn explorer sub-agents (`--explorers=N`, max 5) for parallel deep-dive research. Total agents = `judges * (1 + explorers)`, capped at MAX_AGENTS=12.

---

## Debate Phase (`--debate`)

> **Debate Protocol:** Use `Read` tool on `skills/council/references/debate-protocol.md` for full debate execution flow, R1-to-R2 verdict injection, timeout handling, and cost analysis.

**Summary:** Two-round adversarial review. R1 produces independent verdicts. R2 sends other judges' verdicts via backend messaging (`send_input` or `SendMessage`) for steel-manning and revision. Only supported with validate mode.

---

## Agent Prompts

> **Agent Prompts:** Use `Read` tool on `skills/council/references/agent-prompts.md` for judge prompts (default and perspective-based), consolidation prompt, and debate R2 message template.

---

## Output Format & Consensus Rules

Consensus verdict combination rules, DISAGREE handling, and the finding-extraction flywheel protocol live in [references/consensus-and-output.md](references/consensus-and-output.md). Full report templates (validate, brainstorm, research) and debate-report additions live in [references/output-format.md](references/output-format.md). All reports write to `.agents/council/YYYY-MM-DD-<type>-<target>.md`. Findings extraction targets `.agents/council/extraction-candidates.jsonl`; see [references/finding-extraction.md](references/finding-extraction.md) for schema and classification heuristics.

Core consensus rules: All PASS -> PASS; Any FAIL -> FAIL; Mixed PASS/WARN -> WARN; cross-vendor disagreement -> DISAGREE.

---

## Configuration

**Minimum quorum:** 1 agent. **Recommended:** 80% of judges. On timeout, proceed with remaining judges and note in report. On user cancellation, shutdown all judges and generate partial report with INCOMPLETE marker.

| Env var | Default |
|---------|---------|
| `COUNCIL_CLAUDE_MODEL` | sonnet |
| `COUNCIL_EXPLORER_MODEL` | sonnet |
| `COUNCIL_CODEX_MODEL` | gpt-5.3-codex |
| `COUNCIL_TIMEOUT` | 120 |
| `COUNCIL_EXPLORER_TIMEOUT` | 60 |
| `COUNCIL_R2_TIMEOUT` | 90 |

| Flag | Description |
|------|-------------|
| `--technique=<name>` | Brainstorm technique (reverse, scamper, six-hats). See `references/brainstorm-techniques.md`. |
| `--profile=<name>` | Model quality profile (balanced, budget, fast, inherit, quality, thorough). See `references/model-profiles.md`. |

See [references/flags-reference.md](references/flags-reference.md) for the full flag and environment variable reference (`COUNCIL_TIMEOUT`, `COUNCIL_CODEX_MODEL`, `--deep`, `--mixed`, `--debate`, `--evidence`, `--commit-ready`, `--preset`, `--profile`, and all other flags).

---

## CLI Spawning Commands

> **CLI Spawning:** Use `Read` tool on `skills/council/references/cli-spawning.md` for team setup, Claude/Codex agent spawning, parallel execution, debate R2 commands, cleanup, and model selection.

---

## Examples

See [references/examples-extended.md](references/examples-extended.md) for the full example catalog and walkthroughs (fast single-agent validation, adversarial debate, cross-vendor consensus with explorers).

---

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for common error messages, causes, and solutions, plus the judge→council migration table.

---

## Multi-Agent Architecture

See [references/multi-agent-architecture.md](references/multi-agent-architecture.md) for the deliberation protocol, communication rules, Ralph Wiggum compliance, degradation behavior, and judge naming convention.

---

## See Also

- `skills/vibe/SKILL.md` — Complexity + council for code validation (uses `--preset=code-review` when spec found)
- `skills/pre-mortem/SKILL.md` — Plan validation (uses `--preset=plan-review`, always 3 judges)
- `skills/post-mortem/SKILL.md` — Work wrap-up (uses `--preset=retrospective`, always 3 judges + retro)
- `skills/swarm/SKILL.md` — Multi-agent orchestration
- `skills/standards/SKILL.md` — Language-specific coding standards
- `skills/research/SKILL.md` — Codebase exploration (complementary to council research mode)

## Reference Documents

- [references/architecture-flow.md](references/architecture-flow.md)
- [references/packet-format.md](references/packet-format.md)
- [references/flags-reference.md](references/flags-reference.md)
- [references/examples-extended.md](references/examples-extended.md)
- [references/troubleshooting.md](references/troubleshooting.md)
- [references/multi-agent-architecture.md](references/multi-agent-architecture.md)
- [references/task-type-rigor-gate.md](references/task-type-rigor-gate.md)
- [references/consensus-and-output.md](references/consensus-and-output.md)
- [references/model-routing.md](references/model-routing.md)
- [references/backend-background-tasks.md](references/backend-background-tasks.md)
- [references/backend-claude-teams.md](references/backend-claude-teams.md)
- [references/backend-codex-subagents.md](references/backend-codex-subagents.md)
- [references/backend-inline.md](references/backend-inline.md)
- [references/brainstorm-techniques.md](references/brainstorm-techniques.md)
- [references/claude-code-latest-features.md](references/claude-code-latest-features.md)
- [references/model-profiles.md](references/model-profiles.md)
- [references/presets.md](references/presets.md)
- [references/quick-mode.md](references/quick-mode.md)
- [references/ralph-loop-contract.md](references/ralph-loop-contract.md)
- [references/agent-prompts.md](references/agent-prompts.md)
- [references/cli-spawning.md](references/cli-spawning.md)
- [references/debate-protocol.md](references/debate-protocol.md)
- [references/explorers.md](references/explorers.md)
- [references/finding-extraction.md](references/finding-extraction.md)
- [references/output-format.md](references/output-format.md)
- [references/personas.md](references/personas.md)
- [references/caching-guidance.md](references/caching-guidance.md)
- [references/reviewer-config-example.md](references/reviewer-config-example.md)
- [references/strategic-doc-validation.md](references/strategic-doc-validation.md)
- [references/evidence-mode.md](references/evidence-mode.md)
- [../shared/references/backend-background-tasks.md](../shared/references/backend-background-tasks.md)
- [../shared/references/backend-claude-teams.md](../shared/references/backend-claude-teams.md)
- [../shared/references/backend-codex-subagents.md](../shared/references/backend-codex-subagents.md)
- [../shared/references/backend-inline.md](../shared/references/backend-inline.md)
- [../shared/references/claude-code-latest-features.md](../shared/references/claude-code-latest-features.md)
- [../shared/references/ralph-loop-contract.md](../shared/references/ralph-loop-contract.md)
