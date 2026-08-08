---
name: suede-sync-packaging
description: "Prep songs for sync pitches: scene angles, one-sheets, clean and instrumental assets, lyric flags, mood tags, rights questions, and links."
---

# Suede Sync Package

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


**Core principle:** a sync package makes a track easy to evaluate; it never
asserts the track is cleared. Confirmed facts and open clearance questions
travel in separate, labeled piles, every time.

## Input contract

Provide at minimum:

- **Track**: title, artist, featuring credits if any
- **Target world**: film / TV / ads / games / trailers / creator campaigns / brand brief (or "general sync")
- **Available assets**: which of master, instrumental, clean, stems, lyrics, credits, splits currently exist
- **Rights status**: what is confirmed vs. unknown (sample clearance, ownership splits, publishing assignment)

Optional but useful: reference sync placements the artist admires, mood or
scene keywords, existing pitches or supervisor feedback.

If no rights status is provided, treat every clearance question as open.

## Hard gates

Do not rationalize past these:

1. **Never claim or imply clearance.** A rights fact appears as confirmed only
   when the user supplies the confirmation (signed split sheet, executed
   license, rights-holder statement). Anything else stays OPEN or UNKNOWN. You
   organize the questions; you never answer them.
2. **Never resolve a rights question yourself.** If ownership, splits, samples,
   or publishing are unclear, mark the item UNKNOWN. Do not infer, average, or
   assume. Route the gap to suede-rights-audit.
3. **Asset checklist before pitch copy.** Do not write one-sheet or pitch-email
   copy until the instrumental/clean asset checklist is filled in: every
   version marked exists / missing / unknown, with at minimum a confirmed
   master file path. Missing instrumental or clean versions are flagged in the
   one-sheet, not glossed.
4. **Unresolved sample = pause and put it to the user.** Uncleared samples are
   a legal-risk finding: mark sample status "OPEN — recommend not pitching
   until cleared," tell the user exactly what is unresolved, and let them
   decide whether pitch copy is still drafted. If they proceed, the OPEN flag
   stays embedded in the one-sheet and pitch materials.
5. **Lyric flags are mandatory.** Screen the lyrics and flag profanity, brand
   and product names, artist name-drops, violence, drugs and alcohol, sexual
   content, religious and political content, and date-stamped references. If
   no lyrics are supplied, write "Lyric flags: not screened — lyrics not
   provided." A lyric surprise in review kills the placement.

## Package workflow

1. Identify the track, artist, genre, mood, tempo, lyric themes, versions,
   existing assets, and target sync world.
2. Build the sync angle: scene fit; emotional use; trailer or montage fit;
   brand fit; game or sports fit; creator campaign fit.
3. Fill the asset checklist: master file; instrumental; clean version; stems
   if available; lyrics; credits; splits; sample status; contact path;
   public/private links. Each item: exists / missing / unknown.
4. Screen lyrics and write the lyric flags (hard gate 5).
5. Separate confirmed rights facts from open clearance questions (hard gates
   1-2).
6. Write the one-sheet and pitch email only if gates 3-4 pass.
7. Stop at a clean review package. No promo CTA, placement promise, clearance
   claim, or outreach claim.

## One-sheet contract

The one-sheet is supervisor-facing. It contains exactly these fields:

```text
Track / artist / featuring:
Length / tempo / key (if known):
Genre and mood tags:
Sounds like: (era and energy references; never copy a protected identity)
Scene fits: (top 3, one line each)
Lyric themes:
Lyric flags:
Versions available: (master / instrumental / clean / stems)
Rights status: (one line, confirmed facts only)
Open clearance questions:
Contact path:
Public link:
```

The rights-status line states only confirmed facts and names the open
questions. Never compress "unknown" into silence.

## Failure modes

- **Missing master or instrumental**: flag in the asset checklist as a blocker.
  Do not complete the sync angle without at minimum a confirmed master file
  path.
- **Unresolved sample**: sample status is "OPEN — do not pitch until cleared."
  No pitch copy (hard gate 4).
- **Unknown splits or ownership**: flag in clearance questions. The package can
  be built but must carry the caveat: "Rights holder confirmation required
  before placement."
- **No contact path**: the package is complete but note: "No contact path
  identified — supervisor cannot follow up."
- **Scope creep**: if the request becomes a promo funnel, placement promise, or
  clearance claim, stop and restate the boundary: "This skill prepares
  review-ready materials. It does not clear rights, confirm placement, or
  generate outreach."

## Red flags — stop

If any of these appear in your reasoning, stop and re-read the hard gates:

- "The artist says it's cleared." A claim is not clearance. Status stays
  UNCONFIRMED with a clearance question attached.
- "We'll sort splits later." Splits sort before pitching, or the gap ships as
  an open question. Never silently.
- "The supervisor is waiting — skip the instrumental check." The checklist is
  the package. Skipping it ships a track no one can license.
- "It's a small indie film, nobody checks samples." Sample status is binary:
  cleared with proof, or OPEN.
- "Soften the sample note so the one-sheet reads better." Hidden risk reads
  worse in a licensing call.

## Public copy gate

Before outputting one-sheet copy, pitch email, captions, DMs, press angles,
site copy, bios, CTAs, or review language, run the Suede anti-slop line edit.
Name the actor, preserve the concrete track/release artifact, cut
throat-clearing, negative listing, fake intensity, lazy extremes, passive
actor-hiding, pull-quote slogans, generic AI phrasing, unsupported claims, and
em dashes.

## Output

```text
Sync positioning:
Best scenes:
Mood tags:
Lyric flags:
Asset checklist: (each item exists / missing / unknown)
Confirmed rights facts:
Clearance questions:
One-sheet: (per the one-sheet contract above)
Pitch email: (only if hard gates 3-4 pass)
Next review step:
```

## Routing

- Rights gaps or missing provenance → **suede-rights-audit** to find and
  organize the gaps, then **suede-rights-passport** to package.
- This grows into a release campaign → **suede-campaign-in-a-box**.
- Release folder or metadata gaps → **suede-release-linter**.
- Standalone public copy beyond the one-sheet → **suede-copy** or
  **johnny-suede-write**.
