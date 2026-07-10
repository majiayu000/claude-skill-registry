---
name: setup
description: Use when installing, refreshing, or re-tuning sound taste rules in a project. Triggers on "sound setup", "install taste rules", "scaffold .claude/rules", "set up sound here", starting work in a repo with no .claude/rules/, or a taste-not-defined nudge. Also use to re-run after a stack change (new framework, new package in a monorepo).
---

# sound:setup

Scaffold a project's `.claude/rules/` from the sound corpus: probe the repo's stack, select ONLY the rules whose subject the repo's code actually shows — evidence-cited per rule, never a tag-wide dump — confirm with the user, then install with repo-tuned `paths` globs and examples rewritten in the project's own domain. Once written, the files belong to the user; re-runs reconcile against what exists (see Re-runs).

Corpus location: `../../corpus/` relative to this SKILL.md. If it is missing or unreadable, STOP and say so — never install a partial set silently.

## Phase 1 — Probe

Goal: decide which kind-tags apply. Tags are a PRE-FILTER for Phase 2 candidacy, not the selection.

**Usage evidence decides — manifest presence only tells you where to look.** A dep can be dead weight, hoisted, or tooling-only. For every manifest hint, verify in source before proposing the tag. Negatives need the same rigor: a client's config/wrapper file alone never clears a dep — search the client's USE sites (`.publish(`, `.send(`, `.create(`…) across the repo before ruling a tag out; a cache-shaped wrapper can still be published through elsewhere.

Method: read every `package.json` (root + workspaces) and workspace markers (`pnpm-workspace.yaml`, `turbo.json`) → hypothesis list. Then verify each hypothesis against source. While there, also record: source extensions actually written (`.ts`/`.tsx`/`.js`/`.jsx`/`.mts`), the real test-file convention — read the test RUNNER'S config (vitest/jest include patterns, ava files) when one exists, since it's authoritative over filename guessing and settles which suffixes belong to unit tests vs e2e — and which workspace package each piece of evidence lives in.

| Tag | Fires on (verified usage) | Does NOT fire on |
|---|---|---|
| `react` | `.tsx`/`.jsx` files, JSX or react imports in real source | react in deps with zero usage; react-shaped tooling (ink absent too) |
| `db` | db client/ORM imported in source (prisma, drizzle, pg, kysely, mongoose, neo4j, clickhouse, redis-as-store…); EMBEDDED dbs with owned DDL/schema (sqlite, node:sqlite, level); owned schema/migration files | consuming someone else's hosted API without owning storage |
| `distributed` | any SIDE-EFFECTFUL remote boundary: payments (stripe), email/SMS (nodemailer, twilio), queue/broker publish (kafkajs, bullmq, amqplib, redis `.publish()`), webhook handlers, bot messaging SDKs, multiple owned services reconciling state. Publisher-side evidence alone is SUFFICIENT — the consumer usually lives outside the repo; requiring an in-repo consumer would blind the tag on exactly the topology it exists for | READ-ONLY consumption of remote APIs (fetch-and-render); analytics beacons; redis as a plain same-process cache (get/set/del only) |

## Phase 2 — Select (per rule, evidence-cited)

Candidates = every corpus rule whose `when:` is `always` or shares ANY tag with the Phase 1 tag set. Candidacy is where the tag filter's job ENDS.

A candidate installs iff the repo contains the SUBJECT-SURFACE the rule governs — code where the rule's `Detect:` question is askable — cited as at least one concrete file path. The rule's `Not-when:` can veto. No citation, no install. An actual violation is NOT required (rules are prevention; they should arrive before the first sin) and its absence is never a veto.

- Subject-bearing rule: `command-vs-fact-when-reconciled-elsewhere` installs iff the repo has async-reconciled state (a server ack, a queue, a webhook-confirmed flow) — cite the file. A repo that names no events and sends no commands does NOT get the event-naming rules.
- Universal-subject rule (its subject is "any code": naming, transformation shape, comments, function design): passes trivially — cite any substantive source file. Never manufacture deeper evidence for these.
- Test-scoped rule: its subject-surface is the CODE UNDER TEST, never test-file presence — a zero-test repo with testable logic still earns the general testing rules (cite the testable code; the test glob fires the moment the first test file is written). Test rules with a more specific shape (roundtrip laws need encode/decode pairs; property generators need domain invariants) still need THAT shape cited.
- Every rejected candidate gets a one-line reason (surfaced at Confirm); rejection reasons are how the user audits the judgment.

Method — this analysis is DEEP by design; spend the tokens: partition the candidates into batches of rules that would look at the same code (seed the grouping with when-tags and each rule's subject; batch composition is a means, not a contract). Dispatch one subagent per batch with its rules' full text and repo access; each returns per-rule `install + citation` or `skip + reason`. In propose-only mode the selection may run inline instead — the output set is what's judged, not the mechanism.

## Phase 3 — Tune paths

Principle: **a rule's glob must be able to fire before its Detect moment.** `.claude/rules/` has two loading modes — `paths:` files inject on Read/Edit of a matching file; pathless files load at session launch. A glob that can never match this repo's files is a silently-dead rule; a glob that only matches files edited AFTER the violation moment is worse.

1. **Extensions** — repo writes SUBSTANTIVE source in `.js`/`.jsx`/`.mts` too? Widen `{ts,tsx}` to match. Tooling config files alone (`tailwind.config.js`, `eslint.config.js`…) do NOT widen — the rules target code the team writes, not scaffolding. Pure-TS repos keep corpus defaults. The react-class glob covers JSX-BEARING extensions ONLY: `{tsx,jsx}` (or `.js` where the repo writes JSX inside `.js`) — never `.ts`. WRONG: `frontend/**/*.{ts,tsx}`. RIGHT: `frontend/**/*.{tsx,jsx}`.
2. **Test convention** — replace the `**/*.{test,spec}.{ts,tsx}` class with the repo's real convention, expressed as the SUFFIX pattern alone, repo-wide (`**/*.test.ts`) — do NOT directory-scope it just because tests happen to sit in one dir (rule 4 applies here too). Directory-scope only when the convention has no suffix at all (ava-style bare `test/**/*.js`) or the suffix would match real non-test files. Include only the suffix arms the repo's unit tests actually use: if `.spec.ts` files exist but belong to a different runner (Playwright e2e), they stay OUT of the test class.
3. **Monorepo scoping (kind-tagged rules only)** — scoping units are WORKSPACE PACKAGES (declared in `pnpm-workspace.yaml`/workspaces field), never directories; in a single-package repo there is nothing to scope — kind globs stay repo-wide and no per-tag glob keys exist (rule 4). In a workspace repo, SCOPED is the default: scope each tag's glob to the packages carrying that tag's evidence (`apps/web/**/*.{tsx,jsx}`). Leave it repo-wide only when the evidence genuinely spans most packages — incidental references elsewhere (a type reused by the frontend, an import in a script) do NOT unscope. WRONG: distributed evidence in one app of a workspace, glob `**/*.{ts,js}`. RIGHT: `apps/worker/**/*.ts`. `always` rules stay repo-wide.
4. **No other narrowing** — never tighten to `src/**` in single-package repos. Unmatched `paths` files cost nothing; narrowing only buys miss-risk.
5. **Pathless pair** — `red-green-refactor-is-a-commit-shape` and `tidy-or-behavior-never-both` Detect on COMMIT shape, which no edit-glob reaches: strip their `paths` key entirely so they load at launch. (They still pass through Phase 2 selection like any candidate.)

## Phase 4 — Confirm (never skip, never auto-install)

Present to the user, compactly: the extracted facts (each with its file evidence), the proposed tag set, the proposed rule set — each rule with its citation — the rejected candidates grouped with their one-line reasons, and the proposed glob tunings from Phase 3. Ask for confirmation or correction. The user's answer is the verdict — a corrected tag set or rule set replaces yours without argument; redo the affected phases with it. Only write after explicit confirmation. The user confirms the SET here; tuned example bodies are Phase 5–6 output they own afterward.

**Propose-only mode:** when the invocation asks for a proposal only (evals, dry runs), emit exactly this JSON and stop — no confirmation, no tuning, no writes:

```json
{"facts": ["<evidence with file paths>"], "tags": ["react"], "globs": {"default": "**/*.{ts,tsx}", "test": "**/*.{test,spec}.{ts,tsx}", "react": "**/*.{tsx,jsx}"}, "rules": [{"name": "<corpus-rule-name>", "cite": "<repo file path>"}]}
```

`tags` contains ONLY kind-tags from {react, db, distributed} — `always` is not a tag, it's the unconditional candidacy baseline; listing it is an error. `rules` lists ONLY the install set: every selected rule's corpus filename (no `.md`) with one citation path that exists in the repo; skips are not emitted. The pathless pair, when selected, appears in `rules` like any other.

`globs` keys: `default` and `test` always (they cover the `always` rules); `react` REQUIRED whenever the react tag fires (its rules ship a distinct glob class — omitting the key breaks them) and absent otherwise; plus one key per kind-tag ONLY when monorepo scoping makes its glob differ from `default` (e.g. `"db": "services/api/**/*.ts"`) — a per-tag key repeating the default glob is noise. Every value is the TUNED glob.

## Phase 5 — Tune examples (confirmed set only)

Rewrite each confirmed rule's fenced WRONG/RIGHT code in the project's own domain — its real nouns, types, and naming style — as PLAUSIBLE project code, never a verbatim quote of an existing violation. ALL prose is byte-preserved: statement, `_Avoid_`, `Detect:`, `Not-when:`, `Cross-ref:` stay corpus-verbatim — the examples localize, the law does not. Batch the work across subagents as in Phase 2.

Mechanical gates per tuned rule — any gate fails → keep the corpus example for that rule and say so; never install code that flunks a gate:

1. **Syntax-valid TS** — the fenced code parses (`tsc --noEmit`-clean at the syntax level; unresolved project names are tolerated, snippets don't carry imports).
2. **De-genericized** — no stock corpus nouns (`Order`, `Invoice`, `OrderStatus`, `Payment`, `Cart`…) unless that noun greps in the repo's own source (then it IS the domain).
3. **Grounded** — at least one identifier in the tuned example greps to a real identifier in the repo.

## Phase 6 — Write

For each confirmed rule, write `.claude/rules/<rule-name>.md`: tuned body from Phase 5; frontmatter = the tuned `paths` line ONLY — no `when:`, no `source:`. The pathless pair gets no frontmatter at all. No marker, manifest, or hash.

Which glob each rule gets — by its corpus glob class, never ad hoc: rules shipping the test class → tuned `test`; react-tagged rules → tuned `react`; other kind-tagged rules → their tag's scoped glob when one exists, else `default`; `always` rules → `default`; a multi-kind rule → all of its tags' globs.

## Re-runs (reconcile, never overwrite)

`.claude/rules/` may already hold files — from a previous setup, hand-written, or evolved past what setup wrote. Every existing file is user-owned; reconcile by reading, not bookkeeping. Installed examples are tuned BY DESIGN, so whole-body comparison is meaningless — compare PROSE ONLY: body minus fenced code blocks minus frontmatter, whitespace-normalized.

- **Existing file, no same-named corpus rule** → local taste. Leave untouched; mention only that it was preserved.
- **Selected corpus rule, no existing file** → propose as an addition. This is how the install GROWS as the codebase evolves: every re-run re-derives tags and re-runs selection fresh — a surface that newly appeared makes its rules newly proposable. No memory of prior runs.
- **Both exist, prose identical** → in-sync. At most propose a `paths` re-tune if the repo changed. NEVER regenerate its examples — once written they are the user's, whether setup tuned them or the user edited them; re-tune examples only when the user explicitly asks.
- **Both exist, prose differs** → the user evolved the rule or the corpus moved since install — you cannot tell which, so show the prose diff and ask: keep theirs, take the corpus version, or keep both (theirs renamed as a local rule). Never silently overwrite.

Present the whole reconciliation as ONE compact proposal (additions / updates / preserved) and write only what the user confirms.

## Failure modes to keep loud

- Corpus unreachable / rule file unparseable → stop before writing anything.
- User declines all tags → Phase 2 still runs over the `always` candidates; say that's what happened.
- Repo has no JS/TS at all → the corpus doesn't apply; say so and install nothing.
- A selected rule with no citable evidence is a selection BUG — drop it and say so, never install on vibes.
