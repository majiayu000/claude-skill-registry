---
name: tov-guidelines
version: '1.0'
last_updated: 2026-05-19
author: genesys-growth
description: Extract voice patterns from existing content (website, blog, social, sales-call transcripts) and codify into voice rules. Produces voice analysis + voice guidelines (rules per pattern + violation pattern + fix template). Writes to marketing/brand/brand-voice.md as the canonical voice rules every content skill reads. Triggers - "tone of voice", "brand voice", "voice guidelines", "TOV audit", "writing rules", "extract voice"
goal: Analyze existing content (website, blog, social, sales-call transcripts) and codify voice patterns into 5 voice rules with violation/fix patterns.
outcome: marketing/brand/brand-voice.md with 5 voice rules every content skill applies.
primitive: research
ontology_type: tone-of-voice
review_gate: 2
inputs:
  required: []
  recommended:
    []
outputs:
  - type: tone-of-voice
    feeds_into:
      - content-strategy
      - landing-page-copy
      - product-messaging
owned_by_agent: researcher
mcps_used:
  - exa
triggers:
  slash_commands:
    - /tov-guidelines
status: draft
---

# tov-guidelines — Stage 1 + 2 research skill (PMM spine)

Analyzes existing content (your website, blog, recent LinkedIn posts, sales-call transcripts) and produces voice rules that downstream content skills apply.

---

## When to use

- When onboarding a new content writer / contractor — they need codified voice rules to write in your voice
- When LinkedIn or blog output stops sounding like the founder / brand
- Quarterly refresh

## When NOT to use

- For visual brand identity (use `/brand-kit` — voice + visual are separate but both live in `marketing/brand/`)
- For one-off content checks against existing rules (write a custom gate skill that reads `brand-voice.md`)
- For positioning or messaging (use `/positioning` or `/product-messaging`)

## How it works

1. Inputs: source content (one or more of: website URL, blog URL, LinkedIn handle, sales-call transcripts, founder writing samples).
2. Reads (Exa MCP for fresh data): the source content. Patterns extracted include: vocabulary preferences, sentence-length defaults, headline conventions, em-dash usage, list-vs-prose preference, contraction frequency, persona pronouns, signature opening / closing patterns.
3. Produces a two-phase output:
   - **Phase 1 — Voice analysis** (extracted patterns from source material with frequency scores): "uses em-dash with spaces 87% of the time across 30 LinkedIn posts; sentence case headings 100% of the time; banned-word violations 0 in last 10 posts"
   - **Phase 2 — Voice guidelines** (codified rules every content skill applies):
     - Rule N — {rule name}
     - **The rule:** 1-sentence statement
     - **Why:** 1-sentence justification
     - **Violation pattern:** what breaking this looks like
     - **Fix template:** how to fix
     - **Exception:** when the rule doesn't apply
4. Writes to `marketing/brand/brand-voice.md` (overwrites prior canonical; git history preserves prior versions). Marks `status: locked` once approved.

## Invoke

```
/tov-guidelines https://yourdomain.com + analyze my last 10 LinkedIn posts
```

Or open-ended:
```
/tov-guidelines extract voice from these sales-call transcripts: [paths]
```

## Example output

See [`marketing/brand/brand-voice.md`](../../../marketing/brand/brand-voice.md) for the PulseAnalytics seed. Notice the 5 rules each have rule statement + why + violation pattern + fix template + exception. The 5 rules cluster into two themes (prose hygiene + claim integrity).

## Dependencies

- **Reads from:** source content (URL or files — provided as input); optionally `marketing/icp/ICP.md` (voice should match the ICP's vocabulary register)
- **Reads via Exa MCP (optional):** the source content if it lives on the web
- **Writes to:** `marketing/brand/brand-voice.md` (canonical)
- **Downstream readers:** any content skill (LinkedIn, blog, newsletter, email), `/landing-page-copy`, future gate skills

## Customization

The 5-rule default in the PulseAnalytics example is operator-flavored. Yours may need more rules (large enterprise teams sometimes track 8-12) or fewer (founder voice often clusters into 3-4 rules). Use whatever rule count matches the patterns you can actually enforce.

Don't add a rule you can't enforce — every rule should map to a check a gate skill could run automatically. Vague rules ("be human") get ignored; specific rules ("no em-dashes without spaces") get enforced.

## Where this fits in the Example 1 chain

```
Week 1: /tov-guidelines (parallel with competitor + ICP research) → voice rules locked
Week 2: /positioning + /product-messaging apply voice rules to output
Week 3+: every content / paid / outbound execution skill reads voice rules
```

## Refresh cadence

Quarterly. Trigger sooner when the team finds a new buzzword pattern, customer flags off-brand phrasing, or a new persona is added (vocabulary may shift).
