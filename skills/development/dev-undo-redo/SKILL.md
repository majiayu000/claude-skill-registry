---
name: dev-undo-redo
description: FIX conflicting undo/redo implementations with VueUse + Pinia and DESIGN robust patterns for complex applications. Use for both stabilizing existing systems and implementing advanced undo/redo architecture.
---

# FlowState Undo/Redo Unification

## Instructions

### **MANDATORY: Use VueUse + Pinia System Only**

**ALWAYS** use this exact pattern for FlowState undo/redo:

```typescript
import { useManualRefHistory } from '@vueuse/core'

const {
  history,
  undo,
  redo,
  canUndo,
  canRedo,
  commit
} = useManualRefHistory(unifiedState, {
  capacity: 50,
  deep: true,
  clone: true
})

// Pattern: Save state before and after every change
const saveState = (description: string) => {
  commit() // VueUse handles everything
}
```

### **Implementation Rules**

1. **NEVER** create custom undo/redo implementations
2. **NEVER** use manual JSON serialization
3. **NEVER** create multiple history managers
4. **ALWAYS** call `saveState()` before and after state changes
5. **ALWAYS** use the unified composable `useUnifiedUndoRedo()`
6. **ALWAYS** handle both stores (tasks, canvas, timer) in one system

### **Store Action Pattern**

```typescript
actions: {
  createTask(taskData: Partial<Task>) {
    const undoRedo = useUnifiedUndoRedo()
    undoRedo.saveState('Before task creation')

    // Your logic here
    this.tasks.push(newTask)

    undoRedo.saveState('After task creation')
    return newTask
  }
}
```

### **Component Pattern**

```vue
<script setup>
const { canUndo, canRedo, undo, redo } = useUnifiedUndoRedo()

// Keyboard shortcuts handled automatically
// UI shows correct button states
</script>

<template>
  <button @click="undo" :disabled="!canUndo">↶ Undo</button>
  <button @click="redo" :disabled="!canRedo">↷ Redo</button>
</template>
```

This skill ensures ONE consistent undo/redo system across FlowState, eliminating all conflicts and providing reliable functionality.

---

## Advanced Architecture Patterns

For complex applications requiring enhanced undo/redo capabilities, consider these advanced patterns:

### Command Pattern Implementation

Use the Command Pattern for complex operations requiring granular control:

```typescript
interface Command {
  execute(): void | Promise<void>
  undo(): void | Promise<void>
  getDescription(): string
  canExecute(): boolean
}

class OptimizedHistory {
  private undoStack: HistoryEntry[] = []
  private redoStack: HistoryEntry[] = []

  async execute(command: Command): Promise<void> {
    await command.execute()
    this.undoStack.push({ command, timestamp: Date.now() })
    this.redoStack = []
    this.optimizeMemory()
  }
}
```

### Application-Specific Commands

Create domain-specific commands for all mutable operations:

```typescript
// Task Management Commands
class CreateTaskCommand extends BaseCommand {
  constructor(private taskStore: any, private taskData: any) {
    super(`Create task: ${taskData.title}`)
  }

  async execute(): Promise<void> {
    this.generatedId = await this.taskStore.createTask(this.taskData)
  }

  async undo(): Promise<void> {
    if (this.generatedId) {
      await this.taskStore.deleteTask(this.generatedId)
    }
  }
}

// Canvas Interaction Commands
class MoveNodeCommand extends BaseCommand {
  constructor(
    private canvasStore: any,
    private nodeId: string,
    private fromPos: Position,
    private toPos: Position
  ) {
    super(`Move node ${nodeId}`)
  }

  async execute(): Promise<void> {
    await this.canvasStore.updateNodePosition(this.nodeId, this.toPos)
  }

  async undo(): Promise<void> {
    await this.canvasStore.updateNodePosition(this.nodeId, this.fromPos)
  }
}
```

### Performance Optimizations

For large-scale applications, implement these optimizations:

#### Memory Management
- Automatic cleanup of old history entries
- Delta compression for state changes
- Circular buffer for fixed-size history

#### Batch Operations
- Group related operations into single commands
- Transaction-like behavior for complex changes
- Rollback capability for failed operations

#### Asynchronous Operations
- Support for async/await in command execution
- Progress tracking for long-running operations
- Error recovery and retry mechanisms

### Key Requirements for Advanced Systems
- Always implement both `execute()` and `undo()` methods
- Use async/await for operations that might be slow
- Include descriptive messages for debugging and user feedback
- Handle circular references in state serialization
- Implement memory management for large histories
- Use delta compression for performance optimization

### Common Advanced Patterns
- **Batch Commands**: Group related operations together
- **Checkpoint Commands**: Create application state snapshots
- **Delta Storage**: Store only changes, not full state
- **Memory Management**: Automatic cleanup and compression
- **Error Recovery**: Graceful handling of failed operations

### When to Use Advanced Patterns

Use Command Pattern and advanced architecture when:
- Building new undo/redo systems from scratch
- Need granular control over individual operations
- Working with complex state changes across multiple stores
- Implementing transaction-like behavior
- Requiring advanced memory management and optimization

### When to Use VueUse + Pinia

Use the VueUse approach (from primary section above) when:
- Fixing existing FlowState undo/redo issues
- Working with Vue 3 + Pinia stack
- Need rapid implementation with proven patterns
- Managing state within single store or related stores
- Prioritizing development speed over architectural complexity

This comprehensive approach ensures robust, scalable undo/redo systems that maintain consistency across complex applications while optimizing performance and memory usage.

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
