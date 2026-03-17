---
name: sayt-ide
description: >
  How to write .vscode/tasks.json — build/test task schema, dependsOn chains,
  per-language examples (Gradle, Go, Node/pnpm, Python, Zig).
  Use when creating build tasks, test tasks, or fixing compilation/test failures.
user-invocable: false
---

# build / test — VS Code Tasks via vscode-task-runner

`sayt build` and `sayt test` delegate to vscode-task-runner (vtr), which reads `.vscode/tasks.json` and runs the tasks labeled "build" and "test" respectively.

## How It Works

1. `sayt build` runs `vtr build` which finds the task with `"label": "build"` in `.vscode/tasks.json`
2. `sayt test` runs `vtr test` which finds the task with `"label": "test"`
3. vtr resolves `dependsOn` chains and runs prerequisite tasks first
4. The commands execute as shell commands in the project directory

vtr is installed via uvx (Python) and is cached after `sayt setup` for offline use.

## `.vscode/tasks.json` Schema

Every tasks.json must have:
- `"version": "2.0.0"`
- A `tasks` array with at minimum a `"build"` and `"test"` task

### Required Task Structure

```json
{
  "label": "build",          // MUST be exactly "build" or "test"
  "type": "shell",           // MUST be "shell" for sayt compatibility
  "command": "...",           // The executable to run
  "args": ["..."],           // Arguments (optional)
  "group": {
    "kind": "build",         // "build" or "test"
    "isDefault": true        // Mark as default for the group
  },
  "problemMatcher": [],      // VS Code error matching (can be empty)
  "dependsOn": ["..."]       // Prerequisite tasks (optional)
}
```

### Windows Support

Add a `windows` override for cross-platform commands:

```json
{
  "label": "build",
  "type": "shell",
  "command": "./gradlew",
  "windows": { "command": ".\\gradlew.bat" },
  "args": ["assemble"]
}
```

### Task Dependencies

Use `dependsOn` to run prerequisite tasks:

```json
{
  "label": "build",
  "type": "shell",
  "command": "go",
  "args": ["build", "-o", "app"],
  "dependsOn": ["sqlc-generate", "buf-generate"]
}
```

Dependency tasks don't need `isDefault: true` but should still be in the tasks array.

## Per-Language Examples

### Kotlin/Java (Gradle)

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build",
      "type": "shell",
      "command": "./gradlew",
      "windows": { "command": ".\\gradlew.bat" },
      "args": ["assemble"],
      "problemMatcher": [],
      "group": { "kind": "build", "isDefault": true }
    },
    {
      "label": "test",
      "type": "shell",
      "command": "./gradlew",
      "windows": { "command": ".\\gradlew.bat" },
      "args": ["test"],
      "group": { "kind": "test", "isDefault": true },
      "problemMatcher": []
    }
  ]
}
```

### Go

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build",
      "type": "shell",
      "command": "go",
      "args": ["build", "-o", "app"],
      "group": { "kind": "build", "isDefault": true },
      "dependsOn": ["sqlc-generate", "buf-generate"],
      "problemMatcher": []
    },
    {
      "label": "sqlc-generate",
      "type": "shell",
      "command": "sqlc",
      "args": ["generate"],
      "group": { "kind": "build" },
      "problemMatcher": []
    },
    {
      "label": "buf-generate",
      "type": "shell",
      "command": "buf",
      "args": ["generate", "../../libraries/xproto", "--template", "../../libraries/xproto/buf.go.gen.yaml", "-o", "../../libraries/xproto"],
      "group": { "kind": "build" },
      "problemMatcher": []
    },
    {
      "label": "test",
      "type": "shell",
      "command": "go",
      "args": ["run", "gotest.tools/gotestsum@v1.12.0", "-f", "github-actions", "--", "./...", "-tags=unit_test"],
      "group": { "kind": "test", "isDefault": true },
      "problemMatcher": []
    }
  ]
}
```

### Node.js / pnpm (monorepo with Turbo)

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "install",
      "type": "shell",
      "command": "pnpm install --frozen-lockfile"
    },
    {
      "label": "build",
      "type": "shell",
      "command": "pnpm -C ../.. exec turbo --filter ./guis/web assemble",
      "problemMatcher": ["$tsc"],
      "group": { "kind": "build", "isDefault": true },
      "dependsOn": ["install"]
    },
    {
      "label": "test",
      "type": "shell",
      "command": "pnpm -C ../.. exec turbo --filter ./guis/web test",
      "group": { "kind": "test", "isDefault": true },
      "problemMatcher": ["$tsc"],
      "dependsOn": ["install"]
    }
  ]
}
```

### Node.js / pnpm (standalone)

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build",
      "type": "shell",
      "command": "pnpm",
      "args": ["build"],
      "group": { "kind": "build", "isDefault": true },
      "problemMatcher": ["$tsc"]
    },
    {
      "label": "test",
      "type": "shell",
      "command": "pnpm",
      "args": ["test"],
      "group": { "kind": "test", "isDefault": true },
      "problemMatcher": []
    }
  ]
}
```

### Python

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build",
      "type": "shell",
      "command": "python",
      "args": ["-m", "build"],
      "group": { "kind": "build", "isDefault": true },
      "problemMatcher": []
    },
    {
      "label": "test",
      "type": "shell",
      "command": "pytest",
      "group": { "kind": "test", "isDefault": true },
      "problemMatcher": []
    }
  ]
}
```

### Zig

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build",
      "type": "shell",
      "command": "zig",
      "args": ["build"],
      "group": { "kind": "build", "isDefault": true },
      "problemMatcher": []
    },
    {
      "label": "test",
      "type": "shell",
      "command": "zig",
      "args": ["build", "test"],
      "group": { "kind": "test", "isDefault": true },
      "problemMatcher": []
    }
  ]
}
```

## Writing Good Tasks

1. **Label exactly "build" and "test"** — vtr looks for these exact labels
2. **Use `"type": "shell"`** — Required for sayt/vtr compatibility
3. **Set `isDefault: true`** — Mark one build and one test task as default
4. **Use `dependsOn`** — For code generation or install steps that must run first
5. **Add `problemMatcher`** — Helps VS Code parse errors (use `["$tsc"]` for TypeScript, `[]` otherwise)
6. **Add `windows` overrides** — If the command differs on Windows (e.g., `gradlew` vs `gradlew.bat`)
7. **Keep it simple** — The task should run the same command you'd type in the terminal

## Interpreting Results

- **Build success**: The underlying compiler/bundler exited 0
- **Build failure**: Read the compiler output — fix the source code
- **Test success**: All unit tests passed
- **Test failure**: Read test output for assertion failures and stack traces
- **"command not found: vtr"**: Run `pipx install vscode-task-runner` or `sayt setup`

## Current flags

!`sayt help build 2>&1 || true`
!`sayt help test 2>&1 || true`
