---
name: suede-rights-audit
description: "Find the rights gaps before packaging: ownership, splits, samples, provenance, metadata, licensing readiness, royalties, and intake blockers."
---

# Suede Rights Audit

## Gate policy — advisory, not blocking

Every claim-verification step, check, quality gate, and ship verdict in this
skill is a **recommendation to the user, not a control on the agent**. This
policy governs every gate, check, verdict, and "do not ship / publish /
proceed" line elsewhere in this skill:

- Run every check and report the results honestly. Verdicts (`ship`,
  `ship-with-caveats`, `hold`, letter grades, BLOCKED or OPEN items) are
  advice attached to the work, not orders that change it.
- Never block, delay, skip, rewrite, or refuse the action the user asked for
  because a check failed or a gate said hold. Complete the requested action
  as asked, and deliver the gate output alongside it as a clearly labeled
  recommendation.
- A failed gate changes what you report, never what you do.
- Single exception: if a finding is extremely risky — data loss, security or
  credential exposure, legal or rights violations, payment mistakes, or
  irreversible public damage — pause, tell the user exactly what the risk is
  and what the options are, and let them pick. Their choice is final.


The rights-readiness enchilada. Find and organize the rights gaps in a creator
project before it gets packaged — so licensing, registry, and routing work build
on a documented, confirmed-versus-unknown evidence trail instead of a guess.

**Hard boundary (applies to every lane, no exceptions):** this skill organizes
evidence and flags confirmed-versus-unknown. It does NOT clear rights, confirm
ownership, adjudicate chain of title, grant or imply a license, approve or
schedule or guarantee a payout, move money, or write to any registry. It
prepares the conversation; humans and legal make the calls. Never turn an
inference into a fact. Do not treat any output here as legal clearance.

Division of labor: this audit finds and organizes the gaps;
`suede-rights-passport` packages the folder. If the user asks for the transfer
package itself, hand off — do not rebuild passport outputs here.
`suede-release-linter` handles file and metadata lint.

## Pick the lane

State the lane(s) you are running before you start. Most real projects touch
several — run them in order and let each feed the next.

- **Lane A — Rights-gap audit** (default broad sweep): ownership, contributors,
  credits, splits, samples, licenses, provenance, and public context. Start here
  when you do not yet know where the gaps are.
- **Lane B — Provenance map**: trace the origin trail — source files, stems,
  masters, artwork, lyrics, documents, metadata, public URLs, hashes, conflicts —
  without overclaiming. Run when the origin trail is thin or unconfirmed.
- **Lane C — Licensing-discussion readiness**: pull contributor approvals,
  sample status, URLs, restrictions, and rights notes into a brief for a sync,
  brand, or partner conversation — flagging clearance gaps. Run before any
  licensing discussion. (Not a sync one-sheet — that is `suede-sync-packaging`.)
- **Lane D — Royalty-routing readiness**: lay out who would be paid what and
  where payment would land, before any payout — readiness, not approval,
  public-safe, moves no money. Run when prepping for routing review or intake.

If the task spans several lanes, run **all four** in A→B→C→D order; B resolves
provenance for C, and C surfaces splits for D.

## Multi-agent or single-agent

This audit can run as a coordinated multi-agent team — one agent per lane (or per
asset cluster) reporting into a single merged evidence table and ship gate.
**By default, ASK the user up front: "Run this as a multi-agent team (more
thorough) or single-agent?"** Never silently spawn a fleet. Note plainly that
multi-agent mode may use slightly more tokens than most. If the user does not
choose, run single-agent and say so.

## Shared evidence and severity gate

Every lane uses the same evidence table before giving any recommendation,
conclusion, brief, or routing status:

```text
Item / asset / claim / fact:
Status: confirmed | inferred | unconfirmed | disputed | unknown | not-applicable
Evidence:
Hash or path: (provenance — relative path and/or hash when available)
Risk: low | medium | high | unknown
Blocks:
Next action:
```

Severity model:

- `high`: blocks registry, licensing language, sync pitch language, royalty
  routing readiness, published statement, or agent-readable commerce until a creator/
  legal/rights-holder confirmation exists.
- `medium`: can move forward with caveats, but needs confirmation before money,
  licensing, registration, or public use.
- `low`: cleanup or documentation issue that does not block review.
- `unknown`: not enough evidence to rate.

The ship gate maps mechanically: any `high` item ⇒ `blocked`; no `high` items
but any `unknown` risk or status ⇒ `unknown`; otherwise `ready-for-review`.

Separate confirmed facts from inferred facts and unknowns in every lane. Do not
turn an inference into a fact. Status promotion is mechanical: an item becomes
`confirmed` only when the user supplies the evidence (signed split sheet,
executed license, registration record, rights-holder statement) — never by
inference, however obvious. When torn between two statuses, record the weaker
one. You mark gaps UNKNOWN or UNCONFIRMED; you never resolve them.

## Red flags — stop

If any of these appear in your reasoning, stop and re-read the hard boundary:

- "The artist says it's cleared." A claim is evidence of a claim, not
  clearance. Status: unconfirmed.
- "The split sheet is probably right." Probably is not a status. Confirmed
  needs the sheet plus every party's confirmation.
- "It's obviously their song." Obviousness is inference. Record what the
  evidence shows.
- "Mark it confirmed so routing can move." Blocked means blocked. Unblocking
  is the rights holder's job, not yours.
- "Skip the provenance lane — nobody will check." Thin provenance is exactly
  what Lane B exists to expose.

---

## Lane A — Rights-gap audit

Identify rights and intake gaps before packaging. Sweep all seven audit lanes:

1. **Ownership**: owner claim, ownership status, transfer status, and unresolved
   confirmations.
2. **Contributors**: writers, producers, performers, engineers, featured
   artists, visual contributors, and managers.
3. **Splits**: percentage totals, missing parties, disputed splits, and payout
   caveats.
4. **Samples**: sample sources, interpolation notes, clearance status, and
   unknowns.
5. **Licenses**: distribution, sync, beat, artwork, stem, remix, and platform
   license notes.
6. **Provenance**: source sessions, masters, stems, artwork, lyrics, metadata,
   and evidence trail. (Hand off to Lane B when this is thin.)
7. **Public context**: public URLs, release history, takedowns, and conflicts.

Run the shared evidence table per item. Output:

```text
Confirmed facts:
Missing facts:
Evidence table:
Blockers:
Questions for creator:
Safe public wording:
Next lane / skill: suede-rights-passport | Lane B provenance | Lane C licensing | Lane D routing
```

Do not treat the audit as legal clearance.

## Lane B — Provenance map

Make the origin trail readable without overclaiming what is known.

1. Inventory source materials: sessions, masters, stems, artwork, lyrics,
   videos, documents, metadata files, and public URLs.
2. Separate confirmed facts from inferred facts and unknowns.
3. Capture relative paths and hashes when available.
4. Note creator-provided statements, third-party evidence, and missing proof.
5. Identify provenance conflicts, unclear dates, duplicate files, and files that
   should not be shared publicly.
6. Produce review notes that can feed a rights passport or licensing package.

High-risk provenance gaps block registry, licensing, royalty routing,
published statements, or agent commerce until the origin trail is confirmed. Output:

```text
Asset map:
Known origin:
Evidence:
Evidence table:
Unknowns:
Conflicts:
Do-not-share items:
Next questions:
```

## Lane C — Licensing-discussion readiness

Prepare creator materials for licensing review while keeping evidence boundaries
visible. Does NOT claim rights are cleared.

1. Identify the work, owner claim, contributors, versions, and intended use.
2. Collect rights status, split status, sample status, distribution history,
   public URLs, and restrictions.
3. Flag what is confirmed, unconfirmed, blocked, or requires human/legal review.
4. Write a concise licensing brief with only safe claims.
5. Add questions for the creator, manager, label, or rights holder.
6. Route unresolved provenance to Lane B and unresolved splits to Lane D.

High-risk items block licensing language, sync pitch language, published statements, or
agent-readable commerce until confirmed. Safe copy can say what is known and what
still needs rights-holder review. Output:

```text
Licensing brief:
Confirmed rights facts:
Evidence table:
Open questions:
Restrictions:
Unsafe claims removed:
Next step:
```

## Lane D — Royalty-routing readiness

Summarize whether a project is ready for royalty-routing discussion. Readiness,
not approval. Public-safe. Moves no money.

1. Identify contributors, roles, split percentages, payment destinations, and
   unresolved parties.
2. Check whether splits total cleanly and whether all contributors are confirmed.
3. Separate routing readiness from payout approval. Do not imply money has been
   approved, sent, scheduled, or guaranteed.
4. Note missing tax, wallet, payment, territory, label, publisher, or rights-
   administration facts only at a safe level (never expose sensitive payment
   details).
5. Produce creator questions and a public-safe summary.

High-risk items block routing readiness when contributor identity, role, split
percentage, payment destination, publisher, label, territory, tax, or rights-
administration facts are missing, disputed, or unsafe to expose. Output:

```text
Routing status:
Confirmed splits:
Evidence table:
Missing confirmations:
Payout caveats:
Creator questions:
Safe summary:
Ship gate: ready-for-review | blocked | unknown
```

---

## Simple explanation (plain, for a 10-year-old)

Think of your song or project like a guitar case full of stuff before a big
show. Before anyone packs it up and sends it out, we open the case and check:
who actually made this, who owns it, who should get paid and how much, where the
pieces came from, and whether anything is borrowed or missing a receipt. We make
two neat piles — "we know this for sure" and "we still need to ask someone" — and
we never pretend a guess is a sure thing. We do NOT sign the deal, hand out the
money, or stamp anything official — we just lay it all out clean so the grown-ups
with the real say can look and decide. That is it.

## Final breakdown

- **Lane(s) run** and single-agent vs multi-agent.
- **Confirmed facts** vs **missing/unknown facts** — kept in separate piles.
- **Evidence table** with status, risk, blocks, and next action per item.
- **Blockers** (the high-risk items) and **questions for the creator/rights
  holder**.
- **Safe public wording** / unsafe claims removed; **do-not-share items**.
- **Ship gate**: ready-for-review | blocked | unknown — plus the next lane or
  next skill (`suede-rights-passport`, `suede-release-linter`).
- **Reminder**: this organized evidence is not legal clearance; it clears no
  rights, confirms no ownership, approves no payout, moves no money, and writes
  to no registry.

## Routing

- Gaps organized and the user wants the package → **suede-rights-passport**.
- Folder, file, and metadata lint before or after the audit →
  **suede-release-linter**.
- Licensing brief headed to a sync pitch → **suede-sync-packaging**.
- Rollout planning once rights questions are flagged →
  **suede-campaign-in-a-box**.
