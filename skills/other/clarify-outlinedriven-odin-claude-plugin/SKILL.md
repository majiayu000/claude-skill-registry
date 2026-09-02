---
name: clarify
description: 'Use when the user says "clarify", "what is ambiguous here", or when a prompt or spec reads as under-specified before planning. Surfaces ambiguities as a certainty-tiered findings report with recommended defaults. Not for exploring intent with questions — use askme.'
---

# Clarify

## Contract

| Field | Bound contract |
|---|---|
| Trigger | 'Clarify', 'what is ambiguous', 'find gaps in this spec', or an underspecified request. |
| Authority | Read-only analysis: no file, VCS, credential, paid, published, deployed, or remote mutation. Everything the skill produces is chat text. |
| Side effect | Chat output only: findings, recommended defaults, and questions. |
| Done | No open manual ambiguity remains — each is answered or discharged as a non-issue with a one-line reason — the finding set is MECE, and the restatement matched the target or its mismatch was surfaced as the first finding. |

## Inputs

- Scan target, in strict precedence: an explicit argument (`clarify <text-or-path>`), else the most recent user request when it reads as a spec or task, else the open conversation context. No other input is required; the text-or-path argument is optional.

## Procedure

1. Select the target by the precedence above and read it once for the whole run. **Done when:** the target is selected and read once.
2. Restate the read before scanning: write the target back as a single paraphrased instruction, including what it does not ask for, and compare it against the target. A mismatch is the first finding and outranks every other finding, because a correct answer to a misread request is still wrong. When the restatement matches, carry it silently — it becomes output only if a fork survives. **Done when:** the restatement is written and compared, and any mismatch is surfaced as the first finding.
3. Pre-scan facts before surfacing anything to the user: resolve every ambiguity that is actually an environmental or codebase fact by direct lookup (search, read, or a subagent) — never ask the user for something the repo can answer. Each resolved fact is recorded as tier `auto` with its basis, reported compactly, and never becomes a question. **Done when:** every resolvable-by-lookup ambiguity is resolved as tier `auto` with its basis.
4. Classify every remaining finding with exactly one certainty tier:
   - `auto` — an unambiguous project convention resolves it; record the resolution and basis, then proceed.
   - `gated` — a reasonable default exists; surface it as a recommendation that locks unless the user overrides it.
   - `manual` — evidence cannot settle genuine intent; surface a non-locking recommendation based on the least irreversible standard choice, then ask.
   - `fyi` — worth noting, not worth blocking on; list it, never ask.
   **Done when:** every remaining finding has exactly one certainty tier assigned.
5. Enforce MECE before emitting: merge or drop findings that ask the same thing as, or overlap, another finding. **Done when:** the finding set is MECE with no overlaps.
6. Emit the findings report (see Output). The report is the deliverable; the user overrides only the `gated`/`manual` rows they disagree with. **Done when:** the findings report is emitted grouped by tier with `manual` last.
7. Ask only the manual tier: one single-select question per `manual` finding with its non-locking recommendation marked, at most four questions per fire. At zero `manual` findings, ask nothing — the report alone is the result. **Done when:** manual questions are fired (at most four) or zero manual findings means no questions.
8. After the user's overrides, re-scan the target once; stop when the re-scan adds no new `manual` finding. Record every settled finding as overridden, answered, or discharged as a non-issue with a one-line reason. **Done when:** the re-scan adds no new manual finding, and every settled finding is recorded.
9. List any project-specific term the user settled during clarification as a CONCEPTS.md candidate in the report. Record the candidate; write no files. **Done when:** settled terms are recorded as CONCEPTS.md candidates.

## Failure and recovery
- No identifiable target after one read of the context: stop and ask exactly one question naming what to scan. Classify nothing and emit no report; scanning nothing is a failure, not an empty result.
- A fact lookup fails or is inconclusive: the ambiguity is not `auto`; it falls to normal tiering (usually `manual`). Never guess a fact to avoid asking.
- Partial scan (a span is unreadable or unreachable): emit the findings found so far, name the span excluded, and do not claim done.
- Manual questions left unanswered: the open `manual` findings remain; state that clarification is incomplete and list their ids. The done predicate does not hold.
- Nothing is ever written, so there is no rollback: recovery is re-running the scan. Never swallow a lookup error or present an incomplete pass as done.

## Output
A findings report grouped by tier with `manual` last, one block per finding with fields `id`, `quote` (the exact ambiguous span), `tier`, `recommendation` (`—` for `fyi`), and `basis` (the fact or convention supporting it); `gated` recommendations marked locked-unless-overridden, `manual` ones non-locking, `auto` resolutions appearing compactly with their basis; the manual questions fired (at most four per fire) and the CONCEPTS.md candidates recorded from settled terms; on explicit request for structured output, one fenced `clarify-findings/v1` block containing a YAML list of the per-finding fields.
