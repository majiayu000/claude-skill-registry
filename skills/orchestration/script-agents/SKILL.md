---
name: script-agents
description: Build and maintain minimal, role-aware prompt-dispatch scripts for coding agents. Use when: (1) creating one-shot report/review scripts, (2) wiring deterministic context artifacts into an LLM dispatch step, (3) standardizing configurable harness dispatch contracts (`AGENT_DISPATCH_DIR` + `AGENT_DISPATCH_CMD`) without scope bloat.
category: meta
user-invocable: true
---

# Script Agents

Design and maintain small, high-signal scripts where deterministic local orchestration feeds a configurable coding-agent harness for one-shot analysis.

## Standard (2026-02)

For every new or updated script-agent script:

1. **CLI ergonomics**
- Support `--no-dispatch` for deterministic local execution.
- Support `--debug` when artifact inspection is useful.
- Keep defaults zero-config for this machine, but all runtime integrations overrideable via env vars.

2. **Dispatch contract**
- Use exactly these knobs for model dispatch:
  - `AGENT_DISPATCH_DIR`
  - `AGENT_DISPATCH_CMD`
- Parse dispatch command safely for shell array execution:
  - `typeset -a DISPATCH_CMD_ARR`
  - `DISPATCH_CMD_ARR=(${(z)AGENT_DISPATCH_CMD})`

3. **Artifact contract**
- Write timestamped artifacts to a predictable project-owned directory.
- Write/update a stable `latest-*` pointer when repeated runs are expected.
- In `--no-dispatch`, still emit a useful local report artifact (do not no-op).

4. **Validation contract**
- Fail fast on missing inputs and empty outputs.
- Validate required headings/fields for machine-readability.
- Include a cheap smoke path that can run without networked model calls.

5. **Prompt contract**
- Keep static instructions at top and variable context at bottom.
- Favor XML/section-tagged blocks for deterministic parsing.
- Prefer schema-constrained outputs for structured sections where possible.

## Core Pattern (Fresh-Eyes + RR Prompt A)

Use this exact sequence:

1. **Goal sentence**
- State the project goal in one sentence.

2. **Input contract**
- List exact files/directories consumed.
- Prefer one JSON context artifact.

3. **Output contract**
- Define exact output files and section requirements.
- Keep outputs self-contained and machine-readable where possible.

4. **Scope trim (RR A discipline)**
- Keep only what is needed for the current milestone.
- Defer speculative integrations and abstraction layers.

5. **Dispatch contract**
- Use two knobs only:
  - `AGENT_DISPATCH_DIR`
  - `AGENT_DISPATCH_CMD`
- Provide a sensible project default, but keep it overrideable.
- Allow override to any compatible pi harness command.

6. **Validation**
- Verify script can run with and without dispatch (`--no-dispatch` style path when useful).
- Verify artifacts are non-empty and linked via a `latest-*` pointer when applicable.

## Hard Rules

- Keep scripts close to the owning project (for example `scripts/`).
- Keep prompts and context artifacts in predictable artifact paths.
- Avoid role-specific hardcoding in code when a profile file already contains source-of-truth data.
- Prefer deterministic generation steps before LLM dispatch.
- Do not introduce a framework; use shell + small embedded Python/Node only where required.
- Follow the `dogfood` skill (`/Users/amar/agi/skills/dogfood/SKILL.md`).
- Do not work around broken script UX with manual path gymnastics or direct replacement commands.
- If a script is awkward or fails in normal usage, fix the script and re-run it.

## SOTA Guardrails

Apply these defaults unless the project has a hard reason not to:

1. **Schema-first outputs**
- Prefer Structured Outputs / strict tool schemas over free-form JSON.
- Avoid plain "JSON mode" when schema adherence is needed.

2. **Explicit tool control**
- Use `tool_choice` deliberately (`auto`, `required`/`any`, or forced tool) per step intent.
- Keep tool surface minimal and role-specific.

3. **Cache-friendly prompt layout**
- Put reusable static content first, dynamic context last, so prompt caching works predictably.

4. **Eval + trace loop**
- Add lightweight regression checks for output shape/sections.
- Add periodic trace/eval review for agentic steps, not just final output snapshots.

5. **Injection resistance**
- Treat external text as untrusted.
- Extract validated fields before allowing downstream tool-driving behavior.

## Minimal Script Skeleton

```zsh
#!/usr/bin/env zsh
set -euo pipefail

AGENT_DISPATCH_DIR="${AGENT_DISPATCH_DIR:-/Users/amar/agi/claudette}"
AGENT_DISPATCH_CMD="${AGENT_DISPATCH_CMD:-node --import tsx bin/claudette.ts --profile scope --provider codex --no-session}"

typeset -a DISPATCH_CMD_ARR
DISPATCH_CMD_ARR=(${(z)AGENT_DISPATCH_CMD})

# 1) Build deterministic context JSON
# 2) Assemble prompt
# 3) Optional no-dispatch path
# 4) Dispatch
(
  cd "$AGENT_DISPATCH_DIR" && \
  CLAUDETTE_SKIP_FORCED_EVAL=1 "${DISPATCH_CMD_ARR[@]}" -p "$(cat "$PROMPT_FILE")"
) > "$REPORT_FILE"
```

## Reusable Outputs

1. `context-<ts>.json` (deterministic input snapshot)
2. `prompt-<ts>.md` (exact prompt sent to harness)
3. `report-<ts>.md` (dispatch output)
4. `latest-*` pointers where continuous refresh is useful

## Example Mapping (Clunkers + Claudette)

- `clunkers/scripts/*` as orchestration owner
- `AGENT_DISPATCH_DIR=/Users/amar/agi/claudette`
- `AGENT_DISPATCH_CMD="node --import tsx bin/claudette.ts --profile scope --provider codex --no-session"`

Treat this as an example instantiation, not a required stack.

## Sources (SOTA References)

As of 2026-02-17:

- OpenAI Structured Outputs: https://developers.openai.com/api/docs/guides/structured-outputs
- OpenAI Function Calling (`tool_choice`, strict schemas): https://developers.openai.com/api/docs/guides/function-calling
- OpenAI Safety in building agents: https://developers.openai.com/api/docs/guides/agent-builder-safety
- OpenAI Trace grading: https://developers.openai.com/api/docs/guides/trace-grading
- OpenAI Evaluation best practices: https://developers.openai.com/api/docs/guides/evaluation-best-practices
- Anthropic prompt caching: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic tool use implementation (`tool_choice`, strict tools): https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use
- Anthropic prompt structuring (XML tags): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
- MCP spec (official repo): https://github.com/modelcontextprotocol/modelcontextprotocol
- Google A2A protocol overview: https://a2a.cx/
