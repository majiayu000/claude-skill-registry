---
name: predictive-analytics
description: ML-based estimation patterns, confidence intervals, and predictive modeling. Reference this skill when forecasting costs or time.
---

# Predictive Analytics Skill
# Project Autopilot - ML estimation patterns
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Patterns for accurate predictive estimation using historical data.

---

## Estimation Fundamentals

### The Estimation Pipeline

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Feature    │ →  │   Similar    │ →  │    Base      │
│  Analysis    │    │   Projects   │    │   Estimate   │
└──────────────┘    └──────────────┘    └──────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Adjustment  │ →  │  Confidence  │ →  │    Final     │
│   Factors    │    │   Interval   │    │   Estimate   │
└──────────────┘    └──────────────┘    └──────────────┘
```

### Key Principles

1. **Historical Basis** - All estimates start from historical data
2. **Similarity Matching** - Find most relevant comparisons
3. **Adjustment Factors** - Account for project-specific differences
4. **Confidence Intervals** - Express uncertainty explicitly
5. **Continuous Learning** - Update models with actuals

---

## Feature Analysis

### Complexity Factors

| Factor | Weight | Scoring |
|--------|--------|---------|
| Data Models | 0.20 | # of entities × 0.5 |
| API Endpoints | 0.25 | # of endpoints × 0.3 |
| UI Components | 0.20 | # of screens × 0.4 |
| Integrations | 0.15 | # of external APIs × 0.8 |
| Auth Complexity | 0.10 | Simple=1, OAuth=2, Multi=3 |
| Testing Scope | 0.10 | Unit=1, +Integration=2, +E2E=3 |

### Complexity Score Calculation

```typescript
function calculateComplexity(requirements: Requirements): number {
  const scores = {
    dataModels: requirements.entities * 0.5,
    endpoints: requirements.endpoints * 0.3,
    uiComponents: requirements.screens * 0.4,
    integrations: requirements.externalAPIs * 0.8,
    auth: getAuthScore(requirements.auth),
    testing: getTestingScore(requirements.testing),
  };

  const weighted = Object.entries(weights)
    .reduce((sum, [key, weight]) => sum + scores[key] * weight, 0);

  return weighted;
}
```

### Complexity Tiers

| Tier | Score | Typical Cost | Confidence |
|------|-------|--------------|------------|
| Simple | < 3 | $0.50-1.50 | High (±10%) |
| Medium | 3-6 | $1.50-4.00 | Medium (±20%) |
| Complex | 6-10 | $4.00-8.00 | Medium (±25%) |
| Very Complex | > 10 | $8.00+ | Low (±35%) |

---

## Similarity Matching

### Similarity Score Algorithm

```typescript
function calculateSimilarity(
  current: Project,
  historical: Project
): number {
  let score = 0;

  // Tech stack match (40%)
  const stackOverlap = intersect(current.stack, historical.stack);
  score += (stackOverlap.length / current.stack.length) * 40;

  // Feature type match (30%)
  const featureMatch = compareFeatures(current.features, historical.features);
  score += featureMatch * 30;

  // Complexity similarity (20%)
  const complexityDiff = Math.abs(
    current.complexity - historical.complexity
  ) / current.complexity;
  score += (1 - Math.min(complexityDiff, 1)) * 20;

  // Recency bonus (10%)
  const monthsAgo = getMonthsAgo(historical.completedAt);
  score += Math.max(0, (12 - monthsAgo) / 12) * 10;

  return score;
}
```

### Minimum Similarity Threshold

| Sample Size | Min Similarity | Confidence |
|-------------|----------------|------------|
| ≥ 10 projects | 60% | High |
| 5-9 projects | 70% | Medium |
| < 5 projects | 80% | Low |

---

## Base Estimate Calculation

### Weighted Historical Average

```typescript
function calculateBaseEstimate(
  similar: SimilarProject[]
): Estimate {
  // Weight by similarity score
  const totalWeight = similar.reduce((sum, p) => sum + p.similarity, 0);

  const weightedCost = similar.reduce(
    (sum, p) => sum + p.actualCost * (p.similarity / totalWeight),
    0
  );

  const weightedDuration = similar.reduce(
    (sum, p) => sum + p.duration * (p.similarity / totalWeight),
    0
  );

  return {
    cost: weightedCost,
    duration: weightedDuration,
    confidence: calculateConfidence(similar),
  };
}
```

### Phase-Based Estimation

```typescript
const phaseWeights = {
  setup: 0.05,
  database: 0.10,
  auth: 0.15,
  api: 0.25,
  frontend: 0.25,
  testing: 0.15,
  deployment: 0.05,
};

function estimateByPhase(
  totalEstimate: number,
  phases: string[]
): PhaseEstimates {
  return phases.map(phase => ({
    phase,
    estimate: totalEstimate * (phaseWeights[phase] || 0.10),
  }));
}
```

---

## Adjustment Factors

### Contextual Adjustments

| Factor | Condition | Adjustment |
|--------|-----------|------------|
| New Tech Stack | First time with tech | +25% |
| Familiar Stack | 5+ projects | -10% |
| Complex Integration | 3+ external APIs | +20% |
| Simple CRUD | Basic operations | -15% |
| Strict Requirements | Regulated industry | +30% |
| Prototype Only | MVP/POC | -40% |

### Historical Accuracy Adjustment

```typescript
function applyHistoricalAccuracy(
  estimate: number,
  phaseType: string
): number {
  const accuracy = getHistoricalAccuracy(phaseType);

  // If we typically underestimate, increase estimate
  if (accuracy.avgVariance > 0) {
    return estimate * (1 + accuracy.avgVariance / 100);
  }

  return estimate;
}
```

---

## Confidence Intervals

### Confidence Calculation

```typescript
function calculateConfidence(
  similar: SimilarProject[],
  adjustments: Adjustment[]
): ConfidenceLevel {
  // Base confidence from sample size
  let confidence = 0;
  if (similar.length >= 10) confidence = 90;
  else if (similar.length >= 5) confidence = 75;
  else if (similar.length >= 3) confidence = 60;
  else confidence = 45;

  // Reduce for high similarity variance
  const varianceReduction = calculateVarianceImpact(similar);
  confidence -= varianceReduction;

  // Reduce for many adjustments
  confidence -= adjustments.length * 2;

  return {
    level: confidence >= 80 ? 'high' : confidence >= 60 ? 'medium' : 'low',
    percentage: confidence,
    interval: getInterval(confidence),
  };
}
```

### Confidence Intervals

| Confidence | Interval | Range |
|------------|----------|-------|
| High (80%+) | ±15% | Narrow |
| Medium (60-80%) | ±25% | Moderate |
| Low (<60%) | ±40% | Wide |

### Scenario Generation

```typescript
function generateScenarios(
  estimate: number,
  confidence: ConfidenceLevel
): Scenarios {
  const interval = confidence.interval;

  return {
    best: estimate * (1 - interval),
    likely: estimate,
    worst: estimate * (1 + interval * 1.5),  // Asymmetric - cost overruns more common
  };
}
```

---

## Continuous Learning

### Feedback Loop

```
┌─────────────┐
│  Estimate   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Execute   │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│   Actual    │ →   │   Compare   │
└─────────────┘     └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Learn     │
                    │  & Adjust   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Improve    │
                    │   Model     │
                    └─────────────┘
```

### Learning Updates

```typescript
function updateLearning(
  estimated: Estimate,
  actual: Actual
): void {
  const variance = (actual.cost - estimated.cost) / estimated.cost;

  // Update phase-specific accuracy
  updatePhaseAccuracy(estimated.phases, actual.phases);

  // Update tech stack patterns
  updateTechStackPatterns(estimated.stack, variance);

  // Update complexity calibration
  updateComplexityCalibration(estimated.complexity, variance);

  // Record for future similarity matching
  recordProjectOutcome({
    estimated,
    actual,
    variance,
  });
}
```

---

## Estimation Checklist

### Before Estimating

- [ ] Requirements clearly defined
- [ ] Tech stack identified
- [ ] Similar projects found
- [ ] Complexity scored
- [ ] Risks identified

### During Estimation

- [ ] Base estimate from historicals
- [ ] Adjustments documented
- [ ] Confidence calculated
- [ ] Scenarios generated
- [ ] Budget checked

### After Completion

- [ ] Actual vs estimate recorded
- [ ] Variance analyzed
- [ ] Learnings extracted
- [ ] Model updated
