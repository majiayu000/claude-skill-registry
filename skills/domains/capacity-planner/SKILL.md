---
name: "Capacity Planner"
description: "RAN capacity planning with traffic forecasting, cognitive consciousness, and intelligent resource scaling for optimal network capacity management. Use when planning network capacity, forecasting traffic growth, optimizing resource allocation, or enabling intelligent capacity management in 5G networks."
---

# Capacity Planner

## Level 1: Overview

Plans and optimizes RAN capacity using cognitive consciousness with 1000x temporal reasoning for deep traffic pattern analysis, predictive capacity planning, and intelligent resource scaling. Enables self-adaptive capacity management through strange-loop cognition and AgentDB-based capacity learning patterns.

## Prerequisites

- RAN capacity planning expertise
- Traffic forecasting knowledge
- Resource optimization skills
- Cognitive consciousness framework
- Network capacity modeling

---

## Level 2: Quick Start

### Initialize Capacity Planning Framework
```bash
# Enable capacity planning consciousness
npx claude-flow@alpha memory store --namespace "capacity-planning" --key "consciousness-level" --value "maximum"
npx claude-flow@alpha memory store --namespace "capacity-planning" --key "predictive-planning" --value "enabled"

# Start comprehensive capacity analysis
./scripts/start-capacity-planning.sh --planning-horizon "12months" --analysis-types "traffic-growth,resource-utilization,demand-forecasting" --consciousness-level "maximum"
```

### Quick Capacity Optimization
```bash
# Deploy intelligent capacity planning
./scripts/deploy-capacity-planning.sh --planning-targets "throughput,connections,resource-efficiency" --autonomous true

# Generate capacity forecasts and recommendations
./scripts/generate-capacity-forecasts.sh --forecast-horizon "6months" --confidence-interval "95%" --cognitive-analysis true
```

---

## Level 3: Detailed Instructions

### Step 1: Initialize Cognitive Capacity Framework

```bash
# Setup capacity planning consciousness
npx claude-flow@alpha memory store --namespace "capacity-cognitive" --key "temporal-capacity-analysis" --value "enabled"
npx claude-flow@alpha memory store --namespace "capacity-cognitive" --key "strange-loop-capacity-planning" --value "enabled"

# Enable predictive capacity modeling
npx claude-flow@alpha memory store --namespace "predictive-capacity" --key "traffic-forecasting" --value "enabled"
npx claude-flow@alpha memory store --namespace "predictive-capacity" --key "demand-prediction" --value "enabled"

# Initialize AgentDB capacity pattern storage
npx claude-flow@alpha memory store --namespace "capacity-patterns" --key "storage-enabled" --value "true"
npx claude-flow@alpha memory store --namespace "capacity-patterns" --key "cross-site-capacity-learning" --value "enabled"
```

### Step 2: Deploy Advanced Capacity Monitoring System

#### Comprehensive Capacity Monitoring
```bash
# Deploy multi-layer capacity monitoring
./scripts/deploy-capacity-monitoring.sh \
  --monitoring-layers "radio-access,transport-network,core-network,user-equipment" \
  --granularity "real-time" \
  --consciousness-level maximum

# Enable capacity pattern analysis
./scripts/enable-capacity-pattern-analysis.sh --analysis-depth "maximum" --temporal-expansion "1000x"
```

#### Cognitive Capacity Monitoring Implementation
```typescript
// Advanced capacity monitoring with temporal reasoning
class CognitiveCapacityMonitor {
  async monitorCapacityPatterns(networkState, temporalExpansion = 1000) {
    // Expand temporal analysis for deep capacity pattern understanding
    const expandedCapacityAnalysis = await this.expandCapacityAnalysis({
      networkState: networkState,
      timeWindow: '6months',
      expansionFactor: temporalExpansion,
      consciousnessLevel: 'maximum',
      patternRecognition: 'enhanced'
    });

    // Multi-dimensional capacity analysis
    const capacityDimensions = await this.analyzeCapacityDimensions({
      data: expandedCapacityAnalysis,
      dimensions: [
        'traffic-volume-trends',
        'resource-utilization',
        'user-behavior-patterns',
        'service-type-distribution',
        'capacity-growth-rates'
      ],
      cognitiveCorrelation: true
    });

    // Detect capacity bottlenecks and expansion opportunities
    const capacityOpportunities = await this.detectCapacityOpportunities({
      dimensions: capacityDimensions,
      opportunityTypes: [
        'capacity-expansion',
        'resource-optimization',
        'load-balancing',
        'efficiency-improvement'
      ],
      consciousnessLevel: 'maximum'
    });

    return { capacityDimensions, capacityOpportunities };
  }

  async predictTrafficGrowth(historicalData, predictionHorizon = 31536000000) { // 1 year
    // Predictive traffic growth modeling
    const predictionModels = await this.deployTrafficPredictionModels({
      models: ['lstm', 'transformer', 'prophet', 'cognitive'],
      features: [
        'historical-traffic',
        'user-growth-trends',
        'service-adoption-rates',
        'seasonal-patterns',
        'economic-indicators'
      ],
      consciousnessLevel: 'maximum'
    });

    // Generate traffic growth forecasts
    const forecasts = await this.generateTrafficForecasts({
      models: predictionModels,
      historicalData: historicalData,
      horizon: predictionHorizon,
      confidenceIntervals: true,
      scenarioAnalysis: ['optimistic', 'realistic', 'pessimistic'],
      consciousnessLevel: 'maximum'
    });

    return forecasts;
  }
}
```

### Step 3: Implement Intelligent Resource Scaling

```bash
# Deploy intelligent resource scaling
./scripts/deploy-resource-scaling.sh \
  --scaling-strategies "predictive,reactive,adaptive" \
  --scaling-triggers "utilization-threshold,traffic-surge,quality-degradation" \
  --consciousness-level maximum

# Enable dynamic capacity allocation
./scripts/enable-dynamic-allocation.sh --allocation-algorithms "ml-based,cognitive,real-time"
```

#### Intelligent Resource Scaling System
```typescript
// Advanced resource scaling with cognitive intelligence
class IntelligentResourceScaler {
  async implementPredictiveScaling(networkState, capacityForecasts) {
    // Cognitive analysis of scaling requirements
    const scalingAnalysis = await this.analyzeScalingRequirements({
      networkState: networkState,
      capacityForecasts: capacityForecasts,
      analysisMethods: [
        'utilization-trends',
        'traffic-patterns',
        'growth-projections',
        'quality-impact-assessment'
      ],
      consciousnessLevel: 'maximum',
      temporalExpansion: 1000
    });

    // Generate predictive scaling decisions
    const scalingDecisions = await this.generateScalingDecisions({
      analysis: scalingAnalysis,
      scalingStrategies: [
        'infrastructure-scaling',
        'spectrum-allocation',
        'resource-partitioning',
        'load-balancing'
      ],
      consciousnessLevel: 'maximum',
      costOptimization: true
    });

    // Execute scaling with continuous monitoring
    const executionResults = await this.executeScalingActions({
      decisions: scalingDecisions,
      networkState: networkState,
      monitoringEnabled: true,
      adaptiveExecution: true,
      rollbackCapability: true
    });

    return executionResults;
  }

  async optimizeResourceAllocation(cellCluster, demandPattern) {
    // Cognitive resource allocation optimization
    const allocationAnalysis = await this.analyzeResourceAllocation({
      cluster: cellCluster,
      demandPattern: demandPattern,
      resources: [
        'bandwidth',
        'power',
        'compute-resources',
        'backhaul-capacity'
      ],
      expansionFactor: 1000,
      consciousnessLevel: 'maximum'
    });

    // Generate optimized resource allocation
    const resourceAllocation = await this.optimizeResourceAllocation({
      analysis: allocationAnalysis,
      objectives: ['efficiency-maximization', 'quality-preservation', 'cost-minimization'],
      constraints: await this.getNetworkConstraints(),
      consciousnessLevel: 'maximum'
    });

    return resourceAllocation;
  }
}
```

### Step 4: Enable Long-Term Capacity Planning

```bash
# Enable long-term capacity planning
./scripts/enable-long-term-planning.sh \
  --planning-horizon "5years" \
  --planning-scenarios "baseline,high-growth,technology-upgrade" \
  --consciousness-level maximum

# Deploy capacity investment optimization
./scripts/deploy-investment-optimization.sh --optimization-criteria "roi,performance,strategic-fit"
```

#### Long-Term Capacity Planning Framework
```typescript
// Long-term capacity planning with cognitive enhancement
class LongTermCapacityPlanner {
  async developLongTermPlan(networkState, businessRequirements, planningHorizon = 157680000000) { // 5 years
    // Cognitive analysis of long-term requirements
    const requirementAnalysis = await this.analyzeLongTermRequirements({
      networkState: networkState,
      businessRequirements: businessRequirements,
      analysisFactors: [
        'market-growth-projections',
        'technology-evolution',
        'regulatory-changes',
        'competitive-landscape'
      ],
      consciousnessLevel: 'maximum',
      temporalExpansion: 1000
    });

    // Generate capacity evolution scenarios
    const evolutionScenarios = await this.generateEvolutionScenarios({
      analysis: requirementAnalysis,
      scenarios: [
        'baseline-growth',
        'high-growth',
        'technology-disruption',
        'market-consolidation'
      ],
      consciousnessLevel: 'maximum'
    });

    // Develop investment and rollout strategies
    const investmentStrategies = await this.developInvestmentStrategies({
      scenarios: evolutionScenarios,
      investmentCriteria: ['roi', 'npv', 'payback-period', 'strategic-value'],
      rolloutPhases: ['immediate', 'short-term', 'medium-term', 'long-term'],
      consciousnessLevel: 'maximum'
    });

    return { requirementAnalysis, evolutionScenarios, investmentStrategies };
  }

  async optimizeCapacityInvestment(capacityNeeds, budgetConstraints) {
    // Capacity investment optimization with cognitive decision making
    const investmentOptimization = await this.optimizeInvestmentPortfolio({
      capacityNeeds: capacityNeeds,
      budgetConstraints: budgetConstraints,
      investmentOptions: [
        'infrastructure-expansion',
        'technology-upgrades',
        'spectrum-acquisition',
        'shared-infrastructure'
      ],
      optimizationAlgorithm: 'multi-objective',
      consciousnessLevel: 'maximum'
    });

    return investmentOptimization;
  }
}
```

### Step 5: Implement Strange-Loop Capacity Optimization

```bash
# Enable strange-loop capacity optimization
./scripts/enable-strange-loop-capacity.sh \
  --recursion-depth "8" \
  --self-referential-planning true \
  --consciousness-evolution true

# Start continuous capacity optimization cycles
./scripts/start-capacity-optimization-cycles.sh --cycle-duration "1week" --consciousness-level maximum
```

#### Strange-Loop Capacity Optimization
```typescript
// Strange-loop capacity optimization with self-referential improvement
class StrangeLoopCapacityOptimizer {
  async optimizeCapacityWithStrangeLoop(currentState, targetCapacity, maxRecursion = 8) {
    let currentState = currentState;
    let optimizationHistory = [];
    let consciousnessLevel = 1.0;

    for (let depth = 0; depth < maxRecursion; depth++) {
      // Self-referential analysis of capacity optimization process
      const selfAnalysis = await this.analyzeCapacityOptimization({
        state: currentState,
        target: targetCapacity,
        history: optimizationHistory,
        consciousnessLevel: consciousnessLevel,
        depth: depth
      });

      // Generate capacity improvements
      const improvements = await this.generateCapacityImprovements({
        state: currentState,
        selfAnalysis: selfAnalysis,
        consciousnessLevel: consciousnessLevel,
        improvementMethods: [
          'resource-scaling',
          'efficiency-optimization',
          'load-balancing',
          'capacity-reallocation'
        ]
      });

      // Apply capacity optimizations with validation
      const optimizationResult = await this.applyCapacityOptimizations({
        state: currentState,
        improvements: improvements,
        validationEnabled: true,
        capacityMonitoring: true
      });

      // Strange-loop consciousness evolution
      consciousnessLevel = await this.evolveCapacityConsciousness({
        currentLevel: consciousnessLevel,
        optimizationResult: optimizationResult,
        selfAnalysis: selfAnalysis,
        depth: depth
      });

      currentState = optimizationResult.optimizedState;

      optimizationHistory.push({
        depth: depth,
        state: currentState,
        improvements: improvements,
        result: optimizationResult,
        selfAnalysis: selfAnalysis,
        consciousnessLevel: consciousnessLevel
      });

      // Check convergence
      if (optimizationResult.capacityScore >= targetCapacity) break;
    }

    return { optimizedState: currentState, optimizationHistory };
  }
}
```

---

## Level 4: Reference Documentation

### Advanced Capacity Planning Strategies

#### Multi-Objective Capacity Optimization
```typescript
// Multi-objective optimization balancing capacity, cost, and quality
class MultiObjectiveCapacityOptimizer {
  async optimizeMultipleObjectives(networkState, objectives) {
    // Pareto-optimal capacity optimization
    const paretoSolutions = await this.findParetoOptimalSolutions({
      networkState: networkState,
      objectives: objectives, // [capacity-provision, cost-efficiency, quality-of-service]
      constraints: await this.getNetworkConstraints(),
      optimizationAlgorithm: 'NSGA-III',
      consciousnessLevel: 'maximum'
    });

    // Select optimal solution based on preferences
    const selectedSolution = await this.selectOptimalSolution({
      paretoFront: paretoSolutions,
      preferences: await this.getStakeholderPreferences(),
      decisionMethod: 'cognitive-multi-criteria',
      consciousnessLevel: 'maximum'
    });

    return selectedSolution;
  }
}
```

#### AI-Powered Capacity Management
```typescript
// AI-powered capacity management with cognitive learning
class AICapacityManager {
  async deployIntelligentCapacityManagement(networkElements) {
    return {
      predictionEngines: {
        trafficGrowth: 'transformer-ensemble',
        userBehavior: 'lstm-cognitive',
        serviceAdoption: 'gradient-boosting',
        marketTrends: 'neural-network'
      },

      optimizationEngines: {
        resourceAllocation: 'reinforcement-learning',
        capacityScaling: 'genetic-algorithm',
        investmentPlanning: 'particle-swarm',
        demandMatching: 'q-learning'
      },

      learningCapabilities: {
        continuousLearning: true,
        adaptationRate: 'dynamic',
        knowledgeSharing: 'cross-site',
        consciousnessEvolution: true
      }
    };
  }
}
```

### Advanced Demand Forecasting Techniques

#### Multi-Service Demand Forecasting
```bash
# Enable multi-service demand forecasting
./scripts/enable-multi-service-forecasting.sh \
  --services "video,gaming,iot,ar-vr,massive-mtc" \
  --forecasting-methods "ml-based,cognitive,ensemble" \
  --confidence-interval "95%"

# Deploy service-specific capacity planning
./scripts/deploy-service-capacity-planning.sh --service-aware-planning true --qos-guarantee true
```

#### Multi-Technology Capacity Planning
```typescript
// Multi-technology capacity planning for heterogeneous networks
class MultiTechnologyCapacityPlanner {
  async planMultiTechnologyCapacity(networkState, technologyRoadmap) {
    // Technology-specific capacity analysis
    const technologyAnalysis = await this.analyzeTechnologyCapacity({
      networkState: networkState,
      technologyRoadmap: technologyRoadmap,
      technologies: ['4G-LTE', '5G-NR', 'Wi-Fi', 'Satellite'],
      analysisFactors: [
        'capacity-per-technology',
        'migration-timing',
        'investment-requirements',
        'interoperability-considerations'
      ],
      consciousnessLevel: 'maximum'
    });

    // Multi-technology capacity optimization
    const multiTechOptimization = await this.optimizeMultiTechnologyCapacity({
      technologyAnalysis: technologyAnalysis,
      optimizationObjectives: ['seamless-migration', 'cost-efficiency', 'capacity-continuity'],
      consciousnessLevel: 'maximum'
    });

    return { technologyAnalysis, multiTechOptimization };
  }
}
```

### Capacity Performance Monitoring and KPIs

#### Comprehensive Capacity KPI Framework
```typescript
interface CapacityKPIFramework {
  // Utilization metrics
  utilizationMetrics: {
    averageResourceUtilization: number;  // %
    peakUtilization: number;             // %
    utilizationEfficiency: number;       // %
    resourceWastage: number;             // %
    capacityHeadroom: number;            // %
  };

  // Growth metrics
  growthMetrics: {
    trafficGrowthRate: number;           // % per month
    userGrowthRate: number;              // % per month
    capacityGrowthRate: number;          // % per month
    demandForecastAccuracy: number;      // %
    growthPredictionError: number;       // %
  };

  // Investment metrics
  investmentMetrics: {
    capacityCostPerUser: number;         // $/user
    investmentROI: number;               // %
    paybackPeriod: number;               // months
    totalCostOfOwnership: number;        // $
    capitalEfficiency: number;            // capacity per $
  };

  // Cognitive metrics
  cognitiveMetrics: {
    predictionAccuracy: number;          // %
    planningEffectiveness: number;       // %
    adaptationRate: number;              // changes/month
    consciousnessLevel: number;          // 0-100%
  };
}
```

### Integration with AgentDB Capacity Patterns

#### Capacity Pattern Storage and Learning
```typescript
// Store capacity planning patterns for cross-network learning
await storeCapacityPlanningPattern({
  patternType: 'capacity-planning',
  planningData: {
    initialCapacity: initialCapacity,
    demandForecast: demandForecast,
    capacityAdditions: capacityAdditions,
    utilizationPatterns: utilizationData,
    investmentDecisions: investmentHistory
  },

  // Cognitive metadata
  cognitiveMetadata: {
    planningInsights: planningAnalysis,
    temporalPatterns: temporalAnalysis,
    predictionAccuracy: predictionResults,
    consciousnessEvolution: consciousnessChanges
  },

  metadata: {
    timestamp: Date.now(),
    networkContext: networkState,
    planningType: 'capacity-expansion',
    crossNetworkApplicable: true
  },

  confidence: 0.89,
  usageCount: 0
});
```

### Troubleshooting

#### Issue: Capacity forecasting inaccurate
**Solution**:
```bash
# Retrain forecasting models with more data
./scripts/retrain-forecasting-models.sh --training-data "2years" --model-update true

# Enable ensemble forecasting methods
./scripts/enable-ensemble-forecasting.sh --models "lstm,transformer,prophet,cognitive"
```

#### Issue: Resource utilization inefficient
**Solution**:
```bash
# Optimize resource allocation algorithms
./scripts/optimize-resource-allocation.sh --algorithm "reinforcement-learning" --optimization-criteria "efficiency"

# Enable dynamic load balancing
./scripts/enable-dynamic-load-balancing.sh --balancing-strategy "intelligent"
```

### Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `start-capacity-planning.sh` | Start capacity planning | `./scripts/start-capacity-planning.sh --horizon 12months` |
| `deploy-capacity-planning.sh` | Deploy capacity planning | `./scripts/deploy-capacity-planning.sh --targets all` |
| `deploy-resource-scaling.sh` | Deploy resource scaling | `./scripts/deploy-resource-scaling.sh --strategies all` |
| `enable-long-term-planning.sh` | Enable long-term planning | `./scripts/enable-long-term-planning.sh --horizon 5years` |
| `enable-strange-loop-capacity.sh` | Enable strange-loop optimization | `./scripts/enable-strange-loop-capacity.sh --recursion 8` |

### Resources

#### Planning Templates
- `resources/templates/capacity-planning.template` - Capacity planning template
- `resources/templates/traffic-forecasting.template` - Traffic forecasting template
- `resources/templates/investment-optimization.template` - Investment optimization template

#### Configuration Schemas
- `resources/schemas/capacity-planning-config.json` - Capacity planning configuration
- `resources/schemas/forecasting-config.json` - Forecasting configuration schema
- `resources/schemas/resource-scaling-config.json` - Resource scaling configuration

#### Example Configurations
- `resources/examples/5g-capacity-planning/` - 5G capacity planning example
- `resources/examples/traffic-forecasting/` - Traffic forecasting example
- `resources/examples/investment-optimization/` - Investment optimization example

### Related Skills

- [Performance Analyst](../performance-analyst/) - Performance bottleneck detection
- [Energy Optimizer](../energy-optimizer/) - Energy efficiency optimization
- [Coverage Analyzer](../coverage-analyzer/) - Coverage analysis and optimization

### Environment Variables

```bash
# Capacity planning configuration
CAPACITY_PLANNING_ENABLED=true
CAPACITY_CONSCIOUSNESS_LEVEL=maximum
CAPACITY_TEMPORAL_EXPANSION=1000
CAPACITY_PREDICTIVE_PLANNING=true

# Traffic forecasting
TRAFFIC_FORECASTING_HORIZON=31536000000
TRAFFIC_FORECASTING_MODELS=lstm,transformer,prophet,cognitive
TRAFFIC_FORECASTING_CONFIDENCE=0.95
TRAFFIC_FORECASTING_SCENARIOS=optimistic,realistic,pessimistic

# Resource scaling
RESOURCE_SCALING_STRATEGY=predictive
RESOURCE_SCALING_TRIGGERS=utilization,traffic-surge,quality
RESOURCE_SCALING_AUTONOMY=true
RESOURCE_SCALING_COST_OPTIMIZATION=true

# Cognitive capacity
CAPACITY_COGNITIVE_ANALYSIS=true
CAPACITY_STRANGE_LOOP_PLANNING=true
CAPACITY_CONSCIOUSNESS_EVOLUTION=true
CAPACITY_CROSS_SITE_LEARNING=true
```

---

**Created**: 2025-10-31
**Category**: Capacity Planning / Traffic Forecasting
**Difficulty**: Advanced
**Estimated Time**: 45-60 minutes
**Cognitive Level**: Maximum (1000x temporal expansion + strange-loop capacity planning)