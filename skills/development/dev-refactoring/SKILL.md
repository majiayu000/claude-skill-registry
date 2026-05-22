---
name: dev-refactoring
description: AUTO-ACTIVATE when working in flow-state-refactor worktree or refactoring large components. MANDATORY port 5550 for refactor worktree. Extract Vue composables, split large files, reduce component size, baseline testing, zero regressions. Triggers on keywords refactor, composable, extract, split component, reduce file size, flow-state-refactor directory.
---

# Systematic Code Refactoring

## 🚨 AUTO-ACTIVATION TRIGGERS

This skill AUTOMATICALLY activates when:
- Working directory is `/flow-state-refactor/`
- Keywords: refactor, composable, extract, split, reduce file size
- Task involves breaking down large components (>2000 lines)
- Creating or modifying files in `src/composables/`
- Any work in the refactor worktree

## 🚨 MANDATORY: PORT 5550 ENFORCEMENT

**REFACTOR WORKTREE EXCLUSIVELY USES PORT 5550**

```bash
# ✅ CORRECT: Always use port 5550 for flow-state-refactor
cd /mnt/d/MY\ PROJECTS/AI/LLM/AI\ Code\ Gen/my-builds/Productivity/flow-state/flow-state-refactor

# Kill any existing process on 5550
lsof -ti:5550 | xargs kill -9

# Start server on PORT 5550 ONLY
npm run dev -- --port 5550

# Verify running on 5550
lsof -i:5550
curl http://localhost:5550
```

### Port Rules (NEVER VIOLATE)
1. ✅ **ALWAYS** port 5550 for `/flow-state-refactor/` worktree
2. ❌ **NEVER** use 5546 (main worktree only)
3. ❌ **NEVER** use auto-assigned ports (5547, 5548, 5554, etc.)
4. ✅ **ALWAYS** explicitly specify `--port 5550`
5. ✅ **ALWAYS** test at http://localhost:5550/#/canvas

### Testing URLs
- **Refactor Worktree ONLY**: http://localhost:5550/#/canvas
- **Main Worktree**: http://localhost:5546 (DO NOT USE when refactoring)

---

## Phase 1: Baseline Testing (MANDATORY)

### Rule: NEVER Refactor Without Baseline
**Test the ORIGINAL code FIRST** to establish proof that features work before refactoring.

```bash
# 1. Navigate to ORIGINAL code on main worktree
cd /mnt/d/MY\ PROJECTS/AI/LLM/AI\ Code\ Gen/my-builds/Productivity/flow-state

# 2. Ensure server is running on port 5546
npm run dev

# 3. Test ALL features with Playwright MCP
# - Create comprehensive test plan
# - Document ALL passing tests
# - Take screenshots
# - Record console output
```

### Baseline Documentation Template
```markdown
# Baseline Test Results - [Component Name]

**Date**: YYYY-MM-DD
**Branch**: main
**Port**: 5546
**Component**: src/[path]/[ComponentName].vue
**Line Count**: XXXX lines

## Test Results

| Feature | Status | Notes |
|---------|--------|-------|
| Feature 1 | ✅ PASS | Description |
| Feature 2 | ✅ PASS | Description |
| Feature 3 | ✅ PASS | Description |

**Tests Passed**: X/X (100%)
**Ready for Refactoring**: ✅ YES

## Screenshots
- `baseline-feature1.png`
- `baseline-feature2.png`

## Console Output
```
[No errors in baseline]
```
```

---

## Phase 2: Composable Extraction

### Extraction Guidelines

#### 1. One Concern Per Composable
```typescript
// ❌ BAD: Mixed concerns
function useEverything() {
  const nodes = ref([])
  const handleClick = () => {}
  const zoom = ref(1)
  const sections = ref([])
  // Too much!
}

// ✅ GOOD: Single responsibility
function useCanvasNodes() {
  const nodes = ref([])
  const syncNodes = () => {}
  return { nodes, syncNodes }
}

function useCanvasControls() {
  const zoom = ref(1)
  const handleZoom = (delta) => {}
  return { zoom, handleZoom }
}
```

#### 2. Parameter Passing (Not Service Locator)
```typescript
// ❌ BAD: Service locator pattern
function useCanvasDragDrop() {
  const { project } = useVueFlow() // ❌ Will fail in composable
}

// ✅ GOOD: Dependency injection
function useCanvasDragDrop(
  nodes: Ref<Node[]>,
  project: (pos: {x: number, y: number}) => {x: number, y: number}
) {
  // Use parameters directly
}

// Component calls it:
const { project } = useVueFlow() // ✅ Call in component
const dragDrop = useCanvasDragDrop(nodes, project) // ✅ Pass to composable
```

#### 3. Naming Conventions
- **File names**: `useFeatureName.ts` (camelCase with `use` prefix)
- **Function names**: `useFeatureName()`
- **Exports**: Named exports only (for tree-shaking)

```typescript
// useCanvasNodes.ts
export function useCanvasNodes(
  taskStore: any,
  canvasStore: any
) {
  // Implementation
  return {
    nodes,
    syncNodes
  }
}

// NOT: export default useCanvasNodes
```

#### 4. Size Guidelines
- **Target**: <300 lines per composable
- **Maximum**: 500 lines (split if larger)
- **Complexity**: One main concern + helpers

#### 5. Initialization Order
Document and enforce initialization dependencies:

```typescript
// ✅ CORRECT ORDER (in component)
const { viewport, project } = useVueFlow()

// 1. Edges (no dependencies)
const { syncEdges } = useCanvasEdges(...)

// 2. Nodes (depends on nothing)
const { nodes, syncNodes } = useCanvasNodes(...)

// 3. Resize (depends on nodes, syncEdges)
const { resizeState, handleResize... } = useCanvasResize(nodes, syncEdges)

// 4. Drag/Drop (depends on nodes, resizeState, syncEdges, project)
const { handleDrop... } = useCanvasDragDrop(nodes, resizeState, syncEdges, project)

// 5. Context Menus (depends on nodes, syncNodes, syncEdges)
const { handleContextMenu... } = useCanvasContextMenus(nodes, syncNodes, syncEdges)

// 6. Controls (depends on most other composables)
const { handleZoom... } = useCanvasControls(...)
```

#### 6. Readonly for State Protection
```typescript
export function useCanvasState() {
  const _state = ref({ zoom: 1 })

  const state = readonly(_state) // ✅ Prevent external mutations

  const setState = (newState: any) => {
    _state.value = newState
  }

  return { state, setState }
}
```

#### 7. Cleanup Side Effects
```typescript
export function useWindowResize() {
  const width = ref(window.innerWidth)

  const handleResize = () => {
    width.value = window.innerWidth
  }

  // Add listener
  window.addEventListener('resize', handleResize)

  // ✅ REQUIRED: Cleanup on unmount
  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
  })

  return { width }
}
```

---

## Phase 3: Integration Testing (MANDATORY)

### Rule: Test Refactored Code Before Merge

```bash
# 1. Navigate to REFACTOR worktree
cd /mnt/d/MY\ PROJECTS/AI/LLM/AI\ Code\ Gen/my-builds/Productivity/flow-state/flow-state-refactor

# 2. Kill any processes on port 5550
lsof -ti:5550 | xargs kill -9

# 3. Start server on port 5550
npm run dev -- --port 5550

# 4. Test ALL baseline features again with Playwright MCP
# - Use SAME test plan as baseline
# - Compare results 1:1
# - Document ANY differences
```

### Integration Test Template
```markdown
# Integration Test Results - [Component Name]

**Date**: YYYY-MM-DD
**Branch**: refactor/[branch-name]
**Port**: 5550
**Component**: src/[path]/[ComponentName].vue
**Line Count Before**: XXXX lines
**Line Count After**: YYYY lines
**Reduction**: ZZ% (XXXX - YYYY lines saved)

## Refactoring Summary
- **Composables Created**: X
  - useFeature1.ts (~XXX lines)
  - useFeature2.ts (~XXX lines)
- **Template**: UNCHANGED
- **Styles**: UNCHANGED

## Test Results

| Feature | Baseline | Integration | Regression |
|---------|----------|-------------|------------|
| Feature 1 | ✅ PASS | ✅ PASS | NO |
| Feature 2 | ✅ PASS | ❌ FAIL | **YES** |
| Feature 3 | ✅ PASS | ✅ PASS | NO |

**Tests Passed**: X/X (XX%)
**Regressions Found**: X
**Ready for Merge**: ❌ NO (if any regressions)

## Regressions Identified
1. **Feature 2**: [Description of regression]
   - **Root Cause**: [Analysis]
   - **Fix Required**: [Solution]

## Console Errors
```
[List any errors found]
```
```

---

## Phase 4: Regression Analysis & Fixes

### Common Refactoring Bugs

#### 1. Hook Call Location
**Error**: `useVueFlow()` called in composable instead of component

```typescript
// ❌ WRONG: Composable calling Vue Flow hook
// useCanvasDragDrop.ts
import { useVueFlow } from '@vue-flow/core'

export function useCanvasDragDrop() {
  const { project } = useVueFlow() // ❌ Fails - not in component context
}

// ✅ CORRECT: Component calls hook, passes to composable
// CanvasView.vue
const { project } = useVueFlow() // ✅ In component context
const dragDrop = useCanvasDragDrop(nodes, resizeState, syncEdges, project)
```

#### 2. Data Structure Mismatch
**Error**: Template accessing wrong nested property

```typescript
// Node creation in composable
allNodes.push({
  id: task.id,
  type: 'taskNode',
  data: task // ✅ Task object directly
})

// ❌ WRONG: Template trying to access nested property
<template #node-taskNode="nodeProps">
  <TaskNode :task="nodeProps.data.task" /> <!-- ❌ data.task doesn't exist -->
</template>

// ✅ CORRECT: Access data directly
<template #node-taskNode="nodeProps">
  <TaskNode :task="nodeProps.data" /> <!-- ✅ data IS the task -->
</template>
```

#### 3. Missing Reactive Dependencies
**Error**: Passing unwrapped refs to composables

```typescript
// ❌ WRONG: Passing .value (not reactive)
const nodes = ref([])
useComposable(nodes.value) // ❌ Not reactive

// ✅ CORRECT: Pass ref itself
const nodes = ref([])
useComposable(nodes) // ✅ Reactive
```

#### 4. Initialization Order
**Error**: Using composable before its dependencies

```typescript
// ❌ WRONG: Using dragDrop before nodes defined
const dragDrop = useCanvasDragDrop(nodes, ...)
const nodes = ref([]) // ❌ Too late!

// ✅ CORRECT: Define dependencies first
const nodes = ref([])
const dragDrop = useCanvasDragDrop(nodes, ...) // ✅ nodes exists
```

---

## Phase 5: Documentation

### Required Documentation Files

1. **`docs/refactoring-prd.md`** - Overall refactoring plan
2. **`docs/phase1-extraction-plan.md`** - Composable breakdown
3. **`docs/phase2-test-results.md`** - Baseline test results
4. **`docs/phase3-integration-test-results.md`** - Integration test results
5. **`docs/debug-[issue].md`** - Debug logs for any regressions

### Code Comments
```typescript
/**
 * Canvas Drag and Drop Composable
 *
 * Handles all drag-and-drop interactions for tasks and sections.
 *
 * @param nodes - Reactive array of Vue Flow nodes
 * @param resizeState - Resize state tracking object
 * @param syncEdges - Function to synchronize edges after operations
 * @param project - Vue Flow coordinate transformation function
 *
 * @returns Drag/drop event handlers and helper functions
 *
 * Dependencies:
 * - Must be called AFTER useCanvasNodes and useCanvasResize
 * - Requires project function from useVueFlow() in component
 */
export function useCanvasDragDrop(
  nodes: Ref<Node[]>,
  resizeState: Ref<any>,
  syncEdges: () => void,
  project: (position: { x: number; y: number }) => { x: number; y: number }
) {
  // Implementation
}
```

---

## Refactoring Checklist

### Pre-Refactoring
- [ ] Component identified (>2000 lines recommended)
- [ ] Baseline tests written and passing (Phase 2)
- [ ] Baseline documentation created
- [ ] Screenshots captured
- [ ] Console clean (no errors)

### During Refactoring
- [ ] Port 5550 used for refactor worktree
- [ ] Composables follow naming conventions (`use*`)
- [ ] One concern per composable (<300 lines)
- [ ] Parameters passed (not service locator pattern)
- [ ] Dependencies injected correctly
- [ ] Initialization order documented
- [ ] Side effects cleaned up (onUnmounted)
- [ ] Readonly used for state protection
- [ ] Named exports only

### Post-Refactoring
- [ ] Integration tests passing (Phase 3)
- [ ] Zero regressions detected
- [ ] Template unchanged
- [ ] Styles unchanged
- [ ] Line count reduced significantly
- [ ] Documentation updated
- [ ] Debug logs removed (if temporary)

### Merge Readiness
- [ ] All tests pass (100%)
- [ ] No console errors
- [ ] Performance unchanged or improved
- [ ] Code reviewed
- [ ] Branch rebased on main
- [ ] Ready for PR

---

## Tooling

### Debug Logging (Temporary)
```typescript
// Add during debugging, remove before merge
console.log('[ComposableName] 🎯 Function called with:', params)
console.log('[ComposableName] ✅ Operation complete')
console.log('[ComposableName] ❌ Error:', error)
```

### Port Management
```bash
# Always check port before starting
lsof -i:5550

# Kill if occupied
lsof -ti:5550 | xargs kill -9

# Start with specific port
npm run dev -- --port 5550

# Verify running
curl http://localhost:5550
```

---

## Performance Optimization

### Computed Properties
```typescript
// ✅ Use computed for derived state
const filteredTasks = computed(() =>
  tasks.value.filter(t => t.status !== 'done')
)

// ❌ Don't recalculate on every render
const getFilteredTasks = () =>
  tasks.value.filter(t => t.status !== 'done')
```

### Debounced Operations
```typescript
import { useDebounceFn } from '@vueuse/core'

const debouncedSave = useDebounceFn(() => {
  saveToDatabase()
}, 1000)
```

---

## Success Metrics

### Code Reduction
- **Target**: 50% reduction in component size
- **Example**: 4082 lines → 2051 lines (49.7% reduction)

### Maintainability
- **Composables**: 5-8 focused files
- **Size**: <300 lines each
- **Concerns**: One per composable

### Quality
- **Tests**: 100% passing
- **Regressions**: 0
- **Console**: 0 errors
- **Performance**: Unchanged or improved

---

This skill ensures systematic, regression-free refactoring with mandatory baseline testing and port 5550 enforcement for the refactor worktree.

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**
