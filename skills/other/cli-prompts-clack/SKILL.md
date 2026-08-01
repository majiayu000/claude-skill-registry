---
name: cli-prompts-clack
description: Beautiful interactive CLI prompts with @clack/prompts and custom prompts with @clack/core
---

# Clack CLI Prompts

> **Quick Guide:** Use `@clack/prompts` for pre-styled interactive CLI prompts (text, select, multiselect, confirm, spinner, progress). Check `isCancel()` after EVERY prompt call -- users can Ctrl+C at any point. Use `group()` for multi-step flows with centralized cancellation. Use `@clack/core` only when building fully custom prompt UIs. ESM-only since v1.0.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST check `isCancel()` after EVERY prompt call -- skipping this causes silent crashes when users press Ctrl+C)**

**(You MUST call `process.exit(0)` after `cancel()` -- the cancel message prints but the process keeps running otherwise)**

**(You MUST use `group()` with `onCancel` for multi-step flows -- it handles cancellation centrally so you don't check each prompt individually)**

**(You MUST call `spinner.stop()` before any other output -- overlapping spinner output with prompts or logs corrupts the terminal)**

</critical_requirements>

---

**Auto-detection:** @clack/prompts, @clack/core, clack, isCancel, intro, outro, cancel, spinner, group, text prompt, select prompt, confirm prompt, multiselect, groupMultiselect, selectKey, note, log, tasks, progress, taskLog, stream, box, autocomplete, date prompt, path prompt, updateSettings

**When to use:**

- Building interactive CLI prompts (text input, selection, confirmation)
- Creating multi-step CLI wizards with progress indication
- Adding styled terminal output (notes, logs, boxes, spinners)
- Handling user cancellation gracefully across prompt flows

**When NOT to use:**

- Full terminal UI applications with persistent layout (use a terminal UI framework)
- Non-interactive scripts where stdin is piped (clack prompts require a TTY)
- Simple `y/n` confirmation that doesn't need styling (plain readline suffices)

**Key patterns covered:**

- Core prompts: text, password, select, multiselect, confirm, selectKey
- Session lifecycle: intro, outro, cancel, isCancel
- Progress: spinner, progress bar, tasks
- Composition: group with centralized cancellation
- Output: log, note, box, stream, taskLog
- Custom prompts with @clack/core primitives
- Validation, default values, and AbortSignal cancellation

---

<philosophy>

## Philosophy

Clack provides beautiful, minimal CLI prompts with zero configuration. The `@clack/prompts` package gives you pre-styled components that look great out of the box. Every prompt returns a value or a cancel symbol -- the core discipline is always checking for cancellation.

**Two packages, two purposes:**

- **`@clack/prompts`** -- Pre-styled, opinionated prompts. Use this for 95% of cases.
- **`@clack/core`** -- Unstyled primitives with a `render()` function. Use only when you need a completely custom prompt UI.

**Key design principles:**

- Every prompt is async and returns `value | symbol` -- the symbol indicates cancellation
- Session boundaries (`intro`/`outro`) create visual grouping in the terminal
- `group()` composes multiple prompts with shared cancellation handling
- Spinners, progress bars, and task runners handle long-running operations
- All prompts accept `signal: AbortSignal` for programmatic cancellation

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Session Lifecycle and Cancellation

Every clack CLI flow starts with `intro()` and ends with `outro()`. The critical pattern is checking `isCancel()` after every prompt call.

```typescript
import * as p from "@clack/prompts";

p.intro("Project setup");

const name = await p.text({ message: "Project name?" });

if (p.isCancel(name)) {
  p.cancel("Setup cancelled.");
  process.exit(0);
}

// name is now narrowed to string (not symbol)
p.outro(`Created ${name}`);
```

**Why good:** isCancel check narrows the type from `string | symbol` to `string`, cancel prints a styled message, process.exit prevents dangling execution

```typescript
// BAD: Missing isCancel check
const name = await p.text({ message: "Project name?" });
console.log(`Created ${name}`); // name could be a symbol -- crashes or prints "[Symbol]"
```

**Why bad:** if user presses Ctrl+C, name is a symbol, not a string -- string operations on it will crash or produce garbage output

---

### Pattern 2: Group Prompts with Centralized Cancellation

`group()` chains multiple prompts and handles cancellation in one place. Each prompt receives previous results.

```typescript
import * as p from "@clack/prompts";

const project = await p.group(
  {
    name: () => p.text({ message: "Project name?", placeholder: "my-app" }),
    framework: ({ results }) =>
      p.select({
        message: `Framework for ${results.name}?`,
        options: [
          { value: "react", label: "React" },
          { value: "vue", label: "Vue" },
          { value: "svelte", label: "Svelte" },
        ],
      }),
    install: () => p.confirm({ message: "Install dependencies?" }),
  },
  {
    onCancel: () => {
      p.cancel("Setup cancelled.");
      process.exit(0);
    },
  },
);

// project is typed: { name: string; framework: string; install: boolean }
```

**Why good:** centralized onCancel eliminates per-prompt isCancel checks, results are typed as an object, each prompt can reference previous results via `results`

See [examples/core.md](examples/core.md) for complete group patterns with validation and conditional prompts.

---

### Pattern 3: Spinner and Progress

Spinners show activity during async work. Always stop the spinner before printing other output.

```typescript
import * as p from "@clack/prompts";

const s = p.spinner();
s.start("Installing dependencies");
await installDeps();
s.stop("Dependencies installed");
```

**Progress bar** extends spinner with incremental tracking:

```typescript
const MAX_STEPS = 100;
const prog = p.progress({ max: MAX_STEPS, style: "heavy" });
prog.start("Processing files");
for (const file of files) {
  await processFile(file);
  prog.advance(1, `Processed ${file.name}`);
}
prog.stop("All files processed");
```

**Why good:** spinner and progress provide visual feedback, stop message replaces the spinner line cleanly

See [examples/core.md](examples/core.md) for spinner error handling, cancellation with AbortSignal, and tasks runner.

---

### Pattern 4: Validation

All input prompts accept a `validate` function. Return a string to show an error, or `undefined` to accept.

```typescript
const MIN_LENGTH = 2;
const MAX_LENGTH = 50;

const name = await p.text({
  message: "Package name?",
  validate: (value) => {
    if (!value || value.length < MIN_LENGTH)
      return `Name must be at least ${MIN_LENGTH} characters`;
    if (value.length > MAX_LENGTH)
      return `Name must be at most ${MAX_LENGTH} characters`;
    if (!/^[a-z0-9-]+$/.test(value))
      return "Name must be lowercase alphanumeric with hyphens";
  },
});
```

**Why good:** validation runs inline before the prompt resolves, user sees the error immediately and can retry, named constants for limits

See [examples/core.md](examples/core.md) for validation patterns on different prompt types.

---

### Pattern 5: Output Utilities (log, note, box)

Clack provides styled output functions that match the prompt theme.

```typescript
import * as p from "@clack/prompts";

// Logging with state symbols
p.log.info("Checking configuration...");
p.log.success("Configuration valid");
p.log.warn("Missing optional field: description");
p.log.error("Invalid config file");
p.log.step("Step 1 complete");

// Boxed note for important information
p.note("Run `npm start` to begin development", "Next steps");

// Styled box
p.box("v1.0.0 released!", "Announcement", {
  contentAlign: "center",
  rounded: true,
});
```

**Why good:** themed output matches prompt styling, note/box draw attention to important information

---

### Pattern 6: Tasks Runner

Sequential tasks with automatic success/failure messaging.

```typescript
import * as p from "@clack/prompts";

await p.tasks([
  {
    title: "Downloading template",
    task: async () => {
      await downloadTemplate();
      return "Template downloaded";
    },
  },
  {
    title: "Installing dependencies",
    task: async (message) => {
      message("Resolving packages...");
      await installDeps();
      return "Dependencies installed";
    },
  },
]);
```

**Why good:** tasks display spinner per item, return value becomes the completion message, `message()` callback updates spinner text mid-task

See [examples/core.md](examples/core.md) for error handling in tasks and taskLog for detailed output.

</patterns>

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - All prompt types, cancellation, spinner, progress, tasks, group, validation, output
- [examples/advanced.md](examples/advanced.md) - Custom prompts with @clack/core, AbortSignal, streams, i18n, date/path/autocomplete
- [reference.md](reference.md) - API quick reference, decision framework, prompt type comparison

---

<decision_framework>

## Decision Framework

```
Need user input?
|
+-> Single value?
|   +-> Free text -> text() or password()
|   +-> One of N choices -> select() (list) or selectKey() (keyboard shortcut)
|   +-> Yes/No -> confirm()
|   +-> Date -> date()
|   +-> File path -> path()
|
+-> Multiple values?
|   +-> Flat list -> multiselect()
|   +-> Grouped categories -> groupMultiselect()
|   +-> Searchable -> autocomplete() or autocompleteMultiselect()
|
+-> Multiple prompts in sequence?
    +-> group() with onCancel for centralized handling

Need to show progress?
|
+-> Indeterminate wait -> spinner()
+-> Known total steps -> progress()
+-> Sequential tasks -> tasks()
+-> Detailed logs per task -> taskLog()

Need styled output?
|
+-> Status message -> log.info/warn/error/success/step()
+-> Important notice -> note() or box()
+-> Streaming content -> stream.info/warn/error/success()
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Missing `isCancel()` check after a prompt** -- the return value is `value | symbol`, and using the symbol as a string crashes or produces garbage. Always check before using the value.
- **Missing `process.exit()` after `cancel()`** -- `cancel()` only prints a message, it does not stop execution. The process continues running.
- **Calling another prompt while spinner is active** -- spinner output and prompt output overlap, corrupting the terminal display. Always call `spinner.stop()` first.
- **Using `require()` with @clack/prompts v1.0+** -- the package is ESM-only since v1.0. Use `import` syntax.

**Medium Priority Issues:**

- **Not using `group()` for multi-step flows** -- checking `isCancel()` after every single prompt is verbose and error-prone. `group()` with `onCancel` centralizes this.
- **Ignoring the `validate` option** -- prompts accept invalid input by default. Add validation for any input that has constraints.
- **Using `multiselect` without `required: false` when zero selections should be valid** -- by default, at least one item must be selected.

**Gotchas & Edge Cases:**

- `isCancel()` returns `true` for the cancel symbol but also narrows the TypeScript type -- always use it as a type guard before accessing the value
- `spinner()` returns an object, not a promise -- call `.start()` separately
- `group()` prompt functions receive `{ results }` with all previously collected values, but TypeScript types each value as possibly undefined since earlier prompts might not have run yet
- `confirm()` returns `boolean | symbol`, not just `boolean` -- still needs `isCancel()` check when used outside `group()`
- `select()` generic type parameter controls the return type -- `select<"react" | "vue">({...})` narrows the result
- `log.warn` has an alias `log.warning` -- both work identically
- `progress.advance()` with no arguments advances by 1 -- the step parameter is optional
- `note()` and `box()` are synchronous (not prompts) -- they return `void`, not promises
- All prompts accept `signal: AbortSignal` for programmatic cancellation (e.g., timeouts)
- `updateSettings()` applies globally -- call it once at startup, not per prompt
- v1.1.0 replaced `picocolors` with Node.js built-in `styleText` -- requires Node.js 20.12+

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST check `isCancel()` after EVERY prompt call -- skipping this causes silent crashes when users press Ctrl+C)**

**(You MUST call `process.exit(0)` after `cancel()` -- the cancel message prints but the process keeps running otherwise)**

**(You MUST use `group()` with `onCancel` for multi-step flows -- it handles cancellation centrally so you don't check each prompt individually)**

**(You MUST call `spinner.stop()` before any other output -- overlapping spinner output with prompts or logs corrupts the terminal)**

**Failure to follow these rules will cause silent process hangs, corrupted terminal output, and runtime crashes on user cancellation.**

</critical_reminders>
