---
name: claim-extraction
description: Extract structured claims, predictions, hints, and opinions from AI research content. Use when processing tweets, blog posts, substacks, or other content from AI researchers to identify substantive assertions about AI capabilities, limitations, and progress.
---

# Claim Extraction Skill

Extract all substantive claims from AI research content. A claim is any assertion that:
- States something as true about AI capabilities, limitations, or progress
- Predicts future developments
- Hints at unreleased work
- Expresses a positioned opinion on the field's direction
- Critiques others' claims or work

## Extraction Schema

For each claim, extract:

### 1. claimText
The claim in clear, standalone form. Paraphrase if needed for clarity.

### 2. claimType
- `fact`: Assertion about current state ("GPT-4 can do X")
- `prediction`: Forward-looking ("By 2026, we'll have...")
- `hint`: Implies unreleased work ("We've been seeing interesting results with...")
- `opinion`: Positioned take ("I think scaling is/isn't sufficient")
- `critique`: Challenges others ("Marcus is wrong because...")
- `question`: Genuine uncertainty expressed ("I'm not sure if...")

### 3. topic
Primary topic category:
- `scaling`: Scaling laws, compute, training efficiency
- `reasoning`: LLM reasoning, chain-of-thought, planning
- `agents`: AI agents, tool use, autonomy
- `safety`: AI safety, alignment, control
- `interpretability`: Mechanistic interpretability
- `multimodal`: Vision, audio, video models
- `rlhf`: RLHF, preference learning, Constitutional AI
- `benchmarks`: Evals, benchmarks, capability measurement
- `infrastructure`: Training infra, chips, hardware
- `policy`: AI policy, regulation, governance
- `general`: General AI commentary

### 4. stance
- `bullish`: Optimistic about AI progress/capabilities
- `bearish`: Skeptical/pessimistic about AI progress
- `neutral`: Balanced or factual without clear stance

### 5. bullishness
Float from 0.0 (maximally bearish) to 1.0 (maximally bullish)

### 6. confidence
How confident does the author seem? (0.0-1.0)
- Hedging language: "might", "could", "I think", "possibly" → lower
- Certainty language: "will", "definitely", "it's clear that" → higher

### 7. timeframe (for predictions)
- `near-term`: < 1 year
- `medium-term`: 1-3 years
- `long-term`: 3-10 years
- `unspecified`: No clear timeframe
- `null`: Not a prediction

### 8. evidenceProvided
- `strong`: Cites data, papers, or detailed reasoning
- `moderate`: Some reasoning but not rigorous
- `weak`: Assertion without support
- `appeal-to-authority`: "Trust me, I work on this"

### 9. quoteworthiness
Is this claim notable enough to quote in a digest? (0.0-1.0)

## Output Format

Return JSON:
```json
{
  "claims": [
    {
      "claimText": "The claim in clear form",
      "claimType": "prediction",
      "topic": "reasoning",
      "stance": "bullish",
      "bullishness": 0.8,
      "confidence": 0.7,
      "timeframe": "medium-term",
      "evidenceProvided": "moderate",
      "quoteworthiness": 0.6,
      "relatedTo": ["o1", "chain-of-thought"],
      "originalQuote": "Brief relevant quote if notable"
    }
  ]
}
```

## Guidelines

- Extract MULTIPLE claims from a single piece of content if present
- Don't over-extract - only substantive, meaningful claims
- A tweet saying "Interesting paper" is NOT a claim
- Look for IMPLICIT claims ("We've made a lot of progress" implies capability gains)
- Pay attention to WHO is speaking - lab researchers hinting at their own work is high signal
- Critics often make claims by contradiction ("X is wrong, therefore Y")

## Author Context Matters

Consider the author's affiliation when assessing:
- **Lab researchers** (Anthropic, OpenAI, DeepMind): May hint at unreleased work
- **Critics** (Marcus, Chollet, Mitchell): Often make claims through critique
- **Independent** (Simon Willison, Jim Fan): Provide practitioner perspectives
