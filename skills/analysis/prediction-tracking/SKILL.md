---
name: prediction-tracking
description: Track and evaluate AI predictions over time to assess accuracy. Use when reviewing past predictions to determine if they came true, failed, or remain uncertain.
---

# Prediction Tracking Skill

Track predictions made by AI researchers and critics, evaluate their accuracy over time.

## Prediction Recording

When recording a new prediction, capture:

### Required Fields
- **text**: The prediction as stated
- **author**: Who made it
- **madeAt**: When it was made
- **timeframe**: When they expect it to happen
- **topic**: What area of AI
- **confidence**: How confident they seemed

### Optional Fields
- **sourceUrl**: Where the prediction was made
- **targetDate**: Specific date if mentioned
- **conditions**: Any caveats or conditions
- **metrics**: How to measure success

## Evaluation Status

When evaluating predictions, assign one of:

### `verified`
Clearly came true as stated.
- The predicted capability/event occurred
- Within the stated timeframe
- Substantially as described

### `falsified`
Clearly did not come true.
- Timeframe passed without occurrence
- Contradictory evidence emerged
- Author retracted or modified claim

### `partially-verified`
Partially accurate.
- Some aspects came true, others didn't
- Capability exists but weaker than claimed
- Timeframe was off but direction correct

### `too-early`
Not enough time has passed.
- Still within stated timeframe
- No definitive evidence either way

### `unfalsifiable`
Cannot be objectively assessed.
- Too vague to measure
- No clear success criteria
- Moved goalposts

### `ambiguous`
Prediction was too vague to evaluate.
- Multiple interpretations possible
- Success criteria unclear

## Evaluation Process

For each prediction being evaluated:

### 1. Restate the prediction
What exactly was claimed?

### 2. Identify timeframe
Has enough time passed to evaluate?

### 3. Gather evidence
What has happened since?
- Relevant releases or announcements
- Benchmark results
- Real-world deployments
- Counter-evidence

### 4. Assess status
Which evaluation status applies?

### 5. Score accuracy
If verifiable, rate 0.0-1.0:
- 1.0: Exactly as predicted
- 0.7-0.9: Substantially correct
- 0.4-0.6: Partially correct
- 0.1-0.3: Mostly wrong
- 0.0: Completely wrong

### 6. Note lessons
What does this tell us about:
- The author's forecasting ability
- The topic's predictability
- Common prediction pitfalls

## Output Format

For evaluation:
```json
{
  "evaluations": [
    {
      "predictionId": "id",
      "status": "verified",
      "accuracyScore": 0.85,
      "evidence": "Description of evidence",
      "notes": "Additional context",
      "evaluatedAt": "timestamp"
    }
  ]
}
```

For accuracy statistics:
```json
{
  "author": "Author name",
  "totalPredictions": 15,
  "verified": 5,
  "falsified": 3,
  "partiallyVerified": 2,
  "pending": 4,
  "unfalsifiable": 1,
  "averageAccuracy": 0.62,
  "topicBreakdown": {
    "reasoning": { "predictions": 5, "accuracy": 0.7 },
    "agents": { "predictions": 3, "accuracy": 0.4 }
  },
  "calibration": "Assessment of how well-calibrated they are"
}
```

## Calibration Assessment

Evaluate whether predictors are well-calibrated:

### Well-Calibrated
- High-confidence predictions usually come true
- Low-confidence predictions have mixed results
- Acknowledges uncertainty appropriately

### Overconfident
- High-confidence predictions often fail
- Rarely expresses uncertainty
- Doesn't update on evidence

### Underconfident
- Low-confidence predictions often come true
- Hedges even on likely outcomes
- Too conservative

### Inconsistent
- Confidence doesn't correlate with accuracy
- Random relationship between stated and actual accuracy

## Tracking Notable Predictors

Keep running assessments of key voices:

| Predictor | Total | Accuracy | Calibration | Notes |
|-----------|-------|----------|-------------|-------|
| Sam Altman | 20 | 55% | Overconfident | Timeline optimism |
| Gary Marcus | 15 | 70% | Well-calibrated | Conservative |
| Dario Amodei | 12 | 65% | Slightly over | Safety-focused |

## Red Flags

Watch for prediction patterns that suggest bias:
- Always bullish regardless of topic
- Never acknowledges failed predictions
- Moves goalposts when wrong
- Predictions align suspiciously with financial interests
- Vague enough to claim credit for anything
