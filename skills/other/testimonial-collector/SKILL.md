---
name: testimonial-collector
description: Systematically gather, score, and format client testimonials. Use when someone needs social proof, wants to collect feedback, needs to turn happy clients into public advocates, or asks for help requesting or drafting a testimonial.
---

# Testimonial Collector

## Mode

Detect from context or ask: *"One script, full system, or full system with campaign?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | 1 outreach script + 1 format template | Asking one client, right now |
| `standard` | Full collection system: timing, scripts, formatting, display guidance | Building repeatable social proof |
| `deep` | Full system + multi-channel strategy + case study pipeline | Sales enablement, proposal library |

**Default: `standard`** — use `quick` if they have one client in mind. Use `deep` if they want a system they can hand to a VA.

---

## Context Loading Gates

**Before proceeding, gather:**
- [ ] Client name, company, and industry
- [ ] Project type and specific deliverables
- [ ] Key results — push for at least one number ("even a rough estimate")
- [ ] Desired output format (short quote / medium paragraph / full narrative)
- [ ] Urgency (this week vs. building a library)

If results are vague (e.g., "things improved"), **stop and ask:** "Can you name one specific number — even a rough estimate? That's what makes a testimonial credible and usable." Do not draft until you have this.

If the user wants to skip a field: note it and flag the quality impact in the output.

---

## Phase 1: Situation Analysis

Before drafting anything, reason through:

1. **Client relationship stage:** Was this a quick project or a deep engagement? Depth affects how much authentic language is available.
2. **Results clarity:** Are the outcomes measurable (numbers, timelines, named outcomes) or soft (vibes, general satisfaction)?
3. **Format match:** What placement does the user need this for? A homepage needs different length than a sales deck.
4. **Voice data:** Does the user have existing communication from this client (emails, Slack, quotes) that can inform tone?

Output a brief situation summary:
> "You have a [length] engagement with [client] in [industry], with [strong/weak] results data. I'll draft in [format] with [authentic/templated] voice. Main gap to address: [specific gap]."

---

## Phase 2: Quality Scoring Framework

Score the raw testimonial content (or anticipated content) before drafting:

| Dimension | Score 1 | Score 3 | Score 5 |
|---|---|---|---|
| **Specificity** | No details | Vague references | Specific named result |
| **Measurability** | "It was great" | "Noticeable improvement" | "40% increase in leads" |
| **Authentic Voice** | Sounds like ad copy | Slightly stilted | Reads exactly how a person talks |
| **Length** | Too short (no context) | Decent but thin | Enough for all 3 formats |

**Scoring rule:**
- 4+ on all 4 dimensions → ready to use
- ≤2 on any dimension → apply iteration protocol before delivering

---

## Phase 3: Draft Generation

### The Ask Templates

**Direct Ask:**
```
Subject: Quick favor (30 seconds)

Hey [Name],

Loved working on [project] with you — especially seeing [specific result].

Would you be open to sharing a quick testimonial I could use on my site?

No pressure. If yes, I can either:
A) Send you 3 questions to answer
B) Write a draft for you to approve/edit

Whatever's easier.
```

**Question Route:**
```
3 quick questions:
1. What was the situation before we worked together?
2. What changed or improved?
3. Would you recommend this to others? Why?
```

**Draft-on-Behalf Framework:**
Rules for writing in the client's voice:
- **Tone:** Match their actual communication style (check emails/messages for vocabulary)
- **Structure:** Situation Before → What Changed → Specific Result → Recommendation
- **Avoid:** Superlatives without evidence ("amazing," "life-changing")
- **Avoid:** Leading with praise — lead with the client's situation
- **Length:** 50-75 words (short), 100-150 words (medium), 200+ (long/full)

Fill-in template:
```
"[Client situation in 1 sentence]. [What the engagement delivered — concrete]. 
[Specific result, ideally with a number]. [Recommendation statement in client's natural voice]."
```

---

## Phase 4: Format Production

### Short Format (2-liner)
```
"[One punchy outcome sentence — lead with the result]"
— [Name], [Title] at [Company]
```
**Use for:** Homepage, LinkedIn featured section, proposal proof points

### Medium Format (2-3 sentences)
```
"[Problem or situation]. [What changed]. [Recommendation or result]."
— [Name], [Title] at [Company]
```
**Use for:** Services page, sales decks, email sequences

### Long Format (Full narrative)
Structure:
1. Context paragraph (2-3 sentences on the situation)
2. Transformation paragraph (what happened during the engagement)
3. Results paragraph (outcomes, numbers, named wins)
4. Closing recommendation sentence

**Use for:** Case study pages, downloadable PDFs, high-trust sales assets

---

## Phase 5: Self-Critique Pass (REQUIRED)

After generating all formats, evaluate:

**Specificity check:** Does the short version have at least one concrete outcome (not just "great results")?
**Voice check:** Could the client have actually written this, or does it sound like a marketing headline?
**Placement check:** Is the recommended format actually correct length for the stated use case?
**Ethics check:** Does the draft contain any claims the client didn't make or numbers you added?

Flag any issues: "The short version lacks a specific metric — you'll need to get one number from the client before using this on a homepage."

---

## Iteration Protocol

If the received testimonial scores ≤2 on any dimension, send this gentle follow-up:
```
"Thanks so much — this is great. One small ask: could you add one specific 
number or outcome? Even rough ('saved us about 5 hours a week') makes it 
much more compelling for other clients. Totally optional, but makes a real difference."
```

If a second request still yields nothing specific: use Tier 3 proxy language:
> "noticeable improvement in [area]" or "process now runs without manual oversight"

---

## Placement Recommendation

Always deliver a placement recommendation with the formatted testimonials:

| Format | Recommended Locations | Why |
|---|---|---|
| Short (2-liner) | Homepage, proposals, LinkedIn | Trust at first glance |
| Medium | Services page, email, sales decks | Overcome late-stage objections |
| Long | Case study page, PDF, portfolio | Deep proof for serious buyers |

**Cross-reference:** If this client has a strong story, suggest running `case-study-builder` to expand into a full case study.

---

## Output Structure

```markdown
## Testimonial: [Client Name] — [Date]

### Quality Assessment
- Specificity: [X/5]
- Measurability: [X/5]
- Authentic Voice: [X/5]
- Length: [X/5]
- **Total: [X/20] — [Ready to use / Needs iteration]**

### Short Format (2-liner)
"[Quote]"
— [Name], [Title], [Company]

### Medium Format
"[Quote]"
— [Name], [Title], [Company]

### Long Format
[Full narrative]

### Placement Recommendation
[Where to use each format]

### Next Step
[Iteration note OR cross-reference to case-study-builder]
```

---

*Skill by Brian Wagner | AI Marketing Architect | brianrwagner.com*
