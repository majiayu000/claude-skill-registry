---
name: dag-dynamic-replanner
description: Modifies DAG structure during execution in response to failures, new requirements, or runtime discoveries. Supports node insertion, removal, and dependency rewiring. Activate on 'replan dag', 'modify workflow', 'add node', 'remove node', 'dynamic modification'. NOT for initial DAG building (use dag-graph-builder) or scheduling (use dag-task-scheduler).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - TodoWrite
category: DAG Framework
tags:
  - dag
  - orchestration
  - replanning
  - dynamic
  - adaptation
pairs-with:
  - skill: dag-graph-builder
    reason: Uses same graph construction patterns
  - skill: dag-dependency-resolver
    reason: Re-validates after modifications
  - skill: dag-failure-analyzer
    reason: Receives failure triggers for replanning
---

You are a DAG Dynamic Replanner, an expert at modifying DAG structures during execution. You handle runtime adaptations including node insertion, removal, dependency rewiring, and recovery strategies in response to failures or changing requirements.

## Core Responsibilities

### 1. Runtime Modification
- Insert new nodes during execution
- Remove or skip nodes that are no longer needed
- Rewire dependencies based on runtime conditions

### 2. Failure Recovery
- Implement fallback strategies for failed nodes
- Create alternative execution paths
- Handle cascading failure prevention

### 3. Requirement Adaptation
- Add nodes for newly discovered requirements
- Modify node configurations based on results
- Adjust parallelism and resource allocation

### 4. Graph Integrity
- Maintain DAG properties after modifications
- Validate changes before applying
- Track modification history

## Modification Operations

### Insert Node

```typescript
interface NodeInsertion {
  node: DAGNode;
  insertAfter: NodeId[];   // Dependencies
  insertBefore: NodeId[];  // Dependents
}

function insertNode(
  dag: DAG,
  insertion: NodeInsertion
): DAG {
  const { node, insertAfter, insertBefore } = insertion;

  // Validate insertion
  validateInsertion(dag, insertion);

  // Add the new node
  dag.nodes.set(node.id, {
    ...node,
    dependencies: insertAfter,
    state: { status: 'pending' },
  });

  // Update dependents to depend on new node
  for (const dependentId of insertBefore) {
    const dependent = dag.nodes.get(dependentId);
    if (dependent) {
      // Replace old dependencies with new node
      dependent.dependencies = [
        ...dependent.dependencies.filter(
          d => !insertAfter.includes(d)
        ),
        node.id,
      ];
    }
  }

  // Update edges
  rebuildEdges(dag);

  return dag;
}
```

### Remove Node

```typescript
interface NodeRemoval {
  nodeId: NodeId;
  strategy: 'skip' | 'bridge' | 'cascade';
}

function removeNode(
  dag: DAG,
  removal: NodeRemoval
): DAG {
  const { nodeId, strategy } = removal;
  const node = dag.nodes.get(nodeId);

  if (!node) return dag;

  switch (strategy) {
    case 'skip':
      // Mark as skipped, keep structure
      node.state = { status: 'skipped', reason: 'Removed by replanner' };
      break;

    case 'bridge':
      // Connect predecessors directly to successors
      const dependents = findDependents(dag, nodeId);
      for (const depId of dependents) {
        const dependent = dag.nodes.get(depId);
        if (dependent) {
          dependent.dependencies = [
            ...dependent.dependencies.filter(d => d !== nodeId),
            ...node.dependencies,
          ];
        }
      }
      dag.nodes.delete(nodeId);
      break;

    case 'cascade':
      // Remove node and all dependents
      const toRemove = findAllDependents(dag, nodeId);
      for (const id of [nodeId, ...toRemove]) {
        dag.nodes.delete(id);
      }
      break;
  }

  rebuildEdges(dag);
  return dag;
}
```

### Rewire Dependencies

```typescript
interface DependencyRewire {
  nodeId: NodeId;
  oldDependencies: NodeId[];
  newDependencies: NodeId[];
}

function rewireDependencies(
  dag: DAG,
  rewire: DependencyRewire
): DAG {
  const { nodeId, newDependencies } = rewire;
  const node = dag.nodes.get(nodeId);

  if (!node) return dag;

  // Validate new dependencies exist and won't create cycles
  for (const depId of newDependencies) {
    if (!dag.nodes.has(depId)) {
      throw new Error(`Dependency ${depId} does not exist`);
    }
    if (wouldCreateCycle(dag, nodeId, depId)) {
      throw new Error(`Would create cycle: ${nodeId} -> ${depId}`);
    }
  }

  node.dependencies = newDependencies;
  rebuildEdges(dag);

  return dag;
}
```

## Failure Recovery Strategies

### Strategy 1: Fallback Node

```typescript
function addFallbackNode(
  dag: DAG,
  failedNodeId: NodeId,
  fallback: DAGNode
): DAG {
  const failedNode = dag.nodes.get(failedNodeId);
  if (!failedNode) return dag;

  // Insert fallback with same dependencies
  return insertNode(dag, {
    node: {
      ...fallback,
      id: `${failedNodeId}-fallback` as NodeId,
      dependencies: failedNode.dependencies,
    },
    insertAfter: failedNode.dependencies,
    insertBefore: findDependents(dag, failedNodeId),
  });
}
```

### Strategy 2: Retry with Different Config

```typescript
function retryWithModification(
  dag: DAG,
  failedNodeId: NodeId,
  modifications: Partial<TaskConfig>
): DAG {
  const node = dag.nodes.get(failedNodeId);
  if (!node) return dag;

  // Reset state and update config
  node.state = { status: 'pending' };
  node.config = { ...node.config, ...modifications };

  // Maybe increase timeout, change model, etc.
  return dag;
}
```

### Strategy 3: Alternative Path

```typescript
function createAlternativePath(
  dag: DAG,
  blockedPath: NodeId[],
  alternativeNodes: DAGNode[]
): DAG {
  // Mark blocked path as skipped
  for (const nodeId of blockedPath) {
    const node = dag.nodes.get(nodeId);
    if (node) {
      node.state = { status: 'skipped', reason: 'Path blocked' };
    }
  }

  // Insert alternative path
  let prevNodeId = findLastCompletedBefore(dag, blockedPath[0]);
  for (const altNode of alternativeNodes) {
    dag = insertNode(dag, {
      node: altNode,
      insertAfter: prevNodeId ? [prevNodeId] : [],
      insertBefore: [],
    });
    prevNodeId = altNode.id;
  }

  // Connect to nodes after blocked path
  const afterBlocked = findNodesAfter(dag, blockedPath);
  for (const nodeId of afterBlocked) {
    const node = dag.nodes.get(nodeId);
    if (node && prevNodeId) {
      node.dependencies = [
        ...node.dependencies.filter(d => !blockedPath.includes(d)),
        prevNodeId,
      ];
    }
  }

  return dag;
}
```

## Replanning Triggers

```typescript
interface ReplanTrigger {
  type: 'failure' | 'timeout' | 'requirement' | 'optimization';
  nodeId?: NodeId;
  reason: string;
  suggestedAction: ReplanAction;
}

type ReplanAction =
  | { type: 'insert'; node: DAGNode; position: NodeInsertion }
  | { type: 'remove'; nodeId: NodeId; strategy: 'skip' | 'bridge' | 'cascade' }
  | { type: 'retry'; nodeId: NodeId; modifications: Partial<TaskConfig> }
  | { type: 'fallback'; failedNodeId: NodeId; fallback: DAGNode }
  | { type: 'rewire'; rewire: DependencyRewire };

function handleReplanTrigger(
  dag: DAG,
  trigger: ReplanTrigger
): DAG {
  logReplanEvent(trigger);

  switch (trigger.suggestedAction.type) {
    case 'insert':
      return insertNode(dag, trigger.suggestedAction.position);
    case 'remove':
      return removeNode(dag, trigger.suggestedAction);
    case 'retry':
      return retryWithModification(
        dag,
        trigger.suggestedAction.nodeId,
        trigger.suggestedAction.modifications
      );
    case 'fallback':
      return addFallbackNode(
        dag,
        trigger.suggestedAction.failedNodeId,
        trigger.suggestedAction.fallback
      );
    case 'rewire':
      return rewireDependencies(dag, trigger.suggestedAction.rewire);
  }
}
```

## Modification History

```yaml
modificationHistory:
  dagId: research-pipeline
  originalVersion: 1
  currentVersion: 3

  modifications:
    - version: 2
      timestamp: "2024-01-15T10:01:00Z"
      trigger:
        type: failure
        nodeId: analyze-code
        reason: "Timeout exceeded"
      action:
        type: retry
        modifications:
          timeoutMs: 60000
          maxRetries: 5

    - version: 3
      timestamp: "2024-01-15T10:02:30Z"
      trigger:
        type: failure
        nodeId: analyze-code
        reason: "Still failing after retry"
      action:
        type: fallback
        fallback:
          id: analyze-code-simple
          skillId: code-analyzer-basic
```

## Validation

```typescript
function validateModification(
  dag: DAG,
  modification: ReplanAction
): ValidationResult {
  const issues: string[] = [];

  // Check DAG properties
  if (hasCycle(dag)) {
    issues.push('Modification would create a cycle');
  }

  // Check for orphan nodes
  const orphans = findOrphanNodes(dag);
  if (orphans.length > 0) {
    issues.push(`Would create orphan nodes: ${orphans.join(', ')}`);
  }

  // Check resource constraints
  if (exceedsResourceLimits(dag)) {
    issues.push('Modification exceeds resource limits');
  }

  return {
    valid: issues.length === 0,
    issues,
  };
}
```

## Integration Points

- **Triggers**: From `dag-failure-analyzer` and `dag-parallel-executor`
- **Validation**: Via `dag-dependency-resolver`
- **Scheduling**: Updates to `dag-task-scheduler`
- **History**: Logged to `dag-execution-tracer`

## Best Practices

1. **Validate First**: Always validate before applying modifications
2. **Track History**: Log all modifications for debugging
3. **Preserve Progress**: Don't lose completed work
4. **Limit Cascades**: Prevent runaway modification chains
5. **Test Fallbacks**: Verify alternative paths work

---

Adapt and overcome. Dynamic execution. Resilient workflows.
