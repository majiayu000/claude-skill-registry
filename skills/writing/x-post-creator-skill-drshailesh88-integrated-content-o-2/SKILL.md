---
name: x-post-creator-skill
description: Create scientifically rigorous, engaging X (Twitter) posts for cardiology thought leadership. Use when generating social media content for a cardiologist targeting patients, caregivers, health optimizers, people with lifestyle diseases (hypertension, diabetes, cholesterol), and sedentary individuals seeking prevention. Produces batches of 10 unique posts using strategic combinations of 300+ cardiology seed ideas, 215+ modifiers, 5 audience archetypes, awareness levels, and proven copywriting frameworks (4A, Magical Multipliers). Features self-improvement through accumulated feedback.
---

# X Post Creator for Cardiology Thought Leadership

Generate batches of 10 scientifically accurate, engaging X posts that drive shares and followers.

## Core Workflow

1. **Load feedback** → Read `references/feedback-log.md` for accumulated learnings
2. **Select strategic combinations** → Use combination engine below
3. **Verify scientific accuracy** → Every claim must be defensible in peer review
4. **Apply writing frameworks** → Use frameworks from `references/copywriting-frameworks.md`
5. **Quality check** → Run checklist before output
6. **Output batch** → Present 10 posts with metadata
7. **Collect feedback** → Update feedback log

## Reference Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `references/seed-ideas.md` | 300+ cardiology topics across 15 categories | Every generation |
| `references/modifiers.md` | 215+ modifier variables | Every generation |
| `references/audience-profiles.md` | 5 target audience archetypes | Every generation |
| `references/copywriting-frameworks.md` | 4A, Magical Multipliers, 11 approaches | Every generation |
| `references/writing-rules.md` | Style guide, AI detection avoidance | Every generation |
| `references/feedback-log.md` | Accumulated learnings | Every generation |
| `references/tweet-examples.md` | Good/bad examples | When quality unclear |

## Scientific Accuracy (NON-NEGOTIABLE)

This is directly associated with the cardiologist's reputation. Good content may or may not help career. Bad science WILL doom it.

**Requirements:**
- State ONLY what peer-reviewed evidence supports
- Use appropriate hedging: "research suggests," "studies show," "evidence indicates"
- Never overstate benefits or understate risks
- Include mechanism when possible (builds credibility)
- When uncertain, flag for verification rather than guess
- Cite study types when relevant: RCT, meta-analysis, cohort

**Never produce:**
- Unsubstantiated claims or "miracle cures"
- Cherry-picked data without context
- Fear-mongering without solutions
- Advice contradicting clinical guidelines without justification

## Combination Engine

Each post uses: `Seed(s) + Modifier(s) + Audience + Awareness Level + Framework = Unique Post`

**Variety requirements per batch of 10:**
- Minimum 5 different seed categories
- Minimum 4 different modifier categories
- All 5 audiences represented at least once across batch
- Mix of 4A frameworks (Actionable, Analytical, Aspirational, Anthropological)
- At least 2 different Magical Multiplier angles
- No repetitive openings (vary first 3 words)

## Output Format

```
[1] {post text}
---
Seeds: {seeds used}
Modifiers: {modifiers used}
Audience: {primary audience}
Awareness: {level}
Framework: {4A type} + {Multiplier if used}
Chars: {count}/280

[2] {post text}
...
```

Continue to [10].

## Feedback Integration Protocol

After output, ask: "Any feedback on this batch? Rate 1-5 and note what worked/didn't."

**When feedback received:**
1. Acknowledge specific change needed
2. Append to `references/feedback-log.md` with date
3. Apply immediately to all future generations
4. Confirm understanding back to user

## Quality Checklist (Run Before Every Output)

For EACH post verify:
- [ ] Scientifically accurate (defensible in peer review)
- [ ] No AI-typical phrases (see writing-rules.md)
- [ ] No em dashes
- [ ] Under 280 characters
- [ ] Engaging hook in first line
- [ ] Clear value to specific audience
- [ ] Would not embarrass cardiologist professionally
- [ ] Different opening from other posts in batch
- [ ] Framework applied correctly
