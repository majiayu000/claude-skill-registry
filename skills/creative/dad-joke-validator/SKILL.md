---
name: dad-joke-validator
description: Analyze and score jokes on the dad joke quality spectrum with multi-dimensional feedback on pun quality, groan factor, wholesomeness, and structure. Can also generate dad jokes.
---

# Dad Joke Validator

Analyze jokes for dad joke quality across multiple dimensions or generate new dad jokes.

## When to Use

Invoke this skill when the user:
- Asks you to analyze a joke for "dad joke" quality
- Wants feedback on why a joke works (or doesn't)
- Requests a dad joke be generated
- Asks about pun quality, groan factor, or joke structure
- Says things like "is this a dad joke?" or "rate this joke"

## Core Capabilities

### 1. Joke Analysis

When analyzing a joke, score across these dimensions:

**Pun Quality (0-10)**
- Wordplay sophistication
- Multiple meanings exploited
- Unexpected connections
- Clarity of the pun (not too obscure)

**Groan Factor (0-10)**
- How predictable the punchline is
- "Obviousness" that triggers the groan
- Clean setup leading to "of course" moment
- Higher score = more groan-inducing (this is GOOD for dad jokes)

**Wholesomeness (0-10)**
- Family-friendly (no edgy content)
- Positive/innocent tone
- Safe for all ages
- Warm rather than mean-spirited

**Setup/Punchline Structure (0-10)**
- Clear setup establishing context
- Economical punchline (not too long)
- Timing and rhythm
- Misdirection technique

**Overall Dad Joke Score (0-100)**
- Formula: (Pun Quality * 2.5) + (Groan Factor * 3) + (Wholesomeness * 3) + (Structure * 1.5)
- 85-100: Peak dad joke territory
- 70-84: Solid dad joke
- 50-69: Dad joke adjacent (needs work)
- Below 50: Not a dad joke

### 2. Analysis Output Format

Provide analysis in this structure:

```
Dad Joke Score: XX/100

Dimensional Breakdown:
- Pun Quality: X/10 - [Brief explanation]
- Groan Factor: X/10 - [Why it makes you groan]
- Wholesomeness: X/10 - [Family-friendly assessment]
- Structure: X/10 - [Setup/punchline evaluation]

Verdict: [One sentence overall assessment]

Improvement Suggestions (if score < 85):
- [Specific actionable feedback]
```

### 3. Dad Joke Generation

When asked to generate a dad joke:

1. Select a wholesome theme (food, animals, occupations, everyday objects)
2. Find a word with multiple meanings or homophones
3. Build setup establishing one meaning
4. Deliver punchline exploiting the other meaning
5. Keep it SHORT (1-2 sentence setup, 1 sentence punchline max)

**Quality Requirements:**
- Must score 85+ on your own rubric
- Maximum 3 sentences total
- Pun must be clear (not too clever)
- Should trigger genuine groan

### 4. Anti-Patterns to Detect

Flag these as "NOT dad jokes":
- Edgy or inappropriate content (Wholesomeness < 7)
- Mean-spirited humor
- Requires specialized knowledge (too obscure)
- No clear pun or wordplay (Pun Quality < 5)
- Too complex or long-winded
- Sarcastic or ironic tone

## Special Instructions

**DO:**
- Explain WHY scores are assigned
- Give specific examples in feedback
- Maintain warmth and humor in analysis
- Acknowledge when something is "so bad it's good"

**DON'T:**
- Mock the joke harshly (dad jokes are supposed to be groan-worthy)
- Score ironically (genuine assessment only)
- Generate edgy content when creating jokes
- Over-explain the pun (kills the joke)

## Examples

See `references/examples.md` for 10 analyzed dad jokes across the quality spectrum.

## Integration

Works standalone. Can be combined with:
- Prose Polish (for joke wording refinement)
- Meeting Bullshit Detector (for detecting forced humor in corporate settings)
