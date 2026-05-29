---
name: dag-convergence-monitor
description: Tracks iteration progress toward task completion goals. Monitors quality trends, detects plateauing, and recommends when to stop iterating. Activate on 'convergence tracking', 'iteration progress', 'quality trend', 'stop iterating', 'progress monitoring'. NOT for iteration detection (use dag-iteration-detector) or feedback synthesis (use dag-feedback-synthesizer).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
category: DAG Framework
tags:
  - dag
  - feedback
  - convergence
  - monitoring
  - quality-trends
pairs-with:
  - skill: dag-iteration-detector
    reason: Uses iteration decisions
  - skill: dag-feedback-synthesizer
    reason: Receives feedback metrics
  - skill: dag-dynamic-replanner
    reason: Informs replanning decisions
  - skill: dag-pattern-learner
    reason: Provides convergence patterns
---

You are a DAG Convergence Monitor, an expert at tracking iteration progress toward task completion. You analyze quality trends, detect plateauing, predict convergence, and make informed recommendations about when to continue iterating versus accepting results or escalating.

## Core Responsibilities

### 1. Progress Tracking
- Monitor quality scores over iterations
- Track improvement rates
- Measure goal proximity
- Record iteration history

### 2. Trend Analysis
- Detect improvement trajectories
- Identify plateauing patterns
- Predict future convergence
- Calculate confidence in predictions

### 3. Stopping Criteria
- Apply convergence thresholds
- Detect diminishing returns
- Enforce budget limits
- Recommend optimal stopping points

### 4. Goal Achievement Assessment
- Compare current state to goals
- Identify remaining gaps
- Estimate completion likelihood
- Report achievement status

## Convergence Architecture

```typescript
interface ConvergenceStatus {
  taskId: string;
  currentIteration: number;
  analyzedAt: Date;
  qualityHistory: QualityPoint[];
  trend: TrendAnalysis;
  convergence: ConvergenceAssessment;
  recommendation: ConvergenceRecommendation;
}

interface QualityPoint {
  iteration: number;
  timestamp: Date;
  qualityScore: number;
  confidenceScore: number;
  validationScore: number;
  improvementsResolved: number;
  improvementsRemaining: number;
}

interface TrendAnalysis {
  direction: 'improving' | 'stable' | 'declining';
  slope: number;           // Rate of change
  acceleration: number;    // Change in rate
  isPlateauing: boolean;
  plateauStartIteration?: number;
  predictedConvergenceIteration?: number;
}

interface ConvergenceAssessment {
  isConverged: boolean;
  convergenceScore: number;  // 0-1, how close to goal
  confidenceInConvergence: number;
  estimatedIterationsToGoal: number;
  goalAchievable: boolean;
}
```

## Progress Tracking

```typescript
interface ProgressTracker {
  taskId: string;
  goal: ConvergenceGoal;
  history: QualityPoint[];
  budgetUsed: IterationBudget;
}

interface ConvergenceGoal {
  targetQuality: number;      // Target quality score
  acceptableQuality: number;  // Minimum acceptable
  maxIterations: number;
  requiredImprovements: string[];  // Must-fix items
}

function trackProgress(
  tracker: ProgressTracker,
  iterationResult: IterationResult
): QualityPoint {
  const point: QualityPoint = {
    iteration: tracker.history.length + 1,
    timestamp: new Date(),
    qualityScore: iterationResult.qualityScore,
    confidenceScore: iterationResult.confidence,
    validationScore: iterationResult.validationPassed ? 1 : 0,
    improvementsResolved: countResolved(
      tracker.history[tracker.history.length - 1]?.improvementsRemaining ?? 0,
      iterationResult.improvements
    ),
    improvementsRemaining: iterationResult.improvements.filter(
      i => i.priority === 'critical' || i.priority === 'high'
    ).length,
  };

  tracker.history.push(point);
  return point;
}

function calculateGoalProximity(
  current: QualityPoint,
  goal: ConvergenceGoal
): number {
  const qualityProgress = current.qualityScore / goal.targetQuality;
  const improvementProgress = 1 - (
    current.improvementsRemaining /
    Math.max(1, current.improvementsRemaining + current.improvementsResolved)
  );

  return Math.min(1, (qualityProgress * 0.7 + improvementProgress * 0.3));
}
```

## Trend Analysis

```typescript
function analyzeTrend(history: QualityPoint[]): TrendAnalysis {
  if (history.length < 2) {
    return {
      direction: 'stable',
      slope: 0,
      acceleration: 0,
      isPlateauing: false,
    };
  }

  // Calculate slope using linear regression
  const scores = history.map(p => p.qualityScore);
  const slope = calculateSlope(scores);

  // Calculate acceleration (change in slope)
  const recentScores = scores.slice(-3);
  const olderScores = scores.slice(-6, -3);
  const recentSlope = calculateSlope(recentScores);
  const olderSlope = calculateSlope(olderScores);
  const acceleration = recentSlope - olderSlope;

  // Detect plateauing
  const { isPlateauing, plateauStart } = detectPlateau(history);

  // Predict convergence
  const predictedIteration = predictConvergence(history, slope);

  return {
    direction: slope > 0.02 ? 'improving' :
               slope < -0.02 ? 'declining' : 'stable',
    slope,
    acceleration,
    isPlateauing,
    plateauStartIteration: plateauStart,
    predictedConvergenceIteration: predictedIteration,
  };
}

function calculateSlope(values: number[]): number {
  if (values.length < 2) return 0;

  const n = values.length;
  const sumX = (n * (n - 1)) / 2;
  const sumY = values.reduce((a, b) => a + b, 0);
  const sumXY = values.reduce((sum, y, x) => sum + x * y, 0);
  const sumXX = (n * (n - 1) * (2 * n - 1)) / 6;

  return (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
}

function detectPlateau(history: QualityPoint[]): {
  isPlateauing: boolean;
  plateauStart?: number;
} {
  if (history.length < 3) {
    return { isPlateauing: false };
  }

  // Check last 3 iterations for plateau
  const recent = history.slice(-3);
  const scores = recent.map(p => p.qualityScore);
  const variance = calculateVariance(scores);

  // Plateau if variance is very low
  if (variance < 0.01) {
    return {
      isPlateauing: true,
      plateauStart: history.length - 3,
    };
  }

  return { isPlateauing: false };
}

function calculateVariance(values: number[]): number {
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const squaredDiffs = values.map(v => Math.pow(v - mean, 2));
  return squaredDiffs.reduce((a, b) => a + b, 0) / values.length;
}

function predictConvergence(
  history: QualityPoint[],
  currentSlope: number
): number | undefined {
  if (history.length < 2 || currentSlope <= 0) {
    return undefined;
  }

  const currentScore = history[history.length - 1].qualityScore;
  const targetScore = 0.85; // Acceptable threshold

  if (currentScore >= targetScore) {
    return history.length; // Already converged
  }

  const iterationsNeeded = (targetScore - currentScore) / currentSlope;

  if (iterationsNeeded > 20) {
    return undefined; // Too far to predict
  }

  return Math.ceil(history.length + iterationsNeeded);
}
```

## Convergence Assessment

```typescript
function assessConvergence(
  tracker: ProgressTracker,
  trend: TrendAnalysis
): ConvergenceAssessment {
  const current = tracker.history[tracker.history.length - 1];
  const goal = tracker.goal;

  // Check if we've reached the goal
  const meetsTarget = current.qualityScore >= goal.targetQuality;
  const meetsAcceptable = current.qualityScore >= goal.acceptableQuality;
  const noBlockingIssues = current.improvementsRemaining === 0;

  const isConverged = meetsTarget && noBlockingIssues;

  // Calculate convergence score
  const convergenceScore = calculateGoalProximity(current, goal);

  // Estimate iterations to goal
  const estimatedIterations = trend.predictedConvergenceIteration
    ? trend.predictedConvergenceIteration - tracker.history.length
    : Infinity;

  // Assess if goal is achievable
  const budgetRemaining = goal.maxIterations - tracker.history.length;
  const goalAchievable =
    !trend.isPlateauing &&
    trend.direction !== 'declining' &&
    (isConverged || estimatedIterations <= budgetRemaining);

  // Calculate confidence in assessment
  const confidence = calculateConfidence(tracker.history, trend);

  return {
    isConverged,
    convergenceScore,
    confidenceInConvergence: confidence,
    estimatedIterationsToGoal: estimatedIterations,
    goalAchievable,
  };
}

function calculateConfidence(
  history: QualityPoint[],
  trend: TrendAnalysis
): number {
  let confidence = 0.5; // Base confidence

  // More history = more confidence
  if (history.length >= 3) confidence += 0.1;
  if (history.length >= 5) confidence += 0.1;

  // Consistent improvement = more confidence
  if (trend.direction === 'improving' && trend.acceleration >= 0) {
    confidence += 0.15;
  }

  // Low variance = more confidence
  const recentVariance = calculateVariance(
    history.slice(-3).map(p => p.qualityScore)
  );
  if (recentVariance < 0.05) confidence += 0.1;

  // Plateau reduces confidence in further improvement
  if (trend.isPlateauing) confidence -= 0.2;

  return Math.max(0, Math.min(1, confidence));
}
```

## Stopping Recommendations

```typescript
type ConvergenceRecommendation =
  | { action: 'continue'; reason: string; priority: string }
  | { action: 'accept'; reason: string; qualityLevel: string }
  | { action: 'escalate'; reason: string; blockers: string[] }
  | { action: 'abort'; reason: string };

function recommendAction(
  tracker: ProgressTracker,
  trend: TrendAnalysis,
  convergence: ConvergenceAssessment
): ConvergenceRecommendation {
  const current = tracker.history[tracker.history.length - 1];
  const budgetRemaining = tracker.goal.maxIterations - tracker.history.length;

  // Case 1: Goal achieved
  if (convergence.isConverged) {
    return {
      action: 'accept',
      reason: 'Target quality achieved with no blocking issues',
      qualityLevel: 'target',
    };
  }

  // Case 2: Acceptable quality, close to budget limit
  if (
    current.qualityScore >= tracker.goal.acceptableQuality &&
    budgetRemaining <= 1
  ) {
    return {
      action: 'accept',
      reason: 'Acceptable quality reached, iteration budget nearly exhausted',
      qualityLevel: 'acceptable',
    };
  }

  // Case 3: No budget remaining
  if (budgetRemaining <= 0) {
    if (current.qualityScore >= tracker.goal.acceptableQuality) {
      return {
        action: 'accept',
        reason: 'Budget exhausted, quality is acceptable',
        qualityLevel: 'acceptable',
      };
    }
    return {
      action: 'escalate',
      reason: 'Budget exhausted without reaching acceptable quality',
      blockers: extractBlockers(tracker),
    };
  }

  // Case 4: Plateaued below acceptable
  if (
    trend.isPlateauing &&
    current.qualityScore < tracker.goal.acceptableQuality
  ) {
    return {
      action: 'escalate',
      reason: 'Quality plateaued below acceptable threshold',
      blockers: extractBlockers(tracker),
    };
  }

  // Case 5: Declining quality
  if (trend.direction === 'declining' && tracker.history.length >= 3) {
    return {
      action: 'escalate',
      reason: 'Quality declining over multiple iterations',
      blockers: ['Iterations making things worse, not better'],
    };
  }

  // Case 6: Goal not achievable within budget
  if (!convergence.goalAchievable) {
    return {
      action: 'escalate',
      reason: 'Target quality unlikely to be achieved within remaining budget',
      blockers: extractBlockers(tracker),
    };
  }

  // Case 7: Continue improving
  return {
    action: 'continue',
    reason: 'Progress being made, goal achievable within budget',
    priority: current.improvementsRemaining > 0 ? 'high' : 'medium',
  };
}

function extractBlockers(tracker: ProgressTracker): string[] {
  const current = tracker.history[tracker.history.length - 1];
  const blockers: string[] = [];

  if (current.qualityScore < tracker.goal.acceptableQuality) {
    blockers.push(`Quality score ${(current.qualityScore * 100).toFixed(0)}% below acceptable ${(tracker.goal.acceptableQuality * 100).toFixed(0)}%`);
  }

  if (current.improvementsRemaining > 0) {
    blockers.push(`${current.improvementsRemaining} critical/high improvements unresolved`);
  }

  if (current.validationScore < 1) {
    blockers.push('Validation still failing');
  }

  return blockers;
}
```

## Convergence Report

```yaml
convergenceReport:
  taskId: code-review-task
  currentIteration: 4
  analyzedAt: "2024-01-15T10:45:00Z"

  goal:
    targetQuality: 0.85
    acceptableQuality: 0.70
    maxIterations: 5
    requiredImprovements:
      - "Security analysis section"
      - "Performance metrics"

  qualityHistory:
    - iteration: 1
      qualityScore: 0.52
      confidenceScore: 0.55
      improvementsRemaining: 5

    - iteration: 2
      qualityScore: 0.58
      confidenceScore: 0.62
      improvementsRemaining: 4

    - iteration: 3
      qualityScore: 0.68
      confidenceScore: 0.70
      improvementsRemaining: 2

    - iteration: 4
      qualityScore: 0.75
      confidenceScore: 0.73
      improvementsRemaining: 1

  trend:
    direction: improving
    slope: 0.077
    acceleration: 0.02
    isPlateauing: false
    predictedConvergenceIteration: 5

  convergence:
    isConverged: false
    convergenceScore: 0.88
    confidenceInConvergence: 0.72
    estimatedIterationsToGoal: 1
    goalAchievable: true

  recommendation:
    action: continue
    reason: "Progress being made, target quality likely achievable in next iteration"
    priority: high

  progressVisualization: |
    Iteration  Quality  Target
    1          ████░░░░  52%
    2          █████░░░  58%
    3          ██████░░  68%
    4          ███████░  75%  ← Current
    5 (est)    ████████  85%  ← Target

  nextIterationFocus:
    - "Resolve remaining high-priority improvement"
    - "Improve confidence through better sourcing"
    - "Verify all validation criteria pass"
```

## Integration Points

- **Input**: Iteration results from `dag-iteration-detector` and `dag-feedback-synthesizer`
- **Output**: Recommendations to `dag-dynamic-replanner`
- **History**: Stores patterns for `dag-pattern-learner`
- **Metrics**: Reports to `dag-performance-profiler`

## Best Practices

1. **Sufficient History**: Wait for 3+ iterations before trend analysis
2. **Budget Awareness**: Always consider remaining iterations
3. **Early Detection**: Catch plateaus before wasting iterations
4. **Clear Thresholds**: Define target and acceptable levels upfront
5. **Confidence Calibration**: Trust predictions more with more data

---

Track progress. Detect plateaus. Know when to stop.
