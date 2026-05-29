---
name: pm-improvement-asset-coordination
description: PM self-improvement skill for asset coordination learnings from completed tasks. Use after tasks involving asset loading coordination, when parallel development between Developer and Tech Artist causes conflicts, or when Vite 6 asset handling patterns need to be documented.
category: improvement
---

# PM Asset Coordination Improvement

## When to Use

- After tasks involving asset loading coordination
- When parallel development between Developer and Tech Artist causes conflicts
- When Vite 6 asset handling patterns are needed
- When sequential vs parallel task assignment decisions are required

## Quick Start

### Post-Task Asset Coordination Analysis
```typescript
interface AssetTaskResult {
  taskId: string;
  agent: 'developer' | 'techartist';
  assetType: 'model' | 'material' | 'texture' | 'shader';
  coordinationIssues: string[];
  performanceMetrics: {
    loadTime: number;
    memoryUsage: number;
    errors: string[];
  };
}

function analyzeAssetCoordination(results: AssetTaskResult[]) {
  const developerTasks = results.filter(r => r.agent === 'developer');
  const techArtistTasks = results.filter(r => r.agent === 'techartist');

  // Check for coordination issues
  const coordinationIssues = [];

  if (developerTasks.length > 0 && techArtistTasks.length > 0) {
    // Check for parallel execution issues
    const overlappingPaths = checkPathOverlaps(developerTasks, techArtistTasks);
    if (overlappingPaths.length > 0) {
      coordinationIssues.push('Path overlaps detected between Developer and Tech Artist tasks');
    }

    // Check for dependency mismatches
    const dependencyIssues = checkDependencyConflicts(developerTasks, techArtistTasks);
    if (dependencyIssues.length > 0) {
      coordinationIssues.push('Dependency conflicts found');
    }
  }

  // Performance analysis
  const avgLoadTime = developerTasks.reduce((sum, task) =>
    sum + task.performanceMetrics.loadTime, 0) / developerTasks.length || 0;

  const totalMemoryUsage = developerTasks.reduce((sum, task) =>
    sum + task.performanceMetrics.memoryUsage, 0);

  return {
    coordinationIssues,
    performance: {
      avgLoadTime,
      totalMemoryUsage,
      errorCount: developerTasks.reduce((sum, task) =>
        sum + task.performanceMetrics.errors.length, 0)
    },
    recommendations: generateRecommendations(coordinationIssues, results)
  };
}
```

### Decision Tree for Task Assignment
```typescript
function assignAssetTask(task: AssetTask): { agent: string; execution: 'parallel' | 'sequential' } {
  const { category, dependencies } = task;

  // Model loading should be sequential for memory management
  if (category === 'model') {
    return {
      agent: 'developer',
      execution: 'sequential'
    };
  }

  // Materials can be parallel if models exist
  if (category === 'material' && !dependencies?.some(d => d.category === 'model')) {
    return {
      agent: 'techartist',
      execution: 'parallel'
    };
  }

  // Textures can be parallel
  if (category === 'texture') {
    return {
      agent: 'techartist',
      execution: 'parallel'
    };
  }

  // Shaders may need sequential compilation
  if (category === 'shader') {
    return {
      agent: 'techartist',
      execution: 'sequential'
    };
  }

  // Default to developer for architectural assets
  return {
    agent: 'developer',
    execution: 'sequential'
  };
}
```

## Anti-Patterns

❌ **DON'T:** Assign asset tasks without considering Vite 6 behavior
```typescript
// Bad - Ignores Vite 6 asset handling changes
function badTaskAssignment() {
  const modelTask = {
    category: 'model',
    path: '/assets/character.fbx' // This would create '?import' query
  };

  // No consideration for public vs src/assets
  return assignTasks([modelTask]);
}
```

✅ **DO:** Account for Vite 6 asset handling differences
```typescript
// Good - Considers Vite 6 behavior
function goodTaskAssignment() {
  const modelTask = {
    category: 'model',
    path: '/public/assets/character.fbx', // Public directory
    assetStrategy: 'public-absolute', // Specify strategy
    expectedLoadTime: 5000, // Based on past performance
    memoryEstimate: 20 * 1024 * 1024 // 20MB
  };

  const materialTask = {
    category: 'material',
    path: 'src/assets/materials/', // Source assets for processing
    assetStrategy: 'src-import',
    dependencies: ['modelTask'] // Wait for model first
  };

  return assignTasks([modelTask, materialTask]);
}
```

❌ **DON'T:** Ignore memory implications of sequential loading
```typescript
// Bad - No memory management consideration
function sequentialLoadingWithoutMemoryCheck() {
  const largeModels = ['character1.fbx', 'character2.fbx', 'character3.fbx'];

  // Loading all sequentially but no memory tracking
  return largeModels.map(model => ({
    type: 'model',
    model,
    load: true // No memory limit
  }));
}
```

✅ **DO:** Implement memory-aware sequential loading
```typescript
// Good - Memory-conscious loading
function memoryAwareSequentialLoading(models: string[], memoryBudget: number) {
  const loadedModels = [];
  let currentMemoryUsage = 0;

  for (const model of models) {
    const estimatedMemory = estimateModelMemory(model);

    if (currentMemoryUsage + estimatedMemory <= memoryBudget) {
      loadedModels.push({
        type: 'model',
        model,
        load: true,
        memoryUsage: estimatedMemory
      });
      currentMemoryUsage += estimatedMemory;
    } else {
      loadedModels.push({
        type: 'model',
        model,
        load: false,
        reason: 'Memory budget exceeded',
        deferred: true
      });
    }
  }

  return loadedModels;
}
```

## Coordination Patterns

### Parallel Assignment Validation
```typescript
function validateParallelAssignment(devTasks: AssetTask[], taTasks: AssetTask[]): boolean {
  // Check for file path conflicts
  const pathConflicts = devTasks.some(devTask =>
    taTasks.some(taTask =>
      isPathOverlapping(devTask.path, taTask.path)
    )
  );

  // Check for resource conflicts
  const resourceConflicts = devTasks.some(devTask =>
    taTasks.some(taTask =>
      Math.abs(devTask.priority - taTask.priority) <= 1 &&
      isSameResourceType(devTask.category, taTask.category)
    )
  );

  // Check for timing conflicts
  const timingConflicts = devTasks.some(devTask =>
    taTasks.some(taTask =>
      isTimeOverlapping(devTask.schedule, taTask.schedule)
    )
  );

  return !pathConflicts && !resourceConflicts && !timingConflicts;
}
```

### Asset Performance Monitoring
```typescript
interface AssetPerformanceMetrics {
  taskId: string;
  loadTime: number;
  memoryUsage: number;
  errorRate: number;
  successCriteria: string[];
}

function trackAssetPerformance(metrics: AssetPerformanceMetrics[]) {
  const trends = {
    loadTime: calculateTrend(metrics.map(m => m.loadTime)),
    memoryUsage: calculateTrend(metrics.map(m => m.memoryUsage)),
    errorRate: calculateTrend(metrics.map(m => m.errorRate))
  };

  const recommendations = [];

  if (trends.loadTime > 0) {
    recommendations.push('Consider optimizing asset loading or implementing progressive loading');
  }

  if (trends.memoryUsage > 0) {
    recommendations.push('Memory usage increasing - consider asset compression or deferred loading');
  }

  if (trends.errorRate > 0) {
    recommendations.push('Error rate increasing - implement better error handling and retry mechanisms');
  }

  return {
    trends,
    recommendations,
    nextSteps: determineNextSteps(trends, recommendations)
  };
}
```

### Post-Retrospective Improvement Process
```typescript
function postRetrospectiveAssetImprovement(results: AssetTaskResult[]) {
  // 1. Analyze coordination issues
  const analysis = analyzeAssetCoordination(results);

  // 2. Generate specific improvements
  const improvements = {
    taskAssignment: improveTaskAssignment(analysis),
    resourceManagement: improveResourceManagement(analysis),
    errorHandling: improveErrorHandling(analysis),
    performance: improvePerformance(analysis)
  };

  // 3. Update agent skills
  updateAgentSkills(improvements);

  // 4. Document learnings
  documentLearnings(results, improvements);

  // 5. Plan next iteration improvements
  planNextIteration(improvements);

  return improvements;
}
```

## Decision Framework Matrix

| Scenario | Developer Action | Tech Artist Action | Coordination Strategy |
|----------|------------------|-------------------|----------------------|
| Model + Material needed | Sequential loading | Material preparation | Sequential: Model first, then material |
| Multiple models | Sequential with memory tracking | Texture preparation | Sequential with budget limits |
| UI Assets + Models | UI asset parallel | Model sequential | Parallel UI, sequential models |
| Shader + Texture | Shader compilation first | Texture optimization | Sequential: Shader depends on textures |

## Quality Assurance Metrics

### Asset Loading Success Rate
```typescript
interface AssetQualityMetrics {
  totalTasks: number;
  successfulLoads: number;
  averageLoadTime: number;
  memoryEfficiency: number;
  errorFreeRate: number;
}

function calculateAssetQuality(metrics: AssetQualityMetrics) {
  const qualityScore = {
    loading: (metrics.successfulLoads / metrics.totalTasks) * 40,
    performance: Math.max(0, 100 - metrics.averageLoadTime / 1000) * 30, // 30% weight
    memory: Math.min(100, metrics.memoryEfficiency) * 20, // 20% weight
    reliability: metrics.errorFreeRate * 10 // 10% weight
  };

  const totalScore = Object.values(qualityScore).reduce((sum, score) => sum + score, 0);

  return {
    score: totalScore,
    breakdown: qualityScore,
    rating: totalScore > 80 ? 'Excellent' : totalScore > 60 ? 'Good' : 'Needs Improvement'
  };
}
```

## Reference

- [Vite Asset Handling Documentation](https://vite.dev/guide/assets) — Official Vite asset documentation
- [React Three Fiber Model Loading](https://r3f.docs.pmnd.rs/tutorials/loading-models) — R3F loading patterns
- [Three.js Performance Optimization](https://threejs.org/docs/#manual/en/introduction/Performance) — Performance best practices
- [BMAD Methodology](https://github.com/bmad-code-org/BMAD-METHOD) — Scale-adaptive agent coordination