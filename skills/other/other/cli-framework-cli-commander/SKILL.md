---
name: cli-framework-cli-commander
description: Node.js CLI development with Commander.js, @clack/prompts, and picocolors. Command structure, interactive prompts, state machines, error handling, exit codes, configuration hierarchies.
---

# CLI Application Development with Commander.js

> **Quick Guide:** Use Commander.js for command structure, @clack/prompts for interactive UX, and picocolors for terminal colors. Structure commands in separate files, use standardized exit codes, handle cancellation gracefully, and implement config hierarchies (flag > env > project > global > default).

---

<critical_requirements>

## CRITICAL: Before Building CLI Applications

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST handle SIGINT (Ctrl+C) gracefully and exit with appropriate codes)**

**(You MUST use `p.isCancel()` to detect cancellation in ALL @clack/prompts and handle gracefully)**

**(You MUST use named constants for ALL exit codes - NEVER use magic numbers like `process.exit(1)`)**

**(You MUST use `parseAsync()` for async actions to properly propagate errors)**

</critical_requirements>

---

**Auto-detection:** Commander.js, @clack/prompts, CLI command structure, p.spinner, p.select, p.confirm, p.text, picocolors, process.exit, exit codes, SIGINT handling, interactive prompts, wizard state machine, config hierarchy, CLI error handling

**When to use:**

- Building command-line tools with Node.js
- Creating interactive terminal prompts and wizards
- Implementing multi-step workflows with state machines
- Managing hierarchical configuration (flag > env > project > global)
- Structuring CLI applications with subcommands
- Handling errors and exit codes consistently

**Key patterns covered:**

- Commander.js command structure and options
- @clack/prompts for interactive UX (spinners, selects, confirms)
- picocolors for terminal output styling
- Standardized exit codes with named constants
- SIGINT and cancellation handling
- Config hierarchy resolution (precedence chain)
- Wizard state machines for multi-step flows
- Command organization and subcommands
- Error handling patterns and user feedback
- Dry-run mode implementation
- File system operations with fs-extra and fast-glob

---

<philosophy>

## Philosophy

**User experience first.** CLI tools should be intuitive, provide helpful feedback, and fail gracefully. Users should always know what's happening (spinners), what went wrong (clear errors), and how to fix it (actionable messages).

**Consistency across commands.** Every command should follow the same patterns: options at top, spinner feedback, success/error messaging, and proper exit codes. This makes the CLI predictable and learnable.

**Graceful degradation.** Always handle cancellation (Ctrl+C), invalid input, and errors. Never leave users in an unknown state.

**When to use Commander.js:**

- Multi-command CLI tools (git-like interfaces)
- Tools with complex option parsing
- Applications needing help generation
- TypeScript-first development

**When to use @clack/prompts:**

- Interactive setup wizards
- User confirmation flows
- Multi-step selections
- Any user input beyond simple flags

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: CLI Entry Point Structure

Organize the main entry point with global options, signal handling, and command registration.

#### File: `src/cli/index.ts`

```typescript
import { Command } from "commander";
import pc from "picocolors";
import { initCommand } from "./commands/init";
import { configCommand } from "./commands/config";
import { validateCommand } from "./commands/validate";
import { EXIT_CODES } from "./lib/exit-codes";

// Handle Ctrl+C gracefully - REQUIRED for good UX
process.on("SIGINT", () => {
  console.log(pc.yellow("\nCancelled"));
  process.exit(EXIT_CODES.CANCELLED);
});

async function main() {
  const program = new Command();

  program
    .name("mycli")
    .description("My CLI tool description")
    .version("1.0.0")
    // Global options available to all commands
    .option("--dry-run", "Preview operations without executing")
    .option("-v, --verbose", "Enable verbose output")
    // Customize error output with colors
    .configureOutput({
      writeErr: (str) => console.error(pc.red(str)),
    })
    // Show help after errors for discoverability
    .showHelpAfterError(true);

  // Register commands - keep main file clean
  program.addCommand(initCommand);
  program.addCommand(configCommand);
  program.addCommand(validateCommand);

  // Use parseAsync for proper async error handling
  await program.parseAsync(process.argv);
}

// Centralized error handling
main().catch((err) => {
  console.error(pc.red("Error:"), err.message);
  process.exit(EXIT_CODES.ERROR);
});
```

**Why good:** SIGINT handler prevents orphaned processes, parseAsync properly propagates errors, configureOutput adds consistent styling, global options shared across commands

---

### Pattern 2: Standardized Exit Codes

Define exit codes as named constants for consistency and maintainability.

#### File: `src/cli/lib/exit-codes.ts`

```typescript
/**
 * CLI exit codes for standardized process termination
 * Following Unix conventions: 0 = success, non-zero = error
 */
export const EXIT_CODES = {
  /** Successful execution */
  SUCCESS: 0,
  /** General error */
  ERROR: 1,
  /** Invalid arguments or options */
  INVALID_ARGS: 2,
  /** Network or connectivity error */
  NETWORK_ERROR: 3,
  /** User cancelled operation (Ctrl+C) */
  CANCELLED: 4,
  /** Resource not found */
  NOT_FOUND: 5,
  /** Permission denied */
  PERMISSION_DENIED: 6,
  /** Validation failed */
  VALIDATION_ERROR: 7,
} as const;

export type ExitCode = (typeof EXIT_CODES)[keyof typeof EXIT_CODES];
```

**Why good:** Named constants make code readable, `as const` enables type inference, JSDoc explains each code's meaning, follows Unix conventions

```typescript
// BAD Example - Magic numbers
process.exit(1); // What does 1 mean?
process.exit(0);

// GOOD Example - Named constants
import { EXIT_CODES } from "./lib/exit-codes";
process.exit(EXIT_CODES.VALIDATION_ERROR);
```

**Why bad:** Magic numbers are unmaintainable and unclear to readers

---

### Pattern 3: Command Definition with Options

Structure individual commands with proper typing and option handling.

#### File: `src/cli/commands/init.ts`

```typescript
import { Command } from "commander";
import * as p from "@clack/prompts";
import pc from "picocolors";
import { EXIT_CODES } from "../lib/exit-codes";

export const initCommand = new Command("init")
  .description("Initialize the project")
  // Options with descriptions for auto-generated help
  .option("--source <url>", "Source URL (e.g., github:org/repo)")
  .option("--refresh", "Force refresh from remote", false)
  .option("-f, --force", "Overwrite existing files", false)
  // Consistent error styling
  .configureOutput({
    writeErr: (str) => console.error(pc.red(str)),
  })
  .showHelpAfterError(true)
  // Action handler receives options and command context
  .action(async (options, command) => {
    // Access global options from parent
    const globalOpts = command.optsWithGlobals();
    const dryRun = globalOpts.dryRun ?? false;
    const verbose = globalOpts.verbose ?? false;

    // Start interactive UI
    p.intro(pc.cyan("Project Setup"));

    if (dryRun) {
      p.log.info(
        pc.yellow("[dry-run] Preview mode - no files will be created"),
      );
    }

    // ... implementation
  });
```

**Why good:** Named export follows convention, options have descriptions, access global options via optsWithGlobals(), intro sets context for user

---

### Pattern 4: Interactive Prompts with @clack/prompts

Use @clack/prompts for beautiful, consistent interactive UX.

#### Spinner Pattern

```typescript
import * as p from "@clack/prompts";
import pc from "picocolors";

async function processFiles() {
  const s = p.spinner();

  // Start with descriptive message
  s.start("Processing files...");

  try {
    const result = await doAsyncWork();
    // Stop with success message including result info
    s.stop(`Processed ${result.count} files`);
    return result;
  } catch (error) {
    // Stop spinner before showing error
    s.stop("Failed to process files");
    p.log.error(error instanceof Error ? error.message : "Unknown error");
    process.exit(EXIT_CODES.ERROR);
  }
}
```

#### Select Pattern with Cancellation Handling

```typescript
import * as p from "@clack/prompts";
import pc from "picocolors";

async function selectFramework(): Promise<string | null> {
  const result = await p.select({
    message: "Select a framework:",
    options: [
      { value: "react", label: "React", hint: "recommended" },
      { value: "vue", label: "Vue" },
      { value: "angular", label: "Angular" },
    ],
    initialValue: "react",
  });

  // CRITICAL: Always check for cancellation
  if (p.isCancel(result)) {
    p.cancel("Setup cancelled");
    process.exit(EXIT_CODES.CANCELLED);
  }

  return result;
}
```

**Why good:** isCancel check prevents undefined behavior, hint guides users, initialValue improves UX

#### Confirm Pattern

```typescript
async function confirmDestructiveAction(): Promise<boolean> {
  const proceed = await p.confirm({
    message: "This will delete existing files. Continue?",
    initialValue: false, // Default to safe option
  });

  if (p.isCancel(proceed)) {
    p.cancel("Operation cancelled");
    process.exit(EXIT_CODES.CANCELLED);
  }

  return proceed;
}
```

#### Text Input with Validation

```typescript
async function getProjectName(): Promise<string> {
  const name = await p.text({
    message: "Project name:",
    placeholder: "my-project",
    validate: (value) => {
      if (!value) return "Name is required";
      if (!/^[a-z0-9-]+$/.test(value)) {
        return "Use lowercase letters, numbers, and hyphens only";
      }
    },
  });

  if (p.isCancel(name)) {
    p.cancel("Setup cancelled");
    process.exit(EXIT_CODES.CANCELLED);
  }

  return name;
}
```

---

### Pattern 5: Wizard State Machine

Implement complex multi-step flows with a state machine pattern.

#### Constants

```typescript
// Navigation sentinel values
const BACK_VALUE = "__back__";
const CONTINUE_VALUE = "__continue__";

// State machine step types
type WizardStep = "approach" | "selection" | "review" | "confirm";
```

#### State Interface

```typescript
interface WizardState {
  currentStep: WizardStep;
  selectedItems: string[];
  history: WizardStep[]; // For back navigation
  lastSelectedItem: string | null; // For cursor restoration
}

function createInitialState(): WizardState {
  return {
    currentStep: "approach",
    selectedItems: [],
    history: [],
    lastSelectedItem: null,
  };
}
```

#### State Machine Implementation

```typescript
import * as p from "@clack/prompts";
import pc from "picocolors";

interface WizardResult {
  selectedItems: string[];
  confirmed: boolean;
}

export async function runWizard(): Promise<WizardResult | null> {
  const state = createInitialState();

  // Main wizard loop
  while (true) {
    switch (state.currentStep) {
      case "approach": {
        const result = await stepApproach(state);

        if (p.isCancel(result)) {
          return null; // User cancelled
        }

        if (result === "scratch") {
          pushHistory(state);
          state.currentStep = "selection";
        } else if (result === "template") {
          // Handle template selection...
        }
        break;
      }

      case "selection": {
        const result = await stepSelection(state);

        if (p.isCancel(result)) {
          return null;
        }

        if (result === BACK_VALUE) {
          state.currentStep = popHistory(state) || "approach";
          break;
        }

        if (result === CONTINUE_VALUE) {
          pushHistory(state);
          state.currentStep = "confirm";
          break;
        }

        // Toggle selection
        toggleSelection(state, result as string);
        break;
      }

      case "confirm": {
        const result = await stepConfirm(state);

        if (p.isCancel(result)) {
          return null;
        }

        if (result === BACK_VALUE) {
          state.currentStep = popHistory(state) || "selection";
          break;
        }

        if (result === "confirm") {
          return {
            selectedItems: state.selectedItems,
            confirmed: true,
          };
        }
        break;
      }
    }
  }
}

// History management for back navigation
function pushHistory(state: WizardState): void {
  state.history.push(state.currentStep);
}

function popHistory(state: WizardState): WizardStep | null {
  return state.history.pop() || null;
}

function toggleSelection(state: WizardState, item: string): void {
  const index = state.selectedItems.indexOf(item);
  if (index > -1) {
    state.selectedItems.splice(index, 1);
  } else {
    state.selectedItems.push(item);
  }
  state.lastSelectedItem = item;
}
```

**Why good:** State machine makes complex flows manageable, history enables natural back navigation, separation of step functions keeps code organized

---

### Pattern 6: Configuration Hierarchy

Implement config resolution with clear precedence chain.

#### File: `src/cli/lib/config.ts`

```typescript
import path from "path";
import os from "os";
import { parse as parseYaml, stringify as stringifyYaml } from "yaml";
import { readFile, writeFile, fileExists, ensureDir } from "../utils/fs";

// Config locations
export const GLOBAL_CONFIG_DIR = path.join(os.homedir(), ".myapp");
export const GLOBAL_CONFIG_FILE = "config.yaml";
const PROJECT_CONFIG_DIR = ".myapp";
const PROJECT_CONFIG_FILE = "config.yaml";

// Environment variable name
export const SOURCE_ENV_VAR = "MYAPP_SOURCE";

// Default value
export const DEFAULT_SOURCE = "github:myorg/default-repo";

export interface GlobalConfig {
  source?: string;
  author?: string;
}

export interface ProjectConfig {
  source?: string;
}

export interface ResolvedConfig {
  source: string;
  sourceOrigin: "flag" | "env" | "project" | "global" | "default";
}

/**
 * Resolve configuration with precedence:
 * 1. CLI flag (--source)
 * 2. Environment variable (MYAPP_SOURCE)
 * 3. Project config (.myapp/config.yaml)
 * 4. Global config (~/.myapp/config.yaml)
 * 5. Default value
 */
export async function resolveSource(
  flagValue?: string,
  projectDir?: string,
): Promise<ResolvedConfig> {
  // 1. CLI flag takes highest priority
  if (flagValue !== undefined) {
    if (flagValue.trim() === "") {
      throw new Error("--source flag cannot be empty");
    }
    return { source: flagValue, sourceOrigin: "flag" };
  }

  // 2. Environment variable
  const envValue = process.env[SOURCE_ENV_VAR];
  if (envValue) {
    return { source: envValue, sourceOrigin: "env" };
  }

  // 3. Project config
  if (projectDir) {
    const projectConfig = await loadProjectConfig(projectDir);
    if (projectConfig?.source) {
      return { source: projectConfig.source, sourceOrigin: "project" };
    }
  }

  // 4. Global config
  const globalConfig = await loadGlobalConfig();
  if (globalConfig?.source) {
    return { source: globalConfig.source, sourceOrigin: "global" };
  }

  // 5. Default
  return { source: DEFAULT_SOURCE, sourceOrigin: "default" };
}

export function formatSourceOrigin(
  origin: ResolvedConfig["sourceOrigin"],
): string {
  switch (origin) {
    case "flag":
      return "--source flag";
    case "env":
      return `${SOURCE_ENV_VAR} environment variable`;
    case "project":
      return "project config (.myapp/config.yaml)";
    case "global":
      return "global config (~/.myapp/config.yaml)";
    case "default":
      return "default";
  }
}
```

**Why good:** Clear precedence chain documented, each source explicitly named, format function for user-friendly display

---

### Pattern 7: Subcommand Organization

Structure complex commands with subcommands for related operations.

#### File: `src/cli/commands/config.ts`

```typescript
import { Command } from "commander";
import * as p from "@clack/prompts";
import pc from "picocolors";
import {
  resolveSource,
  loadGlobalConfig,
  saveGlobalConfig,
  getGlobalConfigPath,
  formatSourceOrigin,
} from "../lib/config";
import { EXIT_CODES } from "../lib/exit-codes";

export const configCommand = new Command("config")
  .description("Manage configuration")
  .configureOutput({
    writeErr: (str) => console.error(pc.red(str)),
  })
  .showHelpAfterError(true);

// Subcommand: config show
configCommand
  .command("show")
  .description("Show current effective configuration")
  .action(async () => {
    const projectDir = process.cwd();
    const resolved = await resolveSource(undefined, projectDir);

    console.log(pc.cyan("\nConfiguration\n"));
    console.log(pc.bold("Source:"));
    console.log(`  ${pc.green(resolved.source)}`);
    console.log(
      `  ${pc.dim(`(from ${formatSourceOrigin(resolved.sourceOrigin)})`)}`,
    );
    console.log("");
  });

// Subcommand: config set
configCommand
  .command("set")
  .description("Set a global configuration value")
  .argument("<key>", "Configuration key (source, author)")
  .argument("<value>", "Configuration value")
  .action(async (key: string, value: string) => {
    const validKeys = ["source", "author"];

    if (!validKeys.includes(key)) {
      p.log.error(`Unknown configuration key: ${key}`);
      p.log.info(`Valid keys: ${validKeys.join(", ")}`);
      process.exit(EXIT_CODES.INVALID_ARGS);
    }

    const existingConfig = (await loadGlobalConfig()) || {};
    const newConfig = { ...existingConfig, [key]: value };

    await saveGlobalConfig(newConfig);

    p.log.success(`Set ${key} = ${value}`);
    p.log.info(`Saved to ${getGlobalConfigPath()}`);
  });

// Subcommand: config get
configCommand
  .command("get")
  .description("Get a configuration value")
  .argument("<key>", "Configuration key")
  .action(async (key: string) => {
    if (key === "source") {
      const resolved = await resolveSource(undefined, process.cwd());
      console.log(resolved.source);
    } else {
      p.log.error(`Unknown key: ${key}`);
      process.exit(EXIT_CODES.INVALID_ARGS);
    }
  });
```

**Why good:** Logical grouping of related commands, arguments validated early, consistent error handling across subcommands

---

### Pattern 8: Output Formatting with picocolors

Use consistent styling for different message types.

```typescript
import pc from "picocolors";

// Success messages
console.log(pc.green("Operation completed successfully!"));

// Warnings
console.log(pc.yellow("Warning: This may take a while"));

// Errors
console.error(pc.red("Error:"), error.message);

// Informational with dimmed context
console.log(`Source: ${pc.cyan(source)}`);
console.log(pc.dim(`(from ${origin})`));

// Section headers
console.log(pc.bold("\nConfiguration:\n"));

// Lists with icons
console.log(`  ${pc.green("+")} Added: ${item}`);
console.log(`  ${pc.red("-")} Removed: ${item}`);
console.log(`  ${pc.yellow("!")} Warning: ${message}`);

// Status indicators
const status = isValid ? pc.green("valid") : pc.red("invalid");
console.log(`Status: ${status}`);

// Styled options in prompts
const options = [
  { value: "yes", label: pc.green("Yes, proceed") },
  { value: "no", label: pc.dim("No, cancel") },
];
```

---

### Pattern 9: Dry-Run Mode

Implement preview functionality for destructive operations.

```typescript
import * as p from "@clack/prompts";
import pc from "picocolors";

export async function executeWithDryRun(
  dryRun: boolean,
  operations: Array<{ description: string; execute: () => Promise<void> }>,
): Promise<void> {
  if (dryRun) {
    p.log.info(pc.yellow("[dry-run] Preview mode - no changes will be made"));
    console.log("");

    for (const op of operations) {
      console.log(pc.yellow(`[dry-run] Would: ${op.description}`));
    }

    console.log("");
    p.outro(pc.green("[dry-run] Preview complete"));
    return;
  }

  // Execute for real
  const s = p.spinner();
  for (const op of operations) {
    s.start(op.description);
    await op.execute();
    s.stop(`Done: ${op.description}`);
  }
}

// Usage in command
.action(async (options, command) => {
  const dryRun = command.optsWithGlobals().dryRun ?? false;

  await executeWithDryRun(dryRun, [
    {
      description: "Create config file",
      execute: async () => {
        await writeFile(configPath, content);
      },
    },
    {
      description: "Install dependencies",
      execute: async () => {
        await installDeps();
      },
    },
  ]);
});
```

---

### Pattern 10: File System Utilities

Wrap fs-extra and fast-glob for consistent async patterns.

#### File: `src/cli/utils/fs.ts`

```typescript
import fs from "fs-extra";
import fg from "fast-glob";
import path from "path";

export async function readFile(filePath: string): Promise<string> {
  return fs.readFile(filePath, "utf-8");
}

export async function readFileOptional(
  filePath: string,
  fallback = "",
): Promise<string> {
  try {
    return await fs.readFile(filePath, "utf-8");
  } catch {
    return fallback;
  }
}

export async function fileExists(filePath: string): Promise<boolean> {
  return fs.pathExists(filePath);
}

export async function directoryExists(dirPath: string): Promise<boolean> {
  try {
    const stat = await fs.stat(dirPath);
    return stat.isDirectory();
  } catch {
    return false;
  }
}

export async function glob(pattern: string, cwd: string): Promise<string[]> {
  return fg(pattern, { cwd, onlyFiles: true });
}

export async function writeFile(
  filePath: string,
  content: string,
): Promise<void> {
  // Ensure parent directory exists
  await fs.ensureDir(path.dirname(filePath));
  await fs.writeFile(filePath, content, "utf-8");
}

export async function ensureDir(dirPath: string): Promise<void> {
  await fs.ensureDir(dirPath);
}

export async function remove(filePath: string): Promise<void> {
  await fs.remove(filePath);
}

export async function copy(src: string, dest: string): Promise<void> {
  await fs.copy(src, dest);
}

export async function listDirectories(dirPath: string): Promise<string[]> {
  try {
    const entries = await fs.readdir(dirPath, { withFileTypes: true });
    return entries.filter((e) => e.isDirectory()).map((e) => e.name);
  } catch {
    return [];
  }
}
```

**Why good:** Consistent async API, ensureDir before writes prevents errors, optional file read with fallback

---

### Pattern 11: Verbose Logging Utility

Implement conditional verbose output.

#### File: `src/cli/utils/logger.ts`

```typescript
import pc from "picocolors";

let verboseMode = false;

export function setVerbose(enabled: boolean): void {
  verboseMode = enabled;
}

export function verbose(msg: string): void {
  if (verboseMode) {
    console.log(pc.dim(`  ${msg}`));
  }
}

// Usage in commands
import { setVerbose, verbose } from "../utils/logger";

.action(async (options) => {
  setVerbose(options.verbose);

  verbose("Starting operation...");
  verbose(`Reading from ${path}`);

  // ... regular output
  console.log("Operation complete");
});
```

</patterns>

---

<decision_framework>

## Decision Framework

### Command Structure Decision

```
Is it a single operation?
├─ YES → Single command with options
└─ NO → Are operations related?
    ├─ YES → Subcommands under parent (config show, config set)
    └─ NO → Separate top-level commands
```

### User Input Decision

```
Does user need to provide input?
├─ NO → Use options/flags only
└─ YES → Is it a simple yes/no?
    ├─ YES → p.confirm()
    └─ NO → Is it choosing from options?
        ├─ YES → p.select() or p.multiselect()
        └─ NO → Is it free-form text?
            └─ YES → p.text() with validation
```

### Async Operation Feedback

```
Is operation quick (< 500ms)?
├─ YES → No spinner needed
└─ NO → Use p.spinner() with:
    ├─ start("Descriptive message...")
    ├─ stop("Success with result info")
    └─ Error: stop first, then p.log.error()
```

### Config Value Resolution

```
Check in order, first defined wins:
1. --flag (CLI argument)
2. ENV_VAR (environment variable)
3. ./.myapp/config.yaml (project config)
4. ~/.myapp/config.yaml (global config)
5. DEFAULT_VALUE (hardcoded default)
```

</decision_framework>

---

<testing>

## Testing CLI Commands

### Testing Commander Commands

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import { Command } from "commander";

describe("init command", () => {
  let program: Command;
  let exitSpy: ReturnType<typeof vi.spyOn>;
  let consoleSpy: ReturnType<typeof vi.spyOn>;

  beforeEach(() => {
    program = new Command();
    program.exitOverride(); // Prevent actual process.exit
    exitSpy = vi.spyOn(process, "exit").mockImplementation(() => {
      throw new Error("process.exit called");
    });
    consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});
  });

  it("shows help with --help", async () => {
    const helpSpy = vi.spyOn(program, "outputHelp");

    try {
      await program.parseAsync(["node", "test", "--help"]);
    } catch {
      // exitOverride throws
    }

    expect(helpSpy).toHaveBeenCalled();
  });

  it("validates required options", async () => {
    // Add your command setup here

    await expect(
      program.parseAsync(["node", "test", "init", "--invalid"]),
    ).rejects.toThrow();
  });
});
```

### Testing with Mock File System

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { vol } from "memfs";

vi.mock("fs-extra", async () => {
  const memfs = await import("memfs");
  return memfs.fs.promises;
});

describe("config loading", () => {
  beforeEach(() => {
    vol.reset();
  });

  afterEach(() => {
    vol.reset();
  });

  it("loads config from file", async () => {
    vol.fromJSON({
      "/home/user/.myapp/config.yaml": "source: github:org/repo",
    });

    const config = await loadGlobalConfig();
    expect(config?.source).toBe("github:org/repo");
  });

  it("returns null for missing config", async () => {
    vol.fromJSON({});

    const config = await loadGlobalConfig();
    expect(config).toBeNull();
  });
});
```

### Testing Interactive Prompts

```typescript
import { describe, it, expect, vi } from "vitest";
import * as p from "@clack/prompts";

vi.mock("@clack/prompts", () => ({
  select: vi.fn(),
  confirm: vi.fn(),
  spinner: vi.fn(() => ({
    start: vi.fn(),
    stop: vi.fn(),
  })),
  isCancel: vi.fn((value) => value === Symbol.for("cancel")),
  intro: vi.fn(),
  outro: vi.fn(),
  log: {
    info: vi.fn(),
    error: vi.fn(),
    success: vi.fn(),
  },
}));

describe("wizard flow", () => {
  it("handles user cancellation", async () => {
    vi.mocked(p.select).mockResolvedValueOnce(Symbol.for("cancel"));

    const result = await runWizard();

    expect(result).toBeNull();
  });

  it("completes selection flow", async () => {
    vi.mocked(p.select)
      .mockResolvedValueOnce("scratch")
      .mockResolvedValueOnce("item1")
      .mockResolvedValueOnce("__continue__")
      .mockResolvedValueOnce("confirm");

    const result = await runWizard();

    expect(result?.selectedItems).toContain("item1");
  });
});
```

</testing>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Missing `p.isCancel()` checks after prompts - causes undefined behavior on Ctrl+C
- Using magic numbers for exit codes - makes debugging impossible
- Not handling SIGINT - leaves processes in unknown state
- Synchronous file operations blocking the event loop

**Medium Priority Issues:**

- Missing spinner feedback for operations > 500ms
- Not using `parseAsync()` for async actions - swallows errors
- Inconsistent error message formatting
- Missing `--help` descriptions for options

**Common Mistakes:**

- Forgetting to call `process.exit()` after `p.cancel()` - execution continues
- Not validating early - errors occur deep in flow
- Mixing sync and async patterns - leads to race conditions
- Not cleaning up on errors (spinners left running)

**Gotchas & Edge Cases:**

- Commander converts `--my-option` to `myOption` in camelCase
- `optsWithGlobals()` needed to access parent command options
- Spinner must be stopped before any console output
- YAML parsing can throw - always wrap in try/catch
- `process.exit()` in async context may not wait for cleanup

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST handle SIGINT (Ctrl+C) gracefully and exit with appropriate codes)**

**(You MUST use `p.isCancel()` to detect cancellation in ALL @clack/prompts and handle gracefully)**

**(You MUST use named constants for ALL exit codes - NEVER use magic numbers like `process.exit(1)`)**

**(You MUST use `parseAsync()` for async actions to properly propagate errors)**

**Failure to follow these rules will result in poor UX, orphaned processes, and debugging nightmares.**

</critical_reminders>
