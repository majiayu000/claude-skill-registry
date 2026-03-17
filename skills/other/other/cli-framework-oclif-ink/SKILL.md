---
name: cli-framework-oclif-ink
description: Modern CLI development combining oclif's command framework with Ink's React-based terminal rendering
---

# oclif + Ink CLI Patterns

> **Quick Guide:** Use oclif for command routing, parsing, and plugin architecture. Use Ink for React-based interactive terminal UIs. Combine both when building CLIs that need complex stateful interfaces beyond simple prompts.

---

## Quick Reference

### oclif Command Structure

```typescript
import { Command, Flags, Args } from "@oclif/core";

export class MyCommand extends Command {
  static summary = "Brief description";
  static description = "Detailed description";
  static examples = ["<%= config.bin %> <%= command.id %> --flag value"];

  static flags = {
    name: Flags.string({ char: "n", description: "Name flag", required: true }),
    force: Flags.boolean({ char: "f", default: false }),
  };

  static args = {
    file: Args.string({ description: "File path", required: true }),
  };

  async run(): Promise<void> {
    const { args, flags } = await this.parse(MyCommand);
    this.log(`Processing ${args.file} with name ${flags.name}`);
  }
}
```

### Ink Component Structure

```tsx
import React, { useState } from "react";
import { render, Box, Text, useInput, useApp } from "ink";

const App = () => {
  const [count, setCount] = useState(0);
  const { exit } = useApp();

  useInput((input, key) => {
    if (input === "q") exit();
    if (key.upArrow) setCount((c) => c + 1);
    if (key.downArrow) setCount((c) => c - 1);
  });

  return (
    <Box flexDirection="column">
      <Text>Count: {count}</Text>
      <Text dimColor>Arrows to change, q to quit</Text>
    </Box>
  );
};

render(<App />);
```

### oclif + Ink Integration

```typescript
import { Command, Flags } from "@oclif/core";
import { render } from "ink";
import React from "react";
import { Wizard } from "../components/wizard.js";

export class Init extends Command {
  static flags = {
    source: Flags.string({ char: "s" }),
  };

  async run(): Promise<void> {
    const { flags } = await this.parse(Init);
    const { waitUntilExit } = render(<Wizard source={flags.source} />);
    await waitUntilExit();
  }
}
```

---

## When to Use

**Use oclif when:**

- Building multi-command CLIs (like `git`, `npm`)
- Need plugin architecture for extensibility
- Want auto-generated help and shell completion
- Building enterprise CLIs requiring auto-updates

**Use Ink when:**

- Building complex interactive terminal UIs
- Need React's component model and state management
- Want declarative UI with Flexbox layouts
- Building real-time displays (progress, dashboards)

**Use both together when:**

- CLI commands need rich interactive experiences
- Multi-step wizards with complex state
- Real-time progress displays during operations
- Terminal dashboards or monitoring tools

**Don't use when:**

- Simple one-off scripts (use plain Node.js)
- Basic prompts only (use @clack/prompts or inquirer)
- Performance-critical startup (oclif has ~200ms overhead)

---

## Key Patterns Summary

| Pattern                | Location                                                      |
| ---------------------- | ------------------------------------------------------------- |
| Command definition     | [examples.md](examples.md#command-basics)                     |
| Flags and args         | [examples.md](examples.md#flags-and-args)                     |
| Ink components         | [examples.md](examples.md#ink-basics)                         |
| State with Zustand     | [examples-advanced.md](examples-advanced.md#state-management) |
| Multi-step wizards     | [examples-advanced.md](examples-advanced.md#wizards)          |
| Plugin architecture    | [examples-advanced.md](examples-advanced.md#plugins)          |
| Testing commands       | [examples-testing.md](examples-testing.md)                    |
| Testing Ink components | [examples-testing.md](examples-testing.md#ink-testing)        |

---

## Anti-Patterns

### Command Anti-Patterns

- **Blocking the event loop** - Always use async/await, never sync I/O
- **Not awaiting promises in run()** - Commands timeout after 10s if promises aren't awaited
- **Using `console.log`** - Use `this.log()`, `this.warn()`, `this.error()` instead
- **Mixing Commander.js patterns** - Don't use chained methods, use static properties

### Ink Anti-Patterns

- **Using class components** - Always use functional components with hooks
- **Not wrapping text in `<Text>`** - All text must be inside `<Text>` components
- **Nesting `<Box>` inside `<Text>`** - Only `<Text>` can be nested in `<Text>`
- **Blocking the render loop** - Use `useEffect` for async operations
- **Forgetting cleanup** - Always return cleanup functions from `useEffect`

### Integration Anti-Patterns

- **Not calling `waitUntilExit()`** - Command will exit before Ink component unmounts
- **Using `.tsx` files directly** - oclif doesn't auto-discover `.tsx`, use `.ts` that imports JSX
- **Mixing imperative and declarative** - Don't mix clack prompts with Ink components

---

## Decision Framework

```
Building a CLI?
|
+-> Need multiple commands?
|   +-> YES -> Use oclif
|   +-> NO -> Single command CLI? Use oclif with single command mode
|
+-> Need interactive UI?
|   +-> Simple prompts only? -> Use @clack/prompts (lighter)
|   +-> Complex stateful UI? -> Use Ink
|   +-> Multi-step wizard? -> Use Ink + Zustand
|
+-> Need both routing AND complex UI?
    +-> YES -> oclif + Ink integration
```

---

## Ecosystem Libraries

| Library        | Purpose                  | When to Use                              |
| -------------- | ------------------------ | ---------------------------------------- |
| `@inkjs/ui`    | Pre-built Ink components | Spinners, Select, TextInput, ProgressBar |
| `conf`         | Persistent CLI config    | Store user preferences, last-used values |
| `cosmiconfig`  | Config file loading      | Load .myapprc, myapp.config.js, etc.     |
| `listr2`       | Task list with spinners  | Multiple concurrent/sequential tasks     |
| `execa`        | Child process execution  | Running git, npm, other CLIs             |
| `zod`          | Schema validation        | Validating flags, config, user input     |
| `@oclif/table` | Table rendering          | Displaying data in columns               |

---

## File Structure

```
src/
  commands/           # oclif command classes
    init.ts          # Uses: import { Init } from './init'
    config/
      get.ts         # Subcommand: mycli config get
      set.ts         # Subcommand: mycli config set
  components/        # Ink React components
    wizard.tsx       # Interactive wizards
    spinner.tsx      # Custom spinners
  hooks/             # oclif lifecycle hooks
    init.ts          # Runs before command
    postrun.ts       # Runs after command
  lib/               # Shared utilities
    config.ts        # Configuration helpers
  stores/            # Zustand stores for complex state
    wizard-store.ts
bin/
  dev.js             # Development entry: #!/usr/bin/env -S npx tsx
  run.js             # Production entry
package.json         # oclif configuration
```

---

## Package.json Configuration

```json
{
  "name": "mycli",
  "type": "module",
  "bin": {
    "mycli": "./bin/run.js"
  },
  "oclif": {
    "bin": "mycli",
    "dirname": "mycli",
    "commands": {
      "strategy": "pattern",
      "target": "./dist/commands"
    },
    "plugins": [
      "@oclif/plugin-help",
      "@oclif/plugin-autocomplete",
      "@oclif/plugin-not-found",
      "@oclif/plugin-warn-if-update-available"
    ],
    "hooks": {
      "init": "./dist/hooks/init"
    },
    "topicSeparator": " "
  },
  "dependencies": {
    "@oclif/core": "^4.x",
    "ink": "^5.x",
    "react": "^18.x",
    "@inkjs/ui": "^2.x"
  }
}
```

---

## RED FLAGS

### High Priority

- **Not awaiting promises in run()** - Commands timeout after 10s
- **Missing `waitUntilExit()` call** - Ink component won't complete
- **Using `console.log` in commands** - Breaks JSON output mode
- **Blocking render loop** - Freezes terminal UI

### Medium Priority

- **Using class state in Ink** - Use hooks instead
- **Not handling Ctrl+C** - Always provide exit mechanism
- **Magic numbers** - Use named constants for timeouts, limits

### Common Gotchas

- `.tsx` files not auto-discovered by oclif - import from `.ts` wrapper
- Ink requires React 18+ for concurrent features
- `useInput` callback called once for pasted text (not per-character)
- Multiple `useInput` hooks can conflict - use `isActive` option
- oclif hooks run in parallel, not sequence
