---
name: aesthetic-instrument
description: "great_cto's own committed aesthetic — the instrument panel. Dark five-step surface ladder, exactly one accent, two faces divided by MEANING (Geist speaks, Geist Mono is machine-truth), tabular numerals, and a dash that is not a nought. Twelve checkable rules measured from packages/board and greatcto.systems, not designed for this file. Use when building or extending any great_cto surface — the board, the site, a report, a share page."
when_to_use: |
  Apply when:
  - building or extending ANY great_cto surface (board screen, site section, share report)
  - a new element must sit beside existing ones without re-deciding the system
  Do NOT apply when:
  - designing a CLIENT product — this is our identity, not a default. See rule 0.
effort: low
allowed-tools: Read, Write, Edit, Grep, Glob
---

# The instrument panel

A committed aesthetic in the sense of
[`skills/committed-aesthetic/SKILL.md`](../committed-aesthetic/SKILL.md): every
rule below is checkable, and every value was **read out of the source** —
`packages/board/public/index.html` and `great_cto-site/styles.css` — rather than
chosen to write this document.

The subject is an instrument, not a brochure. One person reads it to decide what a
machine may do next. Everything below follows from that.

## Rule 0 — this is the CATEGORY default, and calling it ours was wrong

The first version of this file opened "this is ours, not a default". Measured
against a real corpus on 2026-09-01, that is false, and the correction matters
more than anything below it.

Refero's top ten styles for a dark technical developer landing describe:
near-black canvas (Depot, Warp, Supabase, Trunk, Checkly, Cron, Linear, Eraser),
depth from surface shifts or borders **rather than shadows** (Warp, Supabase,
Trunk, Linear), and **one green accent used sparingly** (Depot, Warp, Supabase,
Trunk). Four of them are described with the words "instrument panel", "command
center" or "cockpit".

Every one of those is a rule below. This aesthetic is not great_cto's identity —
it is what every infrastructure product looks like, and this file codified the
modal choice and labelled it a differentiator. A skill that does that produces
template work while asserting it does not.

**What follows is still correct, and its correctness is functional, not
distinctive.** Dark, dense, one accent, tabular numerals and a dash that is not a
nought are right for a surface one operator reads all day to decide what a machine
may do next. Keep them for the BOARD. Just do not mistake them for a voice.

Where the category default costs something is the LANDING, where a visitor who has
seen Depot, Warp and Supabase cannot tell us apart. Differentiation there is a
brand decision made through `committed-aesthetic`, not a repaint of this file. And
for a client product — a dental practice does not want an instrument panel — go
through `committed-aesthetic` and choose deliberately.

## The DNA

**1. Five surface steps, each about 5% apart, and depth is always a step.**
`--bg-page #0a0e0c` → `--bg-card #11161a` → `--bg-muted #161c1f` →
`--bg-elevated #1a2025` → `--bg-strong #1e272c`. A raised element takes the next
step up. It does not take a shadow.

**2. Exactly one accent, and it is mostly not a fill.**
`--accent #00d97e` appears as a 1px border, a 3px rail on the active nav item, and
a 6% glow. It fills only a badge count and a swatch. Two accents is a different
design; adding one is a decision, not a tweak.

**3. One shadow in the system carries colour.** Card hover:
`0 1px 2px rgba(0,0,0,.4), 0 8px 24px rgba(0,217,126,.06)` — the accent at 6%.
Everywhere else depth is rule 1.

**4. Two faces, divided by MEANING rather than by taste.**
Geist is the voice the surface speaks in — headings, navigation, controls, prose.
Geist Mono is *machine truth*: anything a person would select and paste. Ids,
agent slugs, paths, money, versions, timestamps, verdict tokens, commands. The
test is one question: **would someone copy this?** Measured: 115 mono uses against
9 display. A task title is Geist and its id beside it is Geist Mono — the two faces
on one row are the point, not an inconsistency.

**5. Numerals are tabular, always.** `font-variant-numeric: tabular-nums` at
`letter-spacing: -0.02em`. A figure that changes width as it changes value reads as
motion the operator did not cause.

**6. A dash is not a nought.** Unmeasured renders as `—` in a lighter weight and
`--text3`; a measured zero renders as `0` in the numeral treatment. Every count on
every surface carries a third state, and it must be visibly different from zero.
This is the house rule the whole product rests on; it is a typographic rule here.

**7. Twelve type tokens, never a raw size.** 11 · 12 · 13 · 14 · 15 · 16 · 19 · 22,
plus numerics 24 · 30 · 36 · 52, as `--fs-*`. If a size is not on the scale, either
the scale is wrong or the element is.

**8. Tracking moves one way at each end.** ≥22px → `-0.02em`. 11px uppercase →
`+0.10em`. Nothing in between is tracked.

**9. Geist Mono never above weight 500.** It is vendored `wght 400 500`; above the
axis the browser synthesises a smeared bold. Geist runs 400–700; 500 is the
workhorse, 600 is emphasis, 700 exists for badge counts only.

**10. Desktop density is deliberate, and does not travel.** Controls are 30–32px,
chips 20px — below the 44px touch floor on purpose, because this is a pointer
surface for one operator. **A mobile or client surface must not inherit these
numbers**; it takes rules 1–9 and its own sizes.

**11. One hue per meaning, and colour never carries meaning alone.** Every status
colour is paired with a glyph or a word. A ▲/▼/— goes with the green/red/grey, so
the row survives a reader who cannot distinguish them.

**12. Latin subset, self-hosted, 52 KB.** Two variable faces, `font-display: swap`,
no CDN. Cyrillic and anything outside latin falls to the system stack mid-line —
a known look, decided for the byte count, not a bug to re-discover.

## What NOT to port

| Do not take | Why | Instead |
|---|---|---|
| The 30–32px control heights, to anything touched by a finger | rule 10 — this is a pointer surface for one operator | 44px minimum, keep rules 1–9 |
| `clamp()` fluid type from the site, to the board | a marketing page is read at every width; an instrument at one | fixed steps from rule 7 |
| The dark ladder, to a client product | rule 0 — it is our identity | choose through `committed-aesthetic` |
| `--max: 1100px`, to board screens | the board's content is rows and cards, not paragraphs | only the Docs reader caps measure, at 72ch |

## The component gallery

Rendered, with every measurement on the artboard, in the published board spec —
foundations, components, shell, screens, typography and the open findings. Working
sources in `.design-spec/`. Read the gallery before adding a component; it is
faster than deriving one from the rules and it is what the rules were written from.

## Where the rules came from, and where they are still broken

This aesthetic is measured, which means it is also **measured to be imperfect**.
`docs/reference/` and the spec's findings artboard carry the open list — spacing
and radius are not tokenised (11 raw `gap` values, 11 raw radii), the site carries
46 distinct font sizes against rule 7, and the light theme has three values under
the AA floor. A rule this file states and the source violates is a finding, not a
licence to violate it further.

Related: [`skills/committed-aesthetic/SKILL.md`](../committed-aesthetic/SKILL.md)
for the form · [`skills/ui-ux-pro-max/SKILL.md`](../ui-ux-pro-max/SKILL.md) for the
catalogue you consult when this does not apply.
