---
name: pre-land-refuters
description: "Dispatch unbiased refuters (fresh Fable + read-only codex exec) to attack a completion claim before landing a large change. Triggers: pre-land validation, refute before push."
practices:
- llm-eval-harness
- ai-assisted-dev
hexagonal_role: driving-adapter
consumes:
- validate
- codex-exec
produces:
- .agents/council/*.md
context_rel:
- kind: customer-of
  with: validate
- kind: customer-of
  with: codex-exec
skill_api_version: 1
user-invocable: true
metadata:
  tier: judgment
  dependencies:
  - validate
  - codex-exec
  internal: false
output_contract: .agents/council/YYYY-MM-DD-pre-land-*.md
---

# /pre-land-refuters — unbiased dual-model validation before landing

> Proven in the ag-s43tg prune landing (2026-06-12): the refuter panel caught 9
> real misses self-review passed over — a silently-failed edit, a CI-breaking
> test, stale image manifests, gate-weakening test retirements, and an upstream
> delete/modify conflict. Self-review is biased toward "looks good"; refuters
> are prompted to win by finding what's wrong.

## When to fire

Before pushing any change that is large (100+ files), regenerates factory
surfaces, repoints contract tests/canaries, or removes capability. NOT for
routine single-file changes — the panel costs two agent runs.

## Constraints

- **Pin acceptance BEFORE the work.** The claim under test must be mechanical:
  grep-able fixtures (pinned phrases, counts, ledger states) frozen before
  implementation, not chosen post-hoc. No pins → write them first.
- **Refuters are read-only and stake-free.** Fresh context, no session history,
  no authorship of the change. Prompt them to REFUTE, default to skepticism.
- **Two model families minimum.** One Fable/Claude subagent + one `codex exec
  --sandbox read-only` validator. Same-family redundancy misses shared blind spots.
- **Findings are fixed forward, never disarmed.** A refuted contract test gets
  an honest repoint to the surviving surface or a real fix — not deletion.
- **Orchestrator stays the single writer.** Refuters report; only the
  orchestrator edits. Run the panel concurrently with the final full gate.
- **Re-verify pins on the landed tree** after merge/push, not just pre-commit.

## Workflow

1. **Freeze the claim.** State it in one sentence with mechanical acceptance
   (e.g. "all N pinned phrases grep green; ledger has N terminal rows; staged
   set is one revert unit").
2. **Dispatch the Fable refuter** (background subagent, fresh context):
   verify counts, sweep every pinned fixture, audit the ledger, hunt stragglers
   referencing removed paths, spot-check routing, check revert-unit coherence
   and upstream drift (`git fetch` + behind-count). Output: VERDICT
   CONFIRMED/REFUTED + numbered findings with evidence.
3. **Dispatch the codex refuter** (`codex exec --sandbox read-only -C <repo>`):
   focus on judgment-sensitive edits — for each contract-test/canary/validator
   change in the diff, judge: honest repoint vs gate-weakening. Same verdict
   shape.
4. **Run the full local gate concurrently** (it is the third, mechanical
   refuter).
5. **Triage findings**: fix each forward; classify pre-existing vs introduced;
   re-run only the affected validators.
6. **Land** (commit → merge upstream if it moved → gate → push), then re-run
   the pinned sweep on the landed tree and record the panel verdicts in
   `.agents/council/YYYY-MM-DD-pre-land-<slug>.md`.

## Output Specification

**Format:** a council artifact at `.agents/council/YYYY-MM-DD-pre-land-<slug>.md`
containing: the frozen claim, both refuter verdicts (verbatim findings), the
fix-forward disposition per finding, and the post-land pin re-verification.

## Quality Rubric

- [ ] Claim frozen with mechanical acceptance before refuters dispatched
- [ ] Two model families, both read-only, both prompted to refute
- [ ] Every REFUTED finding has a fix-forward disposition (none ignored, none disarmed)
- [ ] Pins re-verified green on the landed tree
- [ ] Council artifact persisted

## Examples

**User says:** "land this prune, don't cut corners"
**Do:** freeze the pinned-manifest claim → dispatch Fable refuter (Agent tool,
fresh context) + codex refuter (`codex exec --sandbox read-only "...judge each
contract-test edit: honest repoint vs gate-weakening..."`) + full gate, all in
parallel → fix findings forward → land → re-sweep pins.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Refuter says CONFIRMED instantly | Prompt lacked mechanical checks | Re-dispatch with explicit per-fixture commands; "try to refute" + checklist |
| Findings contradict each other | Different scopes | Triage per finding with evidence; the diff is the arbiter |
| Panel too slow | Run was serial | Dispatch both refuters + gate concurrently; they are read-only |

## See Also

- [validate](../validate/SKILL.md) — verdict contract the panel reports in
- [codex-exec](../codex-exec/SKILL.md) — the codex refuter lane
- [codex-approval](../codex-approval/SKILL.md) — the inverse direction (Codex asks Fable)
- [red-team](../red-team/SKILL.md) — adversarial probing of docs/plans (pre-work); this skill is pre-land
- [rpi](../rpi/SKILL.md) — invokes this panel at Phase 3 exit on full-complexity arcs
- [pre-mortem](../pre-mortem/SKILL.md) — plan-time twin (move 4); this skill is the landing twin (move 6 exit)
- [post-mortem](../post-mortem/SKILL.md) — consumes the council artifact as landing evidence (move 7)
