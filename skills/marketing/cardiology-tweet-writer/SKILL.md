---
name: cardiology-tweet-writer
description: Generate scientifically accurate, engaging cardiology tweets for thought leadership. Use when creating social media content for a cardiologist targeting patients, health enthusiasts, health optimizers, people with lifestyle diseases, and caregivers. Produces 10 tweets per batch using permutations of cardiology seed ideas and modifiers. Incorporates feedback to improve output quality over time.
---

# Cardiology Tweet Writer

Generate batches of 10 scientifically accurate, engaging tweets for a cardiologist building thought leadership on social media.

## Core Workflow

1. **Check feedback log** → Read `references/feedback-log.md` for past learnings
2. **Generate topic combinations** → Randomly combine seeds + modifiers from reference files
3. **Verify scientific accuracy** → Cross-check facts against established medical knowledge
4. **Write tweets** → Apply writing rules strictly
5. **Output batch** → Present 10 tweets numbered 1-10

## Reference Files

- `references/seed-ideas.md` - 300 cardiology topic seeds across 15 categories
- `references/modifiers.md` - 215 modifier variables for audience, angle, context
- `references/tweet-examples.md` - Examples demonstrating good vs bad patterns
- `references/feedback-log.md` - Accumulated user feedback for continuous improvement

## Tweet Generation Rules

### Scientific Accuracy (NON-NEGOTIABLE)

- State ONLY what peer-reviewed evidence supports
- Use hedging language appropriately: "research suggests," "studies show," "evidence indicates"
- Never overstate benefits or understate risks
- Include mechanism when possible (builds credibility)
- When uncertain about a fact, flag it for verification rather than guessing
- Cite study types when relevant: RCT, meta-analysis, cohort, etc.

### Writing Style (Avoid AI Detection)

**NEVER use:**
- Em dashes (—)
- "Delve," "dive into," "game-changer," "revolutionize"
- "In today's world," "It's important to note"
- "Here's the thing," "Let's break it down"
- "Unlock," "harness," "elevate"
- Excessive exclamation marks
- Generic phrases like "Studies show that..."
- Lists introduced with colons followed by bullet points
- Perfect parallel structure in every sentence

**USE INSTEAD:**
- Direct, conversational language
- Short punchy sentences mixed with longer ones
- Contractions (it's, don't, won't)
- Specific numbers and data points
- Rhetorical questions sparingly
- Personal observations framed professionally
- Colons, semicolons, periods, commas naturally

### Tweet Structure Guidelines

**Effective patterns:**
- Lead with a surprising fact or counterintuitive insight
- Ask a question that hooks curiosity
- Challenge a common misconception
- Share a clinical observation (without patient details)
- Connect two seemingly unrelated concepts
- Provide actionable advice backed by evidence

**Character limits:** Stay under 280 characters. Shorter is often better.

**Hashtags:** Optional. If used, max 2, placed naturally or at end.

### Variety Requirements

Each batch of 10 must include:
- At least 3 different seed categories
- At least 3 different modifier types
- Mix of: educational, myth-busting, actionable, and thought-provoking content
- At least 2 tweets under 180 characters
- No repetitive openings (vary first words)

## Combination Formula

`Seed Idea(s) + Modifier Variable(s) = Specific Tweet Topic`

**Single seed + modifier:**
Sleep Apnea (seed) + Prevention (temporal) → Tweet about preventing heart damage from untreated sleep apnea

**Multiple seeds:**
Troponin (seed) + Marathon Running (seed) + Myth-busting (angle) → Tweet about why elevated troponin after marathons isn't a heart attack

**Complex combination:**
SGLT2 Inhibitors (seed) + Heart Failure (seed) + Latest Research (evidence) + Patients with Diabetes (audience) → Tweet about new evidence for SGLT2i benefits

## Output Format

Present each tweet as:

```
[1] {tweet text}
Seeds: {seeds used} | Modifiers: {modifiers used}

[2] {tweet text}
Seeds: {seeds used} | Modifiers: {modifiers used}
```

...continue to [10]

## Feedback Integration

After generating tweets, ask: "Any feedback on these? I'll incorporate it for future batches."

When feedback is received:
1. Acknowledge specifically what to change
2. Log the feedback in `references/feedback-log.md`
3. Apply immediately to subsequent generations

## Quality Checklist (Run Before Output)

For each tweet, verify:
- [ ] Scientifically accurate (could defend this in peer review)
- [ ] No AI-typical phrases
- [ ] No em dashes
- [ ] Under 280 characters
- [ ] Engaging hook
- [ ] Clear value to reader
- [ ] Wouldn't embarrass the cardiologist professionally
