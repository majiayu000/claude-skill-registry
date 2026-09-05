---
name: product-economics
description: "Does this product make money at a price someone will pay? Forces contribution margin, a price with a stated basis, and a bottom-up market size — each number labelled measured / assumed / unknown, so a guess can never be read as a calculation."
when_to_use: |
  Apply BEFORE gate:product, while the brief is being written:
  - product-owner, in Step 4 — the Economics section of BRIEF-*.md
  - architect, when a design choice moves variable cost per user (model tier,
    context size, retrieval, image generation)
  - any time the answer to "should we build this" depends on money rather than
    on feasibility
effort: medium
allowed-tools: Read, Write, WebSearch, WebFetch
paths:
  - "docs/product/**"
  - "docs/architecture/**"
---

# Product economics

A product can pass every gate this pipeline has — architecture reviewed, tests
green, security signed off, deployed — and still lose money on every user. The
pipeline is silent about that, and silence reads as approval.

This is the missing question, and it is three questions:

1. **Does a unit pay for itself?** (contribution margin)
2. **What is the price, and on what basis?** (pricing)
3. **Are there enough units to matter?** (market size, bottom-up)

## The rule that makes this worth doing

**Every number carries its provenance**, in the notation the brief already
uses — do not invent a second vocabulary for this:

- `[source: <where it was read>]` — an invoice, a usage log, a competitor's
  published price with the date you checked it
- `[assumption]` — you made it up, and saying so is the point

`artifact-lint` already rejects a figure carrying neither. That rule was written
for the Problem section; it binds here at least as hard, because arithmetic
launders provenance: an `[assumption]` conversion rate and a `[source:]` one are
indistinguishable once they have been multiplied together, and the product of
two guesses is presented with the same confidence as a measurement.

**The third state is the one the notation has no symbol for: a number nobody
knows.** Do not fill that hole with a plausible figure — a plausible figure
becomes `[assumption]`, gets multiplied, and disappears into a margin. Write the
line as an open question instead, and carry it into **Risks & kill-criteria**
with the threshold that would end the project. An unknown that decides the
answer is a finding, not a gap.

## 1. Contribution margin — per unit, per month

```
price per unit                              $
  − variable cost per unit                  $
      LLM tokens (in + out, at list price)  $   ← usually the largest, often forgotten
      inference / GPU seconds               $
      storage + egress attributable to one unit
      per-unit third-party fees (payments %, SMS, maps, email)
      support minutes × loaded hourly cost
= contribution margin                       $     ← this must be POSITIVE
```

Fixed costs (your time, base infra, domain) do **not** belong here. They decide
when the product breaks even, not whether a unit is viable. A negative
contribution margin cannot be fixed by volume — more users lose more money.

**For AI products the LLM line is the whole question.** A heavy user on a
frontier model at an unmetered flat price is the classic way to build something
excellent and unsellable. Compute it at **list price for the model actually
configured**, at the **95th percentile** of expected usage, not the mean:
flat-rate plans are priced by the tail, and the tail is what arrives.

`cost-model` covers infrastructure and LLM cost for the BUILD. This covers the
cost of one user, for the LIFE of the product. Use its numbers here rather than
re-deriving them.

## 2. Price, and the basis for it

State which of the three the price rests on. Not all three — the one that
actually decided it:

- **Cost-plus** — margin over unit cost. Honest, and a floor; it never tells you
  what someone will pay.
- **Competitor-anchored** — priced against a named incumbent, with the delta
  justified. Name the incumbent and the price you checked, with a date.
- **Value-based** — a stated fraction of the money or hours the buyer saves.
  Requires a number for what they save, which is usually `assumed`; say so.

Then the sanity check that catches most of it: **what does the buyer pay today
for this problem?** Zero is a valid answer and a hard one — it means the budget
does not exist yet and must be created, which is a different product.

## 3. Market size — bottom-up only

Top-down TAM ("the CRM market is $90B, 0.1% is $90M") is not evidence. It is
arithmetic performed on someone else's report.

Bottom-up:

```
number of buyers you can NAME or enumerate
  × realistic annual price
  × a reachable fraction, with the channel that reaches them
= revenue you could plausibly get
```

If the channel cannot be named, the fraction is `unknown`, not optimistic.

For a solo operator the honest threshold is rarely "is the market big" — it is
**"are there 100 buyers I can reach without a sales team"**. Ask that one.

## What this produces

A section in `BRIEF-*.md`, before the recommendation:

```markdown
## Economics

| | value | basis |
|---|---|---|
| Price / unit / month | $X | competitor-anchored `[source: <name> pricing page, <date>]` |
| Variable cost / unit | $Z | `[source: LLM list price, <model>, p95 usage]` |
| Contribution margin | $X−Z | derived |
| What buyers pay today | $W | `[source: …]` or `[assumption]` |
| Reachable buyers (bottom-up) | N | via <named channel> `[assumption]` |

**Kill criterion:** <the number that, if it turns out worse than T, ends this>
**Cheapest way to find out:** <the test that resolves the largest `unknown`>
```

Every `unknown` in that table is carried into **Risks & kill-criteria** with a
threshold, so the brief cannot record an unresolved economic question as a
resolved one.

## What this is NOT

- **Not a forecast.** No three-year revenue curve. A curve built on `assumed`
  inputs is a decorated guess, and its shape persuades where its inputs cannot.
- **Not a reason to refuse to build.** Plenty of things are worth building at a
  loss — a portfolio piece, a wedge, something you want to exist. The rule is
  that the loss is **stated and chosen**, not discovered in month four.
- **Not investment advice**, and not a substitute for the operator's own
  judgement about their market.
