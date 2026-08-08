---
name: suede-public-relations
description: "Suede-owned earned-media discipline. Use when building a media list, validating a story angle, drafting a journalist pitch, preparing a press kit, evaluating newsjacking, or answering a reporter request. NOT FOR: directory submissions (use suede-directory-submissions), launch packaging (use suede-launch-packaging), social publishing (use suede-social), or contacting anyone without approval."
metadata:
  version: 1.0.0
---

# Suede Public Relations & Earned Media

Suede Public Relations turns verified milestones, evidence, and timely angles
into respectful earned-media briefs for journalists, podcasts, and newsletters.
It optimizes story fit and source usefulness without treating a drafted pitch as
sent or coverage as earned.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

---

## Core Philosophy

PR is not a substitute for distribution. Treat it as a channel hypothesis whose
value must be measured against the current audience, story, and sales motion.

- **Do not assume a placement drives or cannot drive conversion.** Track referral
  behavior, brand search, citations, and sales influence for this campaign.
- **Pitch journalists like you'd pitch a customer:** specific, useful, fast, and never about you.
- **The story is not your product. The story is the trend, the data, the conflict, or the human.** Your product is the evidence.
- **Test speed against relevance and accuracy.** Use the story's observed
  coverage curve and deadline; never trade verification for haste.

### When PR is worth it

- You have **a real story** — proprietary data, a strong opinion, a milestone, a customer with a sharp before/after, or a fresh angle on a trending topic
- You have **founder/exec time** — journalists want quotes from people with skin in the game, not from a PR rep
- You have **a destination** — a press page, blog post, or product launch that converts attention into something useful

### When to skip PR (for now)

- Pre-launch with no story beyond "we exist"
- No one on the team can sustain the approved, measured test window
- You don't have a clear ICP — journalists ask "who reads my piece because of this?" and if you can't answer, neither can they

---

## The PR Mix

Four possible modes. Select only those supported by the story, audience,
capacity, and current source access.

| Mode | What it is | Effort | Speed to coverage |
|------|------------|--------|-------------------|
| **Reactive (newsjacking)** | Inject your POV into trending news | Low–medium | Hours to days |
| **Proactive (pitching)** | Build a media list, draft original-story pitches | Measure current capacity | Set from story flow and response data |
| **Inbound (press requests)** | Respond to journalist queries on HARO/Qwoted/Featured | Low | Days to weeks |
| **Owned (press page + media kit)** | Make it easy for journalists to find you | One-time setup | N/A |

**For the reactive newsjacking workflow** — see [references/newsjacking.md](references/newsjacking.md)

**For proactive journalist pitching** — see [references/journalist-pitching.md](references/journalist-pitching.md)

**For inbound press-request platforms (HARO, Qwoted, etc.)** — see [references/press-platforms.md](references/press-platforms.md)

**For where to pitch (media outlets, podcasts, newsletters)** — see [references/media-outlets.md](references/media-outlets.md). For startup/SaaS/AI directories, use the separate `suede-directory-submissions` skill — different intent, different list.

---

## Owned: Press Page + Media Kit

Build this when verified newsroom assets and a maintained press contact would
reduce friction for the current media motion; measure usage rather than assuming
ROI.

**Press page (`/press` or `/newsroom`) should include:**
- One-paragraph company description (copy/paste ready)
- Founder bios with headshots (high-res, downloadable)
- Logo pack (SVG + PNG, light + dark, with usage guidelines)
- Product screenshots (high-res)
- Recent coverage list (social proof for the next journalist)
- Founding date, employee count, funding (if disclosed)
- A current press contact path in the format the intended outlets accept
- Recent press releases / announcements

State a response expectation only if the team has approved and staffed it. Use
the team's real service level rather than a universal 24-hour promise.

---

## Quick Reference: Pitch Quality Bar

Before presenting any draft for send approval, resolve these checks:

- [ ] Does a bounded recent sample show that this journalist covers the beat?
- [ ] Is there a clear news hook — something that just happened or is about to?
- [ ] Could this journalist write a complete story from this email alone? (Data, quotes, customer name, contact.)
- [ ] Is the subject line specific enough to predict the article's headline?
- [ ] Is the pitch as concise as the verified outlet preference and story
      complexity allow?
- [ ] Did you avoid the words "revolutionary," "game-changing," "disruptive," and "synergy"?
- [ ] Is the ask clear? (Interview? Embargo? Exclusive? Quote?)

Keep the output draft-only. Each recipient, channel, identity, and exact message
requires explicit approval before any external action.

---

## Measurement

What to track:

| Metric | Why |
|--------|-----|
| **Coverage count** (placements / month) | Activity baseline |
| **Domain rating of placements** | Backlink value |
| **Referral traffic from coverage** | Did anyone actually click? |
| **Brand search lift** | Did people search you after reading? |
| **AI citation rate** (ChatGPT, Perplexity quote your brand?) | The new measurement that matters |
| **Sales conversations citing the article** | One revenue-influence signal to reconcile with attribution limits |

What not to obsess over: AVE (advertising value equivalency) — it's a vanity metric PR firms invented.

---

## Common Workflows

### "Help me newsjack [trending story]"
Go to [newsjacking.md](references/newsjacking.md), run the scoring rubric, draft
a bounded set of evidence-backed angles, and return a recommended draft for
review. Do not pitch or publish.

### "Find journalists who cover [beat]"
Go to [journalist-pitching.md](references/journalist-pitching.md), use the
discovery checklist, and first discover whether an authorized browser or
research connector is callable. If not, work from user-supplied article URLs,
exports, or a manual research worksheet. Build a sourced, scored list without
claiming any profile or article was reviewed unless it actually was.

### "What's worth pitching this week?"
Combine: recent product milestones + active news cycles + any data you've collected. Score each potential story by the quality bar above.

### "Respond to this HARO query"
Go to [press-platforms.md](references/press-platforms.md), use the response
template, follow current outlet limits, and keep the result draft-only.

### "Build my press page"
Use the checklist above. Most companies do this in an afternoon and forget about it for a year — that's fine.

## Boundaries

- Do not contact journalists, submit reporter responses, publish press
  releases, or represent that a draft has been sent without explicit approval
  and a confirmed recipient.
- Do not fabricate claims, data, quotes, customers, credentials, urgency, or
  coverage; separate verified facts from proposed angles.
- Do not impersonate a source, promise exclusivity, or decide legal disclosure,
  embargo, or crisis-response policy.

## Routing

- Use `suede-launch-packaging` to coordinate a broader product launch.
- Use `suede-directory-submissions` for directory and catalog listings.
- Use `suede-social` for approved social distribution and engagement.
- Use `suede-copy` to polish a verified press-page or announcement draft.
