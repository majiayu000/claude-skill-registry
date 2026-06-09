---
name: codex-exec
description: |-
  Use when running Codex workers or validators non-interactively through codex exec with evidence.
  Triggers:
skill_api_version: 1
user-invocable: false
hexagonal_role: driving-adapter
practices:
- pragmatic-programmer
- continuous-delivery
consumes: []
produces:
- codex-run-output
context_rel:
- kind: supplier-to
  with: codex-sandbox-evidence
context:
  window: inherit
  intent:
    mode: none
  sections:
    exclude:
    - HISTORY
  intel_scope: none
metadata:
  tier: orchestration
  dependencies:
  - ntm
  - caam
  stability: stable
  triggers:
  - codex exec
  - spawn a codex worker
  - run codex non-interactively
  - codex validator
  - headless codex
  - codex resume
  - drive codex from a script
  - factory worker on Codex
output_contract: Runs codex exec on the OAuth/Pro sub; final agent message to stdout (or --output-last-message FILE / --json JSONL).
---

# codex-exec

Drive headless Codex worker and validator agents with `codex exec` on the ChatGPT Pro subscription (OAuth) — the Codex side of the flywheel. The one inviolable rule: **subscription billing, never per-token API billing.**

## ⚠️ Critical Constraints

- **Never API-bill a worker.** Do NOT set `OPENAI_API_KEY` in a worker's env, and do NOT use `codex login --with-api-key`. **Why:** that flips Codex from flat-rate sub billing to per-token API billing — the Codex twin of the banned `claude -p`. A factory cycle on API keys silently burns real money. (Mirror of the "never `claude -p` for workers" rule.)
  - WRONG: `OPENAI_API_KEY=sk-... codex exec -C "$REPO" "<task>"`
  - CORRECT: `codex login status  # Logged in using ChatGPT` then `codex exec -C "$REPO" -s workspace-write "<task>"`
- **Confirm the sub before dispatch.** Run `codex login status` and require `Logged in using ChatGPT`. **Why:** a worker that "runs fine" on a leaked API token bills per token; the check is the only thing standing between a green run and a surprise invoice.
- **Pick the sandbox deliberately.** `-s read-only` for validators, `-s workspace-write` for workers that must edit, `-s danger-full-access` only inside an already-sandboxed host. **Why:** `codex exec` runs model-generated shell commands; the sandbox is the blast radius.
- **`--dangerously-bypass-approvals-and-sandbox` is for externally-sandboxed hosts only.** **Why:** it removes every guardrail in one flag; use it only when the OS/container is the sandbox.
- **Don't strand work in `--ephemeral`.** It skips session persistence, so there is nothing to `resume`. **Why:** a crashed ephemeral run cannot be recovered or continued.
- **Multi-account lanes go through `caam`, not env-var juggling.** **Why:** `caam exec codex <profile> --` keeps each Pro lane isolated; hand-setting `CODEX_HOME` invites cross-account token bleed.

## Why This Exists

`codex exec` runs Codex non-interactively: it takes a prompt (argument or stdin), executes against a working directory under a sandbox policy, and prints the final agent message. It is the Codex analogue of an NTM Claude pane — the right tool for factory/loop workers and validators that need a second vendor lane.

Auth is the whole game. `codex login status` must read **`Logged in using ChatGPT`** (the Pro/Plus subscription via OAuth). That billing is flat-rate. The moment Codex is authed with an API key (`OPENAI_API_KEY`, `codex login --with-api-key`), every token is metered against the API account — the exact failure mode `claude -p` causes on the Claude side. This skill exists to keep Codex workers on the sub. Without it, a loop that dispatches Codex turns can quietly run on metered API billing and produce a surprise invoice.

Verified against `codex-cli 0.137.0` (`codex exec --help`, `codex exec resume --help`).

## Quick Start

```bash
codex login status                      # MUST read: Logged in using ChatGPT
test -z "${OPENAI_API_KEY:-}" || echo "ABORT: API key set"   # MUST be empty
codex exec -C "$REPO" -s read-only "Validate the change. Output VERDICT: PASS|FAIL."
```

## Workflow / Methodology

### Phase 1: Verify the lane is on the subscription
```bash
codex login status          # MUST print: Logged in using ChatGPT
echo "${OPENAI_API_KEY:+API_KEY_SET}"   # MUST print nothing
```
**Checkpoint:** Status reads `Logged in using ChatGPT` AND no `OPENAI_API_KEY` is set. If either fails, STOP — fix auth before dispatching. If API-key auth is present, run `codex login` (browser OAuth) or `--device-auth` to re-auth on the sub.

### Phase 2: Dispatch the worker / validator
```bash
# Worker: edit in a repo
codex exec -C /path/to/repo -s workspace-write \
  "Implement bead ag-123: <task>. Run tests. Report PASS/FAIL."

# Validator: read-only, structured verdict
codex exec -C /path/to/repo -s read-only \
  -o /tmp/verdict.txt \
  "Independently validate the change on this branch. Output VERDICT: PASS|FAIL + reasons."

# Stdin prompt (orchestrator piping the task in)
printf '%s' "$TASK_PROMPT" | codex exec -C "$REPO" -s workspace-write -

# Named profile (a specific model/config lane)
codex exec -p worker-fast -C "$REPO" -s workspace-write "<task>"

# Machine-readable event stream for a loop to parse
codex exec --json -C "$REPO" -s read-only "<task>" > events.jsonl
```
Key flags: `-C/--cd <DIR>` working root · `-s/--sandbox <read-only|workspace-write|danger-full-access>` · `-p/--profile <name>` layers `$CODEX_HOME/<name>.config.toml` · `-m/--model` · `-o/--output-last-message FILE` · `--json` JSONL events · `--output-schema FILE` constrains final-response shape · `--add-dir` extra writable dir · `--skip-git-repo-check` for non-repo dirs · `--ephemeral` no persistence.
**Checkpoint:** Worker exited 0; the final message (stdout / `-o` file / last JSONL `item`) carries the expected verdict or artifact.

### Phase 3: Resume to continue a session
```bash
cd "$REPO" && codex exec resume --last "Address the validator's findings, then re-run tests."
codex exec resume <SESSION_ID> "<follow-up>"
codex exec resume --last --json "<follow-up>" > events2.jsonl
```
`resume` takes a UUID session id or thread name; `--last` picks the newest in the cwd; `--all` disables cwd filtering. **Currency note (codex-cli 0.137.0):** `resume` accepts `-m/--model`, `-o/--output-last-message`, `--json`, `--output-schema`, `--ephemeral`, `-i/--image`, `--skip-git-repo-check` — but **NOT** `-C/--cd` and **NOT** `-s/--sandbox`. The resumed session inherits its original working root and sandbox policy, so `cd` into the repo first (the resume picks the newest session in the cwd) rather than passing `-C`/`-s`.
**Checkpoint:** The resumed session id matches the intended thread and the follow-up landed in the same working tree.

## Output Specification

**Format:** plain text (final agent message) by default; JSONL with `--json`; raw last message to a file with `-o/--output-last-message`.
**Filename:** caller-chosen via `-o <FILE>` (e.g. `/tmp/codex-verdict.txt`) or redirected JSONL (`events.jsonl`). No fixed convention — the orchestrator names it.
**Structure:** non-`--json` = the agent's final message to stdout. `--json` = one JSON event per line (item/agent/tool events); parse the terminal agent message item for the result. `--output-schema FILE` forces the final response to conform to a supplied JSON Schema (use for machine-checkable verdicts).

## Exit Codes

A loop should branch on the process exit code, not on scraped text.

| Code | Meaning | Loop action |
|------|---------|-------------|
| `0` | Run completed; final message emitted | Parse the result (`-o FILE` / last `--json` item); proceed |
| non-zero | Codex error — auth failure, sandbox denial, bad flag, or model/tool error | Do NOT treat as a verdict; re-check `codex login status`, sandbox mode, and flags, then retry or escalate |

## Quality Rubric

- [ ] `codex login status` showed `Logged in using ChatGPT` BEFORE dispatch
- [ ] No `OPENAI_API_KEY` in the worker env and no `--with-api-key` anywhere
- [ ] Sandbox mode matches role (read-only validator / workspace-write worker)
- [ ] Working root set explicitly with `-C`, not assumed from cwd
- [ ] Result captured deterministically (`-o FILE`, `--json`, or `--output-schema`) — not scraped from terminal noise
- [ ] Long/multi-turn work uses `resume` (not `--ephemeral`) so it can be recovered
- [ ] Multi-account lanes dispatched via `caam exec codex <profile> --`

## Examples

```bash
# Factory validator lane (read-only, schema-constrained verdict)
codex exec -C "$REPO" -s read-only \
  --output-schema /tmp/verdict.schema.json \
  -o /tmp/verdict.json \
  "Validate bead $BEAD independently. Emit {verdict, reasons}."

# caam-isolated Pro lane, then continue it
caam exec codex pro-2 -- exec -C "$REPO" -s workspace-write "Start ag-77."
cd "$REPO" && codex exec resume --last "Fix the failing test from the prior turn."
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Tokens billing to API account | API-key auth or `OPENAI_API_KEY` set | `unset OPENAI_API_KEY`; `codex login` (OAuth) or `--device-auth`; re-check `codex login status` |
| `Logged in with API key` in status | Wrong auth path | Re-auth on the sub via browser OAuth / `--device-auth`; never `--with-api-key` for workers |
| `not a git repository` error | `-C` points outside a repo | Add `--skip-git-repo-check` (or point `-C` at a repo) |
| Worker can't write files | `-s read-only` | Use `-s workspace-write`; add `--add-dir` for paths outside the root |
| `resume` finds nothing | Prior run used `--ephemeral`, or wrong cwd | Don't use `--ephemeral` for resumable work; try `resume --all` to drop cwd filtering |
| Empty / truncated output in a loop | Parsing terminal text | Use `-o FILE` or `--json` and read the structured result |
| Rate-limited on the Pro lane | One account saturated | Switch lanes with `caam exec codex <other-profile> --` |

## See Also / References

- `ntm` — Claude worker panes (the Claude-side lane; never `claude -p`)
- `caam` — isolated multi-account profiles for the 4-lane flywheel (Claude Max ×2 + Codex Pro + Gemini)
- `dcg` — destructive-command guard that can enforce the never-API-bill rule
- Memory: "Never claude -p for workers 2026-06-06" — the Claude-side twin of this skill's core rule
