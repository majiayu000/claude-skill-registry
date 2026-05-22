---
name: cli-building
description: Build command-line interfaces with async-first design, composable commands, and proper output formatting. Use when creating CLI tools, commands, or interactive terminal applications.
---

# CLI Building

Guidelines for building command-line interfaces with modern patterns and best practices.

## When to Use

- Creating new CLI tools or commands
- Building interactive terminal applications
- Adding commands to existing projects
- Implementing command-line interfaces
- Working with CLI frameworks

## Core Principles

- **Async-first**: All I/O operations should be async/await, avoid blocking operations
- **Composable commands**: Commands should be modular and reusable, use command composition
- **Strategy pattern**: Use strategy pattern for branching workflows or task-based commands
- **Output formatting**: Proper formatting with unicode symbols and color support

## Framework Selection

### TypeScript/JavaScript

**stricli** (`@bloomberg/stricli`, recommended for modern async-first CLIs):
- Built for async/await from ground up
- Type-safe command definitions with full type inference
- Lazy loading for startup performance
- Zero dependencies

**oclif** (alternative):
- Mature framework with extensive features
- Plugin system
- Good for complex CLIs

### Python

**cyclopts** (recommended for async-first):
- Modern async-first CLI framework
- Type-safe with excellent async support
- Clean API design

**typer** (when fully async support available):
- Based on Python type hints
- Clean and intuitive
- Good for simple to medium complexity CLIs

## Command Architecture

### Composable Commands

Design commands as reusable modules:
- Shared command utilities
- Command middleware
- Reusable command modules
- Command composition patterns

### Strategy Pattern

Use strategy pattern for:
- Workflow branching
- Task-based commands
- Dynamic command routing
- Conditional command execution

## Output Formatting

- **No emojis**: Do not use emojis unless explicitly directed
- **Unicode symbols**: Use unicode symbols (✓, ✗, →, ⚠) for status indicators
- **Color support**: Use color libraries, never hardcoded ANSI codes
- **NO_COLOR**: Always respect `NO_COLOR` environment variable
- **Formatting**: Use formatting for better readability (bold, dim, etc.)

## Async Patterns

### Async-First Design

All I/O should be async:
- File operations: use async file APIs
- Network requests: use async HTTP clients
- Process execution: use async process APIs
- Database operations: use async database clients

### Error Handling

Handle async errors properly:
- Use try/catch with await
- Handle promise rejections
- Provide clear error messages
- Exit with appropriate codes

## Command Structure

### Basic Command

```typescript
// stricli example
import { createCli } from '@bloomberg/stricli';

async function myCommand() {
  // Async implementation
}

const cli = createCli({
  name: 'my-cli',
  commands: {
    'my-command': myCommand
  }
});

cli.run();
```

```python
# cyclopts example
from cyclopts import App

app = App()

@app.default
async def my_command():
    # Async implementation
    pass

if __name__ == '__main__':
    app()
```

## Best Practices

1. **Async by default**: All operations should be async
2. **Composable design**: Build reusable command modules
3. **Strategy pattern**: Use for workflow branching
4. **Proper formatting**: Unicode symbols and color with NO_COLOR support
5. **Error handling**: Clear error messages and exit codes
6. **Type safety**: Use TypeScript types or Python type hints
7. **Testing**: Test commands in isolation

## References

For detailed guidance, see:
- `references/async-patterns.md` - Async/await best practices
- `references/composable-commands.md` - Command composition patterns
- `references/strategy-pattern.md` - Strategy pattern for workflows
- `references/output-formatting.md` - Output formatting guidelines
- `references/frameworks.md` - Framework comparisons and selection
