---
name: landing-copy-proof
description: Use whenever `landing-copywriter` drafts a proof/evidence section — social proof, numbers, case studies, benchmarks, testimonials. Trigger when the section's role in `landing-sequencer`'s list is to make an already-explained claim believable, distinct from the mechanism section (explains the how) or the objection section (handles doubt directly).
---

# Landing Copy: Proof

This section's only job is to make an already-stated claim checkable.
It doesn't introduce a new claim, and it doesn't explain how anything
works — that's `landing-copy-mechanism`, already run. A proof section
that's making its case for the first time here, rather than backing up a
claim made earlier, is out of order.

## What this section answers

One question: **why should the reader believe the mechanism section's
claim is true, not just plausible?** Every sentence in this section
exists to make one specific upstream claim checkable — a number, a name,
a comparison, a quoted result. A proof section with no specific,
attributable evidence isn't a proof section; it's an unearned assertion
wearing this section's placement as false credibility.

## The algorithm

Paragraph count from the beat count `landing-sequencer` assigned, but
proof content is the one archetype most likely to be genuinely
list-shaped — a set of parallel data points (3 stats, 3 logos, 3 quotes)
reads better as a list than forced into prose. Decide the shape first:

1. **Single strong proof point** (1 case study, 1 headline stat) → prose,
   1 paragraph: name the evidence, state the specific number or result,
   connect it back to the exact claim it's proving.
2. **Multiple parallel proof points** (3+ stats, logos, or quotes of
   equal weight) → a `-` list per `landing-copywriter`'s output format,
   each item a specific, named data point — not restated as full
   sentences if a short parallel phrase does the job.
3. **Mixed** (one lead proof point plus supporting parallel evidence) →
   one prose paragraph for the lead point, followed by a `-` list for the
   rest.

Every item, in either shape, names its source: a specific number, a
named customer, a dated benchmark, a quoted individual — never "users
report" or "studies show" without the name attached (per
`landing-copywriter`'s no-unnamed-authority rule, which applies with
extra weight here since this entire section exists to be checkable).

## Writing standard (scoped to this section)

- Apply `landing-copywriter`'s full writing standard.
- **No unnamed authority — this is the section's core failure mode.** If
  a proof point has no name, number, or date attached, it doesn't ship in
  this section in that form. Reframe it as the subject's own claim
  (belongs in `landing-copy-mechanism` instead) or cut it.
- **Concrete over abstract, absolute in this section.** "Significant
  improvement" never ships here — this is the one section whose entire
  purpose is the number that makes a claim checkable.
- **Each proof point traces to a specific upstream claim.** A proof point
  floating free, proving nothing stated earlier in the page, is
  decoration, not evidence — connect it explicitly or cut it.

## Self-test

- Every proof point names a specific source — a number, a customer, a
  date, a quoted person. None reads as "studies show" or "users love it"
  without attribution.
- Each proof point connects to a specific claim made in an earlier
  section (usually `landing-copy-mechanism`'s), not floating as generic
  credibility.
- The shape (prose vs. list vs. mixed) matches whether the content is
  genuinely one strong point or several parallel ones — not forced into
  prose to avoid "too many bullets," and not listed out of laziness when
  one point deserves real prose development.

## Constraints

- Never include a proof point with no named source — an unnamed claim
  doesn't belong in this section in any form.
- Never introduce a new claim here that wasn't already made upstream —
  this section proves, it doesn't originate.
- Never explain how the product works here — that's already
  `landing-copy-mechanism`'s completed job; this section only backs it
  up.
