---
name: model-committee-fable
description: Run a deliberative two-model committee between GPT-5.5 and Claude Opus 4.8, chaired by Fable 5. Same two deliberating members as model-committee; the difference is the chair — Fable 5 aggregates the scores, applies the tie rule, and synthesizes the decision, so a lightweight Claude-family chair handles the tally and synthesis. Use when the user needs one consequential decision from multiple defensible options and wants a Fable-chaired deliberation. Suitable for architecture, research design and interpretation, manuscript strategy, ambiguous diagnosis, evaluation design, and policy or standards tradeoffs. Not for factual lookups, independent-coder reliability, open-ended brainstorming, routine implementation, or final high-stakes professional judgment.
---

# Model Committee (Fable-chaired)

Run GPT-5.5 and Claude Opus 4.8 as a deliberating committee, with **Fable 5 as the chair**. Preserve a clear distinction from `$model-council-voting`: a council measures independent disagreement; this committee deliberately exposes each member to the other's argument and produces one decision.

Read [`references/protocol.md`](references/protocol.md) completely before running a committee.

**Chair variant.** This is the **Fable-chaired** member of a three-variant family; all three deliberate the same two members (GPT-5.5 + Opus 4.8) and differ only in which model chairs the synthesis. Fable's value here is a **lightweight, fast, procedurally disciplined** chair: the heavy reasoning is already spent inside the two members' three rounds, and the chair's remaining job is mostly mechanical, so a lean chair is a deliberate cost choice — and, being neither member, it cannot vote its own prior a third time. Because Fable is a Claude-family model, running under Codex delegates the chair step to it via the bundled `claude-member.sh`. Siblings: [`model-committee`](../model-committee/SKILL.md) (Opus 4.8 chairs) and [`model-committee-sol`](../model-committee-sol/SKILL.md) (GPT-5.6 "Sol" chairs).

## Gate the workflow

Run only when the user explicitly invokes `$model-committee-fable` or requests a Fable-chaired GPT-5.5 / Opus 4.8 deliberation. The workflow makes external model calls and uses more tokens than a single answer.

Apply the use-case gate in the protocol first. If the task does not qualify, recommend the correct alternative and do not call any model.

Before the first call:

1. Confirm the task and the decision that must be returned.
2. Confirm any sensitive material may be sent to both providers.
3. Explain that both CLIs may consume separate plan credits or API spend; obtain confirmation unless already explicit.
4. Precommit the evaluation criteria, weights, and tie rule.

## Preflight members and chair

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`, then run:

```bash
"$SKILL_DIR/scripts/codex-member.sh" --check
"$SKILL_DIR/scripts/claude-member.sh" --check
```

Default pins:

- GPT member: `gpt-5.5`
- Claude member: `claude-opus-4-8`
- Chair: `claude-fable-5` (Fable 5), reached through `claude-member.sh`

These are deliberately exact pins, not moving aliases. Do not silently substitute another model. If a pin is unavailable, report it and ask whether to stop or use a named replacement.

## Run the committee

Create a temporary working directory such as `.committee-tmp/<slug>/`. Follow the protocol's prompt contracts and produce these artifacts:

```text
brief.md
round-1-gpt.prompt.md       round-1-gpt.md
round-1-opus.prompt.md      round-1-opus.md
round-2-gpt.prompt.md       round-2-gpt.md
round-2-opus.prompt.md      round-2-opus.md
round-3-gpt.prompt.md       round-3-gpt.md
round-3-opus.prompt.md      round-3-opus.md
chair.prompt.md             decision.md
```

Invoke each member through the bundled read-only driver:

```bash
"$SKILL_DIR/scripts/codex-member.sh" \
  --prompt-file <prompt.md> --out <output.md> -C <working-directory>

"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file <prompt.md> --out <output.md> -C <working-directory>
```

Launch the two calls in each round concurrently when the runtime supports it. Sequential execution is acceptable only if the second prompt was frozen before the first result arrived. Do not show either member the other's output during round 1.

## Chair with Fable, without becoming a third debater

The chair for this variant is **Fable 5.** Bundle the brief and all round outputs into `chair.prompt.md` (using the protocol's decision-rule and output contracts), then delegate the post-round-3 chair step:

```bash
"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file chair.prompt.md --out decision.md --model claude-fable-5 -C <working-directory>
```

The chair's job:

- validate outputs against the required schemas;
- aggregate the predeclared weighted scores mechanically;
- apply the precommitted tie rule;
- synthesize only components both revisions explicitly mark compatible; and
- never introduce a new substantive option or break a tie by confidence, eloquence, or model identity.

If the evidence remains genuinely unresolved, return the exact fork to the user. A forced but unsupported answer is not committee consensus. Verify the chair's arithmetic against the round-3 score tables and confirm the decision matches the precommitted rule before you deliver it — the mechanical steps are exactly where a lightweight chair must be checked.

## Deliver

Return a compact decision record containing:

1. use case and why committee treatment was justified;
2. decision and decision rule (note that Fable 5 chaired);
3. strongest reasons and evidence;
4. what changed during deliberation;
5. surviving dissent or uncertainty;
6. implementation or verification next step.

Delete `.committee-tmp/` after delivery unless the user asks to preserve the full transcript. Never let any member or the chair edit the workspace during deliberation; implement only after the decision is accepted.
