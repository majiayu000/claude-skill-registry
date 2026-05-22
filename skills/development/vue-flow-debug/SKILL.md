---
name: vue-flow-debug
description: Expert skill for debugging Vue Flow parent-child relationships, coordinate systems, and nesting logic. Contains deep knowledge on coordinate conversion and event handling.
triggers:
  - debug vue flow
  - fix nested nodes
  - node parent issues
  - dragging nodes wrong
  - group node bugs
keywords:
  - vue flow
  - nested
  - coordinates
  - parent
  - computedPosition
---

# Vue Flow Nested Nodes & Parent-Child Debugging

## 🎯 **Capabilities**
- **Coordinate Debugging**: Understanding `position` vs `computedPosition`.
- **Relationship Fixes**: Diagnosing parent-child linkage issues.
- **Event Handling**: Correct implementation of drag/drop for nested nodes.
- **Containment Logic**: Advanced geometry checks for "node inside group".

## ⚡ **Action: Debug Protocol**
1.  **Analyze**: Determine if the issue is visual (rendering), logical (state), or persistent (store).
2.  **Verify**: Use the checklists below to validate parent-child integrity.
3.  **Implement**: Apply the robust patterns provided for parent assignment.

---

# expert-knowledge.md

## 1. Vue Flow Coordinate System {#coordinate-system}

### Understanding position vs computedPosition

**node.position (Stored in State)**
*   For root nodes: position = absolute coordinates on the canvas
*   For child nodes (with parentNode set): position = relative to parent's top-left corner
*   Stored in: Your nodes array/Pinia store
*   Used for: Persistence, serialization, state synchronization

```typescript
// Root node - position is absolute
{
  id: 'node-1',
  position: { x: 100, y: 50 },  // 100px from canvas left, 50px from top
  parentNode: undefined
}

// Child node - position is relative to parent
{
  id: 'task-1',
  position: { x: 20, y: 30 },   // 20px from parent's left, 30px from parent's top
  parentNode: 'group-1'
}
```

**node.computedPosition (Calculated at Runtime)**
*   Always absolute: World coordinates regardless of parent
*   Automatically calculated: Vue Flow computes this from position + parent's computedPosition
*   Used for: Rendering, collision detection, drag operations
*   Read-only: Don't set this directly

### Coordinate Transformation Functions

```typescript
// Absolute (world) to Relative (parent-local)
function toRelativePosition(
  absolutePos: { x: number; y: number },
  parentComputedPos: { x: number; y: number }
): { x: number; y: number } {
  return {
    x: absolutePos.x - parentComputedPos.x,
    y: absolutePos.y - parentComputedPos.y
  }
}

// Relative (parent-local) to Absolute (world)
function toAbsolutePosition(
  relativePos: { x: number; y: number },
  parentComputedPos: { x: number; y: number }
): { x: number; y: number } {
  return {
    x: relativePos.x + parentComputedPos.x,
    y: relativePos.y + parentComputedPos.y
  }
}
```

## 2. Common Bugs & Solutions

### Bug #1: Groups Incorrectly Moving Together (Not Nested)
**Symptoms**: When you drag one group, nearby groups move with it.
**Root Cause**: `parentNode` accidentally set or stale references.
**Solution**: Ensure Group nodes have `parentNode: undefined`.

### Bug #2: Positions Jump on Page Load/Refresh
**Root Cause**: Loading state before Vue Flow initializes or mismatched coordinate systems.
**Solution**: Use `onPaneReady` to gate data loading.

### Bug #3: Nested Groups Don't Move with Parent
**Root Cause**: Child's `parentNode` not set correctly or position is absolute instead of relative.
**Solution**: Verify `child.parentNode === parent.id`.

### Bug #4: False Positive Containment (Center-Point Only)
**Problem**: Standard checks only look at the center point. A large node essentially "outside" a group might have its center "inside", verifying it incorrectly.
**Solution**: Use Multi-Corner Containment Check.

```typescript
/**
 * Comprehensive containment check using ALL 4 corners + percentage
 */
function isNodeReallyInsideGroup(node: Node, group: Node, margin = 10) {
    // ... See full implementation in guide ...
}
```

## 3. Debugging Techniques

### Color-Coded Console Logger
Create a consistent logging utility to trace position updates.

### Real-Time Position Visualization
Overlay a transparent div showing live `computedPosition` values to see what Vue Flow "sees".

### Diagnostic Containment Check
Run a script that checks all 4 corners of a node against all groups to definitively prove if it "should" be inside.

---

## 4. Production Ready Patterns

### Reliable Parent Assignment
Do not just check `isInside`. Check `isInside` AND ensures the node fits logically. Only assign if confidence is high (>75% coverage).

### Syncing External Store
Always listen to `onNodesChange` and sync `position` back to your Pinia store. Remember to sync `parentNode` changes too!

```typescript
onNodesChange((changes) => {
  changes.forEach(change => {
    if (change.type === 'position') {
      const node = getNode(change.id)
      nodeStore.update(change.id, {
        position: node.position,
        parentNode: node.parentNode
      })
    }
  })
})
```

---

## 5. Critical: Parent-Child Timing Issues (BUG-152)

### The Problem
When dropping a task from inbox onto a group:
- ❌ Task count doesn't update
- ❌ Task doesn't move with parent group when dragged
- ✓ Page refresh fixes both issues

**Root Cause**: Vue Flow's internal parent-child discovery and coordinate calculations need extra time to settle after you replace the nodes array.

### The Solution: setNodes() + Double nextTick()

**WRONG (Direct Array Mutation)**:
```typescript
// This doesn't trigger Vue Flow's complete initialization
nodes.value = syncNodes()
await nextTick()
// Vue Flow hasn't finished processing parent-child relationships!
```

**CORRECT (Use setNodes)**:
```typescript
import { useVueFlow } from '@vue-flow/core'

const { setNodes, findNode } = useVueFlow()

async function handleDrop(event, taskId, groupId) {
  // 1. Update store
  taskStore.updateTask(taskId, {
    canvasPosition: { x, y },
    isInInbox: false
  })

  // 2. Use setNodes() - triggers Vue Flow's proper initialization
  setNodes(syncNodes())

  // 3. CRITICAL: Double nextTick() for parent-child discovery
  await nextTick()  // First tick: Vue detects change, updates DOM
  await nextTick()  // Second tick: Vue Flow processes parent-child

  // 4. Now safe to read from Vue Flow state
  const task = findNode(`task-${taskId}`)
  console.log('Parent:', task?.parentNode)  // ✓ Populated
}
```

### Why Double nextTick()?

Vue Flow's parent-child discovery needs multiple render cycles:

| Tick | What Happens |
|------|--------------|
| 1st  | Vue detects array change, updates DOM |
| 2nd  | Vue Flow discovers parent-child relationships, recalculates coordinates |

### Alternative: updateNode() for Single Node Changes

```typescript
const { updateNode, findNode } = useVueFlow()

async function handleDrop(taskId, groupId, pos) {
  // 1. Update store
  taskStore.updateTask(taskId, updates)

  // 2. Update only the dropped task
  const relativePos = convertToRelativeCoordinates(pos, groupPos)
  updateNode(taskId, {
    position: relativePos,
    parentNode: `section-${groupId}`
  })

  // 3. Update group's task count
  const groupNode = findNode(`section-${groupId}`)
  if (groupNode) {
    updateNode(`section-${groupId}`, {
      data: {
        ...groupNode.data,
        taskCount: getTaskCountInGroup(groupId)
      }
    })
  }

  // 4. Double nextTick
  await nextTick()
  await nextTick()
}
```

### Best Practice: Track Parent in Pinia Store

For reliable task counts, track parent-child explicitly in Pinia:

```typescript
// In Pinia store
const taskToGroupMap = ref<Record<string, string>>({})

function setTaskParent(taskId: string, parentGroupId: string | null) {
  if (parentGroupId) {
    taskToGroupMap.value[taskId] = parentGroupId
  } else {
    delete taskToGroupMap.value[taskId]
  }
}

const getTaskCountInGroup = computed(() => (groupId: string) => {
  return Object.entries(taskToGroupMap.value)
    .filter(([_, gId]) => gId === groupId).length
})
```

### Common Mistakes

| Mistake | Why It Breaks | Fix |
|---------|---------------|-----|
| Direct `nodes.value =` | Skips Vue Flow initialization | Use `setNodes()` |
| Single `nextTick()` | Parent-child not discovered yet | Double `nextTick()` |
| Reading from `nodes.value` in computed | Stale data | Use `findNode()` |
| Converting to relative twice | Position is wrong | Let Vue Flow handle it OR you handle it, not both |
| Child created before parent | parentNode can't be found | Create parents first in `syncNodes()` |

### Verification Checklist

After implementing, verify:
- [ ] Drop task on group → count increments immediately
- [ ] Drag group → task moves with it
- [ ] Refresh page → state persists correctly
- [ ] Move task between groups → counts update correctly
- [ ] Rapid drops → no race conditions

## Resources

### references/
- `canvas-group-task-counting-tests.md` - E2E test patterns for validating group-task counting, coordinate verification, and parent-child relationships
