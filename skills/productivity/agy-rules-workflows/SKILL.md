---
name: agy-rules-workflows
description: |-
  Install AGY rules, workflow, goal, and schedule controls for AgentOps loop law.
  Triggers: AGY rules, agy-loop, AGY schedule.
practices:
- design-by-contract
- continuous-delivery
hexagonal_role: driving-adapter
consumes:
- operating-loop-workflow
produces:
- agy-rules
- agy-workflows
context_rel:
- kind: conformist-to
  with: operating-loop-workflow
skill_api_version: 1
user-invocable: true
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: orchestration
  dependencies: [beads-br, operating-loop-workflow]
  stability: experimental
output_contract: |
  Materializes AGY-native artifacts: `.agents/rules/*.md` (invariant law),
  `.agents/workflows/agy-loop.md` (slash workflow), and an optional `hooks` block in
  `~/.gemini/settings.json`. Returns: paths written + the rules/workflow IDs.
---

# agy-rules-workflows

Land the flywheel's invariant **laws** and its **operating loop** as Google Antigravity (`agy`) native Rules and Workflows — so an AGY agent crank obeys the same membrane as the Claude and Codex turnouts, expressed in AGY's own primitives rather than ported wrappers.

## Overview / When to Use

The flywheel runs the same five laws on every harness; only the *skin* changes per vendor. On Claude that skin is `operating-loop-workflow` + `bead-crank` + hooks; on AGY it is **markdown Rules** (invariant law, always-active) + a **markdown slash Workflow** (the loop trajectory) + **`BeforeTool`/`AfterTool` hooks** (mechanical guardrails) + **dynamic subagents** (author!=judge). Use this skill when you are bootstrapping or repairing the AGY node and need those four surfaces to carry the laws below.

The `agy` CLI is real and headless-capable: `agy -p "<prompt>"` (or `--print`) runs one prompt non-interactively; `agy plugin {list,import,install,validate}` packages skills/rules/hooks/subagents; config lives under `~/.gemini/` (Antigravity's on-disk root — `settings.json` for hooks/permissions, `skills/` for skills, `antigravity-cli/{brain,knowledge}/` for durable memory). Project rules live in `.agents/rules/`; loop workflows in `.agents/workflows/` invoked as slash commands.

AGY also exposes two **native loop controls** the contract targets: the AGY goal command pins a durable objective the agent steers toward across turns (the loop's north-star — set it to the bead/epic intent), and the AGY schedule command registers a recurring tick so the loop self-cranks headless without an external cron. Express the trajectory as the `agy-loop` workflow, set the objective with the goal command, and drive the cadence with the schedule command — these three AGY-native primitives replace the gemini-cli wrappers the legacy lane used.

## ⚠️ Critical Constraints

These five are the **laws** — they MUST become always-active AGY Rules, not advisory prose:

- **Rule 1 — Author != Judge.** The agent that wrote a change MUST NOT be the one that closes its bead. Validation runs in a **clean-context AGY subagent** (or worktree-isolated agent). **Why:** a self-grading author reliably rationalizes its own work to PASS — the single biggest false-close vector.
- **Rule 2 — Evidence-gated close.** A bead closes only when each Given/When/Then maps to a captured proof surface (test output, diff, artifact). **Why:** "looks good" closes leave the loop carrying broken state; evidence is the only thing the next ephemeral agent can trust.
- **Rule 3 — No self-grade.** An agent never asserts its own verdict as authority. It reports; a separate judge decides; ties go to a tie-break subagent. **Why:** self-report is biased toward "done" — external verification beats self-report (the core flywheel axiom).
- **Rule 4 — Scoped commits.** Each commit touches only the bead's declared write scope; no drive-by edits outside the slice. **Why:** scope collisions are what make parallel agent waves unsafe; tight scopes are what let waves run at all.
- **Rule 5 — Persist before done.** A loop turn is not complete until evidence + learning are written to shared state (the bead, `.agents/ratchet/`, an AGY artifact). **Why:** an ephemeral agent's knowledge dies with its context unless it is published to the system.

Mechanical enforcement: encode Rules 1/3 as subagent-dispatch policy, Rules 2/5 as an `AfterTool` close-guard hook, and Rule 4 as a pre-commit scope check. Rules are the law; hooks are the immune system.

## Workflow / Methodology

### Phase 1: Verify the AGY surface
Confirm the harness before writing law into it.
```bash
command -v agy && agy plugin list
ls ~/.gemini/settings.json ~/.gemini/skills 2>/dev/null
```
**Checkpoint:** `agy` resolves and `~/.gemini/` exists. If not, stop — the AGY image is not installed; this skill has nothing to enforce against.

### Phase 2: Write the invariant Rules
Materialize each law as an always-active markdown rule at project scope. Create `.agents/rules/flywheel-laws.md`:
```markdown
# Flywheel Laws (always active)
1. Author != Judge — the writer of a change never closes its own bead; close runs in a clean-context subagent.
2. Evidence-gated close — close only when every Given/When/Then maps to a captured proof surface.
3. No self-grade — report, never self-verdict; a separate judge decides; ties -> tie-break subagent.
4. Scoped commits — commit only the bead's declared write scope; no drive-by edits.
5. Persist before done — write evidence + learning to the bead, .agents/ratchet/, and an AGY artifact before closing the turn.
```
**Checkpoint:** the rules file exists and reads as imperative law (not advice). Confirm AGY loads project rules from `.agents/rules/`; if your install uses a different rules path, write there instead and note it.

### Phase 3: Write the loop Workflow
Create `.agents/workflows/agy-loop.md` — a slash workflow expressing claim->work->validate->close->persist (the seven-move operating loop in AGY skin). See `references/agy-loop-workflow.md` for the full workflow body to paste. The trajectory:
1. **Claim** — `br ready` / `bd ready`, pick one bead, claim it (`--claim`). One bead per turn.
2. **Work** — implement the smallest vertical slice; TDD per slice; record evidence onto the bead. Stay inside the declared write scope (Rule 4).
3. **Validate** — dispatch a **clean-context subagent** as judge (Rule 1/3). It re-derives PASS/FAIL from the proof surfaces only, never from the author's claim. Tie -> tie-break subagent.
4. **Close** — only on judge PASS with evidence mapped to each acceptance example (Rule 2). Otherwise reopen with the gap.
5. **Persist** — write evidence + learning to the bead + `.agents/ratchet/` + an AGY artifact, then commit the scoped change (Rule 5).

Bind the trajectory to AGY's native controls: set the durable objective with the goal command so every turn steers toward the same north-star, and register the recurring tick with the schedule command (e.g. `agy -p "/schedule agy-loop --every 15m"`) so the turnout self-cranks headless instead of relying on an external cron. The goal command carries the *what*, the Workflow carries the *how*, and the schedule command carries the *when*.

**Checkpoint:** the workflow is invocable as `agy-loop` or via `agy -p "/agy-loop <intent>"`, the goal command holds the loop's objective, the schedule command is registered for the tick, and its steps name a *separate* validator agent — re-read it and confirm the author never appears as the judge.

### Phase 4: Wire the mechanical guardrails (hooks)
Add close/scope guards to `~/.gemini/settings.json` under `hooks` (the file already carries a `BeforeTool` `dcg` guard — extend, do not clobber). Add an `AfterTool` hook that blocks a `bd close`/`br close` lacking captured evidence, and a `BeforeTool` `run_shell_command` matcher that rejects commits outside the bead scope. See `references/agy-loop-workflow.md` for the hook stanza. This skill ships the two guards as executable stubs — `scripts/scope-guard.sh` (Rule 4) and `scripts/close-guard.sh` (Rules 2/5) — wired and safe (they no-op until you implement the marked tracker-read section, then they ENFORCE).
**Checkpoint:** `agy plugin validate` (or a dry run) passes and the existing `dcg` hook is intact.

### Phase 5: Package + smoke
Optionally bundle Rules + Workflow + hooks + subagents as an AGY plugin (`plugin.json`) for `agy plugin install`. Smoke one bead end-to-end headless:
```bash
agy -p "/agy-loop run one ready bead end-to-end; STOP after persist"
```
**Checkpoint:** the smoke run claimed one bead, validated via a separate subagent, and closed only with evidence. If the author closed its own bead, Rule 1 is not wired — return to Phase 2/3.

## Output Specification

**Format:** markdown rules + markdown workflow + JSON hook stanza.
**Filenames / paths:**
- `.agents/rules/flywheel-laws.md` — the five invariant laws (always-active rule).
- `.agents/workflows/agy-loop.md` — the claim->work->validate->close->persist slash workflow.
- `~/.gemini/settings.json` — extended `hooks` block (close-guard + scope-guard), `dcg` preserved.
- (optional) `plugin.json` — AGY plugin manifest bundling the above.

**Returns:** the list of paths written, the rule/workflow IDs, and the smoke-run verdict (which bead, who judged it, evidence captured).

## Quality Rubric

- [ ] All five laws exist as always-active AGY Rules, written as imperative law (not advice).
- [ ] The loop Workflow dispatches a **separate clean-context subagent** as judge — author is never the judge.
- [ ] Close step is gated on evidence mapped to each Given/When/Then; no "looks good" path exists.
- [ ] Commit step is scoped to the bead's declared write scope; a scope guard rejects drive-by edits.
- [ ] Persist step writes to bead + ratchet + AGY artifact before the turn is marked done.
- [ ] `~/.gemini/settings.json` extends hooks without clobbering the existing `dcg` `BeforeTool` guard.
- [ ] Smoke run proves one bead through the full loop with a separate judge and captured evidence.
- [ ] Nothing here leaks into client-facing surfaces (operator-side only).

## Examples

- **Bootstrap the AGY node:** run Phases 1-5; return the four paths + the smoke verdict.
- **Repair a self-closing AGY agent:** Phase 2 (write Rule 1/3) + Phase 3 (rewrite the validate step to dispatch a subagent) + Phase 4 (close-guard hook). Re-smoke.
- **Headless crank:** `agy -p "/agy-loop <intent>; STOP after one bead"` as the AGY turnout's tick.
- **Self-scheduled turnout:** `agy -p "/goal '<epic intent>'"` then `agy -p "/schedule agy-loop --every 15m"` — the loop steers toward the goal and cranks itself on AGY's native scheduler (no external cron).

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Author closes its own bead | Validate step runs in-context, not a subagent | Rewrite Phase 3 step 3 to dispatch a clean-context AGY subagent; encode Rule 1 |
| Bead closes with no evidence | Close-guard hook missing | Add the `AfterTool` close-guard from `references/agy-loop-workflow.md` |
| `dcg` guard stopped firing | `settings.json` hooks block clobbered | Restore the `BeforeTool` `dcg` entry; merge, don't overwrite |
| Rules ignored | Wrong rules path for this install | Verify AGY's project rules dir locally; write the rule there and note it |
| `agy -p` hangs | Print-mode timeout | Pass `--print-timeout`; scope the prompt to one bead with an explicit STOP |

## See Also / References

- `references/agy-loop-workflow.md` — full `agy-loop.md` workflow body + the hook stanza + subagent definitions to paste.
- `scripts/scope-guard.sh`, `scripts/close-guard.sh` — the shipped Rule-4 / Rule-2+5 hook stubs (wire into `~/.gemini/settings.json`; implement the marked tracker-read to enforce).
- `scripts/validate.sh` — self-check (frontmatter + spine + line budget + refs + artifacts); run before staging.
- `operating-loop-workflow` (Claude turnout of the same seven-move loop) and `bead-crank` (Claude bead loop) — the sibling skins.
- `beads-br` — the `br`/`bd` bead primitives the loop cranks.
- AGY harness research: `~/.agents/research/agy-native-harness-2026-06-06.md`.

## References
- [agy-loop-workflow](references/agy-loop-workflow.md)
