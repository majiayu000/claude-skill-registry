---
name: landing-copy-objection
description: Use whenever `landing-copywriter` drafts an objection-handling section — FAQ, risk-reversal, or direct address of the reader's stated hesitation. Trigger when the section's role in `landing-sequencer`'s list is to remove a specific, nameable doubt before the CTA, distinct from proof (backs up a claim already made) or the CTA section itself (the ask).
---

# Landing Copy: Objection handling

This section names the reader's actual hesitation and answers it
directly. It is not a second proof section, and it is not a place to
restate the mechanism — its job is to name a doubt the reader is likely
already holding and resolve it in the reader's own terms, not the
product's.

## What this section answers

One question per objection handled: **what is the specific, nameable
reason this reader might not act, and what directly removes it?** A
generic FAQ ("How does it work?" restating the mechanism section) isn't
this — a real objection is something the reader would say out loud if
pushed ("this sounds like it'll take longer than what I do now," "I've
been burned by a tool like this before"). If the brief or upstream chain
doesn't supply a real, specific objection, that's a gap to flag, not a
license to invent a generic FAQ to fill the section.

## The algorithm

Paragraph count from the beat count `landing-sequencer` assigned, with
one addition specific to this archetype: **one objection per beat**, not
one paragraph of general reassurance. A 3-beat objection section handles
3 distinct, named objections, not one objection developed across 3
paragraphs.

Per objection:

1. **Name the objection in the reader's own words**, not the product's
   framing of it — a question or a stated doubt, not a euphemism for it.
2. **Answer it directly**, in one or two sentences. No hedge stacks, no
   "well, actually" — a direct answer or, if the honest answer is a
   limitation, a direct acknowledgment of the limitation and why it
   doesn't undermine the reader's specific job (from
   `landing-strategist`'s subject statement).
3. **Don't re-litigate proof or mechanism here.** If the honest answer to
   an objection is "see the proof section above," reference it briefly
   rather than restating the evidence.

If genuinely FAQ-shaped (3+ parallel question/answer pairs), render as a
list per `landing-copywriter`'s output format — each item a
question-plus-answer pair, not a bare noun phrase.

## Writing standard (scoped to this section)

- Apply `landing-copywriter`'s full writing standard.
- **Answer honestly, including real limitations.** A section that only
  handles softball objections ("Is it easy to use? Yes!") reads as
  evasive by omission — if there's a genuine, known limitation the
  audience would ask about, address it directly rather than picking only
  favorable objections to list.
- **No hedge stacks in the answer.** "It could potentially work for most
  teams" fails here specifically, since the whole point of this section
  is removing uncertainty, not restating it in softer language.
- **No manufactured drama in the question framing.** State the objection
  plainly, the way the reader would actually think it.

## Self-test

- Each objection handled is specific and nameable — not a generic FAQ
  restating the mechanism or proof sections.
- Each answer is direct — no hedge stack, no deflection to "it depends."
- At least one genuine limitation or edge case is addressed honestly, if
  the subject statement or brief surfaces one — not only favorable
  objections selected.
- No objection restates content already fully covered in
  `landing-copy-mechanism` or `landing-copy-proof` — if it must reference
  that content, it does so briefly, not by repeating it.

## Constraints

- Never invent a generic FAQ to fill this section's beat count if no
  real objection is available — flag the gap back rather than padding
  with "How does pricing work?" unless pricing genuinely is a live
  objection for this audience.
- Never handle more objections than the assigned beat count allows —
  one objection per beat, not stacked.
- Never soften an honest limitation into a non-answer — a hedge here
  undermines the section's entire purpose.
