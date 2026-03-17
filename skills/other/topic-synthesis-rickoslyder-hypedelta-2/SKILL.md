---
name: topic-synthesis
description: Synthesize claims across multiple sources to identify consensus, disagreements, and emerging narratives on AI research topics. Use when you have claims from both lab researchers and critics on the same topic and need to understand where they agree, disagree, and what the overall hype level is.
---

# Topic Synthesis Skill

Synthesize claims from multiple sources to produce a coherent picture of discourse on an AI topic.

## Input Structure

You'll receive claims grouped by source type:
- **Lab researcher claims**: From people at Anthropic, OpenAI, DeepMind, Meta AI, etc.
- **Critic claims**: From credentialed skeptics like Marcus, Chollet, Mitchell, Bender
- **Independent claims**: From independent researchers and practitioners

## Synthesis Components

### 1. Lab Consensus
What do lab researchers generally agree on? Write 2-3 sentences capturing the central themes.

Look for:
- Repeated claims across multiple lab researchers
- Consistent stance on capabilities/limitations
- Shared predictions or timelines

### 2. Critic Consensus
What do critics generally agree on? Write 2-3 sentences capturing the central themes.

Look for:
- Common critiques raised by multiple critics
- Shared concerns about hype or methodology
- Consistent alternative explanations

### 3. Agreements
What do BOTH sides agree on? These are often the most reliable signal.

Examples:
- "Current models struggle with certain forms of reasoning"
- "More compute does improve capabilities"
- "Benchmarks have limitations"

### 4. Disagreements
Where do they fundamentally disagree? Structure as:

```json
{
  "point": "Whether scaling alone leads to AGI",
  "labPosition": "Many believe continued scaling will yield AGI-like capabilities",
  "criticPosition": "Fundamental architectural changes needed beyond scaling"
}
```

### 5. Emerging Narratives
What new framings or narratives are emerging in the discourse?

Examples:
- "Post-training is the new scaling"
- "Reasoning models are hitting walls"
- "Safety concerns are becoming mainstream"

### 6. Notable Predictions
Extract specific predictions with attribution:

```json
{
  "text": "Prediction text",
  "author": "Author name",
  "confidence": 0.7,
  "timeframe": "medium-term"
}
```

### 7. Evidence Quality
Rate overall quality of evidence cited (0.0-1.0):
- 1.0: Multiple papers cited, detailed reasoning, reproducible claims
- 0.7: Some evidence, logical arguments
- 0.4: Mostly opinions with occasional support
- 0.1: Pure speculation, no evidence

## Hype Delta Calculation

Calculate the "hype delta" - the gap between lab enthusiasm and critic skepticism:

```
hypeDelta = avgLabBullishness - avgCriticBullishness
```

Interpretation:
- **Positive delta (> 0.2)**: Labs more bullish → potentially overhyped
- **Negative delta (< -0.2)**: Critics more bullish → potentially underhyped
- **Near zero (-0.2 to 0.2)**: Relatively aligned assessment

## Output Format

Return JSON:
```json
{
  "topic": "reasoning",
  "labConsensus": "Lab researchers believe...",
  "criticConsensus": "Critics argue...",
  "agreements": ["Point 1", "Point 2"],
  "disagreements": [
    {
      "point": "Description",
      "labPosition": "Lab view",
      "criticPosition": "Critic view"
    }
  ],
  "emergingNarratives": ["Narrative 1", "Narrative 2"],
  "predictions": [
    {
      "text": "Prediction",
      "author": "Name",
      "confidence": 0.7,
      "timeframe": "medium-term"
    }
  ],
  "evidenceQuality": 0.6,
  "hypeDelta": {
    "delta": 0.25,
    "labSentiment": 0.75,
    "criticSentiment": 0.50,
    "interpretation": "Moderately overhyped"
  },
  "synthesisNarrative": "Two paragraphs summarizing the current state..."
}
```

## Synthesis Narrative Guidelines

Write a balanced 2-paragraph narrative:

**Paragraph 1**: Current state of the topic
- What's actually happening
- Key developments
- Where there's genuine progress

**Paragraph 2**: Contested areas and outlook
- Where disagreement exists
- What's uncertain
- What to watch for

Maintain balanced tone - acknowledge both genuine progress AND legitimate concerns.
