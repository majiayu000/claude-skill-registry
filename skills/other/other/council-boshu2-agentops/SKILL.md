---
name: council
description: Run multi-judge consensus.
practices:
- llm-eval-harness
- ai-assisted-dev
- design-by-contract
hexagonal_role: domain
consumes:
- standards
produces:
- result.json
- verdict.json
context_rel:
- kind: shared-kernel
  with: standards
skill_api_version: 1
context:
  window: isolated
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: full
metadata:
  tier: judgment
  dependencies:
  - standards
  replaces: judge
output_contract: skills/council/schemas/verdict.json
---
# /council — Multi-Model Consensus Council

Convene N independent reasoners over a shared briefing and return one synthesis. `--mode` selects the deliberation pattern — `brainstorm`, `debate`, or `verdict`. Everything else (`--focus`, `--depth`, `--runtime`, `--roster`) is an orthogonal knob.

## Loop position

Cross-cutting judgment gate available at any [operating loop](../../docs/architecture/operating-loop.md) move where multi-model consensus is required: typically pre-flight on the slice plan (between moves 3 and 4), per-slice on non-mechanical correctness (move 6), and on the bead acceptance roll-up. Council does not own a loop move — it provides verdicts that other moves consume. Use it at slice level when a single test cannot capture taste; use it at bead level when acceptance examples are passing but the consumer-facing behavior still needs adversarial review.

## Quick Start

```bash
/council validate this plan                                    # verdict mode (the default)
/council --mode=brainstorm caching approaches                  # brainstorm mode
/council --mode=debate should we adopt event sourcing?         # debate mode (named personas duel)
/council --depth=quick validate recent                         # fast inline check
/council --mode=brainstorm --focus=research k8s upgrade paths   # research = focused brainstorm
/council --roster=security-audit validate the auth system      # preset persona roster
/council --depth=deep --runtime=mixed --roster=leadership-quartet validate product thesis
/council --adversarial validate the auth system                # verdict over 2 adversarial rounds
/council                                                       # infers mode from context
```

Council works independently — no RPI workflow, no ratchet chain, no `ao` CLI required.

## Modes — the deliberation taxonomy

`--mode` selects one of exactly three deliberation patterns; `verdict` is the default. The taxonomy is frozen as an executable spec — [references/council-modes.feature](references/council-modes.feature).

| `--mode` | Pattern | Synthesis |
|----------|---------|-----------|
| `brainstorm` | **diverge** — agents generate options independently before any cross-talk | ranked set of ideas, perspectives, risks (no PASS/WARN/FAIL) |
| `debate` | **contend** — independent positions → adversarial 0–1000 cross-scoring → reveal round | ranked decision with recorded dissent |
| `verdict` *(default)* | **converge** — agents judge the artifact against the bar independently | one PASS / WARN / FAIL with consolidated findings |

`verdict` runs when `--mode` is omitted. `validate` is a verdict alias; `research` folds into `brainstorm` (`--focus=research`). When `--mode` is omitted council infers it from natural language — trigger words in [references/task-type-rigor-gate.md](references/task-type-rigor-gate.md).

**Mode and focus are orthogonal.** `--mode` is the deliberation *pattern*; `--focus` is the *subject*. `--depth`, `--runtime`, and `--roster` are knobs, never modes. **Every mode runs the same lifecycle** — convene → brief → deliberate → synthesize → record — and `deliberate` always isolates each agent before any cross-talk. Full taxonomy, knob aliases (`--quick`/`--deep`/`--mixed`), and the lifecycle contract: [references/modes.md](references/modes.md).

### Spawn backend (MANDATORY)

Council requires a runtime that can **spawn parallel subagents** and (for `debate` and `--adversarial`) **send messages between agents**. If no multi-agent capability is detected, fall back to `--depth=quick` (inline single-agent). Skills describe WHAT to do, not WHICH tool — see `skills/shared/SKILL.md` for the capability contract. Backend-specific spawn/wait/message/cleanup examples:

- Claude Native Teams → `references/backend-claude-teams.md` · Codex Sub-Agents / CLI → `references/backend-codex-subagents.md`
- Background Tasks → `references/backend-background-tasks.md` · Inline → `references/backend-inline.md`
- Shared Claude feature contract → `skills/shared/references/claude-code-latest-features.md` (local mirror: `references/claude-code-latest-features.md`)

See `references/cli-spawning.md` for the council-specific spawning flow (phases, timeouts, output collection).

## Debate mode (`--mode=debate`)

`--mode=debate` convenes 2–4 named domain-expert personas who duel: each writes an independent verdict in character, every persona adversarially cross-scores every rival 0–1000, then a **mandatory reveal round** forces concessions and surfaces blind spots. Synthesis is a score matrix → a ranked decision with dissent kept verbatim. `dueling-idea-wizards` maps to `--mode=debate --focus=ideas`; `/expert-council` routes here.

Constraints: personas decide and the orchestrator only counts; the briefing goes on disk, never through argv; the reveal is never skipped. Per-phase persona-slate / duel / reveal / score-matrix templates: [references/dueling-route.md](references/dueling-route.md).

## Adversarial round (`--adversarial`) — a verdict intensifier

`--adversarial` is a **verdict-mode** flag, not the debate mode. It runs `verdict` over two rounds — R1 independent verdicts, R2 steel-manning revision via backend messaging — for high-stakes verdicts where judges are likely to disagree (security audits, architecture decisions, migration plans). Skip it for routine validation where consensus is expected. Full protocol: [references/adversarial-protocol.md](references/adversarial-protocol.md).

**Incompatibilities:**
- `--depth=quick` and `--adversarial` cannot be combined. If both are passed, exit with error: "Error: --quick and --adversarial are incompatible."
- `--adversarial` only applies to verdict mode. Combined with `--mode=brainstorm` or `--mode=debate`, exit with error: "Error: --adversarial is only supported with verdict mode."

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

**Mixed-mode perspective assignment:** Under `--mixed`, the perspective list is built once and each perspective is assigned to one Claude judge **and** one Codex judge with identical prompt and packet. This produces head-to-head pairs (perspective × vendor) so verdict differences isolate the vendor variable. Without `--preset` or `--perspectives`, both vendors run 3 generic judges each (6 total). With a 4-perspective preset like `security-audit`, `plan-review`, or `leadership-quartet`, both vendors run those 4 perspectives (8 total). Do not split perspectives across vendors — symmetric pairing is the whole point of `--mixed`.

---

## Named Perspectives & Consensus

See [references/consensus-and-output.md](references/consensus-and-output.md) for named-perspective usage (`--perspectives`, `--perspectives-file`, YAML format, flag priority), consensus verdict rules (PASS/WARN/FAIL combination table, DISAGREE resolution), and the finding-extraction flywheel protocol. See [references/personas.md](references/personas.md) for built-in presets.

---

## Explorer Sub-Agents

> **Explorer Details:** Use `Read` tool on `skills/council/references/explorers.md` for explorer architecture, prompts, sub-question generation, and timeout configuration.

**Summary:** Judges can spawn explorer sub-agents (`--explorers=N`, max 5) for parallel deep-dive research. Total agents = `judges * (1 + explorers)`, capped at MAX_AGENTS=12.

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

See [references/flags-reference.md](references/flags-reference.md) for the full flag and environment variable reference (`COUNCIL_TIMEOUT`, `COUNCIL_CODEX_MODEL`, `--deep`, `--mixed`, `--adversarial`, `--evidence`, `--commit-ready`, `--preset`, `--profile`, and all other flags).

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
- `skills/research/SKILL.md` — Codebase exploration (complementary to `--mode=brainstorm --focus=research`)

## Reference Documents

- [references/modes.md](references/modes.md)
- [references/council-modes.feature](references/council-modes.feature)
- [references/dueling-route.md](references/dueling-route.md)
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
- [references/adversarial-protocol.md](references/adversarial-protocol.md)
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
