---
name: slogan-generator
description: Generate and evaluate marketing slogans for any product or service. Creates options across multiple angles, scores against criteria, and recommends the best fit.
triggers:
  - slogan
  - tagline
  - marketing slogan
  - brand slogan
  - company tagline
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Marketing Slogan Generator

Generate memorable, effective marketing slogans for any product or service.

## Information Gathering

Ask the user for:

1. **Product/Service name** - What are we creating a slogan for?
2. **What it does** - Core benefit or function (one sentence)
3. **Target audience** - Who is this for?
4. **Brand personality** - (e.g., professional, playful, bold, trustworthy)
5. **Key differentiator** - What makes it different from competitors?
6. **Any words/themes to include or avoid?**

## Slogan Categories

Generate 2-3 slogans in each category (10-15 total):

### 1. Benefit-Focused
Highlight what the customer gets:
- "Save time, not money" (benefit: efficiency)
- "Sleep better tonight" (benefit: peace of mind)

### 2. Emotional Appeal
Connect on a feeling:
- "Because you're worth it" (L'Oréal)
- "Think different" (Apple)

### 3. Clever Wordplay
Memorable through language:
- "Every kiss begins with Kay" (Kay Jewelers)
- "The quicker picker upper" (Bounty)

### 4. Aspirational
Paint a vision of success:
- "Just do it" (Nike)
- "Impossible is nothing" (Adidas)

### 5. Problem-Solution
Address the pain point directly:
- "Got milk?" (California Milk Board)
- "Melts in your mouth, not in your hands" (M&M's)

### 6. Brand Promise
Make a commitment:
- "When it absolutely, positively has to be there overnight" (FedEx)
- "15 minutes could save you 15%" (GEICO)

## Evaluation Criteria

Score each slogan 1-5 on:

| Criterion | What It Measures |
|-----------|------------------|
| **Memorable** | Easy to recall after one hearing |
| **Clear** | Meaning is immediately understood |
| **Differentiating** | Couldn't be used by a competitor |
| **On-brand** | Matches the brand personality |
| **Versatile** | Works across different media/contexts |
| **Timeless** | Won't feel dated in 5 years |

## Output Format

```markdown
## Slogan Options for [Product/Service]

### Benefit-Focused
1. "[Slogan]" - [Brief rationale]
2. "[Slogan]" - [Brief rationale]

### Emotional Appeal
3. "[Slogan]" - [Brief rationale]
4. "[Slogan]" - [Brief rationale]

### Clever Wordplay
5. "[Slogan]" - [Brief rationale]
6. "[Slogan]" - [Brief rationale]

### Aspirational
7. "[Slogan]" - [Brief rationale]
8. "[Slogan]" - [Brief rationale]

### Problem-Solution
9. "[Slogan]" - [Brief rationale]
10. "[Slogan]" - [Brief rationale]

### Brand Promise
11. "[Slogan]" - [Brief rationale]
12. "[Slogan]" - [Brief rationale]

---

## Evaluation Matrix

| # | Slogan | Memorable | Clear | Different | On-brand | Versatile | Timeless | **Total** |
|---|--------|-----------|-------|-----------|----------|-----------|----------|-----------|
| 1 | "..." | 4 | 5 | 3 | 4 | 5 | 4 | **25** |
| 2 | "..." | 5 | 4 | 4 | 5 | 4 | 3 | **25** |
...

---

## Top 3 Recommendations

### 1st Choice: "[Slogan]"
**Score: X/30**
Why it works: [2-3 sentences on why this is the best fit]

### 2nd Choice: "[Slogan]"
**Score: X/30**
Why it works: [2-3 sentences]

### 3rd Choice: "[Slogan]"
**Score: X/30**
Why it works: [2-3 sentences]

---

## Usage Suggestions

For the winning slogan, suggest:
- Where to use it (website header, ads, packaging, email signatures)
- How to pair it with the logo
- Variations for different contexts if needed
```

## Slogan Best Practices

### Length
- **Ideal**: 3-6 words
- **Maximum**: 8 words
- Shorter = more memorable

### Sound
- Alliteration helps ("Best Buy")
- Rhythm matters ("Finger lickin' good")
- Rhyme when natural, not forced

### Clarity
- Avoid jargon
- Skip the cleverness if it obscures meaning
- Test: Can someone understand it without context?

### Uniqueness
- Search existing slogans to avoid overlap
- Ensure it couldn't describe a competitor
- Check for unintended meanings

## What This Skill Does NOT Do

- Generate logos or visual assets
- Create full brand identity systems
- Write marketing plans
- Trademark searches (recommend user verify availability)

## When to Use This vs. Other Skills

| Use `slogan-generator` when... | Use other skills when... |
|---------------------------------|--------------------------|
| Need a tagline/slogan | Need full brand positioning (`value-prop-sharpener`) |
| Launching a new product | Need attention-grabbing hooks (`hook-writer`) |
| Rebranding | Need landing page copy (`landing-page-builder`) |
| Campaign theme | Need full marketing strategy (`marketing-strategy`) |
