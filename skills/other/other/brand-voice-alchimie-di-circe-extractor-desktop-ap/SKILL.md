---
name: brand_voice
description: Brand tone consistency, voice guidelines calibration, and messaging framework alignment
when_to_use: Before writing any customer-facing content, when calibrating tone for a specific platform or audience, or when auditing existing copy for brand consistency
references:
  - references/voice-calibration-guide.md
  - references/tone-spectrum.md
---

# Brand Voice Skill

## Overview

This skill provides a systematic approach to brand voice application: extracting voice guidelines from the RAG knowledge base, calibrating tone for specific platforms and audiences, and auditing content for brand consistency.

## Tools to Use

- **RAG (brand_guidelines)**: Primary source for brand voice, values, and messaging
- **Perplexity**: Research how the brand category typically communicates; identify differentiation
- **Jina**: Analyze existing brand content on website/social for voice audit

## Brand Voice Components

### The 4 Dimensions of Brand Voice

1. **Tone** — How does the brand "feel"?
   - Spectrum: Formal ←→ Conversational
   - Spectrum: Serious ←→ Playful
   - Spectrum: Authoritative ←→ Humble
   - Spectrum: Inspirational ←→ Practical

2. **Vocabulary** — What words does the brand use/avoid?
   - Brand-specific terms and phrases
   - Words to actively use (power words)
   - Words to avoid (corporate-speak, clichés)
   - Technical vocabulary level

3. **Rhythm** — How does the brand structure sentences?
   - Short, punchy sentences vs. flowing prose
   - Use of lists vs. narrative paragraphs
   - Punctuation style (minimal vs. expressive)
   - Cadence (fast/urgent vs. measured/thoughtful)

4. **Persona** — Who is the brand in the reader's mind?
   - Role archetype (Mentor? Peer? Expert? Guide?)
   - Level of familiarity (use "you" / "we" / formal)
   - Cultural references and humor level

## Workflow

### Step 1 — Load Brand Voice from RAG

Query the brand_guidelines RAG source for:
- Brand personality descriptors (3–5 adjectives)
- Explicit do's and don'ts for copy
- Example copy that exemplifies the brand voice
- Core values that should permeate all communication

### Step 2 — Platform Calibration

Brand voice is constant, but **tone adjusts per platform**:

| Platform | Tone Adjustment | Length | Formality |
|----------|----------------|--------|-----------|
| LinkedIn | More professional, industry-credible | Medium-long | Semi-formal |
| Instagram | Warmer, visual-first, approachable | Short | Conversational |
| Email newsletter | Personal, direct, trusted advisor | Variable | Varies |
| Blog/Article | Educational, authoritative, thorough | Long | Semi-formal |
| Website copy | Clear, benefit-focused, trustworthy | Short-medium | Semi-formal |

### Step 3 — Audience Calibration

Adjust vocabulary and complexity for:
- **C-suite**: Strategic, outcome-focused, minimal jargon
- **Practitioners/Professionals**: Specific, technical where earned, peer-to-peer
- **General audience**: Plain language, relatable examples, no industry terms

### Step 4 — Voice Audit (for existing content)

When reviewing content for brand consistency, check:

**Tone checklist**:
- [ ] Does the opening line sound like the brand?
- [ ] Is the formality level consistent throughout?
- [ ] Are there any phrases that feel "off-brand"?
- [ ] Does it end with the right emotional note?

**Vocabulary audit**:
- [ ] No off-brand words used
- [ ] Brand's preferred terminology applied correctly
- [ ] No jargon unless appropriate for audience
- [ ] Consistent pronoun use (you/we/our)

**Rhythm check**:
- [ ] Sentence length variation appropriate to brand
- [ ] Paragraph breaks align with brand style
- [ ] Lists vs. prose ratio correct for platform

### Step 5 — Voice Calibration for Drafts

Before writing new content:

1. Identify the 3 brand voice adjectives most relevant to THIS piece
2. Write a "voice reminder" sentence (e.g., "Write as if you're a trusted mentor who is direct, warm, and backed by data")
3. After drafting: read aloud — does it sound like the brand?

### Step 6 — Voice Consistency Score

Rate drafted content 1–5 on each dimension:
- Tone alignment: [1–5]
- Vocabulary fit: [1–5]
- Rhythm match: [1–5]
- Persona consistency: [1–5]

Minimum threshold: 4+ on all dimensions before approving content.

## Output Format

```markdown
## Brand Voice Brief

**Platform**: [LinkedIn / Instagram / Blog / etc.]
**Audience**: [Target reader profile]
**Content goal**: [Awareness / Engagement / Conversion]

### Active Voice Profile for This Piece
- **Tone**: [3 adjectives from brand voice]
- **Formality**: [1–5, where 1=very casual, 5=very formal]
- **Persona**: [Brand as: Mentor / Peer / Expert / etc.]
- **Key vocabulary**: [Words to use prominently]
- **Words to avoid**: [Off-brand terms]
- **Rhythm**: [Short & punchy / Flowing narrative / Mixed]

### Voice Audit (if reviewing existing content)
- Tone alignment: [1–5] — [notes]
- Vocabulary fit: [1–5] — [notes]
- Rhythm match: [1–5] — [notes]
- Persona consistency: [1–5] — [notes]
- **Recommended edits**: [specific changes]

### Voice Calibration Sentence
"[Write this piece as if you are a [persona] who is [adjectives]...]"
```

## Notes

- Always query brand_guidelines RAG first — do not invent a voice profile
- When brand_guidelines are sparse: use Jina to extract voice from existing brand content on website/social
- For multi-brand projects: create separate voice profiles per brand; never blend
- Italian language brands: pay attention to cultural register (formal "Lei" vs. informal "tu") as this is a brand decision, not just grammar
