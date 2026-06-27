---
name: autolearn
description: Compound a just-solved problem into a durable in-repo learning doc under docs/solutions/, refresh stale learnings as code drifts, and route user/preference facts to memory-update. Use after a verified non-trivial fix, or when the user says "/autolearn", "compound this", "document this fix", "remember this". Fires automatically on success signals like "that worked", "it's fixed", "working now", "problem solved".
metadata:
  short-description: Compound a solved problem into docs/solutions/ + refresh learnings
---

# Autolearn — compound a solved problem, keep the learnings honest

`autolearn` turns a verified fix into one in-repo learning doc, maintains those docs as the code moves, captures durable project vocabulary, and hands user/preference facts to the memory writer. It writes exactly **two** in-repo surfaces itself: the operating repo's `docs/solutions/` (one learning per file) and the repo-root `CONCEPTS.md` (the shared-vocabulary glossary, one definition per concept). One writer per surface still holds — autolearn owns both, and no other skill edits them. Every auto-memory write is delegated to `memory-update` — there is one writer of the memory surface, and it is not this skill.

`Op:` of a compound run is `extend` (a new learning) or, in refresh, `correct`/`purge` (see Commits).

## Auto-invoke

<auto_invoke>
<trigger_phrases>
- "that worked"
- "it's fixed"
- "working now"
- "problem solved"
</trigger_phrases>
Fire automatically on a trigger phrase or after a verified non-trivial fix. The reject-by-default gate below still decides whether a doc is actually warranted — auto-firing is permission to evaluate, not permission to fabricate.
<manual_override>`/autolearn [context]` documents immediately without waiting for a trigger phrase. `autolearn mode:refresh [scope]` runs maintenance. `mode:headless` makes any mode non-interactive.</manual_override>
</auto_invoke>

## Preconditions — then the reject-by-default gate

A doc is earned, not assumed. First the ce preconditions, then the hermes filter.

**Preconditions** (all three):
1. The problem is solved — not in progress.
2. The solution is verified — observed working, not hoped working.
3. It was non-trivial — not a typo or an obvious one-liner.

**Reject-by-default gate** — a lesson earns a doc only if it clears all three filters in order:
1. **Would I forget this?** Skip baseline knowledge anyone in this codebase already carries. If you'd remember it without a note, it isn't a learning.
2. **Already covered?** If an existing `docs/solutions/` doc covers it, updating that doc beats spawning a second one. A duplicate is drift, not knowledge.
3. **Universal or local?** Scope-qualify. A repo-specific quirk says so; a general truth says so. An unqualified claim is a future trap.

**If nothing clears the gate, say so in one line and exit. Never fabricate a doc to look productive.** A clean "nothing worth compounding here" is a valid, correct result.

The gate governs `CONCEPTS.md` entries too: a term earns a slot only when you'd otherwise forget its precise *local* meaning (filter 1), it isn't already defined there (filter 2 — one definition per concept, no duplicates), and it is scope-qualified to this project rather than general programming or domain English (filter 3). A term that clears the gate is a Vocabulary-capture candidate; one that doesn't is noise.

## Mode routing

Strip `mode:` tokens from `$ARGUMENTS` before treating the remainder as context/scope.

| Mode | Trigger | What it does |
|------|---------|--------------|
| **Compound** (default) | none | Document one solved problem → `docs/solutions/` |
| **Vocabulary capture** | a durable, reusable *project* term/concept surfaces | Reconcile the repo-root `CONCEPTS.md` (one definition per concept) — read `references/concepts.md` |
| **Memory handoff** | a fact about the *user / preferences / cross-project context* surfaces | Invoke `memory-update`; that skill writes auto-memory |
| **Refresh** | `mode:refresh [scope]` | Maintain existing `docs/solutions/` docs — read `references/refresh.md` |
| **Headless** | `mode:headless` | Non-interactive overlay on whichever mode is active |

The repo-vs-user fork is the routing decision: a repo-scoped engineering lesson → Compound (this skill writes the doc); a user/preference/cross-project fact → Memory handoff (`memory-update` writes it). Within the repo-scoped side there's a second fork: a solved problem → Compound (a learning doc); a durable project term whose meaning isn't obvious → Vocabulary capture (a `CONCEPTS.md` entry). One run can do all three — write a learning doc, reconcile a concept, and hand a preference fact to `memory-update`.

## Support files — read on demand

Don't bulk-load these at start. Read each at the step that needs it; pass the relevant content into any subagent you spawn.

- `references/schema.md` — frontmatter contract: bug/knowledge tracks, enums, category map, YAML safety. Read when classifying and validating.
- `references/refresh.md` — the whole refresh model and phases. Read only in `mode:refresh`.
- `references/concepts.md` — `CONCEPTS.md` entry schema and the one-definition-per-concept reconciliation/refresh rules. Read in Vocabulary capture and when refreshing `CONCEPTS.md`.
- `assets/solution-template.md` — section structure for a new doc. Read when assembling.
- `scripts/validate-frontmatter.py` — the one runnable check. Run on every written/edited doc.

---

# Mode 1 — Compound (default)

**The deliverable is ONE file: the final learning doc.** Research subagents return text to you; they do not write. Only the orchestrator writes.

### Phase 0.5 — Auto-memory scan

Before research, scan the injected auto-memory block (a "user's auto-memory" block in the system prompt) for entries related to the problem. If the block is absent or empty, skip. If relevant entries exist, carry them as a labeled **supplementary** context block:

```
## Supplementary notes from auto memory
Treat as additional context, not primary evidence. Conversation history and
codebase findings take priority.
[relevant entries]
```

Pass it to the research subagents. Tag any memory-derived line that lands in the final doc with `(auto memory [claude])`. Memory is supplementary — codebase and conversation win every tie.

### Phase 1 — Research (parallel, read-only)

Dispatch three subagents in parallel. Each **returns text and writes nothing** — no Write, no Edit, no files:

1. **Context Analyzer** — reads `references/schema.md`; from the problem decides the track (bug vs knowledge), the `problem_type`, the category directory, and a slug filename (`[sanitized-problem-slug].md`, no date suffix). Returns a frontmatter skeleton (including `category:`) and which track applies. Does not invent enum values or fields.
2. **Solution Extractor** — extracts the substance from the conversation, folding in the auto-memory excerpt as supplementary evidence. Bug track: Problem, Symptoms, What Didn't Work, Solution (with code), Why This Works, Prevention. Knowledge track: Context, Guidance, Why This Matters, When to Apply, Examples.
3. **Related-Docs Finder** — greps `docs/solutions/` (`title:`, `tags:`, `module:`, `component:` on extracted keywords; narrow to the candidate subdirectory when known), reads only frontmatter of candidates, fully reads only strong matches. **Scores overlap** across problem statement, root cause, solution approach, referenced files, prevention rules: High (4–5 dimensions), Moderate (2–3), Low (0–1). Returns links and the overlap verdict.

Wait for all three before assembling.

### Phase 2 — Assemble and write

1. **Overlap gate** (from Related-Docs Finder):

   | Overlap | Action |
   |---------|--------|
   | **High** (4–5) | Update the existing doc, don't create a duplicate. Keep its path and frontmatter; add `last_updated: YYYY-MM-DD`. |
   | **Moderate** (2–3) | Create normally; note it as a refresh/consolidation candidate. |
   | **Low / none** | Create normally. |

   This is the gate's filter 2 made concrete — a duplicate is drift.
2. Read `assets/solution-template.md`; assemble the doc with the track's section structure.
3. Frontmatter per `references/schema.md`; apply the YAML-safety quoting rule to array items.
4. `mkdir -p docs/solutions/<category>/`, write `docs/solutions/<category>/<slug>.md`.
5. **Validate:** `python3 scripts/validate-frontmatter.py <path>`. Exit 0 = parser-safe; exit 1 names the offending field. Quote, re-write, re-run until 0. Don't declare success while it fails.
6. **Read the file back** to confirm it landed as intended.
7. **Concept reconciliation (optional, when warranted).** If the run surfaced a durable project term that clears the reject-by-default gate, reconcile `CONCEPTS.md` in the same run per Mode 4 — one definition per concept, refresh on drift, no duplicate. The solution doc is still the deliverable; a concept entry is an additional write, not a substitute. Read `references/concepts.md` before writing it.

### Phase 2.5 — Refresh check (selective, not automatic)

Refresh is not a default follow-up. Suggest or invoke `mode:refresh` with a narrow scope only when the new fix contradicts or supersedes an older doc, the work was a refactor/migration/rename/dependency-bump that likely invalidated references, or the Related-Docs Finder surfaced strong refresh candidates or moderate overlap (consolidation opportunity). Otherwise don't. Capture the new learning first; refresh is targeted maintenance after.

---

# Mode 4 — Concepts capture

`CONCEPTS.md` at the operating repo root is the shared-vocabulary glossary: the words that mean something precise in *this* codebase, one definition per concept. autolearn owns this surface — one writer, no second skill edits it. **Read `references/concepts.md`** for the entry schema and reconciliation rules before writing.

**When it fires.** A durable project term surfaces — in a learning capture (accretion), or because the user named a concept worth pinning. It must clear the reject-by-default gate above (would-forget / not-already-defined / scope-qualified to this project). General programming and domain English never qualify.

**Reconcile, don't append blindly:**
1. Locate `CONCEPTS.md` at the repo root: `fd -g 'CONCEPTS.md' --max-depth 2`. Absent + a term clears the gate → create it. Absent + nothing clears → write nothing; never scaffold an empty file.
2. Search it for the term and its synonyms: `git grep -ni '<term>' CONCEPTS.md`. **One definition per concept:** a hit means the concept already exists — refresh it on drift, never add a second entry.
3. New term → add one entry: a one-sentence definition of what it means here and what distinguishes it from neighbors; a second paragraph only for non-obvious behavioral rules. Retire synonyms as an `*Avoid:*` aliases line. No file paths, dates, owners, or version-specific claims — the file stands on its own.
4. **Read the file back** to confirm the merge landed and created no duplicate heading.

**Refresh loop.** `autolearn mode:refresh [scope]` maintains `CONCEPTS.md` alongside `docs/solutions/`: re-derive each in-scope definition against current code, refresh drifted ones, de-duplicate, delete a concept whose domain is gone. Per-concept rules in `references/concepts.md`.

---

# Mode 2 — Memory handoff

A fact about *the user, their preferences, or cross-project context* is **not** a repo learning. Do not write it into `docs/solutions/`, and never write `memory/` or `MEMORY.md` yourself. Invoke the `memory-update` skill and hand it the fact — `memory-update` owns and writes the entire auto-memory surface, with its own frontmatter schema and per-proposal confirmation. One writer, no MEMORY.md race.

Hand off when the lesson is: a stable user preference or working style, who the user is or their goals, an external-system pointer, or a fact that holds across repos. Keep in Compound when the lesson is a repo-specific engineering fix or pattern.

---

# Mode 3 — Refresh

`autolearn mode:refresh [scope]` maintains existing `docs/solutions/` docs as code evolves. **Read `references/refresh.md`** and follow it — the five-outcome model (Keep / Update / Consolidate / Replace / Delete), scope routing, investigation phases, per-action flows, the headless `status: stale` variant, and the report format all live there. Prefer no-write Keep; match docs to reality; delete, don't archive.

Refresh also maintains the repo-root `CONCEPTS.md` when it falls in scope: re-derive definitions against current code, refresh drifted ones, de-duplicate entries that name the same concept, delete a concept whose domain is gone. The per-concept refresh rules are in `references/concepts.md`.

---

## Commits

One learning per commit. ODIN `Op:` trailer in the body:

- **New doc** → `Op: extend` (a load-bearing capability added to the doc set).
- **Refresh a drifted doc** → `Op: correct` + `Restores:` citing what fell out of sync (`ref:<commit> | spec:<invariant>`).
- **Delete / Consolidate-away a doc** → `Op: purge` + `Removes:` citing what went (`path:<ref> | surface:<name>`).

`CONCEPTS.md` writes follow the same trailers: a new entry → `extend`; a refreshed definition → `correct`; a deleted or de-duplicated concept → `purge`.

Stage only the surfaces autolearn wrote or edited — a solution doc, `CONCEPTS.md`, or both — never other dirty files; commit and publish by the operating repo's normal flow.

## Disambiguation

- **vs `memory-update`** — `memory-update` scans *past session transcripts* and writes *auto-memory only*. `autolearn` compounds the *current* solved problem into *in-repo* `docs/solutions/` and refreshes those docs; it delegates user/preference facts back to `memory-update`.
- **vs `init`** — `init` builds `AGENTS.md` from codebase analysis (conventions to prime future agents). `autolearn` captures one solved problem as a retrievable learning, and defines durable project terms in `CONCEPTS.md` (the shared-vocabulary glossary, not the agent-priming doc).
- **vs `sync-docs`** — `sync-docs` corrects public docs/examples/versions against a code diff (docs↔code drift). `autolearn` writes net-new knowledge docs and maintains the knowledge set.

## Operating surface

`autolearn` writes exactly two in-repo surfaces: the operating repo's `docs/solutions/` and the repo-root `CONCEPTS.md`. It owns both — one writer per surface, no second skill edits them. All auto-memory writes are delegated to `memory-update`. No writes to undefined or doubly-owned locations.

Adapted from EveryInc/compound-engineering-plugin (MIT).
