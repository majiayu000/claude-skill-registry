---
name: own
description: Use when the user asks for a debrief on recent work, wants to check what they actually own versus what AI carried, or asks to be quizzed on their codebase. Triggers on "debrief", "what do I own", "own this", "quiz me on the code". User-invoked only — never self-trigger from context.
---

Probe the human's understanding of their own codebase so they keep the capacity to own what they ship. A debrief is a conversation, not a score.

## Principles

- The ledger is the baseline, never git history — a commit SHA points into history other people rewrite; the ledger is append-only and owned.
- The human's attention is the constraint: 4 questions per debrief, regardless of ledger size.
- Deterministic work belongs to deterministic tools (jq/date); judgment work to the model.
- Questions come from understood code — callers, invariants, neighbors — never from raw diff hunks. The survey IS the context retrieval.
- A concept that can't be found in current code is asked about, never silently recorded as gone.

## Invisibility (load-bearing)

- Never surface due dates, streaks, mastery labels, or any interval-derived signal. The moment one leaks, the schedule stops measuring forgetting and starts manufacturing performance — and reverts to a fixed staleness window.
- k, interval, priority, assisted/owned status: scheduling internals, model-facing only.

## Ledger

Location: `~/.claude/hope/own/<project-slug>/ledger.json` — hope-owned namespace, never the harness project directory (plugin data must not depend on harness layout or transcript retention). Document shape: `ledger.schema.json`.

Slug source, in order:

| Source | Slug |
|--------|------|
| origin remote URL | strip scheme, user, `.git` — e.g. `github.com-saadshahd-moo.md` |
| no remote | main checkout path via `dirname $(git rev-parse --path-format=absolute --git-common-dir)`, normalized |

- Remote-first: every worktree AND every clone of one repo resolves to one ledger — understanding is project-scoped, not checkout-scoped.
- Adoption rule: remote-slug ledger missing but a path-slug ledger exists (remote added after first debrief) → move it and say so.
- Known defect: a changed remote host (e.g. github→gitlab) yields a new slug and orphans the old ledger — adoption covers add-remote, not change-remote; recover by manual rename.

Rules:

- ALL ledger I/O is mechanical, never mental: reads (ranking, folds) and writes (appends, merges) run as `jq`/`date` one-liners. The model never hand-computes a timestamp and never hand-types ledger JSON content.
- Writes go `jq … ledger.json > tmp && mv` — atomic, last-writer-wins; acceptable because debriefs are single-user and user-invoked.
- Events are append-only — never edited or deleted. No status field is ever stored; assisted/owned is derived at read time.
- One `debriefId` per run, stamped on every event the run writes — distinct-debrief counts are exact `group_by(.debriefId)`, never timestamp clustering.
- Probe question text is stored verbatim — the audit trail that each re-probe is a genuine transformation, never a rephrase.
- Concept name + one-line description only — no volatile code references. A concept that can't be re-located from its description has a bad description.
- Concepts are named in the project's language. Fresh extractions fuzzy-match existing entries (tombstones included); a match reuses the canonical entry.

### Merges

Fuzzy matching is nondeterministic — near-duplicates WILL appear across debriefs. Repair path:

- Events move to the canonical entry intact (original debriefIds, timestamps, question text).
- The duplicate becomes a tombstone `{name, mergedInto, timestamp}`; future fuzzy matches resolve through tombstones in one hop.
- A merge is proposed in one line and user-confirmed — never silent. At most one proposal per debrief.

## Workflow

### Step 1: Locate ledger

Derive the slug, apply the adoption rule — announce any adoption move. Cold start: no ledger → survey from the merge-base with the default branch; the user may override.

### Step 2: Survey

Characterize-first, budget-scoped — scoped by the question budget, never the repo:

1. Re-verify the sampled ledger concepts against current code: present / changed / gone. A "changed" verdict is recorded as an event (it resets the schedule — prior passes no longer attest to current code). Can't find it → ask the user; never silently record gone.
2. Then look for new work.

**Diff hint** — `git diff <last-debrief-commit>..HEAD` is a locator hint only, trusted iff BOTH: (a) the last debrief's commit exists, (b) it is an ancestor of HEAD. Either check fails → drop the hint, say so, proceed ledger-only. The hint may speed the survey; it never decides a verdict.

**New work** is the reachability delta, not a timestamp guess:

| Last debrief commit | New-work source |
|---------------------|-----------------|
| exists AND ancestor of HEAD | `git log <last>..HEAD` — catches squash merges and late-merged branches any date filter misses |
| checks fail (history rewritten) | `git log --since-as-filter=<last-debrief-timestamp>` — announce the fallback when taken |

`--since-as-filter`, never plain `--since` — plain `--since` stops traversal at the first old commit and silently drops out-of-order ones. Committer dates, so rebased work re-enters the pool.

Residual hole, stated not hidden: under the date fallback, a true-merge of a branch whose commits predate the last debrief escapes the filter. The characterize-first survey is the backstop — those concepts surface when ledger entries are re-verified against current code.

### Step 3: Rank and sample

Append new-work concepts (name, description, empty events) mechanically, then run the shipped filter — read its output, never re-derive it:

```
jq -f rank.jq --argjson now "$(date +%s)" ledger.json
```

Fixed budget — 4 questions:

| Slot | Count | Picks |
|------|-------|-------|
| priority | 2 | highest elapsed ÷ interval; fresh new work always wins |
| review | 1 | highest-priority concept with exactly one passed transformed question and no fail or "changed" since — its next pass promotes to owned; none eligible → falls back to priority |
| long-tail | 1 | oldest-probed concept, so nothing decays silently forever |

The review slot is what keeps owned reachable on an active repo — without it, perpetual new work monopolizes priority and owned would crawl. No concept fills two slots.

Decay: a fail steps the schedule back one level (halves the interval, never resets it); a "changed" verdict resets it — the code moved, the human's grasp didn't slip. Mechanics live in `rank.jq`.

State sampling aloud: "covered N of M".

### Step 4: Probe

- One transformed question per sampled concept — a genuine transformation of the stored prior question, never a rephrase.
- Runnable checks execute read-only commands only; anything state-mutating falls back to a stated reveal.
- Append each event mechanically: jq one-liner, `date -u` timestamp, atomic write.

### Step 5: Close

- At most ONE fail card — the most central failed concept; other fails record silently and re-probe later.
- At most ONE reveal — the single most surprising consequence among everything passed this run. One card in, one card out — never a homework list.
- At most one merge proposal (one line, user-confirmed).
- assisted → owned: passed transformed questions in two DISTINCT debriefs — `[events | select(.outcome=="pass") | .debriefId] | unique | length >= 2` — so two passes in one run never promote. A single result never flips state in either direction.

## Grader is the examiner

The model writes the transformed question, judges it a genuine transformation, and grades the answer. Stored question text makes this auditable, not audited. Invisibility bounds the blast radius — a bad grade mis-prioritizes sampling, gates nothing. Stated here so it is never implied away.

## Boundaries

- own measures understanding — it never gates, blocks, or scores work.
- The ledger is allowed persistent state ONLY because it (1) describes the human's understanding, (2) is user-owned, (3) lives outside the repo, (4) is never surfaced. Drop any qualifier and it is an anti-pattern again.
