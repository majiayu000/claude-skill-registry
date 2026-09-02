---
name: catchup
description: 'Use when the human returns after a gap, cannot follow the project, or asks what happened. Returns a screen-length briefing grounded in live state. Also handles pre-decision orientation when the mental model is stale. Not for initial onboarding — use onboard.'
---

# Catchup

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The human returns after a gap, says they can't follow the project, asks what happened or what a term means, or before deciding what to do next when their mental model is stale |
| Authority | Read-only; reads live project state and briefs, does not fix, rename, decide, or mutate anything |
| Side effect | None (read-only briefing); it briefs, it does not act |
| Done | Cold-read of the briefing requires no pre-gap memory or unglossed coined term to parse; needs-you items are each actionable without opening another file; every claim has a checkable source; fits on a screen with expansion offered rather than delivered |

## Inputs

The project working directory, inferred from the current repository when not supplied. If known, use the human's last touch point: their last message, judgment, or commit. When it is not explicitly supplied, infer it from session history or the most recent commit.

## Procedure

1. Read only live state: recent file mtimes, git log and diffs, plan and state docs, task boards, and re0-memo notes. Never brief from conversation memory alone; that memory may have drifted. **Done when:** live state is read from the project, not from conversation memory.
2. Anchor on the human's last touch (their last message, judgment, or commit). Everything after that point is the delta; everything before it is assumed known and stays out. **Done when:** the last touch point is identified and the delta boundary is set.
3. Compose in decision order, not chronological order:
   - **Needs you** — decisions, judgments, or inputs only the human can give, each self-contained enough to act on without opening another file.
   - **Changed while you were away** — outcomes, not process. Prefer "The plan's scoring rule was replaced" to "I ran three analysis passes."
   - **New words** — every term coined or repurposed since their last touch, one line each, with where it lives. Skip terms they already used themselves.
   **Done when:** the three sections are composed in decision order.
4. Gloss on first use: any project-specific term appearing in the briefing gets an inline plain-language aside at its first occurrence, even if a glossary section follows. **Done when:** every project-specific term is glossed at first use.
5. Keep the default short (a screen or less). End with drill-down offers per section, not with everything expanded. **Done when:** the briefing fits on a screen with drill-down offers, not full expansion.
6. Cold-read the briefing for pre-gap memory dependence or unglossed coined terms; confirm each needs-you item is actionable without opening another file; confirm every claim has a checkable source (file, commit, or artifact path). **Done when:** the cold-read passes with no pre-gap memory dependence, no unglossed terms, actionable needs-you items, and sourced claims.

## Failure and recovery
- No live state found: if the working directory has no readable git history, plan docs, or task artifacts, report that the project state is unreadable and name what was checked. Do not fabricate a briefing from memory.
- Last touch point unidentifiable: if the human's last message, judgment, or commit cannot be determined, state the assumption used (e.g., most recent commit) and proceed. Do not guess silently.
- Claim without source: if a claim cannot be traced to a file, commit, or artifact, drop it or mark it explicitly as unverified. Never present an ungrounded claim as fact.
- Briefing exceeds a screen: trim to the needs-you items and one-line summaries of the changed and new-words sections; offer drill-down for the rest. Do not deliver the full expansion by default.
- Partial result: a briefing covering only some sections is still useful if every included claim is source-grounded; state which sections were omitted and why.

## Output
A screen-length briefing with three sections in decision order (Needs you, Changed while you were away, New words), every claim tracing to a file, commit, or artifact path, every project-specific term glossed at first use, and drill-down offers per section; the briefing requires no pre-gap memory to parse.
