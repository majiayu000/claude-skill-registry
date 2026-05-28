---
name: typescript-hook-writer
description: Expert guidance for developing Claude Code hooks in TypeScript with shared utilities, esbuild compilation, and Vitest testing - distributes compiled JS while maintaining TypeScript development experience
---

# TypeScript Hook Writer

Use this skill when developing Claude Code hooks in TypeScript. This skill ensures you maintain type safety, shared utilities, proper build pipeline, and comprehensive testing while distributing single-file JavaScript bundles to users.

## When to Use This Skill

- Creating new TypeScript hooks for Claude Code
- Setting up the hooks development environment
- Adding shared utilities for hooks
- Writing tests for hooks with Vitest
- Building hooks for distribution
- Publishing TypeScript-based hooks as PRPM packages

## Why TypeScript for Hooks?

**Advantages over bash:**
- Type safety catches errors at compile time
- Shared utility functions reduce code duplication
- Better IDE support with autocomplete and refactoring
- Easier to test with Vitest
- More readable for complex logic
- Strong validation with TypeScript interfaces

**Trade-offs:**
- Requires build step (esbuild)
- Slightly larger bundle size (~2-3KB vs bash)
- Users still just need Node.js (no TypeScript dependency)

**When to use TypeScript hooks:**
- Complex input validation or pattern matching
- Hooks that share common logic
- Hooks requiring automated testing
- Teams familiar with TypeScript

**When to stick with bash:**
- Simple one-off hooks (< 20 lines)
- Hooks that just call other CLI tools
- Extreme performance requirements (though difference is negligible)

## Project Structure

```
packages/hooks/
├── package.json              # Build tooling (esbuild, tsx, vitest)
├── tsconfig.json             # TypeScript configuration
├── vitest.config.ts          # Test configuration
├── scripts/
│   └── build-all-hooks.ts    # Build script (compiles all hooks)
├── shared/
│   ├── types.ts              # Shared TypeScript interfaces
│   ├── hook-utils.ts         # Shared utility functions
│   └── hook-utils.test.ts    # Tests for shared utilities

# Each hook lives in .claude/hooks/
.claude/hooks/
├── my-hook/
│   ├── hook.json             # Hook configuration
│   ├── README.md             # Documentation
│   ├── src/
│   │   ├── hook.ts           # TypeScript source (development)
│   │   ├── hook.test.ts      # Vitest tests
│   │   ├── hook-utils.ts     # Copied shared utilities
│   │   └── types.ts          # Copied shared types
│   └── dist/
│       └── hook.js           # Compiled bundle (distributed)
```

## Setup: packages/hooks Infrastructure

### 1. package.json

```json
{
  "name": "@prpm/hooks",
  "version": "1.0.0",
  "description": "Build system and shared utilities for PRPM Claude Code hooks",
  "private": true,
  "type": "module",
  "scripts": {
    "build": "tsx scripts/build-all-hooks.ts",
    "build:watch": "tsx scripts/build-all-hooks.ts --watch",
    "test": "vitest",
    "test:watch": "vitest --watch",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "esbuild": "^0.19.8",
    "tsx": "^4.7.0",
    "typescript": "^5.3.3",
    "vitest": "^1.0.4"
  }
}
```

### 2. tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "lib": ["ES2022"],
    "moduleResolution": "node",
    "esModuleInterop": true,
    "strict": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "types": ["node"]
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

### 3. vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['**/*.test.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.test.ts',
        '**/scripts/**',
      ],
    },
  },
});
```

### 4. Build Script: scripts/build-all-hooks.ts

```typescript
#!/usr/bin/env tsx
/**
 * Build script for compiling all Claude Code hooks to standalone JavaScript bundles
 */

import { build, BuildOptions } from 'esbuild';
import { readdirSync, statSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Root directory is app/ which is 3 levels up from packages/hooks/scripts/
const ROOT_DIR = join(__dirname, '../../..');
const HOOKS_DIR = join(ROOT_DIR, '.claude/hooks');

interface HookInfo {
  name: string;
  srcPath: string;
  distPath: string;
}

/**
 * Find all hooks with TypeScript source files
 */
function findHooks(): HookInfo[] {
  const hooks: HookInfo[] = [];

  if (!existsSync(HOOKS_DIR)) {
    console.error(`Hooks directory not found: ${HOOKS_DIR}`);
    return hooks;
  }

  const entries = readdirSync(HOOKS_DIR);

  for (const entry of entries) {
    const hookPath = join(HOOKS_DIR, entry);

    // Skip non-directories and special directories
    if (!statSync(hookPath).isDirectory() || entry === 'shared') {
      continue;
    }

    const srcPath = join(hookPath, 'src/hook.ts');
    const distPath = join(hookPath, 'dist/hook.js');

    if (existsSync(srcPath)) {
      hooks.push({
        name: entry,
        srcPath,
        distPath,
      });
    }
  }

  return hooks;
}

/**
 * Build a single hook
 */
async function buildHook(hook: HookInfo): Promise<void> {
  const buildOptions: BuildOptions = {
    entryPoints: [hook.srcPath],
    bundle: true,
    platform: 'node',
    target: 'node18',
    outfile: hook.distPath,
    format: 'cjs',
    minify: false, // Keep readable for debugging
    sourcemap: false,
    logLevel: 'error',
    banner: {
      js: '#!/usr/bin/env node',
    },
  };

  try {
    // Ensure dist directory exists
    const distDir = dirname(hook.distPath);
    if (!existsSync(distDir)) {
      mkdirSync(distDir, { recursive: true });
    }

    await build(buildOptions);
    console.log(`✓ Built ${hook.name}`);

    // Make the output file executable
    const { chmodSync } = await import('fs');
    chmodSync(hook.distPath, 0o755);
  } catch (error) {
    console.error(`✗ Failed to build ${hook.name}:`, error);
    throw error;
  }
}

/**
 * Build all hooks
 */
async function buildAll(watch: boolean = false): Promise<void> {
  console.log('🔨 Building PRPM Claude Code hooks...\n');

  const hooks = findHooks();

  if (hooks.length === 0) {
    console.log('No hooks found to build.');
    return;
  }

  console.log(`Found ${hooks.length} hooks:\n`);

  // Build all hooks in parallel
  try {
    await Promise.all(hooks.map(hook => buildHook(hook)));
    console.log(`\n✓ Built ${hooks.length} hooks successfully`);
  } catch (error) {
    console.error('\n✗ Build failed');
    process.exit(1);
  }

  if (watch) {
    console.log('\n👀 Watching for changes...');
    console.log('⚠️  Watch mode not yet implemented. Run `npm run build` after changes.');
  }
}

// Parse command line args
const args = process.argv.slice(2);
const watch = args.includes('--watch') || args.includes('-w');

// Run build
buildAll(watch).catch(error => {
  console.error('Build error:', error);
  process.exit(1);
});
```

## Shared Utilities Pattern

### Why Copy Instead of Import?

Each hook gets its own copy of shared utilities rather than importing from a shared package:

**Benefits:**
- Each hook is a standalone single-file bundle
- No external dependencies at runtime
- Simpler distribution (just one .js file)
- No module resolution issues
- Each hook can be updated independently

**Trade-off:**
- Slight code duplication (~1-2KB per hook)
- Changes to shared utilities require rebuilding all hooks

### shared/types.ts

Define TypeScript interfaces for hook input, exit codes, and options:

```typescript
/**
 * Shared TypeScript types for Claude Code hooks
 */

export interface HookInput {
  session_id?: string;
  transcript_path?: string;
  current_dir?: string;
  input?: {
    file_path?: string;
    command?: string;
    content?: string;
    old_string?: string;
    new_string?: string;
    [key: string]: any;
  };
  message?: string;
  tool?: string;
  [key: string]: any;
}

export enum HookExitCode {
  Success = 0,    // Continue operation
  Error = 1,      // Log error but continue
  Block = 2,      // Block operation (PreToolUse only)
}

export interface ExecOptions {
  skipOnMissing?: boolean;  // Exit successfully if command not found
  background?: boolean;     // Run in background (don't wait)
  timeout?: number;         // Timeout in milliseconds
  env?: Record<string, string>; // Environment variables
}

export interface PatternMatch {
  matched: boolean;
  pattern?: string;
}
```

### shared/hook-utils.ts

Common utility functions used across hooks:

```typescript
import { readFileSync, appendFileSync, existsSync } from 'fs';
import { execSync } from 'child_process';
import type { HookInput, HookExitCode, ExecOptions, PatternMatch } from './types';

/**
 * Read and parse JSON from stdin
 */
export function readStdin(): HookInput {
  try {
    const input = readFileSync(0, 'utf-8');
    return JSON.parse(input);
  } catch (error) {
    return {};
  }
}

/**
 * Extract file path from hook input
 */
export function getFilePath(input: HookInput): string | undefined {
  return input.input?.file_path;
}

/**
 * Extract command from hook input
 */
export function getCommand(input: HookInput): string | undefined {
  return input.input?.command;
}

/**
 * Extract content from hook input
 */
export function getContent(input: HookInput): string | undefined {
  return input.input?.content || input.input?.new_string;
}

/**
 * Check if file has one of the specified extensions
 */
export function hasExtension(filePath: string, extensions: string[]): boolean {
  return extensions.some(ext => filePath.endsWith(ext));
}

/**
 * Check if a command exists in PATH
 */
export function commandExists(command: string): boolean {
  try {
    execSync(`command -v ${command}`, { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

/**
 * Execute a command with options
 */
export function execCommand(
  command: string,
  args: string[],
  options: ExecOptions = {}
): void {
  // Check if command exists if skipOnMissing is true
  if (options.skipOnMissing && !commandExists(command)) {
    return;
  }

  const fullCommand = `${command} ${args.map(arg => `"${arg}"`).join(' ')}`;

  if (options.background) {
    // Run in background - don't wait for completion
    execSync(`(${fullCommand} &)`, {
      stdio: 'ignore',
      timeout: options.timeout,
      env: { ...process.env, ...options.env },
    });
  } else {
    // Run synchronously
    execSync(fullCommand, {
      stdio: 'inherit',
      timeout: options.timeout,
      env: { ...process.env, ...options.env },
    });
  }
}

/**
 * Match file path against glob patterns
 */
export function matchesPattern(filePath: string, patterns: string[]): PatternMatch {
  for (const pattern of patterns) {
    // Convert glob pattern to regex
    const regexPattern = pattern
      .replace(/\./g, '\\.')
      .replace(/\*/g, '.*')
      .replace(/\?/g, '.');

    if (new RegExp(`^${regexPattern}$`).test(filePath)) {
      return { matched: true, pattern };
    }
  }

  return { matched: false };
}

/**
 * Append line to log file
 */
export function appendToLog(logFile: string, line: string): void {
  try {
    appendFileSync(logFile, line + '\n', 'utf-8');
  } catch {
    // Fail silently
  }
}

/**
 * Get current timestamp in YYYY-MM-DD HH:MM:SS format
 */
export function getTimestamp(): string {
  return new Date().toISOString().replace('T', ' ').substring(0, 19);
}

/**
 * Log error message to stderr
 */
export function logError(message: string): void {
  console.error(message);
}

/**
 * Log warning message to stderr
 */
export function logWarning(message: string): void {
  console.error(message);
}

/**
 * Exit hook with specified code
 */
export function exitHook(code: HookExitCode): never {
  process.exit(code);
}

// Re-export HookExitCode for convenience
export { HookExitCode } from './types';
```

## Creating a TypeScript Hook

### Step 1: Create Hook Directory Structure

```bash
mkdir -p .claude/hooks/my-hook/src
mkdir -p .claude/hooks/my-hook/dist
```

### Step 2: Copy Shared Utilities

Copy `shared/types.ts` and `shared/hook-utils.ts` into the hook's `src/` directory:

```bash
cp packages/hooks/shared/types.ts .claude/hooks/my-hook/src/
cp packages/hooks/shared/hook-utils.ts .claude/hooks/my-hook/src/
```

**Why copy instead of symlink?** Each hook becomes a standalone bundle when compiled. The build process bundles utilities into the final .js file.

### Step 3: Write Hook Implementation

`.claude/hooks/my-hook/src/hook.ts`:

```typescript
#!/usr/bin/env tsx
/**
 * My Hook
 * Description of what this hook does
 */

import {
  readStdin,
  getFilePath,
  hasExtension,
  execCommand,
  logError,
  logWarning,
  exitHook,
  HookExitCode,
} from './hook-utils';

async function main() {
  // Read input from stdin
  const input = readStdin();

  // Extract file path
  const filePath = getFilePath(input);
  if (!filePath) {
    exitHook(HookExitCode.Success);
  }

  // Validate file extension
  const supportedExtensions = ['.ts', '.tsx', '.js', '.jsx'];
  if (!hasExtension(filePath, supportedExtensions)) {
    exitHook(HookExitCode.Success);
  }

  // Perform hook action
  try {
    execCommand('prettier', ['--write', filePath], {
      skipOnMissing: true,
      background: true,
    });

    exitHook(HookExitCode.Success);
  } catch (error) {
    logError(`Failed to format ${filePath}: ${error}`);
    exitHook(HookExitCode.Error);
  }
}

main().catch(() => {
  exitHook(HookExitCode.Success); // Don't block on errors
});
```

### Step 4: Create hook.json Configuration

`.claude/hooks/my-hook/hook.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "node .claude/hooks/my-hook/dist/hook.js",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

**Important:** Reference `dist/hook.js` (compiled), not `src/hook.ts` (source).

### Step 4.5: Advanced Hook Configuration (Optional)

All hook types support optional fields for controlling execution behavior:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "node .claude/hooks/my-hook/dist/hook.js",
        "timeout": 5000,
        "continue": true,              // Whether Claude continues after hook (default: true)
        "stopReason": "string",        // Message shown when continue is false
        "suppressOutput": false,       // Hide stdout from transcript (default: false)
        "systemMessage": "string"      // Warning message shown to user
      }]
    }]
  }
}
```

#### `continue` (boolean, default: true)

Controls whether Claude continues after hook execution.

**When to use `false`:**
- Security hooks that must block operations
- Validation hooks that found critical errors
- Hooks that require user intervention

```json
{
  "type": "command",
  "command": "node .claude/hooks/security-validator/dist/hook.js",
  "continue": false,
  "stopReason": "Security validation failed. Please review the detected issues before proceeding."
}
```

**Exit code interaction:**
- If hook exits with `HookExitCode.Block` (2): `continue` is ignored, operation is blocked
- If hook exits with `HookExitCode.Success` (0) or `HookExitCode.Error` (1): `continue` field determines behavior

#### `stopReason` (string)

Message displayed to user when `continue: false`. Should explain why execution stopped and what action is needed.

```json
{
  "continue": false,
  "stopReason": "Pre-commit checks failed. Fix linting errors and try again."
}
```

#### `suppressOutput` (boolean, default: false)

Hides hook stdout from transcript mode (Ctrl-R). Stderr is always shown.

**When to use `true`:**
- Hooks that produce verbose output
- Debugging logs not useful to users
- Noisy background operations

```json
{
  "type": "command",
  "command": "node .claude/hooks/cloud-sync/dist/hook.js",
  "suppressOutput": true  // Don't show sync progress in transcript
}
```

**Note:** Always show critical errors via stderr (use `logError()`), as stderr is never suppressed.

#### `systemMessage` (string)

Warning or info message shown to user when hook executes. Useful for non-blocking warnings.

**TypeScript example:**

```typescript
// In your hook.ts
if (outdatedDeps.length > 0) {
  logWarning(`Found ${outdatedDeps.length} outdated dependencies`);
  // systemMessage in hook.json will also show to user
}
```

```json
{
  "type": "command",
  "command": "node .claude/hooks/dependency-checker/dist/hook.js",
  "systemMessage": "⚠️  Some dependencies are outdated. Consider running 'npm update'."
}
```

**Difference from `stopReason`:**
- `systemMessage`: Informational, Claude continues
- `stopReason`: Critical, requires `continue: false`

### Step 5: Build the Hook

```bash
cd packages/hooks
pnpm build
```

Output:
```
🔨 Building PRPM Claude Code hooks...

Found 1 hooks:

✓ Built my-hook

✓ Built 1 hooks successfully
```

The compiled hook is now at `.claude/hooks/my-hook/dist/hook.js` (~2-3KB single file).

## Testing TypeScript Hooks

### Step 1: Create Test File

`.claude/hooks/my-hook/src/hook.test.ts`:

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock the hook-utils module
vi.mock('./hook-utils', () => ({
  readStdin: vi.fn(),
  getFilePath: vi.fn(),
  hasExtension: vi.fn(),
  execCommand: vi.fn(),
  logError: vi.fn(),
  exitHook: vi.fn((code: number) => {
    throw new Error(`EXIT_${code}`);
  }),
  HookExitCode: {
    Success: 0,
    Error: 1,
    Block: 2,
  },
}));

describe('my-hook', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should exit successfully if no file path is provided', async () => {
    const { readStdin, getFilePath, exitHook, HookExitCode } = await import('./hook-utils');

    vi.mocked(readStdin).mockReturnValue({});
    vi.mocked(getFilePath).mockReturnValue(undefined);

    try {
      await import('./hook');
    } catch (error: any) {
      expect(error.message).toBe('EXIT_0');
    }

    expect(exitHook).toHaveBeenCalledWith(HookExitCode.Success);
  });

  it('should format supported file types', async () => {
    const { readStdin, getFilePath, hasExtension, execCommand, exitHook, HookExitCode } = await import('./hook-utils');

    vi.mocked(readStdin).mockReturnValue({
      input: { file_path: '/path/to/file.ts' },
    });
    vi.mocked(getFilePath).mockReturnValue('/path/to/file.ts');
    vi.mocked(hasExtension).mockReturnValue(true);

    try {
      await import('./hook');
    } catch (error: any) {
      expect(error.message).toBe('EXIT_0');
    }

    expect(execCommand).toHaveBeenCalledWith(
      'prettier',
      ['--write', '/path/to/file.ts'],
      expect.objectContaining({ background: true })
    );
  });

  it('should skip unsupported file types', async () => {
    const { readStdin, getFilePath, hasExtension, execCommand, exitHook } = await import('./hook-utils');

    vi.mocked(readStdin).mockReturnValue({
      input: { file_path: '/path/to/file.py' },
    });
    vi.mocked(getFilePath).mockReturnValue('/path/to/file.py');
    vi.mocked(hasExtension).mockReturnValue(false);

    try {
      await import('./hook');
    } catch (error: any) {
      // Expected exit
    }

    expect(execCommand).not.toHaveBeenCalled();
  });
});
```

### Step 2: Run Tests

```bash
cd packages/hooks
pnpm test:run
```

Output:
```
✓ .claude/hooks/my-hook/src/hook.test.ts (3 tests) 5ms

Test Files  1 passed (1)
Tests  3 passed (3)
Duration  182ms
```

### Step 3: Run Tests with Coverage

```bash
pnpm test:coverage
```

Coverage report shows which code paths are tested.

## Build Workflow: TypeScript → JavaScript

### Development vs Distribution

**Development files (NOT distributed):**
- `.claude/hooks/my-hook/src/hook.ts` - TypeScript source
- `.claude/hooks/my-hook/src/hook.test.ts` - Tests
- `.claude/hooks/my-hook/src/types.ts` - Type definitions
- `.claude/hooks/my-hook/src/hook-utils.ts` - Utilities

**Distribution files (what users get):**
- `.claude/hooks/my-hook/dist/hook.js` - Compiled JavaScript bundle (~2-3KB)
- `.claude/hooks/my-hook/hook.json` - Hook configuration
- `.claude/hooks/my-hook/README.md` - Documentation

### Build Process

The build script (`packages/hooks/scripts/build-all-hooks.ts`) does the following:

1. **Scans** `.claude/hooks/` for directories with `src/hook.ts`
2. **Compiles** each hook with esbuild:
   - Bundles all imports into single file
   - Converts TypeScript to JavaScript
   - Targets Node.js 18+
   - Outputs CommonJS format
   - Adds `#!/usr/bin/env node` shebang
3. **Outputs** to `dist/hook.js` in each hook directory
4. **Sets permissions** to make file executable (`chmod +x`)

### When to Build

**Automatic build:**
- Publishing with `prpm publish` - `prepublishOnly` script builds automatically (if configured)

**Manual build for:**
- Testing hook locally before committing
- Debugging compiled output
- Verifying build succeeds before pushing

**How to build manually:**

```bash
# Build all hooks once
cd packages/hooks
pnpm build

# Output:
# 🔨 Building PRPM Claude Code hooks...
# Found 7 hooks:
# ✓ Built prettier-on-save
# ✓ Built command-logger
# ...
# ✓ Built 7 hooks successfully
```

**Build output structure:**

```
.claude/hooks/my-hook/
├── src/
│   ├── hook.ts           ← TypeScript source (input)
│   ├── hook-utils.ts
│   └── types.ts
└── dist/
    └── hook.js           ← Compiled JavaScript (output)
```

**What gets bundled:**

esbuild traces all imports and bundles them into a single `dist/hook.js`:

```typescript
// src/hook.ts imports these
import { readStdin, getFilePath } from './hook-utils';
import { HookExitCode } from './types';

// dist/hook.js contains:
// - All code from hook.ts
// - All code from hook-utils.ts
// - All type definitions (compiled to runtime checks)
// - No external dependencies
// - Total size: ~2-3KB
```

**Why this approach:**

- ✅ Users don't need TypeScript or build tools
- ✅ Single-file distribution is simple
- ✅ No runtime dependencies (just Node.js)
- ✅ Hooks load instantly (no module resolution)
- ✅ Each hook is independent

## Publishing TypeScript Hooks as PRPM Packages

### Step 1: Build Hooks

**IMPORTANT:** Always build before updating prpm.json or publishing:

```bash
cd packages/hooks
pnpm build
```

Verify dist files exist:

```bash
ls -lh .claude/hooks/*/dist/hook.js
# Should show compiled hooks with ~2-3KB size each
```

### Step 2: Update prpm.json

Add the hook to the root `prpm.json`:

```json
{
  "packages": [
    {
      "name": "my-hook",
      "version": "1.0.0",
      "description": "Brief description of what the hook does",
      "format": "claude",
      "subtype": "hook",
      "tags": ["formatting", "automation", "typescript"],
      "files": [
        ".claude/hooks/my-hook/hook.json",
        ".claude/hooks/my-hook/dist/hook.js",
        ".claude/hooks/my-hook/README.md"
      ]
    }
  ]
}
```

**Important files array:**
- `hook.json` - Hook configuration
- `dist/hook.js` - Compiled JavaScript (NOT src/hook.ts)
- `README.md` - Documentation

**Do NOT include:**
- `src/` directory (source code)
- `*.test.ts` files
- `node_modules/`
- Development files

### Step 2: Create README.md

`.claude/hooks/my-hook/README.md`:

```markdown
# My Hook

Brief description of what this hook does.

## What It Does

- Automatically formats code after Claude edits files
- Supports TypeScript, JavaScript, JSON, and Markdown
- Runs in background (non-blocking)
- Gracefully skips if Prettier not installed

## Installation

```bash
prpm install @prpm/my-hook
```

## Requirements

- Node.js 18+ (already required for Claude Code)
- Prettier (optional): `npm install -g prettier`

## Configuration

This hook activates on `PostToolUse` for `Edit` and `Write` tools.

To customize supported file extensions, fork and modify the source.

## Examples

When Claude writes a TypeScript file:
```
Claude: I'll create a new component...
[Hook auto-formats component.tsx with Prettier]
```

## Troubleshooting

**Hook not running?**
- Check `.claude/settings.json` includes the hook
- Verify `dist/hook.js` exists and is executable
- Check transcript (Ctrl-R) for hook errors

**Format not applying?**
- Ensure Prettier is installed: `prettier --version`
- Check Prettier config in project (`.prettierrc`)
```

### Step 3: Set Up Automatic Build Before Publishing

**Good news:** PRPM now supports `prepublishOnly` scripts! Add this to your prpm.json:

```json
{
  "name": "prpm-packages",
  "license": "MIT",
  "repository": "https://github.com/username/repo",
  "scripts": {
    "prepublishOnly": "cd packages/hooks && npm run build"
  },
  "packages": [
    // ... your packages
  ]
}
```

**What happens:**
- When you run `prpm publish`, the `prepublishOnly` script runs automatically
- Hooks are compiled from TypeScript to JavaScript
- If the build fails, publish is aborted (prevents publishing broken code)
- If the build succeeds, publishing continues with up-to-date dist files

**Manual build (for local testing):**

```bash
cd packages/hooks
npm run build
```

Verify `dist/hook.js` files exist:

```bash
ls -lh .claude/hooks/*/dist/hook.js
# Should show compiled hooks with ~2-3KB size each
```

### Step 4: Publish

```bash
# From project root
prpm publish
```

**What happens automatically:**
1. `prepublishOnly` script runs: `cd packages/hooks && npm run build`
2. All hooks are compiled to dist/hook.js
3. Packages are published with up-to-date compiled files

**Users will receive:**
- `hook.json` - Configuration
- `dist/hook.js` - Single-file executable (~2-3KB)
- `README.md` - Documentation

**Users do NOT get:**
- TypeScript source (src/ directory)
- Build tooling
- Tests

**Why this matters:** The prepublishOnly script prevents publishing stale dist files. If you modify a hook's TypeScript source but forget to build, the build happens automatically before publish.

## Best Practices

### 1. Keep Hooks Fast

Target < 100ms execution time. Use background execution for slow operations:

```typescript
// BAD - blocks for 5 seconds
execCommand('npm', ['test']);

// GOOD - runs in background
execCommand('npm', ['test'], { background: true });
```

### 2. Fail Gracefully

Never crash. Handle missing tools:

```typescript
execCommand('prettier', ['--write', filePath], {
  skipOnMissing: true,  // Exit successfully if prettier not found
  background: true,
});
```

### 3. Use Type Guards

Validate input shape:

```typescript
function isValidInput(input: HookInput): boolean {
  return !!(input.input?.file_path && typeof input.input.file_path === 'string');
}

if (!isValidInput(input)) {
  exitHook(HookExitCode.Success);
}
```

### 4. Copy Shared Utilities

Always copy (not import) shared utilities into each hook's `src/` directory:

```bash
cp packages/hooks/shared/{types.ts,hook-utils.ts} .claude/hooks/my-hook/src/
```

This ensures standalone compilation.

### 5. Test Edge Cases

Test with edge cases:

```typescript
it('should handle files with spaces', async () => {
  const input = { input: { file_path: '/path/my file.ts' } };
  // ...
});

it('should handle Unicode filenames', async () => {
  const input = { input: { file_path: '/path/文件.ts' } };
  // ...
});

it('should handle missing input fields', async () => {
  const input = { input: {} };
  // ...
});
```

### 6. Use Descriptive Exit Codes

```typescript
// Success - continue operation
exitHook(HookExitCode.Success);

// Block - prevent operation (PreToolUse only)
exitHook(HookExitCode.Block);

// Error - log but continue
exitHook(HookExitCode.Error);
```

### 7. Log to stderr

```typescript
// WRONG - pollutes transcript
console.log('Processing file...');

// RIGHT - logs to stderr
logError('⚠️  Warning: something happened');
logWarning('ℹ️  Info: skipping file');
```

## Common Patterns

### Pattern: File Extension Filter

```typescript
const supportedExtensions = ['.ts', '.tsx', '.js', '.jsx'];

if (!hasExtension(filePath, supportedExtensions)) {
  exitHook(HookExitCode.Success);
}
```

### Pattern: Sensitive File Blocker

```typescript
const blockedPatterns = ['.env', '.env.*', '*.pem', '*.key', '*credentials*'];

const match = matchesPattern(filePath, blockedPatterns);
if (match.matched) {
  logError(`⛔ Blocked: Cannot modify sensitive file '${filePath}'`);
  logError(`   Pattern: ${match.pattern}`);
  exitHook(HookExitCode.Block);
}
```

### Pattern: Command Logger

```typescript
import { join } from 'path';
import { homedir } from 'os';

const command = getCommand(input);
if (!command) {
  exitHook(HookExitCode.Success);
}

const logFile = join(homedir(), '.claude-commands.log');
const logLine = `[${getTimestamp()}] ${command}`;

appendToLog(logFile, logLine);
exitHook(HookExitCode.Success);
```

### Pattern: Content Validator

```typescript
const content = getContent(input);
if (!content) {
  exitHook(HookExitCode.Success);
}

const dangerousPatterns = [
  /password\s*=\s*["'][^"']+["']/i,
  /api[_-]?key\s*=\s*["'][^"']+["']/i,
  /AKIA[0-9A-Z]{16}/, // AWS access key
];

for (const pattern of dangerousPatterns) {
  if (pattern.test(content)) {
    logWarning(`⚠️  Warning: Potential credential detected in ${filePath}`);
    logWarning(`   Pattern matched: ${pattern}`);
    break;
  }
}

exitHook(HookExitCode.Success);
```

## Debugging TypeScript Hooks

### 1. Test Compilation

```bash
cd packages/hooks
pnpm build
```

Check for TypeScript errors.

### 2. Test Execution Manually

```bash
echo '{"input":{"file_path":"/tmp/test.ts"}}' | node .claude/hooks/my-hook/dist/hook.js
echo $?  # Check exit code
```

### 3. Check Hook Registration

Verify hook appears in `.claude/settings.json`:

```bash
cat .claude/settings.json | jq '.hooks'
```

### 4. View Transcript

Run Claude Code and check transcript (Ctrl-R) for hook execution:

```
PostToolUse hook: my-hook
  command: node .claude/hooks/my-hook/dist/hook.js
  exit: 0
  duration: 47ms
```

### 5. Add Debug Logging

Temporarily add debug output:

```typescript
logError(`[DEBUG] Processing file: ${filePath}`);
logError(`[DEBUG] Extensions: ${JSON.stringify(supportedExtensions)}`);
```

## Migration: Bash to TypeScript

Converting an existing bash hook to TypeScript:

### Before (bash)

```bash
#!/bin/bash
set -euo pipefail

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.input.file_path // empty')

if [[ -z "$FILE" ]]; then
  exit 0
fi

if ! command -v prettier &>/dev/null; then
  exit 0
fi

prettier --write "$FILE" &
exit 0
```

### After (TypeScript)

```typescript
#!/usr/bin/env tsx
import {
  readStdin,
  getFilePath,
  execCommand,
  exitHook,
  HookExitCode,
} from './hook-utils';

async function main() {
  const input = readStdin();
  const filePath = getFilePath(input);

  if (!filePath) {
    exitHook(HookExitCode.Success);
  }

  execCommand('prettier', ['--write', filePath], {
    skipOnMissing: true,
    background: true,
  });

  exitHook(HookExitCode.Success);
}

main().catch(() => exitHook(HookExitCode.Success));
```

**Benefits:**
- Type safety for `input` object
- Shared utilities reduce code
- Easier to test
- Better IDE support

## Quick Reference

### Build Commands

```bash
pnpm build              # Build all hooks once
pnpm build:watch        # Watch mode (not yet implemented)
pnpm test               # Run tests in watch mode
pnpm test:run           # Run tests once
pnpm test:coverage      # Run tests with coverage
```

### Hook Configuration Fields

**Required:**
- `type` - "command" or "prompt"
- `command` - Path to compiled hook (e.g., "node .claude/hooks/my-hook/dist/hook.js")

**Optional:**
- `timeout` - Max execution time in ms (default: 60000)
- `continue` - Continue after hook? (default: true)
- `stopReason` - Message when continue=false
- `suppressOutput` - Hide stdout from transcript (default: false)
- `systemMessage` - Warning message to user

### Exit Codes (HookExitCode enum)

```typescript
HookExitCode.Success = 0    // Continue operation
HookExitCode.Error = 1      // Log error but continue
HookExitCode.Block = 2      // Block operation (PreToolUse only)
```

### Hook Structure Checklist

- [ ] Created `.claude/hooks/my-hook/src/hook.ts`
- [ ] Copied `types.ts` and `hook-utils.ts` to `src/`
- [ ] Created `hook.json` referencing `dist/hook.js`
- [ ] Created `README.md` with installation and usage
- [ ] Created `hook.test.ts` with test coverage
- [ ] Built hook with `pnpm build`
- [ ] Verified `dist/hook.js` exists and is executable
- [ ] Added to `prpm.json` with correct files array
- [ ] Tested manually with sample JSON input
- [ ] Tested in real Claude Code session

### prpm.json Files Array

**Include:**
- `.claude/hooks/my-hook/hook.json`
- `.claude/hooks/my-hook/dist/hook.js`
- `.claude/hooks/my-hook/README.md`

**Exclude:**
- `src/` directory
- `*.test.ts` files
- `node_modules/`
- Development files

### Common Utilities

```typescript
readStdin()                          // Parse stdin JSON
getFilePath(input)                   // Extract file path
getCommand(input)                    // Extract command
getContent(input)                    // Extract content
hasExtension(path, ['.ts', '.js'])   // Check extension
matchesPattern(path, ['*.env'])      // Glob matching
commandExists('prettier')            // Check command exists
execCommand('cmd', ['arg'], opts)    // Execute command
appendToLog(file, line)              // Append to log
getTimestamp()                       // Current timestamp
logError(msg)                        // Log to stderr
logWarning(msg)                      // Log warning
exitHook(HookExitCode.Success)       // Exit with code
```

## Resources

- [Claude Code Hooks Docs](https://code.claude.com/docs/en/hooks)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [esbuild Documentation](https://esbuild.github.io/)
- [Vitest Documentation](https://vitest.dev/)
- [PRPM Publishing Guide](https://prpm.dev/docs/publishing)
