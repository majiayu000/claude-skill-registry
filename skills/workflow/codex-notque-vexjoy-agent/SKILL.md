---
name: codex
description: "Run bulk/mechanical work on gpt-5.5 via the Codex CLI."
user-invocable: false
compatibility: "Requires codex CLI on PATH (verified codex-cli 0.142.5); ~/.codex/config.toml supplies the model (gpt-5.5) and reasoning-effort defaults"
routing:
  force_route: true
  triggers:
    - through codex
    - codex exec
    - dispatch to codex
    - run on codex
    - codex analysis
    - gpt-5.5
  pairs_with:
    - data-analysis
    - pr-workflow
  complexity: Medium
  category: meta
---

# Codex — the gpt-5.5 Execution Lane

Run a task on gpt-5.5 through the Codex CLI (`codex exec`) and return the result. This is the general-purpose lane for work the model-selection policy sends to gpt-5.5, and the **canonical owner of general `codex exec` mechanics** — when the CLI changes, update here first. gpt-5.5 is reachable only through this CLI; the Agent tool's `model` parameter covers Claude models only.

Two flows keep their own specialized codex integration — route to them instead of re-implementing here:

| Existing flow | Owns | Where |
|---|---|---|
| PR / code review via codex | `codex exec review`, finding triage, report synthesis | `skills/process/pr-workflow/references/codex-review.md` |
| Sprite/image generation backend | codex image backend selection and invocation | `skills/game/game-sprite-pipeline/references/backend-chain.md` |

## Phase 1: DECIDE — does this task belong on gpt-5.5?

Policy mirror — canonical copy: `/do` SKILL.md, Model Selection (edit there first, then here). Rankings, higher = better; cost = what the owner actually pays.

| model | cost | intelligence | taste | role |
|---|---|---|---|---|
| gpt-5.5 | 9 | 8 | 5 | Bulk/mechanical via codex. Dispatch target. |
| sonnet-5 | 5 | 5 | 7 | Mechanical/reader fan-out, lighter work. Dispatch target. |
| opus-4.8 | 4 | 7 | 8 | Reviews, audits, analysis, deep work. Dispatch target. |
| fable-5 | 2 | 9 | 9 | Highest technical requirements only — never routine dispatch. |

Route here when the task is **bulk/mechanical**: clear-spec implementation, data analysis, migrations, extraction/inventory sweeps — gpt-5.5 is effectively free. Route elsewhere when the task is user-facing (UI, copy, API design — needs taste ≥ 7: sonnet/opus) or is a plan/implementation review (opus-4.8 lead; gpt-5.5 optionally adds an extra independent perspective via pr-workflow's codex-review). Consult the canonical model-selection table in `/do` SKILL.md.

These are defaults, not limits. Standing permission to escalate: when gpt-5.5's output misses the bar, rerun on a smarter model without asking — judge the output, not the price tag; escalating costs less than shipping mediocre work. For anything that ships, intelligence > taste > cost; cost is a tie-breaker only.

**Gate**: task classified bulk/mechanical (or investigation — Phase 4 sandbox rule). Otherwise route to the policy's Claude pick and stop here.

## Phase 2: WRAP — how gpt-5.5 runs from this harness

**Wrapper symmetry**: the wrapper is needed for whichever model family is NOT the current harness.

- **Under Claude Code** (current default): gpt-5.5 runs through a wrapper — either the dispatched agent runs `codex exec` via Bash with a self-contained prompt, or a thin Claude wrapper agent (`model: "sonnet"`, low effort) writes the self-contained codex prompt, runs it, and returns the result.
- **Under the Codex harness**: Claude models require the wrapper instead.
- Claude models under Claude Code need no wrapper — just the Agent/Workflow `model` parameter.

Pick the direct-Bash form when the calling agent already holds the task context; pick the thin wrapper agent for fan-out (one wrapper per data source) so the orchestrator stays lean.

**Availability check first**: `command -v codex` — when absent, fall back to the policy's Claude pick (`model: "sonnet"` for mechanical work) and tell the user in one line which lane ran.

## Phase 3: PROMPT — write a self-contained prompt

Codex runs in its own process with no conversation history. The prompt must carry everything:

1. **Context** — one short paragraph: what the repo/data is, what state matters.
2. **Task** — the concrete operation, with file paths relative to the working directory. Let codex read files itself; embedding large content wastes tokens and loses formatting.
3. **Output format** — the exact structure to return (table, JSON, diff), so the wrapper can consume it without a second pass.

**Prompt hygiene (hard rule)**: codex prompts leave the machine. Send only public content — secrets, credentials, and private component names (anything sourced from `INDEX.local.json` or other local-only inventories) stay out. Run the deterministic scan on the prompt text before executing:

```bash
printf '%s' "$PROMPT" | rg -n "Bearer|Authorization|token|secret|api[_-]?key|password|PRIVATE KEY" && echo "HYGIENE VIOLATION"
```

On a hit or a private component name: scrub the flagged content when the task survives without it; otherwise reroute the task to a Claude model. A bare refusal is not an outcome.

## Phase 4: RUN

Model and reasoning effort come from `~/.codex/config.toml` (gpt-5.5, high) — pass `-m`/`-c` overrides only when the task needs them.

**Investigation / data analysis (default for anything that only reads):**

```bash
TMPFILE=$(mktemp)
codex exec -s read-only --skip-git-repo-check -o "$TMPFILE" "$(cat <<'PROMPT'
[self-contained prompt]
PROMPT
)"
cat "$TMPFILE"
```

`-s read-only` sandboxes the run to reads — verified working on this host. Use it for every investigation or analysis prompt not covered by an existing codex flow, because a read-only task never needs write access and the sandbox makes that deterministic.

**Write tasks (clear-spec implementation, migrations):** drop `-s read-only`; run from the target repo's working directory; review the diff (`git status --short`, `git diff`) before committing anything.

**Reviews:** use `codex exec review` via the pr-workflow codex-review flow (table above), not a hand-rolled prompt.

**Gate**: exit code 0 AND output matches the requested format. Non-zero exit: report stderr and stop — codex failures are auth/API/prompt-length issues that a blind retry won't fix. Verify the output against a deterministic check where one exists (counts, file lists, test runs) before passing it upstream — gpt-5.5 output is evidence, not verdict. State the lane in the result ("ran on gpt-5.5 via codex") so the caller can apply the escalation rule.

## Error handling

### `codex: command not found`
Cause: Codex CLI not installed on this host.
Solution: fall back to the policy's Claude pick (`model: "sonnet"` for mechanical work) and report which lane ran; install via the owner's codex setup when authorized.

### Sandbox error mentioning bwrap / `Failed RTM_NEWADDR`
Cause: the bwrap sandbox fails in some containerized/VM environments.
Solution: for read-only work, retry without `-s read-only` only if the environment already provides external sandboxing (Claude Code does); `-s read-only` and `--dangerously-bypass-approvals-and-sandbox` are mutually exclusive — use one.

### Output missing or truncated in `-o` file
Cause: prompt exceeded length limits or codex wrote to stdout only.
Solution: shorten the prompt (point codex at files instead of embedding content); capture stdout as fallback.

## References

- `/do` SKILL.md, Model Selection — canonical policy table and routing decision rules
- `skills/process/pr-workflow/references/codex-review.md` — review-specific codex flow
- `skills/game/game-sprite-pipeline/references/backend-chain.md` — codex image backend
