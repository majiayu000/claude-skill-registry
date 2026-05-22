---
name: cli-framework-oclif-ink
description: Modern CLI development combining oclif's command framework with Ink's React-based terminal rendering
---

# oclif + Ink CLI Patterns

> **Quick Guide:** Use oclif for command routing, flag/arg parsing, and plugin architecture. Use Ink for React-based interactive terminal UIs with Flexbox layout. Combine both when commands need rich stateful interfaces. Always `await waitUntilExit()` when rendering Ink from oclif commands. Use `this.log()` instead of `console.log` to preserve JSON output mode.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST `await waitUntilExit()` after `render()` in oclif commands -- without it the process exits before the UI completes)**

**(You MUST use `this.log()` / `this.warn()` / `this.error()` in commands -- `console.log` breaks `--json` mode and test capture)**

**(You MUST wrap all text in `<Text>` components in Ink -- bare strings cause rendering errors)**

**(You MUST use `useEffect` cleanup to cancel async operations -- Ink components unmount when the user presses Ctrl+C)**

</critical_requirements>

---

**Auto-detection:** oclif, @oclif/core, @oclif/test, Ink, ink, @inkjs/ui, Command class, Flags, Args, useInput, useApp, useFocus, render(), waitUntilExit, terminal UI, CLI command, ink-testing-library

**When to use:**

- Building multi-command CLIs with flag/arg parsing
- Creating interactive terminal UIs (wizards, dashboards, progress displays)
- Combining command routing with rich React-based interfaces
- Building plugin-extensible CLI architectures

**When NOT to use:**

- Simple one-off scripts (plain Node.js suffices)
- Basic prompts only (use @clack/prompts or inquirer -- lighter weight)
- Performance-critical startup under 100ms (oclif adds ~200ms overhead)

**Key patterns covered:**

- oclif command structure with typed flags, args, and output methods
- Ink components, Flexbox layout, keyboard input, and focus management
- Integration: rendering Ink from oclif commands with lifecycle management
- @inkjs/ui pre-built components (Select, TextInput, Spinner, etc.)
- Plugin architecture and lifecycle hooks
- Multi-step wizards, progress indicators, and cancelable operations
- Testing commands with `@oclif/test` and components with `ink-testing-library`

---

<philosophy>

## Philosophy

oclif and Ink solve orthogonal problems. **oclif** handles the boring-but-critical parts: command routing, flag parsing, help generation, plugin discovery, auto-updates. **Ink** handles the interactive parts: stateful terminal UIs using React's component model with Flexbox layout.

**Use oclif alone** when commands do their work and print output. **Add Ink** when a command needs real-time user interaction (wizards, dashboards, progress). The integration point is simple: the oclif command's `run()` calls `render()` and awaits `waitUntilExit()`.

**Key architectural decisions:**

- Commands are `.ts` files (not `.tsx`) -- they import Ink components from separate `.tsx` files
- oclif handles process lifecycle; Ink handles UI lifecycle within it
- Keyboard handling lives in Ink components via `useInput`, not in oclif commands
- State management for complex Ink UIs should use an external store (not prop drilling)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: oclif Command with Typed Flags and Args

Commands use static properties for metadata and flag/arg definitions. The `run()` method is async and returns typed data for JSON output support.

```typescript
import { Command, Flags, Args } from "@oclif/core";

const DEFAULT_RETRIES = 3;

export class Deploy extends Command {
  static summary = "Deploy to target environment";
  static enableJsonFlag = true; // Adds --json flag

  static flags = {
    env: Flags.string({
      char: "e",
      required: true,
      options: ["staging", "production"] as const,
    }),
    retries: Flags.integer({
      char: "r",
      default: DEFAULT_RETRIES,
      min: 0,
      max: 10,
    }),
    verbose: Flags.boolean({ char: "v", default: false, allowNo: true }),
    apiKey: Flags.string({ env: "MY_CLI_API_KEY" }), // From env var
  };

  static args = {
    target: Args.string({ description: "Deploy target", required: true }),
  };

  async run(): Promise<{ status: string }> {
    const { args, flags } = await this.parse(Deploy);
    // Use this.log, this.warn, this.error -- never console.*
    this.log(`Deploying ${args.target} to ${flags.env}`);
    return { status: "deployed" };
  }
}
```

See [examples/core.md](examples/core.md) Pattern 1-5 for complete flag types, args, output methods, and error handling.

---

### Pattern 2: Ink Component with Keyboard Handling

Ink components are React functional components using hooks for input, app lifecycle, and focus.

```tsx
import React, { useState } from "react";
import { Box, Text, useInput, useApp } from "ink";

interface SelectorProps {
  items: string[];
  onSelect: (item: string) => void;
}

export const Selector: React.FC<SelectorProps> = ({ items, onSelect }) => {
  const [index, setIndex] = useState(0);
  const { exit } = useApp();

  useInput((input, key) => {
    if (key.upArrow) setIndex((i) => Math.max(0, i - 1));
    if (key.downArrow) setIndex((i) => Math.min(items.length - 1, i + 1));
    if (key.return) onSelect(items[index]);
    if (input === "q") exit();
  });

  return (
    <Box flexDirection="column">
      {items.map((item, i) => (
        <Text key={item} bold={i === index}>
          {i === index ? "> " : "  "}
          {item}
        </Text>
      ))}
    </Box>
  );
};
```

See [examples/core.md](examples/core.md) Pattern 6-8 for styling, layout, and @inkjs/ui components.

---

### Pattern 3: Rendering Ink from oclif Command

The integration pattern: oclif command renders an Ink component and awaits its completion.

```typescript
import { Command, Flags } from "@oclif/core";
import { render } from "ink";
import React from "react";
import { SetupWizard } from "../components/setup-wizard.js";

export class Init extends Command {
  static summary = "Initialize a new project";
  static flags = {
    yes: Flags.boolean({ char: "y", description: "Use defaults", default: false }),
  };

  async run(): Promise<void> {
    const { flags } = await this.parse(Init);
    if (flags.yes) {
      this.log("Initialized with defaults.");
      return;
    }
    // CRITICAL: Destructure waitUntilExit and await it
    const { waitUntilExit } = render(<SetupWizard />);
    await waitUntilExit();
  }
}
```

See [examples/core.md](examples/core.md) Pattern 9 for the full integration pattern with non-interactive fallback.

---

### Pattern 4: Multi-Step Wizard

Wizards use step-based state with back/forward navigation and data accumulation.

```tsx
const MultiStepWizard: React.FC<WizardProps> = ({ steps, onComplete }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [data, setData] = useState<Record<string, unknown>>({});

  const handleNext = (stepData: Record<string, unknown>) => {
    const merged = { ...data, ...stepData };
    setData(merged);
    if (currentIndex === steps.length - 1) onComplete(merged);
    else setCurrentIndex((i) => i + 1);
  };

  const handleBack = () => setCurrentIndex((i) => Math.max(0, i - 1));
  // Render steps[currentIndex].component with {onNext, onBack, data} props
};
```

See [examples/advanced.md](examples/advanced.md) Pattern 1-2 for complete wizard implementation with navigation.

---

### Pattern 5: Plugin Architecture

oclif plugins are npm packages with their own commands and hooks. The host CLI registers plugins in package.json.

```json
{
  "oclif": {
    "plugins": [
      "@oclif/plugin-help",
      "@oclif/plugin-autocomplete",
      "@myorg/cli-plugin-analytics"
    ]
  }
}
```

See [examples/advanced.md](examples/advanced.md) Pattern 4 for creating plugins and user-installable plugin support.

---

### Pattern 6: Testing Commands and Components

Use `@oclif/test` for command tests (flags, args, output, errors) and `ink-testing-library` for Ink component tests (rendering, keyboard simulation).

```typescript
// Command test
import { runCommand } from "@oclif/test";
const { stdout, error } = await runCommand(["deploy", "--env", "staging", "app"]);
expect(stdout).toContain("Deploying");

// Ink component test
import { render } from "ink-testing-library";
const { lastFrame, stdin } = render(<Selector items={["a", "b"]} onSelect={fn} />);
stdin.write("\u001B[B"); // Down arrow
stdin.write("\r");       // Enter
expect(fn).toHaveBeenCalledWith("b");
```

See [examples/testing.md](examples/testing.md) for full testing patterns including async operations, mocking, and snapshot tests.

</patterns>

---

<decision_framework>

## Decision Framework

```
Building a CLI?
|
+-> Need multiple commands / subcommands?
|   +-> YES -> oclif (multi-command mode)
|   +-> NO  -> oclif (single-command mode) or plain Node.js
|
+-> Need interactive terminal UI?
|   +-> Simple prompts (name, confirm)? -> Lightweight prompt library
|   +-> Complex stateful UI (wizard, dashboard)? -> Ink
|
+-> Need both routing AND complex UI?
    +-> YES -> oclif commands + Ink components
    +-> NO  -> Use whichever fits the primary need
```

### Command File Organization

```
src/
  commands/           # oclif command classes (.ts files)
    init.ts
    config/
      get.ts          # mycli config get <key>
      set.ts          # mycli config set <key> <value>
  components/         # Ink React components (.tsx files)
    wizard.tsx
    progress.tsx
  hooks/              # oclif lifecycle hooks
    init.ts           # Runs before every command
    postrun.ts        # Runs after every command
  lib/                # Shared utilities
```

</decision_framework>

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) -- Commands, flags, args, Ink components, integration
- [examples/advanced.md](examples/advanced.md) -- Wizards, progress, plugins, hooks, error boundaries
- [examples/testing.md](examples/testing.md) -- Command tests, component tests, async testing

---

<red_flags>

## RED FLAGS

**High Priority:**

- **Missing `await waitUntilExit()`** -- Command exits before Ink UI completes, user sees nothing
- **Using `console.log` in commands** -- Breaks `--json` output mode and is not captured by `@oclif/test`
- **Bare strings in Ink** -- All text must be wrapped in `<Text>` or rendering fails
- **Blocking the render loop** -- Synchronous work in components freezes the terminal UI

**Medium Priority:**

- **`.tsx` files as commands** -- oclif does not auto-discover `.tsx` files; use `.ts` command files that import `.tsx` components
- **Missing Ctrl+C handling** -- Always provide an exit mechanism via `useInput` or `useApp().exit()`
- **No cleanup in useEffect** -- Async operations must be canceled on unmount to avoid state updates after exit
- **Conflicting `useInput` hooks** -- Multiple active `useInput` hooks fire simultaneously; use the `isActive` option to scope them

**Gotchas & Edge Cases:**

- oclif hooks run in **parallel**, not sequence -- don't depend on execution order between hooks
- `useInput` fires **once** for pasted text, not per-character -- use `usePaste` for paste handling
- Ink v5 requires **React 18+**, Ink v6 requires **React 19+** -- check your Ink version's peer dependencies
- `enableJsonFlag` makes `run()` return value the JSON output -- ensure the return type matches what consumers expect
- oclif's `this.error()` throws (exits the process) -- it does not return

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST `await waitUntilExit()` after `render()` in oclif commands -- without it the process exits before the UI completes)**

**(You MUST use `this.log()` / `this.warn()` / `this.error()` in commands -- `console.log` breaks `--json` mode and test capture)**

**(You MUST wrap all text in `<Text>` components in Ink -- bare strings cause rendering errors)**

**(You MUST use `useEffect` cleanup to cancel async operations -- Ink components unmount when the user presses Ctrl+C)**

**Failure to follow these rules will cause silent process exits, broken JSON output, and terminal rendering crashes.**

</critical_reminders>
