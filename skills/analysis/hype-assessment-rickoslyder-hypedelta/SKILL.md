---
name: hype-assessment
description: Assess overall hype levels across AI topics by comparing lab researcher enthusiasm against critic skepticism. Use after topic synthesis to identify which topics are overhyped, underhyped, or accurately assessed by the field.
---

# Hype Assessment Skill

Assess which AI topics are overhyped, underhyped, or accurately assessed based on synthesized claims.

## Assessment Framework

### Overhyped Topics (Lab enthusiasm exceeds warranted confidence)

Signs of overhype:
- Lab researchers make strong claims that critics have substantively challenged
- Evidence quality is low but confidence is high
- Past predictions in this area have repeatedly failed
- Marketing language exceeds technical substance
- Hype delta > +0.3

### Underhyped Topics (Critic skepticism may be excessive)

Signs of underhype:
- Real progress has been made but critics haven't updated
- Evidence is strong but narrative hasn't caught up
- Lab hints suggest unreleased capabilities
- Quiet progress without announcements
- Hype delta < -0.3

### Accurately Assessed Topics

Signs of accurate assessment:
- Lab and critic views are relatively aligned
- Claims match observable evidence
- Predictions have been reasonably accurate
- Hype delta between -0.2 and +0.2

## Scoring System

For each topic, assign a score from -1.0 to +1.0:

| Score | Meaning |
|-------|---------|
| +1.0 | Severely overhyped - massive gap between claims and reality |
| +0.5 | Moderately overhyped - lab enthusiasm outpaces evidence |
| +0.2 | Slightly overhyped |
| 0.0 | Accurately assessed |
| -0.2 | Slightly underhyped |
| -0.5 | Moderately underhyped - real progress being underrated |
| -1.0 | Severely underhyped - major developments being ignored |

## Evidence to Consider

### For Overhyped Assessment
- Repeated failed predictions
- Marketing claims exceeding published results
- Hype cycle patterns (lots of announcements, few deliverables)
- Benchmark gaming without real-world transfer
- "Just around the corner" claims that keep slipping

### For Underhyped Assessment
- Steady progress without fanfare
- Working deployments with limited publicity
- Academic results that haven't reached mainstream
- Capabilities that exist but aren't marketed
- Legitimate breakthroughs dismissed by critics

### For Accurate Assessment
- Claims that held up over time
- Convergence between lab and critic views
- Predictions that came true
- Honest acknowledgment of limitations
- Nuanced discussion of tradeoffs

## Output Format

Return JSON:
```json
{
  "overhypedTopics": [
    {
      "topic": "agents",
      "score": 0.6,
      "reasoning": "Lab enthusiasm for autonomous agents significantly exceeds demonstrated reliability. Multiple high-profile failures in production while claims of imminent AGI-like autonomy persist.",
      "keyEvidence": [
        "Devin and similar demos failed to replicate",
        "Production agent deployments have high failure rates",
        "Claims of 'replacing developers' haven't materialized"
      ]
    }
  ],
  "underhypedTopics": [
    {
      "topic": "interpretability",
      "score": -0.5,
      "reasoning": "Significant progress on mechanistic interpretability is being made at Anthropic and elsewhere, but mainstream coverage focuses on capabilities. Real tools for understanding models are emerging.",
      "keyEvidence": [
        "Golden Gate Claude demonstrated genuine steering",
        "Feature extraction becoming reproducible",
        "SAEs showing practical utility"
      ]
    }
  ],
  "accuratelyAssessedTopics": [
    {
      "topic": "multimodal",
      "score": 0.1,
      "reasoning": "Vision-language models have improved substantially and assessments largely reflect actual capabilities. Both enthusiasm and concerns are grounded.",
      "keyEvidence": [
        "GPT-4V and Claude vision work as advertised",
        "Known limitations acknowledged",
        "Incremental improvements match expectations"
      ]
    }
  ],
  "overallFieldSentiment": 0.72,
  "summary": "A paragraph summarizing the overall hype landscape..."
}
```

## Overall Field Sentiment

Calculate as weighted average of lab researcher bullishness across all topics (0.0-1.0).

Interpretation:
- 0.8-1.0: Extremely bullish field sentiment (potential bubble)
- 0.6-0.8: Optimistic but measured
- 0.4-0.6: Balanced/uncertain
- 0.2-0.4: Cautious/skeptical
- 0.0-0.2: Pessimistic

## Summary Guidelines

Write a single paragraph summarizing:
1. Overall hype temperature
2. Most overhyped area and why
3. Most underhyped area and why
4. What sophisticated observers should pay attention to

Tone: Direct, opinionated but fair, grounded in evidence.
