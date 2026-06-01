---
name: agent-native
description: Make an out-of-session Claude (Managed Agent or Agent SDK loop) AgentOps-native — via skills + the ao CLI + CI, not hooks.
skill_api_version: 1
practices:
- continuous-delivery
- ddd
hexagonal_role: supporting
consumes:
- standards
- converter
- validation
produces:
- docs/contracts/agent-runtime-profile.md
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: meta
  dependencies: [standards, converter]
  stability: experimental
output_contract: "An AgentOps-native Agent definition (skills + ao tool surface) graded by the same CI gate as interactive work"
---

# /agent-native — Make Out-of-Session Agents AgentOps-Native (Hookless)

Run a Claude loop *outside* an interactive Claude Code / Codex session — an Anthropic **Managed Agent**, an **Agent SDK** loop, or a self-hosted sandbox job — and keep it under the same AgentOps guardrails. The old reflex ("port the ~50 marketplace hooks into the new runtime") is **wrong for AgentOps 3.0**. This skill is the hookless reframe.

## Overview

**AgentOps 3.0 is hookless.** Guardrails come from three things, never hooks:

1. **Skills** — `skills/<name>/SKILL.md` progressive-disclosure contracts (standards, behavioral-discipline, council, validation, trace, provenance).
2. **The `ao` CLI** — the deterministic tool surface (`ao session bootstrap`, `ao inject`, `ao corpus inject --query`, `ao validate`, `ao goals measure`) plus the `standards` skill loaded into the agent's instructions.
3. **CI as the authoritative gate** — `.github/workflows/validate.yml` runs the standards/scenario checks as CI jobs, NOT as a PreToolUse hook.

So an out-of-session agent becomes AgentOps-native by: **(a)** loading AgentOps skills into the Agent definition, **(b)** exposing the `ao` CLI as a callable tool (MCP or shell-tool) so the agent can `ao session bootstrap` / `ao inject` / `ao validate` itself, and **(c)** running the same CI-style validation gate on its outputs before the work is accepted. The Agent SDK's own hooks become an **optional thin adapter** for teams wanting in-loop interception — never the primary mechanism.

> **Mechanism status (planned, not yet shipped).** This skill is the **doctrine layer** and lands first; the two concrete commands it names — `ao agent bundle` (ag-jspr) and `ao mcp serve` (ag-higd) — are open, ready beads under epic ag-7s9fo, not yet in the live CLI. The `ao session bootstrap` / `ao inject` / `ao corpus inject` / `ao validate` / `ao goals measure` commands the bundled agent calls are real today. When ag-jspr and ag-higd land, remove this skill's entry from `scripts/skill-body-refs-allowlist.txt`.

This is an **extension of two existing skills**, not a rewrite:
- [standards](../standards/SKILL.md) — gains an Agent-runtime profile: how the standards/behavioral-discipline checklists get loaded by a non-interactive Claude and enforced via CI rather than `/vibe`.
- [converter](../converter/SKILL.md) + the `skills/` ↔ `skills-codex/` parity machinery — reused as-is to keep the bundle dual-runtime.

## ⚠️ Critical Constraints

- **This is a reframe of the retired "port hooks" idea, NOT a hook revival.** **Why:** hooks are runtime-coupled and fork the guardrail surface; skills + `ao` + CI are the portable 3.0 waist that works in any runtime.
- **Single source of truth — no skill fork.** The cloud/SDK agent loads the *same* `skills/` files an interactive session uses. **Why:** a forked guardrail set drifts and defeats the corpus moat.
- **Managed Agents are NOT ZDR.** Never bundle holdout `target`/`ground_truth`/PII into an Agent definition or its MCP tool responses. **Why:** anything sent to the cloud agent leaves the boundary permanently. For holdout-touching work see [eval-outcomes](../eval-outcomes/SKILL.md).
- **CI is the gate, not the adapter.** The optional SDK hook adapter is convenience, never the enforcement boundary. **Why:** a bypassed in-loop hook must not mean unvalidated work merges; CI is unconditional.

## Workflow

### Phase 1: Bundle skills into an Agent definition

```bash
ao agent bundle --runtime managed > agent-def.json
```

Stitches the selected AgentOps skills (default: `session-bootstrap`, `standards`, `behavioral-discipline`, `validation`, `provenance`) into a Managed Agents API payload — model + instructions + `skills` array + an MCP descriptor for the `ao` tool surface. POST-able with the `managed-agents-2026-04-01` beta header.

**Checkpoint:** the payload carries the skills + the `ao` MCP descriptor, and contains no holdout values.

### Phase 2: Expose `ao` as a tool

Run a thin MCP server (`ao mcp serve`) — or a documented shell-tool spec — exposing `session_bootstrap`, `inject`, `corpus_inject`, `validate`, `goals_measure` so the hosted loop can orient and self-check. For self-hosted sandboxes (bushido), the MCP server runs **inside** the sandbox boundary with tailnet access to Dolt.

**Checkpoint:** the agent can call `ao session bootstrap` + `ao inject` itself before doing work.

### Phase 3: Gate the output via CI

A reusable workflow (`agent-output-validate.yml`) runs `ao validate` + the standards/scenario gates against whatever the agent produced (PR branch or artifact bundle) — the **same** authoritative gate as interactive work. Green CI is the merge gate.

**Checkpoint:** the agent's output passed the identical CI gate; nothing merges red.

### Optional: SDK hook adapter

For Agent SDK users who *want* in-loop interception, a documented `PreToolUse`/`Stop` adapter shells out to `ao validate` (with the `standards` checklist loaded). **Clearly optional — the default path is CI, never hooks.** Reference samples (TypeScript + Python, wired into no runtime by default): [references/sdk-hook-adapter.md](references/sdk-hook-adapter.md).

## Output Specification

**Format:** a JSON Agent definition plus a validated PR/artifact. **Path:** the Agent definition is written to `agent-def.json` at the repo root; the runtime profile is written to `docs/contracts/agent-runtime-profile.md` (the frontmatter `produces` path). **Structure:** model, instructions (stitched skills), `skills` array, `ao` MCP descriptor; the output is accepted only on a green CI run.

## Quality Rubric

- [ ] Agent definition loads the *same* `skills/` files as interactive sessions (no fork).
- [ ] `ao` is callable by the agent (MCP/shell-tool); it can self-bootstrap + self-validate.
- [ ] Outputs pass the same CI gate as interactive work (CI is the boundary, not a hook).
- [ ] No holdout `target`/`ground_truth`/PII in the Agent definition or tool responses.

## Examples

```bash
# Bundle, serve the ao tool surface, and let CI gate the output
ao agent bundle --runtime managed > agent-def.json
ao mcp serve &   # exposes session_bootstrap/inject/validate/goals_measure as MCP tools
# (submit agent-def.json to the Managed Agents API; its PR is gated by agent-output-validate.yml)
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Tempted to port the hooks | Old runtime-coupled reflex | Don't — bundle skills + expose `ao` + gate via CI. Hooks are the optional adapter only |
| Agent can't orient | `ao` not exposed as a tool | Run `ao mcp serve` (or the shell-tool spec) so the loop can `ao session bootstrap` |
| Unvalidated work merged | Relied on the optional in-loop adapter | CI (`agent-output-validate.yml`) is the gate — never the adapter |

## See Also

- [standards](../standards/SKILL.md) — the checklists the agent loads + CI enforces
- [converter](../converter/SKILL.md) — keeps the bundle dual-runtime (skills ↔ skills-codex)
- [eval-outcomes](../eval-outcomes/SKILL.md) — holdout-safe grading for cloud/out-of-session agents
- [using-gc](../using-gc/SKILL.md) — running a whole out-of-session loop (gc owns orchestration; `ao agent bundle` produces the definition)
- [skill-auditor](../skill-auditor/SKILL.md) — audit this skill before declaring stable
