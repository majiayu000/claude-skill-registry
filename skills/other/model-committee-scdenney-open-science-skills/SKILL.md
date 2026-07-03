---
name: model-committee
description: Run a deliberative two-model committee between GPT-5.5 and Claude Opus 4.8. Use when the user needs one consequential decision from multiple defensible options and wants the two model families to propose independently, inspect each other's reasoning, revise, cross-rank, and converge under a predeclared rubric. Suitable for architecture, research design and interpretation, manuscript strategy, ambiguous diagnosis, evaluation design, and policy or standards tradeoffs. Not for factual lookups, independent-coder reliability, open-ended brainstorming, routine implementation, or final high-stakes professional judgment.
argument-hint: "[decision or problem for GPT-5.5 and Opus 4.8 to deliberate]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
---

# Model Committee

Run GPT-5.5 and Claude Opus 4.8 as a deliberating committee. Preserve a clear distinction from `model-council-voting`: a council measures independent disagreement; this committee deliberately exposes each member to the other's argument and produces one decision.

Read [`reference/protocol.md`](reference/protocol.md) completely before running a committee.

## Gate the workflow

Run only when the user explicitly invokes `/model-committee` or requests GPT-5.5 and Opus 4.8 to deliberate. The workflow makes external model calls and uses more tokens than a single answer.

Apply the use-case gate in the protocol first. If the task does not qualify, recommend the correct alternative and do not call either model.

Before the first call:

1. Confirm the task and the decision that must be returned.
2. Confirm any sensitive material may be sent to both providers.
3. Explain that both CLIs may consume separate plan credits or API spend; obtain confirmation unless already explicit.
4. Precommit the evaluation criteria, weights, and tie rule.

## Preflight both members

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`, then run:

```bash
"$SKILL_DIR/scripts/codex-member.sh" --check
"$SKILL_DIR/scripts/claude-member.sh" --check
```

Default pins:

- GPT member: `gpt-5.5`
- Claude member: `claude-opus-4-8`

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
decision.md
```

Invoke each member through the bundled read-only driver:

```bash
"$SKILL_DIR/scripts/codex-member.sh" \
  --prompt-file <prompt.md> --out <output.md> -C <working-directory>

"$SKILL_DIR/scripts/claude-member.sh" \
  --prompt-file <prompt.md> --out <output.md> -C <working-directory>
```

Launch the two calls in each round concurrently when the runtime supports it. Sequential execution is acceptable only if the second prompt was frozen before the first result arrived. Do not show either member the other's output during round 1.

## Chair without becoming a third debater

Act as a procedural chair after round 3:

- validate outputs against the required schemas;
- aggregate the predeclared weighted scores mechanically;
- apply the precommitted tie rule;
- synthesize only components both revisions explicitly mark compatible; and
- never introduce a new substantive option or break a tie by confidence, eloquence, or model identity.

If the evidence remains genuinely unresolved, return the exact fork to the user. A forced but unsupported answer is not committee consensus.

## Deliver

Return a compact decision record containing:

1. use case and why committee treatment was justified;
2. decision and decision rule;
3. strongest reasons and evidence;
4. what changed during deliberation;
5. surviving dissent or uncertainty;
6. implementation or verification next step.

Delete `.committee-tmp/` after delivery unless the user asks to preserve the full transcript. Never let either member edit the workspace during deliberation; implement only after the decision is accepted.
