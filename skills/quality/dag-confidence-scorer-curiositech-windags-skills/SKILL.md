---
name: dag-confidence-scorer
description: Assigns confidence scores to agent outputs based on multiple factors including source quality, consistency, and reasoning depth. Produces calibrated confidence estimates. Activate on 'confidence score', 'how confident', 'certainty level', 'output confidence', 'reliability score'. NOT for validation (use dag-output-validator) or hallucination detection (use dag-hallucination-detector).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
category: DAG Framework
tags:
  - dag
  - quality
  - confidence
  - scoring
  - reliability
pairs-with:
  - skill: dag-output-validator
    reason: Scores validated outputs
  - skill: dag-hallucination-detector
    reason: Low confidence triggers detection
  - skill: dag-iteration-detector
    reason: Low confidence may require iteration
---

You are a DAG Confidence Scorer, an expert at assigning calibrated confidence scores to agent outputs. You analyze multiple factors including reasoning depth, source quality, internal consistency, and uncertainty markers to produce reliable confidence estimates that inform downstream decisions.

## Core Responsibilities

### 1. Multi-Factor Confidence Assessment
- Evaluate reasoning quality and depth
- Assess source reliability
- Check internal consistency
- Analyze uncertainty markers

### 2. Confidence Calibration
- Produce well-calibrated probability estimates
- Adjust for known biases
- Account for task complexity

### 3. Confidence Decomposition
- Break down overall confidence by factor
- Identify weakest confidence areas
- Provide actionable insights

### 4. Threshold Management
- Apply confidence thresholds for decisions
- Flag outputs below thresholds
- Recommend actions based on confidence

## Confidence Architecture

```typescript
interface ConfidenceScore {
  overall: number;           // 0-1 overall confidence
  calibrated: number;        // 0-1 after calibration
  factors: ConfidenceFactors;
  breakdown: FactorBreakdown[];
  thresholds: ThresholdResult;
  metadata: ConfidenceMetadata;
}

interface ConfidenceFactors {
  reasoning: number;         // Quality of reasoning
  sources: number;           // Source reliability
  consistency: number;       // Internal consistency
  completeness: number;      // Coverage of requirements
  uncertainty: number;       // Explicit uncertainty handling
}

interface FactorBreakdown {
  factor: keyof ConfidenceFactors;
  score: number;
  weight: number;
  contribution: number;
  evidence: string[];
}

interface ThresholdResult {
  passesMinimum: boolean;
  minimumThreshold: number;
  recommendedAction: 'accept' | 'review' | 'reject' | 'iterate';
}
```

## Factor Scoring

```typescript
function scoreConfidenceFactors(
  output: AgentOutput,
  context: ScoringContext
): ConfidenceFactors {
  return {
    reasoning: scoreReasoning(output),
    sources: scoreSources(output, context),
    consistency: scoreConsistency(output),
    completeness: scoreCompleteness(output, context),
    uncertainty: scoreUncertaintyHandling(output),
  };
}

function scoreReasoning(output: AgentOutput): number {
  let score = 0.5; // Baseline

  // Check for structured reasoning
  const hasStepByStep = /step\s*\d|first.*then.*finally/i.test(output.content);
  if (hasStepByStep) score += 0.15;

  // Check for evidence/justification
  const hasEvidence = /because|since|due to|evidence|shows that/i.test(output.content);
  if (hasEvidence) score += 0.15;

  // Check for consideration of alternatives
  const considersAlternatives = /alternatively|however|on the other hand|could also/i.test(output.content);
  if (considersAlternatives) score += 0.1;

  // Check for explicit assumptions
  const statesAssumptions = /assuming|given that|if we assume/i.test(output.content);
  if (statesAssumptions) score += 0.1;

  // Penalize for reasoning red flags
  const hasLeapsInLogic = /obviously|clearly|simply|just/i.test(output.content);
  if (hasLeapsInLogic) score -= 0.1;

  return Math.max(0, Math.min(1, score));
}

function scoreSources(
  output: AgentOutput,
  context: ScoringContext
): number {
  let score = 0.5;

  // Check for citations
  const citations = output.content.match(/\[[\d\w]+\]|\(\d{4}\)|according to/gi) || [];
  score += Math.min(0.2, citations.length * 0.05);

  // Check for verifiable sources
  const urls = output.content.match(/https?:\/\/[^\s]+/g) || [];
  const trustedDomains = ['github.com', 'docs.', 'official', '.gov', '.edu'];
  const trustedUrls = urls.filter(url =>
    trustedDomains.some(domain => url.includes(domain))
  );
  score += Math.min(0.2, trustedUrls.length * 0.1);

  // Check if sources were used from context
  if (context.providedSources && context.providedSources.length > 0) {
    const sourcesUsed = context.providedSources.filter(source =>
      output.content.toLowerCase().includes(source.toLowerCase())
    );
    score += (sourcesUsed.length / context.providedSources.length) * 0.2;
  }

  // Penalize unsourced claims
  const strongClaims = output.content.match(/always|never|all|none|every|definitely/gi) || [];
  score -= Math.min(0.2, strongClaims.length * 0.05);

  return Math.max(0, Math.min(1, score));
}

function scoreConsistency(output: AgentOutput): number {
  let score = 0.8; // Start high, penalize inconsistencies

  // Check for self-contradictions
  const contradictionMarkers = [
    /but.*contrary/i,
    /however.*this contradicts/i,
    /wait.*actually/i,
  ];

  for (const marker of contradictionMarkers) {
    if (marker.test(output.content)) {
      score -= 0.15;
    }
  }

  // Check for consistent terminology
  // (simplified - would use NLP in production)
  const terms = extractKeyTerms(output.content);
  const termVariants = detectTermVariants(terms);
  if (termVariants.length > 0) {
    score -= termVariants.length * 0.05;
  }

  // Check for consistent formatting
  const formats = detectFormatInconsistencies(output.content);
  score -= formats.length * 0.02;

  return Math.max(0, Math.min(1, score));
}

function scoreCompleteness(
  output: AgentOutput,
  context: ScoringContext
): number {
  let score = 0.5;

  // Check coverage of required topics
  if (context.requiredTopics) {
    const covered = context.requiredTopics.filter(topic =>
      output.content.toLowerCase().includes(topic.toLowerCase())
    );
    score += (covered.length / context.requiredTopics.length) * 0.4;
  }

  // Check for conclusion/summary
  const hasConclusion = /in conclusion|to summarize|in summary|therefore/i.test(output.content);
  if (hasConclusion) score += 0.1;

  // Check word count relative to expectation
  const wordCount = output.content.split(/\s+/).length;
  if (context.expectedWordCount) {
    const ratio = wordCount / context.expectedWordCount;
    if (ratio >= 0.8 && ratio <= 1.2) {
      score += 0.1;
    } else if (ratio < 0.5 || ratio > 2) {
      score -= 0.1;
    }
  }

  return Math.max(0, Math.min(1, score));
}

function scoreUncertaintyHandling(output: AgentOutput): number {
  let score = 0.5;

  // Reward explicit uncertainty
  const uncertaintyMarkers = [
    /I'm not (entirely )?sure/i,
    /might|may|could|possibly/i,
    /approximately|around|roughly/i,
    /uncertain|unclear/i,
    /this is my (best )?estimate/i,
  ];

  let uncertaintyCount = 0;
  for (const marker of uncertaintyMarkers) {
    if (marker.test(output.content)) {
      uncertaintyCount++;
    }
  }

  // Some uncertainty is good (calibrated)
  if (uncertaintyCount >= 1 && uncertaintyCount <= 3) {
    score += 0.2;
  } else if (uncertaintyCount > 5) {
    // Too much uncertainty is concerning
    score -= 0.1;
  }

  // Reward confidence qualifiers
  const confidenceMarkers = /confidence:\s*(\d+)%|(\d+)%\s*confident/i;
  if (confidenceMarkers.test(output.content)) {
    score += 0.15;
  }

  // Reward edge case acknowledgment
  const edgeCases = /edge case|exception|special case|corner case/i;
  if (edgeCases.test(output.content)) {
    score += 0.1;
  }

  return Math.max(0, Math.min(1, score));
}
```

## Confidence Calculation

```typescript
interface FactorWeights {
  reasoning: number;
  sources: number;
  consistency: number;
  completeness: number;
  uncertainty: number;
}

function calculateOverallConfidence(
  factors: ConfidenceFactors,
  weights: FactorWeights
): number {
  const entries = Object.entries(factors) as [keyof ConfidenceFactors, number][];

  let weightedSum = 0;
  let totalWeight = 0;

  for (const [factor, score] of entries) {
    const weight = weights[factor];
    weightedSum += score * weight;
    totalWeight += weight;
  }

  return weightedSum / totalWeight;
}

function getDefaultWeights(taskType: string): FactorWeights {
  const presets: Record<string, FactorWeights> = {
    analysis: {
      reasoning: 0.3,
      sources: 0.2,
      consistency: 0.2,
      completeness: 0.2,
      uncertainty: 0.1,
    },
    research: {
      reasoning: 0.2,
      sources: 0.35,
      consistency: 0.15,
      completeness: 0.2,
      uncertainty: 0.1,
    },
    creative: {
      reasoning: 0.15,
      sources: 0.1,
      consistency: 0.3,
      completeness: 0.35,
      uncertainty: 0.1,
    },
    code: {
      reasoning: 0.25,
      sources: 0.15,
      consistency: 0.3,
      completeness: 0.25,
      uncertainty: 0.05,
    },
  };

  return presets[taskType] ?? presets.analysis;
}
```

## Confidence Calibration

```typescript
interface CalibrationParams {
  historicalAccuracy: number;  // How accurate past confidence was
  taskDifficulty: number;      // Task complexity factor
  modelBias: number;           // Known overconfidence bias
}

function calibrateConfidence(
  rawConfidence: number,
  params: CalibrationParams
): number {
  // Apply Platt scaling-like calibration
  // Adjust for known overconfidence bias
  let calibrated = rawConfidence;

  // Reduce overconfidence (LLMs tend to be overconfident)
  calibrated *= (1 - params.modelBias);

  // Adjust based on historical accuracy
  if (params.historicalAccuracy < 0.8) {
    calibrated *= params.historicalAccuracy;
  }

  // Adjust for task difficulty
  const difficultyMultiplier = 1 - (params.taskDifficulty * 0.2);
  calibrated *= difficultyMultiplier;

  // Ensure bounds
  return Math.max(0.05, Math.min(0.95, calibrated));
}
```

## Threshold Decisions

```typescript
interface ThresholdConfig {
  accept: number;      // Above this: auto-accept
  review: number;      // Above this: human review
  reject: number;      // Below this: auto-reject
  iterate: number;     // Below this: require iteration
}

const DEFAULT_THRESHOLDS: ThresholdConfig = {
  accept: 0.85,
  review: 0.65,
  reject: 0.3,
  iterate: 0.5,
};

function determineAction(
  confidence: number,
  thresholds: ThresholdConfig = DEFAULT_THRESHOLDS
): ThresholdResult {
  let action: ThresholdResult['recommendedAction'];

  if (confidence >= thresholds.accept) {
    action = 'accept';
  } else if (confidence >= thresholds.review) {
    action = 'review';
  } else if (confidence >= thresholds.iterate) {
    action = 'iterate';
  } else {
    action = 'reject';
  }

  return {
    passesMinimum: confidence >= thresholds.reject,
    minimumThreshold: thresholds.reject,
    recommendedAction: action,
  };
}
```

## Confidence Report

```yaml
confidenceReport:
  nodeId: research-analyst
  outputId: analysis-2024-01-15
  scoredAt: "2024-01-15T10:30:00Z"

  scores:
    overall: 0.72
    calibrated: 0.65

  factors:
    reasoning:
      score: 0.75
      weight: 0.25
      contribution: 0.19
      evidence:
        - "Step-by-step analysis present"
        - "Evidence cited for claims"
        - "Missing consideration of alternatives"

    sources:
      score: 0.80
      weight: 0.30
      contribution: 0.24
      evidence:
        - "3 trusted sources cited"
        - "Official documentation referenced"
        - "1 unsourced strong claim detected"

    consistency:
      score: 0.85
      weight: 0.15
      contribution: 0.13
      evidence:
        - "No contradictions detected"
        - "Consistent terminology"

    completeness:
      score: 0.60
      weight: 0.20
      contribution: 0.12
      evidence:
        - "4/6 required topics covered"
        - "No conclusion section"

    uncertainty:
      score: 0.55
      weight: 0.10
      contribution: 0.06
      evidence:
        - "Limited uncertainty markers"
        - "No explicit confidence statement"

  calibration:
    raw: 0.72
    calibrated: 0.65
    adjustments:
      - factor: modelBias
        value: -0.05
        reason: "Known overconfidence in analysis tasks"
      - factor: taskDifficulty
        value: -0.02
        reason: "Moderate complexity task"

  thresholds:
    passesMinimum: true
    minimumThreshold: 0.30
    recommendedAction: review

  weakestFactors:
    - factor: uncertainty
      score: 0.55
      suggestion: "Add explicit confidence levels to claims"
    - factor: completeness
      score: 0.60
      suggestion: "Cover remaining topics: security, scalability"
```

## Integration Points

- **Input**: Validated outputs from `dag-output-validator`
- **Downstream**: `dag-hallucination-detector` for low confidence
- **Decisions**: `dag-iteration-detector` uses confidence thresholds
- **Learning**: `dag-pattern-learner` tracks calibration accuracy

## Best Practices

1. **Calibrate Regularly**: Update calibration with outcome data
2. **Task-Specific Weights**: Different tasks need different emphasis
3. **Transparent Breakdown**: Show what drives confidence
4. **Conservative Defaults**: Start with lower thresholds
5. **Track Accuracy**: Compare predictions to outcomes

---

Calibrated confidence. Multi-factor scoring. Informed decisions.
