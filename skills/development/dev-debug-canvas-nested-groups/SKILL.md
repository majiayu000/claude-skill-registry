---
name: dev-debug-canvas-nested-groups
description: This skill should be used when debugging Vue Flow canvas issues involving nested nodes, parent-child relationships, position coordinate systems, and containment detection. Triggers on nested group problems, section nodes jumping, parent-child synchronization bugs, position persistence issues, and coordinate transformation errors in Vue Flow implementations.
---

# Vue Flow Nested Nodes Debugging Skill

## Overview

Debug Vue Flow nested nodes, parent-child relationships, position coordinate systems, and containment detection issues. This skill provides systematic diagnostic procedures, code patterns, and utilities for troubleshooting complex canvas hierarchy problems.

## When to Use This Skill

Use this skill when encountering:
- Nested groups not moving together when parent is dragged
- Section nodes jumping to unexpected positions
- Parent-child relationships not being recognized
- Tasks inside groups not being detected correctly
- Position values appearing incorrect after operations
- Groups resetting or losing their nested structure
- Coordinate mismatches between UI and stored data

## Quick Diagnostic

Before deep debugging, run these quick checks:

```typescript
// 1. Check if parentNode is properly set
const node = getNode('task-123')
console.log('Parent:', node?.parentNode) // Should be group ID or undefined

// 2. Verify coordinate types
console.log('Position (relative):', node?.position)
console.log('ComputedPosition (absolute):', node?.computedPosition)

// 3. Check extent mode
console.log('Extent:', node?.extent) // 'parent' for constrained children
```

## Core Concept: Coordinate Systems

**CRITICAL**: Vue Flow uses TWO coordinate systems that must not be confused:

| Property | Type | When Used |
|----------|------|-----------|
| `node.position` | Relative to parent | Child nodes with `parentNode` set |
| `node.position` | Absolute canvas coords | Root nodes (no parent) |
| `node.computedPosition` | Always absolute | Use for canvas operations |

**Golden Rule**: Store relative positions for children, use `computedPosition` for calculations.

## Debugging Workflow

### Step 1: Identify the Problem Type

Consult the troubleshooting tree in `references/troubleshooting-tree.md`:

- **Position Issues**: Node jumping, incorrect placement, reset positions
- **Hierarchy Issues**: Parent-child not recognized, nesting lost
- **Movement Issues**: Children not moving with parent, group drag problems
- **Containment Issues**: Tasks not detected inside groups

### Step 2: Enable Debug Logging

Add targeted logging based on problem type:

```typescript
// For position debugging
watch(() => node.position, (newPos, oldPos) => {
  console.log(`[POSITION] ${node.id}: ${JSON.stringify(oldPos)} → ${JSON.stringify(newPos)}`)
}, { deep: true })

// For hierarchy debugging
watch(() => node.parentNode, (newParent, oldParent) => {
  console.log(`[HIERARCHY] ${node.id}: parent ${oldParent} → ${newParent}`)
})
```

### Step 3: Use Diagnostic Utilities

Load the debugging utilities from `scripts/vueFlowDebug.ts`:

```typescript
import { logNodeHierarchy, validateParentChild, dumpCanvasState } from './vueFlowDebug'

// Dump full canvas state
dumpCanvasState(getNodes.value, getEdges.value)

// Validate all parent-child relationships
validateParentChild(getNodes.value)

// Log hierarchy tree
logNodeHierarchy(getNodes.value)
```

### Step 4: Apply Fix Patterns

Consult `references/code-patterns.md` for proven solutions:

- **Reparenting**: Correct way to move node between parents
- **Position Conversion**: Converting between coordinate systems
- **Containment Detection**: Proper center-point-in-bounds check

## Common Bugs and Solutions

### Bug 1: Child Not Moving with Parent

**Symptom**: Dragging parent leaves children behind

**Cause**: `parentNode` property not set or position stored as absolute

**Fix**:
```typescript
// Ensure parentNode is set
updateNode(childId, { parentNode: parentId })

// Convert to relative position
const parent = getNode(parentId)
const relativePos = {
  x: child.computedPosition.x - parent.computedPosition.x,
  y: child.computedPosition.y - parent.computedPosition.y
}
updateNode(childId, { position: relativePos })
```

### Bug 2: Node Jumping When Set as Child

**Symptom**: Node teleports when assigned parent

**Cause**: Absolute position interpreted as relative after parent set

**Fix**: Convert position BEFORE setting parentNode:
```typescript
const parent = getNode(parentId)
const child = getNode(childId)

// Step 1: Calculate relative position first
const relativePos = {
  x: child.computedPosition.x - parent.computedPosition.x,
  y: child.computedPosition.y - parent.computedPosition.y
}

// Step 2: Update both in same call
updateNode(childId, {
  parentNode: parentId,
  position: relativePos
})
```

### Bug 3: Containment Detection Fails

**Symptom**: Tasks inside group not recognized

**Cause**: Comparing relative position against absolute bounds

**Fix**: Always use `computedPosition` for containment:
```typescript
function isInsideGroup(task: Node, group: Node): boolean {
  // WRONG: task.position (may be relative)
  // RIGHT: task.computedPosition (always absolute)

  const taskCenter = {
    x: task.computedPosition.x + (task.dimensions?.width ?? 200) / 2,
    y: task.computedPosition.y + (task.dimensions?.height ?? 100) / 2
  }

  return (
    taskCenter.x >= group.computedPosition.x &&
    taskCenter.x <= group.computedPosition.x + (group.dimensions?.width ?? 400) &&
    taskCenter.y >= group.computedPosition.y &&
    taskCenter.y <= group.computedPosition.y + (group.dimensions?.height ?? 300)
  )
}
```

### Bug 4: Position Persistence Issues

**Symptom**: Positions reset on page reload

**Cause**: Storing `computedPosition` instead of `position` for children

**Fix**: Store the correct coordinate type:
```typescript
function saveNodePosition(node: Node) {
  // For children: store relative position
  // For root nodes: store absolute position
  // node.position is ALWAYS what should be stored

  await saveToDatabase({
    id: node.id,
    position: node.position,  // NOT computedPosition
    parentNode: node.parentNode
  })
}
```

### Bug 5: Stale Parent Reference

**Symptom**: "Stale parentGroupId" warnings, child outside parent bounds

**Cause**: Parent moved/deleted but child still references it

**Fix**: Validate and repair on load:
```typescript
function validateHierarchy(nodes: Node[]) {
  const nodeMap = new Map(nodes.map(n => [n.id, n]))

  for (const node of nodes) {
    if (node.parentNode && !nodeMap.has(node.parentNode)) {
      console.warn(`Orphan node ${node.id} - parent ${node.parentNode} missing`)
      // Convert to root node
      node.parentNode = undefined
      // Position is already absolute-equivalent, keep as-is
    }
  }
}
```

## Resources

### references/
- `coordinate-system.md` - Deep dive into Vue Flow coordinate systems
- `troubleshooting-tree.md` - Systematic problem diagnosis flowchart
- `code-patterns.md` - Proven code patterns for common operations
- `e2e-test-patterns.md` - Playwright E2E test patterns for nested groups and parent movement

### scripts/
- `vueFlowDebug.ts` - TypeScript debugging utilities for Vue Flow

## Verification Checklist

After applying fixes, verify:

- [ ] Dragging parent moves all children together
- [ ] Positions persist correctly across page reloads
- [ ] New tasks dropped in group are detected as children
- [ ] Nested groups maintain hierarchy when moved
- [ ] No position jumping on any operation
- [ ] Console shows no stale parent warnings
