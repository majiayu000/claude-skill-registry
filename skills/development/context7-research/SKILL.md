---
name: context7-research
description: Deep library, dependency, framework, and API documentation research using Context7 MCP tools only. Use when you need up-to-date docs, version-specific API reference, migration guidance, or to verify code against official documentation. Triggers on requests like “look up docs”, “API reference”, “how do I use X”, “latest/current”, “deprecated”, “breaking changes”, “best practices”, or whenever correctness depends on primary documentation.
allowed-tools:
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
---

# Context7 Research

Use Context7 as the source of truth for library/framework documentation during implementation, reviews, and debugging.

## Workflow (MUST FOLLOW)

1. Extract:
   - `libraryName`: product/package/framework name (e.g., `next.js`, `zod`, `supabase`)
   - `objective`: what you need to do (e.g., “configure SSR auth”, “migrate v3->v4”, “use hook X”)
   - `version`: only if the user specifies one or you can infer it from repo context (otherwise default to “latest”).
2. If the user already provided a Context7 library ID in `/org/project` (or `/org/project/version`) format, skip resolution.
3. Otherwise call `mcp__context7__resolve-library-id` with:
   - `libraryName`: extracted name
   - `query`: the full user objective (not just a keyword)
4. Select the best match using this rubric:
   - Exact/closest name match
   - Highest source reputation
   - Highest snippet coverage (prefer more snippets when reputation is similar)
   - Highest benchmark score
   - Versions available that match the requested version (if any)
5. Call `mcp__context7__query-docs` with the selected `libraryId` and a tight query (see Query Budget).
6. Synthesize an answer:
   - Include the `libraryId` used (and version if applicable)
   - Quote or paraphrase only what’s needed; prefer code examples
   - If docs are missing/ambiguous, label the gap as `UNVERIFIED` and ask for the smallest clarification needed.

## Query Budget (HARD LIMIT)

Use at most **3** `mcp__context7__query-docs` calls per user request. Plan the queries up-front:

- Query 1 (overview): “Explain the concept and where it lives in the docs; include minimal example.”
- Query 2 (API details): “Exact function/class/method signatures and usage examples for the user’s task.”
- Query 3 (edge cases): “Pitfalls, errors, version differences, and recommended patterns.”

If you can’t cover everything within 3 calls, ask the user to narrow scope (or pick the highest-impact subquestion).

## Output (DEFAULT SHAPE)

- Start with the recommended approach (1–5 bullets).
- Include at least one doc-backed example/snippet when the question is about code.
- End with “Assumptions / Gaps” if anything is uncertain (`UNVERIFIED`) or version-dependent.

## Resources

- Playbook: `references/playbook.md`
- Troubleshooting: `references/troubleshooting.md`
- Design + scoring (maintainers): `references/design-spec.md`
- Report template: `assets/report-template.md`
- Generate a new report file: `python3 scripts/new_report.py --out ./context7-research.md --library-name "<name>" --question "<objective>"`
