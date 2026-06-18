---
name: expert-pov
version: '1.0'
last_updated: 2026-06-17
author: genesys-growth
description: Extract a founder's or expert's point of view — core beliefs, contrarian takes, origin stories, taste — and synthesize a recommended "one big idea" (OBI) that anchors thought leadership and brand voice. Writes to marketing/expert-pov/expert-pov.md. Triggers - "expert pov", "founder point of view", "thought leadership angle", "one big idea", "OBI", "founder beliefs", "founder narrative"
goal: Turn a founder's raw thinking into a structured POV + a recommended OBI that anchors thought leadership, positioning, and brand voice.
outcome: marketing/expert-pov/expert-pov.md with belief map, contrarian positions, origin stories, taste profile, and a recommended OBI.
primitive: research
ontology_type: expert-pov
review_gate: 2
inputs:
  required: []
  recommended:
    - tov-guidelines
outputs:
  - type: expert-pov
    feeds_into:
      - positioning
      - product-messaging
      - content-strategy
owned_by_agent: researcher
mcps_used:
  - exa
triggers:
  slash_commands:
    - /expert-pov
status: draft
---

# expert-pov — founder point-of-view research skill

Extracts the founder's / expert's genuine point of view and synthesizes a recommended "one big idea" (OBI) — the belief they can credibly own for years. Writes to `marketing/expert-pov/expert-pov.md`. This is the source the brand voice, thought-leadership, and founder-led content all read from.

---

## When to use

- Spinning up founder-led thought leadership and you need a defensible angle, not generic takes
- Brand voice or positioning leans on founder conviction and you want it captured once, sourced
- Before a content push where the founder is the face

## When NOT to use

- For company tone-of-voice rules (use `/tov-guidelines` — voice mechanics, not beliefs)
- For positioning strategy (use `/positioning` — market position, not personal POV)
- When there's no real founder input to work from — see the thin-input guard below

## Inputs — and the thin-input guard

Founder input is the raw material: existing content (LinkedIn posts, podcast transcripts, interviews, talks) **or** answers to the question bank. If the available input is thin — fewer than ~3 distinct beliefs, 1 origin story, and 1 contrarian position — **halt before OBI synthesis** and ask the founder for more. A fabricated POV is worse than none; it reads hollow and fails the 100 Posts Test below.

## How it works

1. Inputs: founder content URLs and/or interview answers. Optional: `marketing/brand/brand-voice.md` for voice alignment.
2. Reads (Exa MCP for public founder content): LinkedIn, podcasts, interviews, talks, prior writing.
3. Produces a structured POV with these sections (matches the PulseAnalytics example):
   - **Belief map** — core beliefs + the implicit assumptions under them + where each invites push-back
   - **Contrarian positions** — the hot takes, with what the consensus view is and why the founder departs from it
   - **Origin stories** — 2-3 moments that shaped the thinking (the realization, what changed)
   - **Taste profile** — what they admire, what they reject, their quality bar
   - **Theme clusters** — 3-5 recurring territories the founder returns to
   - **Recommended OBI** — the one big idea, scored on authenticity / differentiation / memorability / scalability / business fit, with an activation angle
4. Apply the **100 Posts Test** — could the founder genuinely write 100 authentic posts on this OBI? If not, it's a campaign, not an OBI. Pick again.
5. Every belief traces to a quote or a stated answer; nothing invented. Mark gaps `[UNAVAILABLE]`.
6. Writes to `marketing/expert-pov/expert-pov.md` (overwrites prior canonical; git history preserves prior versions).

## Invoke

```
/expert-pov
```

Then share founder content links or answer the question bank. Or:

```
/expert-pov — founder LinkedIn: [URL] + this podcast transcript: [paste]
```

## Example output

See [`marketing/expert-pov/expert-pov.md`](../../../pulse-analytics-example/expert-pov/expert-pov.md) for the PulseAnalytics example seed. Notice: beliefs carry their counter-view; the OBI is scored, not asserted; the 100 Posts Test is applied explicitly.

## Dependencies

- **Reads from:** founder content + interview answers (required); `marketing/brand/brand-voice.md` (optional)
- **Reads via Exa MCP (optional):** public founder content
- **Writes to:** `marketing/expert-pov/expert-pov.md` (canonical; thought-leadership + founder content read from here)

## Customization

When there's more than one public-facing expert (a founder + a head of product who both post), run once per person — each gets their own OBI. Keep them distinct; a shared "company POV" dilutes both.

## Where this fits in the chain

```
/tov-guidelines → company voice mechanics
/expert-pov (THIS SKILL) → founder beliefs + OBI
        ↓
/positioning + /product-messaging borrow the founder's framing
content (thought leadership, social) is written from the OBI
```

## Refresh cadence

Every 6 months, or when the founder's thinking visibly shifts (a new belief shows up across recent posts).
