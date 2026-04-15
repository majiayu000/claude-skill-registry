---
name: transformer
description: Use when rewriting a skill so a reasoning model follows it more reliably or with less prompt scaffolding.
argument-hint: <path to skill.md or skill name>
---

input = $ARGUMENTS

Rewrite the target skill so a reasoning model executes it with better judgment, not just different formatting.

## What This Is

Skills fail reasoning models in two opposite ways:

1. **Over-proceduralized** — numbered checklists the model follows mechanically, stopping it from noticing anything not on the list. Scaffolding competes with the model's own chain-of-thought.
2. **Under-specified** — abstract principles without concrete anchoring. The model understands the philosophy but is slow and uncertain about what to actually *do*.

The target is the middle: **motivated structure**. Steps exist where the model genuinely needs them. Each step carries its *why*. Everything the model can reason through on its own is stripped.

## Classify Before Cutting

Read the entire skill. Before changing anything, classify each element:

**Strip** — reasoning scaffolding the model handles natively:
- Steps telling it how to think about problems it already reasons through
- Phantom constraints it already follows (e.g., "write clean code")
- Redundant restatements of project-level conventions (CLAUDE.md covers these)

**Keep and compress** — things the model genuinely can't know:
- **Orchestration** — approval gates, multi-agent coordination, conditional phases. Protocol, not scaffolding.
- **Domain knowledge** — tiers, taxonomies, heuristic catalogs. These look like checklists but encode non-obvious expertise. Compress if verbose; don't flatten into prose.
- **Calibration** — statements countering pretraining bias ("you'll want to skip this step — don't", "this tier accounts for 50% of savings"). Highest-value lines in any skill. Never strip.
- **Templates & contracts** — output formats, teammate prompts, tool restrictions. The model wouldn't produce these without being told.
- **Failure modes** — specific ways the model will go wrong on *this* task. "Watch out for X" is worth more than paragraphs of positive instruction. Anti-examples showing wrong output are especially high-value.

**The litmus test:** Would removing this cause the model to do the wrong thing, skip something, or coordinate incorrectly? Keep it. Would a reasoning model arrive here on its own? Strip it.

## What Good Looks Like

A well-transformed skill has these qualities:

- **Layered** — intent and scope up top, then principles, then specifics. Not a flat rule list.
- **Motivated** — every constraint carries a sentence of *why*, so the model adapts in novel situations instead of pattern-matching.
- **Concrete** — at least one input/output example or anti-example showing the skill's core judgment call. Abstract principles without anchoring produce uncertain behavior.
- **Failure-aware** — names the 2-3 ways the model is most likely to go wrong on this specific task. Generic warnings ("be careful") do nothing; specific ones ("python-pptx silently drops formatting when...") change behavior.
- **Appropriately trusting** — constrains where the model's defaults are genuinely wrong; gives freedom where its instincts are solid. Over-control produces worse results than under-control.

## Rewriting Principles

- **Motivate constraints.** Explain *why* so the model applies the principle in novel situations.
- **Trust in context.** Don't restate what project-level config already specifies.
- **Resist over-specification.** Each instruction competes for attention. Keep only what wouldn't be obvious without the skill.
- **Positive directives over negative framing.** "Use direct tool calls for simple lookups" beats "don't over-engineer" — negative framing primes the behavior it describes.
- **Add failure modes, not just principles.** Where will the model go wrong? Name it. A concrete anti-pattern is the highest-density instruction you can write.

## Process

Read the skill completely. Understand its purpose and the failure modes it prevents. Draft the rewrite. **Present to user for feedback before writing** — transformation is a judgment call, not a mechanical operation.

## Prompt Design Philosophy

Apply these principles when crafting the rewritten skill:

!`cat ~/.claude/skills/prompt/SKILL.md`
