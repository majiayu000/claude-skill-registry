---
name: slop
description: 'Slop front door — verdict or purge, routed by domain. Use when the user asks "is this slop?", "does this feel AI-generated?", or "sloppy?", or says "purge the slop" or "clean the slop out", for any artifact: code, prose, decisions, or UI.'
metadata:
  short-description: 'Slop verdict and purge, routed by domain'
---

# Slop

This skill owns the verdict and the purge, not the doctrine — doctrine lives in three domain authorities, reached by invoking them. Slop is two things under one word: centroid-AI default convergence (the taste sense: hedged, averaged, committed to nothing) and mechanical code debris (the deslop sense: debug leftovers, placeholder bodies, swallowed errors).

## Modes [LOAD-BEARING]

### Mode-selection (hybrid)

Auto-detect from the user's phrasing, with slash-arg override:

- Question phrasing — `is this slop?`, `does this feel AI-generated?`, `sloppy?` → **is-slop** (verdict only, zero edits).
- Imperative phrasing — `purge`, `remove`, `clean out`, `deslop everything` → **purge-slop** (act).
- Anything else → **is-slop** (default; cheaper; no behavior commitment).
- Explicit override: `/slop is-slop | purge-slop`. The override always wins.

## Domain routing

Both modes route every finding through the owning authority:

| Domain signals | Authority (invoke) | Citation source |
|---|---|---|
| Code debris: debug output, placeholder or stub bodies, swallowed errors, dead code, hardcoded credentials | `odin:deslop` | Its catalog categories; its certainty contract governs any edit |
| Judgment slop: hedge-stacks, generic openers, 50/50 recommendations, AI-flat prose | `odin:taste` | Side A rows (ceremony and decoration are Side B overkill, not slop) |
| Visual/UI slop: default gradients, framework-default look, vibe-coded UI | `odin:design` | Its anti-slop reference |

A mixed artifact splits into per-domain findings and returns one combined report.

## is-slop procedure

1. Route the artifact (or its parts) per the table.
2. Per finding, one verdict: `slop | not-slop | overkill-not-slop` — the third names the common misdiagnosis: decoration covering thin ideas is Side B overkill, not slop.
3. Attach a doctrine citation from the routed authority to every finding.

**Completion criterion:** one top-line verdict for the artifact; every finding carries a citation from its routed authority; zero edits made.

## purge-slop procedure

1. Route per the table, then act under each authority's own gates:
   - Code → run the `odin:deslop` workflow end to end: HIGH-certainty fixes applied, MEDIUM/LOW report-only, verification and rollback intact.
   - Prose/decisions → run the `odin:taste` audit, then apply its top-ranked fixes; taste is a judgment register, so where two fixes conflict or a fix would reverse a committed choice, ask the user to pick before applying.
   - UI → apply corrections from `odin:design` anti-slop doctrine.
2. Report edits applied vs flagged-only, per authority.

**Completion criterion:** the report separates edits applied from findings flagged-only, and every applied fix stayed inside its authority's contract.
