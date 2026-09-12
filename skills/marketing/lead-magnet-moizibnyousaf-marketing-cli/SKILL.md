---
name: lead-magnet
description: |
  Create high-converting free resources that capture emails and build trust. Produces complete lead magnets (ebooks, checklists, templates, toolkits, quizzes) with landing page copy, thank-you page, and follow-up email sequence. Use when someone needs a list-building asset, wants to grow their email list, needs an opt-in incentive, a content upgrade, a gated download, or top-of-funnel content. Triggers on 'lead magnet', 'ebook', 'checklist', 'template', 'free resource', 'opt-in', 'grow my list', 'email capture', 'content upgrade', 'list building', 'gated content', or 'free download'. Even if someone just says 'I need something to capture emails' or 'how do I get more subscribers', this is the skill. Every lead magnet passes a 4-gate quality test before shipping.
category: copy-content
tier: must-have
reads:
  - brand/voice-profile.md
  - brand/audience.md
  - brand/keyword-plan.md
writes:
  - marketing/lead-magnets/{name}/content.md
  - marketing/lead-magnets/{name}/landing-page.md
  - marketing/lead-magnets/{name}/thank-you.md
  - marketing/lead-magnets/{name}/follow-up-emails.md
depends-on:
  - brand-voice
  - audience-research
triggers:
  - lead magnet
  - freebie
  - opt-in
  - email capture
  - free download
  - checklist
  - template
  - swipe file
  - ebook
  - gated content
  - grow email list
allowed-tools: []
---

# Lead Magnet Creation

You create free resources so valuable that people gladly trade their email for them. Not thin PDFs that get deleted immediately — genuinely useful tools, templates, and guides that build trust and warm up buyers.

## On Activation

1. Read `brand/audience.md` — identify the sharpest pain point worth solving for free
2. Read `brand/voice-profile.md` — match tone across all deliverables
3. Read `brand/keyword-plan.md` — align lead magnet topic with SEO strategy
4. If brand files don't exist, ask: Who's the audience? What do you sell? What's their biggest frustration?

---

## The Lead Magnet Test

Before building anything, the concept must pass all four:

1. **Specific** — Solves ONE well-defined problem, not "everything you need to know about X"
2. **Quick win** — Delivers a result in under 15 minutes of consumption
3. **High perceived value** — Looks like something worth paying for
4. **Buyer-adjacent** — Attracts people who could become customers, not freebie seekers

If it fails any test, pick a different angle.

---

## Brand Integration

- **voice-profile.md** → Match voice tone in headlines, opening paragraphs, and CTAs. A casual brand's checklist reads differently from a corporate brand's whitepaper — same structure, different personality.
- **audience.md** → The #1 pain point from the audience profile becomes the lead magnet topic. Don't guess — use the persona's exact language for the headline.
- **keyword-plan.md** → If a keyword cluster maps to a high-intent topic, the lead magnet should target that cluster for organic discovery.

---

## Step 1: Identify the Pain Point

Map audience pain points to lead magnet opportunities:

| Pain Point Type | Best Format | Example |
|----------------|-------------|---------|
| "I don't know how" | Step-by-step guide | "The 7-Step SEO Audit Checklist" |
| "I don't have time" | Template / swipe file | "50 Email Subject Lines That Get Opens" |
| "I keep making mistakes" | Checklist | "Pre-Launch Checklist: 23 Things to Verify" |
| "I need a system" | Toolkit / framework | "The Content Calendar Template + SOPs" |
| "I need proof it works" | Case study / data | "How We Got 10K Users in 30 Days (Full Breakdown)" |
| "I can't decide" | Comparison / scorecard | "Framework Comparison: Which Stack Fits Your SaaS?" |

---

## Step 2: Choose Format

### Format Specs

| Format | Length | Production Time | Best For |
|--------|--------|----------------|----------|
| **Checklist** | 1-3 pages | Low | Process-oriented audiences, quick wins |
| **Template** | 1-5 pages | Low | Practitioners who need a starting point |
| **Swipe file** | 5-20 pages | Medium | Copy, design, or strategy examples |
| **Guide/Ebook** | 10-30 pages | High | Complex topics, establishing authority |
| **Toolkit** | 3-10 assets | High | Comprehensive solution bundles |
| **Mini-course** | 3-5 emails | Medium | Nurture-heavy funnels |

**Default to the shortest format that solves the problem.** A killer checklist beats a mediocre ebook every time.

---

## Step 3: Write the Content

### Content Structure (All Formats)

```markdown
---
title: "Lead Magnet Title"
format: checklist | template | guide | toolkit | swipe-file
audience: "Target segment"
pain_point: "Specific problem this solves"
quick_win: "What they'll achieve after consuming"
related_product: "What this naturally leads to buying"
date: 2026-03-12
---
```

### Writing Rules

- **Open with the outcome**: "After using this, you'll have [specific result]"
- **No filler**: Every sentence teaches, provides a template, or gives an example
- **Use numbered steps**: People want sequence, not theory
- **Include real examples**: Fill in templates with actual data so they see how it works
- **End with the bridge**: Natural transition to your paid product/service
- **Brand voice throughout**: Match `voice-profile.md` — this is their first impression

### Checklist Format

```markdown
## [Phase/Section Name]

- [ ] Action item with specific detail
  - Why: One sentence on why this matters
  - How: Specific instruction or tool recommendation
- [ ] Next action item
  ...
```

### Template Format

```markdown
## [Template Name]

**Instructions**: How to fill this out (2-3 sentences)

### Section 1: [Name]
[Template with placeholder text in brackets]

**Example** (filled in):
[Same template completed with real data]
```

---

## Step 4: Landing Page Copy

Write a complete landing page for the lead magnet:

### Structure

```markdown
# Headline: [Specific outcome] + [Format type]
## Subheadline: Who it's for + what changes after they use it

### The Problem (2-3 sentences)
[Agitate the pain point — make them feel it]

### What You'll Get (bullet list)
- Specific deliverable 1 — what it does for them
- Specific deliverable 2 — what it does for them
- Specific deliverable 3 — what it does for them

### Who This Is For
- Perfect for: [specific description]
- Not for: [who should skip this]

### Social Proof (if available)
"Quote from someone who used it" — Name, Title

### CTA
[Button: Get the Free {Format}]
[Subtext: No spam. Unsubscribe anytime.]
```

### Landing Page Rules

- One CTA only — get the email
- No navigation links — no escape routes
- Headline = outcome, not description ("Write Emails That Get Replies" not "Email Writing Guide")
- Bullet points sell specific deliverables, not vague promises
- Keep above the fold: headline, subheadline, 3 bullets, email field, button

---

## Step 5: Thank-You Page

The thank-you page is the highest-attention moment. Use it.

```markdown
# You're in! Check your email for [Lead Magnet Name].

## While you're here...

[One of these plays:]

**Option A — Tripwire**: Offer a low-cost product ($7-$27) at a discount
**Option B — Next step**: Invite to book a call, join a community, or start a trial
**Option C — Share**: Ask them to share with a colleague for bonus content

[Keep it to ONE ask. Don't overwhelm.]
```

---

## Step 6: Follow-Up Email Sequence

3-email sequence delivered over 5 days:

### Email 1: Delivery (Immediate)

```
Subject: Here's your [Lead Magnet Name]
Preview: Plus one tip to get the most out of it

Body:
- Deliver the asset (download link)
- One quick-start tip (the single most important thing to do first)
- Set expectation: "I'll send you [X] over the next few days"
- Sign off warm and personal
```

### Email 2: Value Add (Day 2-3)

```
Subject: The mistake most people make with [topic]
Preview: [Specific detail that creates curiosity]

Body:
- Share an insight related to the lead magnet topic
- Story or example that demonstrates the insight
- Bridge to your product/service naturally
- Soft CTA: "If you want help with this, [link]"
```

### Email 3: Bridge to Product (Day 4-5)

```
Subject: Quick question about [their goal]
Preview: [Question that implies you can help]

Body:
- Ask a question about their situation
- Share a brief case study or result
- Direct CTA to your product/service
- PS: Restate the value prop in one line
```

**Integration**: Output emails compatible with `gws` CLI for sending.

---

## Output Structure

```
marketing/lead-magnets/{name}/
├── content.md          # The actual lead magnet content
├── landing-page.md     # Landing page copy
├── thank-you.md        # Thank-you page copy
└── follow-up-emails.md # 3-email delivery + nurture sequence
```

Every output file includes this frontmatter:

```yaml
---
lead_magnet: "{name}"
type: content | landing-page | thank-you | follow-up-emails
format: checklist | template | guide | toolkit | swipe-file | mini-course
audience: "{target segment}"
pain_point: "{specific problem}"
bridge_product: "{what this leads to buying}"
date: 2026-03-20
status: draft
---
```

---

## Quality Checklist

Before shipping, verify the complete lead magnet passes all checks:

**Content:**
- [ ] Solves ONE specific problem (not a topic overview)
- [ ] Delivers a result in under 15 minutes of consumption
- [ ] Opens with the outcome, not the process
- [ ] Every sentence teaches, templates, or examples — no filler
- [ ] Includes real examples with actual data filled in
- [ ] Ends with a natural bridge to the paid product
- [ ] Voice matches brand (if voice-profile.md exists)

**Landing Page:**
- [ ] Headline states the outcome, not the format
- [ ] 3+ specific bullet points (deliverables, not promises)
- [ ] "Who This Is For" and "Not For" sections present
- [ ] Single CTA — no navigation, no escape routes
- [ ] No spam language in form area
- [ ] Social proof if available

**Follow-Up Emails:**
- [ ] Email 1 delivers immediately with a quick-start tip
- [ ] Each email has ONE purpose and ONE CTA
- [ ] Bridge to paid product feels natural, not forced
- [ ] Under 300 words per email

---

## Anti-Patterns

**Common lead magnet mistakes (and why they fail):**
- **Too broad:** "Everything You Need to Know About Marketing" attracts everyone, converts no one. Broad topics attract browsers, not buyers. Specificity signals "this was made for ME."
- **Too long:** 50-page ebooks don't get read. The lead magnet's job is to deliver a quick win and build trust — not to be comprehensive. If they don't finish it, the follow-up sequence lands on someone who feels guilty, not grateful.
- **No bridge:** Lead magnet topic is unrelated to what you sell. If your lead magnet teaches cooking but you sell marketing software, you've captured the wrong audience. The magnet must make buying the logical next step.
- **Generic title:** "Marketing Guide" vs "The 7-Step SEO Audit Checklist for SaaS Founders" — specificity wins because it passes the "is this for me?" test in 2 seconds. Generic titles get ignored in crowded inboxes.
- **Filler content:** Padding to reach a page count destroys trust. Readers feel cheated when they traded their email for fluff. Every page must earn its place.
- **No quick win:** If they can't get value in the first 5 minutes, they'll never finish it — and an unfinished lead magnet creates negative association with your brand, not positive.
- **Freebie-seeker magnet:** Discount codes and "free stuff" lists attract people who want free stuff, not people who would pay for your product. Design the magnet to attract your ideal buyer, not maximise downloads.

**AI tells to avoid in lead magnet content:**
- "In today's fast-paced world..." / "It's important to note..."
- Every section same length, same structure
- Hedging: "may help," "could potentially," "it's worth considering"
- Overuse of: comprehensive, robust, leverage, streamline, crucial, delve
- No personality, no opinions, no specific examples from experience

---

## Worked Example

**Lead Magnet: "The Pre-Launch Checklist: 23 Things to Verify Before You Ship"**

**Audience:** Indie hackers and solo founders about to launch a SaaS product
**Pain point:** Fear of missing something critical at launch
**Format:** Checklist (2 pages)
**Bridge:** Checklist reveals how much marketing work is needed → mktg skills pack handles it

**Landing Page Headline:** Ship your product without the 3 AM panic attacks.
**Subheadline:** 23 things to verify before launch day — the checklist I wish I had before my first product flopped.

**What You'll Get:**
- The exact 23-item checklist covering technical, marketing, and legal readiness
- Priority labels (must-have vs nice-to-have) so you focus on what matters
- One-line explanations for WHY each item matters — not just what to do

**CTA:** Get the Free Checklist →
**Subtext:** No spam. Just the checklist and one follow-up tip.

**Thank-You Page:** "Your checklist is in your inbox. While you wait — the #1 thing founders skip on this list is marketing prep. Want to fix that in 15 minutes?" → Link to product/trial

**Follow-Up Email 1 (Immediate):**
Subject: Your pre-launch checklist is inside
Body: Download link + "Start with items 1-5. They take 10 minutes and catch 80% of launch-day problems." + "I'll send you the biggest mistake I see founders make on this list in 2 days."

---

## Lead Magnet Ideas by Business Type

| Business | High-Converting Formats |
|----------|------------------------|
| SaaS | Free tool, ROI calculator, comparison template |
| Agency | Audit checklist, swipe file, case study |
| Course/Info | Mini-course, chapter 1, cheat sheet |
| E-commerce | Buying guide, discount code, style quiz |
| B2B | Industry report, benchmark data, decision matrix |

---

## References

- [format-examples.md](references/format-examples.md): Best-in-class examples by format type (quizzes, PDFs, checklists, calculators, challenges, video series, audits, swipe files) with conversion rates and implementation notes
- [psychology.md](references/psychology.md): 7 psychological triggers (reciprocity, specificity bias, loss aversion, social proof, authority, scarcity, curiosity gap) + commitment ladder + quick win effect + trust equation
- [saas-magnets.md](references/saas-magnets.md): SaaS-specific lead magnet strategies (free tools, ROI calculators, freemium, templates)
- [services-magnets.md](references/services-magnets.md): Service business strategies (audits, whitepapers, case studies, consultations)
- [info-product-magnets.md](references/info-product-magnets.md): Info product strategies (Brunson, Porterfield, Flynn, Levesque, Forleo, Robbins)

---

## Related Skills

- **audience-research**: Identify pain points before choosing a lead magnet topic
- **brand-voice**: Establish voice before writing
- **email-sequences**: Build longer nurture sequences after the initial follow-up
- **direct-response-copy**: Write the landing page with conversion copy principles
- **content-atomizer**: Promote the lead magnet across social channels
