---
name: pitch-deck
description: Create a pitch deck for a business, product, or idea. Standard structure — Problem, Solution, Market Size, Product, Business Model, Traction, Team, The Ask. Each slide gets title, 3 key bullet points, and speaker notes. 10-12 slides. Use when user needs a "pitch deck", "investor deck", "business pitch", or "product pitch".
---

## Load Context First

Before executing this skill, read the following files from the project folder if they exist:

1. **USER.md** — who the user is, how they think, how they work
2. **BUSINESS.md** — their business, products, positioning, brand voice, content strategy
3. **ICP.md** — their ideal customer, their language, their fears, what makes them buy
4. **Voice or brand voice skill** — look for any installed skill related to voice, tone, or brand voice and apply it automatically
5. Any additional context provided by the user in this session

Use all context silently. Do not reference or summarize files unless asked.

---

# Pitch Deck Builder

**Purpose:** Create a compelling pitch deck (10-12 slides) that tells a clear story: here's the problem, here's our solution, here's why we'll win. Each slide is designed for maximum impact with minimal text.

## Slide Structure

### Slide 1: Title
- Company/Product name
- One-line tagline (the transformation or value prop)
- Presenter name and date

### Slide 2: The Problem
- **Title:** The problem you're solving
- 3 bullets: specific pain points your audience/market experiences
- **Speaker notes:** Tell the story of the problem. Make it relatable. Use a specific example.

### Slide 3: The Solution
- **Title:** How you solve it
- 3 bullets: what your product/service does differently
- **Speaker notes:** Bridge from the problem. "What if instead of X, you could Y?"

### Slide 4: Market Size
- **Title:** The opportunity
- 3 data points: TAM (Total Addressable Market), SAM, SOM — or market size, growth rate, and target segment
- **Speaker notes:** Why this market is big enough and growing. Why now.

### Slide 5: Product / How It Works
- **Title:** What we've built
- 3 bullets: core features or key differentiators
- **Speaker notes:** Walk through the product. Demo moment if presenting live. Show, don't tell.

### Slide 6: Business Model
- **Title:** How we make money
- 3 bullets: revenue model, pricing, unit economics
- **Speaker notes:** Keep it simple. Show the math works.

### Slide 7: Traction
- **Title:** What we've accomplished
- 3 key metrics: users, revenue, growth rate, partnerships, or other proof points
- **Speaker notes:** This is your credibility slide. Lead with the most impressive metric. Show momentum.

### Slide 8: Competitive Landscape
- **Title:** Why us vs. alternatives
- 3 bullets: key differentiators
- **Speaker notes:** Don't trash competitors. Show your unique positioning. Why are you the team to win this?

### Slide 9: Team
- **Title:** Who's behind this
- Key team members: name, role, relevant credential
- **Speaker notes:** Why this specific team is uniquely qualified. Relevant experience, domain expertise, track record.

### Slide 10: The Ask
- **Title:** What we need
- 3 bullets: what you're raising/requesting, what it will be used for, target milestones
- **Speaker notes:** Be specific. "$500K to reach 1,000 paying users and achieve break-even by Q4."

### Slides 11-12 (Optional)
- **Roadmap** — Key milestones for next 12-18 months
- **Contact / Thank You** — How to reach you, next steps

## Output Format

```markdown
# Pitch Deck: [Company/Product Name]

**Slides:** [X]
**Purpose:** [What this pitch is for — fundraising, partnership, client, internal]

---

## Slide 1: [Title]
### [Company Name]
*[Tagline]*

[Presenter Name] | [Date]

**Speaker notes:** [What to say]

---

## Slide 2: The Problem
### [Title]

• [Bullet 1]
• [Bullet 2]
• [Bullet 3]

**Speaker notes:** [What to say — 3-5 sentences]

---

[Continue for all 10-12 slides...]

---

## Presentation Tips

- **Time:** Aim for 10-15 minutes total
- **Rule of 3:** Max 3 bullets per slide
- **Story arc:** Problem → Solution → Proof → Ask
- **Data:** Every claim should have a number behind it
- **Energy:** Open strong, close stronger
```

## Quality Checklist

- [ ] 10-12 slides (not more)
- [ ] Max 3 bullet points per slide
- [ ] Speaker notes for every slide (what to actually say)
- [ ] Problem slide creates urgency
- [ ] Solution slide is clear and differentiated
- [ ] Traction slide has real metrics or honest "pre-launch" framing
- [ ] The Ask is specific (amount, use of funds, milestones)
- [ ] Story flows logically from problem → solution → proof → ask
- [ ] All info sourced from user input (no fabricated metrics)
- [ ] Presentation tips included
