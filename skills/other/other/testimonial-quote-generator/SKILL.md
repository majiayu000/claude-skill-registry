---
name: generating-testimonial-quotes
description: Extracts and formats compelling quotes from customer feedback for marketing use. Use when the user asks about testimonials, customer quotes, review extraction, social proof, or quote cards.
---

# Quote & Testimonial Generator

## When to use this skill

- User asks to extract testimonials
- User needs customer quotes for marketing
- User wants to format reviews
- User mentions social proof content
- User needs quote graphics or cards

## Workflow

- [ ] Gather source feedback
- [ ] Identify usable quotes
- [ ] Format for different uses
- [ ] Tag by use case
- [ ] Create visual specifications
- [ ] Organize testimonial library

## Instructions

### Step 1: Identify Quote Sources

**Common feedback sources:**

| Source          | Where to Find                     | Quote Quality               |
| --------------- | --------------------------------- | --------------------------- |
| Reviews         | Google, G2, Capterra, Trustpilot  | High - public, verified     |
| Emails          | Support inbox, thank-you messages | Medium - permission needed  |
| Surveys         | NPS, CSAT, post-purchase          | High - direct feedback      |
| Social          | Comments, DMs, mentions           | Medium - permission needed  |
| Interviews      | Customer calls, case study chats  | High - detailed context     |
| Slack/Discord   | Community channels                | Medium - permission needed  |
| Support tickets | Resolved positive tickets         | Medium - ask for permission |

**Permission requirements:**

```markdown
## Before Using a Quote

- [ ] Quote is from public review (Google, G2, etc.) - no permission needed
- [ ] Quote is from private communication - written permission required
- [ ] Customer name and company approved for use
- [ ] Photo usage approved (if applicable)
- [ ] Quote has not been materially altered (minor edits OK)
```

### Step 2: Quote Identification Criteria

**What makes a strong testimonial:**

| Criteria            | Weak Example     | Strong Example                             |
| ------------------- | ---------------- | ------------------------------------------ |
| Specific results    | "Great product!" | "Increased our revenue 47% in 3 months"    |
| Emotional impact    | "Happy customer" | "Finally, I can sleep at night knowing..." |
| Addresses objection | "Works well"     | "I was skeptical at first, but..."         |
| Relatable problem   | "Helpful tool"   | "We struggled with X for years until..."   |
| Credible source     | "John D."        | "Sarah Chen, VP Marketing, Acme Corp"      |

**Quote scoring rubric:**

| Element                           | Points |
| --------------------------------- | ------ |
| Contains specific metric/result   | +3     |
| Names specific feature/benefit    | +2     |
| Includes emotional language       | +2     |
| Overcomes common objection        | +2     |
| From recognizable company/title   | +2     |
| Mentions competitor comparison    | +1     |
| Short and punchy (under 50 words) | +1     |

**Score interpretation:**

- 8-13: A-tier (hero testimonials, landing pages)
- 5-7: B-tier (feature sections, emails)
- 2-4: C-tier (social proof bars, volume displays)

### Step 3: Quote Extraction Patterns

**Look for these phrases:**

```markdown
## High-Value Phrase Patterns

**Result indicators:**

- "We increased/decreased..."
- "Saved us X hours/dollars..."
- "Within X weeks/months..."
- "X% improvement in..."

**Emotional indicators:**

- "Finally..."
- "Game-changer..."
- "Can't imagine going back to..."
- "Wish I had found this sooner..."

**Objection overcomers:**

- "I was skeptical, but..."
- "At first I thought..., but then..."
- "Worth every penny..."
- "Even though [price/concern], we still..."

**Comparison indicators:**

- "Unlike [competitor]..."
- "We tried X before, but..."
- "The only solution that..."
- "Better than..."
```

### Step 4: Quote Formatting

**Raw quote to polished testimonial:**

**Before (raw):**

```
"yeah so we had been using spreadsheets for like 2 years and
it was a total mess, then we found your tool and honestly
within like 3 weeks everything was organized and we saved
probably 10 hours a week on reporting alone, my boss was
super impressed lol"
```

**After (formatted):**

```
"We'd been using spreadsheets for 2 years and it was a mess.
Within 3 weeks of switching to [Product], everything was
organized and we saved 10 hours a week on reporting alone."

— Jamie Torres, Operations Manager, TechStart Inc.
```

**Editing guidelines:**

| Allowed                                  | Not Allowed                  |
| ---------------------------------------- | ---------------------------- |
| Remove filler words (um, like, you know) | Change meaning               |
| Fix grammar/spelling                     | Add claims they didn't make  |
| Shorten for clarity                      | Combine separate quotes      |
| Add context in brackets                  | Invent attribution           |
| Clean up transcript artifacts            | Remove qualifying statements |

### Step 5: Quote Templates by Use Case

**Landing page hero:**

```markdown
## [Short, punchy quote - 15-25 words]

"[Specific result] + [Emotional impact] + [Recommendation]"

— [Full Name], [Title], [Company]
[Optional: Company logo]
```

**Example:**

```markdown
"TaskFlow cut our project delays by 60%. For the first time,
we actually finish sprints on time. Every team needs this."

— Alex Rivera, Engineering Lead, ScaleUp
[ScaleUp logo]
```

**Feature section proof:**

```markdown
### [Feature Name]

[Feature description]

> "[Quote specifically about this feature - 20-40 words]"
> — [Name], [Company]
```

**Social proof bar (short quotes):**

```markdown
⭐⭐⭐⭐⭐ "[5-10 word snippet]" — [Name, Company]
⭐⭐⭐⭐⭐ "[5-10 word snippet]" — [Name, Company]
⭐⭐⭐⭐⭐ "[5-10 word snippet]" — [Name, Company]
```

**Email testimonial:**

```markdown
---

💬 What our customers say:

"[Full quote - 30-50 words with specific result]"

— [Name], [Title] at [Company]

---
```

**Social media quote card:**

```markdown
## Quote Card Specs

**Text:** "[Quote - 80 characters max for readability]"
**Attribution:** [Name] | [Company]
**Background:** [Brand color or photo]
**Dimensions:** 1080x1080 (Instagram) or 1200x628 (LinkedIn)
**Font size:** Quote 32-48pt, Attribution 18-24pt
```

### Step 6: Quote Tagging System

**Tag each quote for easy retrieval:**

| Tag Category        | Options                                       |
| ------------------- | --------------------------------------------- |
| Use case            | Hero, feature, email, social, ad, case study  |
| Strength            | A-tier, B-tier, C-tier                        |
| Topic               | Onboarding, support, features, results, value |
| Objection addressed | Price, complexity, trust, competition         |
| Industry            | SaaS, e-commerce, agency, enterprise          |
| Buyer persona       | Decision maker, end user, influencer          |
| Platform approved   | Website, social, ads, print                   |

### Step 7: Testimonial Library Template

```markdown
## Testimonial Library

### A-Tier (Hero Testimonials)

| ID   | Quote     | Attribution          | Use Cases          | Tags                |
| ---- | --------- | -------------------- | ------------------ | ------------------- |
| T001 | "[Quote]" | Name, Title, Company | Hero, landing page | Results, enterprise |
| T002 | "[Quote]" | Name, Title, Company | Homepage, ads      | ROI, decision-maker |

### B-Tier (Feature & Email)

| ID   | Quote     | Attribution   | Best For         | Tags            |
| ---- | --------- | ------------- | ---------------- | --------------- |
| T003 | "[Quote]" | Name, Company | Feature sections | Ease of use     |
| T004 | "[Quote]" | Name, Company | Email campaigns  | Support quality |

### C-Tier (Social Proof Volume)

| ID   | Short Quote       | Attribution   | Platform         |
| ---- | ----------------- | ------------- | ---------------- |
| T005 | "[Short snippet]" | Name, Company | Social proof bar |
| T006 | "[Short snippet]" | Name, Company | Footer           |

### By Objection

**Price concerns:**

- T002: "[Quote about value/ROI]"

**Complexity concerns:**

- T003: "[Quote about ease of use]"

**Trust concerns:**

- T001: "[Quote with specific results]"
```

### Step 8: Visual Quote Formats

**Quote card specifications:**

| Platform        | Dimensions | Max Quote Length |
| --------------- | ---------- | ---------------- |
| Instagram post  | 1080x1080  | 80-100 chars     |
| Instagram story | 1080x1920  | 60-80 chars      |
| LinkedIn post   | 1200x628   | 100-120 chars    |
| Twitter         | 1200x675   | 80-100 chars     |
| Facebook        | 1200x630   | 100-120 chars    |
| Website hero    | 1920x1080  | 120-150 chars    |

**Visual elements:**

```markdown
## Quote Card Layout

┌─────────────────────────────┐
│ │
│ "[Quote text here, │
│ keeping it short │
│ and impactful]" │
│ │
│ ───────────────── │
│ │
│ [Photo] Name │
│ Title, Company │
│ │
│ ⭐⭐⭐⭐⭐ │
│ │
└─────────────────────────────┘

**Design notes:**

- Use quotation marks or large quote icon
- High contrast for readability
- Customer photo adds trust (if available)
- Include star rating if applicable
- Keep padding generous
```

### Step 9: Video Testimonial Framework

**If converting quotes to video requests:**

```markdown
## Video Testimonial Request

**Questions to ask:**

1. What problem were you trying to solve before [Product]?
2. What made you choose [Product] over alternatives?
3. What specific results have you achieved?
4. What would you tell someone considering [Product]?

**Ideal length:** 60-90 seconds
**Format:** Horizontal, good lighting, quiet space
**Key soundbites needed:**

- Problem statement (10 sec)
- Solution discovery (10 sec)
- Specific result (15 sec)
- Recommendation (10 sec)
```

### Step 10: Permission Request Template

**Email template for requesting permission:**

```markdown
Subject: Quick permission request - using your feedback

Hi [Name],

Thank you for the kind words about [Product]! Your feedback
means a lot to our team.

We'd love to feature your quote on our website and marketing
materials. Here's what we'd like to use:

"[Quote]"
— [Name], [Title], [Company]

Would you be comfortable with us sharing this? We're happy to:

- Use your full name and title, OR
- Use just first name and company, OR
- Keep it anonymous (if you prefer)

Just reply with "yes" and your preference, and we'll take it
from there.

Thanks again!
[Your name]

P.S. If you have a company logo or headshot you'd like us to
include, feel free to attach it.
```

## Output Format

```markdown
## Testimonial Extraction: [Source/Campaign Name]

**Source:** [Where feedback came from]
**Date reviewed:** [Date]

---

### Extracted Quotes

#### Quote 1 (A-Tier)

**Raw:** "[Original quote]"
**Formatted:** "[Polished quote]"
**Attribution:** [Name], [Title], [Company]
**Best for:** [Use cases]
**Tags:** [Tags]
**Permission:** [Status]

#### Quote 2 (B-Tier)

[Same structure]

---

### Quote Cards Needed

| Quote ID | Platform  | Dimensions | Status        |
| -------- | --------- | ---------- | ------------- |
| Q1       | Instagram | 1080x1080  | Design needed |
| Q2       | LinkedIn  | 1200x628   | Design needed |

---

### Testimonial Library Update

[New entries to add to master library]
```

## Validation

Before completing:

- [ ] Quotes are genuine (not fabricated)
- [ ] Specific results included where possible
- [ ] Attribution is accurate
- [ ] Permission obtained or noted as needed
- [ ] Quotes tagged by use case
- [ ] Visual specs provided for quote cards
- [ ] Original meaning preserved in editing
- [ ] Organized in retrievable library format

## Error Handling

- **No permission obtained**: Mark as "internal use only" until permission granted.
- **Quote too generic**: Ask for more context or look for specific results in same feedback.
- **No attribution available**: Use "Verified customer" or request name from source.
- **Quote is negative**: Flag for customer success follow-up, do not use.
- **Quote mentions competitor**: Check legal guidelines; often fine but verify.

## Resources

- [Senja](https://senja.io/) - Testimonial collection tool
- [Testimonial.to](https://testimonial.to/) - Video testimonials
- [Canva](https://www.canva.com/) - Quote card design
- [Walls.io](https://walls.io/) - Social proof walls
