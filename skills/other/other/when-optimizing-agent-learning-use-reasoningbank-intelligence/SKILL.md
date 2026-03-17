---
name: when-optimizing-agent-learning-use-reasoningbank-intelligence
version: 1.0.0
description: Implement adaptive learning with ReasoningBank for pattern recognition, strategy optimization, and continuous improvement
category: utilities
tags: [machine-learning, adaptive-learning, pattern-recognition, optimization]
agents: [safla-neural, ml-developer, performance-analyzer]
difficulty: advanced
estimated_duration: 30-45min
success_criteria:
  - Learning system initialized
  - Patterns captured and analyzed
  - Performance improvement > 15%
  - Strategies optimized
validation_method: performance_benchmark
dependencies:
  - claude-flow@alpha
  - reasoningbank
  - agentdb (optional for 150x faster vector ops)
outputs:
  - Trained learning model
  - Pattern library
  - Performance metrics
  - Optimization recommendations
triggers:
  - Need for agent improvement
  - Repetitive task optimization
  - Strategy refinement required
---

# ReasoningBank Intelligence - Adaptive Agent Learning

## Overview

Implement adaptive learning with ReasoningBank for pattern recognition, strategy optimization, and continuous improvement. Use when building self-learning agents, optimizing decision-making, or implementing meta-cognitive systems.

## When to Use

- Agent performance needs improvement
- Repetitive tasks require optimization
- Need pattern recognition from experience
- Strategy refinement through learning
- Building self-improving systems
- Meta-cognitive capabilities needed

## Theoretical Foundation

### ReasoningBank Architecture

1. **Trajectory Tracking**: Record decision paths and outcomes
2. **Verdict Judgment**: Evaluate success/failure of strategies
3. **Memory Distillation**: Extract patterns from experience
4. **Pattern Recognition**: Identify successful approaches
5. **Strategy Optimization**: Apply learned patterns to new situations

### AgentDB Integration (Optional)

- 150x faster vector operations
- HNSW indexing for similarity search
- Quantization for memory efficiency
- Batch operations for performance

## Phase 1: Initialize Learning System (10 min)

### Objective
Set up ReasoningBank with trajectory tracking

### Agent: ML-Developer

**Step 1.1: Initialize ReasoningBank**
```javascript
const ReasoningBank = require('reasoningbank');

const learningSystem = new ReasoningBank({
  storage: {
    type: 'agentdb', // Or 'memory', 'disk'
    path: './reasoning-bank-data',
    quantization: 'int8' // 4-32x memory reduction
  },
  indexing: {
    enabled: true,
    type: 'hnsw', // 150x faster search
    dimensions: 768
  },
  learning: {
    algorithm: 'decision-transformer',
    learningRate: 0.001,
    batchSize: 32
  }
});

await learningSystem.init();
await memory.store('reasoningbank/system', learningSystem.config);
```

**Step 1.2: Define Trajectory Schema**
```javascript
const trajectorySchema = {
  id: 'uuid',
  timestamp: 'datetime',
  context: {
    task: 'string',
    environment: 'object',
    constraints: 'array'
  },
  reasoning: [
    {
      step: 'number',
      thought: 'string',
      action: 'string',
      observation: 'string'
    }
  ],
  outcome: {
    success: 'boolean',
    metrics: 'object',
    verdict: 'string'
  }
};

await learningSystem.registerSchema('trajectory', trajectorySchema);
```

**Step 1.3: Configure Verdict Criteria**
```javascript
const verdictCriteria = {
  success: {
    thresholds: {
      performance: 0.8,
      efficiency: 0.75,
      quality: 0.9
    },
    weights: {
      performance: 0.4,
      efficiency: 0.3,
      quality: 0.3
    }
  },
  failure: {
    reasons: [
      'timeout',
      'error',
      'poor_quality',
      'resource_exhaustion'
    ]
  }
};

await learningSystem.configureVerdicts(verdictCriteria);
```

### Validation Criteria
- [ ] ReasoningBank initialized
- [ ] Trajectory schema registered
- [ ] Verdict criteria configured
- [ ] Storage backend ready

### Hooks Integration
```bash
npx claude-flow@alpha hooks pre-task \
  --description "Initialize ReasoningBank learning system" \
  --complexity "high"

npx claude-flow@alpha hooks post-task \
  --task-id "reasoningbank-init" \
  --memory-key "reasoningbank/initialization"
```

## Phase 2: Capture Patterns (10 min)

### Objective
Record agent decisions and outcomes for learning

### Agent: SAFLA-Neural

**Step 2.1: Track Trajectories**
```javascript
async function trackTrajectory(task, agent) {
  const trajectory = {
    id: generateUUID(),
    timestamp: new Date(),
    context: {
      task: task.description,
      environment: getEnvironment(),
      constraints: task.constraints
    },
    reasoning: []
  };

  // Hook into agent execution
  agent.on('thought', (thought) => {
    trajectory.reasoning.push({
      step: trajectory.reasoning.length + 1,
      thought: thought.text,
      action: null,
      observation: null
    });
  });

  agent.on('action', (action) => {
    const lastStep = trajectory.reasoning[trajectory.reasoning.length - 1];
    lastStep.action = action.description;
  });

  agent.on('observation', (obs) => {
    const lastStep = trajectory.reasoning[trajectory.reasoning.length - 1];
    lastStep.observation = obs.result;
  });

  agent.on('complete', async (result) => {
    trajectory.outcome = {
      success: result.success,
      metrics: result.metrics,
      verdict: await evaluateVerdict(result)
    };

    await learningSystem.storeTrajectory(trajectory);
  });

  return trajectory;
}
```

**Step 2.2: Evaluate Verdicts**
```javascript
async function evaluateVerdict(result) {
  const scores = {
    performance: result.metrics.score,
    efficiency: result.metrics.duration / result.metrics.expectedDuration,
    quality: result.metrics.qualityScore
  };

  const weightedScore = Object.keys(scores).reduce((sum, key) => {
    return sum + scores[key] * verdictCriteria.success.weights[key];
  }, 0);

  const verdict = {
    score: weightedScore,
    passed: weightedScore >= Object.values(verdictCriteria.success.thresholds)
      .reduce((sum, t) => sum + t, 0) / 3,
    breakdown: scores,
    reasoning: generateVerdictReasoning(scores, weightedScore)
  };

  await learningSystem.recordVerdict(result.id, verdict);
  return verdict;
}
```

**Step 2.3: Pattern Extraction**
```javascript
async function extractPatterns() {
  // Get all successful trajectories
  const successfulTrajectories = await learningSystem.query({
    'outcome.verdict.passed': true
  });

  // Extract common patterns using AgentDB vector similarity
  const patterns = await learningSystem.analyzePatterns({
    trajectories: successfulTrajectories,
    similarity: {
      method: 'cosine',
      threshold: 0.85,
      index: 'hnsw' // 150x faster
    },
    clustering: {
      algorithm: 'dbscan',
      minSamples: 3,
      epsilon: 0.15
    }
  });

  await memory.store('reasoningbank/patterns', patterns);
  return patterns;
}
```

### Validation Criteria
- [ ] Trajectories captured
- [ ] Verdicts evaluated
- [ ] Patterns extracted
- [ ] Similarity clustering complete

## Phase 3: Optimize Strategies (10 min)

### Objective
Apply learned patterns to improve future decisions

### Agent: Performance-Analyzer

**Step 3.1: Train Decision Model**
```javascript
async function trainDecisionModel(patterns) {
  // Use Decision Transformer (from ReasoningBank's 9 RL algorithms)
  const model = await learningSystem.createModel({
    algorithm: 'decision-transformer',
    config: {
      hiddenSize: 256,
      numLayers: 4,
      numHeads: 8,
      maxTrajectoryLength: 50,
      learningRate: 0.0001
    }
  });

  // Prepare training data from successful patterns
  const trainingData = patterns.map(pattern => ({
    states: pattern.reasoning.map(r => r.thought),
    actions: pattern.reasoning.map(r => r.action),
    rewards: calculateRewards(pattern.outcome),
    returns: calculateReturnsToGo(pattern.outcome)
  }));

  // Train with batch operations (AgentDB optimization)
  await model.train({
    data: trainingData,
    epochs: 100,
    batchSize: 32,
    validation: 0.2,
    callbacks: {
      onEpoch: (epoch, metrics) => {
        console.log(`Epoch ${epoch}: loss=${metrics.loss}, accuracy=${metrics.accuracy}`);
      }
    }
  });

  await learningSystem.saveModel('decision-model', model);
  return model;
}
```

**Step 3.2: Generate Strategy Recommendations**
```javascript
async function generateRecommendations() {
  const patterns = await memory.retrieve('reasoningbank/patterns');

  const recommendations = patterns.map(pattern => {
    const frequency = pattern.instances.length;
    const avgScore = pattern.instances.reduce((sum, i) =>
      sum + i.outcome.verdict.score, 0) / frequency;

    return {
      pattern: {
        description: summarizePattern(pattern),
        reasoning: pattern.commonReasoning,
        actions: pattern.commonActions
      },
      metrics: {
        frequency,
        avgScore,
        consistency: calculateConsistency(pattern.instances)
      },
      recommendation: {
        applicability: identifyApplicableContexts(pattern),
        priority: calculatePriority(frequency, avgScore),
        implementation: generateImplementationGuide(pattern)
      }
    };
  }).sort((a, b) => b.recommendation.priority - a.recommendation.priority);

  await memory.store('reasoningbank/recommendations', recommendations);
  return recommendations;
}
```

**Step 3.3: Apply Optimizations**
```javascript
async function applyOptimizations(agent, recommendations) {
  // Apply top 5 recommendations
  const topRecommendations = recommendations.slice(0, 5);

  for (const rec of topRecommendations) {
    // Update agent strategy
    await agent.updateStrategy({
      pattern: rec.pattern,
      priority: rec.recommendation.priority,
      applicableContexts: rec.recommendation.applicability
    });

    console.log(`✅ Applied: ${rec.pattern.description}`);
  }

  // Update agent's decision model
  const model = await learningSystem.loadModel('decision-model');
  agent.setDecisionModel(model);

  await memory.store('reasoningbank/applied-optimizations', topRecommendations);
}
```

### Validation Criteria
- [ ] Model trained successfully
- [ ] Recommendations generated
- [ ] Top strategies identified
- [ ] Optimizations applied

## Phase 4: Validate Learning (10 min)

### Objective
Measure improvement from adaptive learning

### Agent: Performance-Analyzer

**Step 4.1: Benchmark Performance**
```javascript
async function benchmarkPerformance(agent, testCases) {
  const results = {
    baseline: [],
    optimized: []
  };

  // Baseline: Agent without learning
  const baselineAgent = agent.clone({ useLearning: false });
  for (const testCase of testCases) {
    const result = await baselineAgent.execute(testCase);
    results.baseline.push({
      testId: testCase.id,
      metrics: result.metrics,
      success: result.success
    });
  }

  // Optimized: Agent with learning
  const optimizedAgent = agent.clone({ useLearning: true });
  for (const testCase of testCases) {
    const result = await optimizedAgent.execute(testCase);
    results.optimized.push({
      testId: testCase.id,
      metrics: result.metrics,
      success: result.success
    });
  }

  await memory.store('reasoningbank/benchmark-results', results);
  return results;
}
```

**Step 4.2: Calculate Improvement Metrics**
```javascript
function calculateImprovement(results) {
  const baselineAvg = calculateAverage(results.baseline.map(r => r.metrics.score));
  const optimizedAvg = calculateAverage(results.optimized.map(r => r.metrics.score));

  const improvement = {
    scoreImprovement: ((optimizedAvg - baselineAvg) / baselineAvg * 100).toFixed(2) + '%',
    successRateImprovement: calculateSuccessRateImprovement(results),
    efficiencyImprovement: calculateEfficiencyImprovement(results),
    qualityImprovement: calculateQualityImprovement(results)
  };

  return improvement;
}
```

**Step 4.3: Validate Patterns**
```javascript
async function validatePatterns(patterns, testResults) {
  const validation = patterns.map(pattern => {
    // Find test results that used this pattern
    const patternResults = testResults.optimized.filter(r =>
      r.usedPattern === pattern.id
    );

    const successRate = patternResults.filter(r => r.success).length / patternResults.length;

    return {
      pattern: pattern.description,
      timesUsed: patternResults.length,
      successRate,
      avgScore: calculateAverage(patternResults.map(r => r.metrics.score)),
      validated: successRate > 0.8
    };
  });

  await memory.store('reasoningbank/pattern-validation', validation);
  return validation;
}
```

### Validation Criteria
- [ ] Benchmarks completed
- [ ] Improvement > 15%
- [ ] Patterns validated
- [ ] Success rate improved

## Phase 5: Deploy Optimizations (5 min)

### Objective
Integrate learned strategies into production agents

### Agent: ML-Developer

**Step 5.1: Export Learned Model**
```javascript
async function exportModel() {
  const model = await learningSystem.loadModel('decision-model');
  const patterns = await memory.retrieve('reasoningbank/patterns');
  const recommendations = await memory.retrieve('reasoningbank/recommendations');

  const exportPackage = {
    version: '1.0.0',
    timestamp: new Date(),
    model: {
      weights: await model.exportWeights(),
      config: model.config,
      performance: await memory.retrieve('reasoningbank/benchmark-results')
    },
    patterns: patterns.map(p => ({
      id: p.id,
      description: p.description,
      reasoning: p.commonReasoning,
      actions: p.commonActions,
      metrics: p.metrics
    })),
    recommendations: recommendations
  };

  await fs.writeFile(
    '/tmp/reasoningbank-export.json',
    JSON.stringify(exportPackage, null, 2)
  );

  console.log('✅ Model exported to: /tmp/reasoningbank-export.json');
}
```

**Step 5.2: Create Integration Guide**
```markdown
# ReasoningBank Integration Guide

## Installation
\`\`\`bash
npm install reasoningbank
\`\`\`

## Import Learned Model
\`\`\`javascript
const { ReasoningBank } = require('reasoningbank');
const learnedModel = require('./reasoningbank-export.json');

const agent = new Agent({
  decisionModel: learnedModel.model,
  patterns: learnedModel.patterns,
  recommendations: learnedModel.recommendations
});
\`\`\`

## Usage
\`\`\`javascript
// Agent automatically uses learned strategies
const result = await agent.execute(task);
\`\`\`

## Performance Gains
${improvement.scoreImprovement} average improvement
${improvement.successRateImprovement} success rate increase
```

**Step 5.3: Generate Learning Report**
```javascript
const learningReport = {
  summary: {
    totalTrajectories: await learningSystem.countTrajectories(),
    patternsIdentified: patterns.length,
    recommendationsGenerated: recommendations.length,
    improvement: improvement
  },
  topPatterns: patterns.slice(0, 10),
  performanceMetrics: {
    baseline: baselineMetrics,
    optimized: optimizedMetrics,
    improvement: improvement
  },
  nextSteps: [
    'Continue collecting trajectories for ongoing learning',
    'Monitor production performance',
    'Retrain model quarterly',
    'A/B test new patterns'
  ]
};

await fs.writeFile(
  '/tmp/learning-report.json',
  JSON.stringify(learningReport, null, 2)
);
```

### Validation Criteria
- [ ] Model exported
- [ ] Integration guide created
- [ ] Learning report generated
- [ ] Ready for production

## Success Metrics

- Performance improvement > 15%
- Pattern recognition accuracy > 85%
- Model training successful
- Production integration ready

## Memory Schema

```javascript
{
  "reasoningbank/": {
    "session-${id}/": {
      "system": {},
      "patterns": [],
      "recommendations": [],
      "benchmark-results": {},
      "pattern-validation": [],
      "applied-optimizations": []
    }
  }
}
```

## Integration with AgentDB

For 150x faster operations:

```javascript
const AgentDB = require('agentdb');

const db = new AgentDB({
  quantization: 'int8',
  indexing: 'hnsw',
  caching: true
});

await learningSystem.useVectorDB(db);
```

## Skill Completion

Outputs:
1. **reasoningbank-export.json**: Trained model and patterns
2. **learning-report.json**: Performance analysis
3. **integration-guide.md**: Implementation instructions
4. **pattern-library.json**: Validated patterns

Complete when improvement > 15% and ready for production deployment.
