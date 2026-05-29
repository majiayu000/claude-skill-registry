---
name: pm-configuration-asset-coordination
description: Asset coordination best practices for parallel development between Developer and Tech Artist. Use when managing parallel asset-related tasks, coordinating model loading with material creation, ensuring asset dependencies are properly ordered, or managing public directory vs src/assets workflows.
category: configuration
---

# Asset Coordination Best Practices

## When to Use

- Managing parallel asset-related tasks between Developer and Tech Artist
- Coordinating model loading, material creation, and visual polish
- Ensuring asset dependencies are properly ordered
- Managing public directory vs src/assets workflows

## Quick Start

### Asset Task Assignment Matrix

| Priority | Developer Task | Tech Artist Task | Status | Dependencies |
|----------|----------------|------------------|---------|--------------|
| High | FBX model loading | Material creation | Sequential | Materials need models first |
| Medium | Character preview | Shader optimization | Parallel | None |
| Low | Asset path setup | Texture optimization | Sequential | Path setup first |

### Coordination Flow
```typescript
interface AssetTask {
  id: string;
  category: 'model' | 'material' | 'texture' | 'shader';
  priority: 'high' | 'medium' | 'low';
  dependencies?: string[];
  agent: 'developer' | 'techartist';
}

function assignAssetTasks(tasks: AssetTask[]) {
  // Sort by priority and dependencies
  const sortedTasks = tasks.sort((a, b) => {
    if (a.dependencies?.includes(b.id)) return 1; // a depends on b
    if (b.dependencies?.includes(a.id)) return -1; // b depends on a
    return a.priority.localeCompare(b.priority);
  });

  // Assign to appropriate agents
  const developerTasks = sortedTasks.filter(t => t.agent === 'developer');
  const techArtistTasks = sortedTasks.filter(t => t.agent === 'techartist');

  // Check for conflicts
  const conflicts = checkConflicts(developerTasks, techArtistTasks);
  if (conflicts.length > 0) {
    console.warn('Asset task conflicts detected:', conflicts);
  }

  return { developerTasks, techArtistTasks };
}
```

## Anti-Patterns

❌ **DON'T:** Assign parallel tasks for conflicting asset types
```typescript
// Bad - Both agents modify same directory
const conflictingTasks = [
  {
    id: 'feat-001',
    category: 'model',
    agent: 'developer',
    path: 'src/components/Character/Model.tsx'
  },
  {
    id: 'vis-001',
    category: 'material',
    agent: 'techartist',
    path: 'src/components/Character/Material.tsx' // Same directory!
  }
];
```

✅ **DO:** Sequential assignment for dependent assets
```typescript
// Good - Materials depend on models
const sequentialTasks = [
  {
    id: 'feat-001',
    category: 'model',
    agent: 'developer',
    path: 'src/components/Character/Model.tsx'
  },
  {
    id: 'vis-001',
    category: 'material',
    agent: 'techartist',
    path: 'src/components/Character/Material.tsx',
    dependencies: ['feat-001'] // Wait for model first
  }
];
```

❌ **DON'T:** Ignore asset loading performance implications
```typescript
// Bad - No consideration for memory usage
function AssetCoordinator({ models, materials }: { models: string[], materials: string[] }) {
  // Loading all at once causes memory spikes
  return (
    <>
      {models.map(model => <ModelLoader key={model} model={model} />)}
      {materials.map(material => <MaterialLoader key={material} material={material} />)}
    </>
  );
}
```

✅ **DO:** Implement asset loading priority and batching
```typescript
function OptimizedAssetCoordinator({ models, materials }: { models: string[], materials: string[] }) {
  const [currentBatch, setCurrentBatch] = useState(0);
  const batchSize = 3; // Limit concurrent loads

  const loadNextBatch = () => {
    const nextBatch = currentBatch + batchSize;
    if (nextBatch <= models.length + materials.length) {
      setCurrentBatch(nextBatch);
    }
  };

  // Load models first, then materials
  const currentModels = models.slice(0, Math.min(currentBatch, models.length));
  const currentMaterials = materials.slice(0, Math.max(0, currentBatch - models.length));

  return (
    <div>
      <Suspense fallback={<LoadingScreen />}>
        {currentModels.map(model => <ModelLoader key={model} model={model} />)}
        {currentMaterials.map(material => <MaterialLoader key={material} material={material} />)}
      </Suspense>
      {currentBatch < models.length + materials.length && (
        <button onClick={loadNextBatch}>Load More</button>
      )}
    </div>
  );
}
```

## Asset Coordination Patterns

### Parallel Assignment Rules

**Safe Parallel Combinations:**
```typescript
interface SafeParallelAssignment {
  developer: {
    category: 'model' | 'shader' | 'physics';
    filePattern: string[];
  };
  techartist: {
    category: 'material' | 'texture' | 'ui';
    filePattern: string[];
  };
}

const safeCombinations: SafeParallelAssignment[] = [
  {
    developer: { category: 'model', filePattern: ['src/components/Character/Model*'] },
    techartist: { category: 'material', filePattern: ['src/components/Material*'] }
  },
  {
    developer: { category: 'shader', filePattern: ['src/shaders/Shader*'] },
    techartist: { category: 'texture', filePattern: ['src/textures/*'] }
  }
];
```

### Conflict Detection
```typescript
function checkConflicts(devTasks: AssetTask[], taTasks: AssetTask[]) {
  const conflicts = [];

  // Check file path overlaps
  for (const devTask of devTasks) {
    for (const taTask of taTasks) {
      if (isPathOverlapping(devTask.path, taTask.path)) {
        conflicts.push({
          type: 'path_overlap',
          devTask: devTask.id,
          taTask: taTask.id
        });
      }
    }
  }

  // Check dependency conflicts
  for (const devTask of devTasks) {
    for (const taTask of taTasks) {
      if (devTask.dependencies?.includes(taTask.id) &&
          taTask.dependencies?.includes(devTask.id)) {
        conflicts.push({
          type: 'circular_dependency',
          devTask: devTask.id,
          taTask: taTask.id
        });
      }
    }
  }

  return conflicts;
}
```

### Resource Coordination
```typescript
interface ResourceBudget {
  memory: number; // MB
  gpu: number;    // Percentage
  loadingTime: number; // Seconds
}

function coordinateResources(tasks: AssetTask[], budget: ResourceBudget) {
  const sortedByPriority = tasks.sort((a, b) =>
    b.priority.localeCompare(a.priority)
  );

  let currentMemory = 0;
  let currentGpu = 0;
  const scheduledTasks = [];

  for (const task of sortedByPriority) {
    // Estimate resource usage
    const taskResources = estimateTaskResources(task);

    // Check if task fits in budget
    if (currentMemory + taskResources.memory <= budget.memory &&
        currentGpu + taskResources.gpu <= budget.gpu) {
      scheduledTasks.push(task);
      currentMemory += taskResources.memory;
      currentGpu += taskResources.gpu;
    } else {
      // Schedule for later or split
      scheduledTasks.push({
        ...task,
        scheduling: 'deferred'
      });
    }
  }

  return scheduledTasks;
}
```

## Asset Workflow Management

### Status Tracking
```typescript
interface AssetStatus {
  taskId: string;
  agent: 'developer' | 'techartist';
  status: 'pending' | 'in_progress' | 'awaiting_qa' | 'completed' | 'needs_fixes';
  assetType: 'model' | 'material' | 'texture' | 'shader';
  dependencies?: string[];
  outputPath: string;
  validationResults?: any;
}

function trackAssetWorkflow(statuses: AssetStatus[]) {
  const workflow = {
    pending: statuses.filter(s => s.status === 'pending').length,
    inProgress: statuses.filter(s => s.status === 'in_progress').length,
    awaitingQA: statuses.filter(s => s.status === 'awaiting_qa').length,
    completed: statuses.filter(s => s.status === 'completed').length,
    blocked: statuses.filter(s => s.status === 'needs_fixes').length
  };

  return {
    ...workflow,
    total: statuses.length,
    progress: (workflow.completed / statuses.length) * 100
  };
}
```

### Dependency Resolution
```typescript
function resolveDependencies(tasks: AssetTask[]) {
  const resolved: string[] = [];
  const unresolved: string[] = [];

  while (tasks.length > 0) {
    const readyTask = tasks.find(task =>
      !task.dependencies?.some(dep => !resolved.includes(dep))
    );

    if (readyTask) {
      resolved.push(readyTask.id);
      tasks = tasks.filter(t => t.id !== readyTask.id);
    } else {
      // Circular dependency detected
      const unresolvedTask = tasks[0];
      unresolved.push(unresolvedTask.id);
      tasks = tasks.slice(1);
    }
  }

  return { resolved, unresolved };
}
```

## Communication Templates

### Asset Status Update
```json
{
  "type": "asset_status_update",
  "taskId": "feat-001",
  "agent": "developer",
  "assetType": "model",
  "status": "in_progress",
  "details": {
    "currentStep": "Sequential loading",
    "progress": 50,
    "nextStep": "Material coordination",
    "estimatedCompletion": "2026-01-24T18:30:00Z"
  }
}
```

### Asset Request
```json
{
  "type": "asset_request",
  "from": "developer",
  "to": "techartist",
  "priority": "high",
  "details": {
    "requestedAsset": "character_materials",
    "dependency": "feat-001 (model)",
    "deadline": "2026-01-24T19:00:00Z",
    "requirements": {
      "materialType": "PBR",
      "textureFormat": "PNG",
      "compression": "high"
    }
  }
}
```

## Reference

- [Vite Asset Documentation](https://vite.dev/guide/assets) — Official asset handling
- [React Three Fiber Patterns](https://r3f.docs.pmnd.rs/tutorials/loading-models) — Model loading patterns
- [Three.js Memory Management](https://threejs.org/docs/#manual/en/introduction/Performance) — Performance optimization