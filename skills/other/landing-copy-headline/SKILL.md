---
name: landing-copy-headline
description: Use whenever `landing-headline-writer` drafts the page headline (Chain Method step 9). Gives the 8 named rhetorical mechanisms, the outcome-subject test, and the selection procedure for generating 3 distinct-mechanism candidates and presenting them for the user's lock. Trigger on "write the headline", "headline candidates", or the start of `landing-headline-writer`'s own workflow.
---

# Landing Copy: Headline

The headline is the single highest-leverage line on the page — every
section beneath it either delivers on its promise or doesn't. This skill
is the algorithm `landing-headline-writer` runs to generate it: don't
draft headline wording by feel, run the mechanism generation and the
outcome-subject test below every time.

This skill covers the headline only. The subhead or lede immediately
beneath it, if the page has one, is `landing-copywriter`'s
`landing-copy-hero` skill — a different section, a different algorithm.

## Step 1: Pull the raw material, don't invent it

Read, don't re-derive:

- `landing-strategist`'s subject/audience/job statement — the concrete
  claim available to make
- The adjective pairs and their named opposites — what the headline is
  allowed to promise emotionally
- `landing-systems`'s voice spec — sentence rhythm, verb mode, user-side
  naming

Every candidate below is generated from this material. A headline that
doesn't trace to a specific adjective or the subject statement fails
`landing-critic`'s traceability audit later — catch that here, not there.

## Step 2: Generate one candidate per mechanism

Generate against at least 3 of these 8, chosen as whichever the subject
statement actually supports — not the same 3 by default on every build:

- **Outcome** — state the desired outcome directly ("Build software
  that holds together.")
- **Transformation** — current state → desired state ("Turn ideas into
  products people use.")
- **Tension** — expectation → contradiction ("Your product is ready.
  Your story isn't.")
- **Reframe** — common frame → stronger frame ("Your website isn't a
  brochure. It's a decision engine.")
- **Provocation** — command → uncomfortable truth ("Stop building
  features nobody asked for.")
- **Identity** — audience → belief or standard ("For teams that refuse
  to ship generic software.")
- **Mechanism** — how it works → implied benefit ("A disciplined path
  from schema to screen.") — use only when the mechanism itself is the
  distinctive, ownable claim; it still has to pass Step 3.
- **Curiosity** — open question → implied possibility ("What happens
  when your tools finally work together?")

Generate from **distinct mechanisms**, not three phrasings of one idea —
the point is testing which mechanism the subject statement actually
supports, not polishing a single guess.

## Step 3: The outcome-subject test (run on every candidate)

**The reader wants an outcome, not the mechanism that produces it** — the
headline's grammatical subject must be what the reader gets (what
changes for them, what they now have or no longer have to worry about),
not the product, feature, or mechanism that delivers it.

Run this test by reading only the headline, with no subhead for context:
does it state what the reader gets, or does it name the thing that gets
it to them?

- "One signature. Three uses." **fails** — the signature is the subject.
- "Your agent's work outlives the session that made it." **passes.**

A headline built from the subject statement's own phrasing ("ZenBin is
one cryptographic trust primitive...") tends to smuggle the mechanism
into the subject position by default — naming it is not the same as
leading with it. Demote the mechanism one level: it belongs in the
subhead or the sentence right after, earning its specificity once the
outcome has already landed. If a candidate only works because the reader
already knows what the mechanism is for, it's failing this test, not
passing it narrowly.

**This test overrides mechanism choice.** An Outcome- or
Transformation-mechanism candidate that fails it still fails, and a
Mechanism-mechanism candidate that passes it is still eligible. Rewrite
or cut any candidate that fails before Step 4.

## Step 4: Apply the writing standard

Scoped to a single line — the same bar `landing-copywriter` holds section
copy to:

- **Cut inflated words.** No "delve," "landscape," "robust,"
  "comprehensive," "leverage," "seamless," "cutting-edge," "elevate,"
  "unlock," "empower," "streamline," "game-changer," "harness,"
  "revolutionize," or any word from that register.
- **No negation formulas.** Never write "It's not X — it's Y."
- **No em dashes.** Use a comma, period, or restructure the sentence.
- **Concrete over abstract.** A claim like "significant improvement"
  ships only with the number, name, or comparison that makes it
  checkable. If the brief doesn't supply one, the claim doesn't ship in
  that form.

## Step 5: Select and present

Select the 3 strongest, distinct candidates that survived Steps 3 and 4.
Label each with its mechanism name and present all 3 to the user — this
is a hard stop; wait for an explicit pick (the other 2 stand as backups)
or a redirect. Every section `landing-copywriter` writes afterward is
checked against whichever headline locks here, so an unconfirmed pick
compounds the same way an unconfirmed subject statement does at strategy
step 1.

## Self-test

- All 3 presented candidates came from 3 distinct mechanisms, not 3
  phrasings of the same one.
- Every candidate traces to a named adjective or the subject statement —
  a line that could run on a competitor's page unchanged (the swap test)
  was rewritten before presenting, not left for `landing-critic` to
  catch.
- Every candidate passed the outcome-subject test individually — not
  waved through because the set as a whole "feels balanced."
- The user was shown all 3, labeled by mechanism, and explicitly picked
  or redirected — not assumed.

## Constraints

- Never present fewer than 3 distinct-mechanism candidates.
- Never lock a headline without the user's explicit confirmation.
- Never draft the subhead, section body, or CTA copy here — that's
  `landing-copywriter`'s `landing-copy-hero` and other section skills,
  run only after this one locks.
