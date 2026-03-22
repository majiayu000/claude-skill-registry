---
name: re
description: Explicit extra-research mode. Use only when the user says `/re` or clearly asks for a research-heavy pass before coding. This skill should bias Codex toward more source-checking and justification without replacing its normal orchestration.
---

# Re

Use this as a light override, not a rigid workflow. Keep Codex's default orchestration and only add extra diligence where it matters.

## Defaults

- Inspect the local codebase first.
- Do research in 3 passes when the task is genuinely research-heavy:
  1. Plan 3-6 sub-questions.
  2. Retrieve sources for each sub-question and follow 1-2 second-order leads when useful.
  3. Synthesize only after resolving conflicts and gaps that could change the conclusion.
- Use Context7 first for version-sensitive library or framework behavior.
- Use native `web` first for current information.
- Use Jina only when native `web` is not enough for long pages, PDFs, or parallel page reads.
- Only cite sources retrieved in the current workflow, and label any inference that is not directly supported by those sources.
- If sources conflict, state the conflict explicitly instead of averaging them into one answer.
- If a search result is empty, partial, or suspiciously narrow, retry with a broader query, alternate wording, or a second source before concluding there is no answer.
- Compare options only when there is a real tradeoff.
- Implement once the decision is clear.
- Run the smallest relevant verification commands before finishing.

## Avoid

- Do not force phases.
- Do not produce long research reports unless the user asked for them or the task materially benefits.
- Do not ask extra questions if local context is already enough.
- Do not delegate work just because this skill is active.

## Large Tasks

For long tasks, optional scratch notes can live in `/tmp/re-research/<slug>/`.

If useful, keep a short `decisions.md` with:
- key findings
- rejected options
- remaining risks
- pending verification

## Finish

Keep the final response compressed:
- decision
- source-backed justification
- key sources or citations when they materially matter
- code or config changed
- tests run
- remaining unknowns
