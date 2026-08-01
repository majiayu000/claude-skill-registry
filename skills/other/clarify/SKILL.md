---
name: clarify
description: 'Scan a request, document, or conversation for ambiguities, undefined terms, implicit assumptions, and unstated boundaries, then surface them as a certainty-tiered findings report with recommended defaults. Use when the user says "clarify", "what is ambiguous here", "find the gaps in this spec", "what am I assuming", or when a prompt or spec reads as under-specified before planning.'
---

# Clarify

Detect ambiguity before anyone acts on it. `clarify` scans a target — the user's request, a pasted document, or the conversation so far — and returns a structured findings report of every ambiguity, undefined term, implicit assumption, and unstated boundary it finds, each tagged with a certainty tier and a recommended default. It detects first and asks second; it is not a question-batcher (that is `askme`).

## Target

The target is, in order of precedence: an explicit argument (`/clarify <text-or-path>`), the most recent user request if it reads as a spec or task, or the open conversation context if no single request is in scope. If no target is identifiable after one read, stop and ask one question naming what to scan; do not scan nothing.

## Method

1. **Pre-scan facts.** Before surfacing anything to the user, resolve every ambiguity that is actually an environmental or codebase fact by looking it up with a subagent or tool (`grep`, `glob`, `read`, `lsp`) — never ask the user for something the repo can answer. A resolved fact is recorded as tier `auto`, reported compactly with its basis, and never becomes a question.

2. **Classify the rest by certainty tier.** Assign every finding exactly one tier:
   - `auto` — an unambiguous project convention resolves it; record the resolution and basis, then proceed.
   - `gated` — a reasonable default exists; surface it as a recommendation that **locks unless the user overrides it**.
   - `manual` — evidence cannot settle genuine intent; surface a non-locking recommendation based on the least irreversible standard choice, then ask.
   - `fyi` — worth noting, not worth blocking on; list it, do not ask.

3. **Emit the findings report.** Output one block per finding with fields: `id`, `quote` (the exact ambiguous span), `tier`, `recommendation` (the proposed resolution, or `—` for `fyi`), and `basis` (the fact or convention that supports it). Group findings by tier, `manual` last. The report is the deliverable; the user overrides only the `gated`/`manual` rows they disagree with.

4. **Ask only the manual tier.** Fire the `manual` findings as questions using the `ask` tool, one single-select question per finding with its non-locking recommendation marked, at most four per fire. Follow the current `AskUserQuestion` contract in `skills/askme/SKILL.md`. If there are zero `manual` findings, ask nothing — the report alone is the result.

5. **Route resolved terms.** Any `gated`/`manual` finding the user settles that introduces a project-specific term is recorded as a CONCEPTS.md *candidate* and handed to autolearn's concept-capture mode; `clarify` routes the candidate, it does not write CONCEPTS.md (autolearn owns that surface, one writer).

## Completion

`clarify` is done when both hold: (a) zero `manual` findings remain open — each is answered or discharged as a non-issue with a one-line reason, so every ambiguity is resolved or proven irrelevant; and (b) the finding set is MECE — no two findings ask the same thing and none overlaps another. Re-scan once after the user's overrides; stop when a re-scan adds no new `manual` finding.

## Machine-readable output

On explicit request for structured output, emit the findings as a fenced `clarify-findings/v1` block containing a YAML list of the per-finding fields above. In a plain interactive run, emit only the human-readable grouped report.
