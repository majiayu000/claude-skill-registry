---
name: hint-detection
description: Detect hints about unreleased AI research or capabilities from lab researcher communications. Use when analyzing tweets, posts, or interviews from people at major AI labs to identify signals about upcoming work.
---

# Hint Detection Skill

Lab researchers often hint at work before publication. This skill identifies these signals.

## Hint Patterns

### 1. Vague Progress Claims
Language that implies results without specifics:
- "We've been seeing interesting results with..."
- "There's been a lot of progress on..."
- "Things are moving faster than people think in..."

### 2. Deflection with Signal
Answers that acknowledge something exists:
- "I can't say much, but..."
- "You'll see soon..."
- "No comment ;)"
- "That's a great question" (followed by non-answer)

### 3. Future Tense Confidence
Certainty about unreleased capabilities:
- "You'll see that..."
- "This will become clear when..."
- "The next generation will..."

### 4. Unusual Enthusiasm
Disproportionate excitement about a topic:
- Sudden interest in a specific area
- Detailed knowledge about approaches not in their published work
- Defending an approach more vigorously than expected

### 5. Specific Denials
Sometimes denial calls attention:
- "We're definitely NOT working on..."
- "That's not what we're focused on" (when they clearly are)
- Overly specific denials

### 6. Timeline Hints
Suggestions about release timing:
- "In the coming weeks/months..."
- "Stay tuned"
- "Sooner than you think"
- Mentions of specific events (conferences, dates)

### 7. Capability Hedging
Language implying current vs future:
- "Current models can't do X yet"
- "With today's approaches..."
- "The bottleneck right now is..."

### 8. Recruitment Signals
Hiring patterns can indicate direction:
- Sudden push for specific expertise
- "We're building a team for..."
- Job postings for unrevealed projects

## Author Context

Weight hints by author credibility:
- **Lab leadership** (Dario, Sam, Demis): High signal, often deliberate
- **Research leads**: Technical hints about their area
- **Individual researchers**: May hint at their specific work
- **Former employees**: Sometimes reveal direction
- **Adjacent figures** (investors, partners): Second-hand signals

## Analysis Framework

For each potential hint:

### 1. Quote the relevant passage
Extract the exact language that suggests a hint.

### 2. Implied capability
What capability or result is being hinted at?

### 3. Confidence level (0.0-1.0)
How confident are you this is a real hint vs. noise?

Consider:
- Author's position and knowledge
- Specificity of language
- Pattern match to known hint types
- Context of conversation

### 4. Estimated timeframe
When might this be revealed?
- `imminent`: Days to weeks
- `near-term`: 1-3 months
- `medium-term`: 3-12 months
- `unclear`: No timing signal

### 5. Domain
What area of AI?
- reasoning, agents, safety, multimodal, scaling, etc.

## Output Format

Return JSON:
```json
{
  "hints": [
    {
      "hintText": "The exact quote suggesting a hint",
      "author": "Author name",
      "affiliation": "Company/org",
      "impliedCapability": "What they're hinting at",
      "confidence": 0.7,
      "reasoning": "Why you think this is a hint",
      "timeframe": "near-term",
      "domain": "reasoning",
      "sourceUrl": "URL if available"
    }
  ],
  "noHintsFound": false
}
```

If no credible hints are detected, return:
```json
{
  "hints": [],
  "noHintsFound": true,
  "notes": "Brief explanation of why content doesn't contain hints"
}
```

## False Positive Avoidance

Not every comment is a hint. Exclude:
- General optimism without specifics
- Restatement of public roadmaps
- Academic speculation
- Marketing language in official announcements
- Obvious jokes or sarcasm
- Old information presented as new

## High-Value Hint Indicators

Prioritize hints that:
- Come from people with direct knowledge
- Reference specific capabilities or benchmarks
- Include uncharacteristic certainty
- Align with known research directions
- Are followed by unusual silence on the topic
