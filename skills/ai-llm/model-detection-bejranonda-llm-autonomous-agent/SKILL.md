---
name: model-detection
description: Universal model detection and capability assessment for optimal cross-model compatibility
version: 1.0.0
---

## Overview

This skill provides universal model detection and capability assessment to optimize the Autonomous Agent Plugin across different LLM models (Claude Sonnet, Claude 4.5, GLM-4.6, etc.).

## Model Detection Algorithm

### Primary Detection Methods

1. **System Context Analysis**:
   ```javascript
   // Check for model indicators in system context
   const modelIndicators = {
     'claude-sonnet-4.5': { pattern: /sonnet.*4\.5|4\.5.*sonnet/i, confidence: 0.9 },
     'claude-haiku-4.5': { pattern: /haiku.*4\.5|4\.5.*haiku/i, confidence: 0.9 },
     'claude-opus-4.1': { pattern: /opus.*4\.1|4\.1.*opus/i, confidence: 0.9 },
     'glm-4.6': { pattern: /glm|4\.6/i, confidence: 0.9 },
     'claude-haiku': { pattern: /haiku(?!\.*4\.5)/i, confidence: 0.8 }
   }
   ```

2. **Performance Pattern Recognition**:
   ```javascript
   // Analyze execution patterns to identify model
   const performanceSignatures = {
     'claude-sonnet-4.5': { reasoning: 'nuanced', speed: 'fast', adaptability: 'high' },
     'claude-haiku-4.5': { reasoning: 'focused', speed: 'very_fast', adaptability: 'high' },
     'claude-opus-4.1': { reasoning: 'enhanced', speed: 'very_fast', adaptability: 'very_high' },
     'glm-4.6': { reasoning: 'structured', speed: 'moderate', adaptability: 'medium' }
   }
   ```

3. **Capability Assessment**:
   ```javascript
   // Test specific capabilities
   const capabilityTests = {
     nuanced_reasoning: testAmbiguousScenario,
     structured_execution: testLiteralInterpretation,
     context_switching: testMultiTaskContext,
     adaptive_learning: testPatternRecognition
   }
   ```

## Model-Specific Configurations

### Claude Sonnet 4.5 Configuration
```json
{
  "model_type": "claude-sonnet-4.5",
  "capabilities": {
    "reasoning_style": "nuanced",
    "context_management": "adaptive",
    "skill_loading": "progressive_disclosure",
    "error_handling": "pattern_based",
    "communication_style": "natural_flow"
  },
  "performance_targets": {
    "execution_time_multiplier": 1.0,
    "quality_score_target": 90,
    "autonomy_level": "high",
    "delegation_style": "parallel_context_merge"
  },
  "optimizations": {
    "use_context_switching": true,
    "apply_improvisation": true,
    "weight_based_decisions": true,
    "predictive_delegation": true
  }
}
```

### Claude Haiku 4.5 Configuration
```json
{
  "model_type": "claude-haiku-4.5",
  "capabilities": {
    "reasoning_style": "focused",
    "context_management": "efficient",
    "skill_loading": "selective_disclosure",
    "error_handling": "fast_prevention",
    "communication_style": "concise"
  },
  "performance_targets": {
    "execution_time_multiplier": 0.8,
    "quality_score_target": 88,
    "autonomy_level": "medium",
    "delegation_style": "focused_parallel"
  },
  "optimizations": {
    "use_fast_execution": true,
    "apply_focused_reasoning": true,
    "efficient_delegation": true,
    "streamlined_processing": true
  }
}
```

### Claude Opus 4.1 Configuration
```json
{
  "model_type": "claude-opus-4.1",
  "capabilities": {
    "reasoning_style": "enhanced",
    "context_management": "predictive",
    "skill_loading": "intelligent_progressive",
    "error_handling": "predictive_prevention",
    "communication_style": "insightful"
  },
  "performance_targets": {
    "execution_time_multiplier": 0.9,
    "quality_score_target": 95,
    "autonomy_level": "very_high",
    "delegation_style": "predictive_parallel"
  },
  "optimizations": {
    "use_context_switching": true,
    "apply_improvisation": true,
    "anticipatory_actions": true,
    "enhanced_pattern_learning": true
  }
}
```

### GLM-4.6 Configuration
```json
{
  "model_type": "glm-4.6",
  "capabilities": {
    "reasoning_style": "structured",
    "context_management": "sequential",
    "skill_loading": "complete_loading",
    "error_handling": "rule_based",
    "communication_style": "structured_explicit"
  },
  "performance_targets": {
    "execution_time_multiplier": 1.25,
    "quality_score_target": 88,
    "autonomy_level": "medium",
    "delegation_style": "sequential_clear"
  },
  "optimizations": {
    "use_structured_decisions": true,
    "explicit_instructions": true,
    "sequential_processing": true,
    "clear_handoffs": true
  }
}
```

## Adaptive Execution Strategies

### Skill Loading Adaptation

**Claude Models**:
```javascript
function loadSkillsForClaude(skills) {
  // Progressive disclosure with context merging
  return skills.map(skill => ({
    ...skill,
    loading_strategy: 'progressive',
    context_aware: true,
    weight_based: true
  }));
}
```

**GLM Models**:
```javascript
function loadSkillsForGLM(skills) {
  // Complete upfront loading with clear structure
  return skills.map(skill => ({
    ...skill,
    loading_strategy: 'complete',
    explicit_criteria: true,
    priority_sequenced: true
  }));
}
```

### Communication Style Adaptation

**Output Formatting by Model**:

| Model | Terminal Style | File Report Style | Reasoning |
|-------|----------------|-------------------|-----------|
| Claude Sonnet | Natural flow | Insightful analysis | Nuanced communication |
| Claude 4.5 | Concise insights | Enhanced context | Predictive communication |
| GLM-4.6 | Structured lists | Detailed procedures | Explicit communication |

### Error Recovery Adaptation

**Claude Models**: Pattern-based prediction and contextual prevention
**GLM Models**: Rule-based detection and structured recovery protocols

## Capability Testing Functions

### Nuanced Reasoning Test
```javascript
function testNuancedReasoning() {
  // Present ambiguous scenario requiring subtle judgment
  // Evaluate response quality and contextual awareness
  return score >= 0.8; // True for Claude models
}
```

### Structured Execution Test
```javascript
function testStructuredExecution() {
  // Present clear, sequential task
  // Evaluate adherence to structured approach
  return score >= 0.8; // True for GLM models
}
```

## Model Detection Implementation

### Auto-Detection Function
```javascript
function detectModel() {
  // Step 1: Check system context indicators
  const contextResult = analyzeSystemContext();

  // Step 2: Test capability patterns
  const capabilityResult = testCapabilities();

  // Step 3: Analyze performance signature
  const performanceResult = analyzePerformancePattern();

  // Step 4: Combine results with confidence scoring
  return combineDetections(contextResult, capabilityResult, performanceResult);
}
```

### Configuration Loading
```javascript
function loadModelConfiguration(detectedModel) {
  const baseConfig = getBaseModelConfig(detectedModel);
  const adaptiveConfig = generateAdaptiveConfig(detectedModel);
  return mergeConfigurations(baseConfig, adaptiveConfig);
}
```

## Usage Guidelines

### When to Apply Model Detection
1. **Plugin Initialization**: First load of any agent
2. **Agent Delegation**: Before delegating to specialized agents
3. **Skill Loading**: Before loading any skill package
4. **Error Recovery**: When selecting recovery strategy
5. **Performance Optimization**: When setting execution targets

### Integration Points
- **Orchestrator Agent**: Use for autonomous decision-making adaptation
- **All Specialized Agents**: Use for model-specific behavior
- **Skill System**: Use for loading strategy selection
- **Quality Controller**: Use for model-appropriate quality targets

## Fallback Strategy

If model detection fails:
1. **Default to Conservative Settings**: Use structured, explicit approach
2. **Basic Capability Tests**: Run simplified detection tests
3. **Universal Configuration**: Apply cross-model compatible settings
4. **Performance Monitoring**: Continuously assess and adapt

## Validation Metrics

### Detection Accuracy
- Target: >95% correct model identification
- Measurement: Compare detected vs actual model capabilities
- Validation: Test across all supported models

### Performance Improvement
- Target: >10% improvement for GLM models
- Target: >2% improvement for Claude models
- Measurement: Compare pre/post optimization performance

### Adaptation Success
- Target: >90% successful adaptation scenarios
- Measurement: Monitor successful autonomous operations
- Validation: Test with diverse task types

This skill ensures the Autonomous Agent Plugin performs optimally across all supported LLM models while maintaining backward compatibility and future-proofing for new models.