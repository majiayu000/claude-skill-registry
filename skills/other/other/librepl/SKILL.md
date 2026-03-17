---
name: librepl
description: >
  librepl - Interactive REPL utilities. Repl class creates command-line
  interfaces with custom commands, state persistence, and terminal formatting.
  Supports dependency injection for testability. Use for building CLI tools,
  interactive debugging interfaces, and developer utilities.
---

# librepl Skill

## When to Use

- Building interactive CLI tools
- Creating debug and exploration interfaces
- Adding REPL functionality to applications
- Prototyping with persistent state

## Key Concepts

**Repl**: Interactive command-line interface with custom commands, history, and
state management.

## Usage Patterns

### Pattern 1: Create custom REPL

```javascript
import { Repl } from "@copilot-ld/librepl";

const repl = new Repl({
  prompt: "agent> ",
  commands: {
    search: async (query) => {
      const results = await searchIndex(query);
      return JSON.stringify(results, null, 2);
    },
    help: () => "Commands: search <query>, help, exit",
  },
});

await repl.start();
```

### Pattern 2: State persistence

```javascript
const repl = new Repl({
  prompt: "> ",
  storage: storage,
  stateKey: "repl-state",
});
// State persists across sessions
```

## Integration

Used by CLI tools like cli-chat and cli-search. Integrates with libformat for
terminal output.
