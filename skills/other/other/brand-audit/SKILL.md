---
name: brand-audit
description: Score any piece of content against the user's brand voice and context files. Rates voice consistency, ICP alignment, and tone match (1-10 each). Flags off-brand sentences with explanations and suggests rewrites. Use when user wants a "brand audit", "content review", "voice check", or wants to evaluate if content is on-brand.
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

# Brand Audit

**Purpose:** Score a piece of content against the user's brand voice and context profiles. Identify what's on-brand, what's off-brand, and provide specific rewrites for the weakest sections.

## When to Activate

Use this skill when:
- User wants to audit content against their brand
- User mentions "brand check", "voice review", or "is this on-brand?"
- User provides content and wants feedback on consistency
- User wants to evaluate ghostwritten or AI-generated content

## Requirements

**Must have:** At least one context file (BUSINESS.md, ICP.md, or a voice skill) to audit against. Without context files, there's no standard to measure against — ask the user to provide or build them first.

**Must provide:** The content to be audited.

## Scoring Framework

### Dimension 1: Voice Consistency (1-10)
How well does the content match the established voice?
- **Sentence rhythm** — Does it match their natural patterns?
- **Vocabulary** — Are these words they would use?
- **Tone** — Does it feel like them?
- **Personality** — Is their character coming through?

**Scoring guide:**
- 9-10: Indistinguishable from their best writing
- 7-8: Mostly them with minor slips
- 5-6: Recognizably them but inconsistent
- 3-4: Partially off — mixing their voice with generic
- 1-2: Doesn't sound like them at all

### Dimension 2: ICP Alignment (1-10)
How well does the content speak to the ideal customer?
- **Pain points addressed** — Does it touch what the ICP cares about?
- **Language match** — Are these words the ICP uses?
- **Value delivered** — Would the ICP find this useful?
- **Emotional resonance** — Does it connect with their fears/aspirations?

### Dimension 3: Tone Match (1-10)
How well does the tone match the brand guidelines?
- **Formality level** — Too casual? Too corporate?
- **Energy level** — Too enthusiastic? Too flat?
- **Confidence level** — Too hedging? Too aggressive?
- **Approachability** — Too distant? Too familiar?

## Process

### Step 1: Read and internalize all context files
### Step 2: Read the content to be audited
### Step 3: Score each dimension with specific evidence
### Step 4: Flag off-brand sentences with explanations
### Step 5: Provide rewrites for the 3 weakest sections

## Output Format

```markdown
# Brand Audit Report

**Content audited:** [Title or first line]
**Audited against:** [Which context files were used]

---

## Scores

| Dimension | Score | Summary |
|-----------|-------|---------|
| Voice Consistency | [X]/10 | [One-sentence assessment] |
| ICP Alignment | [X]/10 | [One-sentence assessment] |
| Tone Match | [X]/10 | [One-sentence assessment] |
| **Overall** | **[avg]/10** | **[Overall assessment]** |

---

## What's Working ✅

1. **[Specific element]** — [Why it's on-brand, with quote from content]
2. **[Specific element]** — [Why it's on-brand]
3. **[Specific element]** — [Why it's on-brand]

---

## Off-Brand Flags ⚠️

### Flag 1: [Category — e.g., "Voice slip"]
**Sentence:** "[Exact quote from the content]"
**Issue:** [Specific explanation of why this is off-brand]
**Should sound like:** [What it would sound like in their voice]

### Flag 2: [Category]
**Sentence:** "[Exact quote]"
**Issue:** [Explanation]
**Should sound like:** [Corrected version]

### Flag 3: [Category]
[Continue for all flags...]

---

## Top 3 Rewrites

### Rewrite 1: [Section/paragraph being rewritten]

**Original:**
> [Original text]

**Rewritten (on-brand):**
> [Rewritten version that matches voice and brand]

**What changed:** [Brief explanation of the changes]

### Rewrite 2:
[Same format...]

### Rewrite 3:
[Same format...]

---

## Quick Wins

To bring this content fully on-brand:
1. [Most impactful single change]
2. [Second most impactful change]
3. [Third change]
```

## Quality Checklist

- [ ] All three dimensions scored with specific evidence
- [ ] Scores are honest (not inflated to be nice)
- [ ] Off-brand flags include exact quotes from the content
- [ ] Each flag has a specific explanation (not just "this is off")
- [ ] 3 rewrites provided for the weakest sections
- [ ] Rewrites genuinely match the brand voice
- [ ] "What's Working" section acknowledges strengths
- [ ] Quick wins are actionable and prioritized
- [ ] Audit is based on context files (not just general writing advice)
