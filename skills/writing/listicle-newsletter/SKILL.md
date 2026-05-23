---
name: listicle-newsletter
description: Write a numbered listicle newsletter — "7 things I learned", "5 mistakes", "10 lessons" format. Each item gets a bold takeaway + 2-3 sentence explanation. Fast to write, high engagement. 600-1000 words. Use when user wants a list-based newsletter, mentions "X things I learned", "mistakes", "lessons", or wants a scannable, numbered format.
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

# Listicle Newsletter

**Purpose:** Write a numbered list newsletter (600-1,000 words) that delivers fast, scannable value. Each item is a bold takeaway with a tight explanation. This format is high-engagement because readers can skim the bold items and go deeper on what interests them.

## When to Activate

Use this skill when:
- User wants a list-based newsletter ("7 things I learned", "5 mistakes", etc.)
- User mentions "listicle", "lessons", "mistakes", "things I learned"
- User wants fast, scannable content
- User has a collection of related insights to package

## Why Listicles Work

- **Scannable** — readers get value from bold items alone
- **Low commitment** — each item is self-contained, no reading the whole thing required
- **High shareability** — individual items are quotable and forwardable
- **Easy to write** — once you have the items, execution is fast
- **Predictable structure** — readers know what they're getting

## Structure

### Opening (50-100 words)

Brief context for the list. Why these items matter. What prompted this collection.

**Patterns:**
- "I've been [doing X] for [timeframe]. Here are [number] things I wish I knew earlier."
- "After [experience], I realized [number] things about [topic] that changed everything."
- "[Number] lessons from [specific experience] — one for each [clever framing]."

**Rules:**
- Keep it under 100 words
- Set up WHY this list matters
- Don't over-explain — let the list speak for itself

### The List (500-800 words)

**For each item:**

1. **Bold headline** — The takeaway in one sentence. Should deliver value even if the reader skips the explanation.
2. **Explanation** — 2-3 sentences that add context, an example, or a "why this matters" reasoning.

**Format:**
```
### 1. [Bold takeaway as a complete sentence.]

[2-3 sentences expanding on the takeaway. Include a specific example, a personal experience, or a logical explanation of why this is true. End with an actionable implication or memorable phrasing.]
```

**Ideal number of items:** 5-10 (sweet spot is 7)
- 3-4 items feels thin
- 12+ items loses focus
- Odd numbers (5, 7, 9) psychologically feel more natural

**Item ordering strategies:**
- **Strongest first** — hook them immediately, then maintain interest
- **Build to strongest** — save the best for last, create momentum
- **Alternate intensity** — mix lighter items with heavier ones for pacing

### Closing (30-50 words)

Short wrap-up. Don't over-summarize — the list IS the content.

**Patterns:**
- "Pick one. Start there."
- "If I had to keep just one of these, it'd be #[X]. That one changed everything."
- "[Brief forward-looking statement about applying these.]"

## Subject Lines

**Generate 5 options using these patterns:**

1. **X things I learned**: "[Number] things I learned about [topic]"
2. **X mistakes**: "[Number] mistakes [audience] makes with [topic]"
3. **X lessons from**: "[Number] lessons from [specific experience]"
4. **X rules**: "My [number] rules for [topic]"
5. **X things nobody tells you**: "[Number] things nobody tells you about [topic]"

**Requirements:** Sentence-case. Number first works well. Be specific about the topic.

## Output Format

```
## Subject Line Options

1. [Option 1]
2. [Option 2]
3. [Option 3]
4. [Option 4]
5. [Option 5]

**Recommended**: Option [X] — [reasoning]

---

## Newsletter: [Chosen Subject Line]

**Word count**: ~[X] words

---

[Opening — 50-100 words setting up the list]

### 1. [Bold takeaway sentence.]

[2-3 sentence explanation with example or reasoning.]

### 2. [Bold takeaway sentence.]

[2-3 sentence explanation.]

### 3. [Bold takeaway sentence.]

[2-3 sentence explanation.]

[Continue for all items...]

---

[Closing — 30-50 words]

---

**Stats**: [X] words | [X] items | Top pick: #[X]
```

## Quality Checklist

- [ ] Opening is under 100 words and sets up WHY
- [ ] Each item has a bold headline that delivers value standalone
- [ ] Each explanation is 2-3 sentences (no more)
- [ ] Items are specific, not generic ("write better" = bad, "write the headline before the body" = good)
- [ ] 5-10 items (sweet spot: 7)
- [ ] Closing is under 50 words
- [ ] 600-1,000 words total
- [ ] Bold headlines alone tell a complete story if you just skim them
- [ ] No filler items — every item earns its spot
- [ ] Voice matches context profiles

## What Makes Great Listicle Items

**Strong items:**
- Specific and actionable ("Track your time for one week before optimizing anything")
- Surprising or counterintuitive ("The best content idea is the one you're avoiding writing")
- Grounded in experience ("I wasted 6 months on X before realizing Y")

**Weak items:**
- Vague platitudes ("Work hard and stay consistent")
- Obvious advice everyone already knows ("Post regularly on social media")
- Items that need a paragraph of context to make sense (the headline should stand alone)
