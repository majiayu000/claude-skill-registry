---
name: performance-scaling
description: Cross-model performance optimization and scaling configurations for autonomous agents
version: 1.0.0
---

## Overview

This skill provides performance scaling and optimization strategies for autonomous agents across different LLM models, ensuring optimal execution characteristics while maintaining quality standards.

## Model Performance Profiles

### Claude Sonnet 4.5 Performance Profile
```json
{
  "model": "claude-sonnet-4.5",
  "base_performance": {
    "execution_speed": "fast",
    "reasoning_depth": "high",
    "context_switching": "excellent",
    "adaptability": "very_high"
  },
  "scaling_factors": {
    "time_multiplier": 1.0,
    "quality_target": 90,
    "complexity_handling": 0.9,
    "parallel_processing": 1.2
  },
  "optimization_strategies": [
    "context_merging",
    "predictive_delegation",
    "pattern_weighting",
    "adaptive_quality_thresholds"
  ]
}
```

### Claude Haiku 4.5 Performance Profile
```json
{
  "model": "claude-haiku-4.5",
  "base_performance": {
    "execution_speed": "very_fast",
    "reasoning_depth": "medium",
    "context_switching": "good",
    "adaptability": "high"
  },
  "scaling_factors": {
    "time_multiplier": 0.8,
    "quality_target": 88,
    "complexity_handling": 1.1,
    "parallel_processing": 1.0
  },
  "optimization_strategies": [
    "fast_execution",
    "selective_processing",
    "efficient_delegation",
    "streamlined_quality_checks"
  ]
}
```

### Claude Opus 4.1 Performance Profile
```json
{
  "model": "claude-opus-4.1",
  "base_performance": {
    "execution_speed": "very_fast",
    "reasoning_depth": "very_high",
    "context_switching": "excellent",
    "adaptability": "maximum"
  },
  "scaling_factors": {
    "time_multiplier": 0.9,
    "quality_target": 95,
    "complexity_handling": 0.8,
    "parallel_processing": 1.4
  },
  "optimization_strategies": [
    "anticipatory_execution",
    "enhanced_parallelization",
    "predictive_caching",
    "advanced_pattern_recognition"
  ]
}
```

### GLM-4.6 Performance Profile
```json
{
  "model": "glm-4.6",
  "base_performance": {
    "execution_speed": "moderate",
    "reasoning_depth": "medium",
    "context_switching": "good",
    "adaptability": "medium"
  },
  "scaling_factors": {
    "time_multiplier": 1.25,
    "quality_target": 88,
    "complexity_handling": 1.2,
    "parallel_processing": 0.8
  },
  "optimization_strategies": [
    "structured_sequencing",
    "explicit_instruction_optimization",
    "step_by_step_validation",
    "clear_handoff_protocols"
  ]
}
```

## Performance Scaling Strategies

### Time-Based Scaling

**Execution Time Allocation**:
```javascript
function scaleExecutionTime(baseTime, model, complexity) {
  const profiles = {
    'claude-sonnet': { multiplier: 1.0, complexity_factor: 0.9 },
    'claude-4.5': { multiplier: 0.9, complexity_factor: 0.8 },
    'glm-4.6': { multiplier: 1.25, complexity_factor: 1.2 },
    'fallback': { multiplier: 1.5, complexity_factor: 1.4 }
  };

  const profile = profiles[model] || profiles.fallback;
  return baseTime * profile.multiplier * (1 + complexity * profile.complexity_factor);
}
```

**Timeout Adjustments**:
- **Claude Sonnet**: Standard timeouts with 10% buffer
- **Claude 4.5**: Reduced timeouts with 5% buffer
- **GLM-4.6**: Extended timeouts with 25% buffer
- **Fallback**: Conservative timeouts with 50% buffer

### Quality Target Scaling

**Model-Specific Quality Targets**:
```javascript
function getQualityTarget(model, taskType) {
  const baseTargets = {
    'claude-sonnet': { simple: 85, complex: 90, critical: 95 },
    'claude-4.5': { simple: 88, complex: 92, critical: 96 },
    'glm-4.6': { simple: 82, complex: 88, critical: 92 },
    'fallback': { simple: 80, complex: 85, critical: 90 }
  };

  return baseTargets[model]?.[taskType] || baseTargets.fallback.complex;
}
```

**Quality Assessment Adaptation**:
- **Claude Models**: Emphasize contextual understanding and pattern recognition
- **GLM Models**: Emphasize structured accuracy and procedural correctness

### Resource Scaling

**Memory Management**:
```javascript
function scaleMemoryUsage(model, taskSize) {
  const profiles = {
    'claude-sonnet': { base_memory: 'medium', scaling_factor: 1.1 },
    'claude-4.5': { base_memory: 'medium', scaling_factor: 1.0 },
    'glm-4.6': { base_memory: 'high', scaling_factor: 1.3 },
    'fallback': { base_memory: 'high', scaling_factor: 1.5 }
  };

  const profile = profiles[model] || profiles.fallback;
  return allocateMemory(profile.base_memory, taskSize * profile.scaling_factor);
}
```

**Concurrent Task Limits**:
- **Claude Sonnet**: 3-4 concurrent tasks
- **Claude 4.5**: 4-5 concurrent tasks
- **GLM-4.6**: 2-3 concurrent tasks
- **Fallback**: 1-2 concurrent tasks

## Adaptive Optimization Algorithms

### Dynamic Performance Adjustment

**Real-Time Performance Monitoring**:
```javascript
function monitorPerformance(model, currentMetrics) {
  const baseline = getPerformanceBaseline(model);
  const variance = calculateVariance(currentMetrics, baseline);

  if (variance > 0.2) {
    // Performance deviating significantly from baseline
    return adjustPerformanceParameters(model, currentMetrics);
  }

  return currentMetrics;
}
```

**Automatic Parameter Tuning**:
```javascript
function tuneParameters(model, taskHistory) {
  const performance = analyzeTaskPerformance(taskHistory);
  const adjustments = calculateOptimalAdjustments(model, performance);

  return {
    timeout_adjustments: adjustments.timeouts,
    quality_thresholds: adjustments.quality,
    resource_allocation: adjustments.resources,
    delegation_strategy: adjustments.delegation
  };
}
```

### Learning-Based Optimization

**Pattern Recognition for Performance**:
```javascript
function learnPerformancePatterns(executionHistory) {
  const patterns = {
    successful_executions: extractSuccessPatterns(executionHistory),
    failed_executions: extractFailurePatterns(executionHistory),
    optimization_opportunities: identifyOptimizations(executionHistory)
  };

  return generatePerformanceRecommendations(patterns);
}
```

**Model-Specific Learning**:
- **Claude Models**: Learn from nuanced patterns and contextual factors
- **GLM Models**: Learn from structured procedures and clear success/failure patterns

## Performance Metrics and KPIs

### Core Performance Indicators

**Execution Metrics**:
- **Task Completion Time**: Time from task start to completion
- **Quality Achievement**: Final quality score vs target
- **Resource Efficiency**: Memory and CPU usage efficiency
- **Error Rate**: Frequency of errors requiring recovery

**Model-Specific KPIs**:
```javascript
const modelKPIs = {
  'claude-sonnet': {
    'context_switching_efficiency': '>= 90%',
    'pattern_recognition_accuracy': '>= 85%',
    'adaptive_decision_quality': '>= 88%'
  },
  'claude-4.5': {
    'predictive_accuracy': '>= 80%',
    'anticipatory_optimization': '>= 75%',
    'enhanced_reasoning_utilization': '>= 90%'
  },
  'glm-4.6': {
    'procedural_accuracy': '>= 95%',
    'structured_execution_compliance': '>= 98%',
    'explicit_instruction_success': '>= 92%'
  }
};
```

### Performance Benchmarking

**Comparative Analysis**:
```javascript
function benchmarkPerformance(model, testSuite) {
  const results = runPerformanceTests(model, testSuite);
  const baseline = getIndustryBaseline(model);

  return {
    relative_performance: results.score / baseline.score,
    improvement_opportunities: identifyImprovements(results, baseline),
    model_strengths: analyzeModelStrengths(results),
    optimization_recommendations: generateRecommendations(results)
  };
}
```

## Performance Optimization Techniques

### Model-Specific Optimizations

**Claude Sonnet Optimizations**:
1. **Context Merging**: Combine related contexts to reduce switching overhead
2. **Weight-Based Decision Making**: Use historical success patterns for decisions
3. **Progressive Loading**: Load skills progressively based on immediate needs
4. **Adaptive Quality Thresholds**: Adjust quality targets based on task complexity

**Claude 4.5 Optimizations**:
1. **Anticipatory Execution**: Start likely tasks before explicit request
2. **Enhanced Parallelization**: Maximize concurrent task execution
3. **Predictive Caching**: Cache likely-needed resources proactively
4. **Advanced Pattern Matching**: Use complex pattern recognition for optimization

**GLM-4.6 Optimizations**:
1. **Structured Sequencing**: Optimize task order for efficiency
2. **Explicit Instruction Optimization**: Minimize ambiguity in instructions
3. **Step-by-Step Validation**: Validate each step before proceeding
4. **Clear Handoff Protocols**: Ensure clean transitions between tasks

### Universal Optimizations

**Cross-Model Techniques**:
1. **Resource Pooling**: Share resources across compatible tasks
2. **Intelligent Caching**: Cache results based on usage patterns
3. **Batch Processing**: Group similar operations for efficiency
4. **Lazy Loading**: Load resources only when needed

## Implementation Guidelines

### Performance Configuration Loading

```javascript
function loadPerformanceConfiguration(model) {
  const baseConfig = getBasePerformanceProfile(model);
  const historicalData = getHistoricalPerformanceData(model);
  const currentContext = assessCurrentContext();

  return mergeAndOptimizeConfiguration(baseConfig, historicalData, currentContext);
}
```

### Runtime Performance Adjustment

```javascript
function adjustRuntimePerformance(currentMetrics, targetProfile) {
  const adjustments = calculateNeededAdjustments(currentMetrics, targetProfile);

  return {
    timeout_adjustments: adjustments.timeouts,
    quality_modifications: adjustments.quality,
    resource_reallocation: adjustments.resources,
    strategy_changes: adjustments.strategy
  };
}
```

### Performance Monitoring and Alerting

```javascript
function monitorPerformanceHealth(model, metrics) {
  const healthScore = calculatePerformanceHealth(model, metrics);

  if (healthScore < 0.8) {
    return {
      status: 'degraded',
      recommendations: generateImprovementActions(model, metrics),
      automatic_adjustments: applyAutomaticOptimizations(model, metrics)
    };
  }

  return { status: 'healthy', score: healthScore };
}
```

## Usage Guidelines

### When to Apply Performance Scaling

1. **Task Initialization**: Set performance targets based on model and task type
2. **Mid-Execution Adjustment**: Adapt parameters based on current performance
3. **Resource Optimization**: Scale resource allocation based on availability
4. **Quality-Performance Tradeoffs**: Balance speed vs accuracy based on requirements

### Integration Points

- **Orchestrator Agent**: Use for task planning and resource allocation
- **All Specialized Agents**: Use for model-specific execution optimization
- **Quality Controller**: Use for adaptive quality target setting
- **Background Task Manager**: Use for concurrent task optimization

This skill ensures optimal performance across all supported models while maintaining high quality standards and adapting to varying task requirements.