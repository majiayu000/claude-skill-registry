---
name: create-decision-log
description: Record a product or engineering decision with full context when the user asks to log a decision, record a choice, or document why something was decided
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[decision topic or question]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: docs, decisions, tracking
---

# Create Decision Log

## Overview

Create a structured decision journal entry that separates decision quality from outcome quality, inspired by Annie Duke's "Thinking in Bets." Captures the context, options, rationale, and expected outcomes at the time of decision, enabling future review and learning.

## Workflow

1. **Read existing context** — Scan `.chalk/docs/product/` and `.chalk/docs/engineering/` for related decisions, PRDs, ADRs, or other docs that provide context for this decision. Check for previous decision logs that address similar topics.

2. **Capture the decision** — Parse `$ARGUMENTS` to identify the decision topic. If the topic is vague, ask the user to clarify the specific choice being made. Every decision log answers: "What did we decide, and why?"

3. **Document the context** — Record the circumstances at the time of decision: what information was available, what constraints existed, what pressures were present (time, resources, competitive), and what the stakes were. This section is critical for future retrospection.

4. **Enumerate options considered** — List all options that were seriously evaluated, including the option of doing nothing. For each option, note the key pros, cons, and the estimated probability of success or risk.

5. **Record the decision and rationale** — State the chosen option and the reasoning. Distinguish between: (a) evidence-based reasons (data, research), (b) principled reasons (values, strategy alignment), and (c) pragmatic reasons (time pressure, resource constraints). Be honest about which type dominates.

6. **Define expected outcomes** — What does the decision-maker expect to happen? Include both the hoped-for outcome and the realistic range. State the confidence level (high / medium / low) and the timeframe for evaluation.

7. **Set revisit triggers** — Define conditions that should trigger a re-evaluation of this decision: specific metrics thresholds, dates, or events. This prevents both premature reversal and zombie decisions that persist past their relevance.

8. **Determine the next file number** — Read filenames in `.chalk/docs/product/` to find the highest numbered file. Use `highest + 1`.

9. **Write the decision log** — Save to `.chalk/docs/product/<n>_decision_<topic>.md`.

## Output

- **File**: `.chalk/docs/product/<n>_decision_<topic>.md`
- **Format**: Markdown with structured sections
- **Key sections**: Date, Decision Statement, Context, Options Considered (with pros/cons), Decision, Rationale (evidence / principled / pragmatic), Expected Outcome (with confidence and timeframe), Actual Outcome (blank — filled later), Revisit Triggers

## Anti-patterns

- **Outcome bias** — Judging a decision by its outcome rather than the quality of reasoning at the time. A good decision can have a bad outcome and vice versa. This log captures decision quality independently.
- **Hindsight editing** — Rewriting the context or rationale after the outcome is known. The context section must reflect what was known at decision time, not what was learned later.
- **Missing the "do nothing" option** — Every decision should include the status quo as an explicit option with its own pros and cons. Sometimes the best decision is to not decide yet.
- **Vague rationale** — "It felt right" is not a rationale. Even intuition-based decisions should articulate the underlying pattern recognition or experience driving the intuition.
- **No revisit triggers** — A decision without revisit conditions becomes permanent by inertia. Every decision log must define when and under what conditions the decision should be reconsidered.
- **Logging only big decisions** — Small, frequent decisions compound. Log decisions that are reversible but consequential, not just the "big bets."
