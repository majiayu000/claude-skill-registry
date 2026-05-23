---
name: Design Undo/Redo Systems
description: CREATE comprehensive undo/redo systems with Command Pattern. Design state management for complex applications with canvas interactions, multiple stores, and user actions. Use when building new undo/redo functionality from scratch.
---

# Undo/Redo Systems Architecture

## Instructions

### Command Pattern Implementation
Always use the Command Pattern for undo/redo functionality:

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

### Key Requirements
- Always implement both `execute()` and `undo()` methods
- Use async/await for operations that might be slow
- Include descriptive messages for debugging
- Handle circular references in state serialization
- Implement memory management for large histories
- Use delta compression for performance optimization

### Common Patterns
- **Batch Commands**: Group related operations together
- **Checkpoint Commands**: Create application state snapshots
- **Delta Storage**: Store only changes, not full state
- **Memory Management**: Automatic cleanup and compression
- **Error Recovery**: Graceful handling of failed operations

This skill ensures robust, scalable undo/redo systems that maintain consistency across complex applications while optimizing performance and memory usage.